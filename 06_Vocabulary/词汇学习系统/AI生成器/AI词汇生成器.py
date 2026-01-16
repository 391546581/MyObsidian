#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI驱动的雅思词汇笔记自动生成器
支持: LLM自动生成内容 + AI图片记忆 + 批量处理
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import requests
from typing import Dict, List, Optional

class AIVocabularyGenerator:
    """AI词汇笔记生成器"""
    
    def __init__(self, api_key: str = None, api_base: str = None):
        """
        初始化生成器
        
        Args:
            api_key: LLM API密钥 (支持OpenAI/DeepSeek/Claude等)
            api_base: API基础URL (可选,用于自定义端点)
        """
        self.api_key = api_key or os.getenv('LLM_API_KEY')
        self.api_base = api_base or os.getenv('LLM_API_BASE', 'https://api.openai.com/v1')
        
        if not self.api_key:
            print("⚠️  未设置API密钥,将使用模板模式(无AI生成)")
            self.ai_enabled = False
        else:
            self.ai_enabled = True
            print(f"✅ AI模式已启用: {self.api_base}")
    
    def generate_vocabulary_note(
        self, 
        word: str, 
        brand: str = 'Brand7',
        theme: str = None,
        include_image: bool = True
    ) -> Dict:
        """
        生成完整的词汇笔记内容
        
        Args:
            word: 单词
            brand: 等级 (Brand5/7/9)
            theme: 主题 (教育/环境/科技等)
            include_image: 是否生成记忆图片
            
        Returns:
            包含所有笔记内容的字典
        """
        print(f"\n🔍 正在生成词汇笔记: {word} ({brand})")
        
        if self.ai_enabled:
            return self._generate_with_ai(word, brand, theme, include_image)
        else:
            return self._generate_with_template(word, brand, theme)
    
    def _generate_with_ai(
        self, 
        word: str, 
        brand: str, 
        theme: Optional[str],
        include_image: bool
    ) -> Dict:
        """使用AI生成词汇笔记"""
        
        # 构建提示词
        prompt = self._build_prompt(word, brand, theme)
        
        # 调用LLM API
        try:
            response = self._call_llm_api(prompt)
            note_data = self._parse_llm_response(response, word, brand)
            
            # 生成记忆图片
            if include_image:
                image_path = self._generate_memory_image(word, note_data.get('memory_tip', ''))
                note_data['image_path'] = image_path
            
            print(f"✅ AI生成完成: {word}")
            return note_data
            
        except Exception as e:
            print(f"❌ AI生成失败: {e}")
            print("⚠️  回退到模板模式")
            return self._generate_with_template(word, brand, theme)
    
    def _build_prompt(self, word: str, brand: str, theme: Optional[str]) -> str:
        """构建LLM提示词"""
        
        theme_context = f"主题: {theme}\n" if theme else ""
        
        prompt = f"""你是一位专业的雅思词汇教学专家。请为以下单词生成完整的学习笔记。

单词: {word}
等级: {brand}
{theme_context}
要求:
1. 提供精准的中文释义和英文释义
2. 给出音标(IPA格式)
3. 列出3-5个同义词,并按Brand5/7/9分级
4. 提供3个固定搭配,每个搭配配一个雅思真题级别的例句
5. 创建5个不同类型的复习卡片:
   - 卡片1: 基础释义
   - 卡片2: 固定搭配填空
   - 卡片3: 同义词辨析
   - 卡片4: 写作应用(将基础句子提升到{brand}水平)
   - 卡片5: 口语应用(Part3问题回答)
6. 提供词根词缀记忆技巧
7. 标注适用场景和不适用场景
8. 给出3个真实例句(分别来自: 雅思写作范文、口语高分回答、学术文章)

请以JSON格式返回,包含以下字段:
{{
    "word": "单词",
    "phonetic": "音标",
    "pos": "词性",
    "cn_meaning": "中文释义",
    "en_definition": "英文释义",
    "synonyms": {{
        "brand5": ["同义词1", "同义词2"],
        "brand7": ["同义词1", "同义词2"],
        "brand9": ["同义词1", "同义词2"]
    }},
    "collocations": [
        {{"phrase": "搭配", "example": "例句", "translation": "中文翻译"}},
        ...
    ],
    "flashcards": [
        {{
            "title": "卡片标题",
            "question": "问题",
            "answer": "答案",
            "notes": "补充说明"
        }},
        ...
    ],
    "etymology": "词根词缀分析",
    "memory_tip": "记忆技巧",
    "usage_scenarios": {{
        "suitable": ["适用场景1", "适用场景2"],
        "unsuitable": ["不适用场景1", "不适用场景2"]
    }},
    "examples": [
        {{
            "sentence": "例句",
            "source": "来源",
            "translation": "中文翻译"
        }},
        ...
    ],
    "related_words": ["关联词1", "关联词2", "关联词3"]
}}

请确保内容专业、准确、适合雅思考试。"""
        
        return prompt
    
    def _call_llm_api(self, prompt: str, model: str = "gpt-4") -> str:
        """调用LLM API"""
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'messages': [
                {
                    'role': 'system',
                    'content': '你是一位专业的雅思词汇教学专家,擅长创建高质量的词汇学习笔记。'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(
            f'{self.api_base}/chat/completions',
            headers=headers,
            json=data,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        return result['choices'][0]['message']['content']
    
    def _parse_llm_response(self, response: str, word: str, brand: str) -> Dict:
        """解析LLM返回的JSON"""
        
        # 提取JSON部分
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            data = json.loads(json_str)
            data['brand'] = brand
            return data
        else:
            raise ValueError("无法解析LLM返回的JSON")
    
    def _generate_memory_image(self, word: str, memory_tip: str) -> str:
        """生成记忆图片"""
        
        print(f"  🎨 正在生成记忆图片: {word}")
        
        # 这里可以集成DALL-E、Stable Diffusion等图片生成API
        # 示例: 使用OpenAI DALL-E
        
        try:
            prompt = f"""Create a memorable visual mnemonic for the English word "{word}". 
The image should help students remember the word through visual association.
Memory tip: {memory_tip}

Style: Clean, educational, colorful illustration suitable for vocabulary learning."""
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'dall-e-3',
                'prompt': prompt,
                'n': 1,
                'size': '1024x1024',
                'quality': 'standard'
            }
            
            response = requests.post(
                f'{self.api_base}/images/generations',
                headers=headers,
                json=data,
                timeout=120
            )
            
            response.raise_for_status()
            result = response.json()
            
            image_url = result['data'][0]['url']
            
            # 下载图片
            image_path = self._download_image(image_url, word)
            print(f"  ✅ 图片已生成: {image_path}")
            
            return image_path
            
        except Exception as e:
            print(f"  ⚠️  图片生成失败: {e}")
            return None
    
    def _download_image(self, url: str, word: str) -> str:
        """下载图片到本地"""
        
        # 创建图片目录
        image_dir = Path('images/vocabulary')
        image_dir.mkdir(parents=True, exist_ok=True)
        
        # 下载图片
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 保存图片
        image_path = image_dir / f"{word}_memory.png"
        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        return str(image_path)
    
    def _generate_with_template(self, word: str, brand: str, theme: Optional[str]) -> Dict:
        """使用模板生成(无AI)"""
        
        return {
            'word': word,
            'brand': brand,
            'phonetic': '待补充',
            'pos': '待补充',
            'cn_meaning': '待补充',
            'en_definition': '待补充',
            'synonyms': {
                'brand5': [],
                'brand7': [],
                'brand9': []
            },
            'collocations': [],
            'flashcards': [],
            'etymology': '待补充',
            'memory_tip': '待补充',
            'usage_scenarios': {
                'suitable': [],
                'unsuitable': []
            },
            'examples': [],
            'related_words': []
        }
    
    def create_obsidian_note(self, note_data: Dict, output_dir: str = None) -> str:
        """创建Obsidian笔记文件"""
        
        word = note_data['word']
        brand = note_data['brand']
        
        # 默认输出目录
        if not output_dir:
            output_dir = f'06_Vocabulary/词汇学习系统/{brand}'
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 生成笔记内容
        note_content = self._format_obsidian_note(note_data)
        
        # 保存文件
        note_file = output_path / f"{word}.md"
        with open(note_file, 'w', encoding='utf-8') as f:
            f.write(note_content)
        
        print(f"✅ 笔记已创建: {note_file}")
        return str(note_file)
    
    def _format_obsidian_note(self, data: Dict) -> str:
        """格式化为Obsidian笔记"""
        
        word = data['word']
        brand = data['brand']
        
        # YAML frontmatter
        frontmatter = f"""---
sr-due: {self._get_future_date(4)}
sr-interval: 4
sr-ease: 270
tags: [IELTS/{brand}, 词汇/{data.get('pos', '待补充')}]
---

"""
        
        # 主标题
        content = f"# {word}\n\n"
        
        # 卡片1: 基础释义
        content += f"""## 卡片1: 基础释义 #card

**单词**: {word}  
**等级**: {brand}

**问**: {word} 的中文意思是?

**答**: {data.get('cn_meaning', '待补充')}

**英文释义**: {data.get('en_definition', '待补充')}

---

"""
        
        # 卡片2: 固定搭配
        if data.get('collocations'):
            content += "## 卡片2: 固定搭配 #card\n\n**问**: 用{word}完成搭配:\n\n"
            for i, coll in enumerate(data['collocations'][:3], 1):
                phrase = coll['phrase'].replace(word, '_____')
                content += f"{i}. {phrase}\n"
            
            content += "\n**答**:\n"
            for i, coll in enumerate(data['collocations'][:3], 1):
                content += f"{i}. {coll['phrase']}\n"
                content += f"   > {coll['example']}\n\n"
            
            content += "---\n\n"
        
        # 卡片3: 同义词辨析
        if data.get('synonyms'):
            syns = data['synonyms']
            content += f"""## 卡片3: 同义词分级 #card

**问**: {word} 的同义词有哪些?按Brand5/7/9分级

**答**:
- **Brand5**: {', '.join(syns.get('brand5', []))}
- **Brand7**: {', '.join(syns.get('brand7', []))}
- **Brand9**: {', '.join(syns.get('brand9', []))}

---

"""
        
        # 卡片4: 写作应用
        if data.get('flashcards'):
            writing_card = next((c for c in data['flashcards'] if '写作' in c.get('title', '')), None)
            if writing_card:
                content += f"""## 卡片4: 写作应用 #card

**问**: {writing_card.get('question', '待补充')}

**答**: {writing_card.get('answer', '待补充')}

**说明**: {writing_card.get('notes', '')}

---

"""
        
        # 卡片5: 口语应用
        if data.get('flashcards'):
            speaking_card = next((c for c in data['flashcards'] if '口语' in c.get('title', '')), None)
            if speaking_card:
                content += f"""## 卡片5: 口语应用 #card

**场景**: {speaking_card.get('question', '待补充')}

**答**: {speaking_card.get('answer', '待补充')}

**亮点**: {speaking_card.get('notes', '')}

---

"""
        
        # 补充笔记
        content += "## 📝 补充笔记\n\n"
        
        # 词根记忆
        if data.get('etymology'):
            content += f"### 词根词缀\n{data['etymology']}\n\n"
        
        # 记忆技巧
        if data.get('memory_tip'):
            content += f"### 记忆技巧\n{data['memory_tip']}\n\n"
        
        # 记忆图片
        if data.get('image_path'):
            content += f"### 视觉记忆\n![[{data['image_path']}]]\n\n"
        
        # 关联词汇
        if data.get('related_words'):
            links = ' | '.join([f"[[{w}]]" for w in data['related_words']])
            content += f"### 关联词汇\n{links}\n\n"
        
        # 真题例句
        if data.get('examples'):
            content += "### 真题例句\n\n"
            for ex in data['examples']:
                content += f"> {ex['sentence']}\n"
                content += f"> 📄 来源: {ex['source']}\n\n"
        
        # 使用提示
        if data.get('usage_scenarios'):
            scenarios = data['usage_scenarios']
            content += "## 🎯 使用提示\n\n"
            if scenarios.get('suitable'):
                content += "### ✅ 推荐场景\n"
                for s in scenarios['suitable']:
                    content += f"- {s}\n"
                content += "\n"
            
            if scenarios.get('unsuitable'):
                content += "### ❌ 避免场景\n"
                for s in scenarios['unsuitable']:
                    content += f"- {s}\n"
                content += "\n"
        
        # 标签
        content += f"\n---\n\n#IELTS/{brand} #词汇/{data.get('pos', '待补充')}\n"
        
        return frontmatter + content
    
    def _get_future_date(self, days: int) -> str:
        """获取未来日期"""
        from datetime import timedelta
        future = datetime.now() + timedelta(days=days)
        return future.strftime('%Y-%m-%d')
    
    def batch_generate(
        self, 
        word_list: List[str], 
        brand: str = 'Brand7',
        theme: str = None,
        include_images: bool = False
    ) -> List[str]:
        """批量生成词汇笔记"""
        
        print(f"\n🚀 开始批量生成 {len(word_list)} 个词汇笔记")
        print(f"等级: {brand}")
        if theme:
            print(f"主题: {theme}")
        print(f"生成图片: {'是' if include_images else '否'}\n")
        
        created_files = []
        
        for i, word in enumerate(word_list, 1):
            print(f"\n[{i}/{len(word_list)}] 处理: {word}")
            
            try:
                # 生成笔记数据
                note_data = self.generate_vocabulary_note(
                    word, 
                    brand=brand, 
                    theme=theme,
                    include_image=include_images
                )
                
                # 创建Obsidian笔记
                file_path = self.create_obsidian_note(note_data)
                created_files.append(file_path)
                
            except Exception as e:
                print(f"❌ 生成失败: {word} - {e}")
                continue
        
        print(f"\n✅ 批量生成完成! 成功创建 {len(created_files)} 个笔记")
        return created_files


def main():
    """主函数 - 交互式使用"""
    
    print("="*60)
    print("🎯 AI驱动的雅思词汇笔记生成器")
    print("="*60)
    
    # 检查API密钥
    api_key = input("\n请输入LLM API密钥 (或按Enter跳过,使用模板模式): ").strip()
    
    if api_key:
        api_base = input("API Base URL (默认OpenAI,按Enter跳过): ").strip()
        generator = AIVocabularyGenerator(
            api_key=api_key,
            api_base=api_base if api_base else None
        )
    else:
        generator = AIVocabularyGenerator()
    
    # 选择模式
    print("\n选择模式:")
    print("1. 单个词汇生成")
    print("2. 批量生成")
    
    mode = input("\n请选择 (1/2): ").strip()
    
    if mode == '1':
        # 单个词汇
        word = input("\n请输入单词: ").strip()
        brand = input("等级 (Brand5/7/9, 默认Brand7): ").strip() or 'Brand7'
        theme = input("主题 (可选): ").strip() or None
        include_image = input("生成记忆图片? (y/n, 默认n): ").strip().lower() == 'y'
        
        note_data = generator.generate_vocabulary_note(
            word, 
            brand=brand, 
            theme=theme,
            include_image=include_image
        )
        
        generator.create_obsidian_note(note_data)
        
    elif mode == '2':
        # 批量生成
        print("\n请输入单词列表 (每行一个,输入空行结束):")
        word_list = []
        while True:
            word = input().strip()
            if not word:
                break
            word_list.append(word)
        
        if not word_list:
            print("未输入任何单词")
            return
        
        brand = input("\n等级 (Brand5/7/9, 默认Brand7): ").strip() or 'Brand7'
        theme = input("主题 (可选): ").strip() or None
        include_images = input("生成记忆图片? (y/n, 默认n): ").strip().lower() == 'y'
        
        generator.batch_generate(
            word_list,
            brand=brand,
            theme=theme,
            include_images=include_images
        )
    
    print("\n✅ 完成!")


if __name__ == '__main__':
    main()

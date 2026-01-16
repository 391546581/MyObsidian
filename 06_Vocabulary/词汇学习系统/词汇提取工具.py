#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雅思词汇自动提取与分级工具
从字幕文件(SRT/VTT)中提取词汇,自动分级为Brand5/7/9
"""

import re
import os
from collections import Counter
from pathlib import Path
import csv
import json

class SubtitleVocabularyExtractor:
    """字幕词汇提取器"""
    
    def __init__(self):
        # 加载词汇分级数据库
        self.brand5_words = self._load_brand5_words()
        self.brand7_words = self._load_brand7_words()
        self.brand9_words = self._load_brand9_words()
        
        # 停用词(不需要学习的常见词)
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
    
    def _load_brand5_words(self):
        """加载Brand5词汇库(基础高频词)"""
        # 这里是示例数据,实际使用时应该从文件加载
        return {
            'make', 'get', 'go', 'do', 'say', 'see', 'know', 'think', 'take',
            'come', 'want', 'use', 'find', 'give', 'tell', 'work', 'call',
            'try', 'ask', 'need', 'feel', 'become', 'leave', 'put', 'mean',
            'keep', 'let', 'begin', 'seem', 'help', 'talk', 'turn', 'start',
            'show', 'hear', 'play', 'run', 'move', 'like', 'live', 'believe',
            'hold', 'bring', 'happen', 'write', 'provide', 'sit', 'stand',
            'lose', 'pay', 'meet', 'include', 'continue', 'set', 'learn',
            'change', 'lead', 'understand', 'watch', 'follow', 'stop', 'create',
            'speak', 'read', 'allow', 'add', 'spend', 'grow', 'open', 'walk',
            'win', 'offer', 'remember', 'love', 'consider', 'appear', 'buy',
            'wait', 'serve', 'die', 'send', 'expect', 'build', 'stay', 'fall',
            'cut', 'reach', 'kill', 'remain', 'suggest', 'raise', 'pass',
            'important', 'good', 'new', 'first', 'last', 'long', 'great', 'little',
            'own', 'other', 'old', 'right', 'big', 'high', 'different', 'small',
            'large', 'next', 'early', 'young', 'few', 'public', 'bad', 'same',
            'able', 'problem', 'increase', 'number', 'people', 'time', 'year',
            'way', 'day', 'thing', 'man', 'world', 'life', 'hand', 'part',
            'child', 'eye', 'woman', 'place', 'work', 'week', 'case', 'point',
            'government', 'company'
        }
    
    def _load_brand7_words(self):
        """加载Brand7词汇库(雅思高分词)"""
        return {
            'acquire', 'constitute', 'crucial', 'demonstrate', 'enhance',
            'facilitate', 'implement', 'indicate', 'maintain', 'obtain',
            'participate', 'perceive', 'pursue', 'require', 'retain',
            'significant', 'subsequent', 'sufficient', 'utilize', 'assess',
            'attribute', 'capacity', 'component', 'comprehensive', 'conduct',
            'consequence', 'considerable', 'consist', 'constant', 'construct',
            'consume', 'context', 'contribute', 'convert', 'cooperate',
            'coordinate', 'core', 'corporate', 'correspond', 'create',
            'criteria', 'crucial', 'culture', 'data', 'debate', 'decade',
            'decline', 'define', 'demonstrate', 'denote', 'derive', 'design',
            'despite', 'detect', 'device', 'devote', 'dimension', 'diminish',
            'discrete', 'discriminate', 'displace', 'display', 'dispose',
            'distinct', 'distribute', 'diverse', 'document', 'domain',
            'domestic', 'dominate', 'draft', 'drama', 'duration', 'dynamic',
            'economy', 'edit', 'element', 'eliminate', 'emerge', 'emphasis',
            'empirical', 'enable', 'encounter', 'energy', 'enforce', 'enhance',
            'enormous', 'ensure', 'entity', 'environment', 'equate', 'equip',
            'equivalent', 'erode', 'error', 'establish', 'estate', 'estimate',
            'ethic', 'ethnic', 'evaluate', 'eventual', 'evident', 'evolve',
            'exceed', 'exclude', 'exhibit', 'expand', 'expert', 'explicit',
            'exploit', 'export', 'expose', 'external', 'extract', 'facilitate',
            'factor', 'feature', 'federal', 'fee', 'file', 'final', 'finance',
            'finite', 'flexible', 'fluctuate', 'focus', 'format', 'formula',
            'forthcoming', 'foundation', 'founded', 'framework', 'function',
            'fund', 'fundamental', 'furthermore', 'gender', 'generate',
            'generation', 'globe', 'goal', 'grade', 'grant', 'guarantee',
            'guideline', 'hence', 'hierarchy', 'highlight', 'hypothesis',
            'identical', 'identify', 'ideology', 'ignorance', 'illustrate',
            'image', 'immigrate', 'impact', 'implement', 'implicate', 'implicit',
            'imply', 'impose', 'incentive', 'incidence', 'incline', 'income',
            'incorporate', 'index', 'indicate', 'individual', 'induce',
            'inevitable', 'infer', 'infrastructure', 'inherent', 'inhibit',
            'initial', 'initiate', 'injure', 'innovate', 'input', 'insert',
            'insight', 'inspect', 'instance', 'institute', 'instruct',
            'integral', 'integrate', 'integrity', 'intelligence', 'intense',
            'interact', 'intermediate', 'internal', 'interpret', 'interval',
            'intervene', 'intrinsic', 'invest', 'investigate', 'invoke',
            'involve', 'isolate', 'issue', 'item', 'job', 'journal', 'justify',
            'label', 'labor', 'layer', 'lecture', 'legal', 'legislate',
            'levy', 'liberal', 'license', 'likewise', 'link', 'locate', 'logic'
        }
    
    def _load_brand9_words(self):
        """加载Brand9词汇库(学术高阶词)"""
        return {
            'ascertain', 'corroborate', 'ubiquitous', 'mitigate', 'elucidate',
            'substantiate', 'ameliorate', 'exacerbate', 'proliferate', 'disseminate',
            'promulgate', 'inculcate', 'edify', 'pedagogical', 'erudite',
            'didactic', 'matriculate', 'autodidact', 'juxtapose', 'paradigm',
            'quintessential', 'salient', 'tangential', 'vicarious', 'zealous',
            'aberration', 'abstruse', 'acumen', 'adroit', 'aesthetic',
            'alleviate', 'ambiguous', 'ameliorate', 'anachronistic', 'analogous',
            'anomaly', 'antithesis', 'apathy', 'arbitrary', 'archaic',
            'arduous', 'articulate', 'assiduous', 'astute', 'audacious',
            'auspicious', 'austere', 'autonomous', 'avarice', 'banal',
            'benevolent', 'bolster', 'burgeon', 'cacophony', 'candid',
            'capricious', 'catalyst', 'caustic', 'censure', 'charlatan',
            'circumspect', 'clandestine', 'coalesce', 'cogent', 'commensurate',
            'compelling', 'complacent', 'complement', 'complicit', 'comprehensive',
            'conciliatory', 'concise', 'concomitant', 'condone', 'confound',
            'congenial', 'conjecture', 'connote', 'conscientious', 'consensus',
            'construe', 'contentious', 'contextualize', 'contrite', 'convoluted',
            'copious', 'corroborate', 'credulous', 'cryptic', 'culpable',
            'cursory', 'curtail', 'cynical', 'debacle', 'debilitate',
            'decorous', 'decry', 'deference', 'delineate', 'deleterious',
            'demagogue', 'demarcate', 'demeanor', 'demur', 'denigrate',
            'denote', 'depict', 'deprecate', 'deride', 'derivative',
            'desiccate', 'desultory', 'deterrent', 'detrimental', 'deviate',
            'dexterous', 'diaphanous', 'diatribe', 'dichotomy', 'didactic',
            'diffident', 'digress', 'dilapidated', 'dilatory', 'diligent',
            'diminutive', 'discern', 'discomfit', 'discordant', 'discourse',
            'discrepancy', 'discrete', 'discriminate', 'disdain', 'disingenuous',
            'disparage', 'disparate', 'dispassionate', 'disseminate', 'dissent',
            'dissolution', 'dissonance', 'distend', 'divergent', 'divulge',
            'dogmatic', 'dormant', 'dubious', 'duplicity', 'ebullient',
            'eccentric', 'eclectic', 'efficacious', 'effrontery', 'egalitarian',
            'egregious', 'elaborate', 'elicit', 'eloquent', 'elucidate',
            'elusive', 'emaciated', 'embellish', 'eminent', 'empirical',
            'emulate', 'endemic', 'enervate', 'engender', 'enigmatic',
            'enmity', 'ennui', 'ephemeral', 'equanimity', 'equivocal',
            'eradicate', 'erratic', 'erstwhile', 'erudite', 'esoteric',
            'espouse', 'ethereal', 'euphemism', 'evanescent', 'exacerbate',
            'exacting', 'exalt', 'exasperate', 'exemplary', 'exhaustive',
            'exhort', 'exigent', 'exonerate', 'expedient', 'expedite',
            'explicate', 'explicit', 'exploit', 'expound', 'expunge',
            'extant', 'extemporaneous', 'extenuate', 'extol', 'extraneous',
            'extrapolate', 'extricate', 'exuberant', 'facetious', 'facilitate',
            'fallacious', 'fastidious', 'fatuous', 'fawn', 'feasible',
            'feckless', 'fecund', 'felicitous', 'fervent', 'fervid'
        }
    
    def parse_srt(self, file_path):
        """解析SRT字幕文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除时间戳和序号,只保留文本
        # SRT格式: 序号\n时间戳\n文本\n空行
        text = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', '', content)
        text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
        
        return text
    
    def parse_vtt(self, file_path):
        """解析VTT字幕文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除WEBVTT头和时间戳
        text = re.sub(r'WEBVTT.*?\n\n', '', content)
        text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?\n', '', content)
        
        return text
    
    def extract_words(self, text):
        """从文本中提取单词"""
        # 转换为小写
        text = text.lower()
        
        # 提取单词(只保留字母)
        words = re.findall(r'\b[a-z]+\b', text)
        
        # 过滤停用词和短词
        words = [w for w in words if w not in self.stop_words and len(w) > 3]
        
        return words
    
    def classify_word(self, word):
        """分类单词到Brand5/7/9"""
        if word in self.brand9_words:
            return 'Brand9'
        elif word in self.brand7_words:
            return 'Brand7'
        elif word in self.brand5_words:
            return 'Brand5'
        else:
            # 未知词汇,根据长度和复杂度估算
            if len(word) <= 5:
                return 'Brand5'
            elif len(word) <= 8:
                return 'Brand7'
            else:
                return 'Brand9'
    
    def analyze_subtitle(self, file_path, min_frequency=2):
        """分析字幕文件,提取高频词汇"""
        # 解析字幕
        if file_path.endswith('.srt'):
            text = self.parse_srt(file_path)
        elif file_path.endswith('.vtt'):
            text = self.parse_vtt(file_path)
        else:
            raise ValueError("不支持的文件格式,请使用.srt或.vtt文件")
        
        # 提取单词
        words = self.extract_words(text)
        
        # 统计词频
        word_freq = Counter(words)
        
        # 过滤低频词
        high_freq_words = {word: freq for word, freq in word_freq.items() 
                          if freq >= min_frequency}
        
        # 分类
        classified = {
            'Brand5': [],
            'Brand7': [],
            'Brand9': [],
            'Unknown': []
        }
        
        for word, freq in high_freq_words.items():
            brand = self.classify_word(word)
            classified[brand].append({
                'word': word,
                'frequency': freq,
                'brand': brand
            })
        
        # 按频率排序
        for brand in classified:
            classified[brand].sort(key=lambda x: x['frequency'], reverse=True)
        
        return classified
    
    def export_to_csv(self, classified_words, output_file):
        """导出到CSV文件(可导入Anki)"""
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # 写入表头
            writer.writerow(['单词', '等级', '频率', '词性', '释义', '标签'])
            
            # 写入数据
            for brand in ['Brand5', 'Brand7', 'Brand9']:
                for item in classified_words[brand]:
                    writer.writerow([
                        item['word'],
                        item['brand'],
                        item['frequency'],
                        '',  # 词性需要手动填写或API查询
                        '',  # 释义需要手动填写或API查询
                        f"IELTS,{item['brand']},字幕提取"
                    ])
        
        print(f"✅ 已导出到: {output_file}")
    
    def export_to_obsidian(self, classified_words, output_dir):
        """导出为Obsidian笔记"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for brand in ['Brand5', 'Brand7', 'Brand9']:
            brand_dir = output_path / brand
            brand_dir.mkdir(exist_ok=True)
            
            for item in classified_words[brand]:
                word = item['word']
                freq = item['frequency']
                
                # 创建笔记文件
                note_content = f"""---
词汇: {word}
等级: {brand}
频率: {freq}
来源: 字幕提取
创建日期: {self._get_today()}
---

# {word}

## 📊 统计信息
- **出现频率**: {freq}次
- **等级**: {brand}
- **来源**: 学习视频字幕

## 📝 基本信息
**词性**: _待补充_  
**音标**: _待补充_  
**释义**: _待补充_

## 💡 例句 (来自字幕)
> _待提取具体例句_

## 🔗 关联词汇
_待补充_

---

#IELTS/{brand} #字幕提取 #待完善
"""
                
                note_file = brand_dir / f"{word}.md"
                with open(note_file, 'w', encoding='utf-8') as f:
                    f.write(note_content)
        
        print(f"✅ 已导出到Obsidian: {output_dir}")
    
    def _get_today(self):
        """获取今天日期"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')
    
    def generate_report(self, classified_words):
        """生成分析报告"""
        print("\n" + "="*60)
        print("📊 字幕词汇分析报告")
        print("="*60)
        
        total = sum(len(classified_words[brand]) for brand in ['Brand5', 'Brand7', 'Brand9'])
        
        print(f"\n总计提取高频词汇: {total} 个\n")
        
        for brand in ['Brand5', 'Brand7', 'Brand9']:
            words = classified_words[brand]
            count = len(words)
            percentage = (count / total * 100) if total > 0 else 0
            
            print(f"{brand}: {count} 个 ({percentage:.1f}%)")
            
            if count > 0:
                print(f"  Top 5: {', '.join([w['word'] for w in words[:5]])}")
                print()
        
        print("="*60)
        
        # 学习建议
        print("\n💡 学习建议:")
        print(f"  - Brand5词汇({len(classified_words['Brand5'])}个): 重点记忆固定搭配")
        print(f"  - Brand7词汇({len(classified_words['Brand7'])}个): 重点记忆同义替换")
        print(f"  - Brand9词汇({len(classified_words['Brand9'])}个): 重点记忆使用语境")
        print()


def main():
    """主函数"""
    print("🎯 雅思词汇自动提取工具")
    print("="*60)
    
    # 创建提取器
    extractor = SubtitleVocabularyExtractor()
    
    # 示例用法
    print("\n使用方法:")
    print("1. 将字幕文件(.srt或.vtt)放在指定目录")
    print("2. 运行脚本分析")
    print("3. 导出为CSV(Anki)或Markdown(Obsidian)")
    print()
    
    # 交互式输入
    subtitle_file = input("请输入字幕文件路径 (或按Enter使用示例): ").strip()
    
    if not subtitle_file:
        print("\n⚠️  未提供文件路径,显示使用示例...")
        print("\n示例代码:")
        print("""
# 分析字幕文件
classified = extractor.analyze_subtitle('path/to/subtitle.srt', min_frequency=2)

# 生成报告
extractor.generate_report(classified)

# 导出到CSV (可导入Anki)
extractor.export_to_csv(classified, 'output/vocabulary.csv')

# 导出到Obsidian
extractor.export_to_obsidian(classified, 'output/obsidian_notes')
        """)
        return
    
    if not os.path.exists(subtitle_file):
        print(f"❌ 文件不存在: {subtitle_file}")
        return
    
    # 分析
    print(f"\n🔍 正在分析: {subtitle_file}")
    classified = extractor.analyze_subtitle(subtitle_file, min_frequency=2)
    
    # 生成报告
    extractor.generate_report(classified)
    
    # 询问导出选项
    print("\n导出选项:")
    print("1. 导出为CSV (可导入Anki)")
    print("2. 导出为Obsidian笔记")
    print("3. 两者都导出")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        csv_file = input("CSV输出路径 (默认: vocabulary.csv): ").strip() or 'vocabulary.csv'
        extractor.export_to_csv(classified, csv_file)
    
    if choice in ['2', '3']:
        obs_dir = input("Obsidian输出目录 (默认: obsidian_notes): ").strip() or 'obsidian_notes'
        extractor.export_to_obsidian(classified, obs_dir)
    
    print("\n✅ 完成!")


if __name__ == '__main__':
    main()

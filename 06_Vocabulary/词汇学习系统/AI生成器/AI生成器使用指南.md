# 🤖 AI词汇生成器使用指南

> 使用AI自动生成高质量词汇笔记,告别手工录入!

---

## 🎯 核心功能

### 1. **AI自动生成内容**
- ✅ 精准的中英文释义
- ✅ 音标和词性
- ✅ 同义词分级(Brand5/7/9)
- ✅ 固定搭配+例句
- ✅ 5种复习卡片(释义/搭配/辨析/写作/口语)
- ✅ 词根词缀记忆技巧
- ✅ 使用场景建议
- ✅ 雅思真题级别例句

### 2. **AI图片记忆生成**
- ✅ 根据单词自动生成视觉记忆图
- ✅ 结合记忆技巧创建联想图
- ✅ 自动嵌入到Obsidian笔记

### 3. **批量处理**
- ✅ 一次性生成多个词汇笔记
- ✅ 自动按Brand分类存储
- ✅ 支持主题标签

---

## 🚀 快速开始

### 步骤1: 配置API密钥

**选项A: 使用OpenAI (推荐,质量最高)**

1. 获取API密钥: https://platform.openai.com/api-keys
2. 复制 `.env.example` 为 `.env`
3. 填写密钥:
   ```
   LLM_API_KEY=sk-your-openai-key-here
   LLM_API_BASE=https://api.openai.com/v1
   LLM_MODEL=gpt-4
   ```

**选项B: 使用DeepSeek (性价比高,中文友好)**

1. 获取API密钥: https://platform.deepseek.com/
2. 配置:
   ```
   LLM_API_KEY=your-deepseek-key-here
   LLM_API_BASE=https://api.deepseek.com/v1
   LLM_MODEL=deepseek-chat
   ```

**选项C: 使用本地模型 (免费,但质量较低)**

1. 安装Ollama: https://ollama.ai/
2. 下载模型: `ollama pull llama2`
3. 配置:
   ```
   LLM_API_BASE=http://localhost:11434/v1
   LLM_MODEL=llama2
   LLM_API_KEY=ollama
   ```

---

### 步骤2: 安装依赖

```powershell
# 安装Python依赖
pip install requests python-dotenv

# 或使用requirements.txt
pip install -r requirements.txt
```

---

### 步骤3: 运行生成器

#### 方式1: 交互式运行

```powershell
cd d:\MyObsidian\06_Vocabulary\词汇学习系统
python AI词汇生成器.py
```

按提示输入:
- API密钥 (或按Enter使用.env配置)
- 选择单个/批量生成
- 输入单词
- 选择等级和主题

#### 方式2: 命令行参数

```powershell
# 单个词汇
python AI词汇生成器.py --word crucial --brand Brand7 --theme 教育

# 批量生成
python AI词汇生成器.py --batch words.txt --brand Brand7

# 生成图片
python AI词汇生成器.py --word crucial --image
```

#### 方式3: Python脚本调用

```python
from AI词汇生成器 import AIVocabularyGenerator

# 初始化
generator = AIVocabularyGenerator(
    api_key='your-api-key',
    api_base='https://api.openai.com/v1'
)

# 生成单个词汇
note_data = generator.generate_vocabulary_note(
    word='crucial',
    brand='Brand7',
    theme='教育',
    include_image=True
)

# 创建Obsidian笔记
generator.create_obsidian_note(note_data)

# 批量生成
word_list = ['crucial', 'acquire', 'mitigate']
generator.batch_generate(
    word_list,
    brand='Brand7',
    theme='教育',
    include_images=False
)
```

---

## 📊 生成质量对比

### AI生成 vs 手工录入

| 维度 | 手工录入 | AI生成 |
|------|---------|--------|
| **时间成本** | 15-20分钟/词 | 30-60秒/词 |
| **内容完整度** | 取决于个人 | 100%完整 |
| **例句质量** | 需要查找 | 雅思真题级别 |
| **同义词辨析** | 需要研究 | 自动分级 |
| **记忆技巧** | 需要创造 | AI生成 |
| **一致性** | 不稳定 | 高度一致 |

**结论**: AI生成可节省**95%时间**,质量更稳定!

---

## 🎨 AI图片生成示例

### 生成效果

**单词**: crucial  
**记忆技巧**: cruc-(十字) → 十字路口 → 关键选择

**AI生成图片**:
- 十字路口的场景
- 多个方向箭头
- 突出"关键选择"的视觉元素

### 配置图片生成

1. 启用图片生成:
   ```
   ENABLE_IMAGE_GENERATION=true
   IMAGE_API_KEY=your-openai-key
   ```

2. 运行时添加 `--image` 参数:
   ```powershell
   python AI词汇生成器.py --word crucial --image
   ```

3. 图片自动保存到 `images/vocabulary/` 并嵌入笔记

---

## 💡 高质量生成技巧

### 1. 提供主题上下文

```python
# ✅ 好的做法
generator.generate_vocabulary_note(
    word='acquire',
    brand='Brand7',
    theme='教育'  # 提供主题,生成更精准的例句
)

# ❌ 不推荐
generator.generate_vocabulary_note(
    word='acquire',
    brand='Brand7'
    # 缺少主题,例句可能不够聚焦
)
```

### 2. 选择合适的模型

| 模型 | 优势 | 劣势 | 推荐场景 |
|------|------|------|---------|
| **GPT-4** | 质量最高,理解最准 | 价格较高 | 重要词汇,考前冲刺 |
| **GPT-3.5** | 性价比高 | 偶尔不够精准 | 日常学习,批量生成 |
| **DeepSeek** | 中文友好,便宜 | 英文略逊 | 中文释义,性价比优先 |
| **Claude** | 长文本好 | API限制多 | 复杂词汇,深度分析 |

### 3. 批量生成优化

```python
# 分批处理,避免API限流
word_list = ['word1', 'word2', ..., 'word100']

# 每次处理20个
batch_size = 20
for i in range(0, len(word_list), batch_size):
    batch = word_list[i:i+batch_size]
    generator.batch_generate(batch, brand='Brand7')
    time.sleep(5)  # 延迟5秒
```

### 4. 自定义提示词

修改 `AI词汇生成器.py` 中的 `_build_prompt` 方法:

```python
def _build_prompt(self, word: str, brand: str, theme: Optional[str]) -> str:
    # 添加您自己的要求
    prompt = f"""
    ... (原有内容)
    
    额外要求:
    - 例句必须来自剑桥雅思真题
    - 搭配必须是高频搭配
    - 记忆技巧要有趣且易记
    """
    return prompt
```

---

## 🔧 常见问题

### Q1: API调用失败怎么办?

**答**: 
1. 检查API密钥是否正确
2. 检查网络连接
3. 查看API余额是否充足
4. 尝试降低 `MAX_TOKENS` 参数
5. 使用 `--debug` 参数查看详细错误

### Q2: 生成的内容不够准确?

**答**:
1. 使用GPT-4而非GPT-3.5
2. 提供更详细的主题上下文
3. 手动修改提示词,增加约束
4. 生成后人工审核和微调

### Q3: 批量生成太慢?

**答**:
1. 使用更快的模型(GPT-3.5)
2. 减少 `MAX_TOKENS`
3. 关闭图片生成
4. 使用多线程(高级)

### Q4: 图片生成失败?

**答**:
1. 检查 `IMAGE_API_KEY` 是否配置
2. DALL-E 3需要OpenAI Plus订阅
3. 可以使用本地Stable Diffusion
4. 或者跳过图片生成,手动添加

### Q5: 如何集成到现有工作流?

**答**:
```python
# 与字幕提取工具结合
from 词汇提取工具 import SubtitleVocabularyExtractor
from AI词汇生成器 import AIVocabularyGenerator

# 1. 从字幕提取词汇
extractor = SubtitleVocabularyExtractor()
classified = extractor.analyze_subtitle('subtitle.srt')

# 2. AI生成笔记
generator = AIVocabularyGenerator(api_key='your-key')
for word_data in classified['Brand7']:
    word = word_data['word']
    note_data = generator.generate_vocabulary_note(word, 'Brand7')
    generator.create_obsidian_note(note_data)
```

---

## 💰 成本估算

### OpenAI GPT-4

- **输入**: ~500 tokens/词 × $0.03/1K = $0.015
- **输出**: ~1500 tokens/词 × $0.06/1K = $0.09
- **图片**: $0.04/张 (DALL-E 3)

**总计**: ~$0.15/词 (含图片) 或 $0.11/词 (不含图片)

**批量生成100词**: ~$11-15

### DeepSeek (推荐性价比)

- **输入**: ~500 tokens/词 × $0.001/1K = $0.0005
- **输出**: ~1500 tokens/词 × $0.002/1K = $0.003

**总计**: ~$0.0035/词

**批量生成100词**: ~$0.35 (超便宜!)

---

## 🎁 高级功能

### 1. 自动从真题提取词汇并生成

```python
# 读取雅思真题PDF
# 提取生词
# AI生成笔记
# 自动分类存储
```

### 2. 集成语音朗读

```python
# 使用TTS API生成发音
# 嵌入到Obsidian笔记
```

### 3. 自动生成复习计划

```python
# 根据遗忘曲线
# 自动安排复习时间
# 生成每日复习清单
```

### 4. 进度追踪和可视化

```python
# 统计词汇量增长
# 生成学习报告
# 可视化掌握程度
```

---

## 📝 下一步行动

### 今天就开始 (选择一个)

**选项1: 最简单 - 生成3个词汇测试**
```powershell
python AI词汇生成器.py
# 输入: crucial, acquire, mitigate
# 查看生成效果
```

**选项2: 批量生成 - 从真题提取的20个词**
```powershell
# 创建 words.txt,每行一个单词
python AI词汇生成器.py --batch words.txt --brand Brand7
```

**选项3: 完整流程 - 字幕提取+AI生成**
```powershell
# 1. 提取字幕词汇
python 词汇提取工具.py

# 2. AI生成笔记
python AI词汇生成器.py --batch extracted_words.txt
```

---

## 🌟 最佳实践

### 每日工作流

```
1. 早晨: 看英语学习视频
2. 提取: 运行字幕提取工具
3. 生成: AI批量生成笔记(5-10个词)
4. 复习: Obsidian SR插件复习
5. 应用: 写作/口语练习中使用
```

### 每周工作流

```
1. 周一-周五: 每天新增5-10词
2. 周六: 批量生成本周词汇
3. 周日: 复习+调整学习计划
```

---

**开始使用AI,让词汇学习效率提升10倍!** 🚀

#AI工具 #自动化 #词汇学习 #IELTS

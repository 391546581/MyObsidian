# 🎯 雅思词汇学习系统

> AI驱动的智能词汇笔记生成系统  
> 从手工录入到自动化,效率提升10倍!

---

## ✨ 核心特性

- 🤖 **AI自动生成** - 30秒生成完整高质量笔记
- 🎨 **AI图片记忆** - 自动生成视觉记忆图
- 📊 **Brand5/7/9分级** - 精准对应雅思评分标准
- 🔄 **批量处理** - 一次性生成多个词汇
- 📚 **6大主题词簇** - 教育/环境/科技/社会/经济/健康
- 🔗 **Obsidian集成** - 完美适配SR插件
- 💰 **性价比高** - DeepSeek仅$0.0035/词

---

## 📦 文件结构

```
06_Vocabulary/词汇学习系统/
├── 00-AI系统总结.md              # 📖 系统总览和使用指南
├── AI词汇生成器.py                # 🤖 核心AI生成引擎
├── 一键生成.py                    # ⚡ 简化版快速工具
├── 词汇提取工具.py                # 📝 从字幕提取词汇
├── AI生成器使用指南.md            # 📚 详细使用说明
├── 主题词簇完整版.md              # 📊 6大主题词汇库
├── 模板-词汇笔记(SR插件版).md     # 📄 Obsidian模板
├── .env.example                  # ⚙️  配置文件模板
├── requirements.txt              # 📦 Python依赖
└── README.md                     # 📖 本文件
```

---

## 🚀 快速开始 (3分钟)

### 步骤1: 安装依赖

```powershell
# 进入目录
cd d:\MyObsidian\06_Vocabulary\词汇学习系统

# 安装Python依赖
pip install -r requirements.txt
```

### 步骤2: 运行演示

```powershell
# 运行一键生成工具
python 一键生成.py

# 选择演示模式
> 2

# 查看生成的3个示例笔记
```

### 步骤3: 在Obsidian中查看

打开 `06_Vocabulary/词汇学习系统/Brand7/` 文件夹,查看生成的笔记。

---

## 💡 三种使用方式

### 方式1: 一键生成 (推荐新手)

```powershell
python 一键生成.py
> crucial acquire mitigate
> y (使用AI) 或 n (使用模板)
```

**适合**: 快速测试,少量词汇

---

### 方式2: AI自动生成 (推荐日常)

```powershell
# 1. 配置API密钥
cp .env.example .env
# 编辑.env,填写API密钥

# 2. 运行AI生成器
python AI词汇生成器.py

# 3. 批量生成
> 2 (批量模式)
> crucial
> acquire
> mitigate
> (空行结束)
```

**适合**: 高质量内容,批量生成

---

### 方式3: 完整工作流 (推荐进阶)

```powershell
# 1. 从字幕提取词汇
python 词汇提取工具.py

# 2. AI批量生成
python AI词汇生成器.py --batch extracted_words.csv

# 3. Obsidian SR复习
```

**适合**: 大量词汇,自动化流程

---

## 📊 效率对比

| 项目 | 手工录入 | AI生成 | 提升 |
|------|---------|--------|------|
| 时间 | 15-20分钟 | 30-60秒 | **20倍** |
| 质量 | 不稳定 | 雅思真题级 | **显著提升** |
| 完整度 | 60-80% | 100% | **1.3倍** |

---

## 💰 成本估算

### OpenAI GPT-4
- 单词: ~$0.11 (不含图片)
- 100词: ~$11

### DeepSeek (推荐)
- 单词: ~$0.0035
- 100词: ~$0.35
- 月度 (150词): ~$0.53

---

## 🎨 AI生成示例

### 输入
```
单词: crucial
等级: Brand7
主题: 教育
```

### 输出 (30秒)
- ✅ 5个复习卡片 (释义/搭配/辨析/写作/口语)
- ✅ 词根词缀记忆技巧
- ✅ 同义词分级 (Brand5/7/9)
- ✅ 雅思真题级例句
- ✅ 使用场景建议
- ✅ AI生成记忆图片 (可选)

---

## 📚 学习资源

### 已包含的语料

1. **主题词簇完整版.md**
   - 6大主题 (教育/环境/科技/社会/经济/健康)
   - 300+ 词汇
   - Brand5/7/9分级
   - 地道搭配短语

2. **AI生成内容**
   - 雅思真题级例句
   - 场景化应用
   - 写作/口语示例

---

## 🔧 配置说明

### API密钥配置

1. 复制配置文件:
   ```powershell
   cp .env.example .env
   ```

2. 编辑 `.env`,填写API密钥:
   ```
   LLM_API_KEY=your-api-key-here
   LLM_API_BASE=https://api.openai.com/v1
   LLM_MODEL=gpt-4
   ```

3. 支持的API:
   - OpenAI (推荐质量)
   - DeepSeek (推荐性价比)
   - Claude
   - Ollama (本地免费)

---

## 📝 使用技巧

### 1. 批量生成优化

```python
# 分批处理,避免API限流
word_list = ['word1', 'word2', ..., 'word100']
batch_size = 20

for i in range(0, len(word_list), batch_size):
    batch = word_list[i:i+batch_size]
    generator.batch_generate(batch, brand='Brand7')
    time.sleep(5)  # 延迟5秒
```

### 2. 自定义提示词

编辑 `AI词汇生成器.py` 中的 `_build_prompt` 方法,添加您的特殊要求。

### 3. 集成工作流

```python
# 字幕提取 → AI生成 → Obsidian复习
from 词汇提取工具 import SubtitleVocabularyExtractor
from AI词汇生成器 import AIVocabularyGenerator

extractor = SubtitleVocabularyExtractor()
classified = extractor.analyze_subtitle('subtitle.srt')

generator = AIVocabularyGenerator(api_key='your-key')
for word_data in classified['Brand7']:
    generator.generate_vocabulary_note(word_data['word'], 'Brand7')
```

---

## 🆘 常见问题

### Q: 没有API密钥怎么办?

**A**: 使用模板模式,生成结构化笔记,手动填写内容。

### Q: API调用失败?

**A**: 检查:
1. API密钥是否正确
2. 网络连接
3. API余额
4. 速率限制

### Q: 如何选择LLM?

**A**: 
- 日常学习: DeepSeek (性价比)
- 重要词汇: GPT-4 (质量)
- 离线使用: Ollama (免费)

---

## 📖 详细文档

- **00-AI系统总结.md** - 完整系统介绍
- **AI生成器使用指南.md** - 详细使用说明
- **主题词簇完整版.md** - 词汇库参考

---

## 🎯 下一步行动

### 今天 (5分钟)
```powershell
python 一键生成.py
> 选择演示模式
> 查看生成效果
```

### 本周 (1小时)
1. [ ] 配置API密钥
2. [ ] 生成10个词汇
3. [ ] Obsidian SR复习
4. [ ] 评估质量

### 本月
1. [ ] 建立100词库
2. [ ] 集成字幕提取
3. [ ] 优化提示词
4. [ ] 建立自动化流程

---

## 💬 反馈与支持

使用过程中有任何问题或建议,欢迎反馈!

---

## 📄 许可证

本项目仅供个人学习使用。

---

**开始使用AI,让词汇学习效率提升10倍!** 🚀

#IELTS #词汇学习 #AI自动化 #Obsidian

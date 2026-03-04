---
name: text_analyzer
description: "文本分析技能，用于统计文本字数、分析词频、提取关键词等文本处理任务。当用户需要分析文本内容、统计字数、查找高频词汇时使用此技能。"
---

# Text Analyzer Skill

## 功能概述

这个技能提供了强大的文本分析能力，包括：

- **基础统计**：字数、行数、段落数、句子数
- **词频分析**：统计高频词汇，排除停用词
- **关键词提取**：自动提取文本中的关键词
- **可读性分析**：评估文本的阅读难度

## 使用场景

当用户提出以下需求时，应该使用此技能：

1. "帮我统计这篇文章有多少字"
2. "分析这段文本的高频词汇"
3. "提取这个文档的关键词"
4. "这个文本的阅读难度如何"

## 使用方法

### 1. 基础统计

```python
from scripts.analyzer import TextAnalyzer

analyzer = TextAnalyzer(text)
stats = analyzer.get_basic_stats()
print(f"字数: {stats['chars']}")
print(f"行数: {stats['lines']}")
print(f"段落数: {stats['paragraphs']}")
```

### 2. 词频分析

```python
word_freq = analyzer.get_word_frequency(top_n=10)
for word, count in word_freq:
    print(f"{word}: {count}次")
```

### 3. 关键词提取

```python
keywords = analyzer.extract_keywords(num_keywords=5)
print("关键词:", ", ".join(keywords))
```

## 注意事项

- 对于大文件（>10MB），建议分块处理
- 中文文本需要使用jieba分词
- 英文文本会自动转换为小写进行分析

## 示例工作流

当用户说"帮我分析这个文本文件"时：

1. 使用 `read_file` 读取文本文件
2. 使用 `execute_shell_command` 运行分析脚本
3. 将结果整理后返回给用户

## 脚本位置

- `scripts/analyzer.py` - 核心分析类
- `scripts/utils.py` - 工具函数
- `references/stopwords.txt` - 停用词列表

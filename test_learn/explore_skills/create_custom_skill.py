# -*- coding: utf-8 -*-
"""
创建和使用自定义Skill的完整示例

本示例演示：
1. 创建一个完整的skill（包含SKILL.md、scripts、references）
2. 将skill注册到CoPaw系统
3. 模拟AI如何使用这个skill
"""
import os
from pathlib import Path


def create_text_analyzer_skill():
    """
    创建一个文本分析skill的完整示例
    
    这个skill可以帮助AI：
    - 统计文本字数、行数、段落数
    - 分析词频
    - 提取关键词
    """
    
    skill_dir = Path("d:/work/ai_project/CoPaw/test_learn/text_analyzer_skill")
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 创建SKILL.md
    skill_md = """---
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
"""
    
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    print(f"✓ 创建 SKILL.md")
    
    # 2. 创建scripts目录和脚本
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    
    analyzer_script = '''# -*- coding: utf-8 -*-
"""文本分析器核心模块"""
import re
from collections import Counter
from typing import List, Tuple, Dict


class TextAnalyzer:
    """文本分析器"""
    
    def __init__(self, text: str):
        """初始化分析器
        
        Args:
            text: 要分析的文本
        """
        self.text = text
        self._chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        self._english_pattern = re.compile(r'[a-zA-Z]+')
    
    def get_basic_stats(self) -> Dict[str, int]:
        """获取基础统计信息
        
        Returns:
            包含字数、行数、段落数、句子数的字典
        """
        lines = self.text.split('\\n')
        paragraphs = [p for p in self.text.split('\\n\\n') if p.strip()]
        sentences = re.split(r'[。！？.!?]', self.text)
        sentences = [s for s in sentences if s.strip()]
        
        # 统计中文字符
        chinese_chars = len(self._chinese_pattern.findall(self.text))
        # 统计英文单词
        english_words = len(self._english_pattern.findall(self.text))
        
        return {
            'chars': len(self.text),
            'chinese_chars': chinese_chars,
            'english_words': english_words,
            'lines': len(lines),
            'paragraphs': len(paragraphs),
            'sentences': len(sentences),
        }
    
    def get_word_frequency(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """获取词频统计
        
        Args:
            top_n: 返回前N个高频词
            
        Returns:
            (词, 频次) 的列表
        """
        # 简单实现：提取英文单词
        words = self._english_pattern.findall(self.text.lower())
        word_counter = Counter(words)
        
        # 过滤短词
        filtered = {w: c for w, c in word_counter.items() if len(w) > 2}
        
        return sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    def extract_keywords(self, num_keywords: int = 5) -> List[str]:
        """提取关键词
        
        Args:
            num_keywords: 提取的关键词数量
            
        Returns:
            关键词列表
        """
        # 简单实现：使用高频词作为关键词
        word_freq = self.get_word_frequency(top_n=num_keywords * 2)
        
        # 过滤常见停用词
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 
                     'been', 'being', 'have', 'has', 'had', 'do', 'does',
                     'did', 'will', 'would', 'could', 'should', 'may', 'might',
                     'must', 'shall', 'can', 'need', 'dare', 'ought', 'used',
                     'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
                     'as', 'into', 'through', 'during', 'before', 'after',
                     'above', 'below', 'between', 'under', 'again', 'further',
                     'then', 'once', 'here', 'there', 'when', 'where', 'why',
                     'how', 'all', 'each', 'few', 'more', 'most', 'other',
                     'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
                     'so', 'than', 'too', 'very', 'just', 'and', 'but', 'if',
                     'or', 'because', 'until', 'while', 'this', 'that', 'these',
                     'those', 'it', 'its'}
        
        keywords = [word for word, _ in word_freq if word not in stopwords]
        return keywords[:num_keywords]


if __name__ == "__main__":
    # 测试示例
    sample_text = """
    Python is a programming language that lets you work quickly
    and integrate systems more effectively. Python is widely used
    in data science, web development, and automation.
    """
    
    analyzer = TextAnalyzer(sample_text)
    print("基础统计:", analyzer.get_basic_stats())
    print("词频分析:", analyzer.get_word_frequency(5))
    print("关键词:", analyzer.extract_keywords(3))
'''
    
    (scripts_dir / "analyzer.py").write_text(analyzer_script, encoding="utf-8")
    print(f"✓ 创建 scripts/analyzer.py")
    
    # 3. 创建references目录和参考文件
    references_dir = skill_dir / "references"
    references_dir.mkdir(exist_ok=True)
    
    stopwords = """the
a
an
is
are
was
were
be
been
being
have
has
had
do
does
did
will
would
could
should
may
might
must
shall
can
need
dare
ought
used
to
of
in
for
on
with
at
by
from
as
into
through
during
before
after
above
below
between
under
again
further
then
once
here
there
when
where
why
how
all
each
few
more
most
other
some
such
no
nor
not
only
own
same
so
than
too
very
just
and
but
if
or
because
until
while
this
that
these
those
it
its"""
    
    (references_dir / "stopwords.txt").write_text(stopwords, encoding="utf-8")
    print(f"✓ 创建 references/stopwords.txt")
    
    # 4. 创建README
    readme = """# Text Analyzer Skill

## 快速开始

1. 确保已安装Python 3.10+
2. 如需中文分析，安装jieba: `pip install jieba`

## 测试脚本

```bash
python scripts/analyzer.py
```

## 目录结构

```
text_analyzer_skill/
├── SKILL.md              # 技能说明文档
├── README.md             # 本文件
├── scripts/              # 执行脚本
│   └── analyzer.py       # 核心分析器
└── references/           # 参考资源
    └── stopwords.txt     # 停用词列表
```
"""
    
    (skill_dir / "README.md").write_text(readme, encoding="utf-8")
    print(f"✓ 创建 README.md")
    
    print(f"\n✅ Skill创建完成！")
    print(f"目录: {skill_dir}")
    print(f"\n下一步：")
    print(f"1. 测试脚本: python {scripts_dir / 'analyzer.py'}")
    print(f"2. 将skill复制到CoPaw的skills目录")
    print(f"3. 重启CoPaw，AI将自动加载此skill")
    
    return skill_dir


def demo_using_skill():
    """演示如何使用创建的skill"""
    print("\n" + "="*60)
    print("演示：AI如何使用Text Analyzer Skill")
    print("="*60)
    
    sample_interaction = """
用户: 帮我分析一下这段文本的字数和关键词

文本内容：
"Python is a powerful programming language. It is widely used 
in data science, machine learning, and web development. 
Python's simple syntax makes it easy to learn."

AI的工作流程：

【步骤1】识别需求
- 用户需要文本分析
- 查看系统提示中的skills列表
- 发现 'text_analyzer' skill 符合需求

【步骤2】读取SKILL.md
- 使用 read_file 工具
- 读取 text_analyzer/SKILL.md
- 了解如何使用这个skill

【步骤3】执行分析
- 使用 execute_shell_command 运行分析脚本
- 或者使用 read_file + Python执行的方式

命令示例：
```bash
python text_analyzer_skill/scripts/analyzer.py
```

【步骤4】返回结果
根据分析结果，AI会回复：

"我已经分析了这段文本，结果如下：

📊 基础统计：
- 总字符数：156
- 英文单词数：26
- 句子数：3
- 行数：3

🔤 高频词汇：
1. python: 3次
2. used: 1次
3. language: 1次

💡 关键词：
Python, programming, language, data, science

📝 分析说明：
这段文本主要介绍Python编程语言的特点和应用领域。
文本简洁明了，适合作为入门介绍。"
"""
    
    print(sample_interaction)


if __name__ == "__main__":
    print("="*60)
    print("创建Text Analyzer Skill示例")
    print("="*60)
    
    skill_dir = create_text_analyzer_skill()
    
    demo_using_skill()
    
    print("\n" + "="*60)
    print("如何将Skill集成到CoPaw")
    print("="*60)
    print("""
方法1: 手动复制
----------------
将创建的 text_analyzer_skill 目录复制到：
  d:/work/ai_project/CoPaw/src/copaw/agents/skills/

然后重启CoPaw，skill会自动加载。

方法2: 使用CoPaw命令（如果支持）
-------------------------------
copaw skills add text_analyzer_skill

方法3: 放到用户skills目录
------------------------
将skill放到用户的skills目录：
  ~/.copaw/skills/text_analyzer_skill/

验证Skill是否加载成功
--------------------
启动CoPaw后，AI会在系统提示中看到：

## text_analyzer
文本分析技能，用于统计文本字数、分析词频...
Check "path/to/text_analyzer/SKILL.md" for how to use this skill
    """)

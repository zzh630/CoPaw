# -*- coding: utf-8 -*-
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
        self._chinese_pattern = re.compile(r'[一-鿿]')
        self._english_pattern = re.compile(r'[a-zA-Z]+')
    
    def get_basic_stats(self) -> Dict[str, int]:
        """获取基础统计信息
        
        Returns:
            包含字数、行数、段落数、句子数的字典
        """
        lines = self.text.split('\n')
        paragraphs = [p for p in self.text.split('\n\n') if p.strip()]
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

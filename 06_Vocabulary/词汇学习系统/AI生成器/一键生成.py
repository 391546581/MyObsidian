#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键生成词汇笔记 - 简化版
适合快速使用,无需复杂配置
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from AI词汇生成器 import AIVocabularyGenerator


def quick_generate():
    """快速生成模式"""
    
    print("="*60)
    print("🚀 一键生成词汇笔记")
    print("="*60)
    
    # 简化的配置
    print("\n📝 请输入单词 (多个单词用空格分隔):")
    words_input = input("> ").strip()
    
    if not words_input:
        print("❌ 未输入单词")
        return
    
    word_list = words_input.split()
    
    print(f"\n✅ 将生成 {len(word_list)} 个词汇笔记")
    print(f"📋 单词列表: {', '.join(word_list)}")
    
    # 询问是否使用AI
    print("\n🤖 是否使用AI生成? (需要API密钥)")
    print("   y - 使用AI (高质量,需要API密钥)")
    print("   n - 使用模板 (快速,需要手动填写)")
    
    use_ai = input("> ").strip().lower() == 'y'
    
    if use_ai:
        api_key = input("\n请输入API密钥: ").strip()
        if not api_key:
            print("⚠️  未输入API密钥,切换到模板模式")
            use_ai = False
    
    # 创建生成器
    if use_ai:
        generator = AIVocabularyGenerator(api_key=api_key)
    else:
        generator = AIVocabularyGenerator()
    
    # 批量生成
    print(f"\n🔄 开始生成...")
    
    created_files = generator.batch_generate(
        word_list,
        brand='Brand7',  # 默认Brand7
        theme=None,
        include_images=False  # 默认不生成图片
    )
    
    print(f"\n✅ 完成! 已创建 {len(created_files)} 个笔记")
    print("\n📂 笔记位置:")
    for f in created_files:
        print(f"   - {f}")
    
    print("\n💡 下一步:")
    print("   1. 在Obsidian中打开笔记")
    print("   2. 补充/修改内容(如果使用模板模式)")
    print("   3. 使用SR插件开始复习")


def demo_mode():
    """演示模式 - 生成3个示例词汇"""
    
    print("="*60)
    print("🎯 演示模式 - 生成3个示例词汇")
    print("="*60)
    
    demo_words = ['crucial', 'acquire', 'mitigate']
    
    print(f"\n将生成示例词汇: {', '.join(demo_words)}")
    print("使用模板模式(无需API密钥)\n")
    
    generator = AIVocabularyGenerator()
    
    created_files = generator.batch_generate(
        demo_words,
        brand='Brand7',
        theme='教育',
        include_images=False
    )
    
    print(f"\n✅ 演示完成! 已创建 {len(created_files)} 个笔记")
    print("\n请在Obsidian中查看生成的笔记,了解模板结构")


if __name__ == '__main__':
    print("\n选择模式:")
    print("1. 快速生成 (输入自己的单词)")
    print("2. 演示模式 (生成3个示例)")
    
    choice = input("\n请选择 (1/2): ").strip()
    
    if choice == '1':
        quick_generate()
    elif choice == '2':
        demo_mode()
    else:
        print("❌ 无效选择")

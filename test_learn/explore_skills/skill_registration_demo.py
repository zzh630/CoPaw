# -*- coding: utf-8 -*-
"""
Skills 解析和传递流程示例

本示例演示：
1. 如何创建一个skill
2. 如何注册skill到toolkit
3. 如何获取skill的prompt
4. AI如何读取和使用skill
"""
import os
import tempfile
from pathlib import Path
from agentscope.tool import Toolkit


def create_sample_skill(skill_dir: Path, name: str, description: str) -> None:
    """
    创建一个示例skill目录结构
    
    Args:
        skill_dir: skill目录路径
        name: skill名称
        description: skill描述
    """
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    skill_md_content = f"""---
name: {name}
description: "{description}"
---

# {name} Skill

## 概述
这是一个示例skill，用于演示skill的解析流程。

## 使用方法
1. 读取输入文件
2. 处理数据
3. 输出结果

## 示例
```python
# 示例代码
result = process_data(input_file)
print(result)
```

## 注意事项
- 确保输入文件格式正确
- 处理大文件时注意内存使用
"""
    
    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md_content, encoding="utf-8")
    
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    
    script_content = '''# -*- coding: utf-8 -*-
"""示例脚本"""
def process_data(input_file: str) -> str:
    """处理数据"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data.upper()
'''
    
    script_path = scripts_dir / "process.py"
    script_path.write_text(script_content, encoding="utf-8")
    
    print(f"✓ 创建skill: {name}")
    print(f"  目录: {skill_dir}")
    print(f"  SKILL.md: {skill_md_path}")
    print(f"  scripts: {scripts_dir}")


def demo_skill_registration():
    """演示skill注册流程"""
    print("\n" + "="*60)
    print("Skills 解析和传递流程演示")
    print("="*60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        print("\n【步骤1】创建示例skills")
        print("-" * 60)
        
        skill1_dir = tmpdir_path / "data_processor"
        create_sample_skill(
            skill1_dir,
            name="data_processor",
            description="数据处理技能，用于读取、处理和转换数据文件"
        )
        
        skill2_dir = tmpdir_path / "report_generator"
        create_sample_skill(
            skill2_dir,
            name="report_generator",
            description="报告生成技能，用于创建格式化的报告文档"
        )
        
        print("\n【步骤2】创建Toolkit并注册skills")
        print("-" * 60)
        
        toolkit = Toolkit()
        
        toolkit.register_agent_skill(str(skill1_dir))
        print(f"✓ 注册skill: data_processor")
        
        toolkit.register_agent_skill(str(skill2_dir))
        print(f"✓ 注册skill: report_generator")
        
        print("\n【步骤3】查看注册的skills")
        print("-" * 60)
        print(f"已注册 {len(toolkit.skills)} 个skills:")
        for skill_name, skill_info in toolkit.skills.items():
            print(f"  - {skill_name}:")
            print(f"      描述: {skill_info['description']}")
            print(f"      目录: {skill_info['dir']}")
        
        print("\n【步骤4】获取skill prompt（传给AI的内容）")
        print("-" * 60)
        
        skill_prompt = toolkit.get_agent_skill_prompt()
        
        if skill_prompt:
            print("生成的skill prompt:")
            print("\n" + "="*60)
            print(skill_prompt)
            print("="*60)
        else:
            print("没有注册的skills")
        
        print("\n【步骤5】模拟AI如何使用skill")
        print("-" * 60)
        print("""
AI的工作流程：
1. 在系统提示中看到所有可用skills的名称和描述
2. 根据用户任务判断需要使用哪个skill
   例如：用户说"帮我处理这个数据文件"
   AI判断需要使用 'data_processor' skill
3. 使用read_file工具读取对应的SKILL.md文件
   read_file("path/to/data_processor/SKILL.md")
4. 按照SKILL.md中的指令执行任务
5. 可能调用scripts目录下的脚本
        """)
        
        print("\n【步骤6】演示读取SKILL.md内容")
        print("-" * 60)
        
        skill_md_path = skill1_dir / "SKILL.md"
        content = skill_md_path.read_text(encoding="utf-8")
        print(f"读取 {skill_md_path.name} 的内容：")
        print("\n" + "="*60)
        print(content[:500] + "..." if len(content) > 500 else content)
        print("="*60)
        
        print("\n【步骤7】演示完整的系统提示结构")
        print("-" * 60)
        
        original_sys_prompt = """你是一个智能助手，名叫Friday。
你的任务是帮助用户完成各种任务。

请根据用户的需求，选择合适的工具和技能来完成任务。"""
        
        full_sys_prompt = original_sys_prompt + "\n\n" + skill_prompt
        
        print("完整的系统提示结构：")
        print("\n" + "="*60)
        print(full_sys_prompt)
        print("="*60)
        
        print("\n【总结】")
        print("-" * 60)
        print("""
Skills解析和传递流程：
1. Skill目录结构：SKILL.md + scripts/ + references/
2. 注册：toolkit.register_agent_skill(skill_dir)
3. 解析：读取SKILL.md的YAML Front Matter（name, description）
4. 存储：保存到toolkit.skills字典
5. 传递：通过get_agent_skill_prompt()生成prompt
6. AI使用：在系统提示中看到skill列表，按需读取SKILL.md

关键设计：
- 渐进式披露：只在系统提示中展示名称和描述
- 按需加载：AI需要时才读取完整内容
- 模块化：每个skill独立管理
- 标准化：遵循Anthropic Agent Skill标准
        """)


def demo_skill_with_custom_template():
    """演示自定义skill模板"""
    print("\n" + "="*60)
    print("自定义Skill模板演示")
    print("="*60)
    
    custom_instruction = """# 可用技能列表
以下是系统内置的专业技能，你可以根据任务需求选择使用。
每个技能都有详细的操作手册，使用前请先阅读SKILL.md文件。"""
    
    custom_template = """### {name}
{description}

📁 技能目录: {dir}
📖 使用说明: 请阅读 {dir}/SKILL.md"""
    
    toolkit = Toolkit(
        agent_skill_instruction=custom_instruction,
        agent_skill_template=custom_template,
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        skill_dir = tmpdir_path / "custom_skill"
        create_sample_skill(
            skill_dir,
            name="custom_skill",
            description="自定义模板示例技能"
        )
        
        toolkit.register_agent_skill(str(skill_dir))
        
        skill_prompt = toolkit.get_agent_skill_prompt()
        print("\n使用自定义模板生成的prompt：")
        print("="*60)
        print(skill_prompt)
        print("="*60)


if __name__ == "__main__":
    demo_skill_registration()
    print("\n\n")
    demo_skill_with_custom_template()

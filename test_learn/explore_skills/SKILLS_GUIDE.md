# Skills 解析和传递流程总结

## 📚 示例文件说明

### 1. `skill_registration_demo.py`
演示skills的核心机制：
- ✅ 如何创建skill目录结构
- ✅ 如何注册skill到toolkit
- ✅ 如何生成skill prompt
- ✅ AI如何读取和使用skill
- ✅ 自定义skill模板

**运行方式：**
```bash
python test_learn/skill_registration_demo.py
```

### 2. `create_custom_skill.py`
创建一个完整的实用skill示例：
- ✅ 完整的skill目录结构（SKILL.md + scripts + references）
- ✅ 可运行的文本分析脚本
- ✅ 详细的使用说明和工作流程
- ✅ 集成到CoPaw的方法

**运行方式：**
```bash
python test_learn/create_custom_skill.py
```

---

## 🔄 Skills 解析和传递完整流程

### 1️⃣ Skill目录结构
```
skill_name/
├── SKILL.md              # 必需：核心说明文件
│   ├── YAML Front Matter # 必需：name, description
│   └── Markdown Body     # 详细使用说明
├── scripts/              # 可选：执行脚本
│   ├── analyzer.py
│   └── utils.py
└── references/           # 可选：参考资料
    ├── stopwords.txt
    └── templates/
```

### 2️⃣ 注册流程
```python
# react_agent.py:215-227
def _register_skills(self, toolkit: Toolkit):
    ensure_skills_initialized()
    working_skills_dir = get_working_skills_dir()
    available_skills = list_available_skills()
    
    for skill_name in available_skills:
        skill_dir = working_skills_dir / skill_name
        toolkit.register_agent_skill(str(skill_dir))
```

### 3️⃣ 解析流程
```python
# AgentScope: _toolkit.py:1042-1104
def register_agent_skill(self, skill_dir: str):
    # 1. 检查目录和SKILL.md文件
    path_skill_md = os.path.join(skill_dir, "SKILL.md")
    
    # 2. 解析YAML Front Matter
    with open(path_skill_md, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)
    
    # 3. 提取元数据
    name = post.get("name")
    description = post.get("description")
    
    # 4. 存储到skills字典
    self.skills[name] = AgentSkill(
        name=name,
        description=description,
        dir=skill_dir,
    )
```

### 4️⃣ 传递给AI
```python
# AgentScope: _react_agent.py:367-373
@property
def sys_prompt(self) -> str:
    agent_skill_prompt = self.toolkit.get_agent_skill_prompt()
    if agent_skill_prompt:
        return self._sys_prompt + "\n\n" + agent_skill_prompt
    else:
        return self._sys_prompt

# AgentScope: _toolkit.py:1126-1153
def get_agent_skill_prompt(self) -> str | None:
    skill_descriptions = [
        self._agent_skill_instruction,
    ] + [
        self._agent_skill_template.format(
            name=_["name"],
            description=_["description"],
            dir=_["dir"],
        )
        for _ in self.skills.values()
    ]
    return "\n".join(skill_descriptions)
```

### 5️⃣ AI使用流程
```
┌─────────────────────────────────────────────────────────┐
│ 用户请求："帮我分析这个文本文件"                          │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 【步骤1】AI查看系统提示中的skills列表                     │
│                                                          │
│ ## text_analyzer                                        │
│ 文本分析技能，用于统计文本字数、分析词频...              │
│ Check "path/to/text_analyzer/SKILL.md" for details     │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 【步骤2】AI决定使用text_analyzer skill                   │
│                                                          │
│ 匹配度：用户需求"分析文本" ↔ skill描述"文本分析"        │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 【步骤3】AI使用read_file工具读取SKILL.md                 │
│                                                          │
│ read_file("path/to/text_analyzer/SKILL.md")            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 【步骤4】AI按照SKILL.md中的指令执行任务                   │
│                                                          │
│ 1. 读取用户文件                                          │
│ 2. 运行分析脚本                                          │
│ 3. 整理结果返回                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 核心设计理念

### 1. 渐进式披露（Progressive Disclosure）
- **系统提示**：只显示skill的名称和描述（节省token）
- **按需加载**：AI需要时才读取完整的SKILL.md
- **分层信息**：从概览到详细，逐步深入

### 2. 模块化设计
- 每个skill独立管理
- 易于扩展和维护
- 支持自定义模板

### 3. 标准化规范
- 遵循Anthropic Agent Skill开放标准
- 统一的目录结构
- 标准的YAML Front Matter格式

---

## 🔧 实际应用示例

### 示例1：使用text_analyzer skill

**用户输入：**
```
帮我分析这段文本的字数和关键词：
"Python is a powerful programming language..."
```

**AI处理流程：**
1. 识别需求 → 文本分析
2. 选择skill → text_analyzer
3. 读取SKILL.md → 了解使用方法
4. 执行分析 → 运行脚本
5. 返回结果 → 格式化输出

### 示例2：使用pptx skill

**用户输入：**
```
帮我创建一个产品介绍PPT
```

**AI处理流程：**
1. 识别需求 → PPT创建
2. 选择skill → pptx
3. 读取SKILL.md → 了解创建方法
4. 选择方案 → 使用pptxgenjs或模板
5. 执行创建 → 生成PPT文件

---

## 📊 对比：传统方式 vs Skills方式

### 传统方式（硬编码）
```python
# 所有逻辑都在代码中
def create_ppt(content):
    # 1000行代码...
    pass

def analyze_text(text):
    # 500行代码...
    pass

# 问题：
# ❌ 难以维护
# ❌ 难以扩展
# ❌ 逻辑耦合
# ❌ 更新需要改代码
```

### Skills方式（模块化）
```python
# 每个skill独立管理
skills/
├── pptx/
│   └── SKILL.md  # 100行说明
├── text_analyzer/
│   └── SKILL.md  # 50行说明
└── ...

# 优势：
# ✅ 易于维护
# ✅ 易于扩展
# ✅ 逻辑解耦
# ✅ 更新只需修改SKILL.md
```

---

## 🚀 如何创建自己的Skill

### 步骤1：规划Skill功能
```
目标：创建一个[功能名称]skill
功能：[具体功能描述]
场景：[使用场景]
```

### 步骤2：创建目录结构
```bash
mkdir -p my_skill/scripts
mkdir -p my_skill/references
```

### 步骤3：编写SKILL.md
```markdown
---
name: my_skill
description: "技能描述，用于匹配用户需求"
---

# My Skill

## 功能说明
[详细说明]

## 使用方法
[具体步骤]

## 示例
[代码示例]
```

### 步骤4：编写脚本（可选）
```python
# scripts/main.py
def main():
    # 实现核心功能
    pass
```

### 步骤5：测试和部署
```bash
# 测试
python scripts/main.py

# 部署到CoPaw
cp -r my_skill ~/.copaw/skills/
# 或
cp -r my_skill src/copaw/agents/skills/
```

---

## 💡 最佳实践

### 1. SKILL.md编写技巧
- ✅ description要准确，便于AI匹配
- ✅ 提供清晰的使用步骤
- ✅ 包含具体的代码示例
- ✅ 说明注意事项和限制

### 2. 脚本设计原则
- ✅ 独立运行，无外部依赖
- ✅ 提供清晰的输入输出
- ✅ 包含错误处理
- ✅ 添加使用示例

### 3. 目录组织建议
```
skill_name/
├── SKILL.md           # 必需
├── README.md          # 可选，开发者文档
├── scripts/           # 执行脚本
│   ├── main.py        # 主脚本
│   └── utils.py       # 工具函数
└── references/        # 参考资源
    ├── templates/     # 模板文件
    └── examples/      # 示例文件
```

---

## 📖 相关文件

- **核心实现**：[react_agent.py](../src/copaw/agents/react_agent.py)
- **Skill管理**：[skills_manager.py](../src/copaw/agents/skills_manager.py)
- **AgentScope Toolkit**：`agentscope/tool/_toolkit.py`
- **内置Skills**：[src/copaw/agents/skills/](../src/copaw/agents/skills/)

---

## 🎓 学习路径

1. **入门**：运行 `skill_registration_demo.py` 了解基本流程
2. **实践**：运行 `create_custom_skill.py` 创建完整skill
3. **深入**：阅读内置skills（pptx, pdf, xlsx等）
4. **应用**：创建自己的skill并集成到项目中

---

## ❓ 常见问题

### Q1: Skill没有被加载？
**A:** 检查以下几点：
- SKILL.md文件是否存在
- YAML Front Matter是否包含name和description
- skill目录是否在正确的位置

### Q2: 如何调试Skill？
**A:** 
- 直接运行scripts目录下的脚本
- 使用print语句输出中间结果
- 查看CoPaw日志中的skill加载信息

### Q3: Skill可以调用其他Skill吗？
**A:** 可以，AI可以根据需要依次使用多个skills完成复杂任务。

### Q4: 如何更新Skill？
**A:** 直接修改SKILL.md或scripts，重启CoPaw即可生效。

---

## 🌟 总结

Skills是CoPaw的核心扩展机制，通过：
- **标准化格式**：统一的SKILL.md结构
- **渐进式披露**：节省token，按需加载
- **模块化设计**：易于维护和扩展
- **开放标准**：遵循Anthropic Agent Skill规范

让AI能够灵活地使用各种专业技能，实现强大的功能扩展能力。

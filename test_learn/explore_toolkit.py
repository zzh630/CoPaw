
# -*- coding: utf-8 -*-
"""探索 Toolkit 如何获取函数参数"""
from agentscope.tool import Toolkit
from copaw.agents.tools.browser_control import browser_use
import json

def main():
    # 创建 Toolkit 并注册 browser_use
    toolkit = Toolkit()
    toolkit.register_tool_function(browser_use)
    
    # 获取 JSON schemas
    schemas = toolkit.get_json_schemas()
    
    print("=== 工具的 JSON Schema ===")
    print(json.dumps(schemas, ensure_ascii=False, indent=2))
    
    print("\n=== browser_use 函数的详细信息 ===")
    import inspect
    sig = inspect.signature(browser_use)
    print("函数签名:", sig)
    print("\n参数详情:")
    for name, param in sig.parameters.items():
        print(f"  {name}:")
        print(f"    类型: {param.annotation}")
        print(f"    默认值: {param.default}")
        print(f"    类型: {param.kind}")

if __name__ == "__main__":
    main()

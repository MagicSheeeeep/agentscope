#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证快速启动指南中的脚本路径和文件
"""

import os

def validate_guide_references():
    """验证快速启动指南中引用的文件是否存在"""
    print("🔍 验证快速启动指南中的文件引用")
    print("=" * 50)
    
    # 需要验证的文件列表
    files_to_check = [
        # 主要脚本
        "cursor/scripts/simple_chat.py",
        "cursor/scripts/start_agentscope_fixed.py",
        "cursor/scripts/chat_with_studio.py", 
        "cursor/scripts/config_file_demo.py",
        "cursor/scripts/simple_test.py",
        "cursor/scripts/final_solution.py",
        
        # 高级示例
        "cursor/scripts/same_model_multi_agents.py",
        "cursor/scripts/multi_model_orchestration.py",
        "cursor/scripts/simple_same_model_example.py",
        "cursor/scripts/simple_orchestration_example.py",
        "cursor/scripts/run_same_model_demo.py",
        
        # 实用工具
        "cursor/scripts/get_correct_studio_url.py",
        "cursor/scripts/realtime_test.py",
        
        # 测试文件
        "cursor/tests/test_interactive.py",
        "cursor/tests/test_start_script.py",
        
        # 配置和文档
        "cursor/configs/model_configs.json",
        "cursor/docs/快速启动指南.md",
        "cursor/docs/README_MultiModel.md",
        "cursor/docs/README_SameModel.md",
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print(f"\n📊 验证结果:")
    print(f"✅ 存在的文件: {len(existing_files)}")
    print(f"❌ 缺失的文件: {len(missing_files)}")
    
    if missing_files:
        print(f"\n⚠️ 缺失的文件列表:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print(f"\n🎉 所有文件都存在，快速启动指南的引用是正确的！")
        return True

def check_script_directories():
    """检查脚本目录结构"""
    print(f"\n📂 检查目录结构")
    print("=" * 30)
    
    directories = [
        "cursor/scripts",
        "cursor/configs", 
        "cursor/docs",
        "cursor/tests"
    ]
    
    for dir_path in directories:
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            print(f"✅ {dir_path}/ ({len(files)} 个文件)")
            for file in sorted(files)[:5]:  # 显示前5个文件
                print(f"   - {file}")
            if len(files) > 5:
                print(f"   ... 共 {len(files)} 个文件")
        else:
            print(f"❌ {dir_path}/ (不存在)")
        print()

def main():
    """主函数"""
    print("🚀 AgentScope 快速启动指南验证工具")
    print("=" * 60)
    
    # 验证文件引用
    guide_valid = validate_guide_references()
    
    # 检查目录结构
    check_script_directories()
    
    if guide_valid:
        print("✅ 验证完成：快速启动指南可以正常使用！")
        print("💡 您可以按照指南中的路径运行脚本")
    else:
        print("❌ 验证失败：快速启动指南中有文件路径错误")
        print("💡 请检查缺失的文件并修正路径")

if __name__ == "__main__":
    main() 
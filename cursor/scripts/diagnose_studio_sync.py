#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope Studio 同步问题诊断工具
全面检查并修复Command+C状态同步和对话信息同步问题
"""

import requests
import json
import time
import glob
import os
import subprocess
import signal
import psutil
from datetime import datetime

def check_running_processes():
    """检查AgentScope相关进程"""
    print("🔍 检查运行中的AgentScope相关进程...")
    
    agentscope_processes = []
    studio_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = proc.info['name'].lower()
            cmdline_list = proc.info['cmdline']
            cmdline = ' '.join(cmdline_list).lower() if cmdline_list else ''
            
            if 'agentscope' in name or 'agentscope' in cmdline:
                agentscope_processes.append(proc.info)
            
            if 'studio' in name or 'as_studio' in cmdline or ('node' in name and 'studio' in cmdline):
                studio_processes.append(proc.info)
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
            continue
    
    print(f"📊 AgentScope进程: {len(agentscope_processes)} 个")
    for proc in agentscope_processes[:3]:  # 只显示前3个
        print(f"  PID {proc['pid']}: {proc['name']}")
    
    print(f"📊 Studio进程: {len(studio_processes)} 个")  
    for proc in studio_processes[:3]:
        print(f"  PID {proc['pid']}: {proc['name']}")
    
    return agentscope_processes, studio_processes

def check_studio_endpoints():
    """检查Studio可用的API端点"""
    print("\n🔍 检查Studio API端点...")
    
    base_urls = [
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    for base_url in base_urls:
        print(f"\n🌐 测试: {base_url}")
        
        # 测试基本连接
        try:
            response = requests.get(base_url, timeout=3)
            print(f"  ✅ 基本连接: {response.status_code}")
            
            if response.status_code == 200:
                # 测试trpc端点
                trpc_endpoints = [
                    "getRuns", "registerRun", "updateRun", "pushMessage", 
                    "heartbeat", "health", "status"
                ]
                
                working_endpoints = []
                for endpoint in trpc_endpoints:
                    try:
                        url = f"{base_url}/trpc/{endpoint}"
                        resp = requests.get(url, timeout=2)
                        if resp.status_code in [200, 400, 404]:  # 400/404也说明端点存在
                            working_endpoints.append(endpoint)
                    except:
                        pass
                
                print(f"  🔗 可用端点: {working_endpoints}")
                
                if working_endpoints:
                    return base_url, working_endpoints
                    
        except Exception as e:
            print(f"  ❌ 连接失败: {e}")
    
    return None, []

def analyze_run_configs():
    """分析运行配置的差异"""
    print("\n🔍 分析运行记录配置差异...")
    
    runs_dir = "runs"
    if not os.path.exists(runs_dir):
        print("❌ runs目录不存在")
        return
    
    run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
    if not run_dirs:
        print("❌ 没有找到运行记录")
        return
    
    # 按时间排序
    run_dirs.sort(key=os.path.getmtime, reverse=True)
    
    print(f"📊 分析最新的 5 个运行记录...")
    
    # 用于统计的配置项
    config_stats = {
        'studio_url_null': 0,
        'studio_url_correct': 0,
        'save_api_invoke_false': 0,
        'save_api_invoke_true': 0,
        'use_monitor_false': 0,
        'use_monitor_true': 0,
        'has_agentscope_db': 0,
        'no_agentscope_db': 0
    }
    
    detailed_analysis = []
    
    for i, run_dir in enumerate(run_dirs[:5]):
        run_id = os.path.basename(run_dir)
        config_file = os.path.join(run_dir, ".config")
        
        analysis = {
            'run_id': run_id,
            'config_exists': False,
            'studio_url': None,
            'save_api_invoke': None,
            'use_monitor': None,
            'has_db': False,
            'can_display_chat': False
        }
        
        if os.path.exists(config_file):
            analysis['config_exists'] = True
            
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                # 分析配置项
                studio_url = config.get('studio_url')
                save_api_invoke = config.get('file', {}).get('save_api_invoke', False)
                use_monitor = config.get('monitor', {}).get('use_monitor', False)
                
                analysis['studio_url'] = studio_url
                analysis['save_api_invoke'] = save_api_invoke
                analysis['use_monitor'] = use_monitor
                
                # 检查数据库文件
                db_path = os.path.join(run_dir, "agentscope.db")
                analysis['has_db'] = os.path.exists(db_path)
                
                # 判断是否能显示对话
                analysis['can_display_chat'] = (
                    studio_url is not None and 
                    save_api_invoke and 
                    use_monitor
                )
                
                # 更新统计
                if studio_url is None:
                    config_stats['studio_url_null'] += 1
                else:
                    config_stats['studio_url_correct'] += 1
                
                if save_api_invoke:
                    config_stats['save_api_invoke_true'] += 1
                else:
                    config_stats['save_api_invoke_false'] += 1
                
                if use_monitor:
                    config_stats['use_monitor_true'] += 1
                else:
                    config_stats['use_monitor_false'] += 1
                
                if analysis['has_db']:
                    config_stats['has_agentscope_db'] += 1
                else:
                    config_stats['no_agentscope_db'] += 1
                
            except Exception as e:
                print(f"⚠️ 读取配置失败: {run_id} - {e}")
        
        detailed_analysis.append(analysis)
    
    # 显示详细分析
    print("\n📋 详细分析结果:")
    for analysis in detailed_analysis:
        status = "✅ 可显示对话" if analysis['can_display_chat'] else "❌ 不能显示对话"
        print(f"\n🔸 {analysis['run_id']}: {status}")
        print(f"   studio_url: {analysis['studio_url']}")
        print(f"   save_api_invoke: {analysis['save_api_invoke']}")
        print(f"   use_monitor: {analysis['use_monitor']}")
        print(f"   has_db: {analysis['has_db']}")
    
    # 显示统计信息
    print(f"\n📊 配置统计:")
    print(f"   studio_url为null: {config_stats['studio_url_null']} 个")
    print(f"   studio_url正确: {config_stats['studio_url_correct']} 个")
    print(f"   save_api_invoke为false: {config_stats['save_api_invoke_false']} 个")
    print(f"   save_api_invoke为true: {config_stats['save_api_invoke_true']} 个")
    print(f"   use_monitor为false: {config_stats['use_monitor_false']} 个")
    print(f"   use_monitor为true: {config_stats['use_monitor_true']} 个")
    
    return detailed_analysis

def get_running_status_from_config():
    """从配置文件获取仍在运行的记录"""
    print("\n🔍 检查配置文件中的运行状态...")
    
    runs_dir = "runs"
    if not os.path.exists(runs_dir):
        return []
    
    run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
    potentially_running = []
    
    for run_dir in run_dirs:
        run_id = os.path.basename(run_dir)
        config_file = os.path.join(run_dir, ".config")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                pid = config.get('pid', -1)
                
                # 检查进程是否还在运行
                try:
                    if pid > 0 and psutil.pid_exists(pid):
                        process = psutil.Process(pid)
                        if process.is_running():
                            potentially_running.append({
                                'run_id': run_id,
                                'pid': pid,
                                'name': process.name(),
                                'status': process.status()
                            })
                except:
                    pass
            except:
                pass
    
    if potentially_running:
        print(f"⚠️ 发现 {len(potentially_running)} 个可能仍在运行的记录:")
        for item in potentially_running:
            print(f"   {item['run_id']} (PID: {item['pid']}, 状态: {item['status']})")
    else:
        print("✅ 没有发现仍在运行的记录")
    
    return potentially_running

def main():
    """主诊断流程"""
    print("🔧 AgentScope Studio 同步问题诊断工具")
    print("=" * 60)
    print("🎯 诊断目标:")
    print("1. Command+C后状态同步问题")
    print("2. 对话信息无法同步到可视化界面")
    print("=" * 60)
    
    # 1. 检查进程状态
    agentscope_procs, studio_procs = check_running_processes()
    
    # 2. 检查Studio连接和端点
    studio_url, endpoints = check_studio_endpoints()
    
    # 3. 分析运行配置差异
    analysis_results = analyze_run_configs()
    
    # 4. 检查运行状态
    running_records = get_running_status_from_config()
    
    # 生成诊断报告
    print("\n" + "="*60)
    print("📋 诊断报告")
    print("="*60)
    
    print(f"\n🔸 进程状态:")
    if studio_procs:
        print("✅ Studio进程正在运行")
    else:
        print("❌ 没有发现Studio进程")
        print("💡 请运行: as_studio")
    
    print(f"\n🔸 Studio连接:")
    if studio_url:
        print(f"✅ Studio可访问: {studio_url}")
        print(f"🔗 可用端点: {endpoints}")
    else:
        print("❌ 无法连接到Studio")
        print("💡 请确保Studio正在运行")
    
    print(f"\n🔸 配置问题:")
    if analysis_results:
        working_count = sum(1 for a in analysis_results if a['can_display_chat'])
        total_count = len(analysis_results)
        print(f"📊 能显示对话的记录: {working_count}/{total_count}")
        
        if working_count < total_count:
            print("⚠️ 发现配置问题，需要修复:")
            print("   - studio_url 为 null")
            print("   - save_api_invoke 为 false") 
            print("   - use_monitor 为 false")
    
    print(f"\n🔸 运行状态:")
    if running_records:
        print("⚠️ 有记录可能仍显示为Running状态")
        print("💡 这些进程实际上可能已经结束")
    else:
        print("✅ 没有发现状态异常的记录")
    
    print(f"\n💡 解决建议:")
    print("1. 确保Studio正在运行: as_studio")
    print("2. 使用修复脚本修正配置: python3 cursor/scripts/fix_studio_issues_final.py")
    print("3. 使用实时同步脚本: python3 cursor/scripts/chat_with_studio_realtime.py")
    print("4. 手动刷新浏览器页面: Cmd+Shift+R")

if __name__ == "__main__":
    main() 
# Ollama 相关命令参考

本文档包含了 Ollama 的常用命令，帮助您快速查询、管理和运行大语言模型。

## 📋 目录
- [模型查询命令](#模型查询命令)
- [模型运行命令](#模型运行命令)
- [模型管理命令](#模型管理命令)
- [服务管理命令](#服务管理命令)
- [其他实用命令](#其他实用命令)

---

## 🔍 模型查询命令

### 列出本地已安装的模型
```bash
ollama list
```
显示本地已安装的所有模型及其大小和修改时间。

### 搜索可用模型
```bash
ollama search <模型名称>
```
示例：
```bash
ollama search llama
ollama search codellama
```

### 查看模型详细信息
```bash
ollama show <模型名称>
```
示例：
```bash
ollama show llama3.2
ollama show codellama:7b
```

---

## 🚀 模型运行命令

### 启动模型进行对话
```bash
ollama run llama3.2:3b
```
```bash
ollama run qwen3:8b
```

### 运行模型并直接提问
```bash
ollama run <模型名称> "<问题>"
```
示例：
```bash
ollama run llama3.2 "Hello, how are you?"
ollama run codellama:7b "Write a Python function to calculate fibonacci"
```

### 从文件加载提示词
```bash
ollama run <模型名称> < prompt.txt
```

---

## 📦 模型管理命令

### 安装/下载模型
```bash
ollama pull <模型名称>
```
示例：
```bash
ollama pull llama3.2
ollama pull llama3.2:8b
ollama pull codellama:7b
ollama pull mistral:7b
```

### 删除模型
```bash
ollama rm <模型名称>
```
示例：
```bash
ollama rm llama3.2
ollama rm codellama:7b
```

### 复制模型
```bash
ollama cp <源模型> <目标模型>
```
示例：
```bash
ollama cp llama3.2 my-llama
```

---

## ⚙️ 服务管理命令

### 启动 Ollama 服务
```bash
ollama serve
```
在后台启动 Ollama 服务，默认监听端口 11434。

### 查看服务状态
```bash
ollama ps
```
显示当前正在运行的模型和资源使用情况。

### 停止正在运行的模型
如果模型正在运行，可以使用 `Ctrl+C` 停止当前对话，或者：
```bash
ollama stop <模型名称>
```

---

## 🛠️ 其他实用命令

### 查看 Ollama 版本
```bash
ollama --version
```
或
```bash
ollama version
```

### 查看帮助信息
```bash
ollama --help
```
或查看特定命令的帮助：
```bash
ollama run --help
ollama pull --help
```

### 查看模型文件位置
```bash
ollama env
```

---

## 💡 常用模型推荐

| 模型名称 | 大小 | 适用场景 | 拉取命令 |
|---------|------|----------|----------|
| llama3.2:1b | ~1GB | 轻量级对话 | `ollama pull llama3.2:1b` |
| llama3.2:3b | ~2GB | 日常对话 | `ollama pull llama3.2:3b` |
| llama3.2:8b | ~4.7GB | 高质量对话 | `ollama pull llama3.2:8b` |
| codellama:7b | ~3.8GB | 代码生成 | `ollama pull codellama:7b` |
| mistral:7b | ~4.1GB | 多语言支持 | `ollama pull mistral:7b` |

---

## 📝 使用示例

### 快速开始流程
1. 安装模型：
   ```bash
   ollama pull llama3.2
   ```

2. 运行模型：
   ```bash
   ollama run llama3.2
   ```

3. 开始对话：
   ```
   >>> Hello! Can you help me with Python programming?
   ```

### 批量管理
```bash
# 拉取多个模型
ollama pull llama3.2:1b llama3.2:3b codellama:7b

# 查看所有模型
ollama list

# 清理不需要的模型
ollama rm llama3.2:1b
```

---

## ⚠️ 注意事项

- 模型下载需要网络连接，大模型可能需要较长时间
- 确保有足够的磁盘空间存储模型文件
- 运行大模型需要足够的内存资源
- 首次运行模型时可能需要额外的加载时间

---

*更新时间：2024年12月* 
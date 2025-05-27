# 使用同一个大模型创建多智能体

## 概述

在AgentScope中，完全可以使用同一个大模型（如DashScope的qwen-max）创建多个不同角色的智能体。这种方式有以下优势：

- **成本效益**：只需要一个API密钥和模型配置
- **一致性**：所有智能体使用相同的语言模型基础
- **灵活性**：通过不同的系统提示和参数创建不同的角色特性
- **简化管理**：减少模型配置的复杂性

## 三种实现方式

### 方式1：共享模型配置

最简单的方式是创建一个共享的模型配置，所有智能体都使用这个配置。

```python
import agentscope
from agentscope.agents import DialogAgent

# 1. 定义共享的模型配置
model_config = {
    "config_name": "shared_qwen",
    "model_type": "dashscope_chat",
    "model_name": "qwen-max",
    "api_key": "your_api_key",
    "generate_args": {
        "temperature": 0.7
    }
}

# 2. 初始化AgentScope
agentscope.init(model_configs=[model_config])

# 3. 创建多个智能体，使用不同的系统提示
teacher = DialogAgent(
    name="老师",
    sys_prompt="你是一位经验丰富的老师，善于解释复杂概念。",
    model_config_name="shared_qwen"
)

student = DialogAgent(
    name="学生", 
    sys_prompt="你是一位好奇的学生，喜欢提问和学习。",
    model_config_name="shared_qwen"
)
```

### 方式2：同一模型，不同参数

使用同一个模型，但配置不同的参数（如temperature）来创建不同风格的智能体。

```python
# 创建多个配置，使用同一模型但不同参数
model_configs = [
    {
        "config_name": "conservative_qwen",
        "model_type": "dashscope_chat",
        "model_name": "qwen-max",
        "api_key": "your_api_key",
        "generate_args": {"temperature": 0.1}  # 保守，更确定性
    },
    {
        "config_name": "creative_qwen",
        "model_type": "dashscope_chat",
        "model_name": "qwen-max", 
        "api_key": "your_api_key",
        "generate_args": {"temperature": 0.9}  # 创意，更随机
    }
]

agentscope.init(model_configs=model_configs)

# 创建不同风格的智能体
analyst = DialogAgent(
    name="分析师",
    sys_prompt="你是一位严谨的数据分析师。",
    model_config_name="conservative_qwen"
)

creator = DialogAgent(
    name="创意师",
    sys_prompt="你是一位富有创意的设计师。",
    model_config_name="creative_qwen"
)
```

### 方式3：基于角色的系统提示

使用同一个配置，通过详细的角色系统提示来创建专业化的智能体。

```python
# 定义详细的角色提示
roles = {
    "技术专家": """你是一位资深技术专家。特点：
- 专注技术细节和实现方案
- 用专业术语但保持清晰
- 提供具体的技术建议
- 考虑技术可行性和性能""",
    
    "产品经理": """你是一位产品经理。特点：
- 关注用户需求和商业价值
- 平衡技术和业务目标
- 注重用户体验和市场反馈
- 制定产品策略和路线图"""
}

# 创建角色智能体
agents = {}
for role_name, prompt in roles.items():
    agents[role_name] = DialogAgent(
        name=role_name,
        sys_prompt=prompt,
        model_config_name="shared_qwen"
    )
```

## 实际应用场景

### 1. 团队协作模拟

```python
# 创建一个完整的产品开发团队
team_roles = {
    "产品经理": "负责产品规划和需求分析",
    "技术架构师": "负责技术方案设计",
    "UI设计师": "负责用户界面设计", 
    "测试工程师": "负责质量保证",
    "项目经理": "负责项目协调和进度管理"
}

team = {}
for role, description in team_roles.items():
    team[role] = DialogAgent(
        name=role,
        sys_prompt=f"你是团队中的{role}，{description}。请从你的专业角度提供建议。",
        model_config_name="shared_qwen"
    )
```

### 2. 教育场景

```python
# 创建教学环境
education_agents = {
    "数学老师": DialogAgent(
        name="数学老师",
        sys_prompt="你是一位数学老师，善于用简单易懂的方式解释数学概念。",
        model_config_name="shared_qwen"
    ),
    "学生助手": DialogAgent(
        name="学生助手", 
        sys_prompt="你是一位学习助手，帮助学生理解和练习知识点。",
        model_config_name="shared_qwen"
    ),
    "答疑专家": DialogAgent(
        name="答疑专家",
        sys_prompt="你专门解答学生的疑问，提供详细的解释和例子。",
        model_config_name="shared_qwen"
    )
}
```

### 3. 咨询服务

```python
# 创建多领域咨询团队
consultants = {
    "法律顾问": "你是专业律师，提供法律建议和风险评估。",
    "财务顾问": "你是财务专家，提供投资和理财建议。", 
    "健康顾问": "你是健康专家，提供健康和养生建议。",
    "职业顾问": "你是职业规划师，提供职业发展建议。"
}

consultant_agents = {}
for role, prompt in consultants.items():
    consultant_agents[role] = DialogAgent(
        name=role,
        sys_prompt=prompt,
        model_config_name="shared_qwen"
    )
```

## 多智能体交互模式

### 1. 顺序讨论

```python
async def sequential_discussion(agents, topic):
    """顺序讨论模式"""
    results = []
    for agent in agents:
        msg = Msg("user", f"关于'{topic}'，请提供你的观点", "user")
        response = agent(msg)
        results.append({
            "agent": agent.name,
            "response": response.content
        })
    return results
```

### 2. 协作解决问题

```python
async def collaborative_solving(agents, problem):
    """协作解决问题"""
    # 第一轮：各自分析
    analyses = {}
    for agent in agents:
        msg = Msg("user", f"请分析这个问题：{problem}", "user")
        response = agent(msg)
        analyses[agent.name] = response.content
    
    # 第二轮：综合讨论
    all_views = "\n".join([f"{name}: {view}" for name, view in analyses.items()])
    synthesis_prompt = f"基于以下观点，请提供综合解决方案：\n{all_views}"
    
    # 选择一个智能体进行综合
    synthesizer = agents[0]  # 或选择特定角色
    msg = Msg("user", synthesis_prompt, "user")
    final_solution = synthesizer(msg)
    
    return {
        "individual_analyses": analyses,
        "final_solution": final_solution.content
    }
```

### 3. 投票决策

```python
async def voting_decision(agents, options, question):
    """投票决策模式"""
    votes = {}
    reasons = {}
    
    for agent in agents:
        vote_prompt = f"""
问题：{question}
选项：{', '.join(options)}

请选择你认为最好的选项，并说明理由。
格式：选择：[选项] 理由：[理由]
"""
        msg = Msg("user", vote_prompt, "user")
        response = agent(msg)
        
        # 解析投票结果（简化版）
        if "选择：" in response.content:
            choice = response.content.split("选择：")[1].split()[0]
            votes[agent.name] = choice
            reasons[agent.name] = response.content
    
    return {"votes": votes, "reasons": reasons}
```

## 优化技巧

### 1. 角色一致性

```python
# 使用详细的角色描述确保一致性
detailed_prompt = """
你是一位资深的软件架构师，名叫Alex。

背景：
- 10年以上大型系统设计经验
- 专长于微服务架构和云原生技术
- 注重系统的可扩展性和可维护性

性格特点：
- 思维严谨，逻辑清晰
- 善于化繁为简
- 重视技术债务和长期维护

回答风格：
- 先分析问题本质
- 提供多种解决方案
- 说明优缺点和适用场景
- 给出具体的实施建议
"""
```

### 2. 上下文管理

```python
class ContextAwareAgent:
    def __init__(self, agent, context_limit=5):
        self.agent = agent
        self.context = []
        self.context_limit = context_limit
    
    def chat(self, message):
        # 添加上下文
        if len(self.context) >= self.context_limit:
            self.context.pop(0)
        
        context_prompt = "\n".join(self.context) + f"\n用户：{message}"
        msg = Msg("user", context_prompt, "user")
        response = self.agent(msg)
        
        # 更新上下文
        self.context.append(f"用户：{message}")
        self.context.append(f"{self.agent.name}：{response.content}")
        
        return response
```

### 3. 动态角色切换

```python
class DynamicRoleAgent:
    def __init__(self, base_config):
        self.base_config = base_config
        self.current_role = None
        self.agent = None
    
    def switch_role(self, role_name, role_prompt):
        """动态切换角色"""
        if self.current_role != role_name:
            self.agent = DialogAgent(
                name=role_name,
                sys_prompt=role_prompt,
                model_config_name=self.base_config
            )
            self.current_role = role_name
    
    def chat(self, message, role_name, role_prompt):
        self.switch_role(role_name, role_prompt)
        msg = Msg("user", message, "user")
        return self.agent(msg)
```

## 注意事项

1. **API限制**：注意API的调用频率限制和并发限制
2. **成本控制**：虽然使用同一模型，但多智能体会增加API调用次数
3. **角色区分**：确保不同角色的系统提示足够区分，避免角色混淆
4. **上下文长度**：注意模型的上下文长度限制
5. **一致性维护**：在长对话中保持角色的一致性

## 完整示例

参考提供的示例文件：
- `same_model_multi_agents.py` - 完整的多智能体系统
- `simple_same_model_example.py` - 简单的三种实现方式演示

这些示例展示了如何在实际项目中使用同一个DashScope模型创建功能丰富的多智能体系统。 
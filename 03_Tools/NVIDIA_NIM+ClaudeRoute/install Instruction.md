1. 第一步：获取 NVIDIA API Key
访问 NVIDIA NGC 平台：https://ngc.nvidia.com/
登录 / 注册 NVIDIA 账号（需实名认证，部分服务需绑定支付方式）。
进入「API Keys」页面（右上角头像 → Setup → API Keys）。
点击「Generate API Key」生成密钥，复制并保存（仅显示一次），建议存到安全的地方（如密码管理器）。

account :blue4wang@gmail.com 

nvidia-api-key nvapi-KkHpDG2WMKUBtjlFh4Uw9DowwGQ-RF-

2. 第二步：安装 Cloude cli 工具

3. 第三步：安装 claude-code-router 工具
https://github.com/musistudio/claude-code-router  
claude-code-router 核心作用
claude-code-router 是一个为解决「无 Anthropic 账号使用 Claude Code」及「路由 Claude Code 请求到其他大模型服务商」而生的工具，核心功能可总结为：
请求转发与格式转换Claude Code 原生仅调用 Anthropic API（api.anthropic.com），该项目通过 Express.js 实现 /v1/messages 端点，将 Claude Code 发出的 Anthropic 格式请求，转换为 OpenAI 兼容格式并路由到其他大模型服务商（如 DeepSeek、Gemini、Qwen、GLM 等），同时反向转换响应格式，让 Claude Code 能「识别」非 Anthropic 模型的返回结果。
多模型路由与适配支持按任务类型（思考、编码、长上下文、后台轻量任务等）分发请求到不同模型：
默认模型：兜底处理日常任务；
background：路由到本地 Ollama 处理轻量任务（对标 Claude Haiku 3.5）；
think：路由到 DeepSeek-R1 处理推理 / 规划任务；
longContext：处理 32K 以上长上下文场景，弥补 DeepSeek 长上下文短板；
同时通过 Transformer 接口适配不同服务商的参数差异（如 Gemini 的工具参数限制、OpenRouter 的缓存参数、DeepSeek 的 max_output 限制等）。
低成本使用 Claude Code核心目标是替代昂贵的 Anthropic 模型（如 Claude 3.5 Sonnet），转而使用低成本模型（如 DeepSeek-V3/R1，成本仅为前者 1/10），同时修复工具调用、提示词驱动等问题（如强制 DeepSeek 调用工具、引导 GLM-4.6 开启思维链）。
「配置了就可以直接用吗？」—— 并非完全「开箱即用」
该工具需要完成环境配置、代码 / 参数适配 才能正常工作，核心步骤包括：
1. 基础环境准备
依赖 Node.js（≥20.0.0）和 pnpm（≥8.0.0），需先安装；
克隆仓库后执行 pnpm install 安装依赖，再通过 pnpm build 构建项目。
2. 关键环境变量配置
Claude Code 本身支持通过环境变量覆盖核心配置，需在启动 Claude Code 前设置：
ANTHROPIC_BASE_URL：指向 claude-code-router 服务的地址（如 http://localhost:端口），让 Claude Code 的请求转发到该工具；
ANTHROPIC_API_KEY：自定义的密钥（无需真实 Anthropic 密钥），用于路由服务的鉴权；
目标模型服务商的密钥（如 DeepSeek API Key、Gemini API Key 等），需配置到 claude-code-router 的配置文件中。


4. 第四步：配置 claude-code-router 工具   z-ai/glm4.7  minimaxai/minimax-m2.1
![alt text](image.png)

![alt text](image-1.png)

![alt text](image-2.png)

![alt text](image-3.png)
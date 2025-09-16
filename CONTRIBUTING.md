# 贡献指南

感谢您考虑为视频合并工具做出贡献！这是一个开源项目，我们欢迎任何形式的贡献，包括但不限于：

- 代码贡献
- 文档改进
- 错误报告
- 功能建议
- 代码审查

## 开发环境设置

1. Fork 本仓库
2. 克隆您的 fork 到本地机器
   ```bash
   git clone https://github.com/YOUR_USERNAME/video-merger.git
   cd video-merger
   ```
3. 安装开发依赖
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
4. 创建新分支进行开发
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 代码风格

本项目遵循 PEP 8 代码风格指南。请确保您的代码符合以下要求：

- 使用 4 个空格进行缩进
- 每行代码不超过 79 个字符
- 使用有意义的变量名和函数名
- 为函数和类添加适当的文档字符串

我们使用 flake8 进行代码风格检查：

```bash
flake8 src tests
```

## 测试

在提交代码前，请确保所有测试都能通过：

```bash
python -m pytest tests/
```

如果您添加了新功能，请同时添加相应的测试。

## 提交 Pull Request

1. 确保您的代码通过了所有测试
2. 更新文档（如果需要）
3. 提交您的更改
   ```bash
   git commit -m "简明扼要的提交信息"
   ```
4. 推送到您的 fork
   ```bash
   git push origin feature/your-feature-name
   ```
5. 通过 GitHub 界面创建一个新的 Pull Request

## Pull Request 指南

- 请提供清晰的 PR 描述，说明您的更改解决了什么问题或添加了什么功能
- 如果您的 PR 解决了一个已存在的 issue，请在 PR 描述中引用该 issue（例如 "Fixes #123"）
- 确保 PR 只包含一个逻辑更改。如果您有多个不相关的更改，请创建多个 PR

## 问题报告

如果您发现了一个 bug 或有功能建议，请创建一个新的 issue。在创建 issue 时，请提供：

- 对问题的清晰描述
- 重现步骤（如果是 bug）
- 预期行为和实际行为
- 环境信息（操作系统、Python 版本等）

## 行为准则

请尊重所有项目参与者。我们期望所有贡献者遵循以下原则：

- 使用包容性语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情

## 许可证

通过贡献代码，您同意您的贡献将在项目的 MIT 许可证下发布。

感谢您的贡献！
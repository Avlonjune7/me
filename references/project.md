# 项目约定

- 更新 me 时同步 [GitHub me 仓库](https://github.com/Avlonjune7/me)、本机全局目录和 CC Switch 技能存储（本机为 `D:/DATA/cc switch/skills/me/`），核对文件一致性；安装与存储路径以实际配置为准。

- 个人 Codex 技能默认安装到用户级全局目录 `~/.agents/skills/`（本机为 `C:/Users/Tars/.agents/skills/`），安装或更新时复用该目录；用户明确要求项目级安装时再使用项目目录。同名技能保持单一安装位置。
- Windows 下额外安装 CLI、开发工具和工具链优先使用 WinGet，支持自选目录时放到 `D:\code\cli\<工具名>`。项目依赖跟随项目，固定路径遵循工具约定，已有安装按用户要求迁移。
- 查文档优先已有专用 CLI 或 Context7。
- Go 本机开发和测试使用宿主目标。部署 Debian 时按服务器架构构建 Linux 产物，纯 Go 可交叉编译，CGO 按项目依赖选择工具链。目标平台变量限于构建进程，部署后验证实际运行。
- 要求整理规范时维护项目代理说明文件（AGENTS.md / CLAUDE.md，依项目使用的工具选择）。项目明确采用 Astryx 时，允许其初始化与升级工具维护自身生成的指引区块。DESIGN.md 保存当前设计决定，历史另存。

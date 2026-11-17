# me

个人跨项目约定 skill，适用于 Codex 与 Claude Code。新项目或明确重新选型时 React 默认 Astryx、Vue 默认 shadcn-vue，已有项目沿用已确认体系。执行规则见 [SKILL.md](SKILL.md)，版本见 [CHANGELOG](CHANGELOG.md)。

设计目标与[全局 AGENTS.md](https://github.com/Avlonjune7/codex-global-agent/blob/main/AGENTS.md) 一致：响应快、执行快、省 token、节省上下文。全局规则常驻，me 按场景读取，项目文档承载项目自身的需求、架构与进度。

## 安装

个人使用默认用户级安装，克隆整个仓库并保留相对目录。同一工具的扫描范围内避免多个同名副本。

| 工具 | 用户级目录 | 项目级目录 | 调用 |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills/me/` | `.agents/skills/me/` | `$me ...` |
| Claude Code | `~/.claude/skills/me/` | `.claude/skills/me/` | `/me ...` |

```sh
git clone https://github.com/Avlonjune7/me.git ~/.agents/skills/me
```

安装后若未出现，重新开启会话。

## 怎么用

| 任务 | 方式 |
| --- | --- |
| 改文案、调整已有表单、修复明确的 UI 或后端问题 | 直接描述，不需要 me |
| 新建项目、选择或迁移组件体系 | 调用 me，说明技术栈、范围和已有约束 |
| 设计、重设计、评审、精修 | 明确说出“设计/重设计/评审”，使用 Impeccable |
| 页面慢、浏览器验收 | 描述复现步骤，需要个人验收偏好时调用 me |
| 工具安装、接口兼容、项目文档 | 调用 me，说明任务范围 |

```text
$me 新建一个 React 后台，按我的组件体系偏好完成用户列表页，包含搜索、分页和编辑弹窗。
$me 给订单状态增加取消状态，保证已有数据和旧调用方兼容。
$me 整理这个项目的需求、架构与进度文档，以 README 为入口。
```

## 结构

```text
me/
├── SKILL.md                  触发描述、默认选择、场景路由
├── references/
│   ├── project.md            开发环境、兼容性、项目文档
│   ├── components.md         组件复用与设计任务（UI 复用唯一来源）
│   ├── verification.md       验证、浏览器、性能、网页审查
│   └── cli-efficiency.md     CLI 与工具安装
├── evals/cases.md            任务评测用例
├── scripts/check.py          只读维护校验
├── CHANGELOG.md
└── CHANGELOG-archive.md
```

## 编写原则

- 只保留会改变执行选择的个人偏好，agent 已有的通用步骤不重复。
- 每条规则只在一个文件完整书写，其他位置引用。
- 规则改动由评测中观察到的误触发、漏读、重复实现、漏验收或耗时问题驱动；无数据不改。
- 改动攒批发布，每周最多一个版本。

## 更新与维护

仅在明确更新技能时同步，正常任务不联网检查版本。以 GitHub 为唯一来源：本机克隆安装后用 `git pull --ff-only` 更新；CC Switch 若能指向本机目录则直接指向，否则同步完整目录后用校验脚本核对。

版本约定：文字澄清递增补丁版本，兼容性新增递增次版本，改变既有规则含义或适用边界递增主版本。CHANGELOG 只保留近期条目，较早记录移入 CHANGELOG-archive.md。

### 只读校验

需要 Python 3.10+，仅标准库。检查 frontmatter、本地 Markdown 引用、参考文件是否都被 SKILL.md 路由，以及 SKILL.md 体量预算。

```sh
python scripts/check.py
python scripts/check.py --copy /path/to/installed/me
python scripts/check.py --cc-db /path/to/cc-switch.db --cc-skill-dir /path/to/cc-switch/skills/me --cc-id local:me
python scripts/check.py --git-ref origin/main
```

`--copy` 比较完整文件集及内容（忽略换行差异）；CC Switch 检查使用原始字节哈希并核对简介；`--git-ref` 只读本地 Git 引用，最新与否以本次 fetch 为准。成功返回 0，差异返回 1，读取失败返回 2。

### 任务评测

[评测用例](evals/cases.md) 用于衡量路由、读取量、返工与耗时，结果记录在 `evals/results/`。

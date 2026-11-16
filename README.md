# me

个人跨项目偏好 skill，新项目或明确重新选型时 React 默认使用 Astryx、Vue 默认使用 shadcn-vue，已有项目局部任务沿用已确认体系。通过主题和统一组件层落实 UI/UX 一致性，性能测量按任务与改动影响触发。补充适用的工具与安装偏好，适用于 Codex 与 Claude Code。版本与变更见 [CHANGELOG](CHANGELOG.md)。用户当次明确要求优先，项目约定与统一目标冲突时按 SKILL.md 明确目标体系。

## 安装与调用

个人使用默认选择用户级全局安装，项目级安装按用户明确要求执行。克隆整个仓库并保留相对目录。

| 工具 | 用户级目录 | 项目级目录 | 调用示例 |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills/me/` | `.agents/skills/me/` | `$me 按我的规范完成这个功能` |
| Claude Code | `~/.claude/skills/me/` | `.claude/skills/me/` | `/me 按我的规范完成这个功能` |

例如 Codex 用户级安装：

```sh
git clone https://github.com/Avlonjune7/me.git ~/.agents/skills/me
```

Claude Code 使用相同命令并将目标替换为 `~/.claude/skills/me`。组件体系选型、迁移、个人 UI 偏好或工具安装与项目约定需要明确时，按需使用本技能；安装后若未出现，重新开启会话。避免在同一工具的扫描范围安装多个同名副本。

## 日常怎么用

平时直接描述任务、预期结果和修改范围。组件选型、迁移或个人偏好需要明确时，可显式调用 me；Agent 根据技能简介和任务需要选择对应参考。

| 当前任务 | 使用方式 |
| --- | --- |
| 改按钮文案、调整已有表单或修复明确的 UI 问题 | 直接描述修改，沿用项目公共组件并验证受影响入口 |
| 新建项目、选择组件体系 | 调用 me，说明技术栈、产品用途及已有约束 |
| 统一界面或迁移组件库 | 调用 me，说明目标体系、页面范围和允许的迁移范围 |
| 页面卡顿、加载慢 | 描述复现步骤和症状，按需使用性能专业技能；需要个人验收偏好时补充 me |
| 后端修复、数据处理 | 直接描述任务，按实际问题使用专业工具与技能 |
| 工具安装、环境恢复、接口兼容性与项目文档 | 需要个人项目约定时调用 me，说明任务范围 |

### 调用示例

以下示例使用 Codex 的 `$me` 调用形式。Claude Code 使用上表中的 `/me` 形式。

```text
$me 新建一个 React 后台，按我的组件体系偏好完成用户列表页，包含搜索、分页和编辑弹窗。

$me 将订单页和个人中心统一到项目已确认的组件体系，复用现有主题和公共组件，验证相关交互。

$me 这个页面首次加载慢，按我的性能与验收偏好定位原因，比较优化前后的结果。

$me 安装这个开发工具，按我的原生环境和安装目录约定执行。

$me 整理这个持续开发项目的需求、架构与进度文档，复用已有内容，以 README 为入口。
```

局部修改可以直接描述，例如“把订单页提交按钮改成‘保存’，保持现有组件与样式”。明确要调整个人规范时，说明规则内容和同步范围，例如“更新 me 的工具安装偏好，并同步 GitHub、本机与 CC Switch”。

### 文档分工

- README 提供安装、用法、示例和维护说明。
- SKILL.md 提供 Agent 的触发描述、核心约束与参考入口。
- references 按当前问题提供组件、性能、验收和工具等细则。
- CHANGELOG 记录版本历史。执行依据为当前 SKILL.md 与适用参考。

具体执行规则在对应文件维护，README 通过链接说明用法。实际触发、读取范围与任务效果应结合运行记录验证。

## 结构与读取

```text
me/
├── SKILL.md
├── references/
│   ├── project.md
│   ├── cli-efficiency.md
│   ├── components.md
│   ├── web-review.md
│   ├── verification.md
│   └── performance.md
├── README.md
└── CHANGELOG.md
```

[SKILL.md](SKILL.md) 提供核心流程及触发条件，详细规则按任务读取：[项目开发](references/project.md)、[组件与设计系统](references/components.md)、[验证与交付](references/verification.md)、[性能](references/performance.md)、[网页审查](references/web-review.md)。明确微调无需加载所有参考。

版本统一记录在 CHANGELOG，README 与 CHANGELOG 供使用和维护时查阅。

## 按需使用的外部能力

| 场景 | 技能或工具 | 缺失时处理 |
| --- | --- | --- |
| React 复杂组件设计与重构 | vercel-composition-patterns | 沿用项目组件 API，结合项目 React 版本与官方资料 |
| React / Next.js 性能 | vercel-react-best-practices | 用项目测量工具定位瓶颈并查对应官方资料 |
| 网页专项审查 | web-design-guidelines | 依据项目规范和适用的 Web 标准检查，说明审查依据与覆盖缺口 |
| 组件体系、统一视觉与现代 Web 实现 | Astryx、shadcn-vue、Modern Web Guidance | 按项目目标体系查询官方资料，继续遵循统一组件层与复用约束 |
| 浏览器验证 | Playwright CLI、BrowserSkill | 使用可用且满足登录态和验证目标的工具，报告未验证部分 |

这些能力按任务使用，安装按用户要求或项目依赖执行。Vercel 技能可用 `npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices --skill web-design-guidelines --skill vercel-composition-patterns --agent codex --global --yes` 安装。web-design-guidelines 的审查流程要求获取最新远程规则，访问失败时需说明覆盖限制。

Windows 工具入口故障或需要压缩大量命令输出时读取 [CLI 偏好](references/cli-efficiency.md)。全局代理说明文件保留语言、原生环境、效率要求及按需技能入口，me 补充具体个人偏好。安装与同步位置见[项目约定](references/project.md)。

## 编写原则

只保留会改变执行选择的个人偏好与项目约定；Codex、Claude Code 等 agent 已有的通用步骤不在技能中重复展开。影响实际行为的例外仍需明确，例如默认组件体系、技术栈边界、环境复用及验证范围。此原则不意味着各 agent 的默认行为完全一致。

## 使用边界

[全局 AGENTS.md](https://github.com/Avlonjune7/codex-global-agent/blob/main/AGENTS.md) 维护常驻执行约束，me 按需补充个人约定，项目文档承载本项目的需求、架构和进度。

项目文档的创建、读取与更新范围见[项目约定](references/project.md#项目文档与进度)。整理项目代理说明时沿用该文件的对应规则。

## 更新与维护

仅在明确更新技能时同步本地副本，正常任务不联网检查版本。克隆安装可在确认工作区无未提交修改后执行 `git pull --ff-only`；复制安装则同步完整技能目录。更新目标及一致性核对要求统一见[项目约定](references/project.md)。

项目代理说明引用技能入口，项目专属决定保存在项目文档中。

仅纳入经过验证的跨项目经验；项目特例留在项目中。维护技能时更新相关参考与 CHANGELOG，说明原因、范围及实际同步状态，不在执行文档中重复版本和维护记录。

版本约定：文字澄清递增补丁版本，兼容性新增递增次版本，改变既有规则含义或适用边界递增主版本。

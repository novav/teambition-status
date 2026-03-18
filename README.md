# teambition-status

Teambition 项目状态查看与分析的 OpenClaw 技能：自动抓取项目页面数据并生成结构化报告，帮助快速了解项目进度、任务分布与风险点。

更完整的安装使用说明见 `teambition-status-INSTALL.md`。

## 功能特性

- 项目状态概览（项目整体状况快速查看）
- 任务统计（按分类/状态统计任务数量）
- 进度跟踪（监控完成情况与时间节点）
- 团队分析（成员工作负载分析）
- 风险识别（逾期任务与潜在风险识别）

## 前提条件

- 已安装并可运行 OpenClaw
- 已配置浏览器控制服务
- 已登录 Teambition 网页版，并能打开目标项目页面

## 快速开始（Windows 一键安装，推荐）

仓库已提供一键安装脚本与打包好的技能文件：

- `win_install/install-teambition-status.bat`
- `win_install/teambition-status.skill`

步骤：

1. 打开资源管理器进入 `win_install/`
2. 双击运行 `install-teambition-status.bat`
3. 脚本会将技能安装到：
   - `%USERPROFILE%\.openclaw\workspace\skills\teambition-status`

安装完成后，脚本会提示可用触发指令。

## 手动安装

### Windows

```powershell
# 1. 进入技能目录
cd $env:USERPROFILE\.openclaw\workspace\skills

# 2. 创建技能目录
mkdir teambition-status

# 3. 解压 .skill 文件（.skill 本质是 zip）
Expand-Archive -Path "C:\path\to\teambition-status.skill" -DestinationPath "$env:USERPROFILE\.openclaw\workspace\skills\teambition-status"

# 4. 验证安装成功
ls $env:USERPROFILE\.openclaw\workspace\skills\teambition-status
```

### Linux/macOS

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills

# 2. 创建技能目录
mkdir -p teambition-status

# 3. 解压 .skill 文件（.skill 本质是 zip）
unzip /path/to/teambition-status.skill -d teambition-status/

# 4. 验证安装成功
ls -la teambition-status/
```

## 安装验证与目录结构

安装完成后，目录结构应类似：

```text
teambition-status/
├── SKILL.md
├── scripts/
│   └── analyze_teambition.py
├── references/
│   └── teambition-best-practices.md
└── assets/
    └── example-config.json
```

## 使用方法

### 方法 1：自然语言触发（推荐）

直接对 OpenClaw 说出以下任意指令：

| 触发指令 | 功能说明 |
| --- | --- |
| `查看TB任务` | 查看当前项目任务状态 |
| `Teambition 状态` | 获取项目整体状态概览 |
| `看看项目进度` | 查看任务进度和完成情况 |
| `检查团队工作负载` | 分析团队成员任务分配 |
| `我的待办` | 查看个人待处理任务 |
| `今天有哪些任务截止` | 查看今日截止任务 |

### 方法 2：直接运行分析脚本（高级分析）

```bash
cd ~/.openclaw/workspace/skills/teambition-status
python scripts/analyze_teambition.py
```

## 标准使用流程

1. 在浏览器中打开 Teambition 项目页面（确保已登录）
2. 触发技能（例如：`查看TB任务`）
3. 查看输出报告（项目基本信息、任务统计、状态分布、关键时间节点、团队参与情况等）

## 注意事项

- 需要使用 OpenClaw 绑定/接管的浏览器，并确保扩展已连接当前标签页
- 只能查看当前账号有权限访问的项目
- 若数据不完整：滚动页面确保任务加载完成，等待 3–5 秒后重试，或刷新页面再分析

## 可选：自定义配置

可参考示例配置文件：

- `assets/example-config.json`

常见字段示例（仅示意，以实际实现为准）：

```json
{
  "alert_days_before": 3,
  "show_completed": false,
  "focus_status": ["待处理", "开发中"],
  "exclude_unclassified": true
}
```

## 卸载

删除安装目录即可：

- Windows：`%USERPROFILE%\.openclaw\workspace\skills\teambition-status`
- Linux/macOS：`~/.openclaw/workspace/skills/teambition-status`

## 故障排除

- **提示“浏览器未连接”**：确认 OpenClaw 正在运行，并在浏览器里点击 OpenClaw 扩展图标连接当前标签页
- **无法识别 Teambition 页面**：确认 URL 包含 `teambition.com` 且已进入具体项目页面
- **技能未触发**：确认安装目录为 `.../skills/teambition-status/` 且存在 `SKILL.md`

## 许可证

本技能仅供内部使用，请勿外传。

---

最后更新：2026-03-18

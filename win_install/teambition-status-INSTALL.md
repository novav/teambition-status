# 📊 Teambition 状态查看技能 - 安装使用指南

## 🎯 技能简介

**teambition-status** 是一个用于查看和分析 Teambition 项目状态的 OpenClaw 技能，能够自动抓取项目数据并生成结构化报告。

### 功能特性
- ✅ **项目状态概览**：快速了解项目整体状况
- ✅ **任务统计**：按分类、状态统计任务数量
- ✅ **进度跟踪**：监控任务完成情况和时间节点
- ✅ **团队分析**：分析团队成员工作负载
- ✅ **风险识别**：识别逾期任务和潜在风险

---

## 📥 安装步骤

### 前提条件
- 已安装 OpenClaw
- 已配置浏览器控制服务
- 已登录 Teambition 网页版

### 安装方法

#### Windows 用户

```powershell
# 1. 进入技能目录
cd $env:USERPROFILE\.openclaw\workspace\skills

# 2. 创建技能目录
mkdir teambition-status

# 3. 解压 .skill 文件（使用系统自带的解压）
Expand-Archive -Path "C:\path\to\teambition-status.skill" -DestinationPath "$env:USERPROFILE\.openclaw\workspace\skills\teambition-status"

# 4. 验证安装成功
ls $env:USERPROFILE\.openclaw\workspace\skills\teambition-status
```

#### Linux/macOS 用户

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

### 安装验证

安装完成后，目录结构应如下：

```
teamition-status/
├── SKILL.md                    # 技能定义文件
├── scripts/
│   └── analyze_teambition.py   # 数据分析脚本
├── references/
│   └── teambition-best-practices.md  # 最佳实践
└── assets/
    └── example-config.json     # 配置示例
```

---

## 🚀 使用方法

### 方法1：自然语言触发（推荐）

直接对 OpenClaw 说出以下任意指令：

| 触发指令 | 功能说明 |
|----------|----------|
| `查看TB任务` | 查看当前项目任务状态 |
| `Teambition 状态` | 获取项目整体状态概览 |
| `看看项目进度` | 查看任务进度和完成情况 |
| `检查团队工作负载` | 分析团队成员任务分配 |
| `我的待办` | 查看个人待处理任务 |
| `今天有哪些任务截止` | 查看今日截止任务 |

### 方法2：使用Python脚本（高级分析）

如需更详细的数据分析，可直接运行脚本：

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/teambition-status

# 运行分析脚本
python scripts/analyze_teambition.py
```

---

## 📝 使用流程

### 标准使用流程

1. **打开 Teambition**
   - 在浏览器中打开 Teambition 项目页面
   - 确保已登录并进入目标项目

2. **触发技能**
   - 对 OpenClaw 说：`"查看TB任务"`
   - 等待系统自动识别页面并分析

3. **查看报告**
   - 项目基本信息
   - 任务分类统计
   - 看板状态分布
   - 关键时间节点
   - 团队参与情况

### 支持的视图

- ✅ **看板视图**：任务按状态分组（待处理/开发中/已完成）
- ✅ **列表视图**：按分类和优先级排序
- ✅ **甘特图**：时间线任务分布

---

## ⚠️ 注意事项

### 1. 浏览器要求
- 需要使用 OpenClaw 绑定的浏览器
- 确保已点击 OpenClaw Chrome 扩展图标连接当前标签页

### 2. 权限要求
- 需要登录 Teambition 账户
- 只能查看有权限访问的项目

### 3. 数据更新
- Teambition 数据实时更新
- 快照时间会影响数据准确性
- 建议刷新页面后重新分析

### 4. 页面加载
- 确保页面完全加载后再触发技能
- 如遇数据不完整，可等待几秒后重试

---

## 🎨 自定义配置（可选）

如需个性化配置，可编辑配置文件：

```bash
# 复制配置示例到工作目录
cp ~/.openclaw/workspace/skills/teambition-status/assets/example-config.json \
   ~/.openclaw/workspace/teambition-config.json

# 编辑配置
# 修改关注的状态、截止日期提醒天数等
```

配置示例：

```json
{
  "alert_days_before": 3,        // 提前3天提醒即将截止任务
  "show_completed": false,       // 是否显示已完成任务
  "focus_status": ["待处理", "开发中"],  // 重点关注的状态
  "exclude_unclassified": true   // 是否排除未分类需求
}
```

---

## 🔧 故障排除

### 常见问题

#### Q1: 提示 "浏览器未连接"
**解决**：点击 Chrome 浏览器右上角的 OpenClaw 扩展图标，确保按钮显示为"ON"

#### Q2: 数据显示不完整
**解决**：
1. 滚动页面确保所有任务加载
2. 等待 3-5 秒后重试
3. 刷新页面后重新分析

#### Q3: 无法识别 Teambition 页面
**解决**：确保 URL 包含 `teambition.com`，且已进入具体项目页面

#### Q4: 技能未触发
**解决**：检查技能是否已正确安装到 `~/.openclaw/workspace/skills/teambition-status/`

---

## 📞 技术支持

如遇到问题，请提供以下信息：
- OpenClaw 版本
- 浏览器类型和版本
- Teambition 页面 URL
- 错误提示信息

---

## 📄 许可证

本技能仅供内部使用，请勿外传。

---

**最后更新**: 2026-03-18

**技能版本**: v1.0

**作者**: internal

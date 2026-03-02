# IPAUTO 内容工厂系统

完整的内容生产与管理系统

## 系统架构

```
ipauto_system/
├── core/                   # 核心工作流
│   ├── content_factory_workflow_v2.py    # V2.1 完整周工作流
│   └── content_factory_workflow.py       # V2.0 基础版本
├── skills/                 # 技能模块
│   └── article_breakdown.py              # 文章拆解
├── utils/                  # 工具类
│   └── feishu_perfect_writer.py          # 飞书文档写入
├── config/                 # 配置文件
│   └── system_config.py                  # 系统配置
└── docs/                   # 文档
    ├── README.md
    └── CHANGELOG.md
```

## 核心功能

### 1. 内容工厂工作流 V2.1

**工作流程：**
```
你发Hub文章 → 拆解入库 → 生成一周内容 → 自动排期
       ↓
周二-周日 9:00 每天推送当天内容
       ↓
周日 20:00 推送数据报告 → 你填数据 → 我优化
```

**功能模块：**
- 手动触发：Hub文章拆解
- 自动生成：7天短视频脚本 + 小红书图文 + 公众号图文
- 自动排期：飞书排期表
- 定时推送：每日内容推送
- 数据反馈：周末数据报告
- 智能优化：数据分析与策略调整

### 2. 文章拆解技能

自动拆解文章结构：
- 钩子（Hook）
- 信任锚点（Anchor）
- 文章结构（Structure）
- 行动号召（CTA）
- 金句库（Quotes）

### 3. 飞书文档工具

完美写入飞书文档，支持：
- 标题（多级）
- 段落
- 列表
- 表格
- 代码块
- 分割线

## 快速开始

### 环境配置

```bash
# 设置飞书API凭证
export FEISHU_APP_ID="cli_xxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxx"

# 安装依赖
pip install requests
```

### 使用示例

```python
from core.content_factory_workflow_v2 import ContentFactoryWorkflowV2

# 初始化
factory = ContentFactoryWorkflowV2()

# 处理Hub文章
result = factory.process_hub_article(
    article_title="文章标题",
    article_content="文章内容",
    article_url="文章链接"
)
```

## 定时任务

| 任务 | 时间 | 功能 |
|-----|------|------|
| 每日内容推送 | 周二-周日 9:00 | 推送当天内容 |
| 周末数据报告 | 周日 20:00 | 推送数据报告模板 |

## 系统配置

### 系统B（热点×Hub）
- Bitable: `JHVgbte16aW5dXscbAocopwlnpf`
- 热点池、Hub主题索引、爆款选题池

### 系统A（内容库）
- Bitable: `YyUfbaCTxaT6NwsGJOdcjgYFnrh`
- 视频号内容库、小红书内容库、公众号内容库、排期表

## 版本历史

- **V2.1** - 完整周工作流系统
  - 手动触发拆解
  - 自动生成一周内容
  - 每日自动推送
  - 周末数据报告
  - 数据分析优化

- **V2.0** - 系统B集成
  - 热点×Hub匹配
  - 三平台内容生成

- **V1.0** - 基础工作流
  - 5阶段内容生产

## 作者

@zhenxishuai
---
name: writer-style-guide
description: "作家文风系统总入口。自动把“用某作家文风写文章”路由到对应 style-xxx 子 skill；把“创建、优化、批量生成、迭代作家文风skill或总作家skill”路由到 style-analysis-framework 母工厂。用户直接提到作家文风、作者skill、总作家skill或文风迭代时使用。"
---

# 作家文风系统总入口

## 系统结构

```text
writer-style-guide
└── 公共入口与路由
    ├── style-analysis-framework
    │   └── 母工厂：创建、测试、优化并自我迭代
    └── style-<author>
        └── 子产品：接收主题并直接生成对应文风成稿
```

核心能力是 `style-analysis-framework` 母工厂。

`style-dazai`、`style-kafka`、`style-luxun` 等不是总方法论，而是母工厂生成和验证的子产品、范例与测试探针。

## 路由规则

### 直接写作

用户说：

- “用太宰治的文风写一段”
- “卡夫卡风格写一篇小说”
- “按鲁迅的方式写杂文”

执行：

1. 将作者名规范化为 `style-<author>`。
2. 加载对应子 skill。
3. 按子 skill 的硬输出契约直接交付成稿。
4. 不加载母工厂的研究与迭代流程，避免挤占写作上下文。

### 创建作者 Skill

用户说：

- “做一个海明威文风 skill”
- “新增某作家”
- “批量生成作者 skills”

执行：

1. 加载 `style-analysis-framework`。
2. 由母工厂完成语料、机制提取、子 skill 生成、黄金测试和盲测。
3. 新子 skill 只是产物，不把作者特有规则写回本入口。

### 优化单个子 Skill

用户说：

- “太宰治写得不像”
- “优化 style-kafka”
- “这篇像网络散文”

执行：

1. 加载 `style-analysis-framework` 与目标子 skill。
2. 将失败成稿和用户反馈作为测试证据。
3. 仅当问题属于该作者时修改子 skill。
4. 旧版、新版和无 skill 基线盲测；候选未胜出则回滚。

### 迭代总作家 Skill

用户说：

- “优化总作家 skill”
- “迭代作家 skill 生成器”
- “让以后做出来的作者 skill 都更强”

执行：

1. 加载 `style-analysis-framework`。
2. 聚合多个子 skill 的可复现失败。
3. 只把跨作者通用问题回写母工厂。
4. 至少用 3 位差异明显的作者验证母工厂候选。
5. 至少 2/3 子产品提升且无硬门槛退步，才保留母工厂修改。

## 归因规则

| 问题 | 修改位置 |
|---|---|
| 某作者独有的语气、结构或廉价模仿 | 对应 `style-<author>` |
| 同一语言多个作者共同出现的混语、翻译问题 | `style-analysis-framework` 语言协议 |
| 多作者共同出现的输出、测试、盲评或生成问题 | `style-analysis-framework` |
| 作者列表、别名和路由错误 | `writer-style-guide` |
| 单次随机失误且无法复现 | 只记日志，不改 skill |

## 作者别名路由

至少识别：

| 用户称呼 | 子 Skill |
|---|---|
| 芥川、芥川龙之介、Akutagawa | `style-akutagawa` |
| 太宰、太宰治、Dazai | `style-dazai` |
| 陀思妥耶夫斯基、陀氏、Dostoevsky | `style-dostoevsky` |
| 菲茨杰拉德、Fitzgerald | `style-fitzgerald` |
| 高尔基、Gorky | `style-gorky` |
| 卡夫卡、Kafka | `style-kafka` |
| 鲁迅、Lu Xun | `style-luxun` |
| 叔本华、Schopenhauer | `style-schopenhauer` |
| 夏目漱石、漱石、Soseki | `style-soseki` |
| 谷崎润一郎、谷崎、Tanizaki | `style-tanizaki` |
| 托尔斯泰、Tolstoy | `style-tolstoy` |

媒体和中文内容创作者同样按现有 `style-xxx` 名称路由，但不参与“作者母语原文 + 中文翻译”的默认规则。

## 未找到作者

如果用户要求的作者没有对应子 skill：

1. 不用通用模型假装已加载该作者 skill。
2. 自动加载 `style-analysis-framework`。
3. 创建新子 skill，或在用户只要一次性成稿时明确说明当前没有专用 skill。

## 禁止事项

不要：

1. 把本入口写成静态作者名单或研究报告。
2. 在本入口复制各作者的详细文风规则。
3. 把单个作者的经验直接泛化到母工厂。
4. 直接写作时同时加载所有作者 skill。
5. 把子 skill 数量当作系统质量。
6. 候选未经过真实成稿盲测就宣布优化成功。

## 最终原则

```text
本入口负责找对路
母工厂负责造好 skill
子 skill 负责写好文章
真实成稿负责证明系统是否变强
```

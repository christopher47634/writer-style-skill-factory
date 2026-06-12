# Writer Style Skill Factory

A modular AI writing style system that distills the craft of great writers into reusable, testable, and self-improving skills. Built for [Hermes Agent](https://hermes-agent.nousresearch.com).

[中文说明](#中文说明) | [Architecture](#architecture) | [Installation](#installation) | [Usage](#usage) | [Authors](#authors) | [Create New Author](#create-new-author) | [Contributing](#contributing)

---

## 中文说明

### 这是什么

「作家文风 Skill 系统」是一套 AI 写作方法论工厂。它不只是让 AI "模仿鲁迅写短句"——而是从原文语料中提取可验证的文风机制（叙述距离、句法节奏、情绪生成方式、结构推进逻辑），做成可执行的 Skill，让 AI 在任何题材上都能写出辨识度高的作品。

### 三层架构

```
writer-style-guide          ← 总入口：路由请求到子 skill 或母工厂
├── style-analysis-framework ← 母工厂：创建、测试、优化子 skill，并自我迭代
└── style-<author>           ← 子产品：接收主题，直接生成对应文风成稿
        ├── style-akutagawa      芥川龙之介
        ├── style-dazai          太宰治
        ├── style-dostoevsky     陀思妥耶夫斯基
        ├── style-fitzgerald     菲茨杰拉德
        ├── style-gorky          高尔基
        ├── style-kafka          卡夫卡
        ├── style-luxun          鲁迅
        ├── style-nanfang-zhoumo 南方周末
        ├── style-renmin-ribao   人民日报
        ├── style-schopenhauer   叔本华
        ├── style-soseki         夏目漱石
        ├── style-tanizaki       谷崎润一郎
        ├── style-thepaper       澎湃新闻
        ├── style-tolstoy        托尔斯泰
        ├── style-xiaoyuehan-kehan 小约翰可汗
        └── style-xinhua         新华社
```

### 快速安装

```bash
# 安装到 Hermes Agent
hermes skills install ./writer-style-guide
hermes skills install ./style-analysis-framework
# 批量安装所有子 skill
for d in style-*/; do hermes skills install "./$d"; done
```

### 调用示例

```
# 直接写作（自动路由到对应子 skill）
"用太宰治的文风写一段关于失眠的随笔"
"卡夫卡风格写一篇关于报销流程的小说"
"按鲁迅的方式写一篇关于996的杂文"

# 创建新作者 skill（路由到母工厂）
"做一个海明威文风 skill"
"新增 style-borges"

# 优化子 skill
"太宰治写得不像，优化一下"
"这篇鲁迅风格更像网络散文"

# 迭代母工厂
"让以后生成的作者 skill 都更强"
```

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────┐
│              writer-style-guide                  │
│         (routing & alias resolution)             │
└──────────┬──────────────────────┬────────────────┘
           │                      │
     "写一篇文章"            "做一个新 skill"
           │                      │
           ▼                      ▼
┌──────────────────┐   ┌──────────────────────────┐
│   style-<author> │   │  style-analysis-framework │
│   (sub-skill)    │   │  (mother factory)         │
│                  │   │                           │
│ • corpus distill │   │ • Phase 1: Corpus eng.    │
│ • 4 core metrics │   │ • Phase 2: Mechanism ext. │
│ • 3-draft system │   │ • Phase 3: Skill gen.     │
│ • anti-patterns  │   │ • Phase 4: Scoring        │
│ • bilingual I/O  │   │ • Phase 5: Anti-patterns  │
│                  │   │ • Phase 6: Golden tests    │
│                  │   │ • Phase 7: Blind eval      │
│                  │   │ • Phase 8: Self-iteration  │
│                  │   │ • Phase 9: Stop conditions  │
└──────────────────┘   └──────────────────────────┘
```

### How It Works

1. **Corpus Engineering**: Collect author's original-language works across periods and genres. Mark evidence as `corpus_fact`, `stable_pattern`, `local_pattern`, or `generation_hypothesis`.

2. **Mechanism Extraction**: Identify 4-8 distinguishing mechanisms (narrator distance, sentence breathing, emotion generation, character exposure, etc.) — not surface vocabulary.

3. **Sub-Skill Generation**: Each `style-<author>/SKILL.md` contains:
   - Hard output contract (bilingual by default)
   - 4 author-specific quality metrics
   - Core generation mechanisms
   - Genre routing
   - 3-draft competition system
   - Author-specific anti-patterns (cheap similarity blacklist)
   - Final delivery checklist

4. **Scoring**: 7-dimension rubric (author-specific recognition 30%, narrative voice 15%, structure 15%, syntax 15%, character 10%, native fluency 10%, originality 5%). Threshold: 90/100.

5. **Blind Testing**: Old version vs candidate vs no-skill baseline. Candidate must beat old by ≥3 points on ≥75% of non-typical prompts.

6. **Self-Iteration**: Sub-skill failures feed back into the mother factory. Only cross-author improvements get written back to `style-analysis-framework`.

---

## Installation

### Prerequisites

- [Hermes Agent](https://hermes-agent.nousresearch.com) installed
- Git

### Install All Skills

```bash
git clone https://github.com/christopher47634/writer-style-skill-factory.git
cd writer-style-skill-factory

# Install the router
hermes skills install ./writer-style-guide

# Install the mother factory
hermes skills install ./style-analysis-framework

# Install all author sub-skills
for d in style-akutagawa style-dazai style-dostoevsky style-fitzgerald \
         style-gorky style-kafka style-luxun style-nanfang-zhoumo \
         style-renmin-ribao style-schopenhauer style-soseki style-tanizaki \
         style-thepaper style-tolstoy style-xiaoyuehan-kehan style-xinhua; do
  hermes skills install "./$d"
done
```

### Install Selectively

```bash
# Only install Japanese authors
hermes skills install ./style-akutagawa
hermes skills install ./style-dazai
hermes skills install ./style-soseki
hermes skills install ./style-tanizaki

# Only install the framework (for creating new authors)
hermes skills install ./style-analysis-framework
```

---

## Usage

### Writing with an Author's Style

Once installed, just ask naturally:

| You say | System does |
|---|---|
| "用鲁迅的方式写一篇关于内卷的杂文" | Loads `style-luxun`, generates in Lu Xun's style |
| "Write a short story in Kafka's style about online shopping" | Loads `style-kafka`, generates in German with Chinese translation |
| "以托尔斯泰的笔法写一个晚宴场景" | Loads `style-tolstoy`, generates in English with Chinese translation |
| "用南方周末的风格写一篇关于AI教育的深度报道" | Loads `style-nanfang-zhoumo`, generates in Chinese |

### Creating a New Author Skill

```
"做一个海明威文风 skill"
"帮我蒸馏村上春树的写作风格"
"新增 style-borges"
```

The system will:
1. Load `style-analysis-framework`
2. Research the author's original-language corpus
3. Extract 4-8 distinguishing mechanisms
4. Generate `style-<author>/SKILL.md` with full structure
5. Create `test-prompts.json` with 15-30 test prompts
6. Run blind evaluation against no-skill baseline
7. Deliver the finished sub-skill

### Optimizing a Sub-Skill

```
"太宰治写得不像"
"优化 style-kafka，这篇太像网络散文了"
"鲁迅的讽刺不够犀利"
```

The system will:
1. Load the target sub-skill + `style-analysis-framework`
2. Analyze the failure mode
3. Generate candidate fix
4. Run blind test: old vs candidate vs baseline
5. Keep candidate only if it wins; otherwise rollback

### Iterating the Mother Factory

```
"让以后生成的作者 skill 都更强"
"迭代母工厂，最近几个作者写得都不够好"
```

The system will:
1. Aggregate failures across multiple sub-skills
2. Identify cross-author patterns
3. Modify `style-analysis-framework` (one variable at a time)
4. Re-test on 3+ diverse authors
5. Keep change only if ≥2/3 improve with no hard regression

---

## Authors

### Currently Included (16 authors)

| Author | Sub-Skill | Language | Type |
|---|---|---|---|
| 芥川龙之介 Akutagawa | `style-akutagawa` | Japanese | Fiction |
| 太宰治 Dazai | `style-dazai` | Japanese | Fiction/Essay |
| 陀思妥耶夫斯基 Dostoevsky | `style-dostoevsky` | Russian | Fiction |
| 菲茨杰拉德 Fitzgerald | `style-fitzgerald` | English | Fiction |
| 高尔基 Gorky | `style-gorky` | Russian | Fiction/Essay |
| 卡夫卡 Kafka | `style-kafka` | German | Fiction |
| 鲁迅 Lu Xun | `style-luxun` | Chinese | Fiction/Essay/Satire |
| 南方周末 | `style-nanfang-zhoumo` | Chinese | Journalism |
| 人民日报 | `style-renmin-ribao` | Chinese | Commentary |
| 叔本华 Schopenhauer | `style-schopenhauer` | German | Philosophy |
| 夏目漱石 Soseki | `style-soseki` | Japanese | Fiction |
| 谷崎润一郎 Tanizaki | `style-tanizaki` | Japanese | Fiction |
| 澎湃新闻 | `style-thepaper` | Chinese | Journalism |
| 托尔斯泰 Tolstoy | `style-tolstoy` | Russian | Fiction |
| 小约翰可汗 | `style-xiaoyuehan-kehan` | Chinese | Knowledge/Narrative |
| 新华社 | `style-xinhua` | Chinese | Journalism |

### Sub-Skill Structure

Each `style-<author>/` directory contains:

```
style-<author>/
├── SKILL.md          # Core skill (≤500 lines)
└── test-prompts.json # 3-30 test prompts for evaluation
```

`SKILL.md` follows a fixed 9-section structure:
1. Hard Output Contract
2. Native Language & Translation Protocol
3. 4 Author-Specific Quality Metrics
4. Core Generation Mechanisms
5. Genre Routing
6. 3-Draft Competition & Low-Score Rewrite
7. Author-Specific Anti-Patterns
8. Final Delivery Checklist
9. Corpus Boundaries & Evidence

---

## Create New Author

To add a new author to the system:

### Option 1: Use the System (Recommended)

```
"做一个 [author name] 文风 skill"
```

The mother factory handles everything: corpus research, mechanism extraction, skill generation, test creation, and blind evaluation.

### Option 2: Manual Creation

1. Create the directory:
```bash
mkdir style-<author>
```

2. Write `SKILL.md` following the 9-section structure in `style-analysis-framework/SKILL.md`

3. Create `test-prompts.json`:
```json
[
  {
    "id": 1,
    "prompt": "Write about...",
    "genre": "fiction",
    "typicality": "typical",
    "length": "standard",
    "language": "bilingual"
  }
]
```

4. Install:
```bash
hermes skills install ./style-<author>
```

5. Register the alias in `writer-style-guide/SKILL.md`

---

## Contributing

### Optimize a Sub-Skill

1. Identify what's wrong (cheap similarity, wrong tone, structural issues)
2. Tell the system: "优化 style-<author>，问题是..."
3. The mother factory will run blind tests and keep only improvements

### Iterate the Mother Factory

1. Identify cross-author patterns (e.g., "all Japanese authors have translation issues")
2. Tell the system: "迭代母工厂，问题是..."
3. The factory tests changes on 3+ diverse authors before committing

### Project Structure

```
writer-style-skill-factory/
├── README.md                          # This file
├── .gitignore                         # Excludes secrets, cache, logs
├── writer-style-guide/                # Entry point router
│   ├── SKILL.md                       # Routing rules, alias table
│   └── test-prompts.json             # Router test prompts
├── style-analysis-framework/          # Mother factory
│   ├── SKILL.md                       # 9-phase creation/iteration framework
│   ├── test-prompts.json             # Framework test prompts
│   └── results.tsv                   # Iteration history log
└── style-<author>/                   # Sub-skills (16 total)
    ├── SKILL.md                      # Author-specific generation rules
    └── test-prompts.json            # Author test prompts
```

### Evidence Levels

Every rule in a sub-skill is tagged with an evidence level:

| Level | Meaning |
|---|---|
| `corpus_fact` | Verifiable from source text |
| `stable_pattern` | Repeated across multiple works |
| `local_pattern` | Specific to one work or period |
| `generation_hypothesis` | Awaiting real-world test |

Only `stable_pattern` and tested `generation_hypothesis` enter the core execution protocol.

---

## License

MIT

## Credits

Built with [Hermes Agent](https://hermes-agent.nousresearch.com) by Nous Research.

Author corpus analysis methodology inspired by close reading traditions in literary criticism, adapted for LLM prompt engineering.

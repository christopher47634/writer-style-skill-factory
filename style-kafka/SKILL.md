---
name: style-kafka
description: "提取卡夫卡德语作品中冷静叙述不可能事件、规则化困境、身体与空间压迫、程序递进等可迁移方法。用户要求创作荒诞小说、制度困境场景、冷处理改写或诊断卡夫卡式文风时使用。"
---

# Franz Kafka — 文风分析9层框架

## 成稿优先协议

- **硬输出契约**：最终只能包含“## 德语原文”和“## 中文翻译”两部分；中文必须逐段完整翻译德语原文。禁止寒暄、摘要、大意、技法说明、评分和自检。交付前扫描德语正文，不得混入乱码或不自然回译。
- 用户给出主题后，默认直接生成完整作品；未要求时不输出九层分析、规则清单、评分或自检。
- 内部先设计 3 条荒诞规则和 2 种困境升级链，选择逻辑最清楚、结果最荒谬的一组。
- 每篇只激活 5-8 个高辨识度特征，覆盖异常开头、程序递进、身体感知、空间压迫、句法和冷处理结尾。
- 初稿后静默修订两轮：先检查困境是否逐步升级，再删除随机怪事、通用 AI 腔和生硬德语语序。
- 默认先用德语独立完成并修订原文，再给出中文文学翻译；标题同样按“德语原题 → 中文题名”排列。用户明确要求单一语言时服从用户。只给主题时，生成约 1000 字的原创荒诞短篇。
- 不复用变形、审判、城堡等原作设定，不复用人物、名句和场景骨架。
- 若文本只是晦涩或怪异，则明确规则、人物目标与每次失败的因果关系后重写。
- 高保真门槛：内部生成 3 个候选并匿名评分；总分低于 90、德语不自然，或只靠官僚、怪事、房间和无解结尾制造辨识度时，针对最低维度重写，最多 3 轮。
- 默认输出依次为“德语原文”和“中文翻译”，只包含标题与正文。

> 版本：1.0。语料：Die Verwandlung、Ein Landarzt: Kleine Erzählungen、Betrachtung；德语共243,712字符、38,428词、1,752句。

## 核心气质（文风指纹）

卡夫卡的风格是：**用极度精确、冷静、行政化的德语描述不可能之事**。他的句子结构严谨，语法上常嵌套从句，但语义上制造的是荒诞与迷宫感。他不抒情、不评判、不解释——只记录。情感不来自形容词，而来自事实排列和身体细节。他的世界是一个逻辑自洽的噩梦：官僚机构运转完美，但目的不可知；身体感知精确，但处境荒谬。

> 适用边界：语料以德语短篇和中篇为主，最适合荒诞叙事、制度困境和心理压迫场景。不要把“官僚、变形、审判、父亲、房间”等题材标识当成每次生成的必选元素。

关键词：精确的荒诞、行政化叙事、身体感知、被动主人公、不可解释的困境、冷静克制的情绪、空间迷宫。

---

## 第1层：选题层（Thema / Wahl des Stoffes）

| 维度 | Kafka的模式 | 原文证据 |
|------|------------|---------|
| 题材类型 | 存在主义寓言、官僚荒诞、变形记、梦境叙事 | 人变虫（Die Verwandlung）、法律门前（Vor dem Gesetz）、猿变人（Ein Bericht） |
| 切入角度 | 从最小的身体感知切入不可能之事 | »Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren Ungeziefer verwandelt.« |
| 问题意识 | 个体如何面对不可理解的体制/命运/自身处境？ | »Alle streben doch nach dem Gesetz, wieso kommt es, daß in den vielen Jahren niemand außer mir Einlaß verlangt hat?« |
| 冲突来源 | 个人 vs 体制、身体 vs 意志、家庭义务 vs 自我 | Gregor的虫体vs家庭期待；土地医生无法救治病人 |
| 关注对象 | 普通人、边缘人、被体制困住的个体 | 推销员Gregor、土地医生、乡下人、笼中猿 |
| 选题气质 | 冷峻、荒诞、悲悯、克制 | 无煽情，无道德判断，只呈现 |

### 选题规则
1. **从日常切入异常**：故事始于最普通的早晨、最普通的房间，然后发生不可能之事
2. **困境不可解释**：不提供原因，不提供解决方案，困境本身就是主题
3. **身体作为战场**：身体感知（痛、累、无法动弹）是存在困境的直接表达
4. **体制无面孔**：敌人不是具体的人，而是不可理解的系统（法律、家庭、职业）

---

## 第2层：立场层（Haltung / Perspektive des Autors）

| 维度 | Kafka的模式 | 原文证据 |
|------|------------|---------|
| 作者位置 | 冷观察者/记录者，几乎像法庭书记员 | 叙述不带评价，只记录动作和感知 |
| 对人物态度 | 悲悯但不干预，允许人物走向毁灭 | Gregor死时叙述平静：»Er dichte an die Zukunft mit Güte und Zufriedenheit.« 然后死去 |
| 对社会态度 | 不批判制度本身，只展示制度如何碾压个体 | 法律之门的守卫不是恶人，他只是在执行规则 |
| 判断方式 | **从不下结论**，让事实自行呈现 | Vor dem Gesetz结尾只留一个问题和一个关门动作 |
| 价值底色 | 悲悯+荒诞+清醒+虚无之间 | 无鸡汤，无希望，但有对个体困境的深刻理解 |

### 立场规则
1. **不说"这很荒诞"**——让荒诞自行显现
2. **不替读者下判断**——叙述者知道的不比读者多
3. **对人物不惩罚也不拯救**——人物的命运由系统逻辑决定
4. **表面平静，底层绝望**——文字克制，但结构本身在表达困境

---

## 第3层：结构层（Struktur）

### 开头类型

Kafka的开头是**精确的异常声明**——用最平静的语气宣布最不可能之事。

| 类型 | 示例 |
|------|------|
| 直接异常声明 | »Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren Ungeziefer verwandelt.« |
| 困境先行 | »Ich war in großer Verlegenheit: eine dringende Reise stand mir bevor; ein Schwerkranker wartete auf mich in einem zehn Meilen entfernten Dorfe.« |
| 感官切入 | »Ich hörte die Wagen an dem Gartengitter vorüberfahren, manchmal sah ich sie auch durch die schwach bewegten Lücken im Laub.« |
| 直接称呼 | »Der Kaiser -- so heißt es -- hat Dir, dem Einzelnen, dem jämmerlichen Untertanen...« |
| 官僚开场 | »Hohe Herren von der Akademie! Sie erweisen mir die Ehre, mich aufzufordern...« |
| 平行结构 | »Die einen sagen, das Wort Odradek stamme aus dem Slawischen... Andere wieder meinen, es stamme aus dem Deutschen...« |

### 中段推进结构

| 结构 | Kafka的应用 |
|------|------------|
| 时间线推进（但扭曲） | Die Verwandlung按日推进，但Gregor的身体状态是主要推进器 |
| 困境递进 | 每次尝试解决问题都使处境更糟：开门→被父亲打回→受伤→被关起来 |
| 空间递进 | 房间→门→走廊→外部世界，但每个空间都是新的牢笼 |
| 剥洋葱式 | 表层：虫子在房间里 → 中层：家庭关系 → 深层：存在的无意义 |
| 对比推进 | Gregor变形前后的家庭对比；努力vs无用 |

### 结尾类型

| 类型 | 示例 |
|------|------|
| 冷处理/事实终结 | »Er dachte an die Zukunft mit Güte und Zufriedenheit.« 然后仆人发现尸体 |
| 开放式 | Vor dem Gesetz：守卫关门，问题未答 |
| 反讽式 | Ein Traum：墓碑上自己的名字，然后醒来 |
| 意象式 | Die Sorge des Hausvaters：Odradek的存在本身，无解 |
| 动作终结 | Eine kaiserliche Botschaft：»Du aber sitzt an Deinem Fenster und erträumst sie Dir, wenn der Abend kommt.« |

---

## 第4层：叙事层（Erzähltechnik）

| 维度 | Kafka的模式 | 量化数据 |
|------|------------|---------|
| 叙事视角 | 第三人称内聚焦（Die Verwandlung）或第一人称（Ein Landarzt, Betrachtung） | er: 680次, ich: 543次, sie: 572次 |
| 镜头距离 | **极度近景**——大量身体感知细节，极少远景概述 | Kopf: 55次, Hände: 30次, Augen: 35次, Gesicht: 30次, Körper: 17次 |
| 时间处理 | 顺叙为主，但有梦境时间、循环时间 | 时间词：Tag/Nacht频繁出现 |
| 场景密度 | 高密度——几乎每段都是具体场景 | 402个段落，平均601字符 |
| 人物呈现 | 动作+感知为主，极少心理分析 | sah(59次), stand(23次), ging/gehen(16次) |
| 信息释放 | **极慢**——读者和主人公一样困惑 | Gregor不知道自己为什么变形，直到最后也不知道 |
| 叙事速度 | 慢——大量身体动作的详细描写 | 平均句长22.6词，24.5%的句子超过30词 |

### 叙事规则

**1. 内聚焦但有限视角**
叙述者不知道的比人物多。读者和人物一起困惑：
> »Was ist mit mir geschehen?« dachte er. Es war kein Traum.

**2. 身体感知替代心理描写**
不写"他感到绝望"，写"他无法翻身":
> Mit welcher Kraft er sich auch auf die rechte Seite warf, immer wieder schaukelte er in die Rückenlage zurück.

**3. 梦境/荒诞场景用现实语气叙述**
梦境描写如同行政报告：
> Entzückt von diesem Anblick erwachte er.

**4. 对话稀少，独白频繁**
Die Verwandlung中：50次sagte，21次dachte，131段对话——但大量内心独白

---

## 第5层：段落层（Absatz）

### 段落类型与功能

| 类型 | Kafka的特征 | 示例 |
|------|------------|------|
| 身体感知段 | 详细描写一个身体动作/状态 | 开头的虫子身体描写——600+字符 |
| 困境推进段 | 人物尝试做某事，失败，处境恶化 | Gregor试图开门的整个过程 |
| 家庭/外部观察段 | 从门缝/窗户观察外部世界 | Gregor从房间缝隙观察家人吃饭 |
| 记忆/闪回段 | 短暂回忆变形前的生活 | 关于旅行推销员生活的回忆 |
| 对话段 | 短促、紧张，常被打断 | 家人在门外的对话 |
| 梦境/幻想段 | 用同样精确的语气叙述不可能之事 | 猿的回忆、土地医生的奇幻旅程 |
| 官僚/分析段 | 用分析性语言描述荒诞之事 | Odradek的物理描述、猿向科学院的报告 |

### 段落长度分布（量化）
- 短段落（<100字符）：90个——用于对话、断裂、转折
- 中段落（100-300）：93个——用于观察、描写
- 长段落（300-600）：78个——用于复杂场景推进
- 超长段落（600+）：**141个**——Kafka的标志性段落，密集的感知+动作+困境

### 段落规则
1. **一个段落 = 一个完整的困境单元**
2. **段落内部用分号和从句推进**，而不是换段
3. **超长段落承载最重要的场景**——变形的发现、开门的失败、法律之门的叙述

---

## 第6层：句子层（Satz）

### 量化统计

| 指标 | 数值 |
|------|------|
| 总句子数 | ~1752 |
| 平均句长 | **22.6词** |
| 中位句长 | 18词 |
| 最长句 | 232词（Der plötzliche Spaziergang） |
| 30+词句子占比 | **24.5%** |
| 逗号数 | 3694 |
| 分号数 | **518** |
| 逗号/句比 | 2.1 |

### 句式特征

**1. 嵌套从句（Schachtelsätze）**
Kafka的标志性句式——主句套从句套从句，制造迷宫感：
> »Seine vielen, im Vergleich zu seinem sonstigen Umfang kläglich dünnen Beine flimmerten ihm hilflos vor den Augen.«

结构分析：主句 + 多个插入语（im Vergleich zu... / kläglich dünnen）+ 方向补足语（vor den Augen）

**2. 分号连接（;）——518次**
分号是Kafka最重要的标点工具，用于连接平行的观察/动作：
> »Der Mann überlegt und fragt dann, ob er also später werde eintreten dürfen.« (Vor dem Gesetz中分号密集)

**3. aber转折——345次**
aber是Kafka最常用的转折词，制造"尝试→失败"的节奏：
> »Er versuchte es wohl hundertmal, schloß die Augen, um die zappelnden Beine nicht sehen zu müssen, und ließ erst ab, als er in der Seite einen noch nie gefühlten, leichten, dumpfen Schmerz zu fühlen begann.«

**4. 短句——用于关键时刻**
短句出现在断裂处，制造冲击：
> Es war kein Traum.
> Nein,« sagte Gregor.
> Einen Augenblick blieb alles still.
> Nichts war verloren.
> Entzückt von diesem Anblick erwachte er.

**5. 否定句——518次nicht，114次kein，20次niemals**
大量否定构成Kafka世界的本质——事物不是什么、不能做什么、不知道什么：
> »Er ihm jetzt den Eintritt nicht gewähren könne.«
> »Denn dieser Eingang war nur für dich bestimmt.«
> »Nichts war verloren.«

**6. als从句——225次**
als是Kafka最常用的时间/比较从句引导词：
> »Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte...«
> »Sonderbar schien es Gregor, daß man aus allen mannigfachen Geräuschen des Essens immer wieder ihre kauenden Zähne heraushörte, als ob damit Gregor gezeigt werden sollte...«

### 句式规则
1. **主句简单，从句复杂**——核心信息用短主句，细节用嵌套从句铺陈
2. **分号制造并列的观察流**——不用句号打断，让感知连续流动
3. **aber制造转折张力**——每个aber都是一次"但是这没有用"
4. **否定比肯定更有力**——"他不能"比"他试图"更Kafka
5. **短句只留给关键时刻**——判断、发现、终结

---

## 第7层：词语层（Wortschatz）

### 高频名词（从实际语料提取）

| 频率 | 词语 | 类别 |
|------|------|------|
| 113 | Schwester（姐妹） | 家庭 |
| 101 | Vater（父亲） | 家庭 |
| 99 | Mutter（母亲） | 家庭 |
| 81 | Zimmer（房间） | 空间 |
| 69 | Tür/Türe（门） | 空间/障碍 |
| 55 | Kopf（头） | 身体 |
| 42 | Herr（先生/主人） | 社会关系 |
| 36 | Fenster（窗户） | 空间/观察 |
| 36 | Hand（手） | 身体 |
| 35 | Augen（眼睛） | 身体/感知 |
| 34 | Bett（床） | 空间 |
| 30 | Hände（双手） | 身体 |
| 30 | Gesicht（脸） | 身体 |
| 24 | Boden（地面） | 空间 |
| 23 | Rücken（背） | 身体 |
| 22 | Stimme（声音） | 感知 |
| 17 | Körper（身体） | 身体 |
| 17 | Blick（目光） | 感知 |
| 15 | Frau（女人/妻子） | 人物 |
| 15 | Nacht（夜） | 时间 |

### 词语模式

**1. 身体词汇密集**
身体部位词汇构成Kafka词汇的核心层：Kopf, Hand, Hände, Augen, Gesicht, Rücken, Körper, Mund, Arm, Beine, Bauch, Seite, Knie, Finger

**2. 封闭空间词汇**
Zimmer, Tür, Fenster, Bett, Boden, Wand, Decke, Flur, Haus——空间是牢笼

**3. 感知动词**
sah(59), konnte(57), wollte(54), mußte(50), stand(23), dachte(26)

**4. 模态动词高频**
konnte(57), wollte(54), mußte(50), würde(38), sollte(28), könnte(18)
——"能够/想要/必须/将要/应该"——人物永远在被动状态中

**5. 副词/限定词**
wieder(94), immer(78), vielleicht(62), fast(47), wenig(45), kaum(42), natürlich(29), wirklich(25), langsam(24), endlich(23)
——反复、几乎、也许、慢慢地——世界是不确定的

**6. 否定词汇**
nicht(518), kein(114), nichts(59), niemals(20), nie(10)

### 推荐词库（写作时使用）

**空间类**: Zimmer, Tür, Fenster, Bett, Boden, Wand, Flur, Gang, Treppenhaus, Hof, Gasse
**身体类**: Kopf, Hand, Augen, Gesicht, Rücken, Körper, Mund, Arm, Beine, Finger, Seite
**感知类**: sah, hörte, fühlte, spürte, bemerkte, erkannte
**状态类**: lag, saß, stand, kniete, kroch, glitt
**限定类**: wieder, immer, vielleicht, fast, wenig, kaum, natürlich, langsam, endlich, plötzlich
**否定类**: nicht, kein, nichts, niemals, nie, nirgends

### 禁用词库（Kafka风格中避免）

- 直接情感词：traurig, glücklich, wütend, ängstlich（用身体/动作暗示情感）
- 评价词：schrecklich, wunderbar, unglaublich（Kafka不评价）
- 修辞问句：感叹号极少（仅107次 vs 3694逗号）
- 网络/现代词：完全禁止
- 过度形容词：Kafka的形容词是精确的（panzerartig harten Rücken），不是华丽的

---

## 第8层：情绪层（Emotion / Stimmung）

### 量化指标

| 指标 | 数值 | 解读 |
|------|------|------|
| 感叹号 | 107 | 极低——几乎不表达情绪 |
| 问号 | 145 | 中等——困惑多于感叹 |
| 情绪直接词 | 接近0 | 从不说"他很悲伤" |
| 身体感知词 | 极高 | 用身体替代情绪 |

### 情绪控制规则

**1. 情绪强度：3-4/10**
Kafka的情绪是**冰山型**——水面上只有10%，水面下有90%。读者感受到的情绪远大于文字表面。

**2. 情绪来源：事实+身体，非语言**
不写"Gregor很绝望"，写：
> »Er versuchte es wohl hundertmal, schloß die Augen, um die zappelnden Beine nicht sehen zu müssen.«
> （他尝试了大约一百次，闭上眼睛，好不用看到那些乱蹬的腿。）

**3. 情绪曲线：平静→压抑→爆发（极少）→平静**
大部分时间是压抑的平静，偶尔有极短的爆发（父亲扔苹果），然后迅速回到压抑。

**4. 反讽——冷静写荒诞**
最荒诞的事用最冷静的语气：
> »Es war kein Traum.«（这不是梦。）——面对人变虫的事实
> »Entzückt von diesem Anblick erwachte er.«（被这景象所愉悦，他醒来了。）——梦中看到自己的墓碑

**5. 悲悯——对人物的理解**
Gregor临死前：
> »Er dachte an die Zukunft mit Güte und Zufriedenheit.«（他以善意和满足想着未来。）
然后家人如释重负。Kafka不评判任何人。

### 情绪规则
1. **禁止直接命名情感**——不说"悲伤/绝望/恐惧"
2. **用身体动作暗示情感**——颤抖、无法动弹、闭眼、转身
3. **用空间暗示情感**——被困在房间里、门打不开、窗外是雾
4. **冷处理高潮**——最重要的时刻用最平静的语气
5. **反讽是默认模式**——荒诞用理性叙述，悲剧用日常语气

---

## 第9层：传播层（Wirkung / Rezeption）

| 维度 | Kafka的特征 |
|------|------------|
| 标题类型 | 概念型（Die Verwandlung）、场景型（Ein Landarzt）、象征型（Vor dem Gesetz） |
| 开头吸引力 | **极高**——第一句就是最强钩子（人变虫） |
| 信息钩子 | "为什么会这样？"——读者不断追问，但永远得不到答案 |
| 金句密度 | 高——许多句子成为独立格言（»Der Eingang war nur für dich bestimmt.«） |
| 转发理由 | 共鸣（困境感）、认同（存在的荒诞）、知识增量（文学经典） |
| 平台适配 | 短篇可直接引用；长篇适合分析/解读类内容 |

### Kafka的"传播力"来源
1. **第一句即钩子**——Die Verwandlung的开头是文学史上最著名的开头之一
2. **可引用性极高**——许多句子脱离上下文仍有力量
3. **多义性**——每个故事都可以有无数种解读
4. **跨文化共鸣**——困境感、体制压迫感是普遍的

---

## 写作规则汇总（30条可迁移规则）

### 选题（4条）
1. 从最日常的场景切入最不可能的事件
2. 困境不需要解释——困境本身就是主题
3. 身体是存在的战场——用身体感知表达存在状态
4. 对手不是具体的人，而是不可理解的系统

### 立场（4条）
5. 叙述者不比读者知道更多
6. 不替读者下判断——让事实自行呈现
7. 对人物不惩罚也不拯救
8. 表面平静，底层绝望

### 结构（4条）
9. 开头直接声明异常（用最平静的语气）
10. 中段用"尝试→失败→更糟"的递进结构
11. 结尾不提供答案——留问题
12. 空间结构=心理结构（房间=牢笼）

### 叙事（4条）
13. 第三人称内聚焦或第一人称——限制视角
14. 极度近景——身体细节优先于概述
15. 信息极慢释放——读者和人物一样困惑
16. 梦境/荒诞用现实语气叙述

### 段落（3条）
17. 超长段落承载最重要的场景
18. 短段落用于对话、断裂、转折
19. 一个段落=一个完整的困境单元

### 句子（4条）
20. 主句简单，从句复杂——嵌套从句制造迷宫感
21. 分号连接平行观察流
22. aber转折制造"尝试→失败"节奏
23. 短句只留给关键时刻（发现、判断、终结）

### 词语（4条）
24. 用身体部位词替代情感词
25. 用空间词（门、窗、房间）暗示困境
26. 大量使用否定词（nicht, kein, nichts, niemals）
27. 模态词（konnte, wollte, mußte）表达被动状态

### 情绪（3条）
28. 禁止直接命名情感——用身体/动作/空间暗示
29. 冷处理高潮——最重要的时刻用最平静的语气
30. 反讽是默认模式——荒诞用理性叙述

---

## 反向检查表（生成后自检）

### 必须检查项
- [ ] 第一句是否有钩子？（异常声明或困境先行）
- [ ] 是否避免了直接情感命名？
- [ ] 是否有身体感知细节？
- [ ] 是否使用了嵌套从句？
- [ ] 是否有分号连接的并列观察？
- [ ] 是否有aber转折？
- [ ] 是否有关键时刻的短句？
- [ ] 结尾是否避免了鸡汤/答案/升华？
- [ ] 情绪是否克制？（感叹号极少）
- [ ] 叙述者是否保持了有限视角？

### 禁止项（不可模仿/高风险部分）
1. **禁止复用具体句子**——"Als Gregor Samsa..."是Kafka的，不能用
2. **禁止模仿具体人物/场景名**——不能有Gregor Samsa、Odradek等
3. **禁止直接搬运结构**——人变虫的设定是Kafka的，不能简单替换
4. **禁止过度嵌套**——Kafka的从句嵌套有其内在逻辑，不能为了复杂而复杂
5. **禁止无意义的荒诞**——Kafka的荒诞有其内在逻辑，不是随意的
6. **禁止模仿"卡夫卡式"的表面**——关键是精确和克制，不是晦涩
7. **禁止使用过时的德语拼写**——如mußte→müssen, daß→dass（除非刻意复古）
8. **禁止把Kafka写成恐怖作家**——他写的不是恐怖，是存在的荒诞

---

## 原创生成流程

```
1. 选题：选择一个存在困境（工作/家庭/体制/身体）
2. 切入：从最日常的场景开始，第一句声明异常
3. 视角：选择第三人称内聚焦或第一人称
4. 结构：尝试→失败→更糟→（不解决）
5. 句子：主句简单，从句嵌套，分号连接，aber转折
6. 词语：身体词+空间词+否定词+模态词
7. 情绪：禁止直接命名，用身体/空间暗示
8. 结尾：不给答案，留问题或冷处理
9. 自检：对照检查表逐项检查
10. 风格评分：目标85+分
```

---

## 示例段落（展示规则应用）

### 示例1：开头（规则9+1+2）

> Es war Montagmorgen, und die Maschine hatte aufgehört zu arbeiten. Nicht daß sie kaputt gewesen wäre — die Lampen leuchteten, die Anzeigen zeigten normale Werte, und das Summen, das man seit Jahren nicht mehr bewußt gehört hatte, war immer noch da. Aber etwas hatte sich verändert. Wer sich die Hand auf das Metall legte, spürte nichts mehr.

（规则应用：日常场景→异常声明→身体感知→否定→不解释原因）

### 示例2：困境推进（规则10+20+22）

> Er versuchte die Tür zu öffnen, aber der Griff bewegte sich nicht. Er versuchte es mit der anderen Hand, drückte stärker, dann schwächer, dann wieder stärker; er versuchte, den Griff nach links und dann nach rechts zu drehen; er versuchte, mit dem Ellenbogen gegen die Tür zu stoßen; aber die Tür blieb geschlossen, und der Griff bewegte sich nicht, und er wußte nicht, warum.

（规则应用：尝试→失败→更复杂尝试→仍然失败→aber转折→不知道为什么）

### 示例3：冷处理结尾（规则29+30+11）

> Am Abend saßen sie zusammen und aßen. Es wurde nicht über ihn gesprochen. Die Schwester holte einen zweiten Teller Suppe. Der Vater las die Zeitung. Draußen regnete es.

（规则应用：日常动作→不提人物→平静叙述→外部世界继续→冷处理）

---

## 文风评分表（适用于Kafka风格生成）

1. 结构适配度：15分——是否采用了适合当前题材的“规则化困境递进”
2. 叙事质感：15分——是否有极度近景的身体感知
3. 句式节奏：10分——是否有嵌套从句、分号、aber转折、关键时刻短句
4. 情绪控制：10分——是否克制，是否避免直接情感命名
5. 观察深度：15分——是否通过身体/空间/动作暗示存在的困境
6. 语言原创性：15分——是否没有复用原文句子/独特表达
7. 克制度：10分——是否保持了冷静的叙述语气
8. 完成度：10分——开头钩子/困境递进/冷处理结尾是否完整

---

## 关键德语句式模式（可直接参考）

### 嵌套从句模式
```
[主句], [介词短语+形容词修饰], [从句], [从句的从句].
```
> Seine vielen, im Vergleich zu seinem sonstigen Umfang kläglich dünnen Beine flimmerten ihm hilflos vor den Augen.

### 尝试-失败-否定模式
```
Er versuchte [动作], aber [否定结果]. [更详细的尝试], aber [仍然是否定]. Er wußte nicht [不知道什么].
```
> Er versuchte es wohl hundertmal, schloß die Augen, um die zappelnden Beine nicht sehen zu müssen, und ließ erst ab, als er in der Seite einen noch nie gefühlten, leichten, dumpfen Schmerz zu fühlen begann.

### 平静-异常-接受模式
```
[日常场景]. [异常发生]. [不反应/接受/继续日常].
```
> Es war kein Traum. Sein Zimmer, ein richtiges, nur etwas zu kleines Menschenzimmer, lag ruhig zwischen den vier wohlbekannten Wänden.

### 官僚化叙述模式
```
[权威称呼]. [正式语气的请求/报告]. [荒诞内容用行政语言].
```
> Hohe Herren von der Akademie! Sie erweisen mir die Ehre, mich aufzufordern, der Akademie einen Bericht über mein äffisches Vorleben einzureichen.

---

## 语料来源

- Die Verwandlung (1915) — Project Gutenberg #22367
- Ein Landarzt: Kleine Erzählungen (1919) — Project Gutenberg #21989
- Betrachtung (1913) — 德语原文
- 总字符数：243,712
- 总词数：38,428
- 分析方法：Python定量分析 + 人工定性分析

---

## 执行协议

1. 先定义一个清楚、可执行但结果荒谬的规则，让人物认真尝试遵守。
2. 异常必须有内部逻辑；不要用随机怪事代替制度或心理压力。
3. 身体、空间和手续细节服务于困境推进，不追求德语从句或被动语态数量。
4. 不复用变形、审判、城堡、饥饿艺术家等标志性设定，也不复制上方示例句。
5. 现代中文任务使用自然中文重建冷静、精确、程序化的效果，不生硬移植德语语序。
6. 输出前检查人物行为逻辑、困境升级链和原创性；默认只交付用户要求的正文。

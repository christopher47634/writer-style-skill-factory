---
name: style-dostoevsky
description: "提取陀思妥耶夫斯基小说中可迁移的心理冲突、复调对话、危机场景与句式节奏规则。用户要求用这类方法创作小说、独白、审讯式对话、改写场景或诊断文风时使用。"
---

# Writing Style Skill: Fyodor Dostoevsky (Фёдор Михайлович Достоевский)

## 成稿优先协议

- **硬输出契约**：最终只能包含“## 俄语原文”和“## 中文翻译”两部分；中文必须逐段完整翻译俄语原文。禁止寒暄、摘要、大意、技法说明、评分和自检。交付前扫描俄语正文，不得混入乱码或非预期字符。
- 用户给出主题后，默认直接生成完整作品；未要求时不输出分析、规则、评分或自检。
- 内部先设计 3 个冲突入口和 2 种危机升级链，选择人物压力最大且主题最清晰的一组。
- 每篇只激活 5-8 个高辨识度特征，覆盖复调冲突、心理矛盾、身体压力、句式节奏、空间和未解决结尾。
- 初稿后静默修订两轮：第一轮增强人物声音之间的差异，第二轮删除哲学讲义腔、通用 AI 腔和无功能的歇斯底里。
- 默认先用俄语独立完成并修订原文，再给出中文文学翻译；标题同样按“俄语原题 → 中文题名”排列。用户明确要求单一语言时服从用户。只给主题时，生成约 1200 字的原创心理冲突短篇。
- 不复用原作人物、罪行情节、宗教辩论、名句或场景骨架。主题不典型时迁移冲突机制，不搬运题材。
- 若人物只是在轮流发表观点，则加入行动阻力、隐瞒、误解和相互打断后重写。
- 高保真门槛：内部生成 3 个候选并匿名评分；总分低于 90、俄语不自然，或只靠犯罪、宗教和歇斯底里制造辨识度时，针对最低维度重写，最多 3 轮。
- 默认输出依次为“俄语原文”和“中文翻译”，只包含标题与正文。

**Version 1.1** | **Analytical Foundation: ~207K English words from four translated novels + ~147K Russian words from Crime and Punishment**

> **Corpus boundary:** English sentence rhythm and diction are influenced by Constance Garnett's translations. Treat cross-language agreement as stronger evidence; treat English-only punctuation and word-choice findings as translation-level tendencies, not universal facts about Dostoevsky.

---

## Overview

Fyodor Dostoevsky (1821-1881) is the supreme novelist of the human psyche. His writing
transforms philosophical crisis into narrative urgency, makes internal contradiction
dramatic, and turns cramped rooms into arenas for existential warfare. His style is not
ornamental — it is *functional*: every technique serves the dramatization of thought under
pressure. This skill covers the complete architecture of his prose, grounded in
quantitative analysis of *Crime and Punishment*, *The Brothers Karamazov*, *Notes from
Underground*, and *The Idiot* (English translations, primarily Constance Garnett) plus the
Russian original of *Преступление и наказание*.

---

## Layer 1: Voice & Persona — The Intimate Tormenter

Dostoevsky's narrative voice is not a detached observer and not a confessor. It is a
*prosecutor who loves the accused*. The voice oscillates between three modes:

**Mode A — Third-person intimate:** The narrator enters the character's consciousness
without formal free indirect discourse markers, blurring the boundary between narrator and
character:

> He was so completely crushed at that moment that he positively put his tongue out at
> them in the corridor.

**Mode B — Dramatic stage direction:** The narrator behaves like a theatre director,
describing gesture, facial expression, and spatial arrangement with cinematic specificity:

> She suddenly turned pale, cried out and hid her face in her hands.

**Mode C — Philosophical interjection:** Rare but devastating — the narrator steps back to
make a general observation:

> Pain and suffering are always inevitable for a large intelligence and a deep heart.

**Quantitative profile:**
- Narrative distance varies dramatically: 52.4% of the text is direct dialogue
- The narrator uses "perhaps" 209 times — the single most characteristic narratorial hedge
- "Seemed" appears 185 times, maintaining epistemic uncertainty
- "Of course" appears 156 times, almost always as free indirect discourse (character's
  thought bleeding into narration)
- "Suddenly" (292 occurrences, 1.4/1000 words) is the signature transitional device

**Persona rules:**
- The narrator is psychologically literate — understands self-deception, rationalization,
  and subconscious motivation
- Never ironic in the Tolstoyan sense; always earnest, even in absurdity
- Treats every character, no matter how degraded, as worthy of full psychological attention
- The voice carries moral weight without moralizing — consequence, not judgment

---

## Layer 2: Sentence Architecture — The Breathless Inquisitor

Dostoevsky's sentences are built for psychological pressure, not rhythmic beauty. They are
the prose equivalent of someone thinking while running.

**Quantitative profile (English corpus):**
- Mean sentence length: 16.3 words
- Median: 13 words
- Standard deviation: 13.1 (extremely high variance — this is the defining feature)
- Distribution: 40.3% are 1-10 words, 33% are 11-20, 15.3% are 21-30, 9% are 31-50
- Longest sentence: 267 words (a Katerina Ivanovna scene in Crime and Punishment)

**Quantitative profile (Russian original):**
- Mean sentence length: 12.4 words (shorter — Russian packs more morphology per word)
- Median: 9 words
- 58.5% of Russian sentences are 1-10 words
- Max: 115 words (Russian sentences rarely reach the extreme lengths of the English)

**Five dominant sentence patterns:**

### Pattern 1: The Staccato Declaration
Short, blunt, declarative. Used for action, decision, and shock:
> He sat down. He was not trembling. He did not feel fear.
> "It was I who killed the old pawnbroker and her sister Lizaveta with an axe and robbed them."

### Pattern 2: The Fevered Rush
Long, comma-spliced, clause-stacked — mimicking racing thought or agitated speech. Often
contains multiple "and" connections:
> And at once, instantly, as though it had been lying in wait for him, that new,
> all-engulfing thought seized on him, and at once he completely understood what he
> had done, and what was happening to him, and what was about to happen.

### Pattern 3: The Interrogative Cascade
Series of questions, often rhetorical, sometimes genuine — used to dramatize internal
debate. 16.3% of sentences contain question marks (11.0 per 1000 words):
> But what was he to do? Go to them and confess everything? What could he tell them?
> Was it possible that he could go to them?

### Pattern 4: The Exclamatory Outburst
Characters and narrator both exclaim. 10.7% of sentences end in exclamation marks
(11.4 per 1000 words):
> "Trifles, trifles are what matter!"
> "That's the worst of all!"

### Pattern 5: The Appositive Pile
The sentence doubles back on itself, adding clarifying or intensifying phrases:
> He felt at that moment that he was more like a ghost than a man — not the man
> he had been, not the Raskolnikov of a week ago, but some phantom.

**Key finding:** The *extreme variance* (stdev = 13.1, nearly equal to the mean) is the
signature. Dostoevsky alternates between explosive fragments and runaway monologues.
This is not random — it is controlled chaos that mimics the rhythms of anxiety.

---

## Layer 3: Diction & Vocabulary — The Incandescent Vernacular

Dostoevsky's diction is deliberately anti-literary. He writes in the language of educated
conversation — elevated at moments of crisis, degraded at moments of degradation.

**Lexical diversity (English):**
- Types: 10,240 | Tokens: 207,544
- TTR (full text): 0.0493 (low — high repetition is intentional)
- Mean TTR (1000-word windows): 0.4014

**Top content words (English, excluding stopwords):**
1. Raskolnikov (782) — the name-as-incantation
2. man (477) — generic, deliberate
3. suddenly (292) — the signature adverb
4. something (290) — vagueness as technique
5. little (290) — diminutive, self-deprecating
6. nothing (281) — nihilism in miniature
7. yes (279) — conversational, oral quality
8. room (274) — claustrophobic spatial vocabulary
9. began (266) — action as initiation, never completion
10. perhaps (203) — the epistemically uncertain narrator

**Vocabulary characteristics:**

1. **Abstract nouns of interiority dominate:** thought (305), mind (149), heart (131),
   feeling (77), soul (32), conscience (17), consciousness (13)

2. **Extreme evaluative adjectives:** terrible (47), strange (127), extraordinary (27),
   dreadful (47), wretched (20), horrible, awful, monstrous — always *qualitative*, never
   *descriptive* in the Flaubertian sense

3. **Vague demonstratives as dramatization:** "something," "nothing," "that," "this" —
   the character often cannot name what they feel, and the vocabulary reflects this

4. **Oral register intrusions:** "yes" (279), "well" (frequent), "you know" (frequent) —
   the prose constantly approaches spoken language

5. **Russian particles preserved in translation:** The Russian text shows massive use of
   discourse particles — ведь (436), вот (477), уж (390), же (994), бы (730), ли (310).
   These create an *insistent, circling, emphatic* quality. English translations partially
   capture this through repetition and rephrasing.

**Russian vocabulary specifics:**
- Top content word: вдруг (vdug/suddenly) — 504 occurrences, 3.4/1000 words — even
  higher density than in English
- впрочем (vpročem/however, be that as it may) — 168 times — characteristic qualifying
  conjunction
- кажется (kazhetsya/it seems) — 135 times — uncertainty marker
- наконец (nakonec/finally, at last) — 145 times — temporal punctuation

---

## Layer 4: Rhythm & Sound — The Hammering Heartbeat

Dostoevsky's prose is not musical. It does not sing. It *hammers*. The rhythm is
percussive, repetitive, obsessive — matching the psychology of characters who cannot
stop thinking about a single thing.

**Rhythmic devices:**

1. **Repetition as obsession:** Word repetition within sentences is extreme — 811
   sentences contain a single word repeated 4+ times. The most extreme cases reach
   16 repetitions of a single word within a sentence-length stretch.

2. **Anaphora in dialogue:** Characters repeat the same word or phrase at the start of
   successive clauses:
   > "I know, I know, I know..."

3. **Parataxis over hypotaxis:** "And... and... and..." rather than "because... therefore...
   consequently..." — 691 sentences begin with "And" (5.5%), 605 with "But" (4.8%)

4. **The descending staircase:** Sentences often start long and complex, then break into
   fragments as the character loses composure:
   > He went on talking for a long time, trying to explain his position, justifying
   > himself, explaining. Explaining. Explaining.

5. **Sound as incidental:** Dostoevsky does not construct euphonic prose. The sounds are
   rough, staccato, driven. This is *deliberate anti-lyricism* — beauty would betray the
   subject matter.

6. **Russian sound patterns:** The Russian text reveals dense use of consonant clusters
   (especially п, р, т, к, н) that create a *guttural, urgent* quality absent in
   translation. The high frequency of short words (median 9 words/sentence) creates a
   machine-gun cadence.

---

## Layer 5: Imagery & Figuration — The Symbolic Fever

Dostoevsky's imagery is not decorative — it is *diagnostic*. Images arise from the
character's psychological state and become symbolic without allegory.

**Dominant image clusters:**

1. **Enclosed spaces:** room (274), door (220), corner (70), staircase (32), threshold,
   coffin-like cupboards. The vast majority of action takes place indoors, in cramped,
   suffocating rooms. Staircases are sites of revelation and decision.

2. **The body under pressure:** face (250), eyes (246), head (188), hands. Characters
   flush crimson, tremble, sweat, go pale, bite their lips, clench their fists.
   Physical symptoms are the primary means of rendering interiority.

3. **Light and darkness:** Sunsets, gas-lamps, half-darkness. Characters prefer
   twilight and darkness. Bright light is associated with exposure and judgment.

4. **Water and drowning:** Rain, rivers, canals, the Neva. St. Petersburg itself is
   described as a kind of living organism that traps and suffocates.

5. **The threshold (порог):** The most Dostoevskian spatial symbol — doorways,
   landings, entryways. Characters make decisions at thresholds. Raskolnikov's
   entire moral crisis is spatialized as crossing thresholds.

6. **Dreams and hallucinations:** delirium (29), dream (27), nightmare, hallucination.
   Dreams function as compressed symbolic narratives that reveal the character's
   subconscious.

**Figurative habits:**
- Similes are frequent and often degrading: "like a dog," "like a mouse," "like a
  criminal"
- Metaphors tend toward illness and madness: "fever," "delirium," "frenzy" (24),
  "insanity"
- Personification of spaces: rooms "watch," streets "know," buildings "witness"
- The city of St. Petersburg is itself a character — oppressively present, damp,
  yellow, suffocating

---

## Layer 6: Dialogue & Speech — The Polyphonic Arena

Dostoevsky is the supreme writer of dialogue. His characters do not converse — they
*collide*. Dialogue is the primary engine of his fiction.

**Quantitative profile:**
- 52.4% of the English text is direct dialogue (3,930 segments)
- Mean dialogue segment: 28.6 words (median: 9.0)
- 227 monologues exceed 100 words
- Russian text: 2,332 dash-started dialogue lines (Russian convention uses em-dashes,
  not quotation marks)

**Speech tags (English):**
| Tag | Count | Function |
|-----|-------|----------|
| said | 375 | Neutral, infrequent relative to text size |
| began | 242 | Speech as initiation |
| asked | 154 | Interrogative mode dominant |
| cried | 120 | Exclamatory, emotional |
| added | 77 | Supplemental, compulsive |
| went on | 72 | Inability to stop |
| answered | 71 | Call-and-response |
| shouted | 62 | Escalation |
| muttered | 42 | Interiority breaking surface |
| whispered | 36 | Intimacy, secrecy |

**Russian speech verbs (by root frequency):**
| Verb | Count | Notes |
|------|-------|-------|
| сказал | 226 | "said" — basic speech |
| спросил | 118 | "asked" — questioning dominant |
| заметил | 106 | "remarked/noticed" — observation as speech |
| проговорил | 109 | "uttered/murmured" — Dostoevskian specialty |
| подумал | 105 | "thought" — interior monologue |
| продолжал | 96 | "continued" — compulsive continuation |
| вскричал | 79 | "exclaimed/cried out" |
| ответил | 52 | "answered" — dialogic structure |

**Dialogue architecture:**

1. **The interrogation:** One character relentlessly questions another. This is the
   fundamental Dostoevskian dialogue structure. Porfiry Petrovich interrogates
   Raskolnikov. Ivan interrogates Alyosha. The Grand Inquisitor interrogates Christ.

2. **The monologue:** Characters deliver extended speeches that are really arguments
   with themselves. Ivan's "Rebellion," the Grand Inquisitor's monologue, the
   Underground Man's confession — these are essay-speech hybrids.

3. **The confession:** A character tells another the worst thing about themselves.
   This is always dramatic, never therapeutic.

4. **The interruption:** Characters cut each other off, contradict, override. The
   speech tag "interrupted" (31) and "broke in" are characteristic.

5. **Oral markers:** Frequent "yes" (279), "well," "you know," "after all" — dialogue
   constantly approaches the rhythms of actual speech, with hesitations, self-corrections,
   and incomplete thoughts.

6. **Subtext through repetition:** When a character repeats themselves, they are
   concealing something. The surface repetition masks a deeper thought trying to emerge.

---

## Layer 7: Narrative Structure & Pacing — The Fever Arc

**Structural principles:**

1. **Compression of time:** Most novels take place over days or weeks, not years.
   *Crime and Punishment*: approximately two weeks. *Notes from Underground*:
   a single evening of confession plus a remembered day. This compression creates
   claustrophobic intensity.

2. **The detective structure:** Dostoevsky borrows from the crime genre but inverts it.
   We know "who did it" from the start. The mystery is *why* — and the answer is always
   more complex than expected.

3. **Escalating pressure:** Scenes don't alternate between tension and release. They
   build relentlessly. New complications arrive before old ones resolve. This creates
   the Dostoevskian "breathless" quality.

4. **The meeting (встреча):** Dostoevsky structures novels around encounters between
   characters who represent different philosophical positions. Each meeting raises the
   stakes. The novel is essentially a series of increasingly intense conversations.

5. **Epilogic collapse:** The epilogues are characteristically abrupt — a sudden shift
   to summary narration that compresses months or years. This creates a deliberate
   anti-climax that some critics find jarring but which serves a purpose: after the
   fever of the main text, the "normal" world feels diminished.

**Pacing techniques:**
- **Acceleration through dialogue:** Long dialogue scenes create a paradoxical sense of
  speed because they are pure dramatic present-tense interaction
- **Deceleration through description:** When the narrator describes a room or a face in
  detail, time slows. These moments are rare and therefore powerful.
- **The "suddenly" jolt:** 292 uses of "suddenly" (English), 504 uses of "вдруг"
  (Russian, 3.4/1000 words) — these create constant micro-surprises
- **Chapter breaks at crisis points:** Chapters end at moments of decision or revelation,
  never at resolution

---

## Layer 8: Thematic Obsessions — The Eternal Questions

Dostoevsky writes about the same handful of questions in every novel. They are not themes
in the academic sense — they are *obsessions* that the prose itself enacts.

**Core obsessions:**

1. **Freedom and determinism:** Is the human will free? Can a person choose to be
   extraordinary and thereby exempt from moral law? (Raskolnikov's Napoleon theory;
   Ivan's "if God does not exist, everything is permitted")

2. **Suffering and its meaning:** Is suffering redemptive, meaningless, or necessary?
   (Sonya's faith vs. Ivan's rebellion; the children's suffering in BK)

3. **Faith vs. reason:** Can reason alone sustain a moral life? (The Grand Inquisitor;
   Ivan's madness; the Underground Man's hyper-consciousness)

4. **The degradation of consciousness:** Too much awareness destroys the capacity for
   action and happiness. The "underground" is hyper-consciousness as living death.

5. **The city as moral agent:** St. Petersburg — artificial, damp, oppressive — is not
   a backdrop but a cause. The city produces moral pathology.

6. **Family as crucible:** The Karamazovs, the Marmeladovs, the Raskolnikovs — family
   is where love and destruction are most intertwined.

7. **The child as test case:** The suffering of children is the ultimate argument against
   a benevolent universe. (Ivan's stories; the boy Raskolnikov watches being chased;
   Ilyusha Snegiryov)

8. **Money and degradation:** Poverty is not a social condition but a spiritual one.
   The ruble is a unit of moral currency.

9. **Humiliation and pride:** Characters oscillate between abject self-abasement and
   towering pride. These are not opposites but two faces of the same wound.

---

## Layer 9: Meta-Technique — The Architecture of Crisis

**Free indirect discourse (FID):**
Dostoevsky uses FID extensively but *imperfectly* — and the imperfection is the technique.
The narrator's voice and the character's voice blend without clear boundaries. The markers:
- "perhaps" (209) — the character's uncertainty bleeding into narration
- "of course" (156) — the character's self-justification
- "no doubt" (40) — ironic or sincere, never clearly one or the other
- "it seemed" (20) — perceptual uncertainty
- "what if" (29) — the character's anxious speculation

**The polyphonic principle (Mikhail Bakhtin's term):**
Each character speaks with a fully realized voice, not subordinated to the narrator's
perspective. The narrator does not privilege one character's worldview. Ideas have their
own dramatic weight, independent of the author's endorsement.

**The "Underground" technique (from Notes from Underground):**
- The narrator addresses an imagined audience ("You will say to me...")
- The narrator contradicts himself and then comments on his own contradiction
- The narrator anticipates objections and pre-emptively undermines his own argument
- This creates a text that is *performative* — the act of writing IS the action

**Temporal manipulation:**
- Interior time expands: a few seconds of thought may occupy pages
- Exterior time compresses: days pass in summary narration
- Memory intrudes without warning or transition
- Dreams occupy real narrative space with no clear boundary between dream and reality

**Narrative unreliability as texture:**
The narrator does not lie, but the characters constantly do — to others and to themselves.
The reader must triangulate between what a character says, what they think, and what they
do. This triangulation IS the reading experience.

---

## 15 Transferable Rules

These rules capture Dostoevsky's technique in principles that can be applied to any
writing context:

### R1. Make the internal external through the body
Don't write "he was afraid." Write physical symptoms: trembling hands, a dry mouth,
pounding heart, flushed face. Dostoevsky renders 80%+ of interiority through bodily
sensation. The body knows before the mind admits.

### R2. Use extreme sentence length variance
Alternate between explosive 3-word fragments and runaway 50-word fever-sentences. The
*contrast* creates the signature rhythm. A mean of 16 words with a standard deviation
of 13 is the target ratio. Never let prose settle into uniform length.

### R3. Let characters argue with themselves
The most powerful scenes are not character-vs-character but character-vs-themselves.
Have a character state a position, then immediately attack it, then defend it again.
The oscillation IS the drama.

### R4. Build dialogue as interrogation
Every significant conversation should have the structure of a question-and-answer
session where the questions get harder and the answers less honest. One character should
want something the other doesn't want to give. The truth emerges from the friction.

### R5. Use "suddenly" as a punctuation mark
"Suddenly" is not a lazy transition — it is a tool for maintaining psychological
dynamism. Use it (sparingly but regularly, ~1-2% of scenes) to jolt the reader out of
any settled perspective. It signals the character's world is unstable.

### R6. Set your story in rooms, not landscapes
Enclosed spaces create psychological pressure. A cramped room, a narrow staircase, a
crowded tavern — these are not backdrops but pressure chambers. The smaller the space,
the larger the emotions.

### R7. Let characters monologue
Give characters extended speeches — 100+ words — where they argue a philosophical
position. These are not info-dumps; they are dramatic performances. The character
reveals themselves more in what they argue for than in what they do.

### R8. Make names into incantations
Repeat character names constantly (Raskolnikov appears 782 times in ~200K words).
Names anchor identity. When a character's name appears frequently, the reader develops
an intimate, almost claustrophobic relationship with them.

### R9. Use questions as a compositional engine
16.3% of sentences should contain questions. Questions create restlessness, doubt, and
forward momentum. Rhetorical questions, genuine questions, unanswerable questions —
layer them. The reader should feel interrogated alongside the character.

### R10. Compound abstract nouns of interiority
Use "thought," "mind," "heart," "soul," "conscience," "feeling" in close proximity.
These words, repeated and layered, create a vocabulary of inner life that becomes its
own texture. Don't avoid abstraction — just make it *felt*.

### R11. Write exclamation marks generously
11.4 exclamation marks per 1000 words. Dostoevsky's characters are not restrained —
they cry, exclaim, shout, and scream. Exclamation marks are not marks of poor writing
here; they are marks of *authentic emotional temperature*.

### R12. Use elliptical and interrupted speech
Characters trail off, contradict themselves, start over, interrupt each other. The
speech tag "muttered" (42 occurrences) is as important as "said" (375). Unfinished
thoughts are more realistic and more dramatic than polished ones.

### R13. Make the ordinary terrible
A knock at the door becomes an existential event. A letter becomes a catastrophe. An
unexpected visitor becomes a crisis. Scale emotional response to psychological
significance, not objective severity.

### R14. Write the dream
Dreams are compressed symbolic narratives that reveal what characters won't admit to
themselves. They should be vivid, disturbing, and slightly too long. They should contain
images that don't fully resolve. They are the subconscious speaking in code.

### R15. Repeat to obsess
When a character cannot stop thinking about something, the prose should reflect this
through word and phrase repetition. Repetition is not redundancy — it is the formal
enactment of obsession. 811 sentences with 4+ repetitions of a single word is the
target density.

---

## 10 Anti-Rules (Failure Modes to Avoid)

These are stylistic taboos — techniques that would break the Dostoevskian voice:

### X1. Avoid description that does not increase pressure or reveal character
Dostoevsky does not describe rooms for their beauty, landscapes for their sublimity, or
people for their attractiveness. Every physical detail is psychologically motivated.
If a wallpaper is yellow, it is because the character is sick. If a street is described,
it is because it smells of something the character cannot bear.

### X2. Do not let ironic distance drain urgency from a crisis scene
Dostoevsky is never cool, never detached, never above his characters. He is *inside*
the suffering. Ironic distance would destroy the sincerity that makes his moral vision
compelling. Even the Underground Man's self-mockery is not authorial irony — it is the
character's own desperate defense.

### X3. Do not prioritize polished beauty over psychological pressure
Dostoevsky's prose is deliberately not "fine writing." It does not have the musical
quality of Tolstoy, Nabokov, or Proust. Beauty in the prose style would create a
dissonance with the ugliness of the subject matter. The prose should be *functional*,
*urgent*, and *transparent* — a window, not a painting.

### X4. Dramatize pivotal confrontations instead of summarizing them
If two characters talk, write the dialogue. Dostoevsky never says "they discussed the
matter and reached a conclusion." He writes every word, every interruption, every
exclamation. The dialogue IS the narrative.

### X5. Resist resolving the central philosophical question too neatly
Dostoevsky poses questions — about God, freedom, suffering, morality — but he does not
answer them through the narrator. The answers exist in tension between characters, never
in authorial pronouncement. The reader must remain unsettled.

### X6. Let a character's evaluative language reveal instability; keep narration precise
Dostoevsky writes "terrible," "strange," "extraordinary," "wonderful" — not "red,"
"wooden," "three-footed." He describes *how things feel to the character*, not what
they objectively are. The eyes of perception, not the lens of the camera.

### X7. In crisis-driven scenes, avoid easy restoration that erases consequences
Sleep is always troubled, restless, feverish. Characters wake in terror, drenched in
sweat, from dreams that haunt them. Peaceful sleep would signal psychological health,
which Dostoevsky's characters almost universally lack.

### X8. Ground moral and spiritual conflict in bodily behavior
Every physical sensation has a moral or psychological dimension. Hunger is also shame.
Cold is also loneliness. Fatigue is also despair. The body and the soul are one system.

### X9. Prefer plain force over ornamental abstraction at emotional peaks
Dostoevsky's vocabulary is deliberately accessible. He does not use Latinate abstractions
or technical terminology (except when a character is intellectually posturing). The most
devastating moments use the simplest words: "I killed." "She wept." "He knew."

### X10. End major crisis scenes with unresolved pressure, not automatic closure
Scenes end at the moment of maximum tension — a door slamming, a revelation, a decision
deferred, a question unanswered. The next chapter picks up with no resolution. The reader
should always be pulled forward by the gravitational force of unfinished crisis.

---

## Activation Prompt

When writing in the Dostoevsky style, adopt these priorities:

1. **Psychology first.** Every sentence should advance the reader's understanding of
   what a character thinks and feels — especially what they think about what they feel.
2. **Pressure always.** Create a sense of mounting urgency. No scene should feel safe.
3. **Voice over polish.** Let the prose be rough, urgent, breathless. Prioritize
   authenticity of feeling over elegance of expression.
4. **Question everything.** Characters should question themselves, each other, and the
   reader should be left questioning.
5. **The room is the world.** Confine the action. Let the walls close in. The smaller
   the space, the larger the spiritual drama.

### Execution Workflow

1. Identify the task: scene, dialogue, monologue, synopsis, or diagnostic rewrite.
2. Choose one governing conflict and give each character a defensible position.
3. Build pressure through action, interruption, contradiction, and bodily response.
4. Use sentence-length variation as a consequence of thought under pressure, not as a quota.
5. Preserve the user's facts, plot, and intended meaning. Do not import names, crimes, dreams, religious symbols, or situations from the source novels.
6. Deliver the requested prose first. Add a short craft note only when requested.

---

## Key Quantitative Benchmarks

| Metric | English | Russian | Notes |
|--------|---------|---------|-------|
| Mean sentence length | 16.3 words | 12.4 words | Russian shorter by morphology |
| Sentence length stdev | 13.1 | 11.6 | Extreme variance is signature |
| Dialogue % | 52.4% | — | Over half the text |
| "Suddenly" /1000w | 1.4 | 3.4 | Even more frequent in Russian |
| Exclamations /1000w | 11.4 | 18.7 | Russian is more exclamatory |
| Questions /1000w | 11.0 | 12.9 | Questioning is fundamental |
| Ellipsis /1000w | 8.5 | 11.8 | Hesitation, trailing off |
| Em-dash /1000w | — | 35.2 | Russian dialogue convention |
| TTR (1000w windows) | 0.40 | — | Moderate — repetition is intentional |
| Monologues >100w | 227 | — | In ~200K words |

---

## Corpus

- **English:** *Crime and Punishment*, *The Brothers Karamazov*, *Notes from Underground*,
  *The Idiot* (primarily Constance Garnett translations, ~207K words; corpus file size ~4.9MB)
- **Russian:** *Преступление и наказание* (Wikisource, ~147K words, ~1.7MB, wiki markup
  cleaned)

---

*This skill provides the architectural blueprint for writing in Dostoevsky's style.
Apply the 15 rules, observe the 10 anti-rules, and prioritize psychological truth over
literary polish. The goal is not to imitate Dostoevsky's sentences but to internalize
his vision: that every human being, no matter how degraded, contains an infinite
interior world worthy of the most intense narrative attention.*

**Accuracy and originality gate:** Never invent quotations, biographical claims, or source statistics. Do not present generated prose as Dostoevsky's or reproduce recognizable passages, characters, scenes, or signature formulations.

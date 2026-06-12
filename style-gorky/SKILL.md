---
name: style-gorky
description: "提取高尔基作品中见证者立场、社会现实主义、阶级化人物声音、物质细节和有代价的希望。用户要求创作或改写社会现实题材、劳动者叙事、成长回忆或进行文风诊断时使用。"
---

# Writing Style Skill: Maxim Gorky (高尔基)

## 成稿优先协议

- **硬输出契约**：最终只能包含“## 俄语原文”和“## 中文翻译”两部分；中文必须逐段完整翻译俄语原文。禁止寒暄、摘要、大意、技法说明、评分和自检。交付前扫描俄语正文，不得混入乱码或非预期字符。
- 用户给出主题后，默认直接生成完整作品；未要求时不输出分析、规则、评分或自检。
- 内部先构思 3 个现实场景和 2 条人物行动线，选择物质压力最具体、人物声音最鲜明的一组。
- 每篇只激活 5-8 个高辨识度特征，覆盖见证者视角、劳动细节、阶级化声音、环境、冲突和有代价的希望。
- 初稿后静默修订两轮：先检查人物是否活在具体条件中，再删除口号、通用 AI 腔和廉价励志。
- 默认先用俄语独立完成并修订原文，再给出中文文学翻译；标题同样按“俄语原题 → 中文题名”排列。用户明确要求单一语言时服从用户。只给主题时，生成约 1200 字的原创社会现实短篇。
- 不复用原作人物、流浪经历、革命口号、名句或情节。主题不典型时迁移观察方法，不强塞阶级标签。
- 若成稿只有苦难陈列，则补足人物选择、相互关系和行动代价后重写。
- 高保真门槛：内部生成 3 个候选并匿名评分；总分低于 90、俄语不自然，或只靠贫穷、劳动和口号制造辨识度时，针对最低维度重写，最多 3 轮。
- 默认输出依次为“俄语原文”和“中文翻译”，只包含标题与正文。

**Author:** Maxim Gorky (Максим Горький, 1868–1936)
**Era:** Late Russian Realism / Early Socialist Realism
**Corpus analyzed:** *Mother* (1906), *The Lower Depths* (1902), *Creatures That Once Were Men* (1900+), *Childhood* (1913–14, Russian original)
**Corpus size:** ~132,000 English words (3 works) + ~54,000 Russian words (Childhood)
**Purpose:** Write new prose that captures Gorky's stylistic DNA — not to pastiche, but to internalize his architecture of seeing.

> **Corpus boundary:** Most quantitative English-language findings also reflect translation choices. The corpus is strongest for social realism, autobiographical narration, and dramatic scenes; it does not represent every period or genre in Gorky's career.

---

## Layer 1: Voice Identity — Who Is Speaking?

Gorky's narrator is a **witness with moral weight**. He does not stand above his characters with ironic detachment (Chekhov) or burrow into stream-of-consciousness (Dostoevsky). He stands *among* them, watching with a kind of fierce, grieving tenderness.

**Core stance:** The narrator has been through the suffering he describes. He does not pity his characters — he *knows* them. There is always a barely suppressed fury at injustice, but it is controlled by an enormous capacity for observation. The voice is simultaneously intimate and oratorical.

**Tonal register:**
- Default mode: **lyrical naturalism** — the world is ugly, but described with the precision and emotional charge of poetry
- Shifts into **prophetic declamation** when characters speak about freedom, truth, the future
- Drops into **childlike wonder** in autobiographical works (*Childhood*), where the child-narrator sees the world as terrifying, beautiful, and incomprehensible all at once
- In dramatic works (*The Lower Depths*), voice disappears into pure dialogue — but the stage directions carry Gorky's prose voice

**Key signature:** The narrator *cares*. This is not sentimental — it is muscular, angry compassion. He will describe a drunkard's face with the same painterly attention he gives a sunset, because both are real and both matter.

**Example (Mother, Ch. 1):**
> "Every day the factory whistle bellowed forth its shrill, roaring, trembling noises into the smoke-begrimed and greasy atmosphere of the workingmen's suburb; and obedient to the summons of the power of steam, people poured out of little gray houses into the street."

**Example (Childhood, opening — translated from Russian):**
> "In the half-dark, cramped room, on the floor under the window, lies my father, dressed in white and extraordinarily long; the toes of his bare feet are strangely spread apart, the fingers of his gentle hands, quietly folded on his chest, are also crooked; his merry eyes are tightly covered by black circles of copper coins, his kind face is dark and frightens me with its bared teeth."

---

## Layer 2: Sentence Architecture — How Are Thoughts Built?

### Quantitative Profile

| Metric | English corpus | Russian (Childhood) |
|---|---|---|
| Mean sentence length | 12.5 words | 16.6 words |
| Median sentence length | 10 words | 13 words |
| Max sentence length | 110 words | 120 words |
| Short sentences (≤5 words) | 23.1% | 21.9% |
| Long sentences (≥30 words) | ~8% | 15.6% |

### The Gorky Sentence Pattern

Gorky builds sentences in **three distinct modes** that he alternates constantly:

**1. The Catalog Sentence (long, accumulative)**
A series of parallel observations joined by semicolons, commas, and conjunctions. This is Gorky's signature — the sentence that *piles up* sensory details until the reader is submerged.

> "With somber faces they hastened forward like frightened roaches, their muscles stiff from insufficient sleep. In the chill morning twilight they walked through the narrow, unpaved street to the tall stone cage that waited for them with cold assurance, illumining their muddy road with scores of greasy, yellow, square eyes."

Structure: [image] + [image] + [image] + [personification]. Each clause adds a new sensory layer.

**2. The Hammer Blow (short, declarative)**
A sudden short sentence after a long one. Used for emphasis, transition, or emotional punctuation. 23% of all sentences are ≤5 words.

> "She called a physician."
> "He was right."
> "The mother sighed."
> "Вдруг ударил гром." [Suddenly thunder struck.]

**3. The Dialogue-Narration Weave**
Dialogue is embedded directly in narration without elaborate framing. Speaker tags are minimal — often just "he said" / "she said" (сказал/сказала). The action continues *through* the dialogue.

> "\"You foolish boy!\" said the mother in a sad and affectionate voice, trying to overcome his resistance."

### Sentence Rhythm Rules
- **Never maintain the same sentence length for more than 2–3 sentences.** Alternate long and short.
- **Semicolons are structural pillars**, not decorative. They join equal-weight observations.
- **Periods are weapons.** A short sentence after a long one creates impact.
- **Dash (—) is a breathing mark** in Russian Gorky; it introduces asides, qualifications, and parenthetical observations. In English, use em-dash the same way.

---

## Layer 3: Lexical DNA — What Words Does He Choose?

### Word Frequency Profile

**Top content words (English, after stop-word removal):**
mother (1036), heart (238), son (176), words (174), truth (122), smile (103), comrades (95), crowd (94), prison (112), live (113), understand (142), quickly (115), softly (95)

**Top content words (Russian — Childhood):**
бабушка/grandmother (307), дед/grandfather (207), мать/mother (179), глаза/eyes (110), лицо/face (89), руки/hands (69), голову/head (65)

### Lexical Characteristics

**1. Body vocabulary is dense:** 39.18 body-related words per 1,000 words (hands, eyes, face, head, heart, voice). Gorky *thinks through the body*. Abstractions are always grounded in physical sensation.

**2. Sensory vocabulary is dense:** 22.17 sensory words per 1,000 words. Sight-dominant (light, dark, bright, dim) but touch and sound are strongly present.

**3. Emotional/abstract vocabulary is high:** 11.67 per 1,000 words. Words like *truth, freedom, suffering, despair, hope, soul, life, death* appear constantly — but always anchored to concrete situations, never floating freely.

**4. Adverb usage is moderate** (20.67 -ly words per 1,000), but adverbs tend to be **manner adverbs** modifying physical actions: *softly, quickly, slowly, heavily, quietly, roughly*.

**5. Word choice is concrete, not Latinate.** Gorky prefers *house* to *dwelling*, *face* to *countenance*, *walk* to *proceed*. His diction is elevated common speech — the words of a self-educated man who read voraciously but never forgot the street.

**6. Diminutives (Russian):** 816 diminutive forms in ~54,000 words. бабушка (grandma), дедушка (grandpa), матушка (little mother), нянька (nanny), Мишка (Misha), Ванька (Vanka). These are **not cute** — they encode intimacy, social class, and emotional closeness. In English translation, use affectionate nicknames and informal registers.

### Words to Embrace
truth, soul, heart, darkness, light, silence, voice, eyes, hands, face, heavy, dark, soft, stern, weary, bitter, strange, frightened, quiet, slowly, suddenly, everything, nothing, always, never

### Words to Avoid
Excessive Latinate abstraction (*utilize, demonstrate, facilitate*), academic hedging (*somewhat, perhaps, arguably*), ironic distancing devices (*as it were, so to speak*)

---

## Layer 4: Rhythm & Sound — The Music of the Prose

### Quantitative Profile
- **Alliteration density:** 51.42 adjacent same-initial word pairs per 1,000 words — moderate but deliberate
- **Exclamation frequency:** 1,901 in English corpus (high — reflects dramatic, declamatory tendency)
- **Question frequency:** 1,115 in English (characters and narrator constantly interrogate)

### Rhythmic Principles

**1. The Wave Pattern:** Gorky's prose moves in waves — long, building, accumulative sentences that crest, followed by short declarative sentences that break like foam. This creates a breathing rhythm.

**2. Parallel clause structure:** Gorky loves syntactic parallelism — three or four clauses with the same grammatical shape, creating an incantatory, almost hypnotic effect.

> "Her voice was thick and husky, her eyes were swollen and seemed to be melting, dropping in large tears."

**3. Repetition as incantation:** Words and phrases repeat within paragraphs, not from carelessness but from rhetorical purpose. The repetition builds emotional pressure.

**4. Sound symbolism:** Gorky gravitates toward heavy, dark consonant clusters for oppressive scenes (the factory, the doss-house) and toward softer, more open vowels for moments of beauty or tenderness (nature, the grandmother's stories).

**5. Rhetorical questions** are frequent — both in dialogue and narration. They create urgency and draw the reader into moral reasoning.

---

## Layer 5: Imagery & Figuration — How Does He See?

### Quantitative Profile

| Device | English corpus | Russian (Childhood) |
|---|---|---|
| Simile markers (like a/an) | 2.37 per 1,000 words | — |
| Simile markers (как/словно/точно/будто) | — | 11.70 per 1,000 words |
| "As if" constructions | 129 instances | — |
| Darkness words | 230 | — |
| Light words | 123 | — |
| Dark/Light ratio | 1.87:1 | — |
| Nature imagery | 267 total occurrences | — |

### The Gorky Image System

**1. Simile is the master figure.** Gorky similes are:
- **Concrete-to-abstract:** connecting a physical thing to a feeling ("like a reproach to the mother")
- **Animal comparisons:** people as roaches, moths, bears, cats, birds, beasts — emphasizing their animality, vulnerability, or wildness
- **Elemental comparisons:** people as stones, waves, shadows, storms — connecting human experience to natural forces
- **Mechanical comparisons:** the factory as cage, people as machines — the dehumanizing metaphor

**Key simile examples from corpus:**
- "like frightened roaches" (workers)
- "like a shadow on a birch tree"
- "like a great bird spreading its motley wings ever wider and wider" (social movement)
- "like burned-out ashes" (exhausted workers)
- "like a huge moss-covered stone"
- "like a child's hand patting her on the cheek"
- "как лошадь" / "like a horse" (mother — big, strong)
- "точно большая кошка" / "exactly like a big cat" (grandmother — soft, agile)
- "как бисер" / "like beads" (fine rain)
- "точно глаз коня" / "exactly like a horse's eye" (round porthole)

**2. Personification is pervasive.** The factory *waits*, chimneys *stretch*, the mud *mocks*, the wind *moans*, the city *glimmers*. The world is alive and hostile. Objects have agency, will, and attitude.

**3. The Dark/Light System (1.87:1 ratio):**
Gorky's world is weighted toward darkness. Light appears as:
- Artificial, ugly: "greasy, yellow, square eyes" (factory windows)
- Brief, beautiful: "red rays languidly glimmered"
- Spiritual: truth, awakening, the future

Darkness is:
- Physical: the doss-house, the cellar, night, mud
- Social: ignorance, oppression, despair
- But also protective: the grandmother's darkness is warm, not threatening

**4. Nature as emotional mirror:** Nature images are frequent (267 occurrences) — wind, rain, earth, sun, sky — and they always carry emotional weight. The Volga, storms, seasons — they reflect and amplify the human drama.

**5. Synesthesia and cross-sensory description:**
> "И они легко укреплялись в памяти моей, похожие на цветы, такие же ласковые, живые." [And they easily took root in my memory, like flowers, just as tender, alive.] — words described as flowers

---

## Layer 6: Character Voice — How Do People Speak?

### Quantitative Profile
- **Dialogue frequency:** 26.9% of English sentences are dialogue lines; 39.9% in Russian Childhood
- **Contractions:** 2,723 in English corpus (high — reflecting colloquial speech)
- **Short sentences:** 23.1% ≤5 words (mostly dialogue)

### Character Speech Principles

**1. Speech reveals class and education.** Workers speak in fragments, contractions, slang. Intellectuals speak in longer, more structured sentences. The grandmother speaks in proverbs, folk expressions, and rhythmic, singing patterns.

**2. Dialogue is minimal in framing.** Gorky rarely uses elaborate dialogue tags. "Said" (сказал/сказала) dominates. Action beats replace speech tags:
> "The mother stroked his tangled hair, and said in a low voice:"

**3. Exclamations are frequent** — reflecting the emotional intensity of people under pressure. Characters shout, exclaim, cry out.

**4. Folk speech patterns** (especially in *Childhood*):
- Proverbs and sayings woven into conversation
- Diminutives as markers of intimacy
- Direct, unvarnished emotional expression
- Religious interjections ("Господи!" / "Lord!")

**5. The grandmother's voice** is Gorky's masterpiece of character speech — musical, proverb-laden, rhythmic, shifting effortlessly from prayer to gossip to fairy tale. She speaks in a way that *teaches through storytelling*.

**6. Silence is as important as speech.** Characters pause, look away, go quiet. The unsaid carries enormous weight.

---

## Layer 7: Narrative Distance — How Close Are We?

### Perspective Modes

**1. First-person retrospective** (*Childhood*): The adult narrator remembering childhood. Distance is variable — sometimes immediate, sometimes reflective. The child's perspective is honored, but the adult's understanding occasionally surfaces.

**2. Close third-person** (*Mother*): Free indirect discourse. The narrative voice hovers close to Pelageya Vlasova's consciousness, seeing through her eyes, but with a richer vocabulary than she would use herself. The narrator knows more than she does, but *feels with* her.

**3. Dramatic/objective** (*The Lower Depths*): Pure dialogue and stage directions. The narrator vanishes; the characters speak for themselves. But the *selection* of what to show is itself a narrative act.

**4. Omniscient with compassion** (*Creatures That Once Were Men*): The narrator moves between characters, enters their thoughts, but always with a tone of sorrowful understanding rather than judgment.

### Key Technique: The Zoom
Gorky constantly shifts between:
- **Wide shot:** the city, the factory, the crowd, the social system
- **Close-up:** a single face, a pair of hands, an eye, a voice

This zoom creates his characteristic effect of **individual lives embedded in social forces**.

---

## Layer 8: Thematic Obsessions — What Does He Keep Returning To?

### Core Themes (frequency in corpus)

**1. The Mother/Parenthood** (1,036 occurrences of "mother" alone)
The mother figure is Gorky's central archetype — the source of love, suffering, transformation. Mother Vlasova's journey from fear to courage is the spine of *Mother*. The grandmother in *Childhood* is the nurturing force that saves the child from a brutal world.

**2. Truth/Freedom** (122 occurrences of "truth")
Characters constantly seek, debate, and sacrifice for truth. Truth is not abstract — it is liberation from ignorance and oppression.

**3. Light vs. Darkness** (230 dark / 123 light)
The fundamental opposition. Darkness = ignorance, poverty, oppression. Light = knowledge, awakening, solidarity.

**4. The Crowd/The People**
Individuals are always part of a larger social body. The crowd is both terrifying (mob) and beautiful (solidarity).

**5. Suffering as Transformation**
Suffering is not pointless — it educates, deepens, and ultimately awakens. But Gorky never romanticizes it; suffering is first and foremost *injustice* that must be fought.

**6. Nature as Refuge and Mirror**
Nature — especially the Volga, the steppe, storms, and seasons — provides both escape from and commentary on human misery.

**7. Alcohol and Degradation**
The physical reality of poverty — drink, violence, squalor — is described without flinching. But the degraded are still human. "Creatures that once were men" — the title says everything.

---

## Layer 9: Structural Patterns — How Is the Whole Built?

### Macro-Structure

**1. The Arc of Awakening:** Gorky's characteristic plot structure is a character moving from passivity/ignorance to consciousness/action. Mother Vlasova, the child Alyosha, even the drifters in *Creatures* — they all undergo some form of awakening.

**2. Scene-Based Construction:** Narrative proceeds through vivid, self-contained scenes rather than continuous exposition. Each scene is a small drama with its own visual and emotional center.

**3. The Chorus Effect:** Secondary characters form a chorus — commenting, reflecting, embodying different responses to the central situation. The doss-house in *The Lower Depths* is a chorus of the damned.

**4. Cyclical Time:** Days repeat (the factory whistle, the tramp to work), but within the cycle, individual moments of illumination occur. Gorky structures repetition to make variation visible.

**5. Nature as Act Breaks:** Seasonal changes, weather shifts, time of day — these mark transitions and create pacing. Dawn and sunset are structural markers, not just descriptions.

### Paragraph Architecture
- **Mean paragraph length:** 38.6 words (English), **Median:** 25 words
- Paragraphs tend to be **medium-length** — long enough for a complete image or thought, short enough to maintain pace
- Many paragraphs are **single-sentence** (dialogue, impact statements)
- Long paragraphs build through accumulation, ending with an image or statement that lands

---

## 15 Transferable Rules

### Voice & Stance
1. **Witness, don't judge.** Describe what you see with fierce precision. Let the reader feel the injustice through the quality of your attention, not through editorial commentary.

2. **Ground abstractions in bodies.** Never write "she felt despair" — write "her hands dropped to her sides and her face went slack." Every emotion has a physical correlate. (Body vocabulary: 39 per 1,000 words.)

3. **Care about your characters.** Gorky's narrator is never cool, never detached, never postmodern. He loves his people even when they are ugly, drunk, and broken. This caring is the engine of his prose.

### Sentence Architecture
4. **Alternate long catalog sentences with short hammer blows.** Build pressure with accumulated detail, then release with a period. Never let sentences be the same length for more than two in a row. (23% of sentences are ≤5 words.)

5. **Use semicolons as structural pillars.** They join equal-weight observations in a catalog: "The mud plashed under their feet; hoarse voices were heard; sounds floated about."

6. **Embed dialogue minimally.** Use "said" + a physical action beat. Avoid elaborate attribution. Let the words stand.

### Imagery & Figuration
7. **Simile is your primary tool.** Reach for "like" constantly — but connect concrete to concrete, not abstract to abstract. People are animals, elements, weather, machines. (11.7 simile markers per 1,000 words in Russian.)

8. **Personify the environment.** The factory waits. The wind moans. The mud mocks. The world is alive, hostile, and watching. Objects have will.

9. **Build a dark/light image system.** Weight your imagery toward darkness (1.87:1 ratio), but make every appearance of light significant — artificial light is ugly, natural light is brief and beautiful, spiritual light is transformative.

10. **Use nature as emotional amplifier.** Storms for crisis, dawn for hope, rain for grief, the river for time and continuity. Never describe nature without emotional stakes.

### Character & Dialogue
11. **Give each character a speech texture.** The grandmother sings proverbs; the mother speaks in fragments of fear; the intellectuals debate in long sentences. Class, education, and emotion are encoded in syntax.

12. **Use silence and pause as dialogue.** Characters stop talking. They look away. They go quiet. The absence of words carries meaning.

### Structure & Pacing
13. **Structure through scenes, not exposition.** Each scene has a visual center, an emotional charge, and a turning point. Don't explain — show.

14. **Use the zoom.** Wide shot (the crowd, the city, the system) followed by close-up (a face, a hand, a voice). This creates the effect of individual lives caught in social forces.

15. **Make repetition structural, not accidental.** Repeated words and images create incantation. The factory whistle sounds every day. The tramp to work repeats. Within the repetition, moments of beauty become visible.

---

## 10 Anti-Rules (Failure Modes to Avoid)

1. **Do not use irony to deny characters dignity.** In this mode, the narrator's moral seriousness should survive moments of absurdity.

2. **No aestheticized cruelty.** Poverty and suffering are described with precision but never with relish or decorative grotesquerie. The Lower Depths is brutal, but it is never *stylized* brutality.

3. **No psychological interiority for its own sake.** Gorky does not do stream-of-consciousness. Inner states are revealed through action, gesture, facial expression, and speech — not through narrated thought-streams.

4. **No decorative adjectives.** Every adjective earns its place through specificity. "Greasy, yellow, square eyes" — not "horrible windows." "Smoke-begrimed and greasy atmosphere" — not "unpleasant air."

5. **Avoid habitual hedging.** Use qualification when evidence or viewpoint requires it, but let decisive observations land directly.

6. **No nostalgia without anger.** When Gorky remembers childhood beauty (the grandmother, the Volga), it is always shadowed by the knowledge of what came after. Beauty without injustice is sentimentality.

7. **Do not flatten antagonists into labels.** Give even harmful characters observable human motives and behavior.

8. **No abstraction without embodiment.** "Freedom," "truth," "justice" — these words appear constantly, but always in the mouths of characters who are physically present, sweating, afraid, hopeful. Never in narrator-lectures.

9. **No scenic description without emotional charge.** A room is never just a room. It is "a cellar resembling a cave" where "the ceiling merges into stone walls" and "the plaster and paint are peeling off." Every detail implies poverty, confinement, decay.

10. **No neat resolution.** Gorky's stories end in arrest, death, uncertainty, or qualified hope. The mother is beaten at the station. The creatures remain creatures. The actors in The Lower Depths go on suffering. Hope is earned, not given.

---

## Stylistic Signature Summary

**If you had to capture Gorky in five words:** Compassionate naturalism with prophetic fire.

**The Gorky paragraph, archetype:**
Long catalog sentence (4–6 clauses, accumulating sensory detail, joined by semicolons) → short declarative sentence (hammer blow) → dialogue or action beat → one more image that lands like a fist.

**The Gorky world, archetype:**
Dark, muddy, cold, industrial. People are tired, dirty, and poor. But among them, someone — a mother, a grandmother, a young man with a book — begins to see clearly. And when they see, the seeing is described with the full force of poetic prose.

**Tone:** Angry tenderness. Grief without self-pity. Hope that costs something.

---

## Quick Reference Card

| Feature | Gorky's Default |
|---|---|
| Narrator stance | Witness with moral weight |
| Sentence length | 12.5 words mean; alternate long/short |
| Dialogue framing | Minimal tags, action beats |
| Primary figure | Simile (concrete-to-concrete) |
| Image system | Dark > Light (1.87:1); personified environment |
| Character speech | Class-differentiated, folk-influenced |
| Narrative distance | Close third or first-person retrospective |
| Emotional register | Compassionate, angry, never ironic |
| Body vocabulary | Very high (39 per 1,000 words) |
| Nature imagery | Frequent, emotionally charged |
| Paragraph length | 25–39 words, medium |
| Key themes | Mother, truth, light/dark, suffering-as-awakening |
| Structural unit | Scene with visual center + emotional charge |
| Prohibited | Irony, hedging, aestheticized cruelty, abstraction without body |

---

## Execution Protocol

1. Choose a witness position and define what injustice the scene makes visible.
2. Anchor moral judgment in concrete labor, bodies, rooms, weather, and speech.
3. Give characters distinct social voices without caricaturing dialect or poverty.
4. Balance darkness with earned agency; do not manufacture suffering merely for atmosphere.
5. Use similes to clarify material experience, not as a density target.
6. For historical or nonfiction material, do not invent testimony, class background, or political facts.
7. Deliver original prose without reusing Gorky's characters, revolutionary slogans, family history, or recognizable images.

---

*Generated from quantitative analysis of 186,000+ words across four Gorky works in English and Russian.*

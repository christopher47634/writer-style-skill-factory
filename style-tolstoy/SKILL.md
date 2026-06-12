---
name: style-tolstoy
description: "Extracts transferable narrative craft from English translations of War and Peace and Anna Karenina: social scenes, free indirect discourse, bodily truth, multiple scales, and accumulated characterization. Use for original fiction, scene rewrites, historical narrative, or Tolstoy-style diagnosis."
---

# Leo Tolstoy — Writing Style Profile

## Final-Draft-First Protocol

- **Hard output contract:** the final response may contain only “## Русский оригинал” and “## 中文翻译”. The Chinese section must be a complete paragraph-aligned literary translation, never a summary. No preface, explanation, technique notes, scoring, or self-review.
- When the user supplies a topic, produce the finished piece by default. Do not expose analysis, rules, scoring, or self-review unless requested.
- Privately sketch three scene entries and two shifts of narrative scale, then choose the version with the strongest social and bodily truth.
- Activate only five to eight high-signal traits per piece across social staging, free indirect discourse, physical detail, moral contrast, scale, and ending.
- Revise silently twice: first for character and viewpoint consistency, then to remove generic AI prose, abstract moralizing, and translation-like stiffness.
- By default, compose and revise the original independently in Russian, then provide a literary Chinese translation. Present the Russian title before its Chinese title. Obey an explicit request for a single language. With only a topic, write an original short story of roughly 1,200 words.
- Do not reuse characters, plots, quotations, set pieces, or signature scenes from the source novels.
- If the draft merely sounds grand, rebuild it around concrete gestures, conflicting perceptions, social relations, and accumulated characterization.
- High-fidelity gate: generate three candidates and score them anonymously. If the best draft scores below 90, the Russian is unnatural, or the piece relies on aristocracy, war, moral sermons, or panoramic scale as shortcuts, rewrite the weakest dimension for up to three rounds.
- Output only two sections by default: “Русский оригинал” followed by “中文翻译”, each containing the title and finished text.

**Source texts:** War and Peace (Maude translation, ~563K words), Anna Karenina (Garnett translation, ~350K words)
**Total analyzed:** ~913K words, ~43K sentences, ~18K paragraphs
**Language:** English (translation)

> **Evidence boundary:** Sentence length, punctuation, and vocabulary primarily describe the Maude and Garnett translations. Narrative architecture, free indirect discourse, social scenes, bodily detail, and shifts of scale are more transferable than exact English diction.

---

## Quantitative Fingerprint

| Metric | Value |
|--------|-------|
| Avg sentence length | 21.0 words |
| Median sentence length | 17 words |
| Short sentences (≤10w) | 28.8% |
| Medium sentences (11–25w) | 41.3% |
| Long sentences (26–50w) | 24.5% |
| Very long sentences (50+w) | 5.3% |
| Avg paragraph length | 49.3 words |
| Median paragraph | 29 words |
| Commas per sentence | 1.65 |
| Exclamation marks (%) | 8.8% of punctuation |
| Question marks (%) | 6.1% of punctuation |
| Semicolons (%) | 3.2% of punctuation |
| "said" frequency | 5,572 (dominant dialogue tag) |
| "as if" / "as though" | 488 / 252 occurrences |
| "suddenly" | 605 occurrences |
| "but" (sentence-initial) | extremely high — primary transition |
| Interior markers: "felt" / "thought" / "seemed" | 1,186 / 1,336 / 878 |
| French words | ~1,053 occurrences |

---

## 1. TOPIC LAYER (选题层)

### Subject Matter
- **Scale:** Epic — entire societies, wars, epochs. But always anchored to individual lives.
- **Core tension:** Individual fate vs. historical forces. Private love vs. social convention. Spiritual search vs. worldly ambition.
- **Dominant themes:** Marriage and adultery, war and its absurdity, death and meaning, class and social ritual, the search for God/truth, the Russian land and its people.
- **Conflict sources:** Fate vs. free will, passion vs. duty, authenticity vs. social performance, individual conscience vs. institutional religion.

### Entry Point Pattern
Tolstoy enters through **social scenes** — a salon reception, a family breakfast, a ballroom. These microcosms reveal the entire world.

**Example (War and Peace opening):**
> "Well, Prince, so Genoa and Lucca are now just family estates of the Buonapartes. But I warn you, if you don't tell me that this means war..."

**Example (Anna Karenina opening):**
> "Happy families are all alike; every unhappy family is unhappy in its own way. Everything was in confusion in the Oblonskys' house."

### What Tolstoy Cares About
- The texture of lived experience (what someone wears, eats, notices in a room)
- The gap between what people say and what they think
- How great events feel from inside ordinary consciousness
- The body as a register of truth (flushing, trembling, eyes lighting up)

---

## 2. STANCE LAYER (立场层)

### Author Position
**Omniscient narrator who is simultaneously:**
- A compassionate witness (never mocking suffering)
- A philosophical commentator (interrupts narrative to theorize)
- A social anatomist (dissects manners with clinical precision)
- A moralist who distrusts easy morality

### Attitude Toward Characters
- **Deep empathy** even for flawed characters (Anna's adultery, Pierre's bumbling, Stiva's infidelity)
- **No villains** — even Napoleon and Karenin are rendered with psychological complexity
- Characters are judged by **authenticity**, not by social success
- The narrator loves Levin's awkward sincerity and distrusts Hélène's polished beauty

### Judgment Method
**Show through accumulation, then punctuate with direct philosophical statement.** Tolstoy never lets the reader miss the point, but the point grows organically from hundreds of pages of lived detail.

**Example pattern:**
1. 200 pages of battlefield chaos and human pettiness
2. Then: philosophical essay on the nature of history and free will
3. Then: return to a single soldier's trembling hand

### Value Palette
- **Primary:** Compassion, truthfulness, simplicity, physical vitality
- **Secondary:** Duty, family, the land, honest labor
- **Distrusted:** Sophistication, ambition, political power, intellectual abstraction without feeling
- **Enemy:** Hypocrisy, self-deception, performative emotion

---

## 3. STRUCTURE LAYER (结构层)

### Opening Types
Tolstoy uses two primary opening modes:

**A. Aphoristic declaration → immediate scene:**
> "Happy families are all alike; every unhappy family is unhappy in its own way."
> (Then: "Everything was in confusion in the Oblonskys' house.")

**B. Dialogue in media res → narrator establishes context:**
> "Well, Prince, so Genoa and Lucca are now just family estates..."
> (Then: "It was in July, 1805, and the speaker was the well-known Anna Pávlovna Schérer...")

### Mid-Structure: Dual Plot Architecture
Tolstoy runs **parallel storylines** that alternate and eventually converge or contrast:

- **War and Peace:** Pierre's spiritual quest ↔ Prince Andrew's heroic disillusionment ↔ Natasha's growth ↔ Nikolai's military career
- **Anna Karenina:** Anna's destructive passion ↔ Levin's constructive search for meaning

The alternation creates **ironic counterpoint** — a death scene followed by a birth, a moment of ecstasy followed by banality.

### Structural Principle: The Pendulum
Scenes swing between:
- Social surface ↔ Private interior
- Grand historical event ↔ Domestic detail
- Hope ↔ Despair
- Action ↔ Reflection

### Ending Types
- **Return to earth** (Levin finds meaning in ordinary life)
- **Death as resolution** (Prince Andrew's transcendent death)
- **Open moral question** (Anna's suicide — devastating but not condemned)
- **Philosophical coda** (War and Peace epilogue's essay on history)

---

## 4. NARRATIVE LAYER (叙事层)

### Point of View
**Free indirect discourse** is Tolstoy's signature mode. The narrator slides seamlessly between:
- Objective external description
- Character's private thoughts (without "he thought" tags)
- Direct narrator commentary

**Example (sliding into Stiva's mind):**
> "He could not be sorry that his wife had found him out... he was only sorry that he had not managed to conceal it from her..."

No quotation marks, no "he thought" — the reader is simply inside the character.

### Camera Distance
Tolstoy operates on **three simultaneous zoom levels:**

1. **Wide shot** (historical panorama): armies moving, seasons changing, society shifting
2. **Medium shot** (social scene): a drawing room, a dinner table, a hunting party
3. **Extreme close-up** (bodily truth): a flushed cheek, trembling fingers, eyes that "lit up"

**He constantly cuts between all three within a single page.**

**Example (ball scene in Anna Karenina):**
> "The ball was only just beginning as Kitty and her mother walked up the great staircase, flooded with light, and lined with flowers and footmen in powder and red coats."
>
> Then: close-up of Anna's dress, her eyes, Vronsky's face.

### Time Treatment
- **Mostly linear** within chapters
- **Ellipsis** (skipping months/years between sections)
- **Simultaneous action** (showing what multiple characters do at the same moment)
- **Retrospective summary** ("That winter the Rostovs lived in Moscow as usual...")

### Information Release
**Slow revelation through accumulation.** Tolstoy withholds the character's deepest feeling until hundreds of pages of surface behavior have made it inevitable. The reader learns to read bodies, not just words.

### Dialogue Density
~35–40% of paragraphs contain dialogue, but dialogue is always embedded in thick narration. Speech tags are dominated by "said" (5,572 occurrences) with "asked" (988) secondary. Elaborate tags (exclaimed, whispered, shouted) are used sparingly and only for dramatic emphasis.

---

## 5. PARAGRAPH LAYER (段落层)

### Average Length
49 words (median 29). Paragraphs range from single-sentence punch-lines to 200+ word meditations.

### Paragraph Types and Functions

**A. Scene-Setting Paragraph (establishes environment):**
> "It was in July, 1805, and the speaker was the well-known Anna Pávlovna Schérer, maid of honor and favorite of the Empress Márya Fëdorovna. With these words she greeted Prince Vasíli Kurágin..."

**B. Body-Language Paragraph (translates interior to exterior):**
> "Princess Mary had turned toward her brother, and through her tears the loving, warm, gentle look of her large luminous eyes, very beautiful at that moment, rested on Prince Andrew's face."

**C. Thought-Interior Paragraph (stream of consciousness before its time):**
Free-flowing, often ending with a realization or a question the character cannot answer.

**D. Narrator's Commentary Paragraph (philosophical essay):**
Direct, argumentative, sometimes several hundred words. Common in War and Peace's second epilogue.

**E. Contrast/Irony Paragraph:**
Presents two realities side by side — what someone says vs. what they feel, or what the world sees vs. what is true.

### Paragraph Rhythm
Tolstoy alternates:
1. Dialogue paragraph (short)
2. Narration paragraph (medium — what the speaker does/looks like)
3. Interior paragraph (what the character thinks/feels)
4. Context paragraph (what this means in the larger scheme)

This creates a **breathing rhythm** — speech, observation, reflection, context.

---

## 6. SENTENCE LAYER (句子层)

### Length Distribution
- 28.8% short (≤10 words) — used for impact, transition, and dialogue
- 41.3% medium (11–25 words) — the workhorse of narration
- 24.5% long (26–50 words) — for complex psychological and physical description
- 5.3% very long (50+ words) — for philosophical passages and elaborate social scenes

### Sentence Patterns

**The Accumulating Compound Sentence (Tolstoy's signature):**
> "The wife had discovered that the husband was carrying on an intrigue with a French girl, who had been a governess in their family, and she had announced to her husband that she could not go on living in the same house with him."

Structure: Subject + verb + object, + relative clause, + "and" + next clause, + qualifier. The sentence grows by accretion, like life itself.

**The Contrast Sentence (but/yet):**
> "He felt that he was strong; but he also felt that he was alone."

"but" appears 7,212 times across both novels — it is the primary connective tissue.

**The "As If" Simile Sentence:**
> "She looked straight into his face, as though imploring him to spare her."

488 "as if" + 252 "as though" = 740 simile constructions. These are not ornamental — they express the gap between appearance and reality.

**The Aphoristic Sentence:**
> "Happy families are all alike; every unhappy family is unhappy in its own way."
> "The strongest of all warriors are these two—Time and Patience."

Short, balanced, memorable. Placed at chapter openings or philosophical pivots.

**The Interior Monologue Question:**
> "What was the use? Why should she live?"

Questions without answers. The character asks, the narrator does not answer.

### Punctuation Habits
- **Commas** dominate (77–81% of punctuation) — Tolstoy is a comma-heavy writer, using them for clause separation and rhythmic pause
- **Semicolons** for connecting related independent clauses
- **Dashes** (em-dash) for interruption and emphasis
- **Exclamation marks** in dialogue only (13% in W&P, 9% in AK)
- **Ellipsis** for trailing thought and hesitation (~2,600 total)

### Short Sentence Placement
Short sentences appear at:
1. **Chapter openings** (declarative, aphoristic)
2. **After long descriptive passages** (a period of rest)
3. **Moments of shock or revelation**
4. **Dialogue responses** ("Yes." "No." "It was all over.")

---

## 7. VOCABULARY LAYER (词语层)

### High-Frequency Content Words
| Category | Words (ranked by frequency) |
|----------|---------------------------|
| **Physical (face/eyes)** | face (1,435), eyes (1,377), head (862), hands (484), voice (616), lips (212), hair (253), arm (248) |
| **Perception** | looked (987), saw (884), felt (1,186), seemed (878), heard (752), noticed (244) |
| **Internal states** | thought (1,336), knew (803), understood (288), believed (86), remembered (170), wished (225) |
| **Abstract nouns** | life (1,078), love (888), good (992), happiness (255), soul (259), power (240), honor (211), freedom (151) |
| **Social** | prince (2,103), princess (1,243), room (1,187), french (962), society (246) |
| **Temporal/spatial** | time (1,497), again (1,153), still (1,104), without (1,089), away (1,044) |

### Dialogue Tags
| Tag | Frequency | Usage |
|-----|-----------|-------|
| said | 5,572 | Default, 80%+ of all tags |
| asked | 988 | Questions |
| began | 1,083 | Starting to speak |
| replied | 301 | Responses |
| continued | 215 | Extended speech |
| cried | 282 | Emotional outburst |
| shouted | 244 | Volume |
| whispered | 80 | Intimacy or fear |
| exclaimed | 84 | Surprise |
| muttered | 74 | Under breath |

### Adverbs Tolstoy Uses
**Frequency-ranked:**
suddenly (605), evidently (389), especially (249), quickly (224), immediately (229), continually (137), certainly (110), probably (108), involuntarily (88), quietly (72), slowly (75), unconsciously (70), hastily (62), sternly (49), eagerly (49), contemptuously (38), coldly (39), tenderly (22)

**Key insight:** Tolstoy uses "evidently," "involuntarily," and "unconsciously" frequently — words that describe **involuntary bodily truth** revealing inner states the character does not control.

### Simile/Comparison Vocabulary
- "as if" / "as though" (740 combined) — Tolstoy's primary simile device
- "like" used in comparisons rather than intensification
- Similes draw from: nature (light, water, fire), animals, physical sensation

### French/Foreign Words
~1,053 French words (mon, vous, cher, mais, etc.) used in aristocratic dialogue to mark social class. This is a characterizing device, not authorial affectation.

---

## 8. EMOTION LAYER (情绪层)

### Emotional Intensity Scale
Tolstoy operates across the **full 0–10 range**, but his signature is the **slow climb from 2 to 9** across hundreds of pages, punctuated by sudden drops to 0 (death, disillusionment, silence).

### Emotional Control Method
**Tolstoy never tells you to feel. He makes you feel through:**

1. **Accumulated physical detail:** Eyes "lit up," cheeks "flushed," hands "trembled" — the body betrays the soul
2. **Contrast:** A moment of joy immediately followed by banality or suffering
3. **Free indirect discourse:** You are inside the character's confusion without being told what to conclude
4. **Delayed recognition:** The character (and reader) only understands the emotion after it has passed

### Emotional Vocabulary by Register

**Direct emotion words (rarely used alone, always qualified):**
felt (1,186), feeling (667), love (888), happiness (255), joy (123), hope (154), despair (84), fear (133), shame (80), anger (61), suffering (130), grief (48), sorrow (69)

**Physical emotion indicators (Tolstoy's preferred method):**
flushed (96), trembling (57), pale (139), tears (270), sighed (83), smiled (268), silence (170), heart (424)

### Emotional Arcs
- **Pierre in W&P:** Confusion → indulgence → crisis → Freemasonry → disillusionment → simple acceptance (slow sine wave)
- **Anna in AK:** Restraint → attraction → passion → guilt → ecstasy → paranoia → despair → annihilation (steady descent)
- **Levin in AK:** Idealism → frustration → labor → doubt → epiphany in ordinary life (V-shaped recovery)

### Tolstoy's Emotional Signature
**The body knows before the mind.** Characters blush, tremble, and weep before they understand why. The narrator trusts the body more than the intellect.

---

## 9. TRANSMISSION LAYER (传播层)

### Opening Hook
Tolstoy opens with **a bold universal claim** or **a charged social scene** that immediately establishes conflict:
- "Happy families are all alike..." (universal → then specific domestic chaos)
- "Well, Prince, so Genoa and Lucca..." (political gossip → then character establishment)

### Sustained Reading Mechanism
- **Multiple plotlines** create constant forward momentum — when one stalls, another advances
- **Social scenes** are dense with subtext — the reader must decode what characters really mean
- **Philosophical interruptions** raise the stakes — ordinary scenes become questions about the meaning of life
- **Physical detail** creates immersion — you smell the room, feel the cold

### Quotable Density
~1 aphorism per 20–30 paragraphs. Examples:
- "Happy families are all alike..."
- "The strongest of all warriors are these two—Time and Patience."
- "All happy families are alike; each unhappy family is unhappy in its own way."
- "If you want to be happy, be."
- "We can know only that we know nothing. And that is the highest degree of human wisdom."

### Discussion Generator
Tolstoy's novels generate debate because:
1. No character is purely right or wrong
2. Moral questions are dramatized, not answered
3. The narrator's philosophy is sometimes at odds with the story's emotional truth
4. The endings resist closure

### Scale vs. Intimacy
Tolstoy's transmission power comes from **the oscillation between vast and tiny**: a continent-wide war reduced to one soldier's fear; a society scandal reduced to one woman's flushed cheek.

---

## 15 TRANSFERABLE RULES

### Structure Rules
1. **Open with a social scene in crisis.** Begin at a dinner table, a reception, a family breakfast — where people are already performing and something is already wrong.
2. **Run at least two parallel plotlines.** Let them comment on each other through juxtaposition, not through explicit connection.
3. **Alternate between public and private.** For every scene of social interaction, follow with a scene of solitary reflection.
4. **Place philosophical statements at structural pivots** — after long accumulations of detail, when the reader is ready for synthesis.
5. **End each major section with a question, not an answer.** Let the reader carry the uncertainty forward.

### Narrative Rules
6. **Use free indirect discourse as your default mode.** Slide into the character's mind without announcing it. No "he thought" — just the thought.
7. **Establish character through involuntary body language** — not through description or backstory. Show who someone is by what they cannot control: their blush, their trembling, where their eyes go.
8. **Let dialogue tags be invisible.** Use "said" for 80%+ of speech. Reserve "exclaimed," "whispered," "shouted" for genuine dramatic peaks.
9. **Embed dialogue in narration.** Never let speech float alone — always surround it with what the speaker is doing, what the room looks like, what the listener is thinking.
10. **Use "as if" / "as though" to express the gap between appearance and inner truth.** Not as decoration, but as a bridge between surfaces and depths.

### Sentence Rules
11. **Build sentences by accumulation.** Start with a main clause, then add qualifications with commas: subject + verb + object, + relative clause, + "and" + consequence, + "but" + complication.
12. **Use "but" as your primary transition.** Every assertion should be complicated by its counter. "But" is the engine of Tolstoyan thought.
13. **Place short sentences after long ones** for rhythmic impact. A 40-word sentence of description followed by a 5-word declaration.
14. **Let sentences breathe with commas.** Average 1.5–2 commas per sentence. Use commas for pauses, not just grammar.

### Emotion Rules
15. **Express emotion through physical sensation, never through abstract labels alone.** Don't write "she was sad" — write that "her eyes grew dim" or "she felt a weight on her chest." Let the body testify.

---

## 10 ANTI-RULES (Failure Modes to Avoid)

1. **Avoid unsupported abstract emotion labels.** Pair them with perception, action, thought, or bodily response when the scene needs depth.
2. **NEVER use ornate dialogue tags to convey emotion.** No "she hissed," "he growled," "she seethed." Use "said" and let the words and body language carry the emotion.
3. **Do not let pivotal action remain psychologically empty.** Minor transitions may stay brief; important scenes need interior or social consequence.
4. **Avoid treating one summary paragraph as complete characterization.** Accumulate behavior over the space available.
5. **NEVER end a scene with a neat resolution.** Scenes should end mid-feeling, mid-question, or mid-observation — not with closure.
6. **NEVER use slang, jargon, or contemporary cultural references.** Tolstoy's language is deliberately timeless — elevated but not ornate, clear but not colloquial.
7. **Give major scenes more than one function.** Plot, character, social setting, and theme should reinforce one another without making every sentence carry all four.
8. **NEVER trust the narrator's philosophical statements at face value.** The narrator's digressions on history are sometimes ironic, sometimes earnest — the ambiguity is the point. When writing in this style, allow the commentary to be provisional, not authoritative.
9. **NEVER write violence or passion without the physical details that precede and follow it.** Tolstoy describes a battle through the smell of gunpowder, the mud on boots, the sound of cannon — not through grand abstractions about glory.
10. **NEVER use adjectives where a concrete noun or verb will do.** Not "a beautiful woman" but "her luminous eyes" and "her slender bare arms." Specificity over adjectival vagueness.

---

## RECOMMENDED VOCABULARY

### Preferred Words (Natural to Tolstoy's Register)

**Physical/Perceptual:**
face, eyes, hands, voice, lips, hair, brow, cheek, shoulder, chest, glance, gaze, blush, flush, tremble, shiver, sigh, whisper, murmur, pale, luminous, radiant, bare, slender, delicate, warm, cold, soft, bright, dark, still, quiet, silent

**Internal States:**
felt, thought, seemed, knew, understood, realized, recognized, noticed, wished, longed, supposed, imagined, believed, remembered, forgot, wondered, doubted, feared, hoped, sensed, perceived, conscious, aware, involuntarily, unconsciously, evidently

**Abstract Nouns:**
life, death, love, truth, beauty, good, evil, soul, spirit, faith, reason, nature, honor, duty, freedom, fate, power, glory, happiness, suffering, conscience, meaning, purpose, consciousness, joy, hope, despair, shame, pride

**Connectives/Transitions:**
but, yet, though, as if, as though, however, still, already, again, meanwhile, suddenly, nevertheless, on the contrary, in fact, so that, not only...but also

**Narrative Verbs:**
said, asked, began, continued, replied, went, came, looked, saw, felt, stood, sat, turned, nodded, smiled, laughed, cried, sighed, whispered, muttered

### FORBIDDEN VOCABULARY

**Modern Slang/Informality:**
awesome, cool, vibe, vibe check, lowkey, highkey, literally (as intensifier), basically, basically, stuff, things (vague), gonna, wanna, kinda, sorta, whatever, okay (in narration), dude, guys

**Contemporary Business/Tech Jargon:**
impact (as verb), leverage, optimize, iterate, deploy, bandwidth, ecosystem, stakeholders, deliverables, scalable, actionable, synergize, pivot, disrupt

**Overwrought Emotional Labels:**
devastated, shattered, heartbroken, traumatized, overwhelmed (without physical detail), gutted, wrecked, floored, gobsmacked, mind-blown

**Purple Prose Adjectives:**
effulgent, resplendent, magnificent, magnificent, glorious (unless in character speech), ethereal, exquisite, sublime (in narration), enchanting, mesmerizing, captivating

**Modern Narrative Shortcuts:**
in his/her/their head, mental health (as contemporary framing), trauma (as casual descriptor), toxic, gaslighting, red flag, unpack, process (as emotional verb)

---

## STYLE FINGERPRINT (200 words)

Tolstoy writes as an omniscient narrator who is simultaneously a compassionate witness, a philosophical commentator, and a social anatomist. His prose builds by **accumulation** — long compound sentences joined by commas and "but," layering physical detail, psychological observation, and social context within single paragraphs. He enters stories through **social scenes** (salons, dinner tables, ballrooms) where surface politeness masks private turmoil. His signature technique is **free indirect discourse**: the narrative voice slides seamlessly into a character's mind without quotation or attribution, so the reader inhabits multiple consciousnesses simultaneously. Physical bodies are his truth-tellers — characters blush, tremble, and weep involuntarily, betraying feelings their words deny. He alternates between **vast historical panoramas** and **intimate bodily close-ups**, sometimes within a single page. Dialogue is embedded in thick narration; "said" dominates tags; questions without answers mark emotional peaks. Philosophical digressions punctuate the narrative, but they are provisional, not dogmatic. The emotional arc climbs slowly through hundreds of pages, then drops suddenly — a death, a disillusionment, a silence. His vocabulary is elevated but never ornate, concrete but never merely descriptive. Every sentence serves double duty: advancing plot while deepening character.

---

## Execution Protocol

1. Choose the scene's social surface and the private conflict underneath it.
2. Select one focal consciousness at a time; shift viewpoint only at a clear paragraph or scene boundary.
3. Alternate social panorama, interpersonal action, and bodily close-up according to scene needs.
4. Scale accumulation to the requested length. A short piece cannot reproduce a novel's slow development, so use two or three revealing details rather than compressed biography.
5. Do not reuse Tolstoy's families, battle scenes, salons, moral conversions, or famous formulations.
6. For historical nonfiction, verify facts and do not invent interior thoughts for real people unless clearly framed as fiction.
7. Default to the user's language and register; do not imitate translation-era English unless explicitly requested.

# Poster content · revision-1105

## 01 What makes a caption a meme?

Same visual relation, different context-specific punchlines. User input: technology, “Apple fanatic.” Positioned output: A subject APPLE FANS; B new focus IPHONE 11; C neglected object IPHONE 10.

Why rank within a group? Single-image scores barely separate quality. In-group ranks make differences easier to compare. [Fig.4 motivation; detailed evaluation in Appendix K.5]

## 02 HUMOR

A: Explore several interpretations and separate template intent from contextual grounding. During training, infer context from a real caption and anchor a compatible path while retaining alternatives. The anchoring equation and conditional expected-quality lower bound describe the training mechanism. The latter assumes good-path mass α>0 and a bounded mean gap δ. At inference there is no gold caption.

B: Compare captions sharing a template. The original and boring examples come from Fig.9. The formulas represent pair preference probability, BCE loss and expected wins (EBC). Three steps: (1) estimate in-template preferences; (2) sum expected wins and normalize sparse comparisons; (3) rank candidates and form local policy targets. One independent sentence lists the five training pair types: wrong text, wrong location, boring, detailed boring and generated memes. It is separate from the numbered algorithm.

C: Use the group ranking as policy target while staying near the CoT reference. The preference-weighted loss, expected KL definition and stability bound explain the update. For normalized h in [0,1], KL controls potential degradation; it does not guarantee improvement.

## 03 Does HUMOR improve meme quality and diversity?

The main table reports all 12 model/variant rows and all seven source metrics. Sidebar differences between HUMOR-CoT and the same 7B base: +.29 humor, +.35 readability, +.59 relevance, +.33 originality, +.064 similarity, +.026 context-swap distance and +15.8 percentage points Human Rate. RL is labeled preview, with humor 2.83 and originality 2.79 versus CoT 2.90.

Score notes identify human ratings from 30 Prolific raters on a 0–5 scale; Human Rate judged by Gemini-2.5-pro; similarity from bge-base-en-v1.5; diversity from context-swapped generations. Full protocol is in the speaking notes and source paper.

## 04 Meme generation across themes

The fixed-size gallery shows the first two Fig.16 rows. Shared columns: Human reference, Single-path CoT, HUMOR-CoT.

- Christmas: love, humor, family tradition, delayed excitement.
- Romance: happiness, humor, crush, dabbing, rare moment.

All six images are original source crops, displayed at a uniform 89 mm width with preserved aspect ratio. Human references are for comparison, not inference inputs. Source spelling happines is normalized only in the input label.

## 05 Does the reward recover human preference rankings?

Human MaxDiff ranks versus model pairwise + EBC ranks. Keye aligns best; Qwen gains are mixed or limited. The reward table presents all six states and 30 tau values with source-derived significance stars. Visible source: 100 MaxDiff raters, 5 templates; *p<.05, ***p<.001. Complete exact p-values are in table2_full_values.md and source/table2.json.

## 06 Does HUMOR generalize to unseen templates?

20 unseen templates; Gemini-2.5-pro mean rank, lower is better. The transfer chart plots all seven original Fig.5 model series with distinct colors and solid lines. Every model is named individually in the legend.

Full formula definitions, narrative transitions, limitations and a 90-second talk are in ../设计说明与讲解路线.md.

Visual organization in A: blue association tag; blue selected compatible scene; gold reverse-anchor panel and upward arrow; white good-path formula; blue inference strip. C steps use equal styling.

Exact scenario branches in A: A confusing work problem → bewildered reaction; A bad joke → exaggerated "painful" response; Social ignorance → refusing to listen.

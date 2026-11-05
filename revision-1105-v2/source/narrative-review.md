# Narrative review for HUMOR poster revision

Read: revision-1105/source/layout_v6.pyfrag; original section/3.Formulation.tex, 4.Method.tex and Appendix.tex. This is a content recommendation, not an edit of poster source.

## 01 → 02: fix the transition

The current bottom of 01 introduces group comparison, which belongs to B, while the immediately following panel A addresses reasoning construction. Replace it with a two-question bridge, or put only the exploration question in 01 and move local comparison entirely into B.

Preferred compact 01 ending:
**One template, many possible jokes.**
**How do we explore different ideas—and learn which ones work?**

Alternative with explicit two questions:
**Two challenges**
1. Explore plausible interpretations without seeing the answer.
2. Learn which caption works better in the same context.

Chinese oral hand-off: 同一张模板可以承载很多情境。我们面临两个问题：怎么让模型真的展开联想，而不是看到答案后编理由；以及这些联想生成配文之后，怎么判断哪一个更好。A回答第一个问题，B和C回答第二个。

## 02A: answer-hidden exploration → answer-grounded reverse anchoring

Header: **Explore first, anchor second**
Subtitle: **Constructing CoT supervision without revealing the answer too early.**

Stage 1 label: **1  EXPLORE — REFERENCE HIDDEN**
Text: **Given only the template, propose several plausible meanings and scenarios.**
Keep Mr. Bean three branches. Do not describe these as alternative model architectures or 'model ideas'; they are semantic interpretations / associative scenarios.

Stage 2 label: **2  REVERSE-ANCHOR — REFERENCE REVEALED**
Text: **Only after exploration, reveal the real caption. Infer its intended context and trace back to a compatible path.**
Bottom explanatory strip: **The answer guides grounding, not the initial search.**
Tiny separate deployment note if room: **At generation time, use the template and user intent; no reference caption is provided.**

Chinese interpretation: 用户对两阶段的纠正符合原文。图是构造训练推理链的数据流，不应以一个INFERENCE条替代对其设计动机的解释。可以说减少答案先验对探索的影响；不能说严格消除了答案泄漏，第二阶段本来就接触答案。‘为什么这条思路最合理’应改为‘为什么这条思路与这个实际情境和配文相容’，避免把真实meme当唯一最优。

## 02B: subjective scale → local comparison → data → aggregate scores

Header: **Learn humor through local comparisons**
Opening: **Humor has no universal scale. Comparing two captions for the same template and intent gives a more focused preference signal.**
Illustration label: **Same template + same intended context: which caption works better?**
Training-data lead: **Where do the comparisons come from?**
Five compact labels and explanations:
- **Wrong text** — break semantic fit.
- **Wrong location** — break role binding.
- **Boring** — keep meaning, flatten the joke.
- **Detailed boring** — weaken the joke with small edits.
- **Generated** — compare plausible model outputs.

Use 'five difficulty tiers' or 'five types, from obvious errors to subtle humor differences'. Do not imply a verified total difficulty order: source has wrong-location and boring both two stars, generated variable one-to-three stars. Do not claim all pairs are manually labeled or all preferences objectively correct.

Next subhead: **From pairwise preferences to a usable score**
Formula: p_ij = P(m_i preferred to m_j); EBC(i) = sum_(j != i) p_ij.
One sentence: **EBC counts expected wins against the other candidates, then converts these local scores into a soft group-level training target.**
Visual flow: **Pairs → preference probabilities → expected wins → local targets**
If incomplete comparisons are shown: normalize by the number of available opponents, as appendix specifies for evaluation.

Important: EBC aggregates pairwise probabilities into scores and a ranking. It is not literally converting a pre-existing rank into calibrated scores. Scores remain group-local.

### DPO

No DPO experiment, quantitative comparison, or demonstrated DPO failure found in the supplied manuscript. Do not add 'DPO performs poorly on memes' or 'DPO is unsuitable because humor is ambiguous'. DPO itself learns relative preferences; ambiguity also affects this reward model. DPO is a policy-training objective; EBC is aggregation, so they are not mutually exclusive alternatives.

Primary reference checked: https://papers.neurips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html
The paper formulates direct policy optimization on preference pairs through an implicit reward parameterization. It does not require universally correct binary good/bad categories.

If asked why this design, say: **We need an explicit score over the whole candidate group for selection and policy reweighting. EBC aggregates many local comparisons into that target.** This justifies the actual choice without unsupported criticism of DPO.

## 02C: a connected diversity–quality story, with conditional bounds

Header: **Explore broadly, control the humor gap**
Three-step conceptual strip:
**A  Expand the candidate space** → **B  Identify stronger candidates locally** → **C  Shift probability with bounded drift**.
Opening: **Exploration adds plausible ideas, including weaker jokes. Preference learning helps favor the stronger ones, while KL control limits drift from the CoT model.**
This says 'may introduce weaker jokes', not 'CoT lowers humor'. In the actual main table, CoT raises humor from 2.39 to 2.68, and context-swap distance from .564 to .590.

First displayed bound (rearranged directly from manuscript):
**1 − E[h̃_G] ≤ (1 − α)δ**
Caption: **α: mass on best paths. δ: mean gap of the remaining paths.**
Use the manuscript's assumptions explicitly: best-path humor normalized to 1 and specified alpha/delta conditions. 'Promising paths' not literally optimal would not suffice for this exact bound without extra assumptions; keep 'best paths' or 'under the paper’s star-path assumptions'.

Second displayed bound:
**H(CoT) − H(updated) ≤ sqrt(Δ_KL / 2)**
Caption: **For normalized humor, bounded policy drift limits the possible quality drop.**

Closing: **Broader exploration, preference-guided selection, controlled updates.**
Do NOT write 'guaranteed diversity improvement with no humor loss': neither theorem proves diversity gains, shrinking delta, zero degradation, or monotonic RL improvement. Rank consistency under assumptions supports correct ordering, not quantified reduction of the true humor gap after finite training. The existing KL bound follows boundedness and KL proximity; it is not specific proof that EBC fixes the gap.

For oral explanation: CoT先扩大可探索的空间，但其中会有弱笑话。第一个式子把潜在的质量缺口写成优质路径的概率质量和其余路径的平均差距。B提供组内偏好，用来找到更好的候选；C据此更新，并通过KL限制相对CoT模型可能发生的质量下降。它是有条件的质量控制，不是每次更新必然提升。

If parent wants an intuitive combined graphic, display these two bounds sequentially, do not silently sum them into a new theorem: the first operates over reasoning paths, the second over generated captions, and composing them requires aligning the definitions and averaging assumptions.

## Useful empirical evidence for this story

A small Humor vs. Context-swap Distance scatter plot can replace much of the oversized table and directly explain 'variety alone is not enough':
- Qwen 7B: (.564, 2.39)
- Single Path: (.570, 1.87)
- Self Improve: (.578, 2.38)
- Subquestion: (.597, 1.85)
- HUMOR-CoT: (.590, 2.68)
- HUMOR-RL preview: (.588, 2.83)

X label must be 'Context-swap distance ↑', not generic 'Diversity' alone; this is an adaptation proxy under changed context, not measured entropy or unconditional sample diversity. The final CoT→RL arrow slightly decreases this distance, so do not imply strict improvement of both at every step. Useful narration: Subquestion changes the wording a lot but is less funny; HUMOR-CoT balances context adaptation and humor; preference tuning further improves humor with a small reduction in this proxy.

Use source table1 exact values above; no significance claim or confidence bars are available. The detailed reward-backbone tau table validates the evaluator but is less engaging than this conceptual tradeoff or real controlled examples.

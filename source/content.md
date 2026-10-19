# HUMOR v2: dense research poster copy

The following poster copy is approximately 820 words excluding tables/equations. Section numbers indicate reading order, not a prescribed grid. Preserve the paper's formal title and author block. The data table has **12** rows in the current manuscript, not nine.

## 1. Motivation and formulation

Meme generation requires more than naming visible objects: the model must infer a template’s communicative intent, connect it to a situation, and realize that connection as a punchline. Direct image-to-caption supervision compresses these associations into one target. A single rationale reconstructed from that target may reinforce literal matching instead of transferable reasoning.

HUMOR combines hierarchical multi-path reasoning with local preference learning. We represent a meme as image–caption pair m = (I,c) and compare candidates within a coherent group G, typically sharing the same template. A latent humor function h_G captures relative quality within G; its scale need not be comparable across templates. The goal is to improve expected group-relative quality while retaining diverse contextual interpretations.

## 2. Hierarchical CoT supervision

**Stage 1: template interpretation and multi-context exploration.** Teacher-generated traces first describe the image, infer a template-level intent, and explore plausible contexts suggested by its visual relationships. For example, an attention shift can express attraction to new technology, a job opportunity, or a tempting purchase. These alternatives separate reusable metaphorical structure from particular objects or keywords.

**Stage 2: ground-truth anchoring.** During supervision construction, the actual context inferred from a real meme caption anchors one compatible reasoning path. The trace then binds contextual roles to image regions and produces a positioned punchline. This combines broad exploration with a concrete example of successful realization, rather than learning only a rationale reverse-engineered from one answer.

**Inference.** No reference caption is available or required. The model hypothesizes contexts from the template, reasons under the user’s intent, and selects a path using its internal decoding policy. Ground-truth anchoring is exclusively a training operation.

## 3. Pairwise reward data and group ranking

We train a reward model on within-group pairs rather than globally calibrated funniness scores. The training curriculum includes five constructed difficulty tiers:

1. **Wrong text:** unrelated captions replace the original text.
2. **Wrong location:** text moves to inappropriate image positions.
3. **Boring:** a mundane caption weakens the original joke.
4. **Detailed boring:** small wording changes degrade the punchline.
5. **Generated:** model-written memes provide harder comparisons against real examples.

These training pairs include synthetic perturbations and generated examples; they are distinct from the human MaxDiff evaluation rankings. A VLM encodes each rendered meme, and a scalar head predicts pairwise preference probabilities. Binary cross-entropy trains the comparator. Expected Borda Count (EBC) aggregates expected pairwise wins into a within-group order, which guides subsequent optimization.

**Display equations**

p̂ᵍᵢⱼ = σ(sφ(mᵢ) − sφ(mⱼ))

EBC_G(mᵢ) = Σⱼ≠ᵢ p̂ᵍᵢⱼ

## 4. Preference optimization and conditional theory

The policy objective increases the likelihood of captions weighted by the group-local preference distribution q_G. KL regularization keeps the generator near its CoT-trained reference. Auxiliary rewards encourage valid reasoning structure and content.

**Display objective, as presented in the paper**

L(θ) = E_(I,G)[−Σₖ q_G(mₖ) log πθ(cₖ|I)] + β E_I[KL(πθ ‖ πref)]

**Exploration bound.** If promising reasoning paths retain probability mass α and the mean quality gap of remaining paths is at most δ, normalized expected humor satisfies E[h̃_G] ≥ 1 − (1 − α)δ. The result is conditional on retained quality mass and bounded gaps; exploration alone does not establish either assumption.

**Preference consistency.** Under the assumed monotone preference-observation model, the analysis supports recovering within-group order. Larger preference margins are more robust to annotation noise.

**KL stability.** For h_G ∈ [0,1], H(θ) ≥ H(ref) − √(Δ_KL/2), where Δ_KL is expected divergence from the reference. This bounds possible degradation, rather than guaranteeing monotonically improving humor.

## 5. Generation quality and ablations

The processed dataset contains 3,345 training and 368 test instances. General human evaluation recruited 30 native-English-speaking annotators; each rated 3–5 memes per method on humor, readability, relevance, and originality. The table reports means on a 0–5 scale.

HUMOR-CoT raises humor from 2.39 to 2.68 and relevance from 2.91 to 3.50 over the 7B baseline. Single-path CoT scores 1.87 on humor, indicating that adding a reasoning trace alone is insufficient. HUMOR-RL reaches 2.83 in preliminary results, while originality decreases from 2.90 to 2.79 relative to CoT. Context-swap distance measures textual divergence after replacing the user context; it is a diversity proxy, not a humor score.

## 6. Evaluation reliability and generalization

**Absolute scores versus local ranks (Fig. 4).** VLM rubric scores poorly separate human-created memes from text-free images. Group-wise ranking gives clearer distinctions. Independent validation used nine annotators, five image groups, and 30 memes: Gemini–human mean correlations were Spearman 0.72 and Kendall τ = 0.63.

**Reward–human agreement (Table 2).** Human MaxDiff rankings use 100 participants and five templates with 10–15 candidates each. Keye-VL-8B improves from τ = 0.05–0.29 to 0.77–0.78 after reward training. Improvements are less consistent on Qwen backbones.

**Unseen templates (Fig. 5).** On 20 templates without training image–text overlap, HUMOR-CoT ranks second to human-created memes under Gemini-2.5-pro group-wise evaluation. Evidence remains bounded by English-language meme culture, small human-rating samples, and approximately 2–3× output-token cost.

## Full generation table

| Model | Humor ↑ | Readability ↑ | Relevance ↑ | Originality ↑ | Context-swap distance ↑ |
|---|---:|---:|---:|---:|---:|
| Qwen2.5-7B-Instruct | 2.39 | 3.35 | 2.91 | 2.57 | .564 |
| Qwen2.5-32B-Instruct | 2.54 | 3.52 | 3.09 | 2.76 | .566 |
| InternVL3-8B | 2.39 | 2.79 | 3.04 | 2.79 | .564 |
| GLM-4.1V-9B-Thinking | 1.73 | 2.62 | 2.75 | 2.71 | .572 |
| Keye-VL-8B-preview | 2.35 | 3.19 | 2.99 | 2.71 | .580 |
| GPT-4o | 2.70 | 2.99 | 3.21 | **2.97** | .552 |
| Gemini-2.5-flash | 2.81 | 3.29 | 3.25 | 2.88 | .561 |
| HUMOR-CoT | 2.68 | **3.70** | 3.50 | 2.90 | .590 |
| CoT: Single Path | 1.87 | 2.79 | 2.68 | 2.45 | .570 |
| CoT: Self-Improve | 2.38 | 3.68 | 3.00 | 2.65 | .578 |
| CoT: Subquestion | 1.85 | 3.32 | 2.58 | 2.47 | **.597** |
| HUMOR-RL (preview) | **2.83** | 3.67 | **3.55** | 2.79 | .588 |

Table notes: all human values reported means, no CIs supplied. All fine-tuned rows use the paper's 7B backbone. Model naming above follows Table 1 verbatim (which omits VL in Qwen names); avoid silently introducing an unconfirmed model ID.

## Production and source cautions (not poster copy)

- Formula is accurately reproduced from Eq. 4; label “policy objective” instead of suggesting this is the standard clipped GRPO implementation. It is weighted cross-entropy plus KL in the paper.
- Sources: section/4.Method.tex; section/5.Experiments.tex; Appendix sections on pair data, human evaluation, ranking alignment.
- Figure 4 original asset: figure/combined_parallel_coordinates_plot.pdf. Figure 5 original asset: figure/unseen.pdf. Original method assets: cot_data.pdf and pipeline.pdf.
- Human Rate is deliberately omitted: it measures Gemini human/AI discrimination, not human humor preference.
- Do not call the pair curriculum's orderings guaranteed ground truth; the manuscript's own constructed-data assumptions warrant softer wording.
- The manuscript's tier sampling wording conflicts (upweight harder tiers vs equal number per tier); omit sampling weights on poster.

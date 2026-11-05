# Interesting experiments for poster revision

All claims checked against current repository PDF `/Users/lixy/文档/vault/Parttime/论文/HUMOR-poster-v2/assets/Meme_NeurIPS_2026.pdf`, 56 pages. Current poster read via revision-1105/source/poster_copy.md. Original LaTeX Appendix.tex lines 790–841 and 938–979 agrees with PDF, with one qualitative-caption discrepancy noted below.

## Recommended 1: Beyond memes: more ways to caption the same image

Replace reward-model consistency table with a compact quantitative persona pilot. This adds a different task while reinforcing BOTH exploration diversity and local comparison. Source: PDF p33 Figure15, Table6, p34 Table7; Appendix L.2. Actual figure `/Users/lixy/文档/vault/Parttime/论文/Meme_NeurIPS_2026__Copy_/figure/personality_caption_pilot.png`.

Exact setup: 20 recovered image-personality groups; same Qwen2.5-VL-7B-Instruct generator, four candidates per method and group. Direct generation versus HUMOR-style reasoning + local selection. This is NOT full HUMOR-RM training transfer.

Table6:
| Method | distinct-1 | distinct-2 | avg pairwise sentence distance |
| Direct | .734 | .960 | .507 |
| HUMOR-style | .738 | .942 | .563 |
Semantic distance rises 11.05%; bigram diversity falls. Do not label the .507→.563 metric as humor, quality, or general-purpose diversity without “semantic”.

Table7, each row totals20, HUMOR wins / ties / losses:
- Qwen2.5-VL-7B-Instruct: 14 / 0 / 6
- MiniMax-M3: 12 / 3 / 5
- Step-3.7-Flash: 10 / 9 / 1
The third judge IS in repository PDF; older poster_text omitted it. Prefer all3 equal-length segmented bars. A 70% universal win-rate claim is invalid; that is only Qwen.

Print-ready English:
Title: “Beyond memes: persona-conditioned captions”
Setup: “20 image–persona groups · 4 candidates per method · same 7B model”
Main finding: “Semantic diversity: 0.507 → 0.563 (+11%). Local judges prefer the selected HUMOR-style caption more often than the direct baseline.”
Plot legend: “HUMOR wins / ties / losses”
Small qualifier: “Pilot: reasoning + selection only; no reward-model retraining. Bigram diversity decreases (0.960 → 0.942).”

Potential sharper annotation: “Absolute scores tie at 4.0 for all 160 captions; local comparisons still reveal preferences.” Source explicitly says every dimension is4.0. This is striking but primarily evaluation-motivation; keep one sentence, do not build a whole validation section.

Optional genuine caption example from Fig15 right (serious persona, meeting photo):
Direct: “Focused minds converge in a serious brainstorming session.”
HUMOR-style: “A focused team discusses critical strategies in a professional setting.”
Both scored4.0. Neither is visually especially compelling; prefer chart over spending much area on this example. Do not call it humorous, it is persona captioning.

## Recommended 2: When keywords flatten the joke

A compact visual failure case adds a memorable discussion point and complements gains. Source PDF p40 Fig20, qualitative interpretation p37 N.5. `/Users/lixy/文档/vault/Parttime/论文/Meme_NeurIPS_2026__Copy_/figure/failure_case.pdf`.

Original embedded raster images extracted directly from current repository PDF to:
- `/tmp/humor-new-assets/cloud-template.png`
- `/tmp/humor-new-assets/cloud-human.png`
- `/tmp/humor-new-assets/cloud-humor.png`
- `/tmp/humor-new-assets/provenance.json`
All275×183 pixels. These preserve image captions exactly. Use ~75–95mm physical width perimage; add caption transcription beneath ifnecessary for print readability.

Human actual image text:
“JUST A REMINDER: / THERE IS NO \"CLOUD\" / JUST \"SOMEBODY ELSE'S COMPUTER\"”
HUMOR-CoT image text:
“YOUR DATA / IS IN THE CLOUD”
Input terms include technology, daily life, cloud storage, data ownership, love, humor. Highlight “cloud storage / data ownership”.

IMPORTANT: prose in Appendix says the human meme uses “just a cloud”, but that phrase belongs to the generated reasoning path, NOT the actual human image. Use image evidence as above. Do not recreate the wrong human caption.

Print-ready English:
Title: “When keywords flatten the joke”
Input label: “User keywords: cloud storage · data ownership”
Image labels: “Human reference” / “HUMOR-CoT”
Caption: “The model follows the keywords, but settles for a literal cloud pun instead of the reference's twist about data ownership.”
Qualifier ifspace: “Qualitative failure case, not a measured failure rate.”

Layout: two image panels side-by-side; input strip above; one short conclusion below. The source long reasoning box is unnecessary. This is easy to explain aloud in15seconds, culturally accessible, and invites question about balancing adherence and surprise.

## Optional alternate: Diversity alone is not enough

Replot selected Table1 rows in humor-versus-context-swap-distance scatter, rather than a separate fulltable. This directly connects theoretical motivation to empirical tradeoff. PDF mainTable1; exact values:
Base7B (.564,2.39), Single-path (.570,1.87), Self-improve (.578,2.38), Subquestion (.597,1.85), HUMOR-CoT (.590,2.68), HUMOR-RLpreview (.588,2.83).
Coordinates (context-swap distance, human Humor rating). Show all alternativeCoTs and baseline, emphasize our2rows. Subquestion has highest distance but lowest humor amongtheseexcept? 1.85 < single1.87, so indeed lowest here. HUMOR-RL increases humor vsCoT while distance slightly declines; do NOT claimRL improvesboth.
Title: “More variation does not automatically mean a better joke”
Caption: “Subquestion CoT changes captions most under a context swap, but scores lower on humor. HUMOR balances the two in this comparison.”
Limit: distance is not proven useful diversity, no CIsavailable, no per-case causal claim. Since parent already redesigns Table1 and adds2sections, this may fit as compact commentary rather than thirdexperiment.

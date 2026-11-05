# Poster brief · revision-1105

Audience: research attendees working on vision-language models, multimodal reasoning and preference learning. Format: English, 140 × 90 cm landscape.

The central claim is that meme generation benefits from a connected sequence of hierarchical multi-path reasoning, template-local preference learning and KL-controlled policy optimization. The poster explains each mechanism and assigns a separate evaluation question to generation quality, reward agreement and unseen-template transfer.

The reading route is task → A/B/C mechanism → quantitative evidence → thematic examples → reward validation → transfer. The six modules provide independent entry points for a live research discussion. Their interpretation and speaking routes are documented in ../设计说明与讲解路线.md.

Visual emphasis is tied to meaning: the selected scenario in A matches the real caption's inferred context, the gold region represents supervised reverse anchoring, and the inference strip states the inference condition. C treats its workflow steps equally. The result sidebar compares HUMOR-CoT with the same 7B base using descriptive differences.

The six gallery images are original Fig.16 crops under Christmas and Romance inputs. The generator table reports all original rows and metrics. The reward table shows tau with source-derived significance symbols, with exact p-values retained separately. The transfer chart contains all seven source series and eight evaluation dimensions.

Scientific statements follow the supplied paper. Theoretical bounds are conditional, human and model-based evaluators are identified separately, and RL results are labeled preview. Data, image provenance and verification records are maintained in source/.

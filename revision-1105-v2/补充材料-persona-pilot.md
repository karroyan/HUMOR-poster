# 补充实验：Persona-conditioned captioning

来源：论文 Appendix L.2，Tables 6–7（第33–34页）。

20个 image–persona groups，同一7B模型，每个方法生成4个候选。比较直接生成与 HUMOR-style reasoning + local selection；未进行完整奖励模型迁移训练。

| 指标 | Direct | HUMOR-style |
|---|---:|---:|
| distinct-1 | .734 | .738 |
| distinct-2 | .960 | .942 |
| 平均句子语义距离 | .507 | .563 |

语义距离提高约11%，bigram多样性略降。

| 评价模型 | HUMOR胜 | 平 | 负 |
|---|---:|---:|---:|
| Qwen2.5-VL-7B | 14 | 0 | 6 |
| MiniMax-M3 | 12 | 3 | 5 |
| Step-3.7-Flash | 10 | 9 | 1 |

这是小规模方向性证据，不等于完整跨领域训练验证。可在讨论方法迁移性时补充。原文还报告160个候选的独立绝对评分均为4.0，而局部比较能区分偏好。

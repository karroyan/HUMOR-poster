# Table 2 · full reward-agreement values

Each cell is Kendall τ / p. These p-values test ranking agreement, not the trained-minus-base difference.

| Reward backbone / state | G1 τ / p | G2 τ / p | G3 τ / p | G4 τ / p | G5 τ / p |
|---|---|---|---|---|---|
| Qwen2.5-VL-7B · base | 0.16 / 0.60 | 0.28 / 0.17 | 0.47 / 0.07 | -0.10 / 0.63 | 0.29 / 0.29 |
| Qwen2.5-VL-7B · trained | 0.47 / 0.07 | 0.56 / 0.03 | 0.42 / 0.11 | 0.14 / 0.50 | 0.47 / 0.07 |
| Qwen2.5-VL-32B · base | 0.16 / 0.61 | 0.16 / 0.44 | -0.02 / 1.00 | 0.14 / 0.50 | 0.29 / 0.29 |
| Qwen2.5-VL-32B · trained | 0.29 / 0.29 | 0.47 / 0.02 | 0.07 / 0.86 | 0.30 / 0.14 | 0.42 / 0.11 |
| Keye-VL-8B · base | 0.05 / 0.85 | 0.09 / 0.70 | 0.16 / 0.60 | 0.29 / 0.29 | 0.16 / 0.60 |
| Keye-VL-8B · trained | 0.78 / <.001 | 0.77 / <.001 | 0.78 / <.001 | 0.78 / <.001 | 0.78 / <.001 |

Source: paper Table 2, §4.3; 100 Prolific MaxDiff raters, 5 templates, 10–15 candidates per template. The source prints 0.00*** for Keye trained; the stars indicate p<.001.

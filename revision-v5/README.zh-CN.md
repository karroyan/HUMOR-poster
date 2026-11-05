# HUMOR 学术海报 · revision-v5

**From Perception to Punchline: Empowering VLM with the Art of In-the-wild Memes**

140 × 90 cm 横版研究海报。采用三栏结构：左栏定义 meme 任务与局部比较动机，中栏展开多路径推理、偏好学习和策略优化，右栏集中呈现生成、reward agreement 与泛化证据。

## 文件入口

| 文件 | 用途 |
|---|---|
| [HUMOR-poster.html](HUMOR-poster.html) | 离线浏览、整版缩放和打印入口 |
| [HUMOR-poster-preview.png](HUMOR-poster-preview.png) | 快速查看整体布局 |
| [HUMOR-poster-print.pdf](HUMOR-poster-print.pdf) | 单页定尺寸印刷文件 |
| [HUMOR-poster-editable.svg](HUMOR-poster-editable.svg) | 矢量编辑文件 |
| [设计说明与讲解路线.md](设计说明与讲解路线.md) | 表达目标、视觉逻辑、公式解读和现场讲述 |

## 内容与结构

任务区以 Distracted Boyfriend 和 Apple 角色绑定解释输入与位置输出；方法区以 Mr. Bean 展示多场景联想与训练锚定，以猫图展示构造偏好 pairs；证据区包含主结果表、工作场景生成对比、reward 排序一致性及未见模板平均排名。

主表展示全部 12 个模型或变体、四项人类评分及 context-swap distance。人类评分、MaxDiff 排序和 Gemini 评价具有不同含义，详细解读见设计说明。RL 标注为 preview，保留质量收益与原创性之间的取舍。

## 目录与来源

- `assets/`：meme 图像与实验示例。
- `fonts/`：DejaVu 字体及许可证。
- `source/`：场景、文案、数据、生成脚本、素材来源与核验记录。

科学内容以共享论文 `../assets/Meme_NeurIPS_2026.pdf` 为依据。来源记录见 `source/provenance.json`；主表、reward 与未见模板数据核对见 `source/evidence-validation.json`。

## 编辑与重新生成

在本目录执行：

```bash
MPLCONFIGDIR=/tmp/humor-v5-mpl /usr/bin/python3 source/build_poster.py
```

生成依赖 Python 3、matplotlib、Pillow。正文与图形由场景生成，公式通过 mathtext 输出为矢量。完整内容核验脚本为 `source/verify_evidence.py`，另需 pypdf。

SVG 内嵌字体；在不支持内嵌字体的编辑器中，先安装 `fonts/` 中字体，并检查导入后的文字位置。打印使用 PDF，选择 **100% 实际尺寸**。HTML 内嵌图像与字体，采用固定画布整体缩放。

## 核验范围

既有记录覆盖物理尺寸、字体嵌入、文本和公式边界、图像比例、HTML/SVG 一致性，以及主表 60 个数值、reward 表 30 个 τ、Fig.5 的 56 个绘图值。记录位于 `source/validation.json`、`evidence-validation.json`、`image-validation.json` 和 `html-validation.json`。编辑器导入与浏览器打印仍需在相应客户端检查。

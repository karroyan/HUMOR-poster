# HUMOR 海报 v2

## 版本资料入口

| 目录 | 内容组织 | 设计与讲解材料 |
|---|---|---|
| [revision-v5](revision-v5/README.zh-CN.md) | 三栏研究叙事，方法与证据展开 | [设计说明与讲解路线](revision-v5/设计说明与讲解路线.md) |
| [revision-1105](revision-1105/README.zh-CN.md) | 六个模块、A/B/C 流程、双主题示例 | [设计说明与讲解路线](revision-1105/设计说明与讲解路线.md) |

以下说明对应根目录的原始海报文件；两个版本的文件、生成方式和核验范围见各自 README。


尺寸：140 × 90 cm，横向。此版根据用户提供的 56 页论文及 LaTeX 源文件重做；原稿未修改。

## 在 Figma 中打开

- 直接将 `HUMOR-poster-figma.svg` 拖入 Figma 设计文件。图形和图像可继续排版；SVG 导入时文字可能被转为轮廓。
- 若要保留可编辑文字，使用 `figma-native-importer/` 中的本地插件，导入 `HUMOR-scene.json`。详细步骤见该目录 README。主要文字、表格、方法示意、未见模板折线图均由独立图层组成；原论文 Fig. 4 和 meme 样例是嵌入图像。
- 没有伪造 `.fig` 文件。未在实际 Figma 客户端完成导入测试；字体和文字基线仍需在导入后检查。已检查 PDF 排版、画布尺寸、字符覆盖和文本边界。

## 交付内容

- `HUMOR-poster-print.pdf`：1 页印刷文件，140 × 90 cm。
- `HUMOR-poster-figma.svg`：可导入 Figma 的整版 SVG。
- `HUMOR-poster-preview.png`：整版预览。
- `HUMOR-scene.json` + `figma-native-importer/`：保留原生文字的导入方案。
- `设计说明与讲解路线.md`：分区内容、设计逻辑和现场讲解。
- `assets/`：原论文图表 PDF、真实 meme 裁图及海报使用图片。
- `source/`：数据、调研来源、完整文案、验证记录和可复现源文件。

## 重要细节

主结果表保留全部 12 个模型/变体；展示 4 项人评指标及 context-swap distance。未展示 Human Rate（它是模型辨别人类/AI 内容的比例，并非幽默偏好）。RL 明确标为 preview，且保留其 originality 下降的信息。

Fig. 5 根据原矢量 PDF 的曲线坐标重绘为可编辑图形，非目测估算；具体坐标和来源记录在 `source/unseen-figure-data.json`。Fig. 4 保留原图，去除底部无用的 (a)/(b) 标号。方法图中的三个上下文是机制说明，不是新增实验结果。

海报约 850 词（含表格标签等）。颜色为深青绿 #146C68、正文 #172B31、少量赭色 #A5682D。正文以约 27–30 pt 为主。个别原图轴标仍较小，建议现场用主标题和图注引导阅读，电子版可放大。

Paper 链接指向公开 arXiv 摘要页。该公开版本可能较本地论文旧；海报数值以本地稿件为准。

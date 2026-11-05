# HUMOR 学术海报 · revision-1105

**From Perception to Punchline: Empowering VLM with the Art of In-the-wild Memes**

140 × 90 cm 横版会议海报。六个模块依次呈现任务定义、A/B/C 方法、生成质量、双主题输出、reward agreement 和未见模板泛化，适合现场按问题展开交流。

## 文件入口

| 文件 | 用途 |
|---|---|
| [HUMOR-poster.html](HUMOR-poster.html) | 离线浏览与整版缩放 |
| [HUMOR-poster-preview.png](HUMOR-poster-preview.png) | 快速查看整体布局 |
| [HUMOR-poster-print.pdf](HUMOR-poster-print.pdf) | 单页 1400 × 900 mm 打印文件 |
| [HUMOR-poster-editable.svg](HUMOR-poster-editable.svg) | 矢量编辑文件 |
| [HUMOR-poster-editable.pptx](HUMOR-poster-editable.pptx) | PowerPoint 编辑文件 |
| [设计说明与讲解路线.md](设计说明与讲解路线.md) | 设计逻辑、各区解读、公式衔接和现场讲述 |

## 阅读主线

01 用模板、主题和角色位置定义任务。02 的 A/B/C 分别处理推理覆盖、局部偏好和受控更新。03 展示完整主结果与同 backbone 增量；04 以 Christmas / Romance 两个主题展示人类参考、Single-path 和 HUMOR-CoT；05 单独检验 reward 与人类排序的一致性；06 展示 20 个未见模板上的平均排名。

三条完整关联分支、反向锚定箭头、good-path 条件下界和推理条件共同组成 A 的解释。B 区分五类训练 pairs 与三步算法；C 的三步保持一致视觉权重。两张表保留必要评价来源，未见模板图以七种颜色和逐模型图例支持读图。

## 目录与数据

- `assets/`：当前场景使用的图像与公式 SVG。
- `fonts/`：DejaVu 字体及许可证。
- `source/`：生成器、配置、场景、内容提纲、表格数据、图表来源与核验记录。

完整 reward τ / p 数据见 [附表](source/table2_full_values.md)。原论文使用共享路径 `../assets/Meme_NeurIPS_2026.pdf`。数据解释、素材来源和适用边界见设计说明及 `source/provenance.json`。

## 编辑与重新生成

在本目录执行：

```bash
MPLCONFIGDIR=/tmp/humor-1105-mpl /usr/bin/python3 source/build_poster.py
/usr/bin/python3 source/verify_evidence.py
```

生成依赖 Python 3、matplotlib、Pillow、PyYAML。首条命令生成 PDF、PNG、SVG、PPTX 和 HTML；编辑入口为 `source/build_poster.py`，配置为 `source/poster.yaml`。配置读取模块来自 Paper2Poster，许可证见 `source/LICENSE_Paper2Poster`。

生成只使用本目录材料。完整证据核验还使用上述共享论文路径。将本目录单独复制到其他位置时，应为核验提供同样的论文路径。

## 使用与核验

打印使用 PDF，选择 **100% 实际尺寸**。SVG 编辑前按需安装 `fonts/` 中字体。PPTX 的正文、表格与图形可编辑，公式保留为 SVG；导入或字体替换后需检查版面。

核验覆盖主表 83 个已报告数值、reward 表 60 个 τ / p 数值、Fig.5 的 56 个绘图值、六张主题输出裁片及其他素材，以及重叠、边界、公式、PDF 字体和尺寸。独立重生成的预览已进行像素比较。记录见 `source/evidence-validation.json`、`layout_validation.json`、`organization-validation.json`。

PPTX 已进行结构校验，Office/LibreOffice 显示效果尚无客户端实测记录。HTML 使用与独立 SVG 相同的画布，浏览器打印效果应在实际交付环境中检查。

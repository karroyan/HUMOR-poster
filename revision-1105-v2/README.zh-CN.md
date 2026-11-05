# HUMOR 海报：叙事与实验修订版

基于 revision-1105 修订，保留原作者顺序、配色及真实图像，尺寸 140 × 90 cm。

## 打开与编辑

- 印刷：`HUMOR-poster-print.pdf`，100% 实际尺寸。
- Figma：将 `HUMOR-poster-editable.svg` 拖入画布；字体文件位于 `fonts/`。SVG 中正文为文字，公式为矢量路径，图像内文字保持原始像素。Figma 可能将 SVG 文字转成轮廓，本轮未实测 Figma 导入。
- 浏览：`HUMOR-poster.html`，可离线打开。
- 预览：`HUMOR-poster-preview.png`。
- 本次没有新增或改写 PPTX，避免把上版 PowerPoint 当成本版交付。

## 主要修改

01 用“探索不同想法，再判断哪种表达更好”引出 A/B。

A 将训练推理链构造的两步明确标为 REFERENCE CAPTION HIDDEN / REFERENCE REVEALED。第一步不提供真实配文，第二步从真实配文反推情境并锚定已有路径。推理时不使用参考配文作为单独的小字说明，避免混淆两种操作。

B 按主观评分难校准、固定模板与意图后的局部比较、五种训练难度、成对偏好概率、EBC 预计胜场的顺序解释。不声称 DPO 在此任务中效果差；EBC 是比较聚合，DPO 是策略训练目标，两者不在同一环节。

C 集中展示两个不同对象的条件界：归一化推理路径质量缺口，以及策略更新后相对 CoT 的可能幽默损失。没有将路径质量与最终配文幽默度强行等同，也没有宣称多样性或幽默无损得到证明。

主表保留全部 12 个变体与 7 项指标，缩小占位，旁边改为幽默度×context-swap distance 的散点图，包含 7B、三种 CoT 消融、HUMOR-CoT 与 RL。05 恢复 reward agreement 完整表，展示三种 backbone、训练前后和五个模板的全部结果。06 保留用户意图还原实验。Persona pilot 移入 `补充材料-persona-pilot.md`。未见模板曲线保留。

## 证据与限制

- 散点来自 Table 1；context-swap distance 是多样性代理，不等于创造力或质量。
- Persona：论文第33–34页 Tables 6–7，20组，4候选/方法；语义距离 .507→.563；三位judge胜/平/负14/0/6、12/3/5、10/9/1。仅 reasoning + selection pilot，未做完整奖励模型迁移训练。bigram diversity略降。
- 论文来源为仓库共享 assets/Meme_NeurIPS_2026.pdf。06 采用 Table 5 的情绪、意图、主题、风格四项 VLM 重分类准确率，保留三个模型全部 12 个数值；HUMOR 7B 四项均超过 7B 基线，三项超过 32B，主题项略低。新增实验证据页保存在 source/new-experiment-evidence.pdf。
- 本版保留有限人评、英文文化范围、生成成本等说明在讲稿中，供现场问答。

## 检查与重建

PDF 已渲染检查；公式无越界、正文无相互重叠、所有文字位于对应模块内。主表与未见模板数据文件和上版完全一致。新增数据核对当前论文 PDF。

生成入口 `source/build_poster.py`，依赖 Python、matplotlib、PyYAML、Pillow。源文件从自身目录定位素材；配置位于 source/poster.yaml。源码保留 Paper2Poster 配置读取器及许可证。运行后生成 PDF、SVG、PNG、HTML。

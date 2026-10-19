# HUMOR 海报：Figma 可编辑导入

此离线开发插件将 `HUMOR-scene.json` 转换成 Figma 原生文字、矩形、线段和图片图层。无需网络或 API 密钥。

1. 在 Figma 桌面版打开一个设计文件。
2. 在插件开发菜单中选择导入本地插件（Import plugin from manifest），选择本目录的 `manifest.json`。
3. 运行 **HUMOR Poster — Editable Import**。
4. 选择交付文件中的 `HUMOR-scene.json`，点击“导入到当前 Figma 页面”。
5. 导入后检查标题、正文、图表标签及图片；修改后保存为自己的 Figma 文件。

插件建立 1400 × 900 mm 对应的 5291.34 × 3401.57 px 画布（96 dpi），即 140 × 90 cm 横向海报。Figma 的 PDF 导出可能采用不同像素与物理尺寸换算；正式印刷优先使用交付的定尺寸 PDF。若从 Figma 导出，请让印厂按 **140 × 90 cm** 的最终成品尺寸输出并核对页面比例。

优先使用 Arial Regular / Bold；不可用时自动改用 Inter。文字保留可编辑内容。SVG 基线换算为 Figma 文本框顶部使用近似字体度量，字体替代会改变字宽，导入后必须检查文字对齐。图片为嵌入位图，可移动与替换，图片内的原论文字样不成为可编辑文字。

已进行 JavaScript 语法检查；未在实际 Figma 会话内执行导入验证。导入失败会移除本次创建的海报画布，并显示错误。可保留交付的 SVG 作为视觉参考。

若本机 Figma 要求由账户生成的插件 ID，可先在开发菜单创建一个本地插件，保留 Figma 生成的 manifest 中的 `id`，将其余字段与本目录的 manifest 对齐，并复制本目录的 `code.js` 和 `ui.html` 到新插件目录，再运行。此工具不需要发布。

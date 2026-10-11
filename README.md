# oxygenxx77.github.io

作品集「秋招手帐」：<https://oxygenxx77.github.io>

纯静态单页（`index.html` + `assets/`），没有构建步骤。本地预览：

```bash
python3 -m http.server 8000
```

## 设计

页面按手帐拼贴的风格做：点阵纸、纸胶带贴住的截图、红笔批注、便利贴。配色、字体、间距等规格记在 [`design/design-dna.json`](design/design-dna.json)，用 [design-dna](https://github.com/zanwei/design-dna) 的格式写成，颜色取自工具截图的实测值。

标题用 [霞鹜文楷](https://github.com/lxgw/LxgwWenKai)，批注用 [龙藏体](https://fonts.google.com/specimen/Long+Cang)，都只保留页面用到的字，放在 `assets/fonts/`。改了页面文字后重新生成：

```bash
pip install fonttools brotli
python3 tools/subset_fonts.py
```

## 许可证

[MIT](LICENSE)。`assets/fonts/` 里的两款字体遵循 SIL Open Font License（见同目录下的 OFL 文件）。

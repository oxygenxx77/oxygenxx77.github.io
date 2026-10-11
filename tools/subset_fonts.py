"""把标题字体和手写字体裁成只含 index.html 用到的字，输出到 assets/fonts/。

改了页面文字后重新运行：
    pip install fonttools brotli
    python3 tools/subset_fonts.py
原始字体会下载到 ~/.cache/portfolio-fonts/（约 30 MB，只下载一次）。
"""
import re
import urllib.request
from pathlib import Path

from fontTools import subset

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path.home() / ".cache" / "portfolio-fonts"
OUT = ROOT / "assets" / "fonts"

FONTS = {
    "wenkai-medium.woff2": "https://github.com/lxgw/LxgwWenKai/releases/download/v1.522/LXGWWenKai-Medium.ttf",
    "longcang.woff2": "https://github.com/google/fonts/raw/main/ofl/longcang/LongCang-Regular.ttf",
}


def page_text() -> str:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    html = re.sub(r"<(style|script)\b.*?</\1>", "", html, flags=re.S)
    text = re.sub(r"<[^>]+>", "", html)
    printable_ascii = "".join(chr(c) for c in range(0x20, 0x7F))
    return "".join(sorted(set(text + printable_ascii + "，。、；：？！「」『』（）《》—…·～①②③④⑤✓✗")))


def source(url: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / url.rsplit("/", 1)[1]
    if not path.exists():
        print(f"下载 {path.name} …")
        urllib.request.urlretrieve(url, path)
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    chars = page_text()
    for name, url in FONTS.items():
        options = subset.Options()
        options.flavor = "woff2"
        options.layout_features = ["*"]
        font = subset.load_font(str(source(url)), options)
        subsetter = subset.Subsetter(options)
        subsetter.populate(text=chars)
        subsetter.subset(font)
        subset.save_font(font, str(OUT / name), options)
        print(f"{name}: {len(chars)} 个字符，{(OUT / name).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

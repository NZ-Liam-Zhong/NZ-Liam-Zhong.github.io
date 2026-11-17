"""Write /viper/index.html (English) and /viper/zh.html from a VIPER checkout's guides.

    uv run --with markdown python viper/_build.py ~/Desktop/VIPER_Temp

Jekyll skips files that start with an underscore, so this script is not
published; the pages it writes have no front matter and are copied as they are.
"""

import html
import re
import sys
from pathlib import Path

import markdown

REPO = "https://github.com/runtime-si/VIPER_Temp"
BRANCH = "main"
HERE = Path(__file__).parent

PAGES = {
    "en": {
        "source": "docs/guide.md",
        "out": "index.html",
        "lang": "en",
        "title": "Using VIPER",
        "other": ("zh.html", "简体中文"),
    },
    "zh": {
        "source": "docs/guide.zh-CN.md",
        "out": "zh.html",
        "lang": "zh-CN",
        "title": "VIPER 使用指南",
        "other": ("./", "English"),
    },
}

# The English guide used to live here; old links land on it again.
MOVED = {"en.html": "./"}

STYLE = """
:root { --fg: #1f2328; --muted: #59636e; --line: #d1d9e0; --soft: #f6f8fa; --accent: #0969da; }
* { box-sizing: border-box; }
body { margin: 0; color: var(--fg); background: #fff;
  font: 16px/1.7 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB",
  "Microsoft YaHei", Helvetica, Arial, sans-serif; }
header { position: sticky; top: 0; z-index: 2; background: rgba(255,255,255,.96);
  border-bottom: 1px solid var(--line); }
header .bar { max-width: 920px; margin: 0 auto; padding: 10px 20px; display: flex; gap: 18px;
  align-items: center; }
header .brand { font-weight: 600; margin-right: auto; color: var(--fg); text-decoration: none; }
header a { color: var(--muted); text-decoration: none; font-size: 14px; }
header a:hover { color: var(--accent); }
main { max-width: 920px; margin: 0 auto; padding: 8px 20px 80px; }
h1 { font-size: 2em; margin: 28px 0 12px; }
h2 { font-size: 1.45em; margin: 44px 0 12px; padding-bottom: 6px; border-bottom: 1px solid var(--line); }
h3 { font-size: 1.15em; margin: 30px 0 8px; }
a { color: var(--accent); }
code { font: 0.88em/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  background: var(--soft); padding: 0.15em 0.35em; border-radius: 5px; }
pre { background: var(--soft); border: 1px solid var(--line); border-radius: 8px; padding: 14px 16px;
  overflow-x: auto; }
pre code { background: none; padding: 0; font-size: 0.85em; }
pre.mermaid { background: #fff; text-align: center; }
table { border-collapse: collapse; width: 100%; margin: 14px 0; display: block; overflow-x: auto; }
th, td { border: 1px solid var(--line); padding: 7px 11px; text-align: left; vertical-align: top; }
th { background: var(--soft); font-weight: 600; }
blockquote { margin: 0; padding: 0 14px; color: var(--muted); border-left: 4px solid var(--line); }
img { max-width: 100%; height: auto; border: 1px solid var(--line); border-radius: 10px; }
"""


def slug(value: str, separator: str) -> str:
    """GitHub's heading anchors, so the guides' own links work here too."""
    value = re.sub(r"[^\w\- ]", "", value.strip().lower())
    return value.replace(" ", separator)


def links(text: str, checkout: Path) -> str:
    """Point the guides' links into the repository at GitHub, and copy their pictures here."""

    def repoint(match: re.Match) -> str:
        bang, label, target = match.group(1), match.group(2), match.group(3)
        if bang:
            if not target.startswith("http"):
                (HERE / target).parent.mkdir(parents=True, exist_ok=True)
                (HERE / target).write_bytes((checkout / "docs" / target).read_bytes())
            return f"![{label}]({target})"
        if target.startswith(("http", "#")) or target in ("guide.md", "guide.zh-CN.md"):
            target = {"guide.md": "./", "guide.zh-CN.md": "zh.html"}.get(target, target)
            return f"[{label}]({target})"
        path = Path("docs", target).as_posix().replace("docs/../", "")
        return f"[{label}]({REPO}/blob/{BRANCH}/{path})"

    return re.sub(r"(!?)\[([^\]]+)\]\(([^)\s]+)\)", repoint, text)


def page(checkout: Path, spec: dict) -> str:
    text = (checkout / spec["source"]).read_text()
    text = re.sub(r"^\[(English|简体中文)\]\([^)]*\)\n", "", text, flags=re.M)
    body = markdown.markdown(
        links(text, checkout),
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"slugify": slug}},
    )
    body = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        r'<pre class="mermaid">\1</pre>',
        body,
        flags=re.S,
    )
    href, label = spec["other"]
    title = html.escape(spec["title"])
    return f"""<!DOCTYPE html>
<html lang="{spec["lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>{title}</title>
  <style>{STYLE}</style>
</head>
<body>
<header><div class="bar">
  <a class="brand" href="#">VIPER</a>
  <a href="{href}">{label}</a>
  <a href="{REPO}">GitHub</a>
</div></header>
<main>
{body}
</main>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({{ startOnLoad: true, theme: "neutral", securityLevel: "strict" }});
</script>
</body>
</html>
"""


def moved(target: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex, nofollow">
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{target}">
  <title>Using VIPER</title>
</head>
<body><p>The guide is now at <a href="{target}">{target}</a>.</p></body>
</html>
"""


def main() -> None:
    checkout = Path(sys.argv[1]).expanduser()
    for spec in PAGES.values():
        (HERE / spec["out"]).write_text(page(checkout, spec))
        print(HERE / spec["out"])
    for name, target in MOVED.items():
        (HERE / name).write_text(moved(target))
        print(HERE / name, "->", target)


if __name__ == "__main__":
    main()

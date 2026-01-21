from pathlib import Path
from utils import google_news_text_only_markdown

out = Path("docs/news.md")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(google_news_text_only_markdown(limit=10), encoding="utf-8")
print(f"Wrote {out}")

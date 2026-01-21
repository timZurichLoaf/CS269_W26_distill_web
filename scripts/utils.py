#  %%
# utils.py
import feedparser
import html
import re
from datetime import datetime, timezone, timedelta

FEED_URL = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
CTRL_RE = re.compile(r"[\u0000-\u001F\u007F]")

def clean_text(s: str) -> str:
    s = html.unescape(s or "")
    s = TAG_RE.sub(" ", s)
    s = URL_RE.sub("", s)
    s = CTRL_RE.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def split_headline_source(rss_title: str):
    t = clean_text(rss_title)
    if " - " in t:
        headline, source = t.rsplit(" - ", 1)
        return headline.strip(), source.strip()
    return t, ""

def _feed_asof_time() -> str:
    """
    Always return the current time in PST (UTC-8), ignoring DST.
    """
    pst = timezone(timedelta(hours=-8), name="PST")
    dt = datetime.now(pst)
    return dt.strftime("%Y-%m-%d %H:%M")

def google_news_text_only_markdown(limit: int = 10) -> str:
    feed = feedparser.parse(FEED_URL)
    as_of = _feed_asof_time()
    # lines = [
    #     f"# Google News (text-only)",
    #     f"As of {as_of} Los Angeles",
    #     ""
    # ]

    lines = [
        f"As of {as_of} Los Angeles",
        ""
    ]

    for e in feed.entries[:limit]:
        headline, source = split_headline_source(getattr(e, "title", ""))
        parts = [p for p in [headline, source] if p]
        if parts:
            lines.append("- " + " — ".join(parts))
    return "\n".join(lines).strip()

# # %%
# if __name__ == "__main__":
#     print(google_news_text_only_markdown(limit=25))


# # %%

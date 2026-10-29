"""Publish the Patreon posts the title screen shows to the `devstatus` branch.

The game reads
https://raw.githubusercontent.com/SuIT-pub/Mind-the-School/devstatus/news/news.json
and the thumbnails next to it, so news reach players without a game update and
without the game ever talking to Patreon (the creator token stays in GitHub).

What gets picked (see `select_posts`):
- "news":   the newest post with the word "News" in its title. If that one is
            patron-only, the newest public news post comes second, so the game
            can stack it behind the first.
- "latest": the posts since the newest news post (none if a news post is the
            newest of all): the newest public one in front, the newest
            patron-only one behind it.

Thumbnails follow the website (mts-game.com, PatreonPosts.php):
1. the post's cover as patreon.com shows it. The official API v2 has no field for
   it, so it comes from the undocumented endpoint patreon.com's own pages use;
   patron-only posts take Patreon's own blurred cover, never the sharp one.
2. the first image in the post text (or its embed). For patron-only posts it is
   destroyed beyond recognition before it is written.
3. none: the game shows its own placeholder.
Every image is cropped to 16:9 and scaled down here, so players download a few
dozen kilobytes instead of the original upload.

Usage (GitHub Actions, see .github/workflows/publish-news.yml):
    python tools/publish_news.py            publish to origin/devstatus
    python tools/publish_news.py --dry-run  build into ./news_preview, push nothing
"""

import hashlib
import html.parser
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageFilter

TARGET_BRANCH = "devstatus"
NEWS_DIR = "news"
CAMPAIGN_ID = os.getenv("PATREON_CAMPAIGN_ID", "10492412")
API_URL = "https://www.patreon.com/api/oauth2/v2/campaigns/{}/posts"
COVER_URL = "https://www.patreon.com/api/posts"
MAX_PAGES = 4
COVER_COUNT = 60

THUMB_SIZE = (480, 270)
THUMB_QUALITY = 80
BLUR_WIDTH = 24
BLUR_PASSES = 10
# tracking pixels and spacer GIFs
MIN_SIDE = 16

NEWS_TITLE = re.compile(r"\bnews\b", re.IGNORECASE)


# ---------------------------------------------------------------- Patreon --

USER_AGENT = "Mozilla/5.0 (compatible; Mind the School news board)"


def _http_get(url, headers=None):
    # Patreon's image CDN answers urllib's default "Python-urllib/x.y" with 403
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def _https(url):
    return url if isinstance(url, str) and url.startswith("https://") else None


def _absolute_post_url(url):
    if url.startswith("/") and not url.startswith("//"):
        url = "https://www.patreon.com" + url
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme == "https" and parsed.hostname in ("www.patreon.com", "patreon.com"):
        return url
    return None


class _FirstImage(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.src = None

    def handle_starttag(self, tag, attrs):
        if self.src is None and tag == "img":
            src = dict(attrs).get("src") or ""
            if re.match(r"^https?://", src, re.IGNORECASE):
                self.src = src


def first_image_url(content, embed_data):
    """The first image of the post text, else the embed's image (PatreonPostMapper::firstImageUrl)."""
    if content and content.strip():
        parser = _FirstImage()
        parser.feed(content)
        if parser.src:
            return parser.src

    embed_data = embed_data if isinstance(embed_data, dict) else {}
    image = embed_data.get("image") if isinstance(embed_data.get("image"), dict) else {}
    candidate = image.get("url") or embed_data.get("url")
    if isinstance(candidate, str) and re.match(r"^https?://\S+\.(jpe?g|png|gif|webp)(\?\S*)?$", candidate, re.IGNORECASE):
        return candidate
    return None


def map_post(item):
    """One API v2 post resource -> the fields the title screen needs, or None for odd URLs."""
    attributes = item.get("attributes") or {}
    url = _absolute_post_url(str(attributes.get("url") or ""))
    if url is None:
        return None
    return {
        "id": str(item.get("id") or ""),
        "title": str(attributes.get("title") or "").strip() or "Untitled post",
        "url": url,
        "publishedAt": str(attributes.get("published_at") or ""),
        "isPublic": attributes.get("is_public") is True,
        "textImage": first_image_url(str(attributes.get("content") or ""), attributes.get("embed_data")),
    }


def fetch_posts(token, get=_http_get):
    """All posts of the campaign (up to MAX_PAGES pages), newest first."""
    url = API_URL.format(urllib.parse.quote(CAMPAIGN_ID)) + "?" + urllib.parse.urlencode({
        "fields[post]": "title,content,url,published_at,is_public,embed_data,embed_url",
        "page[count]": 50,
    })
    headers = {"Authorization": "Bearer " + token, "User-Agent": "Mind the School news board"}
    posts = []
    for _ in range(MAX_PAGES):
        body = json.loads(get(url, headers))
        for item in body.get("data") or []:
            post = map_post(item) if isinstance(item, dict) else None
            if post is not None:
                posts.append(post)
        next_url = (body.get("links") or {}).get("next")
        if not (isinstance(next_url, str) and next_url.startswith("https://www.patreon.com/")):
            break
        url = next_url
    posts.sort(key=lambda post: post["publishedAt"], reverse=True)
    return posts


def fetch_covers(get=_http_get):
    """{post id: {"sharp": url, "blurred": url}} from patreon.com's own endpoint; {} if it fails or changed."""
    url = COVER_URL + "?" + urllib.parse.urlencode({
        "filter[campaign_id]": CAMPAIGN_ID,
        "filter[contains_exclusive_posts]": "true",
        "sort": "-published_at",
        "page[count]": COVER_COUNT,
        "fields[post]": "image,thumbnail",
        "json-api-version": "1.0",
    })
    try:
        body = json.loads(get(url, {"User-Agent": USER_AGENT}))
    except Exception as error:  # undocumented endpoint: any failure just means "no covers"
        print(f"Cover endpoint failed, posts fall back to their text images: {error}")
        return {}

    covers = {}
    for item in body.get("data") or []:
        attributes = item.get("attributes") or {}
        image = attributes.get("image") if isinstance(attributes.get("image"), dict) else {}
        thumbnail = attributes.get("thumbnail") if isinstance(attributes.get("thumbnail"), dict) else {}
        covers[str(item.get("id") or "")] = {
            "sharp": _https(image.get("large_url") or image.get("url")),
            "blurred": _https(thumbnail.get("default_blurred")),
        }
    return covers


# -------------------------------------------------------------- selection --

def is_news(post):
    return NEWS_TITLE.search(post["title"]) is not None


def select_posts(posts):
    """{"news": [front, behind?], "latest": [front, behind?]} from posts sorted newest first.

    news:   the newest news post; a patron-only one gets the newest public news behind it.
    latest: the posts since the newest news post: the newest public one in front, the
            newest patron-only one behind it; either alone if the other is missing.
    """
    news = [post for post in posts if is_news(post)]
    news_stack = []
    if news:
        news_stack.append(news[0])
        if not news[0]["isPublic"]:
            public = next((post for post in news if post["isPublic"]), None)
            if public is not None:
                news_stack.append(public)

    since_news = []
    for post in posts:
        if is_news(post):
            break
        since_news.append(post)
    # public in front where possible: everyone can open it, the patron-only one waits behind
    public = next((post for post in since_news if post["isPublic"]), None)
    private = next((post for post in since_news if not post["isPublic"]), None)
    latest_stack = [post for post in (public, private) if post is not None]

    return {"news": news_stack, "latest": latest_stack}


def image_sources(post, covers):
    """[(url, needs_blur)] in the order they are tried: cover first, then the text image."""
    cover = covers.get(post["id"]) or {}
    sources = []
    if post["isPublic"]:
        if cover.get("sharp"):
            sources.append((cover["sharp"], False))
    elif cover.get("blurred"):
        # Patreon's blurred cover: the sharp one is never downloaded
        sources.append((cover["blurred"], False))
    if post["textImage"]:
        sources.append((post["textImage"], not post["isPublic"]))
    return sources


# ----------------------------------------------------------------- images --

def make_thumbnail(data, blur):
    """WebP bytes of a 16:9 thumbnail, or None if the data is no usable image."""
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except Exception:
        return None
    if image.width < MIN_SIDE or image.height < MIN_SIDE:
        return None
    image = image.convert("RGB")

    # center crop to 16:9, so every polaroid has the same frame
    target = THUMB_SIZE[0] / THUMB_SIZE[1]
    if image.width / image.height > target:
        width = round(image.height * target)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / target)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))

    if blur:
        # shrink, scale back up and blur: no detail of a patron-only picture survives
        tiny = image.resize((BLUR_WIDTH, round(BLUR_WIDTH / target)), Image.LANCZOS)
        image = tiny.resize(THUMB_SIZE, Image.BILINEAR)
        for _ in range(BLUR_PASSES):
            image = image.filter(ImageFilter.GaussianBlur(2))
    else:
        image = image.resize(THUMB_SIZE, Image.LANCZOS)

    out = io.BytesIO()
    image.save(out, "WEBP", quality=THUMB_QUALITY, method=6)
    return out.getvalue()


def thumbnail_for(post, covers, get=_http_get):
    """WebP bytes from the first source that yields an image, else None."""
    for url, blur in image_sources(post, covers):
        try:
            data = get(url)
        except Exception as error:
            print(f"Image for post {post['id']} failed ({url[:60]}...): {error}")
            continue
        thumbnail = make_thumbnail(data, blur)
        if thumbnail is not None:
            return thumbnail
    return None


def build_news(posts, covers, get=_http_get):
    """(news.json document, {file name: bytes}) for the selected posts."""
    selection = select_posts(posts)
    files = {}

    def entry(post):
        thumbnail = thumbnail_for(post, covers, get)
        image = None
        if thumbnail is not None:
            # named by content, so the game never sees a stale cached copy under an old name
            image = f"{post['id']}-{hashlib.sha1(thumbnail).hexdigest()[:8]}.webp"
            files[image] = thumbnail
        return {
            "id": post["id"],
            "title": post["title"],
            "url": post["url"],
            "publishedAt": post["publishedAt"],
            "isPublic": post["isPublic"],
            "image": image,
        }

    document = {
        "schemaVersion": 1,
        "news": [entry(post) for post in selection["news"]],
        "latest": [entry(post) for post in selection["latest"]],
    }
    return document, files


# ---------------------------------------------------------------- publish --

def _git(repo, *args, input_bytes=None, check=True):
    result = subprocess.run(["git", "-C", str(repo), *args], input=input_bytes, capture_output=True, check=check)
    return result.returncode, result.stdout.decode("utf-8", "replace").strip()


def _blob(repo, data):
    return _git(repo, "hash-object", "-w", "--stdin", input_bytes=data)[1]


def _mktree(repo, entries):
    return _git(repo, "mktree", input_bytes=("\n".join(entries) + "\n").encode("utf-8"))[1]


def publish(document, files, repo=".", attempts=3):
    """Replace the news/ folder on the devstatus branch. Returns "published" or "unchanged"."""
    news_json = (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    entries = [f"100644 blob {_blob(repo, news_json)}\tnews.json"]
    entries += [f"100644 blob {_blob(repo, data)}\t{name}" for name, data in sorted(files.items())]
    news_tree = _mktree(repo, entries)

    for _ in range(attempts):
        code, _out = _git(repo, "fetch", "-q", "origin", TARGET_BRANCH, check=False)
        parent = _git(repo, "rev-parse", "FETCH_HEAD")[1] if code == 0 else None

        root = []
        if parent:
            code, current = _git(repo, "rev-parse", f"{parent}:{NEWS_DIR}", check=False)
            if code == 0 and current == news_tree:
                return "unchanged"
            listing = _git(repo, "ls-tree", parent)[1]
            # other publishers' files (devstatus.json, discord.json, …) stay untouched
            root = [line for line in listing.splitlines() if line and line.split("\t", 1)[1] != NEWS_DIR]
        root.append(f"040000 tree {news_tree}\t{NEWS_DIR}")
        tree = _mktree(repo, root)

        parent_args = ["-p", parent] if parent else []
        commit = _git(repo, "commit-tree", tree, *parent_args, "-m", "Publish Patreon news for the title screen")[1]
        # plain push: if another run published in between, it is rejected and we try again
        code, _out = _git(repo, "push", "-q", "origin", f"{commit}:refs/heads/{TARGET_BRANCH}", check=False)
        if code == 0:
            return "published"
    raise RuntimeError(f"could not push to {TARGET_BRANCH} after {attempts} attempts")


def main(argv):
    token = os.getenv("PATREON_TOKEN")
    if not token:
        print("PATREON_TOKEN is not set.")
        return 1

    posts = fetch_posts(token)
    document, files = build_news(posts, fetch_covers())

    if "--dry-run" in argv:
        preview = pathlib.Path("news_preview")
        preview.mkdir(exist_ok=True)
        (preview / "news.json").write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        for name, data in files.items():
            (preview / name).write_bytes(data)
        print(f"Wrote {len(files)} image(s) and news.json to {preview}/")
        return 0

    print(publish(document, files))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

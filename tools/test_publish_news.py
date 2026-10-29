import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from PIL import Image

import publish_news as news


def post(post_id, title, published, public=True, text_image=None):
    return {"id": post_id, "title": title, "url": f"https://www.patreon.com/posts/{post_id}",
            "publishedAt": published, "isPublic": public, "textImage": text_image}


def png(width, height, color=(200, 40, 40)):
    out = io.BytesIO()
    Image.new("RGB", (width, height), color).save(out, "PNG")
    return out.getvalue()


class SelectPostsTest(unittest.TestCase):
    def test_public_news_on_top_stands_alone(self):
        posts = [post("3", "Public News 01.12", "2025-12-03"), post("2", "Devlog", "2025-12-02")]
        self.assertEqual([p["id"] for p in news.select_posts(posts)["news"]], ["3"])
        self.assertIsNone(news.select_posts(posts)["latest"])

    def test_private_news_gets_the_newest_public_news_behind_it(self):
        posts = [post("4", "Private News", "2025-12-04", public=False),
                 post("3", "Private News", "2025-12-03", public=False),
                 post("2", "Public News", "2025-12-02"),
                 post("1", "Public News", "2025-12-01")]
        self.assertEqual([p["id"] for p in news.select_posts(posts)["news"]], ["4", "2"])

    def test_private_news_without_any_public_news_stands_alone(self):
        posts = [post("4", "Private News", "2025-12-04", public=False)]
        self.assertEqual([p["id"] for p in news.select_posts(posts)["news"]], ["4"])

    def test_newest_post_that_is_no_news_becomes_latest(self):
        posts = [post("5", "Sneak peek", "2025-12-05", public=False), post("4", "Public News", "2025-12-04")]
        selection = news.select_posts(posts)
        self.assertEqual(selection["latest"]["id"], "5")
        self.assertEqual([p["id"] for p in selection["news"]], ["4"])

    def test_news_must_be_a_word_of_its_own(self):
        self.assertTrue(news.is_news(post("1", "Public NEWS 01.12", "")))
        self.assertTrue(news.is_news(post("1", "News: v0.2.2", "")))
        self.assertFalse(news.is_news(post("1", "Newsletter archive", "")))

    def test_no_posts(self):
        self.assertEqual(news.select_posts([]), {"news": [], "latest": None})


class ImageSourcesTest(unittest.TestCase):
    covers = {"1": {"sharp": "https://c/sharp.jpg", "blurred": "https://c/blur.jpg"}}

    def test_public_post_tries_sharp_cover_then_text_image(self):
        sources = news.image_sources(post("1", "x", "", text_image="https://t/a.jpg"), self.covers)
        self.assertEqual(sources, [("https://c/sharp.jpg", False), ("https://t/a.jpg", False)])

    def test_private_post_never_uses_the_sharp_cover_and_blurs_its_text_image(self):
        sources = news.image_sources(post("1", "x", "", public=False, text_image="https://t/a.jpg"), self.covers)
        self.assertEqual(sources, [("https://c/blur.jpg", False), ("https://t/a.jpg", True)])

    def test_fallback_chain_ends_without_an_image(self):
        def failing(url, headers=None):
            raise OSError("offline")
        target = post("1", "x", "", text_image="https://t/a.jpg")
        self.assertIsNone(news.thumbnail_for(target, self.covers, failing))
        self.assertIsNone(news.thumbnail_for(post("9", "x", ""), {}, failing))

    def test_broken_cover_falls_through_to_the_text_image(self):
        def get(url, headers=None):
            return b"not an image" if "sharp" in url else png(800, 600)
        thumbnail = news.thumbnail_for(post("1", "x", "", text_image="https://t/a.jpg"), self.covers, get)
        self.assertIsNotNone(thumbnail)


class FirstImageTest(unittest.TestCase):
    def test_first_http_image_in_the_text(self):
        html = '<p>hi</p><img src="data:x"><img src="https://a/1.png"><img src="https://a/2.png">'
        self.assertEqual(news.first_image_url(html, None), "https://a/1.png")

    def test_embed_image_when_the_text_has_none(self):
        self.assertEqual(news.first_image_url("<p>no image</p>", {"image": {"url": "https://e/i.jpg"}}), "https://e/i.jpg")
        self.assertIsNone(news.first_image_url("", {"url": "https://youtube.com/watch?v=1"}))


class ThumbnailTest(unittest.TestCase):
    def open(self, data):
        return Image.open(io.BytesIO(data))

    def test_any_shape_becomes_a_16_9_webp(self):
        for size in ((1920, 1080), (1000, 1000), (600, 1200)):
            image = self.open(news.make_thumbnail(png(*size), blur=False))
            self.assertEqual(image.format, "WEBP")
            self.assertEqual(image.size, news.THUMB_SIZE)

    def test_tracking_pixels_and_garbage_are_rejected(self):
        self.assertIsNone(news.make_thumbnail(png(1, 1), blur=False))
        self.assertIsNone(news.make_thumbnail(b"<html>", blur=False))

    def test_blur_destroys_detail(self):
        # a sharp black/white checkerboard must come out as a flat grey
        board = Image.new("RGB", (640, 360), "white")
        for x in range(0, 640, 8):
            for y in range(0, 360, 8):
                if (x + y) // 8 % 2:
                    board.paste((0, 0, 0), (x, y, x + 8, y + 8))
        out = io.BytesIO()
        board.save(out, "PNG")
        blurred = self.open(news.make_thumbnail(out.getvalue(), blur=True)).convert("L")
        low, high = blurred.getextrema()
        self.assertLess(high - low, 40)


class PublishTest(unittest.TestCase):
    def git(self, repo, *args):
        return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True, text=True).stdout.strip()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.tmp.name)
        self.remote, self.repo = root / "remote.git", root / "work"
        subprocess.run(["git", "init", "-q", "--bare", str(self.remote)], check=True)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.git(self.repo, "config", "user.name", "test")
        self.git(self.repo, "config", "user.email", "test@example.com")
        self.git(self.repo, "remote", "add", "origin", str(self.remote))
        (self.repo / "devstatus.json").write_text("{}\n")
        self.git(self.repo, "add", "devstatus.json")
        self.git(self.repo, "commit", "-q", "-m", "init")
        self.git(self.repo, "push", "-q", "origin", "HEAD:refs/heads/devstatus")

    def tearDown(self):
        self.tmp.cleanup()

    def test_publishes_next_to_other_files_and_skips_unchanged(self):
        document = {"schemaVersion": 1, "news": [], "latest": None}
        self.assertEqual(news.publish(document, {"1-abc.webp": b"img"}, self.repo), "published")
        files = self.git(self.remote, "ls-tree", "-r", "--name-only", "devstatus").splitlines()
        self.assertEqual(sorted(files), ["devstatus.json", "news/1-abc.webp", "news/news.json"])
        self.assertEqual(news.publish(document, {"1-abc.webp": b"img"}, self.repo), "unchanged")

    def test_old_images_disappear_with_the_next_publish(self):
        document = {"schemaVersion": 1, "news": [], "latest": None}
        news.publish(document, {"1-abc.webp": b"img"}, self.repo)
        news.publish(document, {"2-def.webp": b"img2"}, self.repo)
        files = self.git(self.remote, "ls-tree", "-r", "--name-only", "devstatus").splitlines()
        self.assertNotIn("news/1-abc.webp", files)
        shown = json.loads(self.git(self.remote, "show", "devstatus:news/news.json"))
        self.assertEqual(shown["schemaVersion"], 1)


if __name__ == "__main__":
    unittest.main()

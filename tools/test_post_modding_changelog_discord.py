"""Tests for post_modding_changelog_discord.py. Run: python -m unittest tools/test_post_modding_changelog_discord.py"""

import copy
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from post_modding_changelog_discord import (  # noqa: E402
    TYPE_STYLE, build_message, pending_entries, post_pending,
)
from test_validate_modding_changelog import VALID  # noqa: E402


class FakeWebhook:
    """Records posted payloads; fails on the post number given in `fail_on`."""

    def __init__(self, fail_on=None):
        self.posted = []
        self.fail_on = fail_on

    def post(self, payload):
        if self.fail_on is not None and len(self.posted) + 1 == self.fail_on:
            raise RuntimeError("Discord refused to post the message (HTTP 500)")
        self.posted.append(payload)
        return str(len(self.posted))

    def titles(self):
        return [payload["embeds"][0]["title"] for payload in self.posted]


class BuildMessageTest(unittest.TestCase):
    def test_embed_carries_type_version_and_wiki(self):
        message = build_message(VALID["entries"][1])
        embed = message["embeds"][0]
        self.assertEqual(embed["author"]["name"], "⚠️ Breaking change · 0.2.2")
        self.assertEqual(embed["color"], TYPE_STYLE["breaking"][1])
        self.assertEqual(embed["url"], "https://github.com/SuIT-pub/Mind-the-School/wiki/Events#event-flags")
        self.assertIn("[Events](https://github.com/SuIT-pub/Mind-the-School/wiki/Events#event-flags)", embed["description"])
        self.assertEqual(embed["timestamp"], "2026-10-06T00:00:00Z")

    def test_no_wiki_no_link(self):
        embed = build_message(VALID["entries"][2])["embeds"][0]
        self.assertNotIn("url", embed)
        self.assertNotIn("Wiki", embed["description"])

    def test_nobody_gets_pinged(self):
        entry = dict(VALID["entries"][0], details="@everyone look")
        self.assertEqual(build_message(entry)["allowed_mentions"], {"parse": []})

    def test_multi_word_wiki_page_reads_with_spaces(self):
        entry = dict(VALID["entries"][0], wiki="Building-Situations#situation-flags")
        self.assertIn("[Building Situations](", build_message(entry)["embeds"][0]["description"])

    def test_every_type_has_a_style(self):
        from validate_modding_changelog import TYPES
        self.assertEqual(set(TYPES), set(TYPE_STYLE))


class PostPendingTest(unittest.TestCase):
    def test_first_run_posts_everything_oldest_first(self):
        hook = FakeWebhook()
        state, new_ids = post_pending(VALID, {}, hook)
        self.assertEqual(new_ids, ["map-registry", "event-flags", "event-title"])
        self.assertEqual(hook.titles(), ["Map registry", "Event flags", "Events can carry their own title"])
        self.assertEqual(state["postedIds"], new_ids)

    def test_only_new_entries_are_posted(self):
        doc = copy.deepcopy(VALID)
        hook = FakeWebhook()
        state, new_ids = post_pending(doc, {"postedIds": ["map-registry", "event-flags"]}, hook)
        self.assertEqual(new_ids, ["event-title"])
        self.assertEqual(state["postedIds"], ["map-registry", "event-flags", "event-title"])

    def test_nothing_new_posts_nothing(self):
        hook = FakeWebhook()
        state, new_ids = post_pending(VALID, {"postedIds": [e["id"] for e in VALID["entries"]]}, hook)
        self.assertEqual((hook.posted, new_ids), ([], []))

    def test_edited_entry_is_not_reposted(self):
        doc = copy.deepcopy(VALID)
        doc["entries"][0]["details"] = "Corrected text."
        hook = FakeWebhook()
        post_pending(doc, {"postedIds": [e["id"] for e in doc["entries"]]}, hook)
        self.assertEqual(hook.posted, [])

    def test_failure_midway_keeps_what_was_posted(self):
        hook = FakeWebhook(fail_on=2)
        with self.assertRaises(RuntimeError) as caught:
            post_pending(VALID, {"postedIds": []}, hook)
        self.assertEqual(caught.exception.posted_now, ["map-registry"])
        self.assertEqual(caught.exception.state, {"postedIds": ["map-registry"]})

    def test_pending_ignores_ids_no_longer_in_the_file(self):
        self.assertEqual([e["id"] for e in pending_entries(VALID, ["removed-entry"])],
                         ["map-registry", "event-flags", "event-title"])


if __name__ == "__main__":
    unittest.main()

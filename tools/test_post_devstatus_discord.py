"""Tests for post_devstatus_discord.py. Run: python -m unittest tools/test_post_devstatus_discord.py"""

import copy
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from post_devstatus_discord import (  # noqa: E402
    FIELD_LIMIT, Webhook, build_embed, build_note, describe_changes, embed_size, load_state, pack_fields,
    save_state, sync,
)
from publish_devstatus import publish  # noqa: E402
from test_validate_devstatus import VALID  # noqa: E402


def doc(updated_at="2026-10-12T18:00:00Z"):
    d = copy.deepcopy(VALID)
    d["updatedAt"] = updated_at
    return d


class FakeWebhook:
    """Records calls; `gone` holds ids that Discord would answer with 404."""

    def __init__(self, gone=()):
        self.calls = []
        self.gone = set(gone)
        self.next_id = 100

    def post(self, payload):
        self.next_id += 1
        self.calls.append(("post", str(self.next_id), payload))
        return str(self.next_id)

    def edit(self, message_id, payload):
        self.calls.append(("edit", message_id, payload))
        return message_id not in self.gone

    def delete(self, message_id):
        self.calls.append(("delete", message_id, None))

    def kinds(self):
        return [(kind, message_id) for kind, message_id, _ in self.calls]


class SyncTest(unittest.TestCase):
    def test_first_run_posts_roadmap_then_note(self):
        hook = FakeWebhook()

        state = sync(doc(), {}, hook)

        self.assertEqual(hook.kinds(), [("post", "101"), ("post", "102")])
        self.assertIn("embeds", hook.calls[0][2])
        self.assertIn("The dev status board is up", hook.calls[1][2]["content"])
        self.assertEqual(state["embedMessageId"], "101")
        self.assertEqual(state["noteMessageId"], "102")
        self.assertEqual(state["posted"]["updatedAt"], "2026-10-12T18:00:00Z")

    def test_update_edits_roadmap_and_replaces_note(self):
        hook = FakeWebhook()
        old = {"embedMessageId": "1", "noteMessageId": "2", "posted": doc("2026-10-11T18:00:00Z")}

        state = sync(doc(), old, hook)

        # The new note goes up before the old one comes down, so there is always one.
        self.assertEqual(hook.kinds(), [("edit", "1"), ("post", "101"), ("delete", "2")])
        self.assertEqual(state["embedMessageId"], "1")
        self.assertEqual(state["noteMessageId"], "101")

    def test_roadmap_deleted_in_discord_is_posted_again(self):
        hook = FakeWebhook(gone={"1"})
        old = {"embedMessageId": "1", "noteMessageId": "2", "posted": doc("2026-10-11T18:00:00Z")}

        state = sync(doc(), old, hook)

        self.assertEqual(hook.kinds(), [("edit", "1"), ("post", "101"), ("post", "102"), ("delete", "2")])
        self.assertEqual(state["embedMessageId"], "101")

    def test_already_posted_state_is_skipped(self):
        hook = FakeWebhook()
        old = {"embedMessageId": "1", "noteMessageId": "2", "posted": doc()}

        self.assertIsNone(sync(doc(), old, hook))
        self.assertEqual(hook.calls, [])

    def test_older_branch_does_not_roll_discord_back(self):
        hook = FakeWebhook()
        old = {"embedMessageId": "1", "noteMessageId": "2", "posted": doc("2026-10-13T18:00:00Z")}

        self.assertIsNone(sync(doc("2026-10-01T18:00:00Z"), old, hook))
        self.assertEqual(hook.calls, [])

    def test_no_message_can_ping_anyone(self):
        hook = FakeWebhook()
        sync(doc(), {}, hook)

        for _, _, payload in hook.calls:
            self.assertEqual(payload["allowed_mentions"], {"parse": []})


class DescribeChangesTest(unittest.TestCase):
    def test_finished_item(self):
        old, new = doc(), doc()
        new["done"].insert(0, {**new["now"].pop(0), "doneIn": "0.2.2", "doneAt": "2026-10-14"})
        new["done"][0].pop("progress")

        self.assertIn("✅ Finished: Lab building", describe_changes(old, new))

    def test_started_item(self):
        old, new = doc(), doc()
        new["now"].append(new["next"].pop(0))

        self.assertEqual(describe_changes(old, new), ["🔨 Started: Beach camp"])

    def test_new_item_on_the_roadmap(self):
        old, new = doc(), doc()
        new["later"].append({"id": "pool-party", "title": "Pool party", "summary": "Splash."})

        self.assertEqual(describe_changes(old, new), ["🆕 On the roadmap: Pool party"])

    def test_versions(self):
        old, new = doc(), doc()
        new["currentVersion"], new["targetVersion"] = "0.3.0", "0.3.1"

        self.assertEqual(describe_changes(old, new),
                         ["📦 Version 0.3.0 is out.", "🎯 Now working toward version 0.3.1."])

    def test_wording_change_falls_back_to_generic_line(self):
        old, new = doc(), doc()
        new["now"][0]["summary"] = "A real lab, now with shelves."

        self.assertEqual(describe_changes(old, new), ["📝 Roadmap details updated."])

    def test_note_uses_discord_relative_timestamp(self):
        note = build_note(doc("2026-10-12T18:00:00Z"), None)

        self.assertIn("<t:1791828000:R>", note)


class EmbedTest(unittest.TestCase):
    def test_sections_and_progress(self):
        embed = build_embed(doc())

        names = [field["name"] for field in embed["fields"]]
        self.assertEqual(names, ["🔨 Working on now", "⏭️ Up next", "🗓️ Later", "✅ Recently finished"])
        self.assertIn("`▰▰▰▰▱▱▱▱▱▱` 40%", embed["fields"][0]["value"])
        self.assertIn("Working toward version 0.3.0", embed["description"])
        self.assertEqual(embed["timestamp"], "2026-10-12T18:00:00Z")

    def test_empty_section_is_left_out(self):
        d = doc()
        d["later"] = []

        names = [field["name"] for field in build_embed(d)["fields"]]
        self.assertNotIn("🗓️ Later", names)

    def test_markdown_in_titles_stays_literal(self):
        d = doc()
        d["now"][0]["title"] = "Lab *building*"

        self.assertIn(r"Lab \*building\*", build_embed(d)["fields"][0]["value"])

    def test_long_list_splits_into_continuation_fields(self):
        texts = ["x" * 300 for _ in range(8)]

        fields = pack_fields("🗓️ Later", texts)

        self.assertGreater(len(fields), 1)
        self.assertEqual(fields[0]["name"], "🗓️ Later")
        self.assertTrue(all(len(field["value"]) <= FIELD_LIMIT for field in fields))
        self.assertEqual(sum(field["value"].count("x" * 300) for field in fields), 8)

    def test_too_long_roadmap_drops_finished_items_first(self):
        d = doc()
        d["later"] = [{"id": f"item-{i}", "title": "t" * 60, "summary": "s" * 160} for i in range(23)]
        d["done"] = [{"id": f"done-{i}", "title": "d" * 60, "summary": "s" * 160,
                      "doneIn": "0.2.2", "doneAt": "2026-10-01"} for i in range(3)]

        embed = build_embed(d)

        shown_done = sum(field["value"].count("d" * 60) for field in embed["fields"])
        self.assertLess(shown_done, 3)
        self.assertEqual(sum(field["value"].count("t" * 60) for field in embed["fields"]), 23)
        self.assertLessEqual(embed_size(embed), 6000)

    def test_roadmap_that_cannot_fit_is_refused(self):
        d = doc()
        d["later"] = [{"id": f"item-{i}", "title": "t" * 60, "summary": "s" * 160} for i in range(40)]

        with self.assertRaises(ValueError):
            build_embed(d)

    def test_repo_file_fits(self):
        path = pathlib.Path(__file__).resolve().parent.parent / "devstatus.json"
        build_embed(json.loads(path.read_text(encoding="utf-8")))


class WebhookTest(unittest.TestCase):
    URL = "https://discord.com/api/webhooks/1/secret-token"

    def hook(self, *responses):
        self.requests = []
        replies = list(responses)

        def send(method, url, payload):
            self.requests.append((method, url, payload))
            return replies.pop(0)

        return Webhook(self.URL, send=send, sleep=lambda seconds: self.requests.append(("sleep", seconds, None)))

    def test_post_waits_for_message_id(self):
        hook = self.hook((200, {"id": "42"}))

        self.assertEqual(hook.post({"content": "hi"}), "42")
        self.assertEqual(self.requests[0][:2], ("POST", self.URL + "?wait=true"))

    def test_edit_of_missing_message_reports_false(self):
        self.assertFalse(self.hook((404, {"message": "Unknown Message"})).edit("7", {}))

    def test_delete_of_missing_message_is_fine(self):
        self.hook((404, None)).delete("7")

    def test_rate_limit_is_waited_out(self):
        hook = self.hook((429, {"retry_after": 0.5}), (200, {"id": "42"}))

        self.assertEqual(hook.post({}), "42")
        self.assertIn(("sleep", 0.5, None), self.requests)

    def test_error_does_not_leak_the_url(self):
        with self.assertRaises(RuntimeError) as caught:
            self.hook((401, {"message": "Invalid Webhook Token"})).post({})

        self.assertNotIn("secret-token", str(caught.exception))
        self.assertIn("401", str(caught.exception))


class StateTest(unittest.TestCase):
    """Saves and loads discord.json against a real local bare remote."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.tmp.name)
        self.remote = root / "remote.git"
        subprocess.run(["git", "init", "-q", "--bare", str(self.remote)], check=True)
        self.work = root / "work"
        subprocess.run(["git", "clone", "-q", str(self.remote), str(self.work)], check=True, capture_output=True)
        for key, value in (("user.email", "ci@test"), ("user.name", "ci")):
            subprocess.run(["git", "-C", str(self.work), "config", key, value], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def files_on_branch(self):
        return subprocess.run(
            ["git", "-C", str(self.remote), "ls-tree", "--name-only", "devstatus"],
            capture_output=True, text=True, check=True,
        ).stdout.split()

    def publish(self, document):
        path = self.work / "devstatus.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        publish(path, self.work, "feature/x")

    def test_nothing_saved_yet(self):
        self.assertEqual(load_state(self.work)[0], {})

    def test_round_trip_keeps_devstatus_json(self):
        self.publish(doc())
        _, parent = load_state(self.work)

        save_state(self.work, {"embedMessageId": "1", "noteMessageId": "2", "posted": doc()}, parent)

        state, _ = load_state(self.work)
        self.assertEqual(state["noteMessageId"], "2")
        self.assertEqual(sorted(self.files_on_branch()), ["devstatus.json", "discord.json"])

    def test_next_publish_keeps_discord_json(self):
        self.publish(doc("2026-10-11T18:00:00Z"))
        _, parent = load_state(self.work)
        save_state(self.work, {"embedMessageId": "1", "noteMessageId": "2", "posted": doc()}, parent)

        self.publish(doc("2026-10-12T18:00:00Z"))

        self.assertEqual(sorted(self.files_on_branch()), ["devstatus.json", "discord.json"])
        self.assertEqual(load_state(self.work)[0]["embedMessageId"], "1")


if __name__ == "__main__":
    unittest.main()

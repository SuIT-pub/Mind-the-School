##############################################################################
# The title screen's news board: Patreon posts as polaroids top right and an
# occasional note from the developer taped to the brass plaque.
#
# The posts come from news/news.json on the `devstatus` branch, which the
# "Publish Patreon news" action (tools/publish_news.py) keeps current; the
# game never talks to Patreon. The note is game/message.txt on master.
# Both are only fetched with the "Online content" setting on; with it off
# the board stays empty instead of showing something stale.
##############################################################################

init -10 python:
    import hashlib
    import json
    from datetime import datetime

    NEWS_BASE_URL = "https://raw.githubusercontent.com/SuIT-pub/Mind-the-School/devstatus/news/"
    NEWS_MESSAGE_URL = "https://raw.githubusercontent.com/SuIT-pub/Mind-the-School/master/game/message.txt"

    # polaroid: a 16:9 print, the title and date on the wide bottom border
    NEWS_CARD_SIZE = (300, 232)
    NEWS_CARD_PRINT = (12, 12, 276, 155)

    class NewsBoard(object):
        """
        Everything downloaded for the title screen. Created once at init and only
        ever mutated: a store variable reassigned after init would be written
        into every save, thumbnails included.
        """

        def __init__(self):
            self.clear()

        def clear(self):
            # {"news": [post, …], "latest": [post, …]}; a post carries its thumbnail bytes
            self.stacks = {"news": [], "latest": []}
            self.message = ""
            self.message_hash = None
            # what the screen shows right now. Kept here and not in screen variables:
            # the stacks are used screens, and SetScreenVariable would only reach main_menu.
            self.front = {"news": 0, "latest": 0}
            self.swaps = {"news": 0, "latest": 0}
            self.note_state = "still"

        def swap(self, key: str, index: int):
            self.front[key] = index
            self.swaps[key] += 1

        def pull_note_off(self):
            self.note_state = "falling"

        def note_fallen(self):
            persistent.news_note_dismissed = self.message_hash
            self.note_state = "still"

        def stick_note_back(self):
            persistent.news_note_dismissed = None
            self.note_state = "restuck"

    news_board = NewsBoard()

    def _news_fetch(url: str) -> bytes:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        return response.content

    def _news_download():
        """
        Runs in a background thread: builds the new state completely, then swaps it
        in, so the screen never sees half a board.
        """

        stacks = {"news": [], "latest": []}
        try:
            document = json.loads(_news_fetch(NEWS_BASE_URL + "news.json").decode("utf-8"))
            for key in stacks:
                for post in document.get(key) or []:
                    entry = dict(post)
                    entry["thumbnail"] = None
                    if post.get("image"):
                        try:
                            entry["thumbnail"] = _news_fetch(NEWS_BASE_URL + post["image"])
                        except Exception as e:
                            log(f"News thumbnail {post['image']} failed: {e}", log_type = "warning", category = "news")
                    stacks[key].append(entry)
        except Exception as e:
            log(f"News download failed: {e}", log_type = "warning", category = "news")

        message, message_hash = "", None
        try:
            raw = _news_fetch(NEWS_MESSAGE_URL).decode("utf-8").strip()
            if raw:
                message = refine_downloaded_message(raw)
                # a changed note sticks again even after the player pulled the old one off
                message_hash = hashlib.sha1(raw.encode("utf-8")).hexdigest()
        except Exception as e:
            log(f"Message download failed: {e}", log_type = "warning", category = "news")

        if persistent.load_supporter != 1:
            return  # switched off while the download ran
        news_board.stacks = stacks
        news_board.message = message
        news_board.message_hash = message_hash

    def refresh_news_board():
        """
        Fetches the board in the background when online content is on, clears it otherwise.
        """

        news_board.clear()
        if persistent.load_supporter == 1:
            renpy.invoke_in_thread(_news_download)
        renpy.restart_interaction()

    def news_post_date(post) -> str:
        """
        The publishing time in the player's own time zone, e.g. "Oct 15, 2026, 13:07".
        """

        try:
            moment = datetime.fromisoformat(post["publishedAt"]).astimezone()
        except (KeyError, ValueError, TypeError):
            return ""
        return moment.strftime("%b %d, %Y, %H:%M")

    def news_polaroid(post):
        """
        One post as a polaroid of NEWS_CARD_SIZE (plus a small shadow).
        """

        width, height = NEWS_CARD_SIZE
        px, py, pw, ph = NEWS_CARD_PRINT
        if post.get("thumbnail"):
            photo = Transform(im.Data(post["thumbnail"], post["image"]), fit = "fill", xysize = (pw, ph))
        else:
            # no image anywhere: an unexposed print
            photo = Fixed(
                Solid("#3a342e"),
                Text("no photo", style = "jr_typed_small", color = "#ffffff55", align = (0.5, 0.5)),
                xysize = (pw, ph))

        children = [
            Transform(Solid("#00000040"), pos = (4, 6), xysize = (width, height)),
            Transform(Solid("#faf7f0"), xysize = (width, height)),
            Transform(photo, pos = (px, py)),
        ]
        # the stripe says why a photo may come blurred: Patreon only shows it to members
        stripe = None
        if post.get("freeOnly"):
            stripe = ("FREE MEMBERS", JR_GREEN)
        elif not post.get("isPublic"):
            stripe = ("PATRONS ONLY", JR_ACCENT)
        if stripe:
            children.append(Fixed(
                Solid(stripe[1] + "e0"),
                Text(stripe[0], style = "jr_rubric", size = 11, color = "#faf7f0", align = (0.5, 0.5)),
                xysize = (104, 22), pos = (px + pw - 112, py + 8)))
        border_top = py + ph
        children.append(Text(post.get("title", ""), style = "jr_typed", size = 17, color = JR_TYPED,
            xmaximum = width - 28, xpos = 14, ypos = border_top + 10, layout = "nobreak"))
        children.append(Text(news_post_date(post), style = "jr_typed_small", size = 13, color = JR_PENCIL,
            xpos = 14, ypos = border_top + 36))
        return Fixed(*children, xysize = (width + 4, height + 6))

# A card swings out sideways and settles into its new place; the front one is
# drawn last, so the card coming forward slides over the one going back.
transform news_card_at(x, y, angle):
    anchor (0.5, 0.5) pos (x, y) rotate angle rotate_pad False

transform news_card_swap(x, y, angle, from_x, from_y, from_angle, swing, generation):
    anchor (0.5, 0.5) pos (from_x, from_y) rotate from_angle rotate_pad False
    easeout 0.18 xpos from_x + swing rotate from_angle + swing / 14.0
    # Ren'Py hands a screen transform the state of an identical one at the same
    # spot, and from the second swap on the card going back runs exactly the path
    # the other card ran before: it would count as finished. An invisible alpha
    # step per generation makes every swap a transform of its own (not a position:
    # a float xpos would count as a fraction of the screen).
    easein 0.26 xpos x ypos y rotate angle alpha 1.0 - (generation % 2) * 0.001

transform news_note_stick_on:
    anchor (0.5, 0.0) transform_anchor True rotate -4 rotate_pad False
    alpha 0.0 zoom 1.18
    easein 0.22 alpha 1.0 zoom 1.0

transform news_note_still:
    anchor (0.5, 0.0) transform_anchor True rotate -4 rotate_pad False

transform news_note_fall:
    anchor (0.5, 0.0) transform_anchor True rotate -4 rotate_pad False
    parallel:
        easein 0.55 yoffset 420
    parallel:
        linear 0.55 rotate 26
    parallel:
        pause 0.25
        linear 0.3 alpha 0.0

screen news_polaroid_stack(key, front_pos, back_pos, swing):
    # """
    # The posts of news_board.stacks[key] as stacked polaroids. The front one
    # opens the post; the one peeking out behind swaps places with it.
    # front_pos / back_pos: (x, y, angle) of the card centres.
    # swing: how far (and to which side) a card swings out while swapping.
    # """

    $ posts = news_board.stacks[key]
    # a refreshed board may hold fewer posts than the one the player swapped through
    $ front = min(news_board.front[key], len(posts) - 1)
    $ swaps = news_board.swaps[key]

    $ order = [i for i in range(len(posts)) if i != front] + [front]
    for index in order:
        $ post = posts[index]
        $ is_front = index == front
        $ x, y, angle = front_pos if is_front else back_pos
        $ fx, fy, fangle = back_pos if is_front else front_pos
        button:
            xysize (NEWS_CARD_SIZE[0] + 4, NEWS_CARD_SIZE[1] + 6)
            padding (0, 0, 0, 0)
            background None
            if is_front:
                hover_foreground Solid("#ffffff10")
                tooltip "Open on Patreon"
                action OpenURL(post["url"])
            else:
                tooltip ("Show the public post" if post.get("isPublic") else "Show the patrons' post")
                action Function(news_board.swap, key, index)
            if swaps == 0:
                at news_card_at(x, y, angle)
            else:
                at news_card_swap(x, y, angle, fx, fy, fangle, swing if is_front else -swing, swaps)
            add news_polaroid(post)

screen news_board():
    # """
    # The polaroids top right and the note on the plaque. Used by main_menu.
    # """

    $ note_state = news_board.note_state

    # ---- posts: the newest news on the right, other recent posts left of it
    if news_board.stacks["latest"]:
        use news_polaroid_stack("latest", (1050, 150, 2.5), (1030, 140, -5.0), -150)
    if news_board.stacks["news"]:
        use news_polaroid_stack("news", (1370, 140, -2.0), (1390, 152, 4.5), 150)

    # ---- the developer's note, taped to the plaque
    $ note_up = news_board.message and persistent.news_note_dismissed != news_board.message_hash
    if note_up or note_state == "falling":
        button:
            # the top edge sits on the plaque's leather, so the tape sticks to the plaque
            pos (1440, 872)
            padding (0, 0, 0, 0)
            background None
            tooltip "Pull the note off"
            action Function(news_board.pull_note_off)
            if note_state == "falling":
                at news_note_fall
            elif note_state == "restuck":
                at news_note_stick_on
            else:
                at news_note_still
            fixed:
                fit_first True
                frame:
                    xmaximum 250
                    background Frame("gui/journal/ui/foldout_panel.webp", 12, 12)
                    padding (18, 22, 18, 14)
                    text news_board.message style "jr_typed" size 14 color JR_TYPED
                # a strip of tape over the top edge, half on the note, half on the plaque
                add Transform(Solid("#efe4b8b8"), xysize = (78, 22), rotate = 3, rotate_pad = False) xalign 0.5 yoffset -11
    if note_state == "falling":
        timer 0.6 action Function(news_board.note_fallen)

    # the bare plaque sticks a pulled-off note back on
    if news_board.message and not note_up and note_state != "falling":
        button:
            pos (1290, 838)
            xysize (628, 238)
            padding (0, 0, 0, 0)
            background None
            tooltip "Stick the note back on"
            action Function(news_board.stick_note_back)

default persistent.news_note_dismissed = None

init 1 python:
    # at every start; the setting toggles refresh it with refresh_news_board
    if persistent.load_supporter == 1:
        renpy.invoke_in_thread(_news_download)

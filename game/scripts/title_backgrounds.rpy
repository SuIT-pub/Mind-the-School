##############################################################################
# Title screen backgrounds, found automatically in gui/bg/.
#
# - <name>_<index>.png/.webp/.jpg   images with the same <name> form a set;
#                                   with animation on, a set plays as a
#                                   slideshow in index order (cross-fades)
# - <name>.png/.webp/.jpg           a single image
# - <name>.webm/.mp4/.ogv           a video (webm wins over mp4 of the same name)
#
# Two choices are remembered: the animated one (a set or a video) and the
# still one (any single image). The play/pause ribbon switches between them,
# "next background" steps through the animated ones or through all stills.
# gui.main_menu_background shows whatever is selected, so every screen that
# uses it (title, title journal, help) follows the choice.
##############################################################################

init -5 python:
    import re as _title_re
    import functools as _title_functools

    TITLE_BG_DIR = "gui/bg/"
    TITLE_BG_IMAGE_EXT = (".png", ".webp", ".jpg", ".jpeg")
    TITLE_BG_VIDEO_EXT = (".webm", ".ogv", ".mp4")
    # seconds an image of a set stays at the slowest / fastest slideshow speed
    # (persistent.title_bg_speed 0.0 .. 1.0, the slider on the backgrounds page)
    TITLE_BG_HOLD_SLOW = 15.0
    TITLE_BG_HOLD_FAST = 2.0

    def title_bg_timing():
        """
        (hold, fade) in seconds for the current slideshow speed; the cross-fade
        shrinks with the hold so a fast slideshow doesn't fade most of the time.
        """

        speed = persistent.title_bg_speed if persistent.title_bg_speed is not None else 0.7
        hold = TITLE_BG_HOLD_SLOW + (TITLE_BG_HOLD_FAST - TITLE_BG_HOLD_SLOW) * min(max(speed, 0.0), 1.0)
        return hold, min(1.6, hold * 0.35)

    # Readable names for the sets; anything not listed is named after its file.
    TITLE_BG_LABELS = {
        "main_menu_bg": "Classroom",
        "main_menu_bg_yoga": "Yoga",
        "main_menu_bg_anim": "Classroom",
        "main_menu_bg_yoga_anim": "Yoga",
    }

    class TitleBackground(object):
        """
        One choosable background: kind "set" (frames in order), "image" or
        "video".
        """

        def __init__(self, key, kind, name, frames = None, video = None):
            self.key = key
            self.kind = kind
            self.name = name
            self.frames = frames or []
            self.video = video

        @property
        def label(self):
            if self.name in TITLE_BG_LABELS:
                return TITLE_BG_LABELS[self.name]
            label = self.name
            if label.startswith("main_menu_bg"):
                label = label[len("main_menu_bg"):]
            return label.replace("_", " ").strip().title() or "Background"

        @property
        def animated(self):
            return self.kind == "video" or (self.kind == "set" and len(self.frames) > 1)

    def _title_bg_scan():
        """
        Groups the files in gui/bg/ into sets, single images and videos,
        sorted by name.
        """

        sets = {}
        videos = {}
        for path in renpy.list_files():
            if not path.startswith(TITLE_BG_DIR):
                continue
            filename = path[len(TITLE_BG_DIR):]
            if "/" in filename:
                continue
            stem, dot, ext = filename.rpartition(".")
            ext = "." + ext.lower()
            if ext in TITLE_BG_VIDEO_EXT:
                # prefer webm, then ogv, then mp4 for the same name
                current = videos.get(stem)
                if current is None or TITLE_BG_VIDEO_EXT.index(ext) < TITLE_BG_VIDEO_EXT.index("." + current.rpartition(".")[2].lower()):
                    videos[stem] = path
            elif ext in TITLE_BG_IMAGE_EXT:
                match = _title_re.match(r"^(.*)_(\d+)$", stem)
                name, index = (match.group(1), int(match.group(2))) if match else (stem, None)
                sets.setdefault(name, []).append((index if index is not None else -1, path))

        entries = []
        for name in sorted(sets):
            frames = [path for _, path in sorted(sets[name])]
            kind = "set" if len(frames) > 1 else "image"
            entries.append(TitleBackground("set:" + name if kind == "set" else "image:" + name, kind, name, frames = frames))
        for name in sorted(videos):
            entries.append(TitleBackground("video:" + name, "video", name, video = videos[name]))
        return entries

    title_bg_entries = _title_bg_scan()

    def title_bg_entry(key):
        for entry in title_bg_entries:
            if entry.key == key:
                return entry
        return None

    def title_bg_stills():
        return [path for entry in title_bg_entries if entry.kind != "video" for path in entry.frames]

    def title_bg_animated():
        return [entry for entry in title_bg_entries if entry.animated]

    def _title_bg_defaults():
        """
        First run after the update: keep the old on/off choice, start on the
        first animation and the first still.
        """

        if persistent.title_bg_animate is None:
            old = persistent.main_menu_animation or "anim_1"
            persistent.title_bg_animate = old.startswith("anim")
        if title_bg_entry(persistent.title_bg_anim) is None:
            animated = title_bg_animated()
            persistent.title_bg_anim = animated[0].key if animated else None
        if persistent.title_bg_still not in title_bg_stills():
            stills = title_bg_stills()
            persistent.title_bg_still = stills[0] if stills else None

    @_title_functools.lru_cache(maxsize = 8)
    def _title_bg_movie(path):
        # one Movie per file: a new Movie object would restart the video on every redraw
        return Movie(play = path, size = (1920, 1080))

    def title_background_display(st, at):
        """
        DynamicDisplayable function for gui.main_menu_background.
        """

        _title_bg_defaults()
        if persistent.title_bg_animate:
            entry = title_bg_entry(persistent.title_bg_anim)
            if entry is not None and entry.kind == "video":
                return _title_bg_movie(entry.video), None
            if entry is not None and entry.kind == "set" and len(entry.frames) > 1:
                hold, fade_time = title_bg_timing()
                step = hold + fade_time
                count = len(entry.frames)
                index = int(st // step) % count
                into = st % step
                current = entry.frames[index]
                if into < hold:
                    # redraw at the latest when the fade starts (or soon, if the speed slider moves)
                    return Transform(current, xysize = (1920, 1080)), min(hold - into, 0.5)
                fade = (into - hold) / fade_time
                following = entry.frames[(index + 1) % count]
                return Fixed(Transform(current, xysize = (1920, 1080)),
                    Transform(following, xysize = (1920, 1080), alpha = fade), xysize = (1920, 1080)), 1.0 / 30
            if entry is not None and entry.frames:
                return Transform(entry.frames[0], xysize = (1920, 1080)), None
        if persistent.title_bg_still:
            return Transform(persistent.title_bg_still, xysize = (1920, 1080)), None
        return Solid("#1e1610"), None

    def toggle_animation():
        _title_bg_defaults()
        persistent.title_bg_animate = not persistent.title_bg_animate
        renpy.restart_interaction()

    def switch_background():
        """
        Next background: the next animation while animating, the next still
        image otherwise.
        """

        _title_bg_defaults()
        if persistent.title_bg_animate:
            animated = [entry.key for entry in title_bg_animated()]
            if animated:
                position = animated.index(persistent.title_bg_anim) if persistent.title_bg_anim in animated else -1
                persistent.title_bg_anim = animated[(position + 1) % len(animated)]
        else:
            stills = title_bg_stills()
            if stills:
                position = stills.index(persistent.title_bg_still) if persistent.title_bg_still in stills else -1
                persistent.title_bg_still = stills[(position + 1) % len(stills)]
        renpy.restart_interaction()

    def title_bg_play(key):
        # picker: play a set or video as the animated background
        persistent.title_bg_anim = key
        persistent.title_bg_animate = True
        renpy.restart_interaction()

    def title_bg_pick_still(path):
        # picker: show one image, animation off
        persistent.title_bg_still = path
        persistent.title_bg_animate = False
        renpy.restart_interaction()

default persistent.title_bg_animate = None
default persistent.title_bg_anim = None
default persistent.title_bg_still = None
default persistent.title_bg_speed = 0.7

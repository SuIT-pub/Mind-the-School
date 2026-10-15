##############################################################################
# Journal: Characters (page 9)
#
# Top ribbons pick the group (Class 3A, Staff, Parents), the left page is the
# group's photo roster, the right page the dossier of the selected person.
#
# display = "<group>" or "<group>:<person>" or "<group>:<person>:<portrait index>"
# (portrait index -1 = the person's roster photo)
##############################################################################

init python:
    import re
    import functools

    # roster crop of the 1080x1920 character renders (x, y, w, h as fractions):
    # head down to below the chest, deep enough for the shortest girls too
    JOURNAL_HEADSHOT_CROP = (0.06, 0.0, 0.88, 0.6)
    JOURNAL_HEADSHOT_ASPECT = (0.88 * 1080) / (0.6 * 1920)
    # short intro lines (role, relationships) go under the name, longer ones are the appearance text
    JOURNAL_NOTE_MAX_LENGTH = 60

    def journal_person_groups() -> List[str]:
        return [key for key in person_storage.keys() if key != "NoView" and person_storage[key]]

    def journal_split_fact(line: str) -> Tuple[str, str]:
        """
        "Height: 172.5 cm" -> ("Height", "172.5 cm"); "Bra Size 75F (DDD)" ->
        ("Bra Size", "75F (DDD)"): without a colon the value starts at the
        first word that contains a digit.
        """

        if ":" in line:
            label, value = line.split(":", 1)
            return (label.strip(), value.strip())
        match = re.match(r"^(.*?)\s+(\S*\d.*)$", line)
        if match:
            return (match.group(1).strip(), match.group(2).strip())
        return (line, "")

    def journal_parse_description(lines: List[str]):
        """
        Splits a person's description into the parts the dossier lays out
        differently.

        ### Returns:
        1. facts: List[Tuple[str, str]]
            - "• label: value" lines, wherever they appear (measurements too)
        2. notes: List[str]
            - short lines before the first heading (role, relationships)
        3. sections: List[Tuple[str, List[str]]]
            - heading and paragraphs; the long intro text becomes "Appearance"
        """

        facts = []
        notes = []
        appearance = []
        sections = []
        current = None
        for raw in lines:
            line = str(raw).strip()
            if line == "":
                continue
            heading = re.fullmatch(r"\{b\}(.+?)\{/b\}", line)
            if heading:
                current = (heading.group(1), [])
                sections.append(current)
            elif line.startswith("•"):
                facts.append(journal_split_fact(line.lstrip("•").strip()))
            elif current is not None:
                current[1].append(line)
            elif len(line) <= JOURNAL_NOTE_MAX_LENGTH:
                notes.append(line)
            else:
                appearance.append(line)

        if appearance:
            sections.insert(0, ("Appearance", appearance))
        # a heading whose lines were all facts (Measurements) has nothing left to show
        return facts, notes, [section for section in sections if section[1]]

    def journal_parse_character_display(display: str):
        """
        Resolves the journal display string to (group, person key, portrait
        index), falling back to the first group / first person so the
        dossier is never empty.
        """

        groups = journal_person_groups()
        parts = (display or "").split(":")
        group = parts[0] if parts[0] in groups else (groups[0] if groups else "")
        people = list(person_storage[group].keys()) if group else []
        person = parts[1] if len(parts) > 1 and parts[1] in people else (people[0] if people else "")
        portrait = -1
        if len(parts) > 2:
            try:
                portrait = int(parts[2])
            except ValueError:
                portrait = -1
        return group, person, portrait

    def journal_cropped_photo(path: str, box: Tuple[float, float, float, float], width: int, height: int):
        """
        Cuts box (x, y, w, h as fractions of the image) out of a render and
        scales it exactly onto width x height. The crop is converted to pixels
        so the result always fills its frame, whatever size the render has.
        """

        if journal_is_placeholder_image(path):
            return journal_cover(path, width, height)
        return _journal_cropped_file(path, tuple(box), int(width), int(height))

    # cached like journal_cover (see journal_overview.rpy): the roster shows 15 of these
    @functools.lru_cache(maxsize = 256)
    def _journal_cropped_file(path: str, box, width: int, height: int):
        image_w, image_h = journal_image_size(path)
        crop = (int(box[0] * image_w), int(box[1] * image_h), int(box[2] * image_w), int(box[3] * image_h))
        return Transform(path, crop = crop, fit = "fill", xysize = (width, height))

    def journal_headshot(path: str, width: int, height: int):
        return journal_cropped_photo(path, JOURNAL_HEADSHOT_CROP, width, height)

    def journal_portrait_photo(path: str, width: int, height: int):
        """
        Upper three quarters of a render (head to hips) for the dossier
        polaroid; width/height should keep the 3:4 aspect.
        """

        return journal_cropped_photo(path, (0.0, 0.0, 1.0, 0.75), width, height)

style jr_tile_label:
    background None
    hover_background Frame("gui/journal/ui/underline.webp", 10, 26, 10, 6)
    selected_background Frame("gui/journal/ui/highlight.webp", 12, 0, 12, 0)
    selected_hover_background Frame("gui/journal/ui/highlight.webp", 12, 0, 12, 0)
    xfill True
    padding (4, 0, 4, 2)

style jr_tile_label_text is jr_text:
    size 20
    xalign 0.5
    hover_color "#000"

screen journal_character(display):
    # """
    # Characters page: photo roster of one group on the left, dossier of the
    # selected person on the right.
    # """

    tag interaction_overlay
    modal True

    default zoomed_portrait = None

    $ group, person_key, portrait_index = journal_parse_character_display(display)
    $ sub_entries = [(get_translation(key), (key == group), [With(dissolveM), Call("open_journal", 9, key)])
        for key in journal_person_groups()]

    use journal_backdrop

    use journal_page_selector(9, display, sub_entries = sub_entries)

    if zoomed_portrait is None:
        key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

    if group:
        use journal_character_roster(group, person_key)
    if person_key:
        use journal_character_dossier(group, person_storage[group][person_key], portrait_index)

    use journal_tooltip

    if zoomed_portrait is not None:
        # the full render, upright; any click or ESC puts it back
        button:
            xysize (1920, 1080)
            background Solid("#0b0806e0")
            action SetScreenVariable("zoomed_portrait", None)
            add Transform(zoomed_portrait, fit = "contain", ysize = 1040) align (0.5, 0.5)
        key "K_ESCAPE" action SetScreenVariable("zoomed_portrait", None)

screen journal_character_roster(group, person_key):
    # """
    # Left page: the group as rows of school prints, the first name printed
    # on the white strip under each photo.
    #
    # Height budget for a class of 15 (4 rows): header 92 + 4 x 171 + 3 x 12 = 812
    # of the 832px page, so the column only scrolls for larger groups.
    # """

    $ people = list(person_storage[group].values())
    $ columns = 4
    $ spacing = 20
    $ border = 4
    $ caption_h = 26
    $ tile_w = (JR_LEFT_W - spacing * (columns - 1)) // columns
    $ photo_w = tile_w - border * 2
    # photo keeps the aspect of the crop, so nothing is stretched
    $ photo_h = int(photo_w / JOURNAL_HEADSHOT_ASPECT)
    $ tile_h = border + photo_h + caption_h

    use jr_page("journal_character_roster", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W

            # title and head count share one line to leave the page to the photos
            fixed:
                xysize (JR_LEFT_W, 66)
                text get_translation(group) style "jr_title" yalign 1.0
                text ("1 person on file" if len(people) == 1 else "{} people on file".format(len(people))):
                    style "jr_typed_small"
                    xalign 1.0
                    yalign 1.0
                    yoffset -8
            null height 4
            use jr_double_rule(JR_LEFT_W)
            null height 16

            $ rows = (len(people) + columns - 1) // columns
            grid columns rows:
                xspacing spacing
                yspacing 12
                for person in people:
                    $ selected = person.name == person_key
                    button:
                        xysize (tile_w, tile_h)
                        background None
                        padding (0, 0, 0, 0)
                        selected selected
                        action [With(dissolveM), Call("open_journal", 9, "{}:{}".format(group, person.name))]
                        fixed:
                            add Solid("#00000028") pos (2, 3) xysize (tile_w, tile_h)
                            add Solid("#faf7f0") xysize (tile_w, tile_h)
                            add journal_cover("gui/journal/ui/photo_backdrop.webp", photo_w, photo_h) pos (border, border)
                            add journal_headshot(person.get_thumbnail(), photo_w, photo_h) pos (border, border)
                            frame:
                                style "jr_tile_label"
                                xysize (tile_w - 12, caption_h - 2)
                                pos (6, border + photo_h)
                                text person.get_first_name() style "jr_tile_label_text" yalign 0.5
                # keep the grid full; a short last row would break it
                for _ in range(-len(people) % columns):
                    null

screen journal_character_dossier(group, person, portrait_index):
    # """
    # Right page: photo with its portrait switcher, key facts, then the
    # description sections the player has unlocked so far.
    # """

    $ portraits = person.get_portraits()
    $ portrait_keys = list(portraits.keys())
    $ thumbnail = person.get_thumbnail()
    python:
        if portrait_index < 0 or portrait_index >= len(portrait_keys):
            # -1 (and anything stale) opens on the photo that is pinned to the roster
            portrait_index = next((i for i, key in enumerate(portrait_keys) if portraits[key] == thumbnail), 0)
        portrait_key = portrait_keys[portrait_index] if portrait_keys else ""
        portrait_path = portraits[portrait_key] if portrait_key else thumbnail
        facts, notes, sections = journal_parse_description(person.get_description())
        role = [note for note in notes if len(note) <= 20]
        remarks = [note for note in notes if len(note) > 20]
        person_display = "{}:{}".format(group, person.name)

    # 192x256 photo (3:4) inside the polaroid's 12px border and 58px caption strip
    $ photo_w = 216
    $ photo_h = 326
    $ facts_w = JR_RIGHT_W - photo_w - 28

    use jr_page("journal_character_dossier", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            text person.get_full_name() style "jr_title"
            null height 4
            use jr_double_rule(JR_RIGHT_W)
            null height 10
            text " · ".join([get_translation(group)] + role) style "jr_typed_small"

            null height 22
            hbox:
                spacing 28

                vbox:
                    spacing 10
                    button:
                        # fixed size: the tilted polaroid's bounding box is ~11px wider and
                        # would push the facts column past the page edge
                        xysize (photo_w, photo_h)
                        padding (0, 0, 0, 0)
                        background None
                        action SetScreenVariable("zoomed_portrait", portrait_path)
                        tooltip "Enlarge"
                        use journal_polaroid(journal_portrait_photo(portrait_path, photo_w - 24, photo_h - 70), photo_w, photo_h, -2, "gui/journal/ui/photo_backdrop.webp")

                    if len(portrait_keys) > 1:
                        fixed:
                            xysize (photo_w, 30)
                            if portrait_index > 0:
                                textbutton "‹":
                                    style "jr_entry_button"
                                    text_style "jr_value"
                                    yalign 0.5
                                    action [With(dissolveM), Call("open_journal", 9, "{}:{}".format(person_display, portrait_index - 1))]
                            text (portrait_key[:1].upper() + portrait_key[1:]) style "jr_typed" size 18 xalign 0.5 yalign 0.5
                            if portrait_index < len(portrait_keys) - 1:
                                textbutton "›":
                                    style "jr_entry_button"
                                    text_style "jr_value"
                                    xalign 1.0
                                    yalign 0.5
                                    action [With(dissolveM), Call("open_journal", 9, "{}:{}".format(person_display, portrait_index + 1))]

                vbox:
                    xsize facts_w
                    if facts:
                        use jr_rubric("On file", facts_w)
                        null height 4
                        for label, value in facts:
                            fixed:
                                xysize (facts_w, 32)
                                use jr_leader(journal_text_width(label, size = 22),
                                    facts_w - journal_text_width(value, style = "jr_value", size = 22))
                                text label style "jr_text" size 22 yalign 0.5
                                text value style "jr_value" size 22 xalign 1.0 yalign 0.5

                    if remarks:
                        null height 16
                        for remark in remarks:
                            text remark style "jr_typed" size 18

                    # the two most recently found keywords are pencilled in, pointing at
                    # the photo; older ones are listed underneath
                    $ found_keywords = person.get_keywords()
                    if found_keywords:
                        null height 14
                        for index, keyword in enumerate(found_keywords[-2:]):
                            $ note, note_w, note_h = journal_pencil_note(keyword, ("left" if index == 0 else "down_left"), ("red" if keyword == found_keywords[-1] and len(found_keywords) > 2 else "pencil"), 22, journal_note_seed(person.name, keyword))
                            # long keywords shrink to fit the column instead of running off the page
                            $ note_zoom = min(1.0, (facts_w - index * 18) / float(max(1, note_w)))
                            add Transform(note, zoom = note_zoom) xoffset (index * 18)
                            null height 2
                        if len(found_keywords) > 2:
                            null height 6
                            text "Also noted: " + ", ".join(found_keywords[:-2]) style "jr_small" size 18

                    if portrait_path != thumbnail and not journal_is_placeholder_image(portrait_path):
                        null height 16
                        textbutton "Use this photo in the roster":
                            style "jr_entry_button"
                            text_style "jr_small"
                            action Function(person.set_thumbnail, portrait_path)

            for title, paragraphs in sections:
                null height 24
                use jr_rubric(title, JR_RIGHT_W)
                null height 6
                for paragraph in paragraphs:
                    text paragraph style "jr_body"

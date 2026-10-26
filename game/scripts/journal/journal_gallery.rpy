##############################################################################
# Journal: Replay Gallery (page 7)
#
# Left page: locations (or replay categories), the open one unfolded into
# its scenes. Right page: the category's scenes as photos, or one scene with
# its variant choices and the replay button. Composite scenes get two top
# ribbons: Variants (values of the main event) and Fragments (which fragment
# plays in which slot, each with its own variants).
#
# display = "<category>.<event>.<mode>.<slot>.<fragment>"
#   mode: value_mode (default) | fragment_mode | fragment_selection_mode
#   slot/fragment: only in fragment_selection_mode; a registered fragment
#   in the last part is stored as the slot's choice.
# The replay returns to the same display (journal_display kwarg), so the
# format must stay as it is.
##############################################################################

init python:
    JOURNAL_GALLERY_HIDDEN_KEYS = ("FragStorage", "fragment")

    def journal_gallery_mode() -> str:
        mode = get_setting("show_gallery_category")
        if mode is None:
            mode = "Locations"
            set_setting("show_gallery_category", mode)
        return mode

    def journal_gallery_has_event(event_name: str) -> bool:
        event_obj = get_event_from_register(event_name)
        return (event_obj is not None
            and renpy.has_label(event_obj.get_event_label())
            and event_name in persistent.gallery.get(event_obj.get_location(), {}))

    def journal_gallery_categories(mode: str) -> Dict[str, Any]:
        """
        category key -> its event collection (dict keys or list of names).
        """

        if persistent.gallery is None:
            return {}
        if mode == "Categories":
            return {cat: events for cat, events in event_replay_categories.items()
                if any(journal_gallery_has_event(e) for e in events)}
        return {key: events for key, events in persistent.gallery.items() if key not in JOURNAL_GALLERY_HIDDEN_KEYS}

    def journal_gallery_category_title(category: str, mode: str) -> str:
        if mode == "Locations":
            return get_location_title(category)
        return get_translation(category)

    def journal_gallery_events(category_events) -> List[Event]:
        """
        Replayable events of one category, sorted by title.
        """

        events = [get_event_from_register(name) for name in category_events if journal_gallery_has_event(name)]
        events = [event_obj for event_obj in events if not is_replay_hidden_by_kinks(event_obj)]
        return sorted(events, key = lambda event_obj: event_obj.get_title())

    def journal_gallery_thumbnail(event_obj) -> str:
        return find_loadable_image(event_obj.get_thumbnail()) or ""

    def journal_gallery_ensure_frag_order(location: str, event: str):
        """
        Every fragment slot of a composite event gets a chosen fragment
        (the first one stored for that slot until the player picks another).
        """

        options = persistent.gallery[location][event]['options']
        if 'frag_order' not in options:
            options['frag_order'] = []
        for i, frag_storage_name in enumerate(options['Frag_Storage']):
            if i >= len(options['frag_order']):
                options['frag_order'].append(list(persistent.gallery["FragStorage"][frag_storage_name]['values'].keys())[0])

        # with turned-off content hidden, a slot holding a blocked fragment
        # moves on to the first seen fragment that is allowed
        if persistent.gallery_hide_blocked_kinks:
            for i, slot_fragments in enumerate(journal_gallery_slot_fragments(location, event)):
                if i < len(options['frag_order']) and journal_gallery_fragment_blocked(options['frag_order'][i]):
                    allowed = [name for name in slot_fragments if not journal_gallery_fragment_blocked(name)]
                    if allowed:
                        options['frag_order'][i] = allowed[0]
        return options['frag_order']

    def journal_gallery_prepare_values(base_gallery, display_location: str, display_event: str):
        """
        Brings the global gallery_chooser in line with one event's value tree
        and returns what the variant chooser has to show.

        Keeps the old journal behaviour exactly: the chooser resets when the
        event changes, restores the last session's choice, falls back to the
        first value wherever a choice no longer exists on the current tree
        path, and blocks the replay when gallery_exclude leaves a variable
        without any value.

        ### Returns:
        1. rows: List[Tuple[str, str, List[Tuple[Any, str]]]]
            - variable, title, (value, value title) for every variable with
                more than one choice
        2. disable_play: bool
        """

        global gallery_chooser, gallery_chooser_order, old_event

        if display_event != old_event:
            gallery_chooser = {"values": {}}
            gallery_chooser_order = []
            old_event = display_event

        options = base_gallery['options']
        if 'last_data' in options and 'last_order' in options:
            gallery_chooser["values"] = options['last_data']
            gallery_chooser_order = options['last_order']

        rows = []
        disable_play = False
        tree = base_gallery['values']
        for variant_name in base_gallery['order']:
            values = list(tree.keys())
            if not values:
                break
            if variant_name not in gallery_chooser_order:
                gallery_chooser_order.append(variant_name)
                gallery_chooser["values"][variant_name] = values[0]
            if gallery_chooser["values"][variant_name] not in values:
                gallery_chooser["values"][variant_name] = values[0]
            tree = tree[gallery_chooser["values"][variant_name]]

            if len(values) > 1:
                allowed = [value for value in values if variant_name + '.' + str(value) not in gallery_exclude]
                if not allowed:
                    if gallery_chooser["values"][variant_name] not in allowed:
                        gallery_chooser["values"][variant_name] = None
                        update_gallery_chooser(gallery_chooser_order, gallery_chooser, base_gallery['values'])
                    disable_play = True
                else:
                    # values (and their fallback titles) can be numbers; text needs strings
                    rows.append((variant_name,
                        str(get_gallery_topic_title(display_location, display_event, variant_name)),
                        [(value, str(get_gallery_value_title(variant_name, display_location, display_event, value))) for value in sorted(allowed)]))

        # remember the choice between sessions
        if not disable_play:
            options['last_data'] = gallery_chooser["values"]
            options['last_order'] = gallery_chooser_order
        return rows, disable_play

    def journal_gallery_choose(variant_name, value, base_values):
        gallery_chooser["values"][variant_name] = value
        update_gallery_chooser(gallery_chooser_order, gallery_chooser, base_values)

    def journal_gallery_slot_fragments(location: str, event: str) -> List[List[str]]:
        """
        Per fragment slot of a composite, the names of the fragments seen in it.
        """

        options = persistent.gallery.get(location, {}).get(event, {}).get('options', {})
        output = []
        for frag_storage_name in options.get('Frag_Storage', []):
            output.append(list(persistent.gallery["FragStorage"].get(frag_storage_name, {}).get('values', {}).keys()))
        return output

    def journal_gallery_fragment_blocked(fragment_name: str) -> bool:
        fragment = get_event_from_register(fragment_name)
        return fragment is not None and bool(get_blocked_kinks(fragment.get_kinks()))

    def is_replay_hidden_by_kinks(event_obj) -> bool:
        """
        With the gallery switch on "hidden": a scene disappears when one of its
        own kinks is turned off, or, for a composite, when a fragment slot has
        no seen fragment left without a turned-off kink. A composite that can
        still be played in some combination stays listed.
        """

        if not persistent.gallery_hide_blocked_kinks:
            return False
        if get_blocked_kinks(Event.get_kinks(event_obj)):
            return True
        if event_obj.get_form() != "composite":
            return False
        for slot_fragments in journal_gallery_slot_fragments(event_obj.get_location(), event_obj.get_event()):
            if slot_fragments and all(journal_gallery_fragment_blocked(name) for name in slot_fragments):
                return True
        return False

    def journal_gallery_fragment_candidates(location: str, event: str, slot: int) -> List[Event]:
        options = persistent.gallery[location][event]['options']
        frag_storage = options['Frag_Storage'][slot]
        base_event_data = options.get('last_data', {})
        candidates = []
        for name in persistent.gallery["FragStorage"][frag_storage]['values'].keys():
            event_obj = get_event_from_register(name)
            if event_obj is not None and event_obj.is_available(in_journal_gallery = True, **base_event_data) and not is_replay_hidden_by_kinks(event_obj):
                candidates.append(event_obj)
        return sorted(candidates, key = lambda event_obj: event_obj.get_title())

screen journal_gallery(display):
    # """
    # Replay gallery page.
    # """

    tag interaction_overlay
    modal True

    python:
        parts = display.split('.') if '.' in display else [display]
        category = parts[0]
        event = parts[1] if len(parts) > 1 else ""
        display_mode = parts[2] if len(parts) > 2 and parts[2] else "value_mode"
        slot = int(parts[3]) if len(parts) > 3 and is_integer(parts[3]) else 0
        slot_fragment = parts[4] if len(parts) > 4 else ""

        mode = journal_gallery_mode()
        categories = journal_gallery_categories(mode)
        if category not in categories:
            category = ""
            event = ""
        elif event and not journal_gallery_has_event(event):
            event = ""

        event_obj = get_event_from_register(event) if event else None
        location = event_obj.get_location() if event_obj is not None else ""
        is_composite = event_obj is not None and event_obj.get_form() == "composite"
        if not is_composite and display_mode != "value_mode":
            display_mode = "value_mode"

        frag_order = []
        if is_composite:
            frag_order = journal_gallery_ensure_frag_order(location, event)
            if slot >= len(frag_order):
                slot = 0
            # a fragment picked for a slot comes in through the display string
            if display_mode == "fragment_selection_mode" and get_event_from_register(slot_fragment) is not None:
                frag_order[slot] = slot_fragment

        base_display = "{}.{}".format(category, event)
        sub_entries = None
        if is_composite:
            sub_entries = [
                ("Variants", (display_mode == "value_mode"), [With(dissolveM), Call("open_journal", 7, base_display + ".value_mode")]),
                ("Fragments", (display_mode != "value_mode"), [With(dissolveM), Call("open_journal", 7, base_display + ".fragment_mode")]),
            ]

    use journal_backdrop

    key "K_ESCAPE" action journal_close_action()

    use journal_page_selector(7, display, sub_entries = sub_entries)

    use journal_gallery_index(mode, categories, category, event)

    if event_obj is not None:
        use journal_gallery_scene(event_obj, category, location, display, display_mode, slot, frag_order)
    elif category:
        use journal_gallery_category(mode, category, categories[category])
    else:
        use jr_page("journal_gallery_detail", JR_RIGHT_X, JR_RIGHT_W):
            vbox:
                xsize JR_RIGHT_W
                text "Replays" style "jr_title"
                null height 4
                use jr_double_rule(JR_RIGHT_W)
                null height 22
                if categories:
                    text "Every scene I have seen once can be played again from here, with the variants I have come across. Pick a {} on the left.".format("location" if mode == "Locations" else "category") style "jr_body"
                else:
                    text "Nothing to replay yet. Scenes show up here once I have seen them." style "jr_body"

    use journal_tooltip

screen journal_gallery_index(mode, categories, category, event):
    # """
    # Left page: categories, the open one unfolded into its scenes.
    # """

    $ titled = sorted([(journal_gallery_category_title(key, mode), key) for key in categories.keys()])
    $ total = sum(len(journal_gallery_events(categories[key])) for key in categories.keys())

    use jr_page("journal_gallery_index", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W

            fixed:
                xysize (JR_LEFT_W, 66)
                text "Replay Gallery" style "jr_title" yalign 1.0
                text ("1 scene" if total == 1 else "{} scenes".format(total)):
                    style "jr_typed_small"
                    xalign 1.0
                    yalign 1.0
                    yoffset -8
            null height 4
            use jr_double_rule(JR_LEFT_W)
            null height 10

            hbox:
                spacing 6
                text "Sorted by" style "jr_small" yalign 0.5
                for option in ("Locations", "Categories"):
                    textbutton option:
                        style "jr_entry_button"
                        text_style "jr_small"
                        text_color JR_PRINT
                        selected (mode == option)
                        yalign 0.5
                        action [With(dissolveM), Call("journal_gallery_switch_category", option, 7, "")]

            # scenes with a kink the player turned off: listed with a note, or hidden
            if get_known_kinks():
                hbox:
                    spacing 6
                    text "Turned-off content" style "jr_small" yalign 0.5
                    for option_label, option_value in (("marked", False), ("hidden", True)):
                        textbutton option_label:
                            style "jr_entry_button"
                            text_style "jr_small"
                            text_color JR_PRINT
                            yalign 0.5
                            action [With(dissolveM), SetField(persistent, "gallery_hide_blocked_kinks", option_value)]

            null height 18
            use jr_rubric(mode, JR_LEFT_W)
            null height 4
            if not titled:
                text "Nothing seen yet." style "jr_small"

            for category_title, key in titled:
                $ events = journal_gallery_events(categories[key])
                $ is_open = key == category
                fixed:
                    xysize (JR_LEFT_W, 40)
                    button:
                        style "jr_entry_button"
                        yalign 0.5
                        selected (is_open and event == "")
                        action [With(dissolveM), Call("open_journal", 7, key)]
                        text category_title style "jr_entry_button_text" size 24 font (JR_FONT_SEMIBOLD if is_open else JR_FONT)
                    text ("1 scene" if len(events) == 1 else "{} scenes".format(len(events))):
                        style "jr_text"
                        size 20
                        font "fonts/CrimsonPro-Italic.ttf"
                        color JR_PENCIL
                        xalign 1.0
                        yalign 0.5

                if is_open:
                    for event_obj in events:
                        button:
                            style "jr_entry_button"
                            xoffset 28
                            selected (event_obj.get_event() == event)
                            action [With(dissolveM), Call("open_journal", 7, "{}.{}".format(key, event_obj.get_event()))]
                            text event_obj.get_title() style "jr_entry_button_text" size 22
                    if debug_mode:
                        textbutton "Reset this {}".format("location" if mode == "Locations" else "category"):
                            style "jr_entry_button"
                            text_style "jr_small"
                            text_color JR_ACCENT
                            xoffset 28
                            action [With(dissolveM), Call('reset_event_gallery', key, "")]
                    null height 8

screen journal_gallery_category(mode, category, category_events):
    # """
    # Right page without a scene picked: the category's scenes as small
    # photos to pick from.
    # """

    $ events = journal_gallery_events(category_events)
    $ columns = 2
    $ cell_w = (JR_RIGHT_W - 24) // columns
    $ photo_w = cell_w
    $ photo_h = int((photo_w - 16) * 9 / 16) + 16

    use jr_page("journal_gallery_detail", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            text journal_gallery_category_title(category, mode) style "jr_title"
            null height 4
            use jr_double_rule(JR_RIGHT_W)
            null height 22

            $ rows = (len(events) + columns - 1) // columns
            if events:
                grid columns rows:
                    xspacing 24
                    yspacing 18
                    for event_obj in events:
                        $ thumb = journal_gallery_thumbnail(event_obj)
                        button:
                            xsize cell_w
                            background None
                            padding (0, 0, 0, 0)
                            action [With(dissolveM), Call("open_journal", 7, "{}.{}".format(category, event_obj.get_event()))]
                            vbox:
                                spacing 6
                                fixed:
                                    xysize (photo_w, photo_h)
                                    add Solid("#00000026") pos (2, 3) xysize (photo_w, photo_h)
                                    add Solid("#faf7f0") xysize (photo_w, photo_h)
                                    if thumb:
                                        add journal_cover(thumb, photo_w - 16, photo_h - 16) pos (8, 8)
                                frame:
                                    style "jr_tile_label"
                                    text event_obj.get_title() style "jr_tile_label_text" size 19 textalign 0.5
                    for _ in range(-len(events) % columns):
                        null

screen journal_gallery_scene(event_obj, category, location, display, display_mode, slot, frag_order):
    # """
    # Right page: one scene. Variants for the main event (or for the
    # fragment picked for a slot), the fragment sequence of composites and
    # the replay button.
    # """

    python:
        event = event_obj.get_event()
        base_display = "{}.{}".format(category, event)
        is_composite = event_obj.get_form() == "composite"
        thumb = journal_gallery_thumbnail(event_obj)

        candidates = []
        slot_fragment = ""
        rows = []
        disable_play = False
        value_base = {}
        if display_mode == "fragment_selection_mode":
            # picking a slot: the chooser works on the picked fragment's own values
            slot_fragment = frag_order[slot]
            candidates = journal_gallery_fragment_candidates(location, event, slot)
            if slot_fragment in persistent.gallery.get('fragment', {}):
                fragment_gallery = persistent.gallery['fragment'][slot_fragment]
                rows, disable_play = journal_gallery_prepare_values(fragment_gallery, "fragment", slot_fragment)
                value_base = fragment_gallery['values']
        else:
            # the main event's values drive the replay, also on the Fragments tab
            base_gallery = persistent.gallery[location][event]
            rows, disable_play = journal_gallery_prepare_values(base_gallery, location, event)
            value_base = base_gallery['values']

        # kinks turned off since the scene was seen: no replay, and the note
        # names them (the replay itself would also refuse to start)
        blocked_kinks = get_blocked_kinks(get_replay_kinks(event_obj, frag_order if is_composite else None))

        subtitle = "Composite scene" if is_composite else "Scene"
        if display_mode == "fragment_selection_mode":
            subtitle = "Slot {} of {}".format(slot + 1, len(frag_order))
        photo_w = 340
        photo_h = int((photo_w - 24) * 9 / 16) + 82

    use jr_page("journal_gallery_detail", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            text get_event_title(event) style "jr_title"
            null height 4
            use jr_double_rule(JR_RIGHT_W)
            null height 6
            fixed:
                xysize (JR_RIGHT_W, 30)
                text subtitle style "jr_typed_small" yalign 0.5
                if debug_mode and display_mode != "fragment_selection_mode":
                    textbutton "Reset scene data":
                        style "jr_entry_button"
                        text_style "jr_small"
                        text_color JR_ACCENT
                        xalign 1.0
                        yalign 0.5
                        action [With(dissolveM), Call('reset_event_gallery', location, event)]

            if display_mode != "fragment_selection_mode":
                null height 14
                fixed:
                    # fixed size: the tilted polaroid's bounding box is wider than its frame
                    xysize (photo_w, photo_h)
                    xalign 0.5
                    if thumb:
                        use journal_polaroid(thumb, photo_w, photo_h, -1)
                    else:
                        use journal_polaroid(Solid("#2a2420"), photo_w, photo_h, -1)

            if display_mode == "fragment_mode":
                null height 20
                use jr_rubric("Sequence", JR_RIGHT_W)
                null height 4
                for i, fragment_name in enumerate(frag_order):
                    hbox:
                        spacing 10
                        text "{}.".format(i + 1) style "jr_value" size 22 color JR_ACCENT min_width 28 yalign 0.5
                        button:
                            style "jr_entry_button"
                            yalign 0.5
                            tooltip "Choose another fragment for this slot"
                            action [With(dissolveM), Call("open_journal", 7, ".".join([category, event, "fragment_selection_mode", str(i), fragment_name]))]
                            text get_event_title(fragment_name, 'fragment') + "  ›" style "jr_entry_button_text" size 22

            elif display_mode == "fragment_selection_mode":
                null height 20
                use jr_rubric("Plays in this slot", JR_RIGHT_W)
                null height 4
                if candidates:
                    for candidate in candidates:
                        $ candidate_name = candidate.get_event()
                        button:
                            style "jr_entry_button"
                            selected (candidate_name == slot_fragment)
                            action [With(dissolveM), Call("open_journal", 7, ".".join([category, event, "fragment_selection_mode", str(slot), candidate_name]))]
                            hbox:
                                spacing 12
                                add ("gui/journal/ui/box_full.webp" if candidate_name == slot_fragment else "gui/journal/ui/box_empty.webp") yalign 0.5
                                text candidate.get_title() style "jr_entry_button_text" size 22
                else:
                    text "No other fragment fits the variants chosen for the scene." style "jr_small"

            if rows and display_mode != "fragment_mode":
                null height 20
                use jr_rubric("Variants of this fragment" if display_mode == "fragment_selection_mode" else "Variants", JR_RIGHT_W)
                for variant_name, variant_title, values in rows:
                    null height 8
                    text variant_title style "jr_text" size 21 font JR_FONT_SEMIBOLD
                    hbox:
                        box_wrap True
                        spacing 6
                        xsize JR_RIGHT_W
                        for value, value_title in values:
                            textbutton value_title:
                                style "jr_entry_button"
                                text_style "jr_entry_button_text"
                                text_size 21
                                selected (gallery_chooser["values"].get(variant_name) == value)
                                action [With(dissolveM), Function(journal_gallery_choose, variant_name, value, value_base)]
            elif display_mode == "value_mode" and is_composite:
                null height 20
                text "This scene has no variants to choose." style "jr_small"

            null height 26
            if display_mode == "fragment_selection_mode":
                textbutton "‹ Back to the sequence":
                    style "jr_entry_button"
                    text_style "jr_value"
                    text_size 22
                    text_color JR_ACCENT
                    action [With(dissolveM), Call("open_journal", 7, base_display + ".fragment_mode")]
            elif disable_play:
                text "Replay not available — a variant is missing." style "jr_small"
            elif blocked_kinks:
                text "Replay not available — it contains content you turned off: {}.".format(get_kink_titles(blocked_kinks)):
                    style "jr_small"
                    color JR_ACCENT
                    substitute False
            elif is_composite:
                textbutton "Replay this scene  ›":
                    style "jr_entry_button"
                    text_style "jr_value"
                    text_size 26
                    text_color JR_ACCENT
                    action [Call('start_gallery_composite_replay', location, event, dict(gallery_chooser), list(frag_order), display)]
            else:
                textbutton "Replay this scene  ›":
                    style "jr_entry_button"
                    text_style "jr_value"
                    text_size 26
                    text_color JR_ACCENT
                    action [Call('start_gallery_replay', location, event, dict(gallery_chooser), display)]

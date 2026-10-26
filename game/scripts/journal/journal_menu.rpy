##############################################################################
# Journal: Game Menu (page 11) — replaces Ren'Py's in-game game menu
#
# Every way into the game menu (ESC, right click, the quick menu buttons,
# ShowMenu("save"/"load"/"preferences"/"history")) ends up in label
# game_menu below, which Ren'Py jumps to inside its menu context:
#
# - on the map or with the journal open, it leaves the menu context and
#   opens this page in the normal journal, with every ribbon usable;
# - anywhere else (mid event) the journal opens inside the menu context;
#   only Game Menu, Cheats and Close work there, and Close returns to the
#   exact spot in the event.
#
# Other game-menu screens (help, about, mod manager) still open as before.
#
# display = "save" | "load" | "settings" | "history"
##############################################################################

init python:
    JOURNAL_MENU_TABS = [("save", "Save"), ("load", "Load"), ("settings", "Settings"), ("history", "History")]
    # Ren'Py's game-menu screen names -> journal sub pages
    # (some engine paths still use the old "save_screen"-style names)
    JOURNAL_MENU_SCREENS = {None: "save", "": "save", "save": "save", "load": "load",
        "preferences": "settings", "history": "history",
        "save_screen": "save", "load_screen": "load", "preferences_screen": "settings",
        "history_screen": "history"}

    def journal_in_game_menu() -> bool:
        """
        True while the journal runs inside Ren'Py's game-menu context (opened
        mid event): only Game Menu, Cheats and Close may be used there.
        """

        return bool(renpy.context()._menu) and not main_menu

    def journal_close_action():
        if journal_title_mode():
            # back to the title screen
            return [UISound("journal_close"), Return()]
        if journal_in_game_menu():
            return [UISound("journal_close"), Jump("journal_menu_leave")]
        return [UISound("journal_close"), With(dissolveM), Jump("map_entry")]

    def journal_parent_on_map() -> bool:
        """
        Called inside the menu context: was the player on the map or in the
        journal when the menu was opened? Both show their screen with the tag
        interaction_overlay in the game's own context.
        """

        try:
            parent = renpy.game.contexts[-2]
        except IndexError:
            return False
        return parent.scene_lists.get_displayable_by_tag("screens", "interaction_overlay") is not None

    def journal_menu_screenshot():
        """
        The moment the game menu was opened: Ren'Py takes this screenshot for the
        save thumbnails anyway (Ren'Py 8.1 has no FileCurrentScreenshot yet).
        """

        data = renpy.game.interface.get_screenshot()
        if not data:
            return Solid("#1e1610")
        return im.Data(data, "journal_menu_backdrop.png")

    def journal_save_page_count() -> int:
        """
        Numbered save pages to list: up to the last one that holds a save, and
        at least up to the page that is open (the arrows can go beyond).
        """

        last = 1
        for name in renpy.list_saved_games(regexp = r"\d+-\d+", fast = True):
            try:
                last = max(last, int(name.split("-")[0]))
            except ValueError:
                pass
        current = persistent._file_page
        if current is not None and str(current).isdigit():
            last = max(last, int(current))
        return last

    def journal_file_time(slot) -> str:
        return FileTime(slot, format = _("{#file_time}%a %d %b %Y, %H:%M"), empty = "")

# Ren'Py jumps here (inside its game-menu context) whenever the game menu opens.
label game_menu:
    if _game_menu_screen not in JOURNAL_MENU_SCREENS and renpy.has_screen(_game_menu_screen):
        # help, about, mod manager, ...: the regular screens
        $ renpy.show_screen(_game_menu_screen, _transient = True)
        $ ui.interact()
        jump _noisy_return

    # anything else unknown opens the journal's save page rather than failing
    $ journal_menu_request = JOURNAL_MENU_SCREENS.get(_game_menu_screen, "save")
    $ play_ui_sound("journal_open")

    if journal_parent_on_map():
        $ renpy.jump_out_of_context("journal_menu_from_map")

    # mid event: the journal opens right here; journal_menu_leave unwinds back
    $ journal_menu_base_depth = renpy.call_stack_depth()
    call open_journal(11, journal_menu_request) from journal_game_menu_1

# Back in the game's own context (the menu context was left from the map).
label journal_menu_from_map:
    # set by Ren'Py when entering the menu and not restored by leaving it this way
    $ suppress_overlay = False
    call open_journal(11, journal_menu_request) from journal_game_menu_2

# Close inside the menu context: drop every journal call made since the menu
# opened, then return from the context's root to where the event was.
label journal_menu_leave:
    while renpy.call_stack_depth() > journal_menu_base_depth:
        $ renpy.pop_call()
    return

default journal_menu_request = "save"
default journal_menu_base_depth = 0

screen journal_menu(display):
    # """
    # Game menu page: save, load, settings, history as top ribbons.
    # """

    tag interaction_overlay
    modal True

    $ tab = display if display in [key for key, _ in JOURNAL_MENU_TABS] else "save"
    $ sub_entries = [(label, (key == tab), Call("open_journal", 11, key)) for key, label in JOURNAL_MENU_TABS]

    use journal_backdrop

    key "K_ESCAPE" action journal_close_action()

    use journal_page_selector(11, display, sub_entries = sub_entries)

    if tab in ("save", "load"):
        use journal_menu_files(tab)
    elif tab == "settings":
        use journal_menu_settings()
    else:
        use journal_menu_history()

    use journal_tooltip

screen journal_menu_leave_links():
    # """
    # Main menu and quit, at the foot of the left page on every tab.
    # """

    null height 34
    use jr_rubric("Leave", JR_LEFT_W)
    null height 10
    hbox:
        spacing 36
        if not journal_title_mode():
            textbutton "Main menu ›":
                style "jr_cheat_link"
                action MainMenu()
        if renpy.variant("pc"):
            textbutton "Quit ›":
                style "jr_cheat_link"
                action Quit(confirm = True)
        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton "Controls ›":
                style "jr_cheat_link"
                action ShowMenu("help")

###############
# region Files

screen journal_menu_files(tab):
    # """
    # Save or load: pages on the left, the slots of the open page on the right.
    # """

    $ saving = tab == "save"
    $ slots = gui.file_slot_cols * gui.file_slot_rows

    use jr_page("journal_menu_pages", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W

            text ("Save game" if saving else "Load game") style "jr_title"
            null height 4
            use jr_double_rule(JR_LEFT_W)
            null height 10
            text ("Pick a slot on the right; a filled one is overwritten after asking." if saving else "Pick a saved game on the right to continue from there.") style "jr_small"

            null height 34
            use jr_rubric("Pages", JR_LEFT_W)
            null height 10
            hbox:
                spacing 36
                if config.has_autosave:
                    textbutton "Automatic saves":
                        style "jr_entry_button"
                        text_style "jr_entry_button_text"
                        text_size 22
                        action FilePage("auto")
                if config.has_quicksave:
                    textbutton "Quick saves":
                        style "jr_entry_button"
                        text_style "jr_entry_button_text"
                        text_size 22
                        action FilePage("quick")
            null height 14
            # pages up to the last one that holds a save (or the open one), then
            # arrows to go further
            $ page_count = journal_save_page_count()
            hbox:
                box_wrap True
                box_wrap_spacing 10
                xsize JR_LEFT_W
                spacing 10
                textbutton "‹":
                    style "jr_entry_button"
                    text_style "jr_value"
                    text_size 22
                    action FilePagePrevious(auto = False, quick = False)
                for page in range(1, page_count + 1):
                    textbutton str(page):
                        style "jr_entry_button"
                        text_style "jr_value"
                        text_size 22
                        action FilePage(page)
                textbutton "›":
                    style "jr_entry_button"
                    text_style "jr_value"
                    text_size 22
                    tooltip "Next page"
                    action FilePageNext()
            null height 34
            use jr_rubric("Sync", JR_LEFT_W)
            null height 10
            textbutton ("Upload saves ›" if saving else "Download saves ›"):
                style "jr_cheat_link"
                action (UploadSync() if saving else DownloadSync())

            use journal_menu_leave_links

    $ cols = 2
    $ gap = 24
    $ cell_w = (JR_RIGHT_W - gap) // cols
    $ shot_h = int((cell_w - 16) * 9 / 16)

    use jr_page("journal_menu_slots", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            text FilePageName(auto = "Automatic saves", quick = "Quick saves") style "jr_title" size 44
            null height 4
            use jr_double_rule(JR_RIGHT_W)
            null height 18

            $ rows = (slots + cols - 1) // cols
            grid cols rows:
                xspacing gap
                yspacing 14
                for i in range(slots):
                    $ slot = i + 1
                    button:
                        # explicit height: without it a child fills the whole page height
                        xysize (cell_w, shot_h + 16 + 52)
                        background None
                        padding (0, 0, 0, 0)
                        action (FileSave(slot) if saving else FileLoad(slot))
                        tooltip ("Save here" if saving else "Load this game")
                        key "save_delete" action FileDelete(slot)
                        # right click / long press deletes too (asks first)
                        alternate FileDelete(slot)
                        vbox:
                            spacing 4
                            fixed:
                                xysize (cell_w, shot_h + 16)
                                add Solid("#00000026") pos (2, 3) xysize (cell_w, shot_h + 16)
                                add Solid("#faf7f0") xysize (cell_w, shot_h + 16)
                                if FileLoadable(slot):
                                    add Transform(FileScreenshot(slot), fit = "fill", xysize = (cell_w - 16, shot_h)) pos (8, 8)
                                else:
                                    add Solid("#e9e1d0") xysize (cell_w - 16, shot_h) pos (8, 8)
                                    text "empty" style "jr_typed_small" align (0.5, 0.5)
                            frame:
                                style "jr_tile_label"
                                ysize 46
                                vbox:
                                    xalign 0.5
                                    text journal_file_time(slot) style "jr_typed_small" size 15 xalign 0.5
                                    $ save_name = FileSaveName(slot)
                                    if save_name:
                                        text save_name style "jr_small" size 17 xalign 0.5
                for _ in range(rows * cols - slots):
                    null

            null height 12
            if renpy.variant("touch"):
                text "Press and hold a slot to delete it." style "jr_small"
            else:
                text "Right-click a slot (or hover it and press Delete) to remove it." style "jr_small" size 17

# endregion
###############

##################
# region Settings

screen jr_setting_choices(label, choices):
    # """
    # A setting with its options as words; the active one gets the marker.
    # choices: List[Tuple[str, Action]]
    # """

    fixed:
        xysize (JR_LEFT_W, 38)
        text label style "jr_text" size 22 yalign 0.5
        hbox:
            xalign 1.0
            yalign 0.5
            spacing 4
            for choice_label, choice_action in choices:
                textbutton choice_label:
                    style "jr_entry_button"
                    text_style "jr_entry_button_text"
                    text_size 20
                    action choice_action

screen jr_setting_slider(label, value, extra = None):
    fixed:
        xysize (JR_RIGHT_W, 40)
        text label style "jr_text" size 22 yalign 0.5
        hbox:
            xalign 1.0
            yalign 0.5
            spacing 12
            bar:
                value value
                style "jr_slider"
            if extra:
                textbutton extra[0]:
                    style "jr_cheat_link"
                    yalign 0.5
                    action extra[1]

style jr_slider:
    xsize 260
    ysize 18
    left_bar Frame("gui/journal/ui/bar_full.webp", 8, 6)
    right_bar Frame("gui/journal/ui/bar_empty.webp", 8, 6)
    thumb None
    yalign 0.5

# a thin 18px bar is hard to hit with a finger
style jr_slider:
    variant "touch"
    ysize 32

screen journal_menu_settings():
    use jr_page("journal_menu_settings_left", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W

            text "Settings" style "jr_title"
            null height 4
            use jr_double_rule(JR_LEFT_W)

            null height 18
            use jr_rubric("Display", JR_LEFT_W)
            null height 4
            if renpy.variant("pc") or renpy.variant("web"):
                use jr_setting_choices("Window", [("window", Preference("display", "window")), ("fullscreen", Preference("display", "fullscreen"))])
            use jr_setting_choices("Text box", [("100%", SetField(persistent, "display_textbox", 0)), ("50%", SetField(persistent, "display_textbox", 1)), ("0%", SetField(persistent, "display_textbox", 2))])
            if not renpy.variant("small"):
                use jr_setting_choices("Speaker photo", [("shown", SetField(persistent, "dialog_speaker_photo", True)), ("hidden", SetField(persistent, "dialog_speaker_photo", False))])

            null height 14
            use jr_rubric("Skipping", JR_LEFT_W)
            null height 4
            use jr_setting_choices("Unseen text", [("skip", Preference("skip", "all")), ("stop", Preference("skip", "seen"))])
            use jr_setting_choices("After choices", [("keep skipping", Preference("after choices", "skip")), ("stop", Preference("after choices", "stop"))])
            use jr_setting_choices("Transitions", [("show", Preference("transitions", "all")), ("skip", Preference("transitions", "none"))])

            null height 14
            use jr_rubric("Game", JR_LEFT_W)
            null height 4
            if not renpy.android and not renpy.ios:
                use jr_setting_choices("Shortcuts", [("shown", SetField(persistent, "shortcuts", 0)), ("hidden", SetField(persistent, "shortcuts", 1)), ("off", SetField(persistent, "shortcuts", 2))])
            use jr_setting_choices("Supporter list", [("from web", SetField(persistent, "load_supporter", 1)), ("local", SetField(persistent, "load_supporter", 0))])
            use jr_setting_choices("Tutorial", [("on", SetField(persistent, "tutorial", True)), ("off", SetField(persistent, "tutorial", False))])

            use journal_menu_leave_links

    use jr_page("journal_menu_settings_right", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            text "Speed & sound" style "jr_title" size 44
            null height 4
            use jr_double_rule(JR_RIGHT_W)

            null height 18
            use jr_rubric("Speed", JR_RIGHT_W)
            null height 4
            use jr_setting_slider("Text speed", Preference("text speed"))
            use jr_setting_slider("Auto-forward", Preference("auto-forward time"))
            if preferences.transitions == 2:
                use jr_setting_slider("Transitions", FieldValue(persistent, 'transitionSpeed', 2.0, max_is_zero = False, style = 'jr_slider', offset = 0, step = .2,
                    action = SetVariable("dissolveM", Dissolve(0.5 * (2.0 - persistent.transitionSpeed)))))

            if config.has_music or config.has_sound or config.has_voice:
                null height 14
                use jr_rubric("Sound", JR_RIGHT_W)
                null height 4
                if config.has_music:
                    use jr_setting_slider("Music", Preference("music volume"))
                if config.has_sound:
                    use jr_setting_slider("Ambience", Preference("mixer ambience volume"))
                    use jr_setting_slider("Effects", Preference("sound volume"), (("test", Play("sound", config.sample_sound)) if config.sample_sound else None))
                # scene voices (moans, breathing) share the voice mixer, see wiki/Audio.md
                if config.has_voice:
                    use jr_setting_slider("Voices", Preference("voice volume"), (("test", Play("voice", config.sample_voice)) if config.sample_voice else None))
                fixed:
                    xysize (JR_RIGHT_W, 38)
                    text "In background" style "jr_text" size 22 yalign 0.5
                    hbox:
                        xalign 1.0
                        yalign 0.5
                        spacing 4
                        textbutton "play":
                            style "jr_entry_button"
                            text_style "jr_entry_button_text"
                            text_size 20
                            action [Preference("audio when unfocused", "enable"), Preference("audio when minimized", "enable")]
                        textbutton "silent":
                            style "jr_entry_button"
                            text_style "jr_entry_button_text"
                            text_size 20
                            action [Preference("audio when unfocused", "disable"), Preference("audio when minimized", "disable")]
                fixed:
                    xysize (JR_RIGHT_W, 38)
                    text "Mute everything" style "jr_text" size 22 yalign 0.5
                    textbutton ("muted" if preferences.get_mute("sfx") and preferences.get_mute("ambience") else "mute"):
                        style "jr_entry_button"
                        text_style "jr_entry_button_text"
                        text_size 20
                        xalign 1.0
                        yalign 0.5
                        action Preference("all mute", "toggle")

            # kinks from the base game and active mods; neutral = ask first
            $ known_kinks = get_known_kinks()
            if known_kinks:
                null height 14
                use jr_rubric("Content preferences", JR_RIGHT_W)
                null height 4
                text "Neutral asks before a scene that contains it." style "jr_small" size 17
                null height 4
                use kink_setting_rows(known_kinks, JR_RIGHT_W)

# endregion
##################

#################
# region History

screen journal_menu_history():
    use jr_page("journal_menu_history_left", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W
            text "History" style "jr_title"
            null height 4
            use jr_double_rule(JR_LEFT_W)
            null height 10
            text "Everything said recently, newest at the bottom of the right page." style "jr_small"
            use journal_menu_leave_links

    use jr_page("journal_menu_history", JR_RIGHT_X, JR_RIGHT_W, yinitial = 1.0):
        vbox:
            xsize JR_RIGHT_W
            spacing 10
            if not _history_list:
                text "Nothing has been said yet." style "jr_small"
            for h in _history_list:
                vbox:
                    xsize JR_RIGHT_W
                    if h.who:
                        text h.who:
                            style "jr_text"
                            size 19
                            font JR_FONT_BOLD
                            substitute False
                            if "color" in h.who_args:
                                color h.who_args["color"]
                    text renpy.filter_text_tags(h.what, allow = gui.history_allow_tags):
                        style "jr_body"
                        size 21
                        substitute False

# endregion
#################

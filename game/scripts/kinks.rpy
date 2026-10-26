##################################
# region Kinks ----------------- #
##################################

# What the player allows, per kink key: "yes", "no" or "neutral" (ask).
# Shared by all saves; a key that is missing counts as "neutral".
default persistent.kink_settings = {}

init -99 python:
    from typing import Dict, List, Optional, Tuple

    KINK_SETTINGS = ("yes", "neutral", "no")

    class Kink:
        """
        A content preference the player can allow, block or be asked about.

        The key is the identity: the base game and any number of mods may
        register the same key, and they all share one kink with one setting.

        ### Parameters:
        1. key: str
            - Unique key, compared case-insensitively ("NTR" == "ntr").
        2. title: str
            - Short name for buttons and lists.
        3. description: str
            - One or two neutral, non-explicit sentences for the prompt and
                the settings page.
        """

        def __init__(self, key: str, title: str, description: str = ""):
            self.key = normalize_kink_key(key)
            self.title = title
            self.description = description
            # (source_key, title, description) in registration order
            self.sources: List[Tuple[str, str, str]] = []

        def add_source(self, source_key: str, title: str, description: str):
            if any(source[0] == source_key for source in self.sources):
                return
            if self.sources and (self.sources[0][1] != title or self.sources[0][2] != description):
                log(f"Kink '{self.key}' from '{source_key}' has a different title or description than from '{self.sources[0][0]}'; the first one is used",
                    log_type = "warning", category = "kinks")
            self.sources.append((source_key, title, description))

        def get_source_keys(self) -> List[str]:
            return [source[0] for source in self.sources]

        def get_active_source_keys(self) -> List[str]:
            return [source_key for source_key in self.get_source_keys() if source_key == "base" or is_mod_active(source_key)]

        def _get_text_source(self) -> Tuple[str, str, str]:
            # the base game's text wins, then the first active mod's, then
            # whoever registered it first (a kink of switched-off mods only)
            for source in self.sources:
                if source[0] == "base":
                    return source
            active = self.get_active_source_keys()
            for source in self.sources:
                if source[0] in active:
                    return source
            return self.sources[0]

        def get_title(self) -> str:
            return self._get_text_source()[1] if self.sources else self.title

        def get_description(self) -> str:
            return self._get_text_source()[2] if self.sources else self.description

        def is_known(self) -> bool:
            """
            True while at least one source that registered the kink is active;
            content of a kink nobody active knows about is never allowed.
            """

            return len(self.get_active_source_keys()) > 0

        def to_data(self) -> Dict[str, str]:
            # plain data for persistent.modList: no class instances in persistent
            return {"key": self.key, "title": self.title, "description": self.description}

    # rebuilt at every start; never saved
    kink_registry: Dict[str, Kink] = {}

    def normalize_kink_key(key: str) -> str:
        return str(key).strip().lower()

    def register_kinks(source_key: str, kinks: List[Kink]) -> List[Dict[str, str]]:
        """
        Adds kinks to the registry under the given source (``"base"`` or a
        mod key). Called by ``register_mod(..., kinks = [...])``; the base
        game registers its kinks through it directly.

        ### Returns:
        1. List[Dict[str, str]]
            - The kinks as plain data, for the mod list.
        """

        data = []
        for kink in kinks:
            if not isinstance(kink, Kink):
                log(f"'{source_key}' registered a kink that is not a Kink: {kink!r}", log_type = "error", category = "kinks")
                continue

            registered = kink_registry.get(kink.key)
            if registered is None:
                registered = Kink(kink.key, kink.title, kink.description)
                kink_registry[kink.key] = registered
            registered.add_source(source_key, kink.title, kink.description)
            data.append(kink.to_data())
        return data

    def get_kink(key: str) -> Optional[Kink]:
        return kink_registry.get(normalize_kink_key(key))

    def get_known_kinks() -> List[Kink]:
        """
        All kinks with at least one active source, sorted by title, for the
        settings page.
        """

        return sorted((kink for kink in kink_registry.values() if kink.is_known()), key = lambda kink: kink.get_title().lower())

    def get_mod_kinks(mod_key: str) -> List[Kink]:
        """
        The kinks a mod registered, also while it is switched off (taken from
        its entry in the mod list), so they can be set before switching it on.
        """

        mod = persistent.modList.get(mod_key) if persistent.modList else None
        if mod is None:
            return []
        output = []
        for data in mod.get("kinks", []):
            kink = get_kink(data["key"])
            if kink is None:
                kink = Kink(data["key"], data["title"], data.get("description", ""))
            output.append(kink)
        return output

    ########################
    # Settings and answers

    def get_kink_setting(key: str) -> str:
        """
        The value from the menu: ``"yes"``, ``"no"`` or ``"neutral"``.
        """

        setting = persistent.kink_settings.get(normalize_kink_key(key), "neutral")
        return setting if setting in KINK_SETTINGS else "neutral"

    def set_kink_setting(key: str, setting: str):
        if setting not in KINK_SETTINGS:
            log(f"Unknown kink setting '{setting}' for '{key}'", log_type = "error", category = "kinks")
            return
        key = normalize_kink_key(key)
        persistent.kink_settings[key] = setting
        # a choice made in the menu replaces whatever was answered for now
        _get_kink_session_answers().pop(key, None)

    def _get_kink_session_answers() -> Dict[str, bool]:
        # renpy.session is neither saved nor rolled back and only empties when
        # the game is restarted: exactly the lifetime of a "for now" answer
        return renpy.session.setdefault("kink_answers", {})

    def get_kink_session_answer(key: str) -> Optional[bool]:
        return _get_kink_session_answers().get(normalize_kink_key(key))

    def set_kink_session_answer(key: str, allowed: bool):
        _get_kink_session_answers()[normalize_kink_key(key)] = bool(allowed)

    def get_kink_state(key: str) -> Optional[bool]:
        """
        Whether content with this kink may run right now.

        ### Returns:
        1. Optional[bool]
            - True: allowed (setting yes, or neutral answered "yes, for now").
            - False: not allowed (setting no, neutral answered "no, for now",
                or no active source knows the kink).
            - None: neutral and not answered this session; ask the player.
        """

        kink = get_kink(key)
        if kink is None or not kink.is_known():
            return False

        setting = get_kink_setting(key)
        if setting == "yes":
            return True
        if setting == "no":
            return False
        return get_kink_session_answer(key)

    def get_open_kinks(keys) -> List[str]:
        """
        The keys among ``keys`` that still need an answer, without duplicates,
        in their original order.
        """

        output = []
        for key in keys:
            key = normalize_kink_key(key)
            if key not in output and get_kink_state(key) is None:
                output.append(key)
        return output

    class SetKinkSetting(Action):
        """
        Screen action for the yes / neutral / no choices; selected while the
        kink has that setting, so the active choice gets the marker.
        """

        def __init__(self, key: str, setting: str):
            self.key = normalize_kink_key(key)
            self.setting = setting

        def __call__(self):
            set_kink_setting(self.key, self.setting)
            renpy.restart_interaction()

        def get_selected(self) -> bool:
            return get_kink_setting(self.key) == self.setting

init -98 python:
    # The base game's kinks. Mods pass theirs to register_mod(kinks = [...]).
    base_kinks = []

    repair_mod_list()
    persistent.modList['base']['kinks'] = register_kinks("base", base_kinks)

# endregion
##################################

#######################################
# region Kink prompt ---------------- #
#######################################

init python:
    # answer -> (button text, what it does)
    KINK_ANSWERS = (
        ("yes", "Yes"),
        ("no", "No"),
        ("yes_now", "Yes, for now"),
        ("no_now", "No, for now"),
    )

    def kink_prompt_text(keys: List[str]) -> str:
        """
        The line in the dialogue box under the prompt, naming the kinks.
        """

        titles = []
        for key in keys:
            kink = get_kink(key)
            titles.append(kink.get_title() if kink else key)
        if len(titles) == 1:
            listed = titles[0]
        else:
            listed = ", ".join(titles[:-1]) + " and " + titles[-1]
        return "Quick check before we go on: what comes next can involve {}. How do you want me to handle {}?".format(listed, "that" if len(titles) == 1 else "those")

    def apply_kink_answers(answers: Dict[str, str]):
        """
        Stores the prompt's answers: "yes"/"no" become the setting,
        "yes_now"/"no_now" leave the setting neutral and only hold for this
        session.
        """

        for key, answer in answers.items():
            if answer in ("yes", "no"):
                set_kink_setting(key, answer)
            elif answer == "yes_now":
                set_kink_session_answer(key, True)
            elif answer == "no_now":
                set_kink_session_answer(key, False)

    def ask_kinks(*keys: str):
        """
        Shows the prompt for every key that is still open (neutral and not
        answered this session). Nothing happens when none is. Has to run in
        script (a ``$`` line or an ``if`` in a label), never in screen code.
        """

        open_keys = get_open_kinks(keys)
        if not open_keys:
            return

        # a taller line still on screen would peek out above the prompt's box
        renpy.hide_screen("say")
        renpy.call_screen("kink_prompt", open_keys, show_host = not _kink_prompt_host_on_stage())
        # rolling back past the answer would only bring the same question back
        renpy.block_rollback()

    def _kink_prompt_host_on_stage() -> bool:
        """
        True when a scene has already put Emiko's paperdoll up: the prompt
        then doesn't draw a second Emiko next to her.
        """

        if paperdoll_manager is None:
            return False
        obj = paperdoll_manager.paperdoll_objs.get("emiko_langley")
        return obj is not None and paperdoll_is_visible(obj)

    def kink_prompt_host_layers() -> List[str]:
        """
        Emiko's two paperdoll layers (body, face) for the prompt, resolved
        straight from her patterns: the prompt also runs outside events,
        where there is no paperdoll manager to ask.

        ### Returns:
        1. List[str]
            - The two image paths; empty strings for layers that are missing.
        """

        emiko_person = Person["emiko_langley"]
        if emiko_person is None:
            return []

        values = update_dict(
            {"mood": "neutral", "pose": 1, "outfit": "uniform", "level": 1, "mouth": "closed", "state": "", "char_var": 1, "look": "follow", "extra1": "", "extra2": ""},
            getattr(emiko_person, "paperdollDefaults", None) or {},
        )
        values = update_dict(values, {"pose": "36", "outfit": "uniform", "level": get_character_by_key("secretary").get_level(), "mood": "happy", "mouth": "open"})
        alt_keys = ["level", "mouth", "state", "char_var", "extra1", "extra2"]

        base = f"{emiko_person.basePath}images/paperdoll/{emiko_person.name}"
        patterns = (
            f"{base}/bottom/{emiko_person.name} <char_var> <pose> <outfit> <level> <state> <extra1>.png",
            f"{base}/top/{emiko_person.name} <char_var> <pose> <mood> <mouth> <look> <extra2>.png",
        )
        return [find_available_images(refine_image_with_alternatives(pattern, alt_keys, **values)) for pattern in patterns]

    def kink_check(*keys: str) -> bool:
        """
        For a short branch inside an event: asks about the open keys first,
        then tells whether all of them are allowed.

        ```renpy
        if kink_check("incest_sisters"):
            # the extra beat
        ```
        """

        ask_kinks(*keys)
        return all(get_kink_state(key) is True for key in keys)

    def settle_event_kinks(event_obj, **kwargs) -> bool:
        """
        Right before an event runs: asks about its open kinks (a composite's
        include those of every fragment it could roll), then tells whether the
        answers let it run. Events without kinks pass straight through.
        """

        keys = event_obj.get_kinks(**kwargs)
        if not keys:
            return True
        ask_kinks(*keys)
        return event_obj.kinks_allow(**kwargs)

    # set when a storage call ended with every pick turned down, so the menu
    # that started it shows again instead of running its exit (call_element)
    kink_declined_return = False

    def route_kink_declined(event_storage, no_fallback: bool = False, **kwargs):
        """
        Nothing is left after the player turned events down. A storage with its
        own fallback (a building's entry storage, whose fallback is the action
        menu) uses it; everything else just returns, which puts the player back
        into the menu they picked from, without a daytime change, instead of
        the default "There is nothing to do here." and the map.
        """

        global kink_declined_return
        kink_declined_return = True

        fallback = event_storage.get_fallback()
        if no_fallback or fallback is None or fallback is default_fallback:
            return
        fallback.call(**kwargs)

    def consume_kink_declined_return() -> bool:
        global kink_declined_return
        declined = kink_declined_return
        kink_declined_return = False
        return declined

style kink_prompt_answer is jr_entry_button
style kink_prompt_answer_text is jr_value:
    size 22
    color JR_PRINT
    hover_color "#000"
    selected_color JR_ACCENT

transform kink_prompt_host_enter:
    on show:
        xoffset -500 alpha 0.0
        easein 0.4 xoffset 0 alpha 1.0

screen kink_prompt(keys, show_host = True):
    # """
    # Asks how to handle one or more kinks before content that contains them:
    # Emiko on the left, her question in the dialogue box, the answers on a
    # card. Every kink gets four answers; Continue unlocks once all are
    # answered. There is deliberately no way to cancel: every answer belongs
    # to a kink. Stores the answers (apply_kink_answers) and returns them.
    # """

    modal True
    zorder 50

    default answers = {}
    # resolved once: the file lookups don't need to run on every redraw
    default host_layers = [Image(path) for path in kink_prompt_host_layers() if path] if show_host else []

    $ text = kink_prompt_text(keys)
    $ dialog_height = journal_dialog_box_height(text)
    $ card_w = 900
    $ rows_w = card_w - 84
    $ emiko_person = Person["emiko_langley"]

    # drawn before the box, so the box covers her from the waist down
    if host_layers:
        fixed:
            fit_first True
            at kink_prompt_host_enter
            xpos 470
            xanchor 0.5
            ypos 40
            for layer in host_layers:
                add Transform(layer, fit = "contain", xysize = (900, 1620))

    # with Emiko standing there, her roster photo in the box would be a double
    if emiko_person is not None:
        use say(emiko_person.get_full_name(), text, speaker = (None if host_layers else emiko_person.name))
    else:
        use say(None, text)

    frame:
        background Frame("gui/journal/ui/choice_slip.webp", 14, 12, 14, 14)
        padding (40, 28, 44, 30)
        xsize card_w
        xalign 1.0
        xoffset -40
        yalign 1.0
        yoffset -(dialog_height + 6)

        vbox:
            spacing 18

            # up to three kinks fit above the box; more scroll
            if len(keys) > 3:
                side "c r":
                    xsize rows_w
                    ysize 1080 - dialog_height - 190
                    spacing 8

                    viewport id "kink_prompt_rows":
                        mousewheel True
                        draggable "touch"
                        use kink_prompt_rows(keys, answers, rows_w - 26)

                    vbar value YScrollValue("kink_prompt_rows") style "jr_vscrollbar"
            else:
                use kink_prompt_rows(keys, answers, rows_w)

            textbutton "Continue ›":
                style "jr_choice_slip"
                text_style "jr_choice_text"
                text_color JR_ACCENT
                xalign 1.0
                sensitive len(answers) == len(keys)
                action [Function(apply_kink_answers, answers), Return(answers)]

screen kink_setting_rows(kinks, width):
    # """
    # yes / neutral / no per kink, for the settings page and the mod page.
    # A neutral kink answered "for now" says so next to its title.
    # Positions are absolute: these rows sit in columns that scroll, where
    # yalign would cut them off past the bottom of the page.
    # """

    vbox:
        xsize width
        spacing 6
        for kink in kinks:
            $ session_answer = get_kink_session_answer(kink.key) if get_kink_setting(kink.key) == "neutral" else None
            vbox:
                xsize width
                fixed:
                    xysize (width, 38)
                    hbox:
                        yanchor 0.5
                        ypos 19
                        spacing 8
                        text kink.get_title() style "jr_text" size 22
                        if session_answer is not None:
                            text ("this session: yes" if session_answer else "this session: no"):
                                style "jr_small"
                                font "fonts/CrimsonPro-Italic.ttf"
                                color JR_PENCIL
                                yalign 1.0
                    hbox:
                        xalign 1.0
                        yanchor 0.5
                        ypos 19
                        spacing 4
                        for setting in KINK_SETTINGS:
                            textbutton setting:
                                style "jr_entry_button"
                                text_style "jr_entry_button_text"
                                text_size 20
                                action SetKinkSetting(kink.key, setting)
                if kink.get_description():
                    text kink.get_description() style "jr_small" size 17 color JR_PENCIL xmaximum width

screen kink_prompt_rows(keys, answers, width):
    # one row per kink: title, description and the four answers
    vbox:
        xsize width
        spacing 22
        for key in keys:
            $ kink = get_kink(key)
            vbox:
                spacing 4
                text (kink.get_title() if kink else key) style "jr_text" font JR_FONT_SEMIBOLD size 28
                if kink and kink.get_description():
                    text kink.get_description() style "jr_small" xmaximum width
                null height 2
                hbox:
                    spacing 14
                    for answer, label in KINK_ANSWERS:
                        textbutton label:
                            style "kink_prompt_answer"
                            selected answers.get(key) == answer
                            action [UISound("choice"), SetDict(answers, key, answer)]

# endregion
#######################################

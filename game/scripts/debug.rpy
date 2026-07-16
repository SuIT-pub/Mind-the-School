default time_freeze = False
default debug_mode = False

init -100 python:
    import pprint

    class FloatInputValue(InputValue):
        def __init__(self, variable, default=0.0):
            self.variable = variable
            self.default = default

        def get_text(self):
            return str(getattr(store, self.variable))

        def set_text(self, s):
            try:
                setattr(store, self.variable, float(s))
            except ValueError:
                setattr(store, self.variable, self.default)
            renpy.restart_interaction()

        def enter(self):
            renpy.run(RestartInteraction())
            return True

    def log_separator():
        print("##################################################")

    def log_json(key: str, value: Dict[string, Any]):
        print(key + ":", end="")
        pprint.pprint(value, compact = False)

    def log_val(key: str, *values: Any):
        """
        Prints a key and value

        ### Parameters:
        1. key: str
            - The key to print
        2. value: Any
            - The value to print
        """

        value = ", ".join(map(str, values))

        print(key + ": " + str(value))
        return

    def log(msg: str):
        """
        Prints a message

        ### Parameters:
        1. msg: str
            - The message to print
        """

        print(str(msg))
        return

    def log_error(code: int, msg: str):
        """
        Prints an error message

        ### Parameters:
        1. msg: str
            - The message to print
        """

        print(f"|ERROR[{str(code)}]| {str(msg)}")
        add_notify_message("|ERROR| " + str(msg))
        return

    log_number = 0

    def log_count(msg: str, start = False):
        if start:
            log_number = 0
        
        log_number += 1
        log_val(msg, log_number)

init -1 python:
    test_events = EventStorage("test_events", "misc")

# init 1 python:
    # test_events.add_event(
    #     Event(3, "test_event",
    #         Pattern("main", "images/background/school building/9 0 1.webp"),
    #         thumbnail = "images/background/school building/9 0 1.webp"),
    # )

label test_label():

    $ hide_all()

    call call_available_event(test_events) from test_label_1

    jump map_entry

   
label test_event (**kwargs):
    $ begin_event(**kwargs)

    $ luna = Person["luna_clark"]
    $ luna.register_paperdoll(level = 10, mood = "happy", mouth = "closed")
    $ paperdoll_manager.set_background("images/background/school building/9 0 1.webp", blur = True)
    $ luna.display(PDAMove(alignX = 0.5, duration = 2.0))
    $ renpy.pause()
    $ luna.display(PDAImage(level = 9), PDABlur(10.0, duration = 3.0))
    $ paperdoll_manager.set_background("images/background/school building/9 0 1.webp", blur = False)
    $ renpy.pause()

    $ end_event('new_daytime', **kwargs)

label show_paperdoll_test():

    $ hide_all()

    $ paperdoll_test_character = ""
    $ paperdoll_test_char_var = "$"
    $ paperdoll_test_pose = -1
    $ paperdoll_test_outfit = ""
    $ paperdoll_test_level = -1
    $ paperdoll_test_state = ""
    $ paperdoll_test_emotion = ""
    $ paperdoll_test_mouth = ""

    $ old_paperdoll_test_character = paperdoll_test_character
    $ old_paperdoll_test_pose = paperdoll_test_pose
    $ old_paperdoll_test_outfit = paperdoll_test_outfit
    $ old_paperdoll_test_level = paperdoll_test_level
    $ old_paperdoll_test_state = paperdoll_test_state
    $ old_paperdoll_test_emotion = paperdoll_test_emotion
    $ old_paperdoll_test_mouth = paperdoll_test_mouth

    $ paperdoll_test_override_y_2 = 0.0
    $ paperdoll_test_override_x_2 = 0.0

    $ paperdoll_test_state_values = []
    $ paperdoll_test_level_values = []

    $ paperdoll_show_selection = True
    $ paperdoll_show_values = True
    $ paperdoll_show_presets = True
    $ paperdoll_active_field = None
    $ paperdoll_active_preset = None
    
    $ paperdoll_alignX = 1.0
    $ paperdoll_alignY = 0.0
    $ paperdoll_rotation = 0.0
    $ paperdoll_zoom = 1.0
    $ paperdoll_blur = 0.0
    $ paperdoll_flip = False

    $ paperdoll_sync_buffers()

    $ init_paperdoll_manager()
    $ charact = None

    while(True):
        $ log_separator()
        call screen paperdoll_test_screen()

        $ log_val("paperdoll_test_character", paperdoll_test_character)
        $ log_val("paperdoll_test_char_var", paperdoll_test_char_var)
        $ log_val("paperdoll_test_pose", paperdoll_test_pose)
        $ log_val("paperdoll_test_outfit", paperdoll_test_outfit)
        $ log_val("paperdoll_test_level", paperdoll_test_level)
        $ log_val("paperdoll_test_emotion", paperdoll_test_emotion)
        $ log_val("paperdoll_test_mouth", paperdoll_test_mouth)
        $ log_val("paperdoll_test_state", paperdoll_test_state)
        $ log_val("character", charact)

        if paperdoll_test_character != "" and paperdoll_test_pose > 0 and paperdoll_test_outfit != "" and paperdoll_test_level >= 0 and paperdoll_test_emotion != "" and paperdoll_test_mouth != "":
            $ log_val("displaying paperdoll", paperdoll_test_character)
            if old_paperdoll_test_character != paperdoll_test_character or charact == None:
                $ log_val("registering paperdoll", paperdoll_test_character)
                $ unload_paperdoll_manager()
                $ init_paperdoll_manager()
                $ kwargs = {}
                $ charact = find_person(paperdoll_test_character)
                $ log_val("character", charact)
                $ charact.register_paperdoll()
                
                $ paperdoll_obj = paperdoll_manager.get_obj(paperdoll_test_character)

            $ paperdoll_test_char_var_values = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} ")})

            if paperdoll_test_char_var not in paperdoll_test_char_var_values and len(paperdoll_test_char_var_values) > 0:
                $ paperdoll_test_char_var = paperdoll_test_char_var_values[0]

            $ paperdoll_test_level_values = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} ")})

            if len(paperdoll_test_level_values) > 0 and (len(paperdoll_test_level_values) > 1 or paperdoll_test_level_values[0] != "$"):
                $ paperdoll_test_level_values = sorted(int(i) for i in paperdoll_test_level_values)
                if paperdoll_test_level not in paperdoll_test_level_values:
                    $ paperdoll_test_level = paperdoll_test_level_values[0]

            $ paperdoll_test_state_values = list({s.replace(".png", "").replace(".webp", "").replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} {paperdoll_test_level} ", "").replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} $ ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} {paperdoll_test_level} ") or s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} $ ")})

            if paperdoll_test_state not in paperdoll_test_state_values and len(paperdoll_test_state_values) > 0:
                $ paperdoll_test_state = paperdoll_test_state_values[0]

            if paperdoll_test_state == "$":
                $ paperdoll_test_state = ""

            $ log_val("paperdoll_test_state_values", paperdoll_test_state_values)
            $ log_val("paperdoll_test_state", paperdoll_test_state)

            if paperdoll_active_preset is not None:
                $ paperdoll_sync_preset_to_test_state()

            $ charact.display(*paperdoll_build_test_display_actions())
screen paperdoll_test_screen():
    vbox:
        hbox:
            textbutton "^":
                text_style "buttons_idle"
                action [SetVariable("paperdoll_show_selection", not paperdoll_show_selection), Return()]

            if paperdoll_show_selection:
                $ paperdoll_selector_character = list({s.replace("images/paperdoll/", "").split("/")[0] for s in renpy.list_files() if s.startswith("images/paperdoll/")})
                frame:
                    area(0, 0, 300, 900)
                    background Solid("#fff6")
                    vbox:
                        text "Characters" style "journal_text"
                        if paperdoll_test_character != "":
                            $ log_val("paperdoll_test_character", paperdoll_test_character)
                            $ log_val("paperdoll_selector_character", paperdoll_selector_character)
                            hbox:
                                if paperdoll_selector_character.index(paperdoll_test_character) != 0:
                                    textbutton "<":
                                        text_style "buttons_idle"
                                        action [SetVariable("paperdoll_test_character", paperdoll_selector_character[paperdoll_selector_character.index(paperdoll_test_character) - 1]), SetVariable("paperdoll_test_char_var", ""), SetVariable("paperdoll_test_pose", -1), SetVariable("paperdoll_test_outfit", ""), SetVariable("paperdoll_test_level", 1), SetVariable("paperdoll_test_emotion", ""), SetVariable("paperdoll_test_mouth", ""), SetVariable("paperdoll_test_state", ""), SetVariable("paperdoll_test_state_values", []), Return()]
                                else:
                                    textbutton "<":
                                        text_style "buttons_idle"
                                        action [SetVariable("paperdoll_test_character", paperdoll_selector_character[len(paperdoll_selector_character) - 1]), SetVariable("paperdoll_test_char_var", ""), SetVariable("paperdoll_test_pose", -1), SetVariable("paperdoll_test_outfit", ""), SetVariable("paperdoll_test_level", 1), SetVariable("paperdoll_test_emotion", ""), SetVariable("paperdoll_test_mouth", ""), SetVariable("paperdoll_test_state", ""), SetVariable("paperdoll_test_state_values", []), Return()]
                                if paperdoll_selector_character.index(paperdoll_test_character) != len(paperdoll_selector_character) - 1:
                                    textbutton ">":
                                        text_style "buttons_idle"
                                        action [SetVariable("paperdoll_test_character", paperdoll_selector_character[paperdoll_selector_character.index(paperdoll_test_character) + 1]), SetVariable("paperdoll_test_char_var", ""), SetVariable("paperdoll_test_pose", -1), SetVariable("paperdoll_test_outfit", ""), SetVariable("paperdoll_test_level", 1), SetVariable("paperdoll_test_emotion", ""), SetVariable("paperdoll_test_mouth", ""), SetVariable("paperdoll_test_state", ""), SetVariable("paperdoll_test_state_values", []), Return()]
                                else:
                                    textbutton ">":
                                        text_style "buttons_idle"
                                        action [SetVariable("paperdoll_test_character", paperdoll_selector_character[0]), SetVariable("paperdoll_test_char_var", ""), SetVariable("paperdoll_test_pose", -1), SetVariable("paperdoll_test_outfit", ""), SetVariable("paperdoll_test_level", 1), SetVariable("paperdoll_test_emotion", ""), SetVariable("paperdoll_test_mouth", ""), SetVariable("paperdoll_test_state", ""), SetVariable("paperdoll_test_state_values", []), Return()]
                        viewport id "paperdoll_selector_characters":
                            mousewheel True
                            draggable "touch"
                            vbox:
                                for character in paperdoll_selector_character:
                                    if character == paperdoll_test_character:
                                        textbutton character:
                                            text_style "buttons_active"
                                            action NullAction()
                                    else:
                                        textbutton character:
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_character", character), SetVariable("paperdoll_test_char_var", ""), SetVariable("paperdoll_test_pose", -1), SetVariable("paperdoll_test_outfit", ""), SetVariable("paperdoll_test_level", 1), SetVariable("paperdoll_test_emotion", ""), SetVariable("paperdoll_test_mouth", ""), SetVariable("paperdoll_test_state", ""), SetVariable("paperdoll_test_state_values", []), Return()]
                        vbar value YScrollValue("paperdoll_selector_characters"):
                            unscrollable "hide"
                            xalign 1.05


                if paperdoll_test_character != "":
                    $ paperdoll_selector_char_var = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} ")})
                    if len(paperdoll_selector_char_var) == 0:
                        $ paperdoll_selector_char_var = ["$"]
                    if len(paperdoll_selector_char_var) == 1:
                        $ paperdoll_test_char_var = paperdoll_selector_char_var[0]

                    if len(paperdoll_selector_char_var) > 1:
                        frame:
                            area(0, 0, 200, 900)
                            background Solid("#fff6")
                            vbox:
                                text "char_var" style "journal_text"
                                if paperdoll_test_char_var != "":
                                    hbox:
                                        if paperdoll_selector_char_var.index(paperdoll_test_char_var) != 0:
                                            textbutton "<":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_char_var", paperdoll_selector_char_var[paperdoll_selector_char_var.index(paperdoll_test_char_var) - 1]), Return()]
                                        else:
                                            textbutton "<":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_char_var", paperdoll_selector_char_var[len(paperdoll_selector_char_var) - 1]), Return()]
                                        if paperdoll_selector_char_var.index(paperdoll_test_char_var) != len(paperdoll_selector_char_var) - 1:
                                            textbutton ">":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_char_var", paperdoll_selector_char_var[paperdoll_selector_char_var.index(paperdoll_test_char_var) + 1]), Return()]
                                        else:
                                            textbutton ">":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_char_var", paperdoll_selector_char_var[0]), Return()]
                                viewport id "paperdoll_selector_char_var":
                                    mousewheel True
                                    draggable "touch"
                                    vbox:
                                        for cv in paperdoll_selector_char_var:
                                            if cv == paperdoll_test_char_var:
                                                textbutton cv:
                                                    text_style "buttons_active"
                                                    action NullAction()
                                            else:
                                                textbutton cv:
                                                    text_style "buttons_idle"
                                                    action [SetVariable("paperdoll_test_char_var", cv), Return()]
                                vbar value YScrollValue("paperdoll_selector_char_var"):
                                    unscrollable "hide"
                                    xalign 1.05

                if paperdoll_test_character != "":
                    frame:
                        area(0, 0, 120, 900)
                        background Solid("#fff6")
                        vbox:
                            text "Pose" style "journal_text"
                            hbox:
                                vbox:
                                    if paperdoll_test_pose > 1:
                                        textbutton "-":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_pose", paperdoll_test_pose - 1), Return()]
                                    else:
                                        textbutton "-":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_pose", 34), Return()]
                                    for i in range(1, 18):
                                        if i == paperdoll_test_pose:
                                            textbutton str(i):
                                                text_style "buttons_active"
                                                action NullAction()
                                        else:
                                            textbutton str(i):
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_pose", i), Return()]
                                vbox:
                                    if paperdoll_test_pose < 34:
                                        textbutton "+":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_pose", paperdoll_test_pose + 1), Return()]
                                    else:
                                        textbutton "+":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_pose", 1), Return()]
                                    for i in range(18, 35):
                                        if i == paperdoll_test_pose:
                                            textbutton str(i):
                                                text_style "buttons_active"
                                                action NullAction()
                                        else:
                                            textbutton str(i):
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_pose", i), Return()]
                            
                if paperdoll_test_pose > 0:
                    $ log_val("paperdoll_test_char_var", paperdoll_test_char_var)
                    $ paperdoll_selector_outfit = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} ")})
                    frame:
                        area(0, 0, 200, 900)
                        background Solid("#fff6")
                        vbox:
                            text "Outfits" style "journal_text"
                            if paperdoll_test_outfit != "":
                                hbox:
                                    if paperdoll_selector_outfit.index(paperdoll_test_outfit) != 0:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_outfit", paperdoll_selector_outfit[paperdoll_selector_outfit.index(paperdoll_test_outfit) - 1]), Return()]
                                    else:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_outfit", paperdoll_selector_outfit[len(paperdoll_selector_outfit) - 1]), Return()]
                                    if paperdoll_selector_outfit.index(paperdoll_test_outfit) != len(paperdoll_selector_outfit) - 1:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_outfit", paperdoll_selector_outfit[paperdoll_selector_outfit.index(paperdoll_test_outfit) + 1]), Return()]
                                    else:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_outfit", paperdoll_selector_outfit[0]), Return()]
                            viewport id "paperdoll_selector_outfits":
                                mousewheel True
                                draggable "touch"
                                vbox:
                                    for outfit in paperdoll_selector_outfit:
                                        if outfit == paperdoll_test_outfit:
                                            textbutton outfit:
                                                text_style "buttons_active"
                                                action NullAction()
                                        else:
                                            textbutton outfit:
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_outfit", outfit), Return()]
                            vbar value YScrollValue("paperdoll_selector_outfits"):
                                unscrollable "hide"
                                xalign 1.05
                                        
                if paperdoll_test_outfit != "":
                    $ paperdoll_test_level_values = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} ")})
                    if len(paperdoll_test_level_values) > 1 or paperdoll_test_level_values[0] != "$":
                        $ paperdoll_test_level_values = [int(i) for i in paperdoll_test_level_values]
                        $ paperdoll_test_level_values.sort()
                        if paperdoll_test_level not in paperdoll_test_level_values:
                            $ paperdoll_test_level = paperdoll_test_level_values[0]
                        frame:
                            area(0, 0, 200, 900)
                            background Solid("#fff6")
                            vbox:
                                text "Levels" style "journal_text"
                                if isinstance(paperdoll_test_level, int):
                                    hbox:
                                        if paperdoll_test_level_values.index(paperdoll_test_level) != 0:
                                            textbutton "<":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_level", paperdoll_test_level_values[paperdoll_test_level_values.index(paperdoll_test_level) - 1]), Return()]
                                        else:
                                            textbutton "<":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_level", paperdoll_test_level_values[len(paperdoll_test_level_values) - 1]), Return()]
                                        if paperdoll_test_level_values.index(paperdoll_test_level) != len(paperdoll_test_level_values) - 1:
                                            textbutton ">":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_level", paperdoll_test_level_values[paperdoll_test_level_values.index(paperdoll_test_level) + 1]), Return()]
                                        else:
                                            textbutton ">":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_level", paperdoll_test_level_values[0]), Return()]
                                viewport id "paperdoll_selector_levels":
                                    mousewheel True
                                    draggable "touch"
                                    vbox:
                                        for level in paperdoll_test_level_values:
                                            if level == paperdoll_test_level:
                                                textbutton str(level):
                                                    text_style "buttons_active"
                                                    action NullAction()
                                            else:
                                                textbutton str(level):
                                                    text_style "buttons_idle"
                                                    action [SetVariable("paperdoll_test_level", level), Return()]
                                vbar value YScrollValue("paperdoll_selector_levels"):
                                    unscrollable "hide"
                                    xalign 1.05
                            
                    $ paperdoll_selector_emotion = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/top/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/top/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} ")})
                    frame:
                        area(0, 0, 200, 900)
                        background Solid("#fff6")
                        vbox:
                            text "Emotions" style "journal_text"
                            if paperdoll_test_emotion != "":
                                hbox:
                                    if paperdoll_selector_emotion.index(paperdoll_test_emotion) != 0:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_emotion", paperdoll_selector_emotion[paperdoll_selector_emotion.index(paperdoll_test_emotion) - 1]), Return()]
                                    else:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_emotion", paperdoll_selector_emotion[len(paperdoll_selector_emotion) - 1]), Return()]
                                    if paperdoll_selector_emotion.index(paperdoll_test_emotion) != len(paperdoll_selector_emotion) - 1:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_emotion", paperdoll_selector_emotion[paperdoll_selector_emotion.index(paperdoll_test_emotion) + 1]), Return()]
                                    else:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_emotion", paperdoll_selector_emotion[0]), Return()]
                            viewport id "paperdoll_selector_emotions":
                                mousewheel True
                                draggable "touch"
                                vbox:
                                    for emotion in paperdoll_selector_emotion:
                                        if emotion == paperdoll_test_emotion:
                                            textbutton emotion:
                                                text_style "buttons_active"
                                                action NullAction()
                                        else:
                                            textbutton emotion:
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_emotion", emotion), Return()]
                            vbar value YScrollValue("paperdoll_selector_emotions"):
                                unscrollable "hide"
                                xalign 1.05
                if paperdoll_test_emotion not in ["pout", "suprised"] and paperdoll_test_emotion != "":
                    frame:
                        area(0, 0, 200, 900)
                        background Solid("#fff6")
                        vbox:
                            text "Mouths" style "journal_text"
                            if paperdoll_test_mouth != "":
                                hbox:
                                    if paperdoll_test_mouth != "closed":
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_mouth", "closed"), Return()]
                                    else:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_mouth", "open"), Return()]
                                    if paperdoll_test_mouth != "open":
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_mouth", "open"), Return()]
                                    else:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_mouth", "closed"), Return()]
                            for mouth in ["closed", "open"]:
                                if mouth == paperdoll_test_mouth:
                                    textbutton mouth:
                                        text_style "buttons_active"
                                        action NullAction()
                                else:
                                    textbutton mouth:
                                        text_style "buttons_idle"
                                        action [SetVariable("paperdoll_test_mouth", mouth), Return()]

                if len(paperdoll_test_state_values) > 1:
                    frame:
                        area(0, 0, 200, 900)
                        background Solid("#fff6")
                        vbox:
                            text "States" style "journal_text"
                            if paperdoll_test_state != "":
                                hbox:
                                    if paperdoll_test_state_values.index(paperdoll_test_state) != 0:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_state", paperdoll_test_state_values[paperdoll_test_state_values.index(paperdoll_test_state) - 1]), Return()]
                                    else:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_state", paperdoll_test_state_values[len(paperdoll_test_state_values) - 1]), Return()]
                                    if paperdoll_test_state_values.index(paperdoll_test_state) != len(paperdoll_test_state_values) - 1:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_state", paperdoll_test_state_values[paperdoll_test_state_values.index(paperdoll_test_state) + 1]), Return()]
                                    else:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_state", paperdoll_test_state_values[0]), Return()]
                            viewport id "paperdoll_selector_states":
                                mousewheel True
                                draggable "touch"
                                vbox:
                                    for state in paperdoll_test_state_values:
                                        if state == paperdoll_test_state:
                                            textbutton state:
                                                text_style "buttons_active"
                                                action NullAction()
                                        else:
                                            textbutton state:
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_state", state), Return()]
                            vbar value YScrollValue("paperdoll_selector_states"):
                                unscrollable "hide"
                                xalign 1.05



        hbox:
            textbutton "^":
                text_style "buttons_idle"
                action [SetVariable("paperdoll_show_values", not paperdoll_show_values), Return()]
            if paperdoll_show_values:
                for label, key in [("AlignX", "paperdoll_alignX"), ("AlignY", "paperdoll_alignY"), ("Zoom", "paperdoll_zoom"), ("Blur", "paperdoll_blur")]:
                    textbutton "[label]":
                        text_style "buttons_idle"
                        if paperdoll_active_field == key:
                            text_color "#0f0"
                        action [SetVariable("paperdoll_active_preset", None), SetVariable("paperdoll_active_field", key)]
                    null width 10

                textbutton f"Flip: {paperdoll_flip}":
                    text_style "buttons_idle"
                    action [SetVariable("paperdoll_active_preset", None), SetVariable("paperdoll_flip", not paperdoll_flip), Return()]

        if paperdoll_active_field and paperdoll_show_values:
            hbox:
                text "Edit {}: ".format(paperdoll_active_field)
                input id paperdoll_active_field:
                    value DictInputValue(paperdoll_buf, paperdoll_active_field)
                    length 6
                null width 10
                textbutton "OK":
                    text_style "buttons_idle"
                    action [SetVariable("paperdoll_active_preset", None), Function(paperdoll_apply_buffers), Return()]

        hbox:
            textbutton "^":
                text_style "buttons_idle"
                action [SetVariable("paperdoll_show_presets", not paperdoll_show_presets), Return()]
            if paperdoll_show_presets:
                frame:
                    area (0, 0, 1700, 60)
                    background Solid("#fff6")
                    vbox:
                        viewport id "paperdoll_selector_presets":
                            mousewheel "horizontal"
                            draggable "touch"
                            hbox:
                                if paperdoll_active_preset is None:
                                    textbutton "custom":
                                        text_style "buttons_active"
                                        action NullAction()
                                else:
                                    textbutton "custom":
                                        text_style "buttons_idle"
                                        action [Function(paperdoll_clear_preset), Return()]
                                for preset_key in sorted(paperdoll_presets.keys()):
                                    if preset_key == paperdoll_active_preset:
                                        textbutton preset_key:
                                            text_style "buttons_active"
                                            action NullAction()
                                    else:
                                        textbutton preset_key:
                                            text_style "buttons_idle"
                                            action [Function(paperdoll_sync_preset_to_test_state, preset_key), Return()]
                        bar value XScrollValue("paperdoll_selector_presets"):
                            unscrollable "hide"

    imagebutton:
        idle "icons/stop_idle.webp"
        hover "icons/stop_hover.webp"
        xalign 1.0 yalign 1.0
        action Call("end_paperdoll_test")

init python:
    # Puffer-Strings für die Eingabe
    paperdoll_buf = {}

    def paperdoll_sync_buffers():
        """Aktuelle Float-Werte in die String-Puffer kopieren."""
        paperdoll_buf["paperdoll_alignX"] = str(paperdoll_alignX)
        paperdoll_buf["paperdoll_alignY"] = str(paperdoll_alignY)
        paperdoll_buf["paperdoll_zoom"] = str(paperdoll_zoom)
        paperdoll_buf["paperdoll_blur"] = str(paperdoll_blur)

    def paperdoll_apply_buffers():
        """Puffer-Strings zurück in Float-Variablen schreiben."""
        global paperdoll_alignX, paperdoll_alignY, paperdoll_zoom, paperdoll_blur
        try:
            paperdoll_alignX = float(paperdoll_buf["paperdoll_alignX"])
        except ValueError:
            pass
        try:
            paperdoll_alignY = float(paperdoll_buf["paperdoll_alignY"])
        except ValueError:
            pass
        try:
            paperdoll_zoom = float(paperdoll_buf["paperdoll_zoom"])
        except ValueError:
            pass
        try:
            paperdoll_blur = float(paperdoll_buf["paperdoll_blur"])
        except ValueError:
            pass

    def paperdoll_get_test_pd_obj():
        """
        Returns the active paperdoll object for the current test character, if available.

        ### Returns:
        1. Optional[Paperdoll_Obj]
            - The paperdoll object, or None when it is not registered yet.
        """
        if charact is None or paperdoll_manager is None or paperdoll_test_character == "":
            return None
        try:
            return paperdoll_manager.get_obj(paperdoll_test_character)
        except Exception:
            return None

    class _PaperdollConfigProxy(object):
        """Minimal stand-in for Paperdoll_Obj.config resolution during preset preview."""

        def __init__(self, alignX, alignY, zoom, blur):
            self.config = {
                "alignX": alignX,
                "alignY": alignY,
                "zoom": zoom,
                "blur": blur,
            }

    def paperdoll_flatten_preset(preset_key, **overrides):
        """
        Expands a preset into a flat action list, recursively resolving nested presets.

        ### Parameters:
        1. preset_key: str
            - The preset key to flatten.
        2. **overrides
            - Optional override values passed to nested preset actions.

        ### Returns:
        1. List[PDAction]
            - Flat list of non-preset actions in execution order.
        """
        result = []
        for action in get_preset_with_overrides(preset_key, **overrides):
            if action.key == "preset":
                result.extend(paperdoll_flatten_preset(action.preset, **action.values))
            else:
                result.append(action)
        return result

    def paperdoll_format_preset_actions(preset_key):
        """
        Formats the flattened preset actions as a comma-separated string for UI display.

        ### Parameters:
        1. preset_key: str
            - The preset key to format.

        ### Returns:
        1. str
            - Comma-separated action keys, e.g. "move, blur, flip".
        """
        return ", ".join(action.key for action in paperdoll_flatten_preset(preset_key))

    def paperdoll_apply_action_to_test_state(action, alignX, alignY, zoom, blur, flip, config_proxy):
        """
        Applies a single paperdoll action to simulated test state values.

        ### Parameters:
        1. action: PDAction
            - The action to apply.
        2. alignX: float
            - Current alignX value.
        3. alignY: float
            - Current alignY value.
        4. zoom: float
            - Current zoom value.
        5. blur: float
            - Current blur value.
        6. flip: bool
            - Current flip value.
        7. config_proxy: _PaperdollConfigProxy
            - Config proxy used for partial action resolution.

        ### Returns:
        1. Tuple[float, float, float, float, bool]
            - Updated alignX, alignY, zoom, blur and flip values.
        """
        if action.key == "move":
            alignX, alignY, zoom, _ = action.get_values(config_proxy)
            config_proxy.config["alignX"] = alignX
            config_proxy.config["alignY"] = alignY
            config_proxy.config["zoom"] = zoom
        elif action.key == "blur":
            blur, _ = action.get_values(config_proxy)
            config_proxy.config["blur"] = blur
        elif action.key == "flip":
            flip = action.flip < 0

        return alignX, alignY, zoom, blur, flip

    def paperdoll_sync_preset_to_test_state(preset_key=None):
        """
        Selects a preset and syncs editable test fields from its resolved actions.

        Move, blur and flip values are simulated sequentially, matching run_paperdoll_actions.
        Other action types remain part of the preset and are shown in the UI, but have no editable field.

        ### Parameters:
        1. preset_key: Optional[str]
            - Preset key to activate. When omitted, re-syncs the currently active preset.
        """
        global paperdoll_active_preset, paperdoll_alignX, paperdoll_alignY, paperdoll_zoom, paperdoll_blur, paperdoll_flip
        if preset_key is not None:
            paperdoll_active_preset = preset_key
        if paperdoll_active_preset is None:
            return

        pd_obj = paperdoll_get_test_pd_obj()
        if pd_obj is not None:
            alignX = pd_obj.config["alignX"]
            alignY = pd_obj.config["alignY"]
            zoom = pd_obj.config["zoom"]
            blur = pd_obj.config["blur"]
        else:
            alignX = paperdoll_alignX
            alignY = paperdoll_alignY
            zoom = paperdoll_zoom
            blur = paperdoll_blur

        flip = paperdoll_flip
        config_proxy = _PaperdollConfigProxy(alignX, alignY, zoom, blur)

        for action in paperdoll_flatten_preset(paperdoll_active_preset):
            alignX, alignY, zoom, blur, flip = paperdoll_apply_action_to_test_state(
                action, alignX, alignY, zoom, blur, flip, config_proxy
            )

        paperdoll_alignX = alignX
        paperdoll_alignY = alignY
        paperdoll_zoom = zoom
        paperdoll_blur = blur
        paperdoll_flip = flip
        paperdoll_sync_buffers()

    def paperdoll_build_test_display_actions():
        """
        Builds the paperdoll action list for the current test screen state.

        ### Returns:
        1. List[PDAction]
            - Actions passed to Person.display for the current test configuration.
        """
        image_action = PDAImage(
            char_var = paperdoll_test_char_var,
            pose = paperdoll_test_pose,
            outfit = paperdoll_test_outfit,
            level = paperdoll_test_level,
            state = paperdoll_test_state,
            mood = paperdoll_test_emotion,
            mouth = paperdoll_test_mouth,
        )

        if paperdoll_active_preset is not None:
            return [image_action, PDAPreset(paperdoll_active_preset)]

        return [
            image_action,
            PDAMove(alignX = paperdoll_alignX, alignY = paperdoll_alignY, zoom = paperdoll_zoom),
            PDABlur(blur = paperdoll_blur),
            PDAFlip(flip = paperdoll_flip),
        ]

    def paperdoll_clear_preset():
        """Clears the active preset selection without changing the current move values."""
        global paperdoll_active_preset
        paperdoll_active_preset = None

label end_paperdoll_test():
    $ unload_paperdoll_manager()
    $ hide_all()
    jump map_entry


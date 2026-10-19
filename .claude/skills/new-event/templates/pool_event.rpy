# TEMPLATE: building/pool event with selectors, paperdoll hand-off and a gated decision menu.
# Replace my_event / pool / paths / people. Delete the blocks you don't need.

init 1 python:
    set_current_mod('base')

    cafeteria_events["look_around"].add_event(Event(
        3,                                              # 1 blocking · 2 always · 3 random ambient
        "my_event",                                     # == label name below
        TimeCondition(weekday="d", daytime="f"),        # free time on workdays
        LevelCondition("2-4", char_obj="school"),       # climate gate (char goes in char_obj=)
        # Variety: rolled once per run, readable via get_value and as <topic> in paths.
        RandomListSelector("topic", "the vending machine", "the new menu", "the broken clock"),
        # Readings used for gated choices / reactive lines (gallery-registered).
        StatSelector("charm", CHARM, "school", [20, 100]),
        GameDataSelector("met_before", "my_event_met", 0),
        ReplayCategoryOption("my_storyline"),
        Pattern("main", "images/events/cafeteria/my_event/my_event <school_level> <step>.webp"),
        thumbnail = "images/events/cafeteria/my_event/my_event 2 1.webp",
        title = "My Event"))

# region SCENE · my_event ══════════════════════════════════════════════════════
#  One paragraph: where we are, who is there, what happens, what the beat is for.

label my_event (**kwargs):
    $ begin_event(**kwargs)

    $ topic = get_value("topic", **kwargs)
    $ met_before = get_value("met_before", **kwargs)
    $ high_charm = get_stat_value("charm", [20, 100], **kwargs) >= 20
    $ miwa = Person["miwa_igarashi"]

    # Establishing beat on the rendered still.
    $ image = convert_pattern("main", **kwargs)
    $ image.show(0)
    subtitles "Narration that sets the scene."
    headmaster.think "The headmaster's take on it."

    # Hand-off to conversation: blurred still behind a live paperdoll.
    $ miwa.register_paperdoll()
    $ paperdoll_manager.set_background(image[0], blur = True, **kwargs)
    $ miwa.display(PDAImage(pose = "1", outfit = "uniform", level = 2, mood = "neutral", mouth = "open"),
        PDAPreset("close_body_center", duration = 0.4))
    if met_before:
        miwa.say "Oh — you again."
    else:
        miwa.say "Can I help you with something?"

    $ miwa.display(PDAImage(mouth = "closed"), PDAMove(alignX = -0.2, duration = 1.0))
    $ call_custom_menu_with_text("What do you say?", character.subtitles, False,
        MenuElement("ask",   "Ask about [topic]",       EventEffect("my_event.ask")),
        MenuElement("charm", "Make her laugh",          EventEffect("my_event.charm"), high_charm),
        MenuElement("leave", "Leave her to it",         EventEffect("my_event.leave")),
        menu_anchor = MENU_ANCHOR_MIDDLE_RIGHT,
    **kwargs)

label .ask (**kwargs):
    $ miwa.display(PDAMove(alignX = 0.5, duration = 1.0), PDAImage(mood = "happy", mouth = "open"))
    miwa.say "Branch dialogue."
    $ set_game_data("my_event_met", 1)
    call change_stats_with_modifier(happiness=TINY) from _my_event_ask
    $ end_event("new_daytime", **kwargs)

label .charm (**kwargs):
    $ miwa.display(PDAMove(alignX = 0.5, duration = 1.0), PDAImage(mood = "shining", mouth = "open"))
    miwa.say "Branch dialogue."
    $ set_game_data("my_event_met", 1)
    call change_stats_with_modifier(happiness=SMALL, charm=TINY) from _my_event_charm
    $ end_event("new_daytime", **kwargs)

label .leave (**kwargs):
    $ image.show(1)
    subtitles "You leave her to it."
    $ end_event("new_daytime", **kwargs)

# endregion ═════════════════════════════════════════════════════════════════════

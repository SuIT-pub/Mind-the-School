# TEMPLATE: select / routing event — one map action opens a sub-menu whose options are
# other EventStorages. No scene label: the runner is select_event_runner. The select is
# available only if at least one of its storages has an available event, and each event
# inside those storages is a normal Event (with its own label, conditions and flags).

init 1 python:
    set_current_mod('base')

    my_left_events = EventStorage("my_left", "school_dormitory", fallback_text = "Nobody's there.")
    my_right_events = EventStorage("my_right", "school_dormitory", fallback_text = "Nobody's there.")

    sd_events["peek_students"].add_event(EventSelect(3, "my_room_select", "Which room do you check?",
        {"left": my_left_events, "right": my_right_events},
        TimeCondition(daytime="n"),
        override_menu_exit = "map_entry",
        person = character.subtitles,
        title = "Pick a Room"))

    # Fill the storages with ordinary events (see pool_event.rpy for the scene side):
    # my_left_events.add_event(Event(3, "my_left_scene", ...))

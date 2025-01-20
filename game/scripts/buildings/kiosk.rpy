####################################
# region Kiosk Event Handler ----- #
####################################

init -1 python:
    set_current_mod('base')
    
    kiosk_timed_event = TempEventStorage("kiosk_timed", "kiosk", fallback = Event(2, "kiosk.after_time_check"))
    kiosk_general_event = EventStorage("kiosk_general", "kiosk", fallback = Event(2, "kiosk.after_general_check"))
    register_highlighting(kiosk_timed_event, kiosk_general_event)

    kiosk_events = {}
    add_storage(kiosk_events, EventStorage("get_snack",    "kiosk", fallback_text = "I don't want anything."))

    kiosk_bg_images = BGStorage("images/background/kiosk/c.webp",
        BGImage("images/background/kiosk/<school_level> <variant> <nude>.webp", 1, OR(TimeCondition(daytime = "f"), TimeCondition(daytime = "c", weekday = "w"))), # show kiosk with students
        BGImage("images/background/kiosk/n.webp", 1, TimeCondition(daytime = 7)), # show kiosk at night empty
    )

init 1 python:
    set_current_mod('base')

    kiosk_event1 = Event(3, "kiosk_event_1",
        LevelSelector('school_level', 'school'),
        RandomValueSelector("variant", 1, 2),
        RandomListSelector("girl_name", "aona_komuro", "ikushi_ito", "gloria_goto", "lin_kato"),
        OR(TimeCondition(weekday = "d", daytime = "1,3"), TimeCondition(weekday="w", daytime = "4-")),
        Pattern("main", "images/events/kiosk/kiosk_event_1/kiosk_event_1 <girl_name> <school_level> <variant>.webp"),
        thumbnail = "images/events/kiosk/kiosk_event_1/kiosk_event_1 aona_komuro 1 1.webp")

    kiosk_event2 = Event(3, "kiosk_event_2",
        LevelSelector('school_level', 'school'),
        RandomListSelector("girl_name", "hatano_miwa", "kokoro_nakamura", "soyoon_yamamoto"),
        OR(TimeCondition(weekday = "d", daytime = "f"), TimeCondition(weekday="w", daytime = "d")),
        Pattern("main", "images/events/kiosk/kiosk_event_2/kiosk_event_2 <girl_name> <school_level> <step>.webp"),
        thumbnail = "images/events/kiosk/kiosk_event_2/kiosk_event_2 hatano_miwa 1 0.webp")

    kiosk_event3 = Event(3, "kiosk_event_3",
        LevelSelector('school_level', 'school'),
        RandomListSelector("topic", "normal", (0.25, "kind"), (0.05, "slimy")),
        OR(TimeCondition(weekday = "d", daytime = "f"), TimeCondition(weekday="w", daytime = "d")),
        NOT(BuildingCondition("cafeteria")),
        RandomCondition(65, 100),
        LevelCondition("4-", "school"),
        Pattern("main", "images/events/kiosk/kiosk_event_3/kiosk_event_3 <school_level> <step>.webp"),
        thumbnail = "images/events/kiosk/kiosk_event_3/kiosk_event_3 1 0.webp")

    kiosk_events["get_snack"].add_event(
        kiosk_event1, 
        kiosk_event2, 
        kiosk_event3,
    )

# endregion
####################################

##################################
# region Kiosk Entry Point ----- #
##################################

label kiosk ():
    call call_available_event(kiosk_timed_event) from kiosk_1

label .after_time_check (**kwargs):
    call call_available_event(kiosk_general_event) from kiosk_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do at the Kiosk?", 
        kiosk_events, 
        default_fallback,
        character.subtitles,
        bg_image = kiosk_bg_images,
    ) from kiosk_3

    jump kiosk

# endregion
##################################

#############################
# region Kiosk Events ----- #
#############################

#########################
# region Regular Events #

label kiosk_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ variant = get_value("variant", **kwargs)
    $ girl_name = get_value("girl_name", **kwargs)


    $ show_pattern("main", **kwargs)
    subtitles "For some, coffee is the only way to save the day."

    call change_stats_with_modifier('school',
        happiness = SMALL) from _call_change_stats_with_modifier_32

    $ end_event('new_daytime', **kwargs)

label kiosk_event_2 (**kwargs):
    $ begin_event(**kwargs)

    $ get_value('school_level', **kwargs)
    $ girl_name = get_value("girl_name", **kwargs)

    $ girl = get_person("class_3a", girl_name).get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    girl "*AHHH*"
    $ image.show(1)
    subtitles "A girl seems to have spilt her drink down her blouse."
    $ image.show(2)
    subtitles "Luckily she doesn't notice her see-through blouse in all the excitement."

    call change_stats_with_modifier('school',
        happiness = DEC_TINY, inhibition = DEC_MEDIUM, corruption = TINY) from _call_change_stats_with_modifier_33

    $ end_event('new_daytime', **kwargs)

label kiosk_event_3 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    $ topic = get_value("topic", **kwargs)

    $ miwa = get_person("class_3a", "miwa_igarashi").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    miwa "Hi, I want a Bento!"
    $ image.show(1)
    vendor "Sure that makes 2.50$"
    $ image.show(2)
    miwa "2.50?! It has been only 1.50$ last week?"
    $ image.show(3)
    vendor "I'm sorry, but I can no longer afford to keep the prices so low."
    $ image.show(2)
    miwa "But I can't afford that!"

    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave alone", "kiosk_event_3.leave"),
        ("Help her out  ({color=#a00000}-50${/color})", "kiosk_event_3.help"), 
    **kwargs)
label .leave (**kwargs):
    
    $ begin_event(**kwargs)
    
    if topic == "slimy":
        $ image.show(4)
        vendor "You know what? I think I could help you."
        $ image.show(5)
        miwa "Really?"
        $ image.show(6)
        vendor "Yeah you could, you know have my Hot Dog."
        $ image.show(7)
        miwa "Your Hot Dog? What do you m..."
        $ image.show(8)
        miwa "Eeek! Pervert!"
        $ image.show(9)
        headmaster_thought "Mhh what kind of noise is that? Hmmm... I guess it's nothing serious."

        call change_stats_with_modifier('school',
            happiness = DEC_MEDIUM, charm = DEC_MEDIUM, reputation = DEC_SMALL) from _call_change_stats_with_modifier_34
        $ end_event('new_daytime', **kwargs)
        
    elif topic == "kind":
        $ image.show(10)
        vendor "I'm sorry to hear that... You know what? This one is on the house."
        $ image.show(11)
        miwa "Really? Thank you."
        $ image.show(12)
        headmaster_thought "Mhh, things are worse than I thought. I can't believe the students have to go hungry."
        headmaster_thought "I should think about doing something about that."

        $ update_quest("trigger", name = "kiosk_observe_kindness")

        call change_stats_with_modifier('school',
            happiness = SMALL, charm = TINY) from _call_change_stats_with_modifier_35
    
        if get_progress("unlock_cafeteria") == -1:
            $ start_progress("unlock_cafeteria")
            $ add_notify_message("Added new building to journal!")

        $ end_event('new_daytime', **kwargs)
    else:
        $ image.show(10)
        vendor "I'm sorry but there is nothing I can do."
        $ image.show(13)
        miwa "*sob*"
        $ image.show(12)
        headmaster_thought "Poor girl..."

        call change_stats_with_modifier('school',
            happiness = DEC_TINY, charm = DEC_SMALL) from _call_change_stats_with_modifier_36
        $ end_event('new_daytime', **kwargs)
label .help (**kwargs):
    
    $ begin_event(**kwargs)
    
    $ image.show(14)
    headmaster "What's the matter here?"
    $ image.show(15)
    miwa "Oh Mr. [headmaster_last_name]... nothing..."
    $ image.show(16)
    headmaster "I'll pay her meal and please add a coffee."
    $ image.show(17)
    headmaster "Do you drink coffee?"
    miwa "Yes?"
    $ image.show(18)
    headmaster "Good, coffee then."
    vendor "Sure!"
    $ image.show(19)
    headmaster "Thank you!"
    $ image.show(20)
    miwa "Thank you very much!"
    $ image.show(21)
    headmaster "No problem. I know it can be hard, but if you are in a predicament just come talk to me and I'm sure we can find a way." 
    $ image.show(22)
    miwa "..."

    call change_money_with_modifier(-50) from _call_change_money_with_modifier_38

    call change_stats_with_modifier('school',
        happiness = MEDIUM, reputation = MEDIUM) from _call_change_stats_with_modifier_37
    jump new_daytime

# endregion
#########################

# endregion
#############################
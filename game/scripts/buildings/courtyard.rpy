#######################################
# ----- Courtyard Event Handler ----- #
#######################################

init -1 python:
    courtyard_timed_event = EventStorage("courtyard", "", Event(2, "courtyard.after_time_check"))
    courtyard_events = {
        "talk_student": EventStorage("talk_student", "Talk with students", default_fallback, "There is nobody here."),
        "talk_teacher": EventStorage("talk_teacher", "Talk with teacher",  default_fallback, "There is nobody here."),
        "patrol":       EventStorage("patrol",       "Patrol",             default_fallback, "There is nobody here."),
    }
    
    courtyard_timed_event.add_event(Event(1,
        ["first_week_courtyard_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))
    
    courtyard_timed_event.add_event(Event(1,
        ["first_potion_courtyard_event"],
        TimeCondition(day = 9, month = 1, year = 2023),
    ))

    courtyard_events["patrol"].add_event(Event(3, 
        ["courtyard_event_1", "courtyard_event_2"],
        OR(TimeCondition(daytime = "f", weekday = "d"), TimeCondition(daytime = "d", weekday = "w"))
    ))

    courtyard_events["patrol"].add_event(Event(3, 
        ["courtyard_event_3"],
        TimeCondition(daytime = "d"),
    ))

    courtyard_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), courtyard_events.values())

    courtyard_bg_images = [
        BGImage("images/background/courtyard/bg 1,6 <name> <level> <nude>.webp", 1, OR(TimeCondition(daytime = "1,6", weekday = "w"), TimeCondition(daytime = "c", weekday = "d"))), # show courtyard with a few students
        BGImage("images/background/courtyard/bg 3 <name> <level> <nude>.webp", 1, TimeCondition(daytime = 3)), # show courtyard full of students and teacher
        BGImage("images/background/courtyard/bg 7.webp", 1, TimeCondition(daytime = 7)), # show empty courtyard at night
    ]
    
#######################################

#####################################
# ----- Courtyard Entry Point ----- #
#####################################

label courtyard ():

    call call_available_event(courtyard_timed_event) from courtyard_1

label .after_time_check (**kwargs):

    $ school_obj = get_random_school()

    call show_idle_image(school_obj, "images/background/courtyard/bg c.webp", courtyard_bg_images) from courtyard_2

    call call_event_menu (
        "What to do at the Courtyard?", 
        courtyard_events, 
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
        fallback_text = "There is nothing to see here."
    ) from courtyard_3

    jump courtyard

#####################################

################################
# ----- Courtyard Events ----- #
################################

label first_potion_courtyard_event (**kwargs):

    show first potion courtyard 1 with dissolveM
    subtitles "You walk around in the courtyard."

    show first potion courtyard 2 with dissolveM
    subtitles "The first thing you notice is the group of students sunbathing in the middle of the yard."
    
    show first potion courtyard 3 with dissolveM
    subtitles "Normally that wouldn't be such a weird thing, if they weren't in only their underwear."
    headmaster_thought "I certainly enjoy the view. Unfortunately it only lasts for today until the serum finishes settling in their bodies."

    $ set_building_blocked("courtyard")

    jump new_daytime

# first week event
label first_week_courtyard_event (**kwargs):
    show first week courtyard 1 with dissolveM
    subtitles "You walk through the courtyard."

    headmaster_thought "Hmm, the courtyard looks really bad..."
    
    show first week courtyard 2 with dissolveM
    headmaster_thought "Tt seems most of the appliances here are out of order."

    show first week courtyard 3 with dissolveM
    headmaster_thought "For example the public toilet is broken."

    show first week courtyard 4 with dissolveM
    headmaster_thought "At least the courtyard doesn't need immediate fixing."

    $ change_stat_for_all("happiness", 5, charList["schools"])

    $ set_building_blocked("courtyard")

    jump new_day

# TODO: modify for Level 4+
label courtyard_event_1 (**kwargs):
    $ variant = get_random_int(1, 1)

    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ name = "high_school"

    $ image = Image_Series("images/events/courtyard/courtyard_event_1 <name> <level> <variant> <step>.webp", name = name, variant = variant, **kwargs)

    $ begin_event("courtyard_event_1")

    $ image.show(0)
    subtitles "You walk along the courtyard when a gist of wind blows up the girls skirt in front of you."
    $ call_custom_menu_with_text("How do you react?", character.subtitles, False,
        ("Look", "courtyard_event_1.look"),
        ("Look away", "courtyard_event_1.look_away"),
    **kwargs)

label .look (**kwargs):
    $ image.show(1)
    subtitles "You take the chance to stare directly ahead and burn that image into your brain and retina."
    $ image.show(2)
    subtitles "The girl looks at you, screams, covers herself and runs away."
    $ image.show(3)
    sgirl "PERVERT!"

    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = DEC_SMALL, reputation = DEC_TINY, inhibition = DEC_SMALL)
    jump new_daytime

label .look_away (**kwargs):
    $ image.show(4)
    subtitles "You quickly look away, but the image is already burned into your brain."
    $ image.show(5)
    subtitles "The girl looks at you ashamed of the situation and runs away. Glad you didn't stare."

    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = TINY, reputation = TINY, inhibition = DEC_TINY)
    jump new_daytime

# TODO: make images
label courtyard_event_2 (**kwargs):
    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ name = "high_school"

    $ image = Image_Series("images/events/courtyard/courtyard_event_2 <name> <level> <step>.webp", name = name, **kwargs)

    $ begin_event("courtyard_event_2")

    $ image.show(0)
    subtitles "You notice a girl sitting alone in the courtyard, apparently left out by the others."
    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Talk to her", "courtyard_event_2.talk"),
        ("Leave her alone", "courtyard_event_2.leave"),
    **kwargs)

label .talk (**kwargs):
    $ image.show(2)
    headmaster "Hey, are you alright?"
    $ image.show(3)
    sgirl "Oh, hi. I'm fine, just a bit tired."
    $ image.show(4)
    headmaster "You look a bit lonely. Why don't you join the others?"
    $ image.show(5)
    sgirl "I don't really like them. They are all so... shallow."
    $ image.show(6)
    headmaster "I see. Well, I'm sure you'll find some friends eventually."
    $ image.show(7)
    sgirl "..."
    $ image.show(8)
    headmaster "If you need anything, just ask me. See you later."
    $ image.show(9)
    sgirl "Thanks, bye."
    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = DEC_TINY, reputation = TINY)
    jump new_daytime

label .leave (**kwargs):
    $ image.show(1)
    subtitles "You decide to leave her alone."
    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = DEC_MEDIUM, reputation = DEC_SMALL)
    jump new_daytime

label courtyard_event_3 (**kwargs):
    $ begin_event("courtyard_event_3")
    
    call show_image ("images/events/courtyard/courtyard_event_3 <name> <level>.webp", name = "high_school", **kwargs) from _call_show_image
    subtitles "You notice a group of girls taking a break together."

    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = SMALL, happiness = TINY, education = TINY, reputation = SMALL)
    jump new_daytime

################################
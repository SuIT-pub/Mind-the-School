#######################################
# ----- Courtyard Event Handler ----- #
#######################################

init -1 python:
    courtyard_timed_event = TempEventStorage("courtyard_timed", "courtyard", Event(2, "courtyard.after_time_check"))
    courtyard_general_event = EventStorage("courtyard_general", "courtyard", Event(2, "courtyard.after_general_check"))
    courtyard_events = {
        "patrol":       EventStorage("patrol", "courtyard", default_fallback, "There is nobody here."),
    }

    courtyard_bg_images = [
        BGImage("images/background/courtyard/bg 1,6 <loli> <school_level> <nude>.webp", 1, OR(TimeCondition(daytime = "1,6", weekday = "w"), TimeCondition(daytime = "f", weekday = "d"))), # show courtyard with a few students
        BGImage("images/background/courtyard/bg 3 <loli> <school_level> <nude>.webp", 1, TimeCondition(daytime = 3)), # show courtyard full of students and teacher
        BGImage("images/background/courtyard/bg 7.webp", 1, TimeCondition(daytime = 7)), # show empty courtyard at night
    ]    

init 1 python:
    first_week_courtyard_event_event = Event(1, "first_week_courtyard_event",
        TimeCondition(day = "2-4", month = 1, year = 2023),
        thumbnail = "images/events/first week/first week courtyard 1.webp")
    
    first_potion_courtyard_event_event = Event(1, "first_potion_courtyard_event",
        TimeCondition(day = 9, month = 1, year = 2023),
        thumbnail = "images/events/first potion/first potion courtyard 1.webp")

    courtyard_event1 = Event(3, "courtyard_event_1",
        RandomValueSelector('variant', 1, 1),
        OR(TimeCondition(daytime = "f", weekday = "d"), TimeCondition(daytime = "d", weekday = "w")),
        thumbnail = "images/events/courtyard/courtyard_event_1 1 1 0.webp")

    courtyard_event2 = Event(3, "courtyard_event_2",
        OR(TimeCondition(daytime = "f", weekday = "d"), TimeCondition(daytime = "d", weekday = "w")),
        thumbnail = "images/events/courtyard/courtyard_event_2 1 0.webp")

    courtyard_event3 = Event(3, "courtyard_event_3",
        TimeCondition(daytime = "d"),
        thumbnail = "images/events/courtyard/courtyard_event_3 1.webp")

    courtyard_event4 = Event(3, "courtyard_event_4",
        OR(TimeCondition(weekday = "d", daytime = "f"),
            TimeCondition(weekday = "w", daytime = "d")),
        RandomListSelector('girl_name', "Gloria Goto", "Sakura Mori", "Ikushi Ito", "Ishimaru Maki",
            (
                RandomListSelector('', 'Luna Clark', 'Hiroshi Suzuki', 'Miela Frejadottir', 'Sofia Harada', 'Thanchanok Cooper'),
                LoliContentCondition("1+")
            )),
        thumbnail = "images/events/courtyard/courtyard_event_4 1.webp")

    courtyard_event5 = Event(3, "courtyard_event_5",
        OR(TimeCondition(weekday = "d", daytime = "f"),
            TimeCondition(weekday = "w", daytime = "d")),
        thumbnail = "images/events/courtyard/courtyard_event_5 1.webp")

    courtyard_event6 = Event(3, "courtyard_event_6",
        TimeCondition(weekday = "d", daytime = "2,4"),
        thumbnail = "images/events/courtyard/courtyard_event_6 1.webp")

    courtyard_timed_event.add_event(
        first_week_courtyard_event_event,
        first_potion_courtyard_event_event,
    )

    courtyard_events["patrol"].add_event(
        courtyard_event1, 
        courtyard_event2, 
        courtyard_event3,
        courtyard_event4,
        courtyard_event5,
        courtyard_event6,
    )

#######################################

#####################################
# ----- Courtyard Entry Point ----- #
#####################################

label courtyard ():
    call call_available_event(courtyard_timed_event) from courtyard_1

label .after_time_check (**kwargs):
    call call_available_event(courtyard_general_event) from courtyard_4

label .after_general_check (**kwargs):
    $ loli = get_random_loli()

    call show_idle_image("images/background/courtyard/bg c.webp", courtyard_bg_images, 
        loli = loli
    ) from courtyard_2

    call call_event_menu (
        "What to do at the Courtyard?", 
        courtyard_events, 
        default_fallback,
        character.subtitles,
        context = loli,
        fallback_text = "There is nothing to see here."
    ) from courtyard_3

    jump courtyard

#####################################

################################
# ----- Courtyard Events ----- #
################################

label first_potion_courtyard_event (**kwargs):
    $ begin_event(**kwargs)
    
    show first potion courtyard 1 with dissolveM
    subtitles "You walk around in the courtyard."

    show first potion courtyard 2 with dissolveM
    subtitles "The first thing you notice is the group of students sunbathing in the middle of the yard."
    
    show first potion courtyard 3 with dissolveM
    subtitles "Normally that wouldn't be such a weird thing, if they weren't in only their underwear."
    headmaster_thought "I certainly enjoy the view. Unfortunately it only lasts for today until the serum finishes settling in their bodies."

    $ set_building_blocked("courtyard")

    $ end_event("new_daytime", **kwargs)

# first week event
label first_week_courtyard_event (**kwargs):
    $ begin_event(**kwargs)
    
    show first week courtyard 1 with dissolveM
    subtitles "You walk through the courtyard."

    headmaster_thought "Hmm, the courtyard looks really bad..."
    
    show first week courtyard 2 with dissolveM
    headmaster_thought "Tt seems most of the appliances here are out of order."

    show first week courtyard 3 with dissolveM
    headmaster_thought "For example the public toilet is broken."

    show first week courtyard 4 with dissolveM
    headmaster_thought "At least the courtyard doesn't need immediate fixing."

    $ change_stat("happiness", 5, get_school())

    $ set_building_blocked("courtyard")

    $ end_event("new_day", **kwargs)

# TODO: modify for Level 4+
label courtyard_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)

    $ image = Image_Series("images/events/courtyard/courtyard_event_1 <school_level> 1 <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "You walk along the courtyard when a gist of wind blows up the girls skirt in front of you."
    $ call_custom_menu_with_text("How do you react?", character.subtitles, False,
        ("Look", "courtyard_event_1.look"),
        ("Look away", "courtyard_event_1.look_away"),
    **kwargs)
label .look (**kwargs):
    $ begin_event()
    
    $ image.show(1)
    subtitles "You take the chance to stare directly ahead and burn that image into your brain and retina."
    $ image.show(2)
    subtitles "The girl looks at you, screams, covers herself and runs away."
    $ image.show(3)
    sgirl "PERVERT!"

    $ change_stats_with_modifier(school_obj,
        happiness = DEC_SMALL, reputation = DEC_TINY, inhibition = DEC_SMALL)
    
    $ end_event("new_daytime", **kwargs)
label .look_away (**kwargs):
    
    $ begin_event()
    
    $ image.show(4)
    subtitles "You quickly look away, but the image is already burned into your brain."
    $ image.show(5)
    subtitles "The girl looks at you ashamed of the situation and runs away. Glad you didn't stare."

    $ change_stats_with_modifier(school_obj,
        happiness = TINY, reputation = TINY, inhibition = DEC_TINY)
    
    $ end_event("new_daytime", **kwargs)

# TODO: make images
label courtyard_event_2 (**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)

    $ image = Image_Series("images/events/courtyard/courtyard_event_2 <school_level> <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "You notice a girl sitting alone in the courtyard, apparently left out by the others."
    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Talk to her", "courtyard_event_2.talk"),
        ("Leave her alone", "courtyard_event_2.leave"),
    **kwargs)
label .talk (**kwargs):
    
    $ begin_event()
    
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
    
    $ change_stats_with_modifier(school_obj,
        happiness = DEC_TINY, reputation = TINY)
    $ end_event("new_daytime", **kwargs)
label .leave (**kwargs):
    
    $ begin_event()
    
    $ image.show(1)
    subtitles "You decide to leave her alone."
    
    $ change_stats_with_modifier(school_obj,
        happiness = DEC_MEDIUM, reputation = DEC_SMALL)
    $ end_event("new_daytime", **kwargs)

label courtyard_event_3 (**kwargs):
    $ begin_event(**kwargs)
    
    $ school_obj = get_char_value('school_obj', **kwargs)
    
    call show_image ("images/events/courtyard/courtyard_event_3 <school_level>.webp", **kwargs) from _call_show_image
    subtitles "You notice a group of girls taking a break together."

    $ change_stats_with_modifier(school_obj,
        charm = SMALL, happiness = TINY, education = TINY, reputation = SMALL)
    
    $ end_event("new_daytime", **kwargs)

label courtyard_event_4(**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)
    $ girl_name = get_value("girl_name", **kwargs)

    # headmaster walks with umbrella
    # Student comes running towards him
    # Students runs past him, but headmaster gets a good view through the wet and see-through clothing
    headmaster "Interesting..."

    $ end_event("new_daytime", **kwargs)

label courtyard_event_5(**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)

    # headmaster walks by
    # students walk by talking with each other
    subtitles "You come across a group of students talking to each other."

    $ end_event("new_daytime", **kwargs)

label courtyard_event_6(**kwargs):
    $ begin_event(**kwargs)

    $ school_obj = get_char_value('school_obj', **kwargs)

    # headmaster approaches a student sitting on the courtyard
    headmaster "Excuse me, but what are you doing here?"
    # student looks up kinda surprised
    sgirl "I'm taking my break sir."
    # headmaster looking rather angry
    headmaster "Class already started. You should be in class."
    # student surprised
    sgirl "Really?!"
    # headmaster nods
    headmaster "Yes. Now run along and check the time next time so you don't arrive late!"
    # student runs off
    sgirl "Sorry!"

    $ end_event("new_daytime", **kwargs)

################################
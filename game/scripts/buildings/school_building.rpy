#############################################
# ----- School Building Event Handler ----- #
#############################################

init -1 python:
    sb_timed_event = TempEventStorage("sb", "", Event(2, "school_building.after_time_check"))
    sb_events = {
        "check_class": EventStorage("check_class", "Check Class",      default_fallback, "There is nobody here."),
        "teach_class": EventStorage("teach_class", "Teach a Class",    default_fallback, "There is nobody here."),
        "patrol":      EventStorage("patrol",      "Patrol building",  default_fallback, "There is nobody here."),
        "students":    EventStorage("students",    "Talk to students", default_fallback, "There is nobody here."),
    }

    sb_timed_event.add_event(Event(1,
        ["first_week_sb_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    sb_timed_event.add_event(Event(1,
        ["first_potion_sb_event"],
        TimeCondition(day = 9, month = 1, year = 2023),
    ))

    event1 = Event(3, 
        ["sb_event_1"],
        TimeCondition(daytime = "c", weekday = "d"),
    )

    sb_events["teach_class"].add_event(event1)
    sb_events["teach_class"].add_event(Event(3,
        ["sb_event_2"],
        TimeCondition(daytime = "c", weekday = "d"),
    ))
    
    sb_events["patrol"].add_event(event1)
    sb_events["patrol"].add_event(Event(3, 
        ["sb_event_3"], 
        TimeCondition(daytime = "d")
    ))



    sb_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), sb_events.values())

    sb_bg_images = [
        BGImage("images/background/school building/bg c <loli> <level> <nude>.webp", 1, TimeCondition(daytime = "c", weekday = "d")),
        BGImage("images/background/school building/bg 7.webp", 1, TimeCondition(daytime = 7)),
    ]

##################################################

###########################################
# ----- School Building Entry Point ----- #
###########################################

label school_building ():

    call call_available_event(sb_timed_event) from school_building_1

label .after_time_check (**kwargs):

    $ school_obj = get_character("school", charList)

    call show_idle_image(school_obj, "images/background/school building/bg f.webp", sb_bg_images,
        loli = get_random_loli()
    ) from school_building_2

    call call_event_menu (
        "What to do in the School?", 
        sb_events,
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from school_building_3

    jump school_building

################################################

######################################
# ----- School Building Events ----- #
######################################

# first week event
label first_week_sb_event (**kwargs):
    
    show first week high school building 1 with dissolveM
    subtitles """You enter the main building of the high school.
        
        Well, you don't really need to enter the building to get an idea of the state it's in."""
        
    show first week high school building 2 with dissolveM
    headmaster_thought """Despite my fear, the building seems to be rather well maintained.

        It could be a bit cleaner but the corridor seems rather well.

        Let's see the classrooms."""
    
    show first week high school building 3 with dissolveM
    headmaster_thought "Oh not bad as well. "

    show first week high school building 4 with dissolveM
    headmaster_thought "Hmm I think there should be a class right now, let's check."

    show first week high school building 6 with dissolveM
    headmaster_thought "Hmm looks like a normal class, but I think the students have no material?"
    headmaster_thought "Yeah, not one school girl has even one book."
    headmaster_thought "I guess the former headmaster cut back on those"

    $ change_stat("education", 5, 'school', charList)

    $ set_building_blocked("school_building")

    jump new_day

label first_potion_sb_event (**kwargs):

    show first potion high school building 1 with dissolveM
    headmaster_thought "Let's see how classes are today."
    
    show first potion high school building 2 with dissolveM
    subtitles "You look into a classroom and the first thing you notice is that almost everyone has opened up or at least partially removed their clothes."
    subtitles "Apparently the teachers also took a drink."
    headmaster_thought "Hmm, I can't wait to have this view on a regular basis, but that's gonna take some time."

    $ set_building_blocked("school_building")

    jump new_daytime

###########################################

###########################################
# ----- High School Building Scenes ----- #
###########################################


# TODO: make images
label sb_event_1 (**kwargs): # patrol, check class
    # show screen black_screen_text("sb_event_1")
    $ image = Image_Series("/images/events/school building/sb_event_1 <name> <step>.webp", **kwargs)

    $ begin_event()

    # call show_image("/images/events/school building/sb_event_1 <name> 1.webp", SCENE, **kwargs)
    $ image.show(0)
    subtitles "You walk through the corridors of the high school."

    # call show_image("/images/events/school building/sb_event_1 <name> 2.webp", SCENE, **kwargs)
    $ image.show(1)
    subtitles "You come across a couple making out in the hallway."

    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave and let them have fun", "sb_event_1.leave"),
        ("Stop them", "sb_event_1.stop", not is_rule_unlocked("student_student_relation")), 
    **kwargs)
label .leave (**kwargs):
    # show screen black_screen_text("sb_event_1.leave")
    $ image.show(2)
    # call show_image("/images/events/school building/sb_event_1 <name> 3.webp", SCENE, **kwargs)
    subtitles "You decide to leave them and let them have their fun."
    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = DEC_SMALL, education = TINY, corruption = TINY, inhibition = DEC_SMALL)
    jump new_daytime

label .stop (**kwargs):
    # show screen black_screen_text("sb_event_1.stop")
    $ image.show(3)
    # call show_image("/images/events/school building/sb_event_1 <name> 4.webp", SCENE, **kwargs)
    headmaster "Hey you! Stop that. You know that is against the rules!"
    sgirl "We're sorry!"
    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = MEDIUM, happiness = DEC_SMALL, education = SMALL, reputation = TINY, inhibition = DEC_TINY)
    jump new_daytime

# TODO: make images
label sb_event_2 (**kwargs): # teach class
    $ image = Image_Series("/images/events/school building/sb_event_2 <name> <step>.webp", **kwargs)

    $ begin_event()

    $ image.show(0)
    subtitles "A student tripped while handing out assignments in class."

    $ image.show(1)
    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave alone", "sb_event_2.leave"),
        ("Help her up", "sb_event_2.help"), 
    **kwargs)

label .leave (**kwargs):
    $ image.show(2)
    subtitles "You decide to leave her alone."
    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = DEC_TINY, education = TINY)
    jump new_daytime

label .help (**kwargs):
    $ image.show(3)
    subtitles "You help her up."
    $ change_stats_with_modifier(kwargs["char_obj"],
        charm = DEC_TINY, happiness = SMALL, education = TINY)
    jump new_daytime

# TODO: make images
label sb_event_3 (**kwargs): # patrol
    $ image = Image_Series("/images/events/school building/sb_event_3 <name> <step>.webp", **kwargs)

    $ begin_event()

    $ image.show(0) # walk with girl sitting
    subtitles "As you walk through the corridors of the high school, you notice a student sitting in the corner of the hallway."
    sgirl "*sniffle*"

    $ image.show(1) # stand next to her asking
    headmaster "Are you okay?"
    
    $ image.show(2) # girl answers without looking up
    sgirl "I'm fine. It's just... No I'm fine."

    $ call_custom_menu(False,
        ("What is going on?", "sb_event_3.what"),
        ("If it's nothing, go back to class", "sb_event_3.send_class", time.check_daytime("c") and time.check_weekday("d")), 
    **kwargs)

label .what (**kwargs):
    $ image.show(3) # headmaster sits next to her
    headmaster "What is going on? I can see there is something bothering you."

    $ image.show(4) # girl still doesn't look
    sgirl "I really don't want to talk about it. I'd like to be alone right now."

    $ image.show(5) # headmaster asks looking straight
    headmaster "Did someone do this to you?"

    $ image.show(6) # girl looks away, headmaster looks at her
    sgirl "..."

    $ call_custom_menu(False, 
        ("Leave her alone", "sb_event_3.leave"), 
        ("Get to the bottom of this", "sb_event_3.get_to_bottom"), 
    **kwargs)

label .leave (**kwargs):
    $ image.show(6)
    subtitles"You hesitate for a moment, but then decide to leave her alone."

    $ image.show(7) # headmaster stands up
    headmaster "Okay, I'll leave you alone."

    $ image.show(1) # headmaster stands next to her talking
    headmaster "But if you need anything, you can always come to me. My door is always open."

    $ image.show(2) # image 2 but with girl not talking
    sgirl "..."

    $ image.show(8) # headmaster stands a bit further away looking back to her
    subtitles"You walk away with a heavy heart."

    $ change_stats_with_modifier(kwargs["char_obj"], 
        charm = TINY, happiness = DEC_LARGE, education = TINY, reputation = DEC_TINY)
    jump new_daytime

label .get_to_bottom (**kwargs):
    $ image.show(3) # headmaster looks to girl
    headmaster "I really want to help you. Please tell me what is going on."

    $ image.show(10) # headmaster looks girl doesn't answer
    sgirl "..."
    
    $ image.show(9) # headmaster rests head against wall talking
    headmaster "Please listen."

    $ image.show(10) # headmaster rests head against wall talking
    sgirl "..."
    $ image.show(9) # headmaster rests head against wall talking
    headmaster "Whatever happened to you, if some someone did or said anything."

    $ image.show(11) # girl buries head deeper into arms
    sgirl "*sniffle*"
    subtitles "She slowly and silently starts crying."

    $ image.show(12) # headmaster looks to girl
    headmaster "Let's go to my office, shall we? There it is more private and nobody will bother us. You can then decide what you want to share. Is that okay?"

    $ image.show(13) # girl looks to headmaster
    sgirl "I- I... yes... thank-"

    $ image.show(14) # headmaster and girl walk to office
    subtitles "You support her back to your office and bring her something warm to drink."

    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = LARGE, reputation = TINY)
    jump new_daytime

label .send_class (**kwargs):
    $ image.show(15) # headmaster starts walking away
    headmaster "Then you better get back to class."

    $ image.show(16) # girl looks up
    sgirl "B- But... I..."

    $ image.show(17) # headmaster looks back
    headmaster "Yes?"

    $ image.show(18) # girl again buries head in arms
    sgirl "I d-don't..."

    $ call_custom_menu(False, 
        ("Poor thing", "sb_event_3.poor_thing"), 
        ("Chin up", "sb_event_3.chin_up"), 
    **kwargs)

label .poor_thing (**kwargs):

    $ image.show(19) # headmaster squats next to her
    headmaster "Look, maybe you should just take the day off. I'll notify your teacher."

    $ image.show(20) # girl looks to headmaster
    sgirl "Yes... thank you..."

    $ image.show(14) # headmaster helps girl up
    subtitles "You help her up and walk her to the dormitory."
    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = LARGE, reputation = TINY)
    jump new_daytime

label .chin_up (**kwargs):
    
    $ image.show(19) # headmaster squats next to her
    headmaster "Now, now, it can't be that bad. I'm sure whatever caused those tears will soon be forgotten."

    $ image.show(21) # girl says nothing
    sgirl "..."

    $ image.show(22) # headmaster stands up
    headmaster "Now, run along. Just tell the teachers you needed a breath of air. I'll take care of the rest."
    sgirl "Ok..."

    $ image.show(23) # girl walks away
    subtitles "You help her up and she walks off."
    $ change_stats_with_modifier(kwargs["char_obj"],
        happiness = LARGE, reputation = TINY)
    jump new_daytime

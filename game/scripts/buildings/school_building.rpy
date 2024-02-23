#############################################
# ----- School Building Event Handler ----- #
#############################################

init -1 python:
    sb_timed_event = TempEventStorage("school_building", "school_building", Event(2, "school_building.after_time_check"))
    sb_general_event = EventStorage("school_building", "school_building", Event(2, "school_building.after_general_check"))
    sb_events = {
        "check_class": EventStorage("check_class",  "school_building", default_fallback, "There is nobody here."),
        "teach_class": EventStorage("teach_class",  "school_building", default_fallback, "There is nobody here."),
        "patrol":      EventStorage("patrol",       "school_building", default_fallback, "There is nobody here."),
        "students":    EventStorage("talk_student", "school_building", default_fallback, "There is nobody here."),
    }
    sb_teach_events = {
        "english": EventStorage("english", "school_building", default_fallback, "There is nobody here."),
        "math":    EventStorage("math",    "school_building", default_fallback, "There is nobody here."),
    }

    sb_bg_images = [
        BGImage("images/background/school building/bg c <loli> <level> <nude>.webp", 1, TimeCondition(daytime = "c", weekday = "d")),
        BGImage("images/background/school building/bg 7.webp", 1, TimeCondition(daytime = 7)),
    ]

init 1 python:

    ####################
    # Event construction
    first_week_sb_event = Event(1, "first_week_sb_event",
        TimeCondition(day = "2-4", month = 1, year = 2023),
        thumbnail = "images/events/first week/first week school building 2.webp")

    first_potion_sb_event = Event(1, "first_potion_sb_event",
        TimeCondition(day = 9, month = 1, year = 2023),
        thumbnail = "images/events/first potion/first potion school building 1.webp")

    first_class_sb_event_event = Event(1, "first_class_sb_event",
        TimeCondition(weekday = "d", daytime = "c"),
        ProgressCondition('first_class', '2-'),
        RandomListSelector('class', 
            ('3A', NOT(GameDataCondition('first_class_3A', True))),
            (
                '2A', 
                AND(
                    NOT(GameDataCondition('first_class_2A', True)),
                    LoliContentCondition('1+')
                ),
            ),
            (
                '1A', 
                AND(
                    NOT(GameDataCondition('first_class_1A', True)),
                    LoliContentCondition('2')
                ),
            )
        ),
        thumbnail = "")

    sb_event1 = Event(3, "sb_event_1",
        TimeCondition(daytime = "c", weekday = "d"),
        thumbnail = "images/events/school building/sb_event_1 0.webp")

    sb_event2 = Event(3, "sb_event_2",
        TimeCondition(daytime = "c", weekday = "d"),
        thumbnail = "images/events/school building/sb_event_2 0.webp")
    
    sb_event3 = Event(3, "sb_event_3",
        TimeCondition(daytime = "d"),
        thumbnail = "images/events/school building/sb_event_3 0.webp")

    sb_event4 = Event(3, "sb_event_4",
        TimeCondition(weekday = "d", daytime = "f"),
        thumbnail = "images/events/school building/sb_event_4 0.webp")

    # Teaching events
    sb_event_teach_class_event = Event(3, "teach_class_event",
        TimeCondition(weekday = "d", daytime = "c"),
    )

    sb_teach_english_1_event = Event(3, "sb_teach_english_1")
    sb_teach_math_1_event = Event(3, "sb_teach_math_1")

    #################
    # Event insertion

    sb_timed_event.add_event(
        first_week_sb_event, 
        first_potion_sb_event,
    )

    sb_general_event.add_event(
    )

    sb_events["teach_class"].add_event(
        first_class_sb_event_event, 
        sb_event_teach_class_event,
    )
    sb_events["patrol"].add_event(
        sb_event1, 
        sb_event3,
        sb_event4,
    )

    sb_teach_events["english"].add_event(
        sb_teach_english_1_event,
        sb_event2,
    )
    sb_teach_events["math"].add_event(
        sb_teach_math_1_event,
        sb_event2,
    )

##################################################

###########################################
# ----- School Building Entry Point ----- #
###########################################

label school_building ():
    call call_available_event(sb_timed_event) from school_building_1
    
label .after_time_check (**kwargs):
    call call_available_event(sb_general_event) from school_building_4

label .after_general_check (**kwargs):
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

#####################
# Introduction Events

# first week event
label first_week_sb_event (**kwargs):
    $ begin_event(**kwargs)

    show first week school building 1 with dissolveM
    subtitles """You enter the main building of the high school.
        
        Well, you don't really need to enter the building to get an idea of the state it's in."""
        
    show first week school building 2 with dissolveM
    headmaster_thought """Despite my fear, the building seems to be rather well maintained.

        It could be a bit cleaner but the corridor seems rather well.

        Let's see the classrooms."""
    
    show first week school building 3 with dissolveM
    headmaster_thought "Oh not bad as well. "

    show first week school building 4 with dissolveM
    headmaster_thought "Hmm I think there should be a class right now, let's check."

    show first week school building 6 with dissolveM
    headmaster_thought "Hmm looks like a normal class, but I think the students have no material?"
    headmaster_thought "Yeah, not one school girl has even one book."
    headmaster_thought "I guess the former headmaster cut back on those"

    $ change_stat("education", 5, get_school())

    $ set_building_blocked("school_building")

    $ end_event('new_day', **kwargs)

label first_potion_sb_event (**kwargs):

    $ begin_event(**kwargs)
    
    show first potion school building 1 with dissolveM
    headmaster_thought "Let's see how classes are today."
    
    show first potion school building 2 with dissolveM
    subtitles "You look into a classroom and the first thing you notice is that almost everyone has opened up or at least partially removed their clothes."
    subtitles "Apparently the teachers also took a drink."
    headmaster_thought "Hmm, I can't wait to have this view on a regular basis, but that's gonna take some time."

    $ set_building_blocked("school_building")

    
    $ end_event('new_daytime', **kwargs)

label first_class_sb_event (**kwargs):
    $ begin_event(**kwargs)

    $ char_obj = set_char_value(get_school(), **kwargs)
    $ school_class = get_value('class', **kwargs)
    
    # $ image = Image_Series("/images/events/school building/first_class_sb_event <class> <nude> <step>.webp", **kwargs)

    show screen black_screen_text("first_class_sb_event\nClass:" + school_class)

    headmaster "Hello, let me introduce myself again. I'm [headmaster_first_name] [headmaster_last_name], the new headmaster of this school."
    headmaster "I'm actually a psychologist but I got myself a teaching license to help students like you to receive a better education."
    headmaster "Don't worry, you will still be taught by your regular teachers. I work mainly on school reform and will only occasionally teach a class."
    headmaster "If you have any questions or issues, feel free to come to me. I always put heavy emphasis on the well-being of my students."
    headmaster "Now I'd like to get to know you a bit better. Would you please all introduce yourself?"

    if school_class == "3A":
        headmaster "Miss Ryan, would you like to start?"
        teacher3 "Yes, of course."
        teacher3 "My name is Finola Ryan. I'm 28 years old and I'm a teacher for English and Geography. I am also the class teacher of 3A."
        # students introduce themselves
        $ set_game_data('first_class_3A', True)
        $ advance_progress('first_class')
        if loli_content == 0:
            $ set_progress('first_class', 3)

    elif school_class == "2A":
        headmaster "Miss Anderson, would you like to start?"
        teacher1 "Yes, of course."
        teacher1 "My name is Lily Anderson. I'm 32 years old and I'm a teacher for Math and Sciences. I am also the class teacher of 2A."
        # students introduce themselves
        $ set_game_data('first_class_2A', True)
        $ advance_progress('first_class')
        if loli_content <= 1:
            $ set_progress('first_class', 3)

    elif school_class == "1A":
        headmaster "Miss Parker, would you like to start?"
        teacher5 "Yes, of course."
        teacher5 "My name is Zoe Parker. I'm 24 years old and I'm a teacher for Sport and Art. I am also the class teacher of 1A."
        # students introduce themselves
        $ set_game_data('first_class_1A', True)
        $ advance_progress('first_class')

    $ end_event('new_daytime', **kwargs)

#################
# Teaching events

label teach_class_event (**kwargs):
    $ school_obj = get_character("school", charList)
    
    call show_idle_image(school_obj, "images/background/school building/bg f.webp", sb_bg_images,
        loli = get_random_loli()
    ) from teach_class_event_2

    call call_event_menu (
        "What subject do you wanna teach?", 
        sb_teach_events,
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from teach_class_event_1

    jump school_building

label sb_teach_english_1 (**kwargs):
    subtitles "Todo: english subject"
    jump new_daytime

label sb_teach_math_1 (**kwargs):
    subtitles "Todo: math subject"
    jump new_daytime

#######################
# General Random Events

label sb_event_1 (**kwargs): # patrol, check class
    $ begin_event(**kwargs)

    $ char_obj = get_char_value(**kwargs)
    
    # show screen black_screen_text("sb_event_1")
    $ image = Image_Series("/images/events/school building/sb_event_1 <step>.webp", **kwargs)

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
    
    $ begin_event()
    
    # show screen black_screen_text("sb_event_1.leave")
    $ image.show(2)
    # call show_image("/images/events/school building/sb_event_1 <name> 3.webp", SCENE, **kwargs)
    subtitles "You decide to leave them and let them have their fun."
    $ change_stats_with_modifier(char_obj,
        charm = DEC_SMALL, education = TINY, corruption = TINY, inhibition = DEC_SMALL)
    
    $ end_event('new_daytime', **kwargs)
label .stop (**kwargs):
    
    $ begin_event()
    
    # show screen black_screen_text("sb_event_1.stop")
    $ image.show(3)
    # call show_image("/images/events/school building/sb_event_1 <name> 4.webp", SCENE, **kwargs)
    headmaster "Hey you! Stop that. You know that is against the rules!"
    sgirl "We're sorry!"
    $ change_stats_with_modifier(char_obj,
        charm = MEDIUM, happiness = DEC_SMALL, education = SMALL, reputation = TINY, inhibition = DEC_TINY)
    
    $ end_event('new_daytime', **kwargs)

label sb_event_2 (**kwargs): # teach class
    $ begin_event(**kwargs)

    $ char_obj = get_char_value(**kwargs)
    
    $ image = Image_Series("/images/events/school building/sb_event_2 <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "A student tripped while handing out assignments in class."

    $ image.show(1)
    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave alone", "sb_event_2.leave"),
        ("Help her up", "sb_event_2.help"), 
    **kwargs)
label .leave (**kwargs):
    
    $ begin_event()
    
    $ image.show(2)
    subtitles "You decide to leave her alone."
    $ change_stats_with_modifier(char_obj,
        charm = DEC_TINY, education = TINY)
    
    $ end_event('new_daytime', **kwargs)
label .help (**kwargs):
    
    $ begin_event()
    
    $ image.show(3)
    subtitles "You help her up."
    $ change_stats_with_modifier(char_obj,
        charm = DEC_TINY, happiness = SMALL, education = TINY)
    
    $ end_event('new_daytime', **kwargs)

label sb_event_3 (**kwargs): # patrol
    $ begin_event(**kwargs)

    $ char_obj = get_char_value(**kwargs)
    
    $ image = Image_Series("/images/events/school building/sb_event_3 <step>.webp", **kwargs)

    $ image.show(0) # walk with girl sitting
    subtitles "As you walk through the corridors of the high school, you notice a student sitting in the corner of the hallway."
    sgirl "*sniffle*"

    $ image.show(1) # stand next to her asking
    headmaster "Are you okay?"
    
    $ image.show(2) # girl answers without looking up
    sgirl "I'm fine. It's just... No I'm fine."

    $ call_custom_menu(False,
        ("What is going on?", "sb_event_3.what"),
        ("If it's nothing, go back to class", "sb_event_3.send_class", (time.check_daytime("c") and time.check_weekday("d")) or is_replay(**kwargs)), 
    **kwargs)
label .what (**kwargs):
    
    $ begin_event()
    
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
    
    $ begin_event()
    
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

    $ change_stats_with_modifier(char_obj, 
        charm = TINY, happiness = DEC_LARGE, education = TINY, reputation = DEC_TINY)
    
    $ end_event('new_daytime', **kwargs)
label .get_to_bottom (**kwargs):
    
    $ begin_event()
    
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

    $ change_stats_with_modifier(char_obj,
        happiness = LARGE, reputation = TINY)
    
    $ end_event('new_daytime', **kwargs)
label .send_class (**kwargs):
    
    $ begin_event()
    
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

    $ begin_event()
    
    $ image.show(19) # headmaster squats next to her
    headmaster "Look, maybe you should just take the day off. I'll notify your teacher."

    $ image.show(20) # girl looks to headmaster
    sgirl "Yes... thank you..."

    $ image.show(14) # headmaster helps girl up
    subtitles "You help her up and walk her to the dormitory."
    $ change_stats_with_modifier(char_obj,
        happiness = LARGE, reputation = TINY)
    
    $ end_event('new_daytime', **kwargs)
label .chin_up (**kwargs):
    
    $ begin_event()
    
    $ image.show(19) # headmaster squats next to her
    headmaster "Now, now, it can't be that bad. I'm sure whatever caused those tears will soon be forgotten."

    $ image.show(21) # girl says nothing
    sgirl "..."

    $ image.show(22) # headmaster stands up
    headmaster "Now, run along. Just tell the teachers you needed a breath of air. I'll take care of the rest."
    sgirl "Ok..."

    $ image.show(23) # girl walks away
    subtitles "You help her up and she walks off."
    $ change_stats_with_modifier(char_obj,
        happiness = LARGE, reputation = TINY)
    
    $ end_event('new_daytime', **kwargs)

label sb_event_4(**kwargs):
    $ begin_event(**kwargs)

    $ char_obj = get_char_value(**kwargs)

    # you see a girl falling in the hallway
    sgirl "AHH!"
    subtitles "*CRASH*"
    sgirl "Ouch..."

    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave her alone", "sb_event_4.leave"),
        ("Help her up", "sb_event_4.help"),
        ("Point out her panties", "sb_event_4.panties"),
    **kwargs)

label .leave (**kwargs):

    # students run to fallen student helping her, headmaster standing further back observing it and then walking away
    headmaster_thought "Hmm, the others already rush to help her. No need for me to get involved."

    $ end_event('new_daytime', **kwargs)

label .help (**kwargs):

    # headmaster quickly approaches girl and helps her up
    headmaster "Are you okay? Here let me help you."
    # girl smiles and thanks him
    sgirl "Thank you."
    # headmaster looking worried
    headmaster "Does anything hurt?"
    # girl happy 
    sgirl "No, I'm fine."
    # headmaster standing behind waving as girl walks off
    headmaster "Okay then. Be more careful next time."
    # girl waves back
    sgirl "Yes, I will."

    $ end_event('new_daytime', **kwargs)

label .panties (**kwargs):

    # headmaster crouches in front of her
    headmaster "Cute panties."
    # girl jumps back
    sgirl "Eh?!"
    # headmaster points down
    headmaster "Oh, sorry. I didn't mean to embarrass you. But that bear is cute cute."
    # girl jumps up
    sgirl "Eeeek! Pervert!"
    # girl runs off

    $ end_event('new_daytime', **kwargs)
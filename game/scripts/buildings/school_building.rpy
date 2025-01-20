##############################################
# region School Building Event Handler ----- #
##############################################

init -1 python:
    set_current_mod('base')
    
    sb_timed_event   = TempEventStorage("school_building", "school_building", fallback = Event(2, "school_building.after_time_check"))
    sb_general_event =     EventStorage("school_building", "school_building", fallback = Event(2, "school_building.after_general_check"))
    register_highlighting(sb_timed_event, sb_general_event)

    sb_events = {}
    add_storage(sb_events, EventStorage("teach_class",  "school_building", fallback_text = "There is nobody here."))
    add_storage(sb_events, EventStorage("patrol",       "school_building", fallback_text = "There is nobody here."))

    sb_teach_events = {}
    add_storage(sb_teach_events, EventStorage("math",    "school_building", fallback_text = "There is nobody here."))
    add_storage(sb_teach_events, EventStorage("history", "school_building", fallback_text = "There is nobody here."))

    sb_teach_math_ld_storage = FragmentStorage('sb_teach_math_ld')
    sb_teach_math_main_storage = FragmentStorage('sb_teach_math_main')
    sb_teach_history_intro_storage = FragmentStorage('sb_teach_history_intro')
    sb_teach_history_main_storage = FragmentStorage('sb_teach_history_main')

    sb_bg_images = BGStorage("images/background/school building/f.webp",
        BGImage("images/background/school building/<school_level> <nude> <variant>.webp", 1, TimeCondition(daytime = "c", weekday = "d")),
        BGImage("images/background/school building/n.webp", 1, TimeCondition(daytime = 7)),
    )

init 1 python:
    set_current_mod('base')

    ####################
    # Default Events
    first_class_sb_event_event = Event(1, "first_class_sb_event",
        TimeCondition(weekday = "d", daytime = "c"),
        ProgressCondition('first_class', '2-'),
        RandomListSelector('class', '3A'),
        Pattern("main", "/images/events/school building/first_class_sb_event/first_class_sb_event <class> <nude> <step>.webp"),
        thumbnail = "images/events/school building/first_class_sb_event/first_class_sb_event 3A 0 2.webp")

    sb_event1 = Event(3, "sb_event_1",
        TimeCondition(daytime = "c", weekday = "d"),
        LevelSelector('school_level', 'school'),
        Pattern("main", "/images/events/school building/sb_event_1/sb_event_1 <school_level> <step>.webp"),
        thumbnail = "images/events/school building/sb_event_1/sb_event_1 1 1.webp")

    sb_event3 = Event(3, "sb_event_3",
        TimeCondition(daytime = "d", weekday = "d"),
        Pattern("main", "/images/events/school building/sb_event_3/sb_event_3 <school_level> <step>.webp"),
        thumbnail = "images/events/school building/sb_event_3/sb_event_3 1 1.webp")

    sb_event4 = Event(3, "sb_event_4",
        TimeCondition(daytime = "f", weekday = "d"),
        Pattern("main", "/images/events/school building/sb_event_4/sb_event_4 <school_level> <step>.webp"),
        thumbnail = "images/events/school building/sb_event_4/sb_event_4 1 0.webp")

    sb_event5 = Event(3, "sb_event_5",
        TimeCondition(daytime = "c", weekday = "d"),
        LevelCondition("5-", "school"),
        RandomListSelector('girls', 'ikushi_ito', 'soyoon_yamamoto', 'yuriko_oshima'),
        Pattern('main', "/images/events/school building/sb_event_5/sb_event_5 <school_level> <girls> <step>.webp", 'school_level', 'girls'),
        thumbnail = "images/events/school building/sb_event_5/sb_event_5 1 soyoon_yamamoto 11.webp")
    ####################

    #################
    # Event insertion

    sb_events["patrol"].add_event(
        sb_event1, 
        sb_event3,
        sb_event4,
        sb_event5,
    )

    #################

# endregion
##############################################

############################################
# region School Building Entry Point ----- #
############################################

label school_building ():
    call call_available_event(sb_timed_event) from school_building_1
    
label .after_time_check (**kwargs):
    call call_available_event(sb_general_event) from school_building_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do in the School?", 
        sb_events,
        default_fallback,
        character.subtitles,
        bg_image = sb_bg_images,
    ) from school_building_3

    jump school_building

#endregion
############################################

#######################################
# region School Building Events ----- #
#######################################

#########################
# region Regular Events #

label sb_event_1 (**kwargs): # patrol, check class
    $ begin_event(**kwargs)

    $ school_level = get_value('school_level', **kwargs)
    
    $ sakura = get_person("class_3a", "sakura_mori").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You walk through the corridors of the high school."

    $ image.show(1)
    subtitles "You come across a couple making out in the hallway."

    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave and let them have fun", "sb_event_1.leave"),
        ("Stop them", "sb_event_1.stop", not is_rule_unlocked("student_student_relation")), 
    **kwargs)
label .leave (**kwargs):
    
    $ begin_event(**kwargs)
    
    # show screen black_screen_text("sb_event_1.leave")
    $ image.show(2)
    # call show_image("/images/events/school building/sb_event_1 <name> 3.webp", SCENE, **kwargs)
    subtitles "You decide to leave them and let them have their fun."
    call change_stats_with_modifier('school',
        charm = DEC_SMALL, education = TINY, corruption = TINY, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_63
    
    $ end_event('new_daytime', **kwargs)
label .stop (**kwargs):
    
    $ begin_event(**kwargs)
    
    # show screen black_screen_text("sb_event_1.stop")
    $ image.show(3)
    # call show_image("/images/events/school building/sb_event_1 <name> 4.webp", SCENE, **kwargs)
    headmaster "Hey you! Stop that. You know that is against the rules!"
    sakura "We're sorry!"
    call change_stats_with_modifier('school',
        charm = MEDIUM, happiness = DEC_SMALL, education = SMALL, reputation = TINY, inhibition = DEC_TINY) from _call_change_stats_with_modifier_64
    
    $ end_event('new_daytime', **kwargs)

label sb_event_3 (**kwargs): # patrol
    $ begin_event("2", **kwargs)

    $ miwa = get_person("class_3a", "miwa_igarashi").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0) # walk with girl sitting
    subtitles "As you walk through the corridors of the high school, you notice a student sitting in the corner of the hallway."
    miwa "*sniffle*"

    $ image.show(1) # stand next to her asking
    headmaster "Are you okay?"
    
    $ image.show(2) # girl answers without looking up
    miwa "I'm fine. It's just... No I'm fine."

    $ call_custom_menu(False,
        ("What is going on?", "sb_event_3.what"),
        ("If it's nothing, go back to class", "sb_event_3.send_class", (time.check_daytime("c") and time.check_weekday("d")) or is_replay(**kwargs)), 
    **kwargs)
label .what (**kwargs):
    
    $ begin_event(**kwargs)
    
    $ image.show(3) # headmaster sits next to her
    headmaster "What is going on? I can see there is something bothering you."

    $ image.show(4) # girl still doesn't look
    miwa "I really don't want to talk about it. I'd like to be alone right now."

    $ image.show(5) # headmaster asks looking straight
    headmaster "Did someone do this to you?"

    $ image.show(6) # girl looks away, headmaster looks at her
    miwa "..."

    $ call_custom_menu(False, 
        ("Leave her alone", "sb_event_3.leave"), 
        ("Get to the bottom of this", "sb_event_3.get_to_bottom"), 
    **kwargs)
label .leave (**kwargs):
    
    $ begin_event(**kwargs)
    
    $ image.show(6)
    subtitles"You hesitate for a moment, but then decide to leave her alone."

    $ image.show(7) # headmaster stands up
    headmaster "Okay, I'll leave you alone."

    $ image.show(1) # headmaster stands next to her talking
    headmaster "But if you need anything, you can always come to me. My door is always open."

    $ image.show(2) # image 2 but with girl not talking
    miwa "..."

    $ image.show(8) # headmaster stands a bit further away looking back to her
    subtitles"You walk away with a heavy heart."

    call change_stats_with_modifier('school', 
        charm = TINY, happiness = DEC_LARGE, education = TINY, reputation = DEC_TINY) from _call_change_stats_with_modifier_65
    
    $ end_event('new_daytime', **kwargs)
label .get_to_bottom (**kwargs):
    
    $ begin_event(**kwargs)
    
    $ image.show(3) # headmaster looks to girl
    headmaster "I really want to help you. Please tell me what is going on."

    $ image.show(10) # headmaster looks girl doesn't answer
    miwa "..."
    
    $ image.show(9) # headmaster rests head against wall talking
    headmaster "Please listen."

    $ image.show(10) # headmaster rests head against wall talking
    miwa "..."
    $ image.show(9) # headmaster rests head against wall talking
    headmaster "Whatever happened to you, if some someone did or said anything."

    $ image.show(11) # girl buries head deeper into arms
    miwa "*sniffle*"
    subtitles "She slowly and silently starts crying."

    $ image.show(12) # headmaster looks to girl
    headmaster "Let's go to my office, shall we? There it is more private and nobody will bother us. You can then decide what you want to share. Is that okay?"

    $ image.show(13) # girl looks to headmaster
    miwa "I- I... yes... thank-"

    $ image.show(14) # headmaster and girl walk to office
    subtitles "You support her back to your office and bring her something warm to drink."

    call change_stats_with_modifier('school',
        happiness = LARGE, reputation = TINY) from _call_change_stats_with_modifier_66
    
    $ end_event('new_daytime', **kwargs)
label .send_class (**kwargs):
    
    $ begin_event(**kwargs)
    
    $ image.show(15) # headmaster starts walking away
    headmaster "Then you better get back to class."

    $ image.show(16) # girl looks up
    miwa "B- But... I..."

    $ image.show(17) # headmaster looks back
    headmaster "Yes?"

    $ image.show(18) # girl again buries head in arms
    miwa "I d-don't..."

    $ call_custom_menu(False, 
        ("Poor thing", "sb_event_3.poor_thing"), 
        ("Chin up", "sb_event_3.chin_up"), 
    **kwargs)
label .poor_thing (**kwargs):

    $ begin_event(**kwargs)
    
    $ image.show(19) # headmaster squats next to her
    headmaster "Look, maybe you should just take the day off. I'll notify your teacher."

    $ image.show(20) # girl looks to headmaster
    miwa "Yes... thank you..."

    $ image.show(14) # headmaster helps girl up
    subtitles "You help her up and walk her to the dormitory."
    call change_stats_with_modifier('school',
        happiness = LARGE, reputation = TINY) from _call_change_stats_with_modifier_67
    
    $ end_event('new_daytime', **kwargs)
label .chin_up (**kwargs):
    
    $ begin_event(**kwargs)
    
    $ image.show(19) # headmaster squats next to her
    headmaster "Now, now, it can't be that bad. I'm sure whatever caused those tears will soon be forgotten."

    $ image.show(21) # girl says nothing
    miwa "..."

    $ image.show(22) # headmaster stands up
    headmaster "Now, run along. Just tell the teachers you needed a breath of air. I'll take care of the rest."
    miwa "Ok..."

    $ image.show(23) # girl walks away
    subtitles "You help her up and she walks off."
    call change_stats_with_modifier('school',
        happiness = LARGE, reputation = TINY) from _call_change_stats_with_modifier_68
    
    $ end_event('new_daytime', **kwargs)

label sb_event_4(**kwargs):
    $ begin_event("2", **kwargs)

    $ ikushi = get_person("class_3a", "ikushi_ito").get_character()

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1) from _call_Image_Series_show_image_9
    sgirl "AHH!"

    $ image.show(2)
    subtitles "*CRASH*"
    ikushi "Ouch..."

    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave her alone", "sb_event_4.leave"),
        ("Help her up", "sb_event_4.help"),
    **kwargs)
label .leave (**kwargs):

    $ image.show(3)
    headmaster_thought "Hmm, the others already rush to help her. No need for me to get involved."

    call change_stats_with_modifier('school',
        happiness = DEC_TINY, charm = SMALL, education = TINY) from _call_change_stats_with_modifier_69

    $ end_event('new_daytime', **kwargs)
label .help (**kwargs):


    $ image.show(4)
    headmaster "Are you okay? Here let me help you."
    
    $ image.show(5)
    ikushi "Thank you."
    
    headmaster "Does anything hurt?"
    
    $ image.show(6)
    ikushi "No, I'm fine."
    
    $ image.show(7)
    headmaster "Okay then. Be more careful next time."
    
    $ image.show(8)
    ikushi "Yes, I will."

    call change_stats_with_modifier('school',
        happiness = SMALL, charm = DEC_TINY, education = TINY) from _call_change_stats_with_modifier_70

    call empty_label() from _call_Image_Series_show_image_10
    call empty_label() from _call_change_stats_with_modifier_71

    $ end_event('new_daytime', **kwargs)

label sb_event_5 (**kwargs):
    $ begin_event("2", **kwargs)

    $ girls = get_value('girls', **kwargs)

    $ image = convert_pattern('main', **kwargs)

    $ girl_char = get_person('class_3a', girls).get_character()

    call Image_Series.show_image(image, 0, 1, 2) from _call_show_image_sb_event_5_event_1
    # headmaster walks through hallway
    subtitles "*thump*"
    $ image.show(3)
    headmaster "Huh?"
    $ image.show(4)
    headmaster_thought "Hmm, is someone in the classroom?"
    headmaster_thought "That class should have physical education right now."
    $ image.show(5)
    headmaster_thought "I should check that out."
    # headmaster opens door
    # you see three girls changing clothes
    call Image_Series.show_image(image, 6, 7, 8) from _call_show_image_sb_event_5_event_2
    girl_char "Huh?!"
    # headmaster closes door
    call Image_Series.show_image(image, 7, 9, 10) from _call_show_image_sb_event_5_event_3
    headmaster "I'm sorry! I didn't mean to barge into you changing."
    headmaster "But I have to ask, why are you here? Should you be in the gym for class?"
    $ image.show(11)
    girl_char "We like to change clothes here. The changing rooms in the gym are too small and uncomfortable."
    $ image.show(10)
    headmaster "I understand. But please hurry up. You'll be late for class."
    $ image.show(11)
    girl_char "Yes, sir."

    call change_stats_with_modifier('school',
        inhibition = DEC_TINY) from _call_change_stats_with_modifier_72

    $ end_event('new_daytime', **kwargs)

# endregion
#########################

# endregion
#######################################
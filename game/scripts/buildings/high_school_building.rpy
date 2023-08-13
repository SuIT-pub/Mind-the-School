##################################################
# ----- High School Building Event Handler ----- #
##################################################

init python:
    high_school_building_after_time_check = Event("high_school_building_after_time_check", "high_school_building.after_time_check", 2)
    high_school_building_fallback         = Event("high_school_building_fallback",         "high_school_building_fallback",         2)
    high_school_building_person_fallback  = Event("high_school_building_person_fallback",  "high_school_building_person_fallback",  2)

    high_school_building_timed_event = EventStorage("high_school_building", "", high_school_building_after_time_check)
    high_school_building_events = {
        "check_class": EventStorage("check_class", "Check Class",      high_school_building_person_fallback),
        "teach_class": EventStorage("teach_class", "Teach a Class",    high_school_building_person_fallback),
        "patrol":      EventStorage("patrol",      "Patrol building",  high_school_building_person_fallback),
        "students":    EventStorage("students",    "Talk to students", high_school_building_person_fallback),
    }

    high_school_building_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_high_school_building_event"],
        1,
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    high_school_building_timed_event.add_event(Event(
        "first_potion_event",
        ["first_potion_high_school_building_event"],
        1,
        TimeCondition(day = 9),
    ))

    # high_school_building_events["check_class"].add_event(Event(
    #     "check_class_events",
    #     [
    #         "hsb_peek_into_class_concentrated",
    #         "hsb_peek_into_class_not_concentrated",
    #         "hsb_peek_into_class_chaos",
    #         "hsb_check_class_concentrated",
    #         "hsb_check_class_seemingly_concentrated",
    #     ],
    #     3,
    #     # TimeCondition(daytime = 'c', weekday = 'd'),
    #     # LevelCondition('1+', "high_school"),
    # ))

    # high_school_building_events["teach_class"].add_event(Event(
    #     "teach_class_events",
    #     [
    #         "hsb_teach_class_concentrated",
    #         "hsb_teach_class_partly_unconcentrated",
    #         "hsb_teach_class_unconcentrated",
    #         "hsb_teach_class_chaos",
    #     ],
    #     3,
    #     # TimeCondition(daytime = 'c', weekday = 'd'),
    #     # LevelCondition('1+', "high_school"),
    # ))

    # high_school_building_events["patrol"].add_event(Event(
    #     "patrol_events",
    #     [
    #         "hsb_patrol_stare",
    #         "hsb_patrol_mobbing",
    #         "hsb_patrol_wind",
    #         "hsb_patrol_trip",
    #     ],
    #     3,
    #     # TimeCondition(daytime = 'f', weekday = 'd'),
    #     # LevelCondition('1+', "high_school"),
    # ))
    # high_school_building_events["patrol"].add_event(Event("patrol_events_1","hsb_patrol_kiss", 3,
    #     # TimeCondition(daytime = 'f', weekday = 'd'),
    #     # LevelCondition('1+', "high_school"),
    #     # RuleCondition("student_student_relation"),
    # ))
    # high_school_building_events["patrol"].add_event(Event("patrol_events","hsb_patrol_groping", 3,
    #     # TimeCondition(daytime = 'f', weekday = 'd'),
    #     # LevelCondition('5+', "high_school"),
    # ))

    # high_school_building_events["students"].add_event(Event(
    #     "students_events",
    #     [
    #         "hsb_talk_students_1",
    #         "hsb_talk_students_2",
    #         "hsb_talk_students_3",
    #     ],
    #     3,
    #     # TimeCondition(daytime = 'f', weekday = 'd'),
    #     # LevelCondition('1+', "high_school"),
    # ))


##################################################

################################################
# ----- High School Building Entry Point ----- #
################################################

label high_school_building:
    # show school corridor

    $ image_path = "images/background/high school building/bg f.png"

    if time.check_daytime("c"):
        $ image_path = get_image_with_level(
            "images/background/high school building/bg c {level} {nude}.png", 
            "high_school", 
            charList["schools"]
        )

    if time.check_daytime(7):
        $ image_path = "images/background/high school building/bg 7.png"

    show screen image_with_nude_var (image_path, 0)

    call call_available_event(high_school_building_timed_event) from _call_call_available_event_6

label .after_time_check:

    call call_event_menu (
        "What to do in the High School?",
        1, 
        7, 
        high_school_building_events, 
        high_school_building_fallback,
    ) from _call_call_event_menu_6

    jump high_school_building

################################################

####################################################
# ----- High School Building Fallback Events ----- #
####################################################

label high_school_building_fallback:
    subtitles "There is nothing to do here."
    return
label high_school_building_person_fallback:
    subtitles "There is nobody here."
    return

####################################################

###########################################
# ----- High School Building Events ----- #
###########################################

# first week event
label first_week_high_school_building_event:
    show first week high school building 1
    subtitles """You enter the main building of the high school.
        
        Well, you don't really need to enter the building to get an idea of the state it's in."""
        
    show first week high school building 2
    principal_thought """Despite my fear, the building seems to be rather well maintained.

        It could be a bit cleaner but the corridor seems rather well.

        Let's see the classrooms."""
    
    show first week high school building 3
    principal_thought "Oh not bad as well. "

    show first week high school building 4
    principal_thought "Hmm I think there should be a class right now, let's check."

    show first week high school building 6
    principal_thought "Hmm looks like a normal class, but I think the students have no material?"
    principal_thought "Yeah, not one school girl has even one book."
    principal_thought "I guess the former principal cut back on those"

    $ set_stat_for_all("education", 15, schools)

    $ set_building_blocked("high_school_building")
    $ set_building_blocked("middle_school_building")
    $ set_building_blocked("elementary_school_building")

    jump new_day

label first_potion_high_school_building_event:

    show first potion high school building 1
    principal_thought "Let's see how classes are today."
    
    show first potion high school building 2
    subtitles "You look into a classroom and the first thing you notice is that almost everyone has opened up or at least partially removed their clothes."
    subtitles "Apparently the teachers also took a drink."
    principal_thought "Hmm, I can't wait to have this view on a regular basis, but that's gonna take some time."

    $ set_building_blocked("high_school_building")
    $ set_building_blocked("middle_school_building")
    $ set_building_blocked("elementary_school_building")

    jump new_daytime

# check class events

# look through window, students concentrated
label hsb_peek_into_class_concentrated:
    subtitles "You are looking into one of the windows of a classroom."
    subtitles "The students are paying attention to the lesson."

    $ change_stat("education", renpy.random.random() * 0.25, "high_school", charList["schools"])

    jump new_daytime

# look through window, students not concentrated
label hsb_peek_into_class_not_concentrated:
    subtitles "You are looking into one of the windows of a classroom."
    subtitles "You see many students doing other things and the teacher struggling to get their attention."

    $ change_stat("education", renpy.random.random() - 1 * 0.5, "high_school", charList["schools"])

    jump new_daytime

# look thorugh window, students in chaos
label hsb_peek_into_class_chaos:
    subtitles "You are looking into one of the windows of a classroom."
    subtitles "Total Mayhem controls the classroom.\nYou see the teacher struggling to keep control of the class.{p}Maybe I should train the teachers more."

    $ change_stat("education", renpy.random.random() * -0.25, "high_school", charList["schools"])

    jump new_daytime

# step into classroom, students concentrated
label hsb_check_class_concentrated:
    subtitles "You enter one of the classes.\nAlmost no one pays attention to you because all the students are paying close attention to the teacher."
    subtitles "You peek into one of the student's notebooks and notice the neatly written notes."

    $ change_stat("education", 0.5, "high_school", charList["schools"])

    jump new_daytime

# step into classroom, students concentrated, nude drawing
label hsb_check_class_seemingly_concentrated:
    subtitles "You enter one of the classes.\nAlmost no one pays attention to you because all the students are paying close attention to the teacher."
    subtitles "You peek into one of the student's notebooks."

    menu:
        subtitles "You notice a naked drawing of the teacher."

        "Scold the student in front of the class":
            call hsb_check_class_seemingly_concentrated.scolding_student_public from _call_hsb_check_class_seemingly_concentrated_scolding_student_public
        "Silently scold the student":
            call hsb_check_class_seemingly_concentrated.scolding_student_private from _call_hsb_check_class_seemingly_concentrated_scolding_student_private
        "Praise the student in front of the class":
            call hsb_check_class_seemingly_concentrated.praise_student_public from _call_hsb_check_class_seemingly_concentrated_praise_student_public
        "Silently praise the student":
            call hsb_check_class_seemingly_concentrated.praise_student_private from _call_hsb_check_class_seemingly_concentrated_praise_student_private
        
label .scolding_student_public:
    principal_shout "What are you drawing? This is not tolerable. Come to my office this evening!"

    $ add_temp_event(Event("male_student_scolding", "male_student_scolding", 2, 
        TimeCondition(daytime = 6)
    ))

    $ change_stat("education", 0.5, "high_school", charList["schools"])
    $ change_stat("happiness", -0.25, "high_school", charList["schools"])
    $ change_stat("inhibition", 0.1, "high_school", charList["schools"])
    jump new_daytime

label .scolding_student_private:
    principal_whisper "What are you drawing? This is not tolerable. Come to my office this evening!"

    $ add_temp_event(Event("male_student_scolding", "male_student_scolding", 2, 
        TimeCondition(daytime = 6)
    ))

    $ change_stat("education", 0.1, "high_school", charList["schools"])
    $ change_stat("happiness", -0.1, "high_school", charList["schools"])
    jump new_daytime

label .praise_student_public:
    principal_shout "Look at this student and his art-piece. He will bring it far with this talent in art."

    $ change_stat("education", -0.1, "high_school", charList["schools"])
    $ change_stat("happiness", 0.75, "high_school", charList["schools"])
    $ change_stat("inhibition", 0.2, "high_school", charList["schools"])
    jump new_daytime

label .praise_student_private:
    principal_whisper "You are really talented. Your choice on who to draw is also very nice."

    $ change_stat("happiness", 0.25, "high_school", charList["schools"])
    $ change_stat("inhibition", 0.1, "high_school", charList["schools"])
    jump new_daytime

# teach class events

# teach class, students unconcentrated
label hsb_teach_class_concentrated:
    subtitles "You teached a class and everything went alright."
    $ change_stat("education", 0.5, "high_school", charList["schools"])
    jump new_daytime

# teach class, not all students concentrated
label hsb_teach_class_partly_unconcentrated:
    subtitles "You teached a class but not everyone seemed to pay attention."
    $ change_stat("education", 0.25, "high_school", charList["schools"])
    jump new_daytime

# teach class, no students concentrated
label hsb_teach_class_unconcentrated:
    subtitles "You tried to teach a class but nobody seemed to pay any attention to you."
    $ change_stat("education", -0.2, "high_school", charList["schools"])
    jump new_daytime

# teach class, all students run around classroom doing other things
label hsb_teach_class_chaos:
    subtitles "You planned to teach a class, but what happened in the room is nowhere near anything teachable."
    $ change_stat("education", -0.5, "high_school", charList["schools"])
    jump new_daytime


# patrol events

label hsb_patrol_intro_variants:
    $ level = get_level_for_char("high_school", charList["schools"])
    $ poss_variants = [1, 2]
    if rules["student_student_relation"]:
        $ poss_variants.append(3)
    if level >= 3:
        $ poss_variants.append(4)
    if level >= 5:
        $ poss_variants.append(5)
    if level >= 7:
        $ poss_variants.append(6)
    $ variant = renpy.random.choice(poss_variants)

    if variant == 1:
        # show students talking
        # scene expression "events/high_school_building/variants_patrol_talking_[high_school_lvl].png"
        subtitles "You walk through the hallway of the school building."
        subtitles "The hallway is filled with students talking to each other."
    elif variant == 2:
        # show students playing with each other
        # scene expression "events/high_school_building/variants_patrol_playing_[high_school_lvl].png"
        subtitles "You walk through the hallway of the school building."
        subtitles "You see students playing with each other, clapping and such."
    elif variant == 3:
        # show students kissing each other
        # scene expression "events/high_school_building/variants_patrol_kissing_[high_school_lvl].png"
        subtitles "You walk through the hallway of the school building."
        subtitles "The hallway is filled with love and students kissing."
    elif variant == 4:
        # show students hugging and kuddling
        # scene expression "events/high_school_building/variants_patrol_cuddling_[high_school_lvl].png"
        subtitles "You walk through the hallway of the school building."
        subtitles "The view is heartwarming, seeing the student hug and cuddle.{p} You are happy with the results."
    elif variant == 5:
        # show students groping each other and having fun
        # scene expression "events/high_school_building/variants_patrol_groping_[high_school_lvl].png"
        subtitles "You walk through the hallway of the school building."
        subtitles "The students having fun grabbing and groping each other, discovering ther bodies."
    elif variant == 6:
        # show students having sex in all areas and corners of the hallway
        # scene expression "events/high_school_building/variants_patrol_sex_[high_school_lvl].png"
        subtitles "You walk through the hallway of the school building."
        subtitles "What a view! Everywhere you look, you see students having sex. Nice!"
    return

label hsb_patrol_stare:
    call hsb_patrol_intro_variants from _call_hsb_patrol_intro_variants

    $ level = get_level_for_char("high_school", charList["schools"])

    if level <= 1:
        # scene expression "events/high_school_building/patrol_stare_1_[high_school_lvl].png"
        subtitles "As you patrol the area, you see the sudents stare in your direction.{p}Their cold gazes hurt a little bit, but you're sure they don't mean it that way."
        $ change_stat("happiness", 0.1, "high_school", charList["schools"])
    elif 2 <= level <= 4:
        # scene expression "events/high_school_building/patrol_stare_2_[high_school_lvl].png"
        subtitles "You walk through the hallways and everywhere the students smile at you. It is really nice here at this school!"
        $ change_stat("happiness", 0.5, "high_school", charList["schools"])
    elif 5 <= level <= 6:
        # scene expression "events/high_school_building/patrol_stare_3_[high_school_lvl].png"
        subtitles " As soon as the students see you, they start pulling up their tops to present their bosom for their official greeting to you."
        $ change_stat("happiness", 0.5, "high_school", charList["schools"])
        $ change_stat("inhibition", 0.2, "high_school", charList["schools"])
        $ change_stat("corruption", 0.1, "high_school", charList["schools"])
    elif level >= 7:
        # scene expression "events/high_school_building/patrol_stare_4_[high_school_lvl].png"
        subtitles " As soon as the students see you, they start pulling up their tops and skirts to present their beautiful bodies for their official greeting to you."
        $ change_stat("happiness", 0.5, "high_school", charList["schools"])
        $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
        $ change_stat("corruption", 0.3, "high_school", charList["schools"])
    jump new_daytime

label hsb_patrol_kiss:
    call hsb_patrol_intro_variants from _call_hsb_patrol_intro_variants_1

    menu:
        subtitles "You spot two students kissing each other. What do you do?"

        "Break them up":
            subtitles "You step in and break them apart. Scolding them about the rules and the indecency they are spreading."
            $ change_stat("happiness", -0.5, "high_school", charList["schools"])
            $ change_stat("inhibition", -0.3, "high_school", charList["schools"])
            $ change_stat("corruption", -0.2, "high_school", charList["schools"])
            $ change_stat("education", 0.4, "high_school", charList["schools"])
        "Leave them be":
            subtitles "You decide to ignore them. They noticed you and appreciate you being so considerate of their love."
            $ change_stat("happiness", 0.4, "high_school", charList["schools"])
            $ change_stat("inhibition", 0.2, "high_school", charList["schools"])
            $ change_stat("education", -0.2, "high_school", charList["schools"])

    jump new_daytime

label hsb_patrol_mobbing:
    call hsb_patrol_intro_variants from _call_hsb_patrol_intro_variants_2

    $ variant = renpy.random.randint(1,2)

    $ level = get_level_for_char("high_school", charList["schools"])

    subtitles "You spot students punching and pushing a helpless girl."
    if 4 <= level <= 5:
        if variant == 1:
            subtitles "Pulling and ripping open her top."
        elif variant == 2:
            subtitles "Pulling and ripping open her top and bra."
    elif 5 <= level <= 6:
        if variant == 1:
            subtitles "Pulling open her top and playing with her boobs."
        elif variant == 2:
            subtitles "Opening her shirt and pulling down skirt and panties."
    elif level >= 7:
        subtitles "Pushing her down to the ground, pulling open her top and panties."
        if variant == 1:
            subtitles "Shoving a dildo up her pussy."
        elif variant == 2:
            subtitles "Pushing her fist in her pussy."

    menu:
        subtitles "What do you do?"

        "Break them up":
            principal_shout "What the hell is happening here?!"
            principal_shout "Get off her. You all come to my office this evening!"
            principal_shout "And you better pray to the heavens if any of won't come!"
            
            $ add_temp_event(Event("mobbing_scolding", "mobbing_scolding", 2, 
                TimeCondition(daytime = 6)
            ))

            $ change_stat("happiness", 0.2, "high_school", charList["schools"])
            $ change_stat("education", 0.2, "high_school", charList["schools"])
            jump new_daytime
        "Leave them be":
            subtitles "You choose to look away and go the other direction."
            subtitles "The mobbed girl looks in your direction and cries for help, tears in her eyes for being left alone."
            $ change_stat("happiness", -1, "high_school", charList["schools"])
            $ change_stat("education", -0.5, "high_school", charList["schools"])
            $ change_stat("inhibition", 1, "high_school", charList["schools"])
            $ change_stat("corruption", 0.5, "high_school", charList["schools"])
            jump new_daytime

label hsb_patrol_groping:
    call hsb_patrol_intro_variants from _call_hsb_patrol_intro_variants_3

    $ level = get_level_for_char("high_school", charList["schools"])

    subtitles "The students are having fun touching and groping each other."
    subtitles "A healthy sight for healty students!"

    if 5 <= level <= 6:
        subtitles "You see them grabbing each others boobs and nicely formed butts."
        $ change_stat("happiness", 0.2, "high_school", charList["schools"])
        $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
        $ change_stat("corruption", 0.2, "high_school", charList["schools"])
        jump new_daytime
    elif level == 7:
        subtitles "The students are touching each others pussies through the panties."
        $ change_stat("happiness", 0.3, "high_school", charList["schools"])
        $ change_stat("inhibition", 0.6, "high_school", charList["schools"])
        $ change_stat("corruption", 0.3, "high_school", charList["schools"])
        jump new_daytime
    elif level == 8:
        subtitles "The students are touching each others pussies."
        subtitles "Fingering them and playing with their clits."
        $ change_stat("happiness", 0.4, "high_school", charList["schools"])
        $ change_stat("inhibition", 0.8, "high_school", charList["schools"])
        $ change_stat("corruption", 0.4, "high_school", charList["schools"])
        jump new_daytime
    elif level >= 9:
        subtitles "Everywhere you look, you see students having sex."
        $ change_stat("happiness", 0.6, "high_school", charList["schools"])
        $ change_stat("inhibition", 1, "high_school", charList["schools"])
        $ change_stat("corruption", 0.5, "high_school", charList["schools"])
        jump new_daytime

label hsb_patrol_wind:
    call hsb_patrol_intro_variants from _call_hsb_patrol_intro_variants_4

    $ level = get_level_for_char("high_school", charList["schools"])
    $ variant = renpy.random.randint(1, 2)

    subtitles "As you walk through the hallway, a strong gust of wind blows through an open window and throws the students' skirts."

    menu:
        subtitles "How do you react?"

        "Look away visibly":
            subtitles "You decide to be decent and look away."
            if 0 <= level <= 3:
                subtitles "The students appreciate your decency."
                $ change_stat("happiness", 0.2, "high_school", charList["schools"])
                $ change_stat("inhibition", -0.2, "high_school", charList["schools"])
                jump new_daytime
            elif 4 <= level <= 5:
                subtitles "The students are a bit sad about your decision."
                $ change_stat("happiness", -0.2, "high_school", charList["schools"])
                $ change_stat("inhibition", -0.3, "high_school", charList["schools"])
                jump new_daytime
            elif level >= 6:
                subtitles "The students look very disappointed."
                $ change_stat("happiness", -0.4, "high_school", charList["schools"])
                $ change_stat("inhibition", -0.4, "high_school", charList["schools"])
                jump new_daytime
        "Ignore them":
            subtitles "You don't notice their mishap."
            if 0 <= level <= 3:
                subtitles "The students sigh in relief that nobody saw them."
                $ change_stat("happiness", 0.2, "high_school", charList["schools"])
                $ change_stat("inhibition", 0.2, "high_school", charList["schools"])
                jump new_daytime
            elif 4 <= level <= 5:
                subtitles "The students took their time to fix their skirts, seemingly disappointed that nobody saw their sweet knickers."
                $ change_stat("happiness", -0.2, "high_school", charList["schools"])
                $ change_stat("inhibition", -0.3, "high_school", charList["schools"])
                jump new_daytime
            elif level >= 6:
                subtitles "The students a very disappointed of nobody noticing them."
                $ change_stat("happiness", -0.4, "high_school", charList["schools"])
                $ change_stat("inhibition", -0.4, "high_school", charList["schools"])
                jump new_daytime
        "Look":
            subtitles "You don't avert you eyes, burning every second of those girls panties into your memory."
            if 0 <= level <= 3:
                subtitles "The students cry, grab their skirts and angrily stare in your direction."
                $ change_stat("happiness", -0.5, "high_school", charList["schools"])
                $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                jump new_daytime
            elif 4 <= level <= 5:
                subtitles "The students fix their skirts but smile and wink at you in appreciation of your gaze."
                $ change_stat("happiness", 0.3, "high_school", charList["schools"])
                $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                jump new_daytime
            elif level == 6:
                if variant == 1:
                    subtitles "The students smile at you while holding up their skirts to present you their bottoms."
                    $ change_stat("happiness", 0.6, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.8, "high_school", charList["schools"])
                    jump new_daytime
                if variant == 2:
                    subtitles "You just notice their seductive looks before they open your pants and start sucking your dick."
                    $ change_stat("happiness", 0.8, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                    $ change_stat("corrption", 0.4, "high_school", charList["schools"])
                    jump new_daytime
            elif level >= 7:
                if variant == 1:
                    subtitles "The students smile at you while before they start fingering themselves."
                    $ change_stat("happiness", 0.8, "high_school", charList["schools"])
                    $ change_stat("inhibition", 1, "high_school", charList["schools"])
                    jump new_daytime
                if variant == 2:
                    subtitles "You just notice their seductive looks before they open your pants throw you on the ground to just psuh your dick into their pussies."
                    $ change_stat("happiness", 1, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.5, "high_school", charList["schools"])
                    $ change_stat("corrption", 1, "high_school", charList["schools"])
                    jump new_daytime

label hsb_patrol_trip:
    call hsb_patrol_intro_variants from _call_hsb_patrol_intro_variants_5

    $ level = get_level_for_char("high_school", charList["schools"])
    $ variant = renpy.random.randint(1, 2)
    $ trip_variant = renpy.random.randint(1, 2)

    subtitles "A girl runs past you. Just before you were to call her out to not run in the building, she strips and falls."
label .patrol_trip_check1:

    subtitles "Now she lies there exposing her bottom to the world and more importantly to you."

    menu:
        subtitles "How do you react?"

        "Ignore":
            subtitles "You choose to ignore the girl lying on the ground and walk away."
            if level <= 3:
                subtitles "The girl is happy you didn't seem to see her panties but still sad about you being so indifferent to your students."
                $ change_stat("happiness", -0.5, "high_school", charList["schools"])
                $ change_stat("inhibition", -0.2, "high_school", charList["schools"])
                jump new_daytime
            elif 4 <= level <= 6:
                subtitles "The girl is sad you didn't see her panties. She even put on her cute ones."
                $ change_stat("happiness", -0.2, "high_school", charList["schools"])
                $ change_stat("inhibition", -0.4, "high_school", charList["schools"])
                jump new_daytime
            elif level >= 7:
                subtitles "The girl feels really sad about you not giving her any attention."
                $ change_stat("happiness", -0.5, "high_school", charList["schools"])
                jump new_daytime
        "Scold":
            subtitles "You step up to her and start scolding her about not running in the hallways."
            if level <= 4:
                subtitles "The girl is very apologetic and ashamed that you can see her panties."
                subtitles "Not that you would have a problem with that."
                $ change_stat("happiness", -0.3, "high_school", charList["schools"])
                $ change_stat("inhibition", -0.2, "high_school", charList["schools"])
                $ change_stat("education", 0.2, "high_school", charList["schools"])
                jump new_daytime
            elif 5 <= level <= 7:
                subtitles "The girl looks very sad about you scolding her. As an apology she starts jerking you off"
                $ change_stat("happiness", -0.2, "high_school", charList["schools"])
                $ change_stat("inhibition", 0.2, "high_school", charList["schools"])
                $ change_stat("education", 0.4, "high_school", charList["schools"])
                jump new_daytime
            elif level >= 8:
                subtitles "The girl is very sad you about you shouting at her. Under tears she spreads her legs to present you her apology."
                $ change_stat("happiness", -0.5, "high_school", charList["schools"])
                $ change_stat("inhibition", 0.2, "high_school", charList["schools"])
                $ change_stat("corruption", 0.5, "high_school", charList["schools"])
                $ change_stat("education", 0.2, "high_school", charList["schools"])
                jump new_daytime
        "Help":
            subtitles "You quickly run to the girl and offer your helping hand to her."
            if level <= 3:
                subtitles "The girl gladly accepts your help, her face bright red after everyone seeing her panties."
                $ change_stat("happiness", 0.3, "high_school", charList["schools"])
                $ change_stat("inhibition", 0.1, "high_school", charList["schools"])
                jump new_daytime
            elif 4 <= level <= 6:
                subtitles "The girl is happy about your help. As a thank you she pulls up her top to present you her sweet bosom."
                $ change_stat("happiness", 0.5, "high_school", charList["schools"])
                $ change_stat("inhibition", 0.3, "high_school", charList["schools"])
                jump new_daytime
            elif level >= 7:
                if variant == 1:
                    subtitles "The girl thanks you for your help, grabbing your crotch and giving you a kiss"
                    $ change_stat("happiness", 0.5, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                    jump new_daytime
                else:
                    subtitles "The girl thanks you for your help, opening your pants and jerking you off."
                    $ change_stat("happiness", 0.5, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                    $ change_stat("corruption", 0.2, "high_school", charList["schools"])
                    jump new_daytime
        "Look":
            subtitles "You can't help yourself but stare at this wonderful view of that girls exposed butt."
            if level <= 4:
                subtitles "The girl notices your stare, cries and quickly covers herself, red in shame."
                $ change_stat("happiness", -0.3, "high_school", charList["schools"])
                $ change_stat("inhibition", 0.3, "high_school", charList["schools"])
                jump new_daytime
            elif 5 <= level <= 7:
                if variant == 1:
                    subtitles "The girl appreciates you looking. As an extra she pulls up her top, exposing her breasts"
                    $ change_stat("happiness", 0.5, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.5, "high_school", charList["schools"])
                    jump new_daytime
                else:    
                    subtitles "The girl appreciates you looking. She now crawls over to you, unpacking your dick and stroking it."
                    $ change_stat("happiness", 0.5, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.2, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.2, "high_school", charList["schools"])
                    jump new_daytime
            elif level >= 8:
                if variant == 1:
                    subtitles "The girl notices your look. Interpreting it as invitiation, she directly jumps onto you, pushing your dick into her."
                    $ change_stat("happiness", 0.5, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                    jump new_daytime
                else:
                    subtitles "The girl spreads her legs and pussy after seeing you staring."
                    principal_thought "The school really develops perfectly."
                    $ change_stat("happiness", 0.5, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                    jump new_daytime
        "Take advantage":
            menu:
                subtitles "How to take advantage?"
                "Grope":
                    subtitles "You can't help yourself but grab the butt thats clearly presented in front of you."
                    if level <= 3:
                        subtitles "A loud scream can be heard across the hallway. The girl is NOT amoused."
                        $ change_stat("happiness", -2, "high_school", charList["schools"])
                        $ change_stat("corruption", -0.5, "high_school", charList["schools"])
                        jump new_daytime
                    elif 4 <= level <= 6:
                        subtitles "The girl is suprised about the hand feeling up her butt, but she is not displeased."
                        $ change_stat("happiness", 0.3, "high_school", charList["schools"])
                        $ change_stat("corruption", 0.2, "high_school", charList["schools"])
                        jump new_daytime
                    elif level >= 7:
                        subtitles "The girl appreciates your nice gesture and thanks you with a view on her boobs."
                        $ change_stat("happiness", 0.5, "high_school", charList["schools"])
                        $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                        jump new_daytime
                "Finger":
                    subtitles "You take advantage of the situation and start rubbing your finger on the girls pussy."
                    if level <= 3:
                        subtitles "You hear a scream, a slap and feel pain on your face. You got slapped by the girl."
                        principal_thought "Well, I deserved that. But worth it!"
                        $ change_stat("happiness", -4, "high_school", charList["schools"])
                        $ change_stat("corruption", 0.2, "high_school", charList["schools"])
                        $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                        jump new_daytime
                    elif 4 <= level <= 6:
                        subtitles "The girl moans loudly after you started touching her. She is visibly pleased but seems to try to hide it."
                        $ change_stat("happiness", 0.5, "high_school", charList["schools"])
                        $ change_stat("corruption", 0.4, "high_school", charList["schools"])
                        jump new_daytime
                    elif level >= 7:
                        subtitles "The girl grabs you, visibly enjoying it. You continue, pushing your finger into her until she cums."
                        $ change_stat("happiness", 0.8, "high_school", charList["schools"])
                        $ change_stat("corruption", 0.6, "high_school", charList["schools"])
                        jump new_daytime
                "Sex" if level >= 4:
                    subtitles "This sight exhilarates you. Your primal instincts take over. You open your pants and rush to ram your dick into that poor girls pussy."
                    if level <= 4:
                        subtitles "The girl gasps loudly. Suprised over the thick rod moving inside her."
                        subtitles "She seems not totally happy about it, but she isn't displeased either."
                        $ change_stat("happiness", -0.2, "high_school", charList["schools"])
                        $ change_stat("corruption", 0.1, "high_school", charList["schools"])
                        $ change_stat("inhibition", 0.3, "high_school", charList["schools"])
                        jump new_daytime
                    elif 5 <= level <= 7:
                        subtitles "The girl is suprised but enjoys it very much. Her moans can be heard across the hallway."
                        $ change_stat("happiness", 0.5, "high_school", charList["schools"])
                        $ change_stat("corruption", 0.4, "high_school", charList["schools"])
                        jump new_daytime
                    elif level >= 8:
                        subtitles "The girl is extremely happy about her situation. After seeing you the other girls step in to join."
                        subtitles "They are now a mass of fucking, kissing and licking bodies."
                        $ change_stat("happiness", 0.1, "high_school", charList["schools"])
                        $ change_stat("corruption", 0.8, "high_school", charList["schools"])
                        jump new_daytime
                "Anal" if level >= 7 and trip_variant == 2:
                    subtitles "You take hold of this situation. Push away the underwear and push your dick into her ass."
                    if level <= 8:
                        subtitles "The girl screams silently. It seems to hurt her a little. After a while she seems to like it but she is a little bit angry about you."
                        $ change_stat("happiness", -0.2, "high_school", charList["schools"])
                        $ change_stat("corruption", 1, "high_school", charList["schools"])
                        jump new_daytime
                    elif level >= 9:
                        subtitles "The girls gasps shortly because of the pain. But she is definetly into it."
                        $ change_stat("happiness", 0.2, "high_school", charList["schools"])
                        $ change_stat("corruption", 1.3, "high_school", charList["schools"])
                        jump new_daytime

label hsb_patrol_collide:
    call hsb_patrol_intro_variants from _call_hsb_patrol_intro_variants_6

    $ level = get_level_for_char("high_school", charList["schools"])
    $ variant = renpy.random.randint(1, 3)

    subtitles "As you turn around the corner, you collide with a student that seemingly ran too fast through the hallway."
    if variant == 1:
        jump hsb_patrol_trip.patrol_trip_check1
    elif variant == 2:
        subtitles "You both fall. After you open your eyes you see yourself lying on top of the girl that ran into you."
        menu:
            subtitles "How do you react?"
            "Stand up":
                if level <= 3:
                    subtitles "You stand up and pat the dust from your clothing. After that, you help the girl get up."
                    subtitles "The girl thanks you and you both continue to go your ways."
                    $ change_stat("happiness", 0.3, "high_school", charList["schools"])
                    jump new_daytime
                elif 4 <= level <= 6:
                    subtitles "You stand up and help the girl. She then presents you her boobs as a thank you."
                    $ change_stat("happiness", 0.7, "high_school", charList["schools"])
                    jump new_daytime
                elif level >= 7:
                    subtitles "You stand up and hold out your hand to help the girl. But she helps herself with your dick and gives you a blowjob."
                    $ change_stat("corruption", 0.2, "high_school", charList["schools"])
                    jump new_daytime
            "'Are you okay?'":
                if level <= 3:
                    principal "Are you okay?"
                    sgirl "Yes, but could you please get off me?"
                    principal "O-Of course, excuse me!"
                    $ change_stat("happiness", -0.2, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.2, "high_school", charList["schools"])
                    jump new_daytime
                if 4 <= level <= 6:
                    principal "Are you okay?"
                    sgirl "Yes, thank you!" 
                    #image kiss
                    $ change_stat("happiness", 0.6, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                    jump new_daytime
                if level >= 7:
                    $ variant = renpy.random.randint(1, 2)
                    principal "Are you okay?"
                    #girl grabs crotch
                    sgirl "Oh yeah I'm okay!"
                    #girl kiss
                    $ change_stat("happiness", 0.8, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.8, "high_school", charList["schools"])
                    if variant == 1:
                        sgirl "If we're like this, we could also just do it."
                        $ change_stat("corruption", 0.4, "high_school", charList["schools"])
                    jump new_daytime
            "Grope":
                if level <= 3:
                    subtitles "You take the opportunity and grab the girls breast."
                    principal "Oh I'm sorry, I just landed quite unfortunate."
                    sgirl "The girl is not convinced and throws you off her."
                    $ change_stat("happiness", -0.5, "high_school", charList["schools"])
                    $ change_stat("inhibition", 0.4, "high_school", charList["schools"])
                    $ change_stat("corruption", 0.2, "high_school", charList["schools"])
                    jump new_daytime
                if 4 <= level <= 6:
                    subtitles "You grab the girls breast."
                    sgirl "Mhh! Do you like them?" 
                    $ change_stat("inhibition", 0.6, "high_school", charList["schools"])
                    $ change_stat("corruption", 0.3, "high_school", charList["schools"])
                    jump new_daytime
                if level >= 7:
                    subtitles "You start kneading her breasts."
                    sgirl "Oh yeah that's good!"
                    sgirl "Let's just do it right here!"
                    $ change_stat("inhibition", 0.9, "high_school", charList["schools"])
                    $ change_stat("corruption", 0.5, "high_school", charList["schools"])
                    jump new_daytime
    else:
        subtitles "The girl knocks you off, you fall and the girl on top."
        $ variant = renpy.random.randint(1, 11)
        $ variant2 = renpy.random.randint(1, 2)
        if variant <= 3:
            subtitles "She now sits on your lap."
            principal "Are you okay?"
            if level <= 3:
                sgirl "Y-yes! Thank you!"
                $ change_stat("happiness", 0.4, "high_school", charList["schools"])
                jump new_daytime
            elif level <= 6:
                sgirl "Oh I am more than alright!"
                #kiss and greeting
                $ change_stat("happiness", 0.6, "high_school", charList["schools"])
                $ change_stat("inhibition", 0.2, "high_school", charList["schools"])
                jump new_daytime
            elif level >= 7:
                sgirl "Oh I'm sure this is fate."
                # grabs crotch
                $ change_stat("happiness", 0.8, "high_school", charList["schools"])
                $ change_stat("inhibition", 0.6, "high_school", charList["schools"])
                if variant2 == 2:
                    #sex
                    $ change_stat("corruption", 0.4, "High_school", charList["schools"])
                jump new_daytime
        elif variant <= 6:
            subtitles "She now sits on your lap. The Boner in your pants pressing against her."
            principal "Are you okay?"
            if level <= 3:
                sgirl "W-What is that thing poking me down there?"
                principal "Oh. I'm sorry, that's my... I mean... You are very cute, so..."
                sgirl "Eeek!"
                $ change_stat("inhibition", 0.3, "high_school", charList["schools"]);
                $ change_stat("happiness", -0.3, "high_school", charList["schools"]);
                jump new_daytime
            elif level <= 6:
                sgirl "Oh is that a banana, or are you happy to see me?"
                sgirl "In any case, I hope you're happy to see these."
                # show boobs
                $ change_stat("inhibition", 0.5, "high_school", charList["schools"]);
                $ change_stat("happiness", 0.3, "high_school", charList["schools"]);
                jump new_daytime
            elif level >= 7:
                sgirl "Oh someone wants some action, I guess."
                # sex
                $ change_stat("inhibition", 0.8, "high_school", charList["schools"]);
                $ change_stat("corruption", 0.3, "high_school", charList["schools"]);
                jump new_daytime
        elif variant <= 8:
            subtitles "As you open your eyes. All you see are panties. The ones from the girl lying on top of you."
            if level <= 4:
                subtitles "The girl straightens up. Only after you try talking and the girls starts to feel a little tingling on her pussy. She jumps up and runs away blushing and screaming."
                $ change_stat("inhibition", 0.6, "high_school", charList["schools"]);
                $ change_stat("happiness", -0.3, "high_school", charList["schools"]);
                jump new_daytime
            elif level <= 7:
                subtitles "The girl seems to be a bit fixated on your crotch, before she opens your pants and gives you a handjob."
                subtitles "Likewise you start fingering her pussy."
                $ change_stat("inhibition", 0.8, "high_school", charList["schools"]);
                $ change_stat("corruption", 0.4, "high_school", charList["schools"]);
                jump new_daytime
            elif level >= 8:
                subtitles "The girl seems to take that as an invitation to open your pants and suck your dick."
                subtitles "You pull the panties aside and start licking her pussy."
                $ change_stat("inhibition", 1, "high_school", charList["schools"]);
                $ change_stat("corruption", 0.6, "high_school", charList["schools"]);
                jump new_daytime
        elif variant <= 10:
            subtitles "Your pants seemed to be open as now the girl is sitting on your lap with your naked dick poking her in the panties."
            if level <= 4:
                subtitles "The girl starts blushing as she notices the tip of your penis penetrating her pussy through her panties."
                subtitles "She quickly jumps up and runs away screaming."
                $ change_stat("inhibition", 0.7, "high_school", charList["schools"])
                $ change_stat("happiness", -2, "high_school", charList["schools"])
                jump new_daytime
            elif level <= 7:
                sgirl "I appreciate your attempt but that seems a little bit fast, doesn't it?"
                subtitles "She gets of your dick but grabs it."
                sgirl "Better start small."
                # handjob
                $ change_stat("inhibition", 1, "high_school", charList["schools"])
                $ change_stat("corruption", 0.5, "high_school", charList["schools"])
                $ change_stat("happiness", -0.3, "high_school", charList["schools"])
                jump new_daytime
            elif level >= 8:
                sgirl "You careful quickpants! You gotta remove the panties first!"
                # sex
                $ change_stat("inhibition", 1.2, "high_school", charList["schools"])
                $ change_stat("corruption", 0.8, "high_school", charList["schools"])
                $ change_stat("happiness", 0.6, "high_school", charList["schools"])
                jump new_daytime
        elif variant == 11:
            subtitles "They always laugh at you when you say that. But here it really happens. She literally fell on your dick."
            if level <= 4:
                subtitles "The girl seems to be speechless. Either she is baffled by the situation or overwhelmed by pleasure."
                subtitles "She tries to get off but she slips and again rams your dick into her pussy."
                subtitles "She starts twitching and passes out."
                $change_stat("inhibition", 1.5, "high_school", charList["schools"])
                $change_stat("corruption", 1, "high_school", charList["schools"])
                $change_stat("happiness", -4, "high_school", charList["schools"])
                jump new_daytime
            elif level <= 6:
                sgirl "Whaaaa...?! What are you doing, you can't just do that! I'd like to play with you but not this much!"
                $change_stat("inhibition", 0.9, "high_school", charList["schools"])
                $change_stat("corruption", 0.6, "high_school", charList["schools"])
                $change_stat("happiness", -1, "high_school", charList["schools"])
                jump new_daytime
            elif level >= 7:
                subtitles "The girl twitches. She apparently came from the sudden penetration."
                subtitles "A few seconds later she starts riding your dick."
                $change_stat("inhibition", 0.8, "high_school", charList["schools"])
                $change_stat("corruption", 0.5, "high_school", charList["schools"])
                $change_stat("happiness", 0.5, "high_school", charList["schools"])
                jump new_daytime



# student talk events

label hsb_talk_students_1:
    subtitles "You approach a few students."
    subtitles "But as soon as you get close to the students, they scurry around the corner."
    jump new_daytime

label hsb_talk_students_2:
    subtitles "You see a few students and move over to talk to them."
    subtitles "You have a deep discussion about the school and their life in this school."
    subtitles "The students are visibly happy to have a headmaster they can talk to."
    $ change_stat("happiness", 0.25, "high_school", charList["schools"])
    jump new_daytime

label hsb_talk_students_3:
    subtitles "You see a few students and move over to talk to them."
    subtitles "The students have a few issues about the school that they want to talk to you about."
    subtitles "You discuss a few points with them."
    subtitles "The students are visibly happy to have a headmaster who cares about their concerns."
    $ change_stat("happiness", 0.4, "high_school", charList["schools"])
    jump new_daytime

    

###########################################

###########################################
# ----- High School Building Scenes ----- #
###########################################


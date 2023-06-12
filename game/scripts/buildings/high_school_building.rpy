##################################################
# ----- High School Building Event Handler ----- #
##################################################

init -10 python:
    high_school_building_events = {}

    high_school_building_events["fallback"] = "high_school_building_fallback"

    # event check before menu
    high_school_building_events["high_school_building"] = {
        "fallback": "high_school_building.after_time_check", # no event
    }

    high_school_building_events["check_class"] = {
        "fallback": "high_school_building_person_fallback",
        "x.x.x.c.d.1+:x:x.0": [
            "hsb_peek_into_class_concentrated",
            "hsb_peek_into_class_not_concentrated",
            "hsb_peek_into_class_chaos",
            "hsb_check_class_concentrated",
            "hsb_check_class_seemingly_concentrated",
        ],
    }

    high_school_building_events["teach_class"] = {
        "fallback": "high_school_building_person_fallback",
        "x.x.x.c.d.1+:x:x.0": [
            "hsb_teach_class_concentrated",
            "hsb_teach_class_partly_unconcentrated",
            "hsb_teach_class_unconcentrated",
            "hsb_teach_class_chaos",
        ]
    }

    high_school_building_events["patrol"] = {
        "fallback": "high_school_building_fallback",
        "x.x.x.f.d.1+:x:x.0": [
            "hsb_patrol_stare",
            "hsb_patrol_kiss", # is conditional
            "hsb_patrol_mobbing",
            "hsb_patrol_wind",
            "hsb_patrol_trip",
        ],
        "x.x.x.f.d.5+:x:x.0": [
            "hsb_patrol_groping",
        ]
    }

    high_school_building_events["students"] = {
        "fallback": "high_school_building_person_fallback",
        "x.x.x.f.d.1+:x:x.0": [
            "hsb_talk_students_1",
            "hsb_talk_students_2",
            "hsb_talk_students_3",
        ]
    }

##################################################

################################################
# ----- High School Building Entry Point ----- #
################################################

label high_school_building:
    # show school corridor

    # if daytime in [1, 3, 6]:
    #     # show corridor filled with students
    # if daytime in [2, 4, 5]:
    #     # show empty corridor
    # if daytime in [7]:
    #     # show empty corridor at night

    call event_check_area("high_school_building", high_school_building_events)

label.after_time_check:

    $ check_events = [
        get_events_area_count("check_class", high_school_building_events),
        get_events_area_count("teach_class", high_school_building_events),
        get_events_area_count("patrol"     , high_school_building_events),
        get_events_area_count("students"   , high_school_building_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do in the High School?"

            "Check class" if check_events[0] > 0:
                call event_check_area("check_class", high_school_building_events)
            "Teach class" if check_events[1] > 0:
                call event_check_area("teach_class", high_school_building_events)
            "Patrol building" if check_events[2] > 0:
                call event_check_area("patrol", high_school_building_events)
            "Talk to students" if check_events[3] > 0:
                call event_check_area("students", high_school_building_events)
            "Return":
                jump map_overview
    else:
        call high_school_building_fallback
        jump map_overview

    jump high_school_building

################################################

####################################################
# ----- High School Building Fallback Events ----- #
####################################################

label high_school_building_fallback:
    Subtitles "There is nothing to do here."
    return
label high_school_building_person_fallback:
    Subtitles "There is nobody here."
    return

####################################################

###########################################
# ----- High School Building Events ----- #
###########################################

# check class events

# look through window, students concentrated
label hsb_peek_into_class_concentrated:
    Subtitles "You are looking into one of the windows of a classroom."
    Subtitles "The students are paying attention to the lesson."

    $ change_stat("education", renpy.random.random() * 0.25, "high_school")

    jump new_daytime

# look through window, students not concentrated
label hsb_peek_into_class_not_concentrated:
    Subtitles "You are looking into one of the windows of a classroom."
    Subtitles "You see many students doing other things and the teacher struggling to get their attention."

    $ change_stat("education", renpy.random.random() - 1 * 0.5, "high_school")

    jump new_daytime

# look thorugh window, students in chaos
label hsb_peek_into_class_chaos:
    Subtitles "You are looking into one of the windows of a classroom."
    Subtitles "Total Mayhem controls the classroom.\nYou see the teacher struggling to keep control of the class.{p}Maybe I should train the teachers more."

    $ change_stat("education", renpy.random.random() * -0.25, "high_school")

    jump new_daytime

# step into classroom, students concentrated
label hsb_check_class_concentrated:
    Subtitles "You enter one of the classes.\nAlmost no one pays attention to you because all the students are paying close attention to the teacher."
    Subtitles "You peek into one of the student's notebooks and notice the neatly written notes."

    $ change_stat("education", 0.5, "high_school")

    jump new_daytime

# step into classroom, students concentrated, nude drawing
label hsb_check_class_seemingly_concentrated:
    Subtitles "You enter one of the classes.\nAlmost no one pays attention to you because all the students are paying close attention to the teacher."
    Subtitles "You peek into one of the student's notebooks."

    menu:
        Subtitles "You notice a naked drawing of the teacher."

        "Scold the student in front of the class":
            call hsb_check_class_seemingly_concentrated.scolding_student_public
        "Silently scold the student":
            call hsb_check_class_seemingly_concentrated.scolding_student_private
        "Praise the student in front of the class":
            call hsb_check_class_seemingly_concentrated.praise_student_public
        "Silently praise the student":
            call hsb_check_class_seemingly_concentrated.praise_student_private
        
label .scolding_student_public:
    char_Principal_shout "What are you drawing? This is not tolerable. Come to my office this evening!"

    $ temp_time_check_events.append("x.x.x.6.x.x:x:x~male_student_scolding")

    $ change_stat("education", 0.5, "high_school")
    $ change_stat("happiness", -0.25, "high_school")
    $ change_stat("inhibition", 0.1, "high_school")
    jump new_daytime

label .scolding_student_private:
    char_Principal_whisper "What are you drawing? This is not tolerable. Come to my office this evening!"

    $ temp_time_check_events.append("x.x.x.6.x.xxx:male_student_scolding")

    $ change_stat("education", 0.1, "high_school")
    $ change_stat("happiness", -0.1, "high_school")
    jump new_daytime

label .praise_student_public:
    char_Principal_shout "Look at this student and his art-piece. He will bring it far with this talent in art."

    $ change_stat("education", -0.1, "high_school")
    $ change_stat("happiness", 0.75, "high_school")
    $ change_stat("inhibition", 0.2, "high_school")
    jump new_daytime

label .praise_student_private:
    char_Principal_whisper "You are really talented. Your choice on who to draw is also very nice."

    $ change_stat("happiness", 0.25, "high_school")
    $ change_stat("inhibition", 0.1, "high_school")
    jump new_daytime

# teach class events

# teach class, students unconcentrated
label hsb_teach_class_concentrated:
    Subtitles "You teached a class and everything went alright."
    $ change_stat("education", 0.5, "high_school")
    jump new_daytime

# teach class, not all students concentrated
label hsb_teach_class_partly_unconcentrated:
    Subtitles "You teached a class but not everyone seemed to pay attention."
    $ change_stat("education", 0.25, "high_school")
    jump new_daytime

# teach class, no students concentrated
label hsb_teach_class_unconcentrated:
    Subtitles "You tried to teach a class but nobody seemed to pay any attention to you."
    $ change_stat("education", -0.2, "high_school")
    jump new_daytime

# teach class, all students run around classroom doing other things
label hsb_teach_class_chaos:
    Subtitles "You planned to teach a class, but what happened in the room is nowhere near anything teachable."
    $ change_stat("education", -0.5, "high_school")
    jump new_daytime


# patrol events

label hsb_patrol_intro_variants:
    $ level = schools["high_school"].get_level()
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
        Subtitles "You walk through the hallway of the school building."
        Subtitles "The hallway is filled with students talking to each other."
    elif variant == 2:
        # show students playing with each other
        # scene expression "events/high_school_building/variants_patrol_playing_[high_school_lvl].png"
        Subtitles "You walk through the hallway of the school building."
        Subtitles "You see students playing with each other, clapping and such."
    elif variant == 3:
        # show students kissing each other
        # scene expression "events/high_school_building/variants_patrol_kissing_[high_school_lvl].png"
        Subtitles "You walk through the hallway of the school building."
        Subtitles "The hallway is filled with love and students kissing."
    elif variant == 4:
        # show students hugging and kuddling
        # scene expression "events/high_school_building/variants_patrol_cuddling_[high_school_lvl].png"
        Subtitles "You walk through the hallway of the school building."
        Subtitles "The view is heartwarming, seeing the student hug and cuddle.{p} You are happy with the results."
    elif variant == 5:
        # show students groping each other and having fun
        # scene expression "events/high_school_building/variants_patrol_groping_[high_school_lvl].png"
        Subtitles "You walk through the hallway of the school building."
        Subtitles "The students having fun grabbing and groping each other, discovering ther bodies."
    elif variant == 6:
        # show students having sex in all areas and corners of the hallway
        # scene expression "events/high_school_building/variants_patrol_sex_[high_school_lvl].png"
        Subtitles "You walk through the hallway of the school building."
        Subtitles "What a view! Everywhere you look, you see students having sex. Nice!"
    return

label hsb_patrol_stare:
    call hsb_patrol_intro_variants

    $ level = schools["high_school"].get_level()

    if level <= 1:
        # scene expression "events/high_school_building/patrol_stare_1_[high_school_lvl].png"
        Subtitles "As you patrol the area, you see the sudents stare in your direction.{p}Their cold gazes hurt a little bit, but you're sure they don't mean it that way."
        $ change_stat("happiness", 0.1, "high_school")
    elif 2 <= level <= 4:
        # scene expression "events/high_school_building/patrol_stare_2_[high_school_lvl].png"
        Subtitles "You walk through the hallways and everywhere the students smile at you. It is really nice here at this school!"
        $ change_stat("happiness", 0.5, "high_school")
    elif 5 <= level <= 6:
        # scene expression "events/high_school_building/patrol_stare_3_[high_school_lvl].png"
        Subtitles " As soon as the students see you, they start pulling up their tops to present their bosom for their official greeting to you."
        $ change_stat("happiness", 0.5, "high_school")
        $ change_stat("inhibition", 0.2, "high_school")
        $ change_stat("corruption", 0.1, "high_school")
    elif level >= 7:
        # scene expression "events/high_school_building/patrol_stare_4_[high_school_lvl].png"
        Subtitles " As soon as the students see you, they start pulling up their tops and skirts to present their beautiful bodies for their official greeting to you."
        $ change_stat("happiness", 0.5, "high_school")
        $ change_stat("inhibition", 0.4, "high_school")
        $ change_stat("corruption", 0.3, "high_school")
    jump new_daytime

label hsb_patrol_kiss:
    if rules["student_student_relation"]:
        call event_check_area("patrol", high_school_building_events)
        jump new_daytime
    
    call hsb_patrol_intro_variants

    menu:
        Subtitles "You spot two students kissing each other. What do you do?"

        "Break them up":
            Subtitles "You step in and break them apart. Scolding them about the rules and the indecency they are spreading."
            $ change_stat("happiness", -0.5, "high_school")
            $ change_stat("inhibition", -0.3, "high_school")
            $ change_stat("corruption", -0.2, "high_school")
            $ change_stat("education", 0.4, "high_school")
        "Leave them be":
            Subtitles "You decide to ignore them. They noticed you and appreciate you being so considerate of their love."
            $ change_stat("happiness", 0.4, "high_school")
            $ change_stat("inhibition", 0.2, "high_school")
            $ change_stat("education", -0.2, "high_school")

    jump new_daytime

label hsb_patrol_mobbing:
    call hsb_patrol_intro_variants

    $ variant = renpy.random.randint(1,2)

    $ level = schools["high_school"].get_level()

    Subtitles "You spot students punching and pushing a helpless girl."
    if 4 <= level <= 5:
        if variant == 1:
            Subtitles "Pulling and ripping open her top."
        elif variant == 2:
            Subtitles "Pulling and ripping open her top and bra."
    elif 5 <= level <= 6:
        if variant == 1:
            Subtitles "Pulling open her top and playing with her boobs."
        elif variant == 2:
            Subtitles "Opening her shirt and pulling down skirt and panties."
    elif level >= 7:
        Subtitles "Pushing her down to the ground, pulling open her top and panties."
        if variant == 1:
            Subtitles "Shoving a dildo up her pussy."
        elif variant == 2:
            Subtitles "Pushing her fist in her pussy."

    menu:
        Subtitles "What do you do?"

        "Break them up":
            char_Principal_shout "What the hell is happening here?!"
            char_Principal_shout "Get off her. You all come to my office this evening!"
            char_Principal_shout "And you better pray to the heavens if any of won't come!"
            $ temp_time_check_events.append("x.x.x.6.x.x:x:x~mobbing_scolding")
            $ change_stat("happiness", 0.2, "high_school")
            $ change_stat("education", 0.2, "high_school")
            jump new_daytime
        "Leave them be":
            Subtitles "You choose to look away and go the other direction."
            Subtitles "The mobbed girl looks in your direction and cries for help, tears in her eyes for being left alone."
            $ change_stat("happiness", -1, "high_school")
            $ change_stat("education", -0.5, "high_school")
            $ change_stat("inhibition", 1, "high_school")
            $ change_stat("corruption", 0.5, "high_school")
            jump new_daytime
    jump new_daytime

label hsb_patrol_groping:
    call hsb_patrol_intro_variants

    $ level = schools["high_school"].get_level()

    Subtitles "The students are having fun touching and groping each other."
    Subtitles "A healthy sight for healty students!"

    if 5 <= level <= 6:
        Subtitles "You see them grabbing each others boobs and nicely formed butts."
        $ change_stat("happiness", 0.2, "high_school")
        $ change_stat("inhibition", 0.4, "high_school")
        $ change_stat("corruption", 0.2, "high_school")
        jump new_daytime
    elif level == 7:
        Subtitles "The students are touching each others pussies through the panties."
        $ change_stat("happiness", 0.3, "high_school")
        $ change_stat("inhibition", 0.6, "high_school")
        $ change_stat("corruption", 0.3, "high_school")
        jump new_daytime
    elif level == 8:
        Subtitles "The students are touching each others pussies."
        Subtitles "Fingering them and playing with their clits."
        $ change_stat("happiness", 0.4, "high_school")
        $ change_stat("inhibition", 0.8, "high_school")
        $ change_stat("corruption", 0.4, "high_school")
        jump new_daytime
    elif level >= 9:
        Subtitles "Everywhere you look, you see students having sex."
        $ change_stat("happiness", 0.6, "high_school")
        $ change_stat("inhibition", 1, "high_school")
        $ change_stat("corruption", 0.5, "high_school")
        jump new_daytime

label hsb_patrol_wind:
    call hsb_patrol_intro_variants

    $ level = schools["high_school"].get_level()
    $ variant = renpy.random.randint(1, 2)

    Subtitles "As you walk through the hallway, a strong gust of wind blows through an open window and throws the students' skirts."

    menu:
        Subtitles "How do you react?"

        "Look away visibly":
            Subtitles "You decide to be decent and look away."
            if 0 <= level <= 3:
                Subtitles "The students appreciate your decency."
                $ change_stat("happiness", 0.2, "high_school")
                $ change_stat("inhibition", -0.2, "high_school")
                jump new_daytime
            elif 4 <= level <= 5:
                Subtitles "The students are a bit sad about your decision."
                $ change_stat("happiness", -0.2, "high_school")
                $ change_stat("inhibition", -0.3, "high_school")
                jump new_daytime
            elif level >= 6:
                Subtitles "The students look very disappointed."
                $ change_stat("happiness", -0.4, "high_school")
                $ change_stat("inhibition", -0.4, "high_school")
                jump new_daytime
        "Ignore them":
            Subtitles "You don't notice their mishap."
            if 0 <= level <= 3:
                Subtitles "The students sigh in relief that nobody saw them."
                $ change_stat("happiness", 0.2, "high_school")
                $ change_stat("inhibition", 0.2, "high_school")
                jump new_daytime
            elif 4 <= level <= 5:
                Subtitles "The students took their time to fix their skirts, seemingly disappointed that nobody saw their sweet knickers."
                $ change_stat("happiness", -0.2, "high_school")
                $ change_stat("inhibition", -0.3, "high_school")
                jump new_daytime
            elif level >= 6:
                Subtitles "The students a very disappointed of nobody noticing them."
                $ change_stat("happiness", -0.4, "high_school")
                $ change_stat("inhibition", -0.4, "high_school")
                jump new_daytime
        "Look":
            Subtitles "You don't avert you eyes, burning every second of those girls panties into your memory."
            if 0 <= level <= 3:
                Subtitles "The students cry, grab their skirts and angrily stare in your direction."
                $ change_stat("happiness", -0.5, "high_school")
                $ change_stat("inhibition", 0.4, "high_school")
                jump new_daytime
            elif 4 <= level <= 5:
                Subtitles "The students fix their skirts but smile and wink at you in appreciation of your gaze."
                $ change_stat("happiness", 0.3, "high_school")
                $ change_stat("inhibition", 0.4, "high_school")
                jump new_daytime
            elif level == 6:
                if variant == 1:
                    Subtitles "The students smile at you while holding up their skirts to present you their bottoms."
                    $ change_stat("happiness", 0.6, "high_school")
                    $ change_stat("inhibition", 0.8, "high_school")
                    jump new_daytime
                if variant == 2:
                    Subtitles "You just notice their seductive looks before they open your pants and start sucking your dick."
                    $ change_stat("happiness", 0.8, "high_school")
                    $ change_stat("inhibition", 0.4, "high_school")
                    $ change_stat("corrption", 0.4, "high_school")
                    jump new_daytime
            elif level >= 7:
                if variant == 1:
                    Subtitles "The students smile at you while before they start fingering themselves."
                    $ change_stat("happiness", 0.8, "high_school")
                    $ change_stat("inhibition", 1, "high_school")
                    jump new_daytime
                if variant == 2:
                    Subtitles "You just notice their seductive looks before they open your pants throw you on the ground to just psuh your dick into their pussies."
                    $ change_stat("happiness", 1, "high_school")
                    $ change_stat("inhibition", 0.5, "high_school")
                    $ change_stat("corrption", 1, "high_school")
                    jump new_daytime

label hsb_patrol_trip:
    call hsb_patrol_intro_variants

    $ level = schools["high_school"].get_level()
    $ variant = renpy.random.randint(1, 2)
    $ trip_variant = renpy.random.randint(1, 2)

    Subtitles "A girl runs past you. Just before you were to call her out to not run in the building, she strips and falls."
label .patrol_trip_check1:

    Subtitles "Now she lies there exposing her bottom to the world and more importantly to you."

    menu:
        Subtitles "How do you react?"

        "Ignore":
            Subtitles "You choose to ignore the girl lying on the ground and walk away."
            if level <= 3:
                Subtitles "The girl is happy you didn't seem to see her panties but still sad about you being so indifferent to your students."
                $ change_stat("happiness", -0.5, "high_school")
                $ change_stat("inhibition", -0.2, "high_school")
                jump new_daytime
            elif 4 <= level <= 6:
                Subtitles "The girl is sad you didn't see her panties. She even put on her cute ones."
                $ change_stat("happiness", -0.2, "high_school")
                $ change_stat("inhibition", -0.4, "high_school")
                jump new_daytime
            elif level >= 7:
                Subtitles "The girl feels really sad about you not giving her any attention."
                $ change_stat("happiness", -0.5, "high_school")
                jump new_daytime
        "Scold":
            Subtitles "You step up to her and start scolding her about not running in the hallways."
            if level <= 4:
                Subtitles "The girl is very apologetic and ashamed that you can see her panties."
                Subtitles "Not that you would have a problem with that."
                $ change_stat("happiness", -0.3, "high_school")
                $ change_stat("inhibition", -0.2, "high_school")
                $ change_stat("education", 0.2, "high_school")
                jump new_daytime
            elif 5 <= level <= 7:
                Subtitles "The girl looks very sad about you scolding her. As an apology she starts jerking you off"
                $ change_stat("happiness", -0.2, "high_school")
                $ change_stat("inhibition", 0.2, "high_school")
                $ change_stat("education", 0.4, "high_school")
                jump new_daytime
            elif level >= 8:
                Subtitles "The girl is very sad you about you shouting at her. Under tears she spreads her legs to present you her apology."
                $ change_stat("happiness", -0.5, "high_school")
                $ change_stat("inhibition", 0.2, "high_school")
                $ change_stat("corruption", 0.5, "high_school")
                $ change_stat("education", 0.2, "high_school")
                jump new_daytime
        "Help":
            Subtitles "You quickly run to the girl and offer your helping hand to her."
            if level <= 3:
                Subtitles "The girl gladly accepts your help, her face bright red after everyone seeing her panties."
                $ change_stat("happiness", 0.3, "high_school")
                $ change_stat("inhibition", 0.1, "high_school")
                jump new_daytime
            elif 4 <= level <= 6:
                Subtitles "The girl is happy about your help. As a thank you she pulls up her top to present you her sweet bosom."
                $ change_stat("happiness", 0.5, "high_school")
                $ change_stat("inhibition", 0.3, "high_school")
                jump new_daytime
            elif level >= 7:
                if variant == 1:
                    Subtitles "The girl thanks you for your help, grabbing your crotch and giving you a kiss"
                    $ change_stat("happiness", 0.5, "high_school")
                    $ change_stat("inhibition", 0.4, "high_school")
                    jump new_daytime
                else:
                    Subtitles "The girl thanks you for your help, opening your pants and jerking you off."
                    $ change_stat("happiness", 0.5, "high_school")
                    $ change_stat("inhibition", 0.4, "high_school")
                    $ change_stat("corruption", 0.2, "high_school")
                    jump new_daytime
        "Look":
            Subtitles "You can't help yourself but stare at this wonderful view of that girls exposed butt."
            if level <= 4:
                Subtitles "The girl notices your stare, cries and quickly covers herself, red in shame."
                $ change_stat("happiness", -0.3, "high_school")
                $ change_stat("inhibition", 0.3, "high_school")
                jump new_daytime
            elif 5 <= level <= 7:
                if variant == 1:
                    Subtitles "The girl appreciates you looking. As an extra she pulls up her top, exposing her breasts"
                    $ change_stat("happiness", 0.5, "high_school")
                    $ change_stat("inhibition", 0.5, "high_school")
                    jump new_daytime
                else:    
                    Subtitles "The girl appreciates you looking. She now crawls over to you, unpacking your dick and stroking it."
                    $ change_stat("happiness", 0.5, "high_school")
                    $ change_stat("inhibition", 0.2, "high_school")
                    $ change_stat("inhibition", 0.2, "high_school")
                    jump new_daytime
            elif level >= 8:
                if variant == 1:
                    Subtitles "The girl notices your look. Interpreting it as invitiation, she directly jumps onto you, pushing your dick into her."
                    $ change_stat("happiness", 0.5, "high_school")
                    $ change_stat("inhibition", 0.4, "high_school")
                    jump new_daytime
                else:
                    Subtitles "The girl spreads her legs and pussy after seeing you staring."
                    char_Principal_thought "The school really develops perfectly."
                    $ change_stat("happiness", 0.5, "high_school")
                    $ change_stat("inhibition", 0.4, "high_school")
                    jump new_daytime
        "Take advantage":
            menu:
                Subtitles "How to take advantage?"
                "Grope":
                    Subtitles "You can't help yourself but grab the butt thats clearly presented in front of you."
                    if level <= 3:
                        Subtitles "A loud scream can be heard across the hallway. The girl is NOT amoused."
                        $ change_stat("happiness", -2, "high_school")
                        $ change_stat("corruption", -0.5, "high_school")
                        jump new_daytime
                    elif 4 <= level <= 6:
                        Subtitles "The girl is suprised about the hand feeling up her butt, but she is not displeased."
                        $ change_stat("happiness", 0.3, "high_school")
                        $ change_stat("corruption", 0.2, "high_school")
                        jump new_daytime
                    elif level >= 7:
                        Subtitles "The girl appreciates your nice gesture and thanks you with a view on her boobs."
                        $ change_stat("happiness", 0.5, "high_school")
                        $ change_stat("inhibition", 0.4, "high_school")
                        jump new_daytime
                "Finger":
                    Subtitles "You take advantage of the situation and start rubbing your finger on the girls pussy."
                    if level <= 3:
                        Subtitles "You hear a scream, a slap and feel pain on your face. You got slapped by the girl."
                        char_Principal_thought "Well, I deserved that. But worth it!"
                        $ change_stat("happiness", -4, "high_school")
                        $ change_stat("corruption", 0.2, "high_school")
                        $ change_stat("inhibition", 0.4, "high_school")
                        jump new_daytime
                    elif 4 <= level <= 6:
                        Subtitles "The girl moans loudly after you started touching her. She is visibly pleased but seems to try to hide it."
                        $ change_stat("happiness", 0.5, "high_school")
                        $ change_stat("corruption", 0.4, "high_school")
                        jump new_daytime
                    elif level >= 7:
                        Subtitles "The girl grabs you, visibly enjoying it. You continue, pushing your finger into her until she cums."
                        $ change_stat("happiness", 0.8, "high_school")
                        $ change_stat("corruption", 0.6, "high_school")
                        jump new_daytime
                "Sex" if level >= 4:
                    Subtitles "This sight exhilarates you. Your primal instincts take over. You open your pants and rush to ram your dick into that poor girls pussy."
                    if level <= 4:
                        Subtitles "The girl gasps loudly. Suprised over the thick rod moving inside her."
                        Subtitles "She seems not totally happy about it, but she isn't displeased either."
                        $ change_stat("happiness", -0.2, "high_school")
                        $ change_stat("corruption", 0.1, "high_school")
                        $ change_stat("inhibition", 0.3, "high_school")
                        jump new_daytime
                    elif 5 <= level <= 7:
                        Subtitles "The girl is suprised but enjoys it very much. Her moans can be heard across the hallway."
                        $ change_stat("happiness", 0.5, "high_school")
                        $ change_stat("corruption", 0.4, "high_school")
                        jump new_daytime
                    elif level >= 8:
                        Subtitles "The girl is extremely happy about her situation. After seeing you the other girls step in to join."
                        Subtitles "They are now a mass of fucking, kissing and licking bodies."
                        $ change_stat("happiness", 0.1, "high_school")
                        $ change_stat("corruption", 0.8, "high_school")
                        jump new_daytime
                "Anal" if level >= 7 and trip_variant == 2:
                    Subtitles "You take hold of this situation. Push away the underwear and push your dick into her ass."
                    if level <= 8:
                        Subtitles "The girl screams silently. It seems to hurt her a little. After a while she seems to like it but she is a little bit angry about you."
                        $ change_stat("happiness", -0.2, "high_school")
                        $ change_stat("corruption", 1, "high_school")
                        jump new_daytime
                    elif level >= 9:
                        Subtitles "The girls gasps shortly because of the pain. But she is definetly into it."
                        $ change_stat("happiness", 0.2, "high_school")
                        $ change_stat("corruption", 1.3, "high_school")
                        jump new_daytime

label hsb_patrol_collide:
    call hsb_patrol_intro_variants

    $ level = schools["high_school"].get_level()
    $ variant = renpy.random.randint(1, 3)

    Subtitles "As you turn around the corner, you collide with a student that seemingly ran too fast through the hallway."
    if variant == 1:
        jump .patrol_trip_check1
    elif variant == 2:
        Subtitles "You both fall. After you open your eyes you see yourself lying on top of the girl that ran into you."
        menu:
            Subtitles "How do you react?"
            "Stand up":
                if level <= 3:
                    Subtitles "You stand up and pat the dust from your clothing. After that, you help the girl get up."
                    Subtitles "The girl thanks you and you both continue to go your ways."
                    $ change_stat("happiness", 0.3, "high_school")
                    jump new_daytime
                elif 4 <= level <= 6:
                    Subtitles "You stand up and help the girl. She then presents you her boobs as a thank you."
                    $ change_stat("happiness", 0.7, "high_school")
                    jump new_daytime
                elif level >= 7:
                    Subtitles "You stand up and hold out your hand to help the girl. But she helps herself with your dick and gives you a blowjob."
                    $ change_stat("corruption", 0.2, "high_school")
                    jump new_daytime
            "'Are you okay?'":
                if level <= 3:
                    char_Principal "Are you okay?"
                    char_SGirl "Yes, but could you please get off me?"
                    char_Principal "O-Of course, excuse me!"
                    $ change_stat("happiness", -0.2, "high_school")
                    $ change_stat("inhibition", 0.2, "high_school")
                    jump new_daytime
                if 4 <= level <= 6:
                    char_Principal "Are you okay?"
                    char_SGirl "Yes, thank you!" 
                    #image kiss
                    $ change_stat("happiness", 0.6, "high_school")
                    $ change_stat("inhibition", 0.4, "high_school")
                    jump new_daytime
                if level >= 7:
                    $ variant = renpy.random.randint(1, 2)
                    char_Principal "Are you okay?"
                    #girl grabs crotch
                    char_SGirl "Oh yeah I'm okay!"
                    #girl kiss
                    $ change_stat("happiness", 0.8, "high_school")
                    $ change_stat("inhibition", 0.8, "high_school")
                    if variant == 1:
                        char_SGirl "If we're like this, we could also just do it."
                        $ change_stat("corruption", 0.4, "high_school")
                    jump new_daytime
            "Grope":
                if level <= 3:
                    Subtitles "You take the opportunity and grab the girls breast."
                    char_Principal "Oh I'm sorry, I just landed quite unfortunate."
                    char_SGirl "The girl is not convinced and throws you off her."
                    $ change_stat("happiness", -0.5, "high_school")
                    $ change_stat("inhibition", 0.4, "high_school")
                    $ change_stat("corruption", 0.2, "high_school")
                    jump new_daytime
                if 4 <= level <= 6:
                    Subtitles "You grab the girls breast."
                    char_SGirl "Mhh! Do you like them?" 
                    $ change_stat("inhibition", 0.6, "high_school")
                    $ change_stat("corruption", 0.3, "high_school")
                    jump new_daytime
                if level >= 7:
                    Subtitles "You start kneading her breasts."
                    char_SGirl "Oh yeah that's good!"
                    char_SGirl "Let's just do it right here!"
                    $ change_stat("inhibition", 0.9, "high_school")
                    $ change_stat("corruption", 0.5, "high_school")
                    jump new_daytime
    else:
        Subtitles "The girl knocks you off, you fall and the girl on top."
        $ variant = renpy.random.randint(1, 11)
        $ variant2 = renpy.random.randint(1, 2)
        if variant <= 3:
            Subtitles "She now sits on your lap."
            char_Principal "Are you okay?"
            if level <= 3:
                char_SGirl "Y-yes! Thank you!"
                $ change_stat("happiness", 0.4, "high_school")
                jump new_daytime
            elif level <= 6:
                char_SGirl "Oh I am more than alright!"
                #kiss and greeting
                $ change_stat("happiness", 0.6, "high_school")
                $ change_stat("inhibition", 0.2, "high_school")
                jump new_daytime
            elif level >= 7:
                char_SGirl "Oh I'm sure this is fate."
                # grabs crotch
                $ change_stat("happiness", 0.8, "high_school")
                $ change_stat("inhibition", 0.6, "high_school")
                if variant2 == 2:
                    #sex
                    $ change_stat("corruption", 0.4, "High_school")
                jump new_daytime
        elif variant <= 6:
            Subtitles "She now sits on your lap. The Boner in your pants pressing against her."
            char_Principal "Are you okay?"
            if level <= 3:
                char_SGirl "W-What is that thing poking me down there?"
                char_Principal "Oh. I'm sorry, that's my... I mean... You are very cute, so..."
                char_SGirl "Eeek!"
                $ change_stat("inhibition", 0.3, "high_school");
                $ change_stat("happiness", -0.3, "high_school");
                jump new_daytime
            elif level <= 6:
                char_SGirl "Oh is that a banana, or are you happy to see me?"
                char_SGirl "In any case, I hope you're happy to see these."
                # show boobs
                $ change_stat("inhibition", 0.5, "high_school");
                $ change_stat("happiness", 0.3, "high_school");
                jump new_daytime
            elif level >= 7:
                char_SGirl "Oh someone wants some action, I guess."
                # sex
                $ change_stat("inhibition", 0.8, "high_school");
                $ change_stat("corruption", 0.3, "high_school");
                jump new_daytime
        elif variant <= 8:
            Subtitles "As you open your eyes. All you see are panties. The ones from the girl lying on top of you."
            if level <= 4:
                Subtitles "The girl straightens up. Only after you try talking and the girls starts to feel a little tingling on her pussy. She jumps up and runs away blushing and screaming."
                $ change_stat("inhibition", 0.6, "high_school");
                $ change_stat("happiness", -0.3, "high_school");
                jump new_daytime
            elif level <= 7:
                Subtitles "The girl seems to be a bit fixated on your crotch, before she opens your pants and gives you a handjob."
                Subtitles "Likewise you start fingering her pussy."
                $ change_stat("inhibition", 0.8, "high_school");
                $ change_stat("corruption", 0.4, "high_school");
                jump new_daytime
            elif level >= 8:
                Subtitles "The girl seems to take that as an invitation to open your pants and suck your dick."
                Subtitles "You pull the panties aside and start licking her pussy."
                $ change_stat("inhibition", 1, "high_school");
                $ change_stat("corruption", 0.6, "high_school");
                jump new_daytime
        elif variant <= 10:
            Subtitles "Your pants seemed to be open as now the girl is sitting on your lap with your naked dick poking her in the panties."
            if level <= 4:
                Subtitles "The girl starts blushing as she notices the tip of your penis penetrating her pussy through her panties."
                Subtitles "She quickly jumps up and runs away screaming."
                $ change_stat("inhibition", 0.7, "high_school")
                $ change_stat("happiness", -2, "high_school")
                jump new_daytime
            elif level <= 7:
                char_SGirl "I appreciate your attempt but that seems a little bit fast, doesn't it?"
                Subtitles "She gets of your dick but grabs it."
                char_SGirl "Better start small."
                # handjob
                $ change_stat("inhibition", 1, "high_school")
                $ change_stat("corruption", 0.5, "high_school")
                $ change_stat("happiness", -0.3, "high_school")
                jump new_daytime
            elif level >= 8:
                char_SGirl "You careful quickpants! You gotta remove the panties first!"
                # sex
                $ change_stat("inhibition", 1.2, "high_school")
                $ change_stat("corruption", 0.8, "high_school")
                $ change_stat("happiness", 0.6, "high_school")
                jump new_daytime
        elif variant == 11:
            Subtitles "They always laugh at you when you say that. But here it really happens. She literally fell on your dick."
            if level <= 4:
                Subtitles "The girl seems to be speechless. Either she is baffled by the situation or overwhelmed by pleasure."
                Subtitles "She tries to get off but she slips and again rams your dick into her pussy."
                Subtitles "She starts twitching and passes out."
                $change_stat("inhibition", 1.5, "high_school")
                $change_stat("corruption", 1, "high_school")
                $change_stat("happiness", -4, "high_school")
                jump new_daytime
            elif level <= 6:
                char_SGirl "Whaaaa...?! What are you doing, you can't just do that! I'd like to play with you but not this much!"
                $change_stat("inhibition", 0.9, "high_school")
                $change_stat("corruption", 0.6, "high_school")
                $change_stat("happiness", -1, "high_school")
                jump new_daytime
            elif level >= 7:
                Subtitles "The girl twitches. She apparently came from the sudden penetration."
                Subtitles "A few seconds later she starts riding your dick."
                $change_stat("inhibition", 0.8, "high_school")
                $change_stat("corruption", 0.5, "high_school")
                $change_stat("happiness", 0.5, "high_school")
                jump new_daytime



# student talk events

label hsb_talk_students_1:
    Subtitles "You approach a few students."
    Subtitles "But as soon as you get close to the students, they scurry around the corner."
    jump new_daytime

label hsb_talk_students_2:
    Subtitles "You see a few students and move over to talk to them."
    Subtitles "You have a deep discussion about the school and their life in this school."
    Subtitles "The students are visibly happy to have a headmaster they can talk to."
    $ change_stat("happiness", 0.25, "high_school")
    jump new_daytime

label hsb_talk_students_3:
    Subtitles "You see a few students and move over to talk to them."
    Subtitles "The students have a few issues about the school that they want to talk to you about."
    Subtitles "You discuss a few points with them."
    Subtitles "The students are visibly happy to have a headmaster who cares about their concerns."
    $ change_stat("happiness", 0.4, "high_school")
    jump new_daytime

    

###########################################

###########################################
# ----- High School Building Scenes ----- #
###########################################


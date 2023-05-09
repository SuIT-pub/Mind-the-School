#########################################################
# ----- High School Dormitory Event Handler ----- #
#########################################################

init -10 python:
    high_school_dormitory_events = {}

    high_school_dormitory_events["fallback"] = "high_school_dormitory_fallback"

    # event check before menu
    high_school_dormitory_events["high_school_dormitory"] = {
        "fallback": "high_school_dormitory.after_time_check", # no event
    }

    high_school_dormitory_events["check_rooms"] = {
        "fallback": "high_school_dormitory_person_fallback",
        "x.x.x.f.d.x:x:x.0": [
            "hsd_check_room_1",
        ],
        "x.x.x.x.w.x:x:x.0": [
            "hsd_check_room_1",
        ]
    }

    high_school_dormitory_events["talk"] = {
        "fallback": "high_school_dormitory_person_fallback",
    }

    high_school_dormitory_events["patrol"] = {
        "fallback": "high_school_dormitory_person_fallback",
    }

    high_school_dormitory_events["peek"] = {
        "fallback": "high_school_dormitory_person_fallback",
    }

#######################################################
# ----- High School Dormitory Entry Point ----- #
#######################################################

label high_school_dormitory:
    # show dorm corridor

    # if daytime in [1, 3, 6]:
    #     # show corridor filled with students and open doors
    # if daytime in [2, 4, 5]:
    #     # show empty corridor
    # if daytime in [7]:
    #     # show empty corridor at night

    call event_check_area("high_school_dormitory", high_school_dormitory_events)

label.after_time_check:

    $ check_events = [
        get_events_area_count("check_rooms", high_school_dormitory_events),
        get_events_area_count("talk"       , high_school_dormitory_events),
        get_events_area_count("patrol"     , high_school_dormitory_events),
        get_events_area_count("peek"       , high_school_dormitory_events),
    ]

    if any(check_events):
        menu:
            Subtitles "What to do in the High School Dorm?"
            
            "Check rooms" if check_events[0] > 0:
                call event_check_area("check_rooms", high_school_dormitory_events)
            "Talk to students" if check_events[1] > 0:
                call event_check_area("talk", high_school_dormitory_events)
            "Patrol building" if check_events[2] > 0:
                call event_check_area("patrol", high_school_dormitory_events)
            "Peek on students" if check_events[3] > 0:
                call event_check_area("peek", high_school_dormitory_events)
            "Return":
                jump map_overview
    else:
        call high_school_building_fallback
        jump map_overview

    jump high_school_dormitory

#####################################################
# ----- High School Dormitory Fallback Events ----- #
#####################################################

label high_school_dormitory_fallback:
    Subtitles "There is nothing to do here."
    return

label high_school_dormitory_person_fallback:
    Subtitles "There is nobody here."
    return

############################################
# ----- High School Dormitory Events ----- #
############################################

label hsd_check_room_1:
    Subtitles "You knock on one of the dorm rooms. Nobody opens."
    Subtitles "You hold your ear on the door but you hear nothing!"

    menu:
        "Enter Room":
            jump hsd_check_room_1.enter_room_all
        "Knock":
            jump hsd_check_room_1.knock_room
        "Leave":
            jump new_daytime
    jump new_daytime

label .knock_room:
    $ variant = renpy.random.randInt(1, 2)
    if variant == 1:
        Subtitles "You knock but nobody answers."
        menu:
            Subtitles "What do you do?"
            "Enter room":
                jump hsd_check_room_1.enter_room_empty
            "Leave":
                jump new_daytime
        jump new_daytime
    if variant == 2:
        char_SGirl "Enter!"
        menu:
            Subtitles "What do you do?"
            "Enter room":
                jump hsd_check_room_1.enter_room_girl
            "Leave":
                jump new_daytime
        jump new_daytime
    jump new_daytime
    

label .enter_room_empty:
    Subtitles "You enter the room."
    $ variant = renpy.random.randInt(1, 3)
    if variant == 1:
        jump hsd_check_room_1.enter_room_empty_empty
    if variant == 2:
        jump hsd_check_room_1.enter_room_empty_clothing
    jump new_daytime

label .enter_room_all:
    Subtitles "You enter the room."
    $ variant = renpy.random.randInt(1, 3)
    if variant == 1:
        jump hsd_check_room_1.enter_room_empty_empty
    if variant == 2:
        jump hsd_check_room_1.enter_room_empty_clothing
    if variant == 3:
        jump hsd_check_room_1.enter_room_girl_dressing
    jump new_daytime

label .enter_room_empty_empty:
    Subtitles "The room is empty. You can't find anything interesting."
    jump new_daytime
label .enter_room_empty_clothing:
    Subtitles "The room is empty but there is clothing lying around everywhere."
    menu:
        Subtitles "What to do?"
        "Steal panties":
            jump hsd_check_room_1.enter_room_steal_panties
        "Steal bras":
            jump hsd_check_room_1.enter_room_steal_bras
        "Leave":
            jump new_daytime
    jump new_daytime
label .enter_room_girl_dressing:
    Subtitles "You get greeted by a half naked student in the process of dressing up."
    char_SGirl "EEEK! Get out!"
    $ change_stat("inhibition", 0.1, "high_school")
    $ change_stat("corruption", 0.02, "high_school")
    $ change_stat("happiness", -0.1, "high_school")
    jump new_daytime

label .enter_room_girl:
    Subtitles "As you enter you get greeted by a student. You talk a little bit before you leave again."
    jump new_daytime

label .enter_room_steal_panties:
    Subtitles "You quickly take some panties."
    jump new_daytime

label .enter_room_steal_bras:
    Subtitles "You quickly take some bras."
    jump new_daytime


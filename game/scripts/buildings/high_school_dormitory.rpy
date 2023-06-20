#########################################################
# ----- High School Dormitory Event Handler ----- #
#########################################################

init -10 python:
    high_school_dormitory_events = {}
    high_school_dormitory_events_title = {
        "check_rooms": "Check Rooms",
        "talk_students": "Talk to students",
        "patrol": "Patrol building",
        "peek_students": "Peek on students",
    }

    high_school_dormitory_events["fallback"] = "high_school_dormitory_fallback"

    # event check before menu
    create_event_area(high_school_dormitory_events, "high_school_dormitory", "high_school_dormitory.after_time_check")

    create_event_area(high_school_dormitory_events, "check_rooms", "high_school_dormitory_person_fallback")
    add_area_event(high_school_dormitory_events, "check_rooms", "x.x.x.f.d.x:x:x.0", "hsd_check_room_1")
    add_area_event(high_school_dormitory_events, "check_rooms", "x.x.x.x.w.x:x:x.0", "hsd_check_room_1")

    create_event_area(high_school_dormitory_events, "talk", "high_school_dormitory_person_fallback")
    create_event_area(high_school_dormitory_events, "patrol", "high_school_dormitory_person_fallback")
    create_event_area(high_school_dormitory_events, "peek", "high_school_dormitory_person_fallback")

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

label .after_time_check:

    call call_event_menu (
        "What to do in the High School Dorm?",
        1, 
        7, 
        high_school_dormitory_events, 
        high_school_dormitory_events_title,
        "fallback", "high_school_dormitory"
    )

    jump high_school_dormitory

#####################################################
# ----- High School Dormitory Fallback Events ----- #
#####################################################

label high_school_dormitory_fallback:
    subtitles "There is nothing to do here."
    return

label high_school_dormitory_person_fallback:
    subtitles "There is nobody here."
    return

############################################
# ----- High School Dormitory Events ----- #
############################################

label hsd_check_room_1:
    subtitles "You knock on one of the dorm rooms. Nobody opens."
    subtitles "You hold your ear on the door but you hear nothing!"

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
        subtitles "You knock but nobody answers."
        menu:
            subtitles "What do you do?"
            "Enter room":
                jump hsd_check_room_1.enter_room_empty
            "Leave":
                jump new_daytime
        jump new_daytime
    if variant == 2:
        sgirl "Enter!"
        menu:
            subtitles "What do you do?"
            "Enter room":
                jump hsd_check_room_1.enter_room_girl
            "Leave":
                jump new_daytime
        jump new_daytime
    jump new_daytime
    

label .enter_room_empty:
    subtitles "You enter the room."
    $ variant = renpy.random.randInt(1, 3)
    if variant == 1:
        jump hsd_check_room_1.enter_room_empty_empty
    if variant == 2:
        jump hsd_check_room_1.enter_room_empty_clothing
    jump new_daytime

label .enter_room_all:
    subtitles "You enter the room."
    $ variant = renpy.random.randInt(1, 3)
    if variant == 1:
        jump hsd_check_room_1.enter_room_empty_empty
    if variant == 2:
        jump hsd_check_room_1.enter_room_empty_clothing
    if variant == 3:
        jump hsd_check_room_1.enter_room_girl_dressing
    jump new_daytime

label .enter_room_empty_empty:
    subtitles "The room is empty. You can't find anything interesting."
    jump new_daytime
label .enter_room_empty_clothing:
    subtitles "The room is empty but there is clothing lying around everywhere."
    menu:
        subtitles "What to do?"
        "Steal panties":
            jump hsd_check_room_1.enter_room_steal_panties
        "Steal bras":
            jump hsd_check_room_1.enter_room_steal_bras
        "Leave":
            jump new_daytime
    jump new_daytime
label .enter_room_girl_dressing:
    subtitles "You get greeted by a half naked student in the process of dressing up."
    sgirl "EEEK! Get out!"
    $ change_stat("inhibition", 0.1, "high_school")
    $ change_stat("corruption", 0.02, "high_school")
    $ change_stat("happiness", -0.1, "high_school")
    jump new_daytime

label .enter_room_girl:
    subtitles "As you enter you get greeted by a student. You talk a little bit before you leave again."
    jump new_daytime

label .enter_room_steal_panties:
    subtitles "You quickly take some panties."
    jump new_daytime

label .enter_room_steal_bras:
    subtitles "You quickly take some bras."
    jump new_daytime


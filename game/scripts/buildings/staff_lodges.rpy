##########################################
# ----- Staff Lodges Event Handler ----- #
##########################################

init -1 python:
    def staff_lodges_events_available() -> bool:
        return (staff_lodges_timed_event.has_available_highlight_events() or 
            staff_lodges_general_event.has_available_highlight_events() or 
            any(e.has_available_highlight_events() for e in staff_lodges_events.values()))

    staff_lodges_timed_event = TempEventStorage("staff_lodges_timed", "staff_lodges", fallback = Event(2, "staff_lodges.after_time_check"))
    staff_lodges_general_event = EventStorage("staff_lodges_general", "staff_lodges", fallback = Event(2, "staff_lodges.after_general_check"))
    staff_lodges_events = {}

    staff_lodges_bg_images = BGStorage("images/background/staff_lodges/bg c.webp", ValueSelector('loli', 0),
        BGImage("images/background/staff_lodges/bg 1,3 <loli> <level> <nude>.webp", 1, TimeCondition(daytime = "1,3")), # show bath with students
        BGImage("images/background/staff_lodges/bg 6 <loli> <level> <nude>.webp", 1, TimeCondition(daytime = 6)), # show bath with students and/or teacher
        BGImage("images/background/staff_lodges/bg 7.webp", 1, TimeCondition(daytime = 7)), # show bath at night empty or with teachers
    )
    
init 1 python:
    
    staff_lodges_action_tutorial_event = Event(2, "action_tutorial",
        NOT(ProgressCondition('action_tutorial')),
        ValueSelector('return_label', 'staff_lodges'),
        NoHighlightOption(),
        TutorialCondition(),
        override_location = "misc", thumbnail = "images/events/misc/action_tutorial 0.webp")

    staff_lodges_general_event.add_event(
        staff_lodges_action_tutorial_event
    )


##################################

########################################
# ----- Staff Lodges Entry Point ----- #
########################################

label staff_lodges ():
    call call_available_event(staff_lodges_timed_event) from staff_lodges_1

label .after_time_check (**kwargs):
    call call_available_event(staff_lodges_general_event) from staff_lodges_4

label .after_general_check (**kwargs):
    call call_event_menu (
        "What to do at the Staff Lodges?",
        staff_lodges_events,
        default_fallback,
        character.subtitles,
        bg_image = staff_lodges_bg_images,
        fallback_text = "There is nothing to see here."
    ) from staff_lodges_3

    jump staff_lodges

##################################

###################################
# ----- Staff Lodges Events ----- #
###################################


###########################
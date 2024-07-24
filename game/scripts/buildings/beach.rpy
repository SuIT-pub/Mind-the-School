###################################
# ----- Beach Event Handler ----- #
###################################

init -1 python:
    def beach_events_available() -> bool:
        return (beach_timed_event.has_available_highlight_events() or 
            beach_general_event.has_available_highlight_events() or 
            any(e.has_available_highlight_events() for e in beach_events.values()))

    beach_timed_event = TempEventStorage("beach_timed", "beach", fallback = Event(2, "beach.after_time_check"))
    beach_general_event = EventStorage("beach_general", "beach", fallback = Event(2, "beach.after_general_check"))
    beach_events = {}

    beach_bg_images = BGStorage("images/background/beach/bg c.webp", 
        BGImage("images/background/beach/bg 1,3 <loli> <level> <nude>.webp", 1, TimeCondition(daytime = "1,3")), # show bath with students
        BGImage("images/background/beach/bg 6 <loli> <level> <nude>.webp", 1, TimeCondition(daytime = 6)), # show bath with students and/or teacher
        BGImage("images/background/beach/bg 7.webp", 1, TimeCondition(daytime = 7)), # show bath at night empty or with teachers
    )
    
# init 1 python:

##################################

#################################
# ----- Beach Entry Point ----- #
#################################

label beach ():
    call call_available_event(beach_timed_event) from beach_1

label .after_time_check (**kwargs):
    call call_available_event(beach_general_event) from beach_4

label .after_general_check (**kwargs):
    $ loli = get_random_loli()

    $ beach_bg_images.add_kwargs(loli = loli)

    call call_event_menu (
        "What to do at the Beach?",
        beach_events,
        default_fallback,
        character.subtitles,
        bg_image = beach_bg_images,
        context = loli
        fallback_text = "There is nothing to see here."
    ) from beach_3

    jump beach

##################################

############################
# ----- Beach Events ----- #
############################


###########################
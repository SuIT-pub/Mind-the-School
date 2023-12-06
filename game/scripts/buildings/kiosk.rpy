###################################
# ----- Kiosk Event Handler ----- #
###################################

init -1 python:
    kiosk_timed_event = EventStorage("kiosk", "", Event(2, "kiosk.after_time_check"))
    kiosk_events = {
        "snack":    EventStorage("snack",    "Get a snack",      default_fallback, "I don't want anything."),
        "students": EventStorage("students", "Talk to students", default_fallback, "There is nobody here."),
    }
    
    kiosk_timed_event.add_event(Event(1,
        ["first_week_kiosk_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    k_event_1 = Event(3, 
        ["kiosk_event_1", "kiosk_event_2"],
        OR(TimeCondition(weekday = "d", daytime = "f"), TimeCondition(weekday="w", daytime = "d"))
    )

    k_event_3 = Event(3, 
        ["kiosk_event_3"],
        OR(TimeCondition(weekday = "d", daytime = "f"), TimeCondition(weekday="w", daytime = "d")),
        NOT(BuildingCondition("cafeteria")),
        RandomCondition(75, 100)
    )

    kiosk_events["snack"].add_event(k_event_1)
    kiosk_events["snack"].add_event(k_event_3)

    kiosk_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), kiosk_events.values())

    kiosk_bg_images = [
        BGImage("images/background/kiosk/bg f <name> <level> <nude> <variant>.webp", 2, OR(TimeCondition(daytime = "f"), TimeCondition(daytime = "c", weekday = "w"))), # show kiosk with students
        BGImage("images/background/kiosk/bg f <name> <level> <nude>.webp", 1, OR(TimeCondition(daytime = "f"), TimeCondition(daytime = "c", weekday = "w"))), # show kiosk with students
        BGImage("images/background/kiosk/bg 7.webp", 1, TimeCondition(daytime = 7)), # show kiosk at night empty
    ]
    
###################################

#################################
# ----- Kiosk Entry Point ----- #
#################################

label kiosk ():

    call call_available_event(kiosk_timed_event) from kiosk_1

label .after_time_check (**kwargs):

    $ school_obj = get_random_school()

    call show_idle_image(school_obj, "images/background/kiosk/bg c.webp", kiosk_bg_images) from kiosk_2

    call call_event_menu (
        "What to do at the Kiosk?", 
        kiosk_events, 
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from kiosk_3

    jump kiosk

#################################

############################
# ----- Kiosk Events ----- #
############################

# first week event
label first_week_kiosk_event (**kwargs):

    show first week kiosk 1 with dissolveM
    headmaster_thought "Now, somewhere here should be the kiosk..."
    show first week kiosk 2 with dissolveM
    headmaster_thought "Hmm, why is it so crowded?"

    show first week kiosk 3 with dissolveM
    headmaster "Excuse me, did something happen? Why is it so crowded here?"
    
    show first week kiosk 4 with dissolveM
    sgirl "What do you mean? It's always this full. We can't get food anywhere else than here." (name = "Lin Kato")
    
    show first week kiosk 3 with dissolveM
    headmaster "Oh I understand... Thanks."

    show first week kiosk 5 with dissolveM
    headmaster_thought "This is not acceptable. Did the former headmaster really close the kiosk?"
    headmaster_thought "That can't be right..."

    $ change_stat_for_all("reputation", 5, charList['schools'])

    $ set_building_blocked("kiosk")

    jump new_day

label kiosk_event_1 (**kwargs):
    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ variant = get_random_int(1, 2)
    $ girl = get_random_choice("Aona Komuro", "Ikushi Ito", "Gloria Goto", "Lin Kato")

    $ begin_event()

    call show_image("images/events/kiosk/kiosk_event_1 <name> <girl> <level> <variant>.webp", name = "high_school", girl = girl, variant = variant, **kwargs) from _call_show_image_1
    subtitles "For some, coffee is the only way to save the day."

    $ change_stats_with_modifier(char_obj,
        happiness = SMALL)

    jump new_daytime

label kiosk_event_2 (**kwargs):
    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ girl = get_random_choice("Hatano Miwa", "Kokoro Nakamura", "Soyoon Yamamoto")

    $ image = Image_Series("images/events/kiosk/kiosk_event_2 <name> <girl> <level> <step>.webp", name = "high_school", girl = girl, **kwargs)

    $ begin_event()

    $ image.show(0)
    sgirl "*AHHH*" (name = girl)
    $ image.show(1)
    subtitles "A girl seems to have spilt her drink down her blouse."
    $ image.show(2)
    subtitles "Luckily she doesn't notice her see-through blouse in all the excitement."

    $ change_stats_with_modifier(char_obj,
        happiness = DEC_TINY, inhibition = DEC_MEDIUM, corruption = TINY)

    jump new_daytime

label kiosk_event_3 (**kwargs):
    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ topic = get_random_choice("normal", (0.25, "kind"), (0.05, "slimy"))
    $ girl = "Miwa Igarashi"

    $ kwargs["topic"] = topic

    $ image = Image_Series("images/events/kiosk/kiosk_event_3 <name> <level> <step>.webp", name = "high_school", **kwargs)

    $ begin_event()

    $ image.show(0)
    sgirl "Hi, I want a Bento!" (name = girl)
    $ image.show(1)
    vendor "Sure that makes 2.50$"
    $ image.show(2)
    sgirl "2.50?! It has been only 1.50$ last week?" (name = girl)
    $ image.show(3)
    vendor "I'm sorry, but I can no longer afford to keep the prices so low."
    $ image.show(2)
    sgirl "But I can't afford that!" (name = girl)

    $ call_custom_menu_with_text("What do you do?", character.subtitles, False,
        ("Leave alone", "kiosk_event_3.leave"),
        ("Help her out", "kiosk_event_3.help"), 
    **kwargs)

label .leave (**kwargs):
    if kwargs["topic"] == "slimy":
        $ image.show(4)
        vendor "You know what? I think I could help you."
        $ image.show(5)
        sgirl "Really?" (name = girl)
        $ image.show(6)
        vendor "Yeah you could, you know have my Hot Dog."
        $ image.show(7)
        sgirl "Your Hot Dog? What do you m..." (name = girl)
        $ image.show(8)
        sgirl "Eeek! Pervert!" (name = girl)
        $ image.show(9)
        headmaster_thought "Mhh what kind of noise is that? Hmmm... I guess it's nothing serious."

        $ change_stats_with_modifier(kwargs[CHAR],
            happiness = DEC_LARGE, charm = DEC_MEDIUM, reputation = DEC_SMALL)
        jump new_daytime
        
    elif kwargs["topic"] == "kind":
        $ image.show(10)
        vendor "I'm sorry to hear that... You know what? This one is on the house."
        $ image.show(11)
        sgirl "Really? Thank you." (name = girl)
        $ image.show(12)
        headmaster_thought "Mhh, things are worse than I thought. I can't believe the students have to go hungry."
        headmaster_thought "I should think about doing something about that."

        $ change_stats_with_modifier(kwargs[CHAR],
            happiness = DEC_SMALL, charm = TINY)
    
        if get_progress("unlock_cafeteria") == -1:
            $ start_progress("unlock_cafeteria")

        jump new_daytime
    else:
        $ image.show(10)
        vendor "I'm sorry but there is nothing I can do."
        $ image.show(13)
        sgirl "*sob*" (name = girl)
        $ image.show(12)
        headmaster_thought "Poor girl..."

        $ change_stats_with_modifier(kwargs[CHAR],
            happiness = DEC_MEDIUM, charm = DEC_SMALL)
        jump new_daytime

label .help (**kwargs):
    $ image.show(14)
    headmaster "What's the matter here?"
    $ image.show(15)
    sgirl "Oh Mr. [headmaster_last_name]... nothing..." (name = girl)
    $ image.show(16)
    headmaster "I'll pay her meal and please add a coffee."
    $ image.show(17)
    headmaster "Do you drink coffee?"
    sgirl "Yes?" (name = girl)
    $ image.show(18)
    headmaster "Good, coffee then."
    $ image.show(19)
    vendor "Sure!"
    $ image.show(20)
    sgirl "Thank you very much!" (name = girl)
    $ image.show(21)
    headmaster "No problem. I know it can be hard, but if you are in a predicament just come talk to me and I'm sure we can find a way." 
    $ image.show(22)
    sgirl "..." (name = girl)

    $ change_stats_with_modifier(kwargs[CHAR],
        happiness = MEDIUM, reputation = MEDIUM, charm = DEC_TINY)
    jump new_daytime

    

############################
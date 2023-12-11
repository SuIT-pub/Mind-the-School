###################################################
# ----- High School Dormitory Event Handler ----- #
###################################################

init -1 python:
    sd_timed_event = EventStorage("school_dormitory", "", Event(2, "school_dormitory.after_time_check"))
    sd_events = {
        "check_rooms":   EventStorage("check_rooms",   "Check Rooms",      default_fallback, "There is nobody here."),
        "talk_students": EventStorage("talk_students", "Talk to students", default_fallback, "There is nobody here."),
        "patrol":        EventStorage("patrol",        "Patrol building",  default_fallback, "There is nobody here."),
        "peek_students": EventStorage("peek_students", "Peek on students", default_fallback, "There is nobody here."),
    }

    sd_timed_event.add_event(Event(1,
        ["first_week_school_dormitory_event"],
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))

    sd_timed_event.add_event(Event(1,
        ["first_potion_school_dormitory_event"],
        TimeCondition(day = 9, month = 1, year = 2023),
    ))

    event1 = Event(3, 
        ["sd_event_1", "sd_event_2"],
        OR(
            TimeCondition(weekday = "d", daytime = "f"), 
            TimeCondition(weekday = "d", daytime = "n"), 
            TimeCondition(weekday = "w")
        )
    )

    # hsd_events["check_rooms"].add_event(event1)
    sd_events["peek_students"].add_event(event1)

    sd_timed_event.check_all_events()
    map(lambda x: x.check_all_events(), sd_events.values())

    school_dormitory_bg_images = [
        BGImage("images/background/school dormitory/bg f <level> <nude>.webp", 1, TimeCondition(daytime = "f")),
        BGImage("images/background/school dormitory/bg f <level> <nude>.webp", 1, TimeCondition(daytime = "c", weekday = "w")),
        BGImage("images/background/school dormitory/bg 7.webp", 1, TimeCondition(daytime = 7)),
    ]
    
###################################################

############################################
# ----- School Dormitory Entry Point ----- #
############################################

label school_dormitory ():
    
    call call_available_event(sd_timed_event) from school_dormitory_1

label .after_time_check (**kwargs):

    $ school_obj = get_school()

    call show_idle_image(school_obj, "images/background/school dormitory/bg c.webp", school_dormitory_bg_images) from school_dormitory_2

    call call_event_menu (
        "What to do in the High School Dorm?", 
        hsd_events, 
        default_fallback,
        character.subtitles,
        char_obj = school_obj,
    ) from school_dormitory_3

    jump school_dormitory

#################################################

#######################################
# ----- School Dormitory Events ----- #
#######################################


# first week event
label first_week_school_dormitory_event (**kwargs):
    show first week high school dormitory 1 with dissolveM
    headmaster_thought "The dormitory looks alright."

    show first week high school dormitory 2 with dissolveM
    headmaster_thought "As far as I know, the students have to share a communal bathroom."
    headmaster_thought "Private bathrooms would be nice for the students, but for one I don't think we really need that and then it would need a lot of rebuilding. So that should be last on the list."
    
    show first week high school dormitory 3 with dissolveM
    headmaster_thought "Let's see if someone would let me see their room so I can check the state of these."
    
    show first week high school dormitory 4 with dissolveM
    headmaster "Hello? I'm Mr. [headmaster_last_name] the new Headmaster. Can I come in? I'm here to inspect the building."
    subtitles "..."
    headmaster "Hello?"

    show first week high school dormitory 5 with dissolveM
    headmaster_thought "Hmm nobody seems to be here. Nevermind. I just let my Secretary give me a report."

    $ change_stat_for_all("inhibition", -3, charList["schools"])
    $ change_stat_for_all("happiness", 3, charList["schools"])

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_day


label first_potion_school_dormitory_event (**kwargs):

    show first potion dormitory 1 with dissolveM
    subtitles "You enter the dormitory of the high school."
    headmaster_thought "Mhh, where does the noise come from?"

    show first potion dormitory 2 with dissolveM
    headmaster_thought "Ah I think there are some students in the room over there."

    show first potion high school dormitory 2 with dissolveM
    headmaster_thought "Ahh party games!"

    show first potion high school dormitory 3 with dissolveM
    if time.check_daytime("c"):
        headmaster_thought "Normally I would scold them for skipping class but today is a special day so I gladly enjoy this view."
    else:
        headmaster_thought "Ahh I like this view. Nothing more erotic than nudity in combination with a party game."

    $ set_building_blocked("high_school_dormitory")
    $ set_building_blocked("middle_school_dormitory")
    $ set_building_blocked("elementary_school_dormitory")

    jump new_daytime


# education < 80
label sd_event_1 (**kwargs):
    $ image = Image_Series("images/events/school dormitory/sd_event_1 <name> <level> <step>.webp", name = "high_school", **kwargs)

    $ girl_name = "Easkey Tanaka"

    $ begin_event()

    $ char_obj = get_kwargs("char_obj", **kwargs)

    $ education = char_obj.get_stat_number(EDUCATION)
    $ inhibition = char_obj.get_stat_number(INHIBITION)

    if education > 50 and get_random_int(0, 1) == 0:
        $ image.show(0)
        sgirl "Umm, hello!" (name = girl_name)
        $ image.show(1)
        headmaster "Hello there, is everything okay?"
        if inhibition >= 90:
            $ image.show(2)
            sgirl "Yeah Mr. [headmaster_last_name], but would you please knock before entering next time?" (name = girl_name)
            $ image.show(3)
            headmaster "Ah yes... yes of course."
            $ change_stats_with_modifier(char_obj,
                HAPPINESS = DEC_TINY)
            jump new_daytime
        else:
            $ image.show(5)
            sgirl "Yeah Mr. [headmaster_last_name], you just surprised me." (name = girl_name)
            $ image.show(6)
            headmaster "Oh, sorry about that."
            $ change_stats_with_modifier(char_obj,
                HAPPINESS = DEC_TINY, education = MEDIUM)
            jump new_daytime
    else:
        $ image.show(4)
        sgirl "hmm... This homework is hard. Why do I need to learn this anyway?" (name = girl_name)
        $ change_stats_with_modifier(char_obj,
            education = SMALL)
        jump new_daytime

label sd_event_2 (**kwargs):
    $ char_obj = get_kwargs("char_obj", **kwargs)
    $ inhibition = char_obj.get_stat_number(INHIBITION)

    $ location = get_random_choice("dorm_room", "shower")
    $ topic = []

    $ topic_set = 1 if inhibition > get_random_int(30, 50) else 2

    if topic_set == 1:
        $ topic = ["ah", "ahhh", "oh", "eeek", (0.05, "panties"), (0.02, "breasts")]
    else:
        $ topic = ["guys_stop", "huh", "reason", "dressing", "blush"]

    $ topic = get_random_choice(*topic)
    
    $ girl_name = get_random_choice("Aona Komuro", "Lin Kato", "Gloria Goto")

    if location == "shower":
        $ girl_name = get_random_choice("Sakura Mori", "Elsie Johnson", "Ishimaru Maki")

    $ image = Image_Series("images/events/school dormitory/sd_event_2 <name> <topic> <location> <girl> <level> <step>.webp", name = "high_school", location = location, topic = topic, girl = girl_name, **kwargs)
    $ image2 = Image_Series("images/events/school dormitory/sd_event_2 <location> <step>.webp", location = location)

    $ begin_event()

    if topic == "ah":
        $ image.show(0)
        sgirl "Ah!" (name = girl_name)
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_TINY, inhibition = DEC_TINY)
    elif topic == "ahhh":
        $ image.show(0)
        sgirl "AHHH!!!" (name = girl_name)
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_TINY, inhibition = DEC_TINY, reputation = DEC_TINY)
    elif topic == "eeek":
        $ image.show(0)
        sgirl "Eek!" (name = girl_name)
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_LARGE, inhibition = DEC_TINY)
    elif topic in ["panties", "breasts"]:
        $ image.show(0)
        $ random_say(
            "Ah!!! Look away, please, you can see my [topic]!",
            "Ah!!! Look away, please, I don't want guys seeing my [topic]!",
            "Eek! Stop! Don't stare at my [topic]!",
            person = character.sgirl, name = girl_name)
        $ change_stats_with_modifier(char_obj,
            happiness = DEC_LARGE, inhibition = DEC_TINY, charm = MEDIUM)
    elif topic == "oh":
        $ image.show(0)
        sgirl "Oh!" (name = girl_name)
        $ image.show(1)
        headmaster "I'm terribly sorry."
        $ image.show(2)
        sgirl "I-it's ok..." (name = girl_name)
        $ image.show(3)
        subtitles "You quickly make an exit."
        $ change_stats_with_modifier(char_obj,
            inhibition = DEC_TINY, happiness = DEC_MEDIUM)
        jump new_daytime
    # elif topic == "guys_stop":
    #     $ image.show(0)
    #     sgirl "Excuse me!\n Can you guys stop running in and out of here?!"
    #     $ change_stats_with_modifier(char_obj,
    #         inhibition = DEC_TINY, morale = DEC_SMALL)
    # elif topic == "huh":
    #     $ image.show(0)
    #     $ random_say(
    #         ("Umm... What are you doing in here?", character.sgirl),
    #         ("Mr. [headmaster_last_name]? What are you doing in here?", character.sgirl),
    #     )
    #     $ change_stats_with_modifier(char_obj,
    #         inhibition = DEC_TINY, morale = DEC_SMALL)
    # elif topic == "reason":
    #     $ image.show(0)
    #     sgirl "Hey Mr. [headmaster_last_name]!"
    #     $ image.show(1)
    #     headmaster "Hello there!"
    #     $ image.show(2)
    #     if get_random_int(0, 1000) == 0:
    #         sgirl "General Kenobi!"
    #     sgirl "Any particular reason I get a visit?"
    #     $ image.show(3)
    #     headmaster "Oh no, I just saw an open door and..."
    #     $ image.show(4)
    #     sgirl "Oh, silly me, would you mind closing it on your way out?"
    #     $ image.show(5)
    #     headmaster "No problem."
    #     $ change_stats_with_modifier(char_obj,
    #         charm = MEDIUM, inhibition = DEC_MEDIUM);
    #     jump new_daytime;
    # elif topic == "blush":
    #     $ image.show(0)
    #     $ random_say(
    #         ("Ah! What are you doing here?", character.sgirl),
    #         ("Oh! Mr. [headmaster_last_name]!"),
    #     )
    #     $ change_stats_with_modifier(char_obj,
    #         charm = MEDIUM, inhibition = DEC_MEDIUM)
    # elif topic == "dressing":
    #     $ image.show(0)
    #     $ random_say(
    #         ("Umm, do you mind?", character.sgirl),
    #         ("I'm getting dressed! GET OUT!", character.sgirl),
    #     )
    #     $ change_stats_with_modifier(char_obj,
    #         inhibition = DEC_TINY, charm = SMALL)

    
    $ random_say(
        ("Oh, wrong door, bye!", 0),
        ("Sorry, I'm leaving!", 0),
        ("So sorry!", topic_set == 1, 0),
        ("I'm terribly sorry!", topic_set == 1, 0),
        ("I'm leaving, I'm leaving!", topic_set == 1,  0),
        ("You hastily beat a retreat.", character.subtitles, topic_set == 1, 1),
        ("Good view, bad timing.", character.subtitles, topic_set == 1, 1),
        person = character.headmaster, image = image2)
        # ("Oh, sorry.", topic_set == 2),
        # ("Oh, sorry about that!", topic_set == 2),
        # ("Sorry miss, wrong door obviously!", topic_set == 2),
        # ("Nice view, wrong door. Sorry!", topic_set == 2),
        # ("Bad timing I see. Sorry about that!", topic_set == 2),
        # ("After a quick look at the sexy girl, you apologize and leave.", character.subtitles, topic_set == 2),
        # ("A nice view, but you quickly leave anyway.", character.subtitles, topic_set == 2),

    jump new_daytime

label sd_event_3 (**kwargs):
    $ char_obj = get_kwargs("char_obj", **kwargs)
    $ inhibition = char_obj.get_stat_number(INHIBITION)

    $ topic = get_random_choice("normal", (0.1, "panties"), (0.02, "nude"))

    $ image = Image_Series("images/events/school dormitory/sd_event_3 <name> <topic> <level> <step>.webp", name = "high_school", topic = topic, **kwargs)

    $ begin_event()

    # if inhibition >= 80:
    $ image.show(0)
    subtitles "Looks like some of the students are ready to bunk."
    headmaster "I'm sorry, I didn't realize..."
    $ image.show(1)
    sgirl "Mm- Mr. [headmaster_last_name]"
    $ image.show(0)
    headmaster "Bye!"
    
    if topic == "normal":
        $ change_stats_with_modifier(char_obj, inhibition = DEC_SMALL)
    elif topic == "panties":
        $ change_stats_with_modifier(char_obj, inhibition = DEC_MEDIUM)
    elif topic == "nude":
        $ change_stats_with_modifier(char_obj, inhibition = DEC_LARGE)

    jump new_daytime







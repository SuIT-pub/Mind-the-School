#############################################
# ----- Office Building Event Handler ----- #
#############################################

init -1 python:
    office_building_after_time_check = Event("office_building_after_time_check", "office_building.after_time_check", 2)
    office_building_fallback         = Event("office_building_fallback",         "office_building_fallback",         2)

    office_building_timed_event = EventStorage("office_building", "", office_building_after_time_check)
    office_building_events = {
        "tutorial":  EventStorage("tutorial",  "About the school...", office_building_fallback),
        "paperwork": EventStorage("paperwork", "Do paperwork",        office_building_fallback),
        "messages":  EventStorage("messages",  "Check messages",      office_building_fallback),
        "internet":  EventStorage("internet",  "Surf internet",       office_building_fallback),
        "council":   EventStorage("council",   "Council work",        office_building_fallback),
    }
    
    office_building_timed_event.add_event(Event(
        "first_week_event",
        ["first_week_office_building_event"],
        1,
        TimeCondition(day = "2-4", month = 1, year = 2023),
    ))
    
    office_building_timed_event.add_event(Event(
        "first_potion_event",
        ["first_potion_office_building_event"],
        1,
        TimeCondition(day = 9),
    ))

    office_building_bg_images = [
        BGImage("images/background/office building/bg c Teacher.jpg", 1, TimeCondition(daytime = "c"), ValueCondition('staff', 'teacher')), # show headmasters/teachers office empty
        BGImage("images/background/office building/bg f Secretary <level> <nude>.jpg", 1, TimeCondition(daytime = "c"), ValueCondition('staff', 'secretary')), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg f <staff> <level> <nude>.jpg", 1, TimeCondition(daytime = "f")), # show headmasters/teachers office with people
        BGImage("images/background/office building/bg 7 <staff>.jpg", 1, TimeCondition(daytime = 7)), # show headmasters/teachers office empty at night
    ]
    
#############################################

###########################################
# ----- Office Building Entry Point ----- #
###########################################

label office_building:

    call call_available_event(office_building_timed_event) from office_building_1

label .after_time_check:

    $ staff = get_random_choice("teacher", "secretary")

    call show_office_building_idle_image(staff) from office_building_2

    call call_event_menu (
        "Hello Headmaster! How can I help you?",
        1, 
        7, 
        office_building_events, 
        office_building_fallback,
        character.secretary,
        staff,
    ) from office_building_3

    jump office_building

label show_office_building_idle_image(staff_val):

    $ max_nude, image_path = get_background(
        "images/background/office building/bg f.jpg", # show headmasters office empty
        office_building_bg_images,
        get_level_for_char(staff_val, charList["staff"]),
        staff = staff_val
    )

    call show_image_with_nude_var (image_path, max_nude) from _call_show_image_with_nude_var_12

    return

###########################################

####################################################
# ----- High School Building Fallback Events ----- #
####################################################

label office_building_fallback:
    subtitles "There is nothing to do here."
    return

####################################################

###########################################
# ----- High School Building Events ----- #
###########################################

label first_potion_office_building_event:

    show first potion office 1 with dissolveM
    subtitles "You enter the teachers office."
    headmaster_thought "Ahh the teacher seem to be eating at the kiosk as well."
    show first potion office 2 with dissolveM
    headmaster_thought "Not that I have a problem with it. Quite the opposite. That makes some things a bit easier."

    $ set_building_blocked("office_building")

    jump new_daytime

# first week event
label first_week_office_building_event:

    show first week office building 1 with dissolveM
    subtitles "Mhh. The office is nothing special but at least not really run down."
    subtitles "I can work with that."

    $ set_building_blocked("office_building")

    jump new_day

label old_pta_meeting:
    subtitles "You enter the conference room."
    subtitles "All representatives already gathered and wait for you."
    headmaster "Thank you all for gathering today."

    headmaster "First point for today. Does someone have anything to discuss today?"

    headmaster "No? Alright then lets jump straight to the next point."

    # todo: implement PTA Meeting
    subtitles "PTA Meeting not implemented yet."

    jump new_daytime

label old_first_pta_meeting:
    subtitles "You enter the conference room."
    subtitles "All representatives already gathered and wait for you."
    headmaster "Thank you all for gathering today."

    headmaster """
        Please allow me to introduce myself as the new Headmaster of this institution as of Monday. 

        I am aware that many of you probably don't know me yet, but I hope to change that soon. 

        During my first week, I took time to gather information about the current status of the school, and it's clear 
        that there is much needed work to be done. 

        Rest assured, my goal is to get this school back on track and establish it as one of the leading academic 
        institutions in the country.
        
        My theory on how to improve the educational system has been criticised by established psychologists and 
        teachers. But I can guarantee the effectiveness.

        To give you a better understanding about me. 15 years ago I made my Diploma in Psychology, specifically 
        Educational Psychology. And over the last years I worked to revolotionize this countries educational system.

        My methods have yet to be accepted by the masses, but this is largely due to the conservative views of the 
        community and their unwillingness to change their habits and adapt to new approaches.

        To summarize my theory briefly. I aim to use the parts of the human body that no system every used. 
        
        The human body is a complex biological machine made to survive in a rough and dangerous ecosystem. So 
        originally it was built to learn new patterns and methods to give it a better chance at survival.

        Thus the human body handles informations and actions that seem to be of no use as unnecessary. And the human 
        body developed a relatively simple system to signal all kinds of information. Hormons.

        Hormons are used to deliver certain messages throughout the whole body. And I want to focus on the hormone 
        dopamine.

        Dopamine is one of the happy hormones and high concentrations of dopamine evoke a feeling of happiness. 
        Dopamine also helps transfer memories from short-term to long-term memory. And that is where my theory comes 
        into play.

        The easiest way to produce dopamine is to get intimate. Sure for some that sound like I try to just create a 
        giant harem school and sure there are other ways but I assure you my intentions are as sincere as they get and 
        I think this is a great opportunity to fix many problems that occur in our society.

        Problems that are the result of old educational methods and techniques.

        One of the main problems is the rising alienation of individuals in our society. Loneliness is becoming 
        increasingly prevalent, often due to social isolation caused by a lack of interpersonal skills and inadequate 
        support from the community.

        Unfortunately it's more that people unable to socialise become outcasts with little to no way to rehabilitate.

        My goal is to create a form of kinship and a deeper form of intimacy among the students. In a way that 
        emotional and physical support becomes the norm and to help people become more sociable and make it easier for 
        them to integrate into society.

        It was difficult to apply my theory in a big case study but the investors of this school complex reached out 
        to me and gave me the opportunity to show the effectiveness of this new method. And that will be achieved to
        make these schools the best in the country.

        If you want to learn more about my theory, please read my book. I'll happily distribute them to you if you're 
        interested.

        Of course I don't plan to run these schools alone. I wouldn't be able to handle that. That's why called this 
        group together so we can work to better these schools together!

        I plan to hold this meeting every friday in the evening so we can exchange ideas, talk about the current state 
        of the schools and discuss and vote for changes that are planned to be applied for the schools.

        To a good cooperation amd thank you all for listening.

        Now that I finished my {i}small{/i} introduction, please introduce yourself.
    """

    secretary """
        Hello everyone, I am the headmasters secretary and I will be in charge some organisational tasks like managing
        the schedule and lower beraucracy tasks.

        I already worked for the last headmaster and observed the decline of our school with my own eyes.

        If you got any questions or issues for the headmaster, please contact me. Thanks.
    """

    teacher """
        Hello, we are teachers at this school.
        
        First we are glad to have a new headmaster and we hope you bring this school back to what it once was.
    
        I am Teacher 1, currently responsible for the subjects: economics, politics, english and geography.
    """ (name="Teacher 1")
    
    teacher "I am Teacher 2 and I teach the science subjects like biology, chemistry, physics and mathematics." (name="Teacher 2")

    teacher "Teacher 3, pleased. I teach sport, physics and mathematics." (name="Teacher 3")

    teacher "And I am Teacher 4. I teach art, music and history." (name="Teacher 4")

    teacher """
        As you can see, we are way understaffed and we sometimes have to teach subjects we don't even specialize in.

        We hope you will be able to hire more teachers to ease our workload and support your school reform efforts.

        Now our role during these meetings will be to ensure that new policies and ideas continue to benefit the 
        students.

        That's all from our side. Thank you very much.
    """ (name="Teacher 1")
    
    parent """
        Hello, I am a concerned parent of one of the students attending this school and I speak for all parents when I 
        say that we are worried about the recent changes. However, we trust that you will handle your job competently 
        and we will observe closely to ensure the well-being of our children.
    """
    
    # introduction school council

    $ set_all_buildings_blocked(True)
    $ set_building_blocked("office_building", False)
    

label .end_meeting:
    headmaster """
        That should be all for today.\n
        Good work, thank you all for coming and have a nice weekend.
    """
    jump new_daytime

###########################################
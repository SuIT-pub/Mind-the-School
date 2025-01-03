init 1 python:
    set_current_mod('base')
    
    ####################
    # Courtyard
    courtyard_general_event.add_event(
        Event(1, "first_week_courtyard_event",
            IntroCondition(),
            TimeCondition(day = "2-4", month = 1, year = 2023),
            Pattern("main", "images/events/first week/first week courtyard <step>.webp"),
            thumbnail = "images/events/first week/first week courtyard 1.webp"),
        Event(1, "first_potion_courtyard_event",
            IntroCondition(),
            TimeCondition(day = 9, month = 1, year = 2023),
            Pattern("main", "images/events/first potion/first potion courtyard <step>.webp"),
            thumbnail = "images/events/first potion/first potion courtyard 1.webp")
    )

    ####################
    # Gym
    gym_general_event.add_event(
        Event(1, "first_week_gym_event",
            IntroCondition(),
            TimeCondition(day = "2-4", month = 1, year = 2023),
            Pattern("main", "images/events/first week/first week gym <step>.webp"),
            thumbnail = "images/events/first week/first week gym 1.webp"),
        Event(1, "first_potion_gym_event",
            IntroCondition(),
            TimeCondition(day = 9, month = 1, year = 2023),
            Pattern("main", "images/events/first potion/first potion gym <step>.webp"),
            thumbnail = "images/events/first potion/first potion gym 1.webp")
    )

    ####################
    # Kiosk
    kiosk_general_event.add_event(
        Event(1, "first_week_kiosk_event",
            IntroCondition(),
            TimeCondition(day = "2-4", month = 1, year = 2023),
            Pattern("main", "images/events/first week/first week kiosk <step>.webp"),
            thumbnail = "images/events/first week/first week kiosk 1.webp")
    )

    ####################
    # Office Building    
    office_building_general_event.add_event( 
        Event(1, "first_week_office_building_event",
            IntroCondition(),
            TimeCondition(day = "2-4", month = 1, year = 2023),
            Pattern("main", "images/events/first week/first week office building <step>.webp"),
            thumbnail = "images/events/first week/first week office building 1.webp"),
        Event(1, "first_potion_office_building_event",
            IntroCondition(),
            TimeCondition(day = 9, month = 1, year = 2023),
            Pattern("main", "images/events/first potion/first potion office <step>.webp"),
            thumbnail = "images/events/first potion/first potion office 1.webp")
    )

    ####################
    # School Building
    sb_general_event.add_event(
        Event(1, "first_week_sb_event",
            IntroCondition(),
            TimeCondition(day = "2-4", month = 1, year = 2023),
            Pattern("main", "images/events/first week/first week school building <step>.webp"),
            thumbnail = "images/events/first week/first week school building 2.webp"),
        Event(1, "first_potion_sb_event",
            IntroCondition(),
            TimeCondition(day = 9, month = 1, year = 2023),
            Pattern("main", "images/events/first potion/first potion school building <step>.webp"),
            thumbnail = "images/events/first potion/first potion school building 1.webp")
    )

    ####################
    # School Dormitory
    sd_general_event.add_event(
        Event(1, "first_week_school_dormitory_event",
            IntroCondition(),
            TimeCondition(day = "2-4", month = 1, year = 2023),
            Pattern("main", "images/events/first week/first week school dormitory <step>.webp"),
            thumbnail = "images/events/first week/first week school dormitory 1.webp"),
        Event(1, "first_potion_school_dormitory_event",
            IntroCondition(),
            TimeCondition(day = 9, month = 1, year = 2023),
            Pattern("main", "images/events/first potion/first potion school dormitory <step>.webp"),
            thumbnail = "images/events/first potion/first potion school dormitory 3.webp")
    )

    ####################


###########################
# region Courtyard Events #

label first_potion_courtyard_event (**kwargs):
    $ begin_event(**kwargs)
    
    $ image = convert_pattern("main", step_start = 1, **kwargs)

    $ image.show(1)
    subtitles "You walk around in the courtyard."

    $ image.show(2)
    subtitles "The first thing you notice is the group of students sunbathing in the middle of the yard."
    
    $ image.show(3)
    subtitles "Normally that wouldn't be such a weird thing, if they weren't in only their underwear."
    headmaster_thought "I certainly enjoy the view. Unfortunately it only lasts for today until the serum finishes settling in their bodies."

    $ set_building_blocked("courtyard")

    $ end_event("new_daytime", **kwargs)

label first_week_courtyard_event (**kwargs):
    $ begin_event(**kwargs)
    
    $ image = convert_pattern("main", step_start = 1, **kwargs)

    $ image.show(1)
    subtitles "You walk through the courtyard."

    headmaster_thought "Hmm, the courtyard looks really bad..."
    
    $ image.show(2)
    headmaster_thought "It seems most of the appliances here are out of order."

    $ image.show(3)
    headmaster_thought "For example the public toilet is broken."

    $ image.show(4)
    headmaster_thought "At least the courtyard doesn't need immediate fixing."

    $ change_stat("happiness", 5, get_school())

    $ set_building_blocked("courtyard")

    $ end_event("new_day", **kwargs)


#endregion
###########################

#####################
# region Gym Events #

label first_potion_gym_event (**kwargs):
    $ begin_event(**kwargs)
    
    $ image = convert_pattern("main", step_start = 1, **kwargs)

    $ image.show(1)
    subtitles "You enter the Gym and see a group of students and teacher in a yoga session."

    $ image.show(2)
    headmaster_thought "Oh that is a sport session I can get behind!"

    $ image.show(3)
    headmaster_thought "Mhh, yes very flexible!"

    $ image.show(4)
    headmaster_thought "Oh they seem to really get into it!"

    $ set_building_blocked("gym")

    $ end_event('new_daytime', **kwargs)

# first week event
label first_week_gym_event (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", step_start = 1, **kwargs)
    
    $ image.show(1)
    headmaster_thought "Okay, now the Gym. I have been here shortly for my introduction speech but I haven't had the chance to get a thorough look."

    $ image.show(2)
    headmaster_thought "Mhh, doesn't look to shabby..."
    
    $ image.show(3)
    headmaster_thought "Seems to be decently stocked."
    headmaster_thought "The material is well maintained. I guess it's alright."

    $ change_stat("charm", 5, get_school())

    $ set_building_blocked("gym")

    $ end_event('new_daytime', **kwargs)

# endregion
#####################

#######################
# region Kiosk Events #
label first_week_kiosk_event (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", step_start = 1, **kwargs)

    $ image.show(1)
    headmaster_thought "Now, somewhere here should be the kiosk..."
    $ image.show(2)
    headmaster_thought "Hmm, why is it so crowded?"

    $ image.show(3)
    headmaster "Excuse me, did something happen? Why is it so crowded here?"
    
    $ image.show(4)
    sgirl "What do you mean? It's always this full. We can't get food anywhere else than here." (name = "Lin Kato")
    
    $ image.show(3)
    headmaster "Oh I understand... Thanks."

    $ image.show(5)
    headmaster_thought "This is not acceptable. Did the former headmaster really close the kiosk?"
    headmaster_thought "That can't be right..."

    $ change_stat("reputation", 5, get_school())

    $ set_building_blocked("kiosk")

    $ end_event('new_day', **kwargs)

# endregion
#######################

#################################
# region School Building Events #

label first_week_sb_event (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", step_start = 1, **kwargs)
    
    $ image.show(1)
    subtitles """You enter the main building of the high school.
        
        Well, you don't really need to enter the building to get an idea of the state it's in."""
        
    $ image.show(2)
    headmaster_thought """Despite my fear, the building seems to be rather well maintained.

        It could be a bit cleaner but the corridor seems rather well.

        Let's see the classrooms."""
    
    $ image.show(3)
    headmaster_thought "Oh not bad as well. "

    $ image.show(4)
    headmaster_thought "Hmm I think there should be a class right now, let's check."

    $ image.show(6)
    headmaster_thought "Hmm looks like a normal class, but I think the students have no material?"
    headmaster_thought "Yeah, not one school girl has even one book."
    headmaster_thought "I guess the former headmaster cut back on those"

    $ change_stat("education", 5, get_school())

    $ set_building_blocked("school_building")

    $ end_event('new_day', **kwargs)

label first_potion_sb_event (**kwargs):
    $ begin_event(**kwargs)
    
    $ image = convert_pattern("main", step_start = 1, **kwargs)

    $ image.show(1)
    headmaster_thought "Let's see how classes are today."
    
    $ image.show(2)
    subtitles "You look into a classroom and the first thing you notice is that almost everyone has opened up or at least partially removed their clothes."
    subtitles "Apparently the teachers also took a drink."
    headmaster_thought "Hmm, I can't wait to have this view on a regular basis, but that's gonna take some time."

    $ set_building_blocked("school_building")
    
    $ end_event('new_daytime', **kwargs)

# endregion
#################################

##################################
# region School Dormitory Events #

label first_week_school_dormitory_event (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", step_start = 1, **kwargs)
    
    $ image.show(1)
    headmaster_thought "The dormitory looks alright."

    $ image.show(2)
    headmaster_thought "As far as I know, the students have to share a communal bathroom."
    headmaster_thought "Private bathrooms would be nice for the students, but for one I don't think we really need that and then it would need a lot of rebuilding. So that should be last on the list."
    
    $ image.show(3)
    headmaster_thought "Let's see if someone would let me see their room so I can check the state of these."
    
    $ image.show(4)
    headmaster "Hello? I'm Mr. [headmaster_last_name] the new Headmaster. Can I come in? I'm here to inspect the building."
    subtitles "..."
    headmaster "Hello?"

    $ image.show(5)
    headmaster_thought "Hmm nobody seems to be here. Nevermind. I just let my Secretary give me a report."

    $ change_stat("inhibition", -3, get_school())
    $ change_stat("happiness", 3, get_school())

    $ set_building_blocked("school_dormitory")

    $ end_event('new_day', **kwargs)

label first_potion_school_dormitory_event (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", step_start = 1, **kwargs)
    
    $ image.show(1)
    subtitles "You enter the dormitory of the high school."
    headmaster_thought "Mhh, where does the noise come from?"

    $ image.show(2)
    headmaster_thought "Ah I think there are some students in the room over there."

    $ image.show(3)
    headmaster_thought "Ahh party games!"

    $ image.show(4)
    if time.check_daytime("c"):
        headmaster_thought "Normally I would scold them for skipping class but today is a special day so I gladly enjoy this view."
    else:
        headmaster_thought "Ahh I like this view. Nothing more erotic than nudity in combination with a party game."

    $ set_building_blocked("school_dormitory")

    $ end_event('new_daytime', **kwargs)

# endregion
##################################

############################
# region Game Intro Events #

label intro ():
    subtitles "All characters and events in this game, even those based on real people, are entirely fictional."

    $ school_name = renpy.input("Please name your School: (Default: \"Windstor School\")")
    $ school_name = school_name.strip() or "Windstor Academy"

    $ set_game_data("school_name", school_name)

    $ headmaster_first_name = renpy.input("First name of your Character: (Default \"Mark\")")
    $ headmaster_first_name = headmaster_first_name.strip() or "Mark"

    $ headmaster_last_name = renpy.input("Last name of your Character: (Default \"Benson\")")
    $ headmaster_last_name = headmaster_last_name.strip() or "Benson"

    $ set_name("headmaster", headmaster_first_name, headmaster_last_name)

    $ school_config = "a High School."
    # if loli_content == 1:
    #     $ school_config = "a High and Middle School."
    # if loli_content == 2:
    #     $ school_config = "a High, Middle and Elementary School."

    $ school_config_noun = "school"

    show screen black_error_screen_text ("")

    menu:
        "Play intro?"

        "Yes. Play intro!":
            jump .start
        "Skip intro.":
            jump .jump_to_tutorial
        "Skip to free-roam. (Skips first week bonus stats.)":
            call skip_to_free_roam from intro_3

label .jump_to_tutorial:
    $ time.set_time(day = 1, month = 1, year = 2023, daytime = 1)

    jump new_day

label .start:
    hide screen black_error_screen_text

    nv_text "Welcome to [school_name]!"
    nv_text "[school_name] is a school located deep in the woods, miles away from the nearest city."
    nv_text "This academy consists of [school_config]"
    nv_text "Here it is where you, the new headmaster, will take on the task of managing the school and restoring them back to their former glory."

    nvl clear

    nv_text "To be fair, after the fuckup of the last headmaster, this school lost a lot of its prestige."
    nv_text "And after the last headmaster mysteriously disappeared, you were invited to take over."

    nvl clear

    nv_text "A little more about you:"
    nv_text "You're just an ordinary educator, nothing special."
    nv_text "Just one thing: You're known for your {w}{cps=10}special methods.{/cps}"
    nv_text "Even if the people involved are aware of your tendencies, you are strongly discouraged from turning the school into a sex haven."
    nv_text "But what they don't know. {w}At least you hope so.{w} You {b}will{/b} turn this school into a sex paradise."
    
    nvl clear

    nv_text "And this time you will succeed."
    nv_text "People always blocked you off. Never let you try your theory of intimate conditioning."
    nv_text "But now you got the chance. The sponsors were very impressed by yours talks and theories so they helped you get ahold of this school."
    nv_text "You will not let them down."

    nvl clear

    nv_text "You enter the office..."
    
    call screen black_screen_text ("Monday, 1 January 2023") with dissolveM

    $ headmaster_last_name = get_name_last("headmaster")
    $ secretary_name = get_name_str("secretary")

    $ image = Image_Series("images/events/intro/intro <step>.webp")

    $ image.show(3)
    secretary """Hello Mr. [headmaster_last_name], nice to meet you!
        My name is [secretary_name].
    """ (name="Secretary")
    secretary "From now on I'll be your secretary."

    $ image.show(0)
    secretary """I used to work for the previous headmaster, 
        so I know the school pretty well.
    """

    $ image.show(4)
    secretary "If you have any questions just come and ask me."

    $ image.show(5)
    secretary """
        Unfortunately, the last headmaster left this school in pretty bad shape.

        We had to close almost all of our facilities to save some money.

        This wasn't only bad for the students' education, but also for the school's reputation.
    """

    $ image.show(4)
    secretary "So now it is your job to go on and fix this school!"

    $ image.show(6)
    secretary """
        You won't be handling all the details like hiring teachers or setting up schedules.

        You will administer the rules, patrol the campus, manage the infrastructure, interact with the students, and 
        occasionally teach a class or two.
    """

    $ image.show(1)
    secretary """But new rules must be approved by the PTA which is made up of the school council, teachers and a 
        representative from the regional government.
    """

    call tutorial_menu from first_day_introduction_3

    $ image.show(2)
    secretary "Now you know the basics. You might want to hurry down to the gym for the weekly meeting."

    $ image.show(4)
    secretary "I'm sure the students are eager to meet you."

    
    call show_image ("images/events/intro/intro gym 2 0.webp") from _call_show_image_tutorial_1
    subtitles "You leave the office with the secretary and head for the Gym."
    
    #show inside gym with students walking towards their position in gym or talking to each other in groups by school
    subtitles "As you enter the hall, you are greeted by students standing all around the hall."
    
    #show move up stairs with secretary in front and clear view of butt
    call show_image ("images/events/intro/intro gym 3 1.webp") from _call_show_image_tutorial_2
    subtitles "As you and your secretary make your way to the stage, all the students begin to form neat rows."
    secretary_whisper "The students in the left are from the high school."
    # if loli_content >= 1:
    #     secretary_whisper "The students in the center are from the middle school."
    # if loli_content == 2:
    #     secretary_whisper "And to the right are the elementary school students."

    call show_image ("images/events/intro/intro gym 3 2.webp") from _call_show_image_tutorial_3
    headmaster_thought "Wow she has a nice butt. I can't wait to make it mine."
    
    #show secretary stand at podium with hands on podium
    call show_image ("images/events/intro/intro gym 4.webp") from _call_show_image_tutorial_4
    secretary_shout "Good Morning Students!"
    crowd_shout "Good Morning!"

    #show crowd from behind Secretary (students standing in clear rows)
    call show_image ("images/events/intro/intro gym 5 0.webp") from _call_show_image_tutorial_5
    secretary_shout "It is with great pleasure, that I introduce you to your new Headmaster."
    secretary_shout "He will be starting today and we're all very excited to see the positive changes he will bring!"

    #show view from slightly behind crowd towards stage (secretary pointing towards headmaster)
    secretary_shout "But without further ado... Greet your new Headmaster Mr. [headmaster_last_name]!"
    subtitles "You walk to the podium."

    #show view of stage from front with headmaster standing at podium with hands on podium
    call show_image ("images/events/intro/intro gym 7.webp") from _call_show_image_tutorial_6
    headmaster_shout "Greetings to you all. I am honored to stand here today."
    headmaster_shout "When I came here, I saw the condition of this school and the mishaps of your former headmaster."
    headmaster_shout "I guarantee I won't repeat the same mistakes and I will bring this school back to its former glory and beyond."

    #show view of crowd from slightly behind but other side, headmaster hand on chest
    call show_image ("images/events/intro/intro gym 8 0.webp") from _call_show_image_tutorial_7
    headmaster_shout "Now a little about me. My name is [headmaster_first_name] [headmaster_last_name] and I come from the country."
    headmaster_shout "I taught in various schools and was also the headmaster of a school in the capitol."

    #show headmaster rasing finger
    headmaster_shout "I want to make it clear that I will not tolerate misbehavior! {b}BUT{/b} I am a fair person."
    headmaster_shout "No one will be punished if they don't deserve it, and I will do everything I can to make sure that you all have a nice and safe place to grow and learn!"

    #show headmaster with wide open arms
    headmaster_shout "If you ever have any problems, ideas or questions, feel free to come to me anytime. I will help wherever I can!"
    headmaster_shout "Thank you and let's have a great time together!"
    crowd_shout "*clapping*"

    $ image.show(4)
    secretary "Wow! That was a nice speech!"
    secretary "Now that we finished the introduction, let's start with the entry paperwork."
    headmaster "Alright."

    $ time.set_time(day = 1, month = 1, year = 2023, daytime = 1)

    jump new_day

##########################

label skip_to_free_roam ():
    
    $ set_level_for_char(1, "school", charList)
    $ set_level_for_char(1, "teacher", charList["staff"])
    $ set_level_for_char(1, "parent", charList)
    $ set_level_for_char(5, "secretary", charList["staff"])

    $ time.set_time(day = 10, month = 1, year = 2023)

    call first_week_epilogue_final.skip from skip_to_free_roam_1

# endregion
############################
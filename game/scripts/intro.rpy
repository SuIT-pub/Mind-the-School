label ask_age ():
    menu:
        "This Game contains sexual content and is not suitable for consumption by underage people.\nPlease confirm you are not underage in your country."

        "Yes I am above 18.":
            jump intro
        "No unfortunately I am underage.":
            return

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
    if loli_content == 1:
        $ school_config = "a High and Middle School."
    if loli_content == 2:
        $ school_config = "a High, Middle and Elementary School."

    $ school_config_noun = "school"

    show screen black_error_screen_text ("")

    menu:
        "Play intro?"

        "Yes. Play intro!":
            jump .start
        "Skip to tutorial.":
            call tutorial_1.tutorial_2 from intro_1
        "Skip after intro.":
            call tutorial_1.tutorial_3 from intro_2
        "Skip to free-roam. (Skips first week bonus stats.)":
            call skip_to_free_roam from intro_3

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

    $ headmaster_last_name = get_last_name("headmaster")
    $ secretary_name = get_name("secretary")

    show office secretary 1 smile with dissolveM
    secretary """Hello Mr. [headmaster_last_name], nice to meet you!
        My name is [secretary_name].
    """ (name="Secretary")
    secretary "From now on I'll be your secretary."

    show office secretary 1 talk with dissolveM
    secretary """I used to work for the previous headmaster, 
        so I know the school pretty well.
    """

    show office secretary 3 big smile  with dissolveM
    secretary "If you have any questions just come and ask me."

    show office secretary 2 emotionless with dissolveM
    secretary """
        Unfortunately, the last headmaster left this school in pretty bad shape.

        We had to close almost all of our facilities to save some money.

        This wasn't only bad for the students' education, but also for the school's reputation.
    """

    show office secretary 3 big smile with dissolveM
    secretary "So now it is your job to go on and fix this school!"

    show office secretary 4 smile with dissolveM
    secretary """
        You won't be handling all the details like hiring teachers or setting up schedules.

        You will administer the rules, patrol the campus, manage the infrastructure, interact with the students, and 
        occasionally teach a class or two.
    """

    show office secretary 1 emotionless with dissolveM
    secretary """But new rules must be approved by the PTA which is made up of the school council, teachers and a 
        representative from the regional government.
    """

    call tutorial_menu from first_day_introduction_3

    show office secretary 3 smile with dissolveM
    secretary "Now you know the basics. You might want to hurry down to the gym for the weekly meeting."

    show office secretary 3 big smile with dissolveM
    secretary "I'm sure the students are eager to meet you."

    scene expression "events/intro/intro gym 2 [loli_content].webp" with dissolveM 
    subtitles "You leave the office with the secretary and head for the Gym."
    
    #show inside gym with students walking towards their position in gym or talking to each other in groups by school
    subtitles "As you enter the hall, you are greeted by students standing all around the hall."
    
    #show move up stairs with secretary in front and clear view of butt
    show intro gym 3 1 with dissolveM
    subtitles "As you and your secretary make your way to the stage, all the students begin to form neat rows."
    secretary_whisper "The students in the left are from the high school."
    if loli_content >= 1:
        secretary_whisper "The students in the center are from the middle school."
    if loli_content == 2:
        secretary_whisper "And to the right are the elementary school students."

    scene intro gym 3 2 with dissolveM
    headmaster_thought "Wow she has a nice butt. I can't wait to make it mine."
    
    #show secretary stand at podium with hands on podium
    scene intro gym 4 with dissolveM
    secretary_shout "Good Morning Students!"
    crowd_shout "Good Morning!"

    #show crowd from behind Secretary (students standing in clear rows)
    show expression "events/intro/intro gym 5 [loli_content].webp" with dissolveM
    secretary_shout "It is with great pleasure, that I introduce you to your new Headmaster."
    secretary_shout "He will be starting today and we're all very excited to see the positive changes he will bring!"

    #show view from slightly behind crowd towards stage (secretary pointing towards headmaster)
    # show expression "events/intro/intro gym 6 [loli_content].webp"
    secretary_shout "But without further ado... Greet your new Headmaster Mr. [headmaster_last_name]!"
    subtitles "You walk to the podium."

    #show view of stage from front with headmaster standing at podium with hands on podium
    show intro gym 7
    hide expression "events/intro/intro gym 5 [loli_content].webp" with dissolveM
    headmaster_shout "Greetings to you all. I am honored to stand here today."
    headmaster_shout "When I came here, I saw the condition of this school and the mishaps of your former headmaster."
    headmaster_shout "I guarantee I won't repeat the same mistakes and I will bring this school back to its former glory and beyond."

    #show view of crowd from slightly behind but other side, headmaster hand on chest
    show expression "events/intro/intro gym 8 [loli_content].webp" with dissolveM
    headmaster_shout "Now a little about me. My name is [headmaster_first_name] [headmaster_last_name] and I come from the country."
    headmaster_shout "I taught in various schools and was also the headmaster of a school in the capitol."

    #show headmaster rasing finger
    # scene expression "events/intro/intro gym 9 [loli_content].webp"
    headmaster_shout "I want to make it clear that I will not tolerate misbehavior! {b}BUT{/b} I am a fair person."
    headmaster_shout "No one will be punished if they don't deserve it, and I will do everything I can to make sure that you all have a nice and safe place to grow and learn!"

    #show headmaster with wide open arms
    # scene expression "events/intro/intro gym 10 [loli_content].webp"
    headmaster_shout "If you ever have any problems, ideas or questions, feel free to come to me anytime. I will help wherever I can!"
    headmaster_shout "Thank you and let's have a great time together!"
    crowd_shout "*clapping*"

    scene office secretary 3 big smile
    secretary "Wow! That was a nice speech!"
    secretary "Now that we finished the introduction, let's start with the entry paperwork."
    headmaster "Alright."

    jump new_day

##########################


label skip_to_free_roam ():
    
    $ set_level_for_char(1, "school", charList)
    $ set_level_for_char(1, "teacher", charList["staff"])
    $ set_level_for_char(1, "parents", charList)
    $ set_level_for_char(5, "secretary", charList["staff"])

    $ time.set_time(day = 10, month = 1, year = 2023)

    call first_week_epilogue_final.skip from skip_to_free_roam_1
label ask_age:
    menu:
        "This Game contains sexual content and is not suitable for consumption by underage people.\nPlease confirm you are not underage in your country."

        "Yes I am above 18.":
            jump intro
        "No unfortunately I am underage.":
            return

label intro:
    subtitles "All characters and events in this game, even those based on real people, are entirely fictional."

    $ school_name = renpy.input("Please name your School: (Default: \"Windstor School\")")
    $ school_name = school_name.strip() or "Windstor Academy"

    $ set_game_data("school_name", school_name)

    $ principal_first_name = renpy.input("First name of your Character: (Default \"Mark\")")
    $ principal_first_name = principal_first_name.strip() or "Mark"

    $ set_game_data("principal_first_name", principal_first_name)

    $ principal_last_name = renpy.input("Last name of your Character: (Default \"Benson\")")
    $ principal_last_name = principal_last_name.strip() or "Benson"

    $ set_game_data("principal_last_name", principal_last_name)

    $ school_config = "a High School."
    if loli_content == 1:
        $ school_config = "a High and Middle School."
    if loli_content == 2:
        $ school_config = "a High, Middle and Elementary School."

    $ school_config_noun = "school"
    if loli_content > 0:
        $ school_config_noun = "schools"

    show screen black_error_screen_text ("")

    menu:
        subtitles "Play intro?"

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
    nv_text "[school_name] is a school located deep in the woods, aeons away from the nearest city."
    nv_text "This academy consists of [school_config]"
    nv_text "Here it is where you, the new headmaster, will take on the task of managing the [school_config_noun] and restoring them back to their former glory."

    nvl clear

    nv_text "To be fair, after the fuckup of the last principal, this school lost a lot of its prestige."
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
    nv_text "But now you got the chance. The sponsors where very impressed by yours talks and theories so they helped you get ahold of this school."
    nv_text "You will not let them down."

    nvl clear

    nv_text "You enter the office..."

    jump new_daytime

label skip_to_free_roam:
    
    dev "[intro_dev_message]"

    $ set_level_for_char(1, "high_school", charList["schools"])
    $ set_level_for_char(1, "middle_school", charList["schools"])
    $ set_level_for_char(1, "elementary_school", charList["schools"])
    $ set_level_for_char(1, "teacher", charList["staff"])
    $ set_level_for_char(5, "secretary", charList["staff"])

    $ time.set_time(day = 10, month = 1, year = 2023)

    call first_week_epilogue_final from skip_to_free_roam_1
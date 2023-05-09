label ask_age:
    menu:
        "This Game contains sexual content and is not suitable for consumption by underage people.\nPlease confirm you are not underage in your country."

        "Yes I am above 18.":
            jump intro
        "No unfortunately I am underage.":
            return

label intro:
    $ school_name = renpy.input("Please name your School: (Default: \"Windstor School\")")
    $ school_name = school_name.strip() or "Windstor Academy"

    $ principal_name = renpy.input("Please name your Character: (Default \"Mark\")")
    $ principal_name = principal_name.strip() or "Mark"

    $ nvl_text = Character(None, kind=nvl)

    $ school_config = "a High School."
    if loli_content == 1:
        $ school_config = "a High and Middle School."
    if loli_content == 2:
        $ school_config = "a High, Middle and Elementary School."

    $ school_config_noun = "school"
    if loli_content > 0:
        $ school_config_noun = "schools"

    nvl_text "Welcome to [school_name]!"
    nvl_text "[school_name] is a school located deep in the woods, aeons away from the nearest city."
    nvl_text "This academy consists of [school_config]"
    nvl_text "Here it is where you, the new headmaster, will take on the task of managing the [school_config_noun] and restoring them back to their former glory."

    nvl clear

    nvl_text "To be fair, after the fuckup of the last principal, this school lost a lot of its prestige."
    nvl_text "And after the last headmaster mysteriously disappeared, you were invited to take over."

    nvl clear

    nvl_text "A little more about you:"
    nvl_text "You're just an ordinary educator, nothing special."
    nvl_text "Just one thing: You're known for your {w}{cps=10}special methods.{/cps}"
    nvl_text "Even if the people involved are aware of your tendencies, you are strongly discouraged from turning the school into a sex haven."
    nvl_text "But what they don't know. {w}At least you hope so.{w} You {b}will{/b} turn this school into a sex paradise."
    
    nvl clear

    nvl_text "And this time you will succeed."
    nvl_text "This time you won't rush things and keep what's happening here out of the public eye, until it's ready for it."
    nvl_text "Luckily, unlike your previous school, this one is a boarding school. And a very strict one at that."
    nvl_text "No going out, no going home during the holidays. Parents are only allowed to visit with prior notice."
    nvl_text "It's almost like a prison, only nicer. It's perfect!"

    jump new_daytime
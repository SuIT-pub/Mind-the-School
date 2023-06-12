##################################################
# ----- Office Building Event Handler ----- #
##################################################

init -10 python:
    office_building_events = {}

    office_building_events["fallback"] = "office_building_fallback"

    # event check before menu
    office_building_events["office_building"] = {
        "fallback": "office_building.after_time_check", # no event
    }

    office_building_events["tutorial"] = {
        "fallback": "tutorial_menu",
    }

    office_building_events["journal"] = {
        "fallback": "check_journal",
    }

################################################
# ----- Office Building Entry Point ----- #
################################################

label office_building:
    scene office secretary 4 big smile

    call event_check_area("office_building", office_building_events)

label.after_time_check:

    menu:
        char_Secretary "Hello Headmaster! How can I help you?"

        "About the School...":
            call event_check_area("tutorial", office_building_events) 
        "Check Journal":
            call event_check_area("journal", office_building_events)
        "Do Paperwork":
            call event_check_area("paperwork", office_building_events)
        "Check Messages":
            call event_check_area("messages", office_building_events)
        "Surf Internet":
            call event_check_area("internet", office_building_events)
        "Counsel work":
            call event_check_area("counsel", office_building_events)
        "Check rules":
            call event_check_area("rules", office_building_events)
        "Leave":
            jump map_overview

    jump office_building

####################################################
# ----- High School Building Fallback Events ----- #
####################################################

label office_building_fallback:
    Subtitles "There is nobody here."
    return

###########################################
# ----- High School Building Events ----- #
###########################################

label first_day_introduction:

    scene office secretary 1 smile
    char_Secretary "Hello, nice to meet you! From now on I'll be your secretary."

    scene office secretary 1 talk
    char_Secretary "I used to work for the previous principal, so I know the school pretty well."

    scene office secretary 3 big smile 
    char_Secretary "If you have any questions just come and ask me."

    scene office secretary 2 emotionless
    char_Secretary "Unfortunately, the last principal left this school in pretty bad shape."
    char_Secretary "We had to close almost all of our facilities to save some money."
    char_Secretary "This wasn't only bad for the students' education, but also for the school's reputation."

    scene office secretary 3 big smile
    char_Secretary "So now it is your job to go on and fix this school!"

    scene office secretary 4 smile
    char_Secretary "You won't be handling all the details like hiring teachers or setting up schedules."
    char_Secretary "You will administer the rules, patrol the campus, manage the infrastructure, interact with the students, and occasionally teach a class or two."

    scene office secretary 1 emotionless
    char_Secretary "But new rules must be approved by the PTA which is made up of the school council, teachers and a representative from the regional government."

    call tutorial_menu

    scene office secretary 3 smile
    char_Secretary "Now you know the basics. You might want to hurry down to the gym for the weekly meeting."

    scene office secretary 3 big smile
    char_Secretary "I'm sure the students are eager to meet you."

    return

image movie_potion_intro_16 = Movie(loop = False, play = "potion_intro_16.mp4")
image movie_potion_intro_17 = Movie(loop = True, play = "images/office/potion_intro_17.mp4")
image movie_potion_intro_18 = Movie(loop = True, play = "images/office/potion_intro_18.mp4")
image movie_potion_intro_18 = Movie(loop = True, play = "images/office/potion_intro_19.mp4", image = "office/potion_intro_20.png")

# screen video(movie_name):
#     add image movie_name

label potion_introduction_1:

    scene expression "office/potion_intro_01.png"
    char_Secretary "Good Morning, Headmaster!"
    char_Secretary "Someone dropped a package off for you. But there is no sender."

    scene expression "office/potion_intro_02.png"
    char_Principal "Mhh... Thats weird, I didn't order anything. Well lets look inside what it is."
    char_Secretary "Are you sure? What if it is something dangerous?"
    char_Principal "I wouldn't know why. I'm sure it will be fine."

    scene expression "office/potion_intro_03.png"
    char_Principal "See it's just some bottles. Here let's drink one together!"
    char_Secretary "I don't think that's safe."
    char_Principal "Ah come on! I'm sure it'll be fine."

    scene expression "office/potion_intro_04.png"
    char_Principal_thought "Good she didn't see the letter in the box."
    char_Principal_thought "In reality, this box comes from my secret supporter. And the bottles are filled with a new special potion."
    char_Principal_thought "Unfortunately he could only send me 4 potions so I have to find a way reproduce them."
    char_Principal_thought "But first gonna test them out!"

    scene expression "office/potion_intro_05.png"
    char_Principal "Come on lets drink it!"
    char_Secretary "Okay let's do it."

    scene expression "office/potion_intro_06.png"
    char_Secretary "Wow it tastes really nice. But are you getting hot as well?"

    scene expression "office/potion_intro_07.png"
    char_Secretary "I'm burning up! Gotta take some clothing off."

    scene expression "office/potion_intro_08.png"
    $ renpy.pause ()

    scene expression "office/potion_intro_09.png"
    $ renpy.pause ()

    scene expression "office/potion_intro_10.png"
    $ renpy.pause ()

    scene expression "office/potion_intro_11.png"
    $ renpy.pause ()

    scene expression "office/potion_intro_12.png"
    char_Secretary "Ahh way better."

    scene expression "office/potion_intro_13.png"
    char_Secretary "Headmaster why don't you come over here, so we can better talk to each other."

    scene expression "office/potion_intro_14.png"
    char_Secretary "Oh someone seems to be excited. Does my body turn you on that much?"

    scene expression "office/potion_intro_15.png"
    char_Secretary "Don't worry I will take responsibility."

    $ renpy.movie_cutscene("office/potion_intro_16.webm")
    $ renpy.pause(0.0)

    # $ renpy.movie_cutscene("office/potion_intro_17.webm", None, -1)
    # $ renpy.pause()

    $ renpy.movie_cutscene("office/potion_intro_18.webm", -1, -1)
    $ renpy.pause(0.0)

    $ renpy.movie_cutscene("office/potion_intro_19.webm", -1)

    scene expression "office/potion_intro_20.png"
    $ renpy.pause()

    scene expression "office/potion_intro_21.png"
    char_Secretary "Ahh I can't take it anymore, please give it to me!"

    $ renpy.movie_cutscene("office/potion_intro_22.webm")
    $ renpy.movie_cutscene("office/potion_intro_23.webm", -1, -1)
    $ renpy.movie_cutscene("office/potion_intro_24.webm", -1, -1)
    $ renpy.movie_cutscene("office/potion_intro_25.webm", -1, -1)
    $ renpy.movie_cutscene("office/potion_intro_26.webm", -1, -1)
    $ renpy.movie_cutscene("office/potion_intro_27.webm")

    scene expression "office/potion_intro_28.png"
    $ renpy.pause ()

    scene expression "office/potion_intro_29.png"
    $ renpy.pause ()

    $ renpy.movie_cutscene("office/potion_intro_30.webm", -1, -1)
    $ renpy.movie_cutscene("office/potion_intro_31.webm", -1, -1)
    $ renpy.movie_cutscene("office/potion_intro_32.webm", -1, -1)
    $ renpy.movie_cutscene("office/potion_intro_33.webm")

    scene expression "office/potion_intro_34.png"
    $ renpy.pause ()
    
    scene expression "office/potion_intro_35.png"
    char_Principal "Oh I seem to have overdone it. Propably should give her some rest and look for her tomorrow."
    char_Principal_thought "But the potion seems to be working full. But I need to check if she is like this tomorrow as well."

    jump new_day
    
label potion_introduction_2:
    # next day screen
    scene expression "office/potion_intro_36.png"
    char_Secretary "Good Morning Headmaster!"
    char_Principal "Oh good morning! How are you feeling?"
    char_Principal_thought "Wow! Now that's some nice outfit!"

    scene expression "office/potion_intro_37.png"
    char_Secretary "Oh I feel amazing! I never felt so good before drinking the potion!"
    char_Principal "So you remember everything that happened yesterday?"

    scene expression "office/potion_intro_38.png"
    char_Secretary "Oh for sure I remember everything!"

    scene expression "office/potion_intro_39.png"
    char_Secretary "Although I'm really emberassed with us having had sex."

    scene expression "office/potion_intro_40.png"
    char_Secretary "But I'm feeling so free now!"

    scene expression "office/potion_intro_listen.png"
    char_Principal "That's amazing news! Now my plan is to share this feeling among the students."

    scene expression "office/potion_intro_41.png"
    char_Secretary "No, I don't think you will do that."
    char_Principal "What? Why?"

    scene expression "office/potion_intro_42.png"
    char_Secretary "Because you don't have enough potions!"

    scene expression "office/potion_intro_listen.png"
    char_Principal "Oh! Mhh... You're right!"
    char_Principal "Well for one, there are other ways to corrupt... Öhm I mean influence the students."

    scene expression "office/potion_intro_42.png"
    char_Secretary "Oh don't worry dear! I'm fully on your side. I feel great and I want the students to also feel like this."

    scene expression "office/potion_intro_listen.png"
    char_Secretary "So what other ways do you mean?"
    char_Principal "Well there are for example more classical ways like influencing them with lewd materials or more obscure ways like hypnosis."

    scene expression "office/potion_intro_43.png"
    char_Secretary "Hypnosis?"

    scene expression "office/potion_intro_listen.png"
    char_Principal "Yeah, I know it's quite absurd. I only heard of ways to do it but I don't know how to do it."
    char_Principal "Well let's just forget that. Well for one we still have 3 potions."
    char_Principal "There was a letter with the potions and it says we can water it down to create more potions with a smaller effect."
    char_Principal "I think if we water 2 potions down enough to serve every student in the school a small drink, then we could create a good base to really influence every student."
    char_Secretary "Do you think that works? Would there still be enough of an effect?"
    char_Principal "Well I observed the school over the last week and as far as I could see, the students are not only prudish, they are the abstinence in person."
    char_Principal "So I think the classical methods would not work until they are at least a little bit open to the idea sex."
    char_Principal "And without the potion or any other good working method we have no other way."
    char_Principal "So with the watered down potion we could open their minds and then start the real operation."
    char_Principal "And while we change the students, we could reopen the lab and work on reproducing the potion using the last remaining as a draft."

    scene expression "office/potion_intro_44.png"
    char_Secretary "Mhh... That sounds like it could work..."

    scene expression "office/potion_intro_45.png"
    char_Secretary "Okay let's do that!"
    char_Secretary "I think the best would be to distribute the diluted potion during recess."
    char_Principal "Yeah that sounds good, can I entrust that to you?"

    scene expression "office/potion_intro_44.png"
    char_Secretary "Of course! But there are still some problems."
    char_Principal "What do you mean?"
    char_Secretary "The regional representative visits the school every month to make sure the school follows national laws."

    scene expression "office/potion_intro_46.png"
    char_Secretary "We have to thank the old headmaster for that. So we have to be careful. He manages our monthly budget and es long as the school follows the rules we don't get budget cuts."
    char_Secretary "So we have to play the long game until we find a way to corrupt the department. The representatives change every month so corrupting one wouldn't help."

    scene expression "office/potion_intro_listen.png"
    char_Principal "Mhh you're right. I guess we have to be careful. But we can later think of a way to deal with them."
    char_Principal "I have to travel to the city. I have some thing to prepare. I'll be back tomorrow. You meanwhile distribute the potions. Can you make it happen by today's recess?"

    scene expression "office/potion_intro_47.png"
    char_Secretary "Sure, just let me handle it!"

    scene expression "office/potion_intro_48.png"
    char_Principal "Nice! I will be on my way then!"

    $ schools["high_school"].set_level(1)
    $ schools["middle_school"].set_level(1)
    $ schools["elementary_school"].set_level(1)

    jump new_day

label check_journal:
    $ nvl_text = Character(None, kind=nvl)
    $ hCorr = schools["high_school"].get_level()
    $ mCorr = schools["middle_school"].get_level()
    $ eCorr = schools["elementary_school"].get_level()
    menu:
        Subtitles "What do you want to check?"

        "High School":
            nvl_text "High School"
            nvl_text "Corruption Level: [hCorr]"
            jump check_journal
        "Middle School" if loli_content >= 1:
            Subtitles "school"
            jump check_journal
        "Elementary School" if loli_content == 2:
            Subtitles "school"
            jump check_journal
        "Close Journal":
            jump office_building

label pta_meeting:
    Subtitles "You enter the conference room."
    Subtitles "All representatives already gathered and wait for you."
    char_Principal "Thank you all for gathering today."

    if today() == "5.1.2023":
        jump pta_meeting.first_pta_meeting
    
    char_Principal "First point for today. Does someone have anything to discuss today?"

    char_Principal "No? Alright then lets jump straight to the netx point."

label .pta_menu:
    menu:
        "Rules":
            jump pta_meeting.menu_rules
        "Buildings":
            jump pta_meeting.menu_buildings
        "Events":
            jump pta_meeting.menu_events
        "End meeting.":
            jump pta_meeting.end_meeting

    return

label .menu_rules:

    $ page = 0

label .menu_rules_check:

    # menu_block_set = list(rule_names.values())

    # menu:
    #     set menu_block_set

    #     Subtitles "What rules do you want to establish?"

label .menu_rules_return:

label .menu_buildings:

label .menu_events:
    
label .first_pta_meeting:

label .end_meeting:
    char_Principal "Thank you all for coming today."
    char_Principal "Good work and have a nice weekend!"
    jump new_daytime

label male_student_scolding:
    Subtitles "todo: male scolding"

    return

label mobbing_scolding:
    Subtitles "todo: mobbing scolding"

    return
##################################################
# ----- Office Building Event Handler ----- #
##################################################

init -10 python:
    office_building_events = {}
    office_building_events_title= {
        "tutorial": "About the school...",
        "paperwork": "Do paperwork",
        "messages": "Check messages",
        "internet": "Surf internet",
        "council": "Council work",
    }

    office_building_events["fallback"] = "office_building_fallback"

    # event check before menu
    create_event_area(office_building_events, "office_building", "office_building.after_time_check")

    create_event_area(office_building_events, "tutorial", "tutorial_menu")

    create_event_area(office_building_events, "journal", "check_journal")

################################################
# ----- Office Building Entry Point ----- #
################################################

label office_building:
    scene office secretary 4 big smile

    call event_check_area("office_building", office_building_events)

label .after_time_check:

    call call_event_menu (
        "Hello Headmaster! How can I help you?",
        1, 
        7, 
        office_building_events, 
        office_building_events_title,
        "fallback", "office_building",
        character.secretary
    )

    jump office_building

####################################################
# ----- High School Building Fallback Events ----- #
####################################################

label office_building_fallback:
    subtitles "There is nobody here."
    return

###########################################
# ----- High School Building Events ----- #
###########################################

label first_day_introduction:

    scene office secretary 1 smile
    secretary """Hello, nice to meet you! 
        From now on I'll be your secretary.
    """

    scene office secretary 1 talk
    secretary """I used to work for the previous principal, 
        so I know the school pretty well.
    """

    scene office secretary 3 big smile 
    secretary "If you have any questions just come and ask me."

    scene office secretary 2 emotionless
    secretary """
        Unfortunately, the last principal left this school in pretty bad shape.

        We had to close almost all of our facilities to save some money.

        This wasn't only bad for the students' education, but also for the school's reputation.
    """

    scene office secretary 3 big smile
    secretary "So now it is your job to go on and fix this school!"

    scene office secretary 4 smile
    secretary """
        You won't be handling all the details like hiring teachers or setting up schedules.

        You will administer the rules, patrol the campus, manage the infrastructure, interact with the students, and 
        occasionally teach a class or two.
    """

    scene office secretary 1 emotionless
    secretary """But new rules must be approved by the PTA which is made up of the school council, teachers and a 
        representative from the regional government.
    """

    call tutorial_menu

    scene office secretary 3 smile
    secretary "Now you know the basics. You might want to hurry down to the gym for the weekly meeting."

    scene office secretary 3 big smile
    secretary "I'm sure the students are eager to meet you."

    return

image movie_potion_intro_16 = Movie(loop = False, play = "potion_intro_16.mp4")
image movie_potion_intro_17 = Movie(loop = True, play = "images/office/potion_intro_17.mp4")
image movie_potion_intro_18 = Movie(loop = True, play = "images/office/potion_intro_18.mp4")
image movie_potion_intro_18 = Movie(
    loop = True, 
    play = "images/office/potion_intro_19.mp4", 
    image = "office/potion_intro_20.png"
)

# screen video(movie_name):
#     add image movie_name

label potion_introduction_1:

    scene expression "office/potion_intro_01.png"
    secretary "Good Morning, Headmaster!"
    secretary "Someone dropped a package off for you. But there is no sender."

    scene expression "office/potion_intro_02.png"
    principal "Mhh... Thats weird, I didn't order anything. Well lets look inside what it is."
    secretary "Are you sure? What if it is something dangerous?"
    principal "I wouldn't know why. I'm sure it will be fine."

    scene expression "office/potion_intro_03.png"
    principal "See it's just some bottles. Here let's drink one together!"
    secretary "I don't think that's safe."
    principal "Ah come on! I'm sure it'll be fine."

    scene expression "office/potion_intro_04.png"
    principal_thought """
        Good she didn't see the letter in the box.

        In reality, this box comes from my secret supporter. And the bottles are filled with a new special potion.

        Unfortunately he could only send me 4 potions so I have to find a way reproduce them.

        But first gonna test them out!
    """

    scene expression "office/potion_intro_05.png"
    principal "Come on lets drink it!"
    secretary "Okay let's do it."

    scene expression "office/potion_intro_06.png"
    secretary "Wow it tastes really nice. But are you getting hot as well?"

    scene expression "office/potion_intro_07.png"
    secretary "I'm burning up! Gotta take some clothing off."

    scene expression "office/potion_intro_08.png"
    $ renpy.pause ()

    scene expression "office/potion_intro_09.png"
    $ renpy.pause ()

    scene expression "office/potion_intro_10.png"
    $ renpy.pause ()

    scene expression "office/potion_intro_11.png"
    $ renpy.pause ()

    scene expression "office/potion_intro_12.png"
    secretary "Ahh way better."

    scene expression "office/potion_intro_13.png"
    secretary "Headmaster why don't you come over here, so we can better talk to each other."

    scene expression "office/potion_intro_14.png"
    secretary "Oh someone seems to be excited. Does my body turn you on that much?"

    scene expression "office/potion_intro_15.png"
    secretary "Don't worry I will take responsibility."

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
    secretary "Ahh I can't take it anymore, please give it to me!"

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
    principal "Oh I seem to have overdone it. Propably should give her some rest and look for her tomorrow."
    principal_thought """But the potion seems to be working full. But I need to check if she is like this tomorrow 
        as well.
    """

    jump new_day
    
label potion_introduction_2:
    # next day screen
    scene expression "office/potion_intro_36.png"
    secretary "Good Morning Headmaster!"
    principal "Oh good morning! How are you feeling?"
    principal_thought "Wow! Now that's some nice outfit!"

    scene expression "office/potion_intro_37.png"
    secretary "Oh I feel amazing! I never felt so good before drinking the potion!"
    principal "So you remember everything that happened yesterday?"

    scene expression "office/potion_intro_38.png"
    secretary "Oh for sure I remember everything!"

    scene expression "office/potion_intro_39.png"
    secretary "Although I'm really emberassed with us having had sex."

    scene expression "office/potion_intro_40.png"
    secretary "But I'm feeling so free now!"

    scene expression "office/potion_intro_listen.png"
    principal "That's amazing news! Now my plan is to share this feeling among the students."

    scene expression "office/potion_intro_41.png"
    secretary "No, I don't think you will do that."
    principal "What? Why?"

    scene expression "office/potion_intro_42.png"
    secretary "Because you don't have enough potions!"

    scene expression "office/potion_intro_listen.png"
    principal "Oh! Mhh... You're right!"
    principal "Well for one, there are other ways to corrupt... Öhm I mean influence the students."

    scene expression "office/potion_intro_42.png"
    secretary """Oh don't worry dear! I'm fully on your side. I feel great and I want the students to also feel 
        like this.
    """

    scene expression "office/potion_intro_listen.png"
    secretary "So what other ways do you mean?"
    principal """Well there are for example more classical ways like influencing them with lewd materials or more 
        obscure ways like hypnosis.
    """

    scene expression "office/potion_intro_43.png"
    secretary "Hypnosis?"

    scene expression "office/potion_intro_listen.png"
    principal """
        Yeah, I know it's quite absurd. I only heard of ways to do it but I don't know how to do it.

        Well let's just forget that. Well for one we still have 3 potions.

        There was a letter with the potions and it says we can water it down to create more potions with a smaller 
        effect.

        I think if we water 2 potions down enough to serve every student in the school a small drink, then we could 
        create a good base to really influence every student.

        Do you think that works? Would there still be enough of an effect?

        Well I observed the school over the last week and as far as I could see, the students are not only prudish, 
        they are the abstinence in person.

        So I think the classical methods would not work until they are at least a little bit open to the idea sex.

        And without the potion or any other good working method we have no other way.

        So with the watered down potion we could open their minds and then start the real operation.

        And while we change the students, we could reopen the lab and work on reproducing the potion using the last 
        remaining as a draft.
    """

    scene expression "office/potion_intro_44.png"
    secretary "Mhh... That sounds like it could work..."

    scene expression "office/potion_intro_45.png"
    secretary """
        Okay let's do that!

        I think the best would be to distribute the diluted potion during recess.
    """
    principal "Yeah that sounds good, can I entrust that to you?"

    scene expression "office/potion_intro_44.png"
    secretary "Of course! But there are still some problems."
    principal "What do you mean?"
    secretary """The regional representative visits the school every month to make sure the school follows 
        national laws.
    """

    scene expression "office/potion_intro_46.png"
    secretary """
        We have to thank the old headmaster for that. So we have to be careful. He manages our monthly budget and as 
        long as the school follows the rules we don't get budget cuts.

        So we have to play the long game until we find a way to corrupt the department. The representatives change 
        every month so corrupting one wouldn't help.
    """

    scene expression "office/potion_intro_listen.png"
    principal """
        Mhh you're right. I guess we have to be careful. But we can later think of a way to deal with them.

        I have to travel to the city. I have some thing to prepare. I'll be back tomorrow. You meanwhile distribute the 
        potions. Can you make it happen by today's recess?
    """

    scene expression "office/potion_intro_47.png"
    secretary "Sure, just let me handle it!"

    scene expression "office/potion_intro_48.png"
    principal "Nice! I will be on my way then!"

    $ schools["high_school"].set_level(1)
    $ schools["middle_school"].set_level(1)
    $ schools["elementary_school"].set_level(1)

    jump new_day

label pta_meeting:
    subtitles "You enter the conference room."
    subtitles "All representatives already gathered and wait for you."
    principal "Thank you all for gathering today."

    if time.today() == "5.1.2023":
        jump pta_meeting.first_pta_meeting
    
    principal "First point for today. Does someone have anything to discuss today?"

    principal "No? Alright then lets jump straight to the next point."

label .first_pta_meeting:
    principal """
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
    

label .end_meeting:
    principal """
        That should be all for today.\n
        Good work, thank you all for coming and have a nice weekend.
    """
    jump new_daytime

label male_student_scolding:
    subtitles "todo: male scolding"

    return

label mobbing_scolding:
    subtitles "todo: mobbing scolding"

    return
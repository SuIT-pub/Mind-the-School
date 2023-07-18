##################################################
# ----- Office Building Event Handler ----- #
##################################################

init -1 python:
    office_building_after_time_check = Event("office_building_after_time_check", "office_building.after_time_check", 2)
    office_building_fallback         = Event("office_building_fallback",         "office_building_fallback",         2)

    office_building_timed_event = EventStorage("office_building", "", office_building_fallback)
    office_building_events = {
        "tutorial":  EventStorage("tutorial",  "About the school...", office_building_fallback),
        "paperwork": EventStorage("paperwork", "Do paperwork",        office_building_fallback),
        "messages":  EventStorage("messages",  "Check messages",      office_building_fallback),
        "internet":  EventStorage("internet",  "Surf internet",       office_building_fallback),
        "council":   EventStorage("council",   "Council work",        office_building_fallback),
    }

################################################
# ----- Office Building Entry Point ----- #
################################################

label office_building:
    scene office secretary 4 big smile

    call call_available_event(office_building_timed_event) from _call_call_available_event_12

label .after_time_check:

    call call_event_menu (
        "Hello Headmaster! How can I help you?",
        1, 
        7, 
        office_building_events, 
        office_building_fallback,
        character.secretary
    ) from _call_call_event_menu_12

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

    call tutorial_menu from _call_tutorial_menu

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

    show potion intro 01
    secretary "Good Morning, Headmaster!"
    secretary "Someone dropped a package off for you. But there is no sender."

    show potion intro 02
    principal "Mhh... Thats weird, I didn't order anything. Well lets look inside what it is."
    secretary "Are you sure? What if it is something dangerous?"
    principal "I wouldn't know why. I'm sure it will be fine."

    show potion intro 03
    principal "See it's just some bottles. Here let's drink one together!"
    secretary "I don't think that's safe."
    principal "Ah come on! I'm sure it'll be fine."

    show potion intro 04
    principal_thought """
        Good she didn't see the letter in the box.

        In reality, this box comes from my secret supporter. And the bottles are filled with a new special potion.

        Unfortunately he could only send me 4 potions so I have to find a way reproduce them.

        But first gonna test them out!
    """

    show potion intro 05
    principal "Come on lets drink it!"
    secretary "Okay let's do it."

    show potion intro 06
    secretary "Wow it tastes really nice. But are you getting hot as well?"

    show potion intro 07
    secretary "I'm burning up! Gotta take some clothing off."

    show potion intro 08
    $ renpy.pause ()

    show potion intro 09
    $ renpy.pause ()

    show potion intro 10
    $ renpy.pause ()

    show potion intro 11
    $ renpy.pause ()

    show potion intro 12
    secretary "Ahh way better."

    show potion intro 13
    secretary "Headmaster why don't you come over here, so we can better talk to each other."

    show potion intro 14
    secretary "Oh someone seems to be excited. Does my body turn you on that much?"

    show potion intro 15
    secretary "Don't worry I will take responsibility."

    $ renpy.movie_cutscene("images/office/potion intro 16.webm")
    $ renpy.pause(0.0)

    # $ renpy.movie_cutscene("office/potion intro 17.webm", None, -1)
    # $ renpy.pause()

    $ renpy.movie_cutscene("images/office/potion intro 18.webm", -1, -1)
    $ renpy.pause(0.0)

    $ renpy.movie_cutscene("images/office/potion intro 19.webm", -1)

    show potion intro 20
    $ renpy.pause()

    show potion intro 21
    secretary "Ahh I can't take it anymore, please give it to me!"

    $ renpy.movie_cutscene("images/office/potion intro 22.webm")
    $ renpy.movie_cutscene("images/office/potion intro 23.webm", -1, -1)
    $ renpy.movie_cutscene("images/office/potion intro 24.webm", -1, -1)
    $ renpy.movie_cutscene("images/office/potion intro 25.webm", -1, -1)
    $ renpy.movie_cutscene("images/office/potion intro 26.webm", -1, -1)
    $ renpy.movie_cutscene("images/office/potion intro 27.webm")

    show potion intro 28
    $ renpy.pause ()

    show potion intro 29
    $ renpy.pause ()

    $ renpy.movie_cutscene("images/office/potion intro 30.webm", -1, -1)
    $ renpy.movie_cutscene("images/office/potion intro 31.webm", -1, -1)
    $ renpy.movie_cutscene("images/office/potion intro 32.webm", -1, -1)
    $ renpy.movie_cutscene("images/office/potion intro 33.webm")

    show potion intro 34
    $ renpy.pause ()
    
    show potion intro 35
    principal "Oh I seem to have overdone it. Propably should give her some rest and look for her tomorrow."
    principal_thought """But the potion seems to be working full. But I need to check if she is like this tomorrow 
        as well.
    """

    jump new_day
    
label potion_introduction_2:
    # next day screen
    show potion intro 36
    secretary "Good Morning Headmaster!"
    principal "Oh good morning! How are you feeling?"
    principal_thought "Wow! Now that's some nice outfit!"

    show potion intro 37
    secretary "Oh I feel amazing! I never felt so good before drinking the potion!"
    principal "So you remember everything that happened yesterday?"

    show potion intro 38
    secretary "Oh for sure I remember everything!"

    show potion intro 39
    secretary "Although I'm really emberassed with us having had sex."

    show potion intro 40
    secretary "But I'm feeling so free now!"

    scene expression "office/potion intro listen.png"
    principal "That's amazing news! Now my plan is to share this feeling among the students."

    show potion intro 41
    secretary "No, I don't think you will do that."
    principal "What? Why?"

    show potion intro 42
    secretary "Because you don't have enough potions!"

    scene expression "office/potion intro listen.png"
    principal "Oh! Mhh... You're right!"
    principal "Well for one, there are other ways to corrupt... Öhm I mean influence the students."

    show potion intro 42
    secretary """Oh don't worry dear! I'm fully on your side. I feel great and I want the students to also feel 
        like this.
    """

    scene expression "office/potion intro listen.png"
    secretary "So what other ways do you mean?"
    principal """Well there are for example more classical ways like influencing them with lewd materials or more 
        obscure ways like hypnosis.
    """

    show potion intro 43
    secretary "Hypnosis?"

    scene expression "office/potion intro listen.png"
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

    show potion intro 44
    secretary "Mhh... That sounds like it could work..."

    show potion intro 45
    secretary """
        Okay let's do that!

        I think the best would be to distribute the diluted potion during recess.
    """
    principal "Yeah that sounds good, can I entrust that to you?"

    show potion intro 44
    secretary "Of course! But there are still some problems."
    principal "What do you mean?"
    secretary """The regional representative visits the school every month to make sure the school follows 
        national laws.
    """

    show potion intro 46
    secretary """
        We have to thank the old headmaster for that. So we have to be careful. He manages our monthly budget and as 
        long as the school follows the rules we don't get budget cuts.

        So we have to play the long game until we find a way to corrupt the department. The representatives change 
        every month so corrupting one wouldn't help.
    """

    scene expression "office/potion intro listen.png"
    principal """
        Mhh you're right. I guess we have to be careful. But we can later think of a way to deal with them.

        I have to travel to the city. I have some thing to prepare. I'll be back tomorrow. You meanwhile distribute the 
        potions. Can you make it happen by today's recess?
    """

    show potion intro 47
    secretary "Sure, just let me handle it!"

    show potion intro 48
    principal "Nice! I will be on my way then!"

    $ schools["high_school"].set_level(1)
    $ schools["middle_school"].set_level(1)
    $ schools["elementary_school"].set_level(1)

    jump new_day

label pta_meeting:
    subtitles "You enter the conference room."
    subtitles "All representatives already gathered and wait for you."
    principal "Thank you all for gathering today."

    principal "First point for today. Does someone have anything to discuss today?"

    principal "No? Alright then lets jump straight to the next point."

    jump new_daytime

label first_pta_meeting:
    subtitles "You enter the conference room."
    subtitles "All representatives already gathered and wait for you."
    principal "Thank you all for gathering today."

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
init -1 python:
    def after_load_event_check(location: str, events: Dict[str, EventStorage], general_event: EventStorage, timed_event: TempEventStorage):
        
        timed_event.check_all_events()
        general_event.check_all_events()
        if events != None:
            map(lambda x: x.check_all_events(), events.values())

    def add_temp_event(event: Event):
        temp_time_check_events.add_event(event)
    def remove_temp_event(event: Event):
        temp_time_check_events.remove_event(event)

    after_temp_event_check = Event(2, "time_event_check.after_temp_event_check")
    after_event_check      = Event(2, "time_event_check.after_event_check")

    temp_time_check_events = TempEventStorage("temp_time_check_events", "misc", after_temp_event_check)
    time_check_events      = EventStorage("time_check_events", "misc", after_event_check)

init 1 python:
    tutorial_1_event = Event(2, "tutorial_1", 
        IntroCondition(),
        TimeCondition(day = 2, month = 1, year = 2023, daytime = 1),
        thumbnail = "images/events/intro/intro tutorial 9.webp"
    )

    first_week_epilogue_event = Event(1, "first_week_epilogue", 
        IntroCondition(),
        TimeCondition(day = 5, month = 1, year = 2023, daytime = 2),
        thumbnail = "images/events/first week/first week epilogue 8.webp"
    )

    first_week_epilogue_final_event = Event(1, "first_week_epilogue_final", 
        TimeCondition(day = 10, month = 1, year = 2023, daytime = 1),
        thumbnail = "images/events/first week/first week epilogue final 3.webp"
    )

    first_pta_meeting_event = Event(1, "first_pta_meeting", 
        IntroCondition(),
        TimeCondition(day = 5, month = 1, year = 2023, daytime = 1),
        thumbnail = "images/events/pta/first meeting/first pta meeting 0 0.webp"
    )

    pta_meeting_event = Event(2, "pta_meeting",
        TimeCondition(weekday = 5, daytime = 1)
    )

    new_week_event = Event(2, "new_week",
        TimeCondition(weekday = 1, daytime = 1)
    )

    end_of_month_event = Event(2, "end_of_month",
        TimeCondition(day = 1, daytime = 1)
    )

    event_all_events_seen_event = Event(1,
        "event_all_events_seen",
        GameDataCondition("all_events_seen", True)
    )

    event_reached_max_stats_event = Event(1,
        "event_reached_max_stats",
        StatCondition(inhibition = "90-", corruption = "5+")
    )

    intro_check_all_facilities_event = Event(2, "intro_check_all_facilities", 
        TimeCondition(day = 2, month = 1, year = 2023, daytime = 1)
    )

    intro_check_all_first_potions_event = Event(1, "intro_check_all_first_potions", 
        TimeCondition(day = 9, month = 1, year = 2023, daytime = 4)
    )

    game_over_happiness_event = Event(1, "game_over_happiness", 
        StatCondition(happiness = "0-")
    )

    game_over_education_event = Event(1, "game_over_education", 
        StatCondition(education = "0-")
    )

    game_over_reputation_event = Event(1, "game_over_reputation", 
        StatCondition(reputation = "0-")
    )

    time_check_events.add_event(
        tutorial_1_event, 
        first_week_epilogue_event, 
        first_week_epilogue_final_event, 
        first_pta_meeting_event, 
        pta_meeting_event, 
        new_week_event,
        end_of_month_event,
        intro_check_all_facilities_event,
        intro_check_all_first_potions_event,
        game_over_happiness_event,
        game_over_education_event,
        game_over_reputation_event,
    )
    temp_time_check_events.add_event(
        event_all_events_seen_event, 
        event_reached_max_stats_event,
    )

label time_event_check ():
    hide screen school_overview_map
    hide screen school_overview_stats
    hide screen school_overview_buttons

    call call_available_event(temp_time_check_events, 0, True, with_removal = True) from time_event_check_1

label .after_temp_event_check (**kwargs):

    call call_available_event(time_check_events, 0, True) from time_event_check_2

label .after_event_check (**kwargs):
    return

############################
# ----- Intro Events ----- #
############################

label game_over_happiness (**kwargs):
    $ begin_event()

    show screen black_error_screen_text ("")

    nvl clear

    nv_text "The students happiness plunged to an all-time low."
    nv_text "The students are revolting and protesting against you, demanding the school board to fire you."
    nv_text "The school board has no choice but to fire you."
    nv_text "You are now unemployed and have to find a new job."

    $ MainMenu(confirm=False)()

label game_over_education (**kwargs):
    $ begin_event()

    show screen black_error_screen_text ("")

    nvl clear

    nv_text "The school board noticed the lack of education and the low grades of the students."
    nv_text "They decided to fire you and hire a new headmaster."

    $ MainMenu(confirm=False)()

label game_over_reputation (**kwargs):
    $ begin_event()

    show screen black_error_screen_text ("")
    
    nvl clear

    nv_text "Your bad reputation made it into the news."
    nv_text "The school board put under pressure by the public, decided to fire you."

    $ MainMenu(confirm=False)()

label intro_check_all_facilities (**kwargs):
    $ begin_event()

    scene bg school overview idle
    show screen school_overview_stats

    headmaster_thought "Okay time to check all the facilities and see if they need improvement."
    headmaster_thought "I should try to inspect all the locations until friday where I will have my first PTA meeting."

    jump map_overview

label intro_check_all_first_potions (**kwargs):
    $ begin_event()

    scene bg school overview idle
    show screen school_overview_stats

    headmaster_thought "By this time all the students should have eaten."
    headmaster_thought "Time to go around campus and check on the students and the potion's effect."

    jump map_overview

label event_all_events_seen (**kwargs):
    $ begin_event()
    $ hide_all()
    
    $ renpy.choice_for_skipping()

    show thanks 1 with dissolveM
    dev "Thank you for playing, you found all events, that are currently in this version."
    dev "You can still continue playing. Some events have different variants that change every time you visit them."

    jump new_daytime

label event_reached_max_stats (**kwargs):
    $ begin_event()
    $ hide_all()
    
    $ renpy.choice_for_skipping()

    show thanks 1 with dissolveM
    dev "Thank you for playing, you reached a stat level that pretty much maxes out your experience."
    dev "You can still continue to play, but raising your stats beyond this point will not have any effect."
    dev "With your current stat level, you will be able to unlock all there is to see in this version."
    dev "Thanks for playing!"

    jump new_daytime

label tutorial_1 (**kwargs):
    $ begin_event(**kwargs)

    show screen black_error_screen_text ("")

    if get_kwargs("in_replay", False, **kwargs):
        jump .tutorial_2

    menu:
        "Play tutorial?"
        "Yes":
            jump .tutorial_2
        "No":
            jump .tutorial_3

label .tutorial_2:
    hide screen black_error_screen_text

    show intro tutorial 1 with dissolveM
    dev "Hello, I'm Suit-Kun and welcome to Mind the School. I'm going to explain a few things about the game."
    dev "The game is a simple event-driven sandbox management game. This means that you visit the available locations, an event happens and you get stat points or other effects."
    dev "Then, after fulfilling certain conditions, you can unlock new rules, clubs or buildings for your school."
    if loli_content > 0:
        dev "There are several schools on campus. Each school has its own rules and clubs. So you have to unlock new things for each school individually."
    dev "Now for the game elements."
    dev "In the background you can see a map of the campus."
    dev "Your lovely secretary has probably already shown you the various facilities, so I'll just show you the overlay."
    
    show intro tutorial 2 with dissolveM
    dev "These are all the facilities on campus. You can click or tap on them to enter and trigger events."
    
    show intro tutorial 3 with dissolveM
    dev "At a facility, you are given a selection of activities you can do at the facility. The activities you can do depend on the level of your school and the day and time."
    dev "You can select the choices either by clicking them or pressing the corresponding buttons shown in the brackets. You can turn this function off in the settings."

    show intro tutorial 4 with dissolveM
    dev "This version has a little extra that will be hidden behind an item in later versions, but keep an eye out for this icon in the top left corner and feel free to click on it."

    show intro tutorial 3 with dissolveM
    dev "An activity usually lasts for one time unit."
    
    show intro tutorial 1 with dissolveM
    dev "While we're at it. One day is separated into 7 segments. Morning, Early Noon, Noon, Early Afternoon, Afternoon, Evening and Night."
    
    show intro tutorial 5 with dissolveM
    dev "You can see the current date and time up here."
    
    show intro tutorial 6 with dissolveM
    dev "And here you can skip to the next time segment."
    
    show intro tutorial 7 with dissolveM
    dev "Here you can see your current stats."
    if loli_content > 0:
        dev "Remember that these statistics show the average of all schools. So if one school has 100 points and another has 0 points, this table would show a score of 50."
    dev "I'm not going to explain these stats. You can find a more detailed explanation of the stats in your journal."
    dev "The stats also have no effect on the game at the moment. This will change in future versions." ######## version dependent
    
    show intro tutorial 8 with dissolveM
    dev "You can find the journal up here."    

    show intro tutorial 9 with dissolveM
    dev "This is the journal. Here you will find all the information you need to manage your school."

    if loli_content > 0:
        show intro tutorial 10 with dissolveM
        dev "Here you can switch between the schools."

    show intro tutorial 11 with dissolveM
    dev "And here you can change the page."

    show intro tutorial 12 with dissolveM
    dev "Here you can see the statistics for the current school."
    
    show intro tutorial 13 with dissolveM
    dev "You can click on a stat to get more detailed information on the right hand side of the journal."

    show intro tutorial 14 with dissolveM
    dev "The upper part is the description of the stat, divided into three parts."
    dev "The first part describes the level of the stat, the second part describes the stat itself and the last part describes how to increase the stat."

    show intro tutorial 15 with dissolveM
    dev "The bottom part would normally be an image showing and representing the current stat level."
    dev "But I haven't made them yet. They will be added later." ######## version dependent

    show intro tutorial 16 with dissolveM
    dev "Now we come to the Rules page in your journal. This is where you can manage your school rules."
    dev "It is very similar to the school overview page. On the left you have an overview of all the rules."
    dev "Rules may not be visible until certain conditions are met."
    dev "Rules highlighted in green are already unlocked and active."
    dev "Clicking on a rule will bring up a detail page on the right."

    show intro tutorial 17 with dissolveM
    dev "The top part is again a description of the rule and the conditions for unlocking the rule."
    
    show intro tutorial 18 with dissolveM
    dev "Below this is another image. You can click on the image to get a full screen view of it."
    dev "The images for some rules change as you progress through the game to better represent the effects behind the rule, according to the school's state."
    dev "So it may be worth revisiting some of the rules after you have upgraded a school. ;)"
    
    show intro tutorial 19 with dissolveM
    dev "Next to the image you will see a small overview of the conditions that need to be fulfilled."
    dev "However, only conditions related to the school's statistics are shown here to give a clearer picture of the stats required."
    dev "The list in the description will always include all conditions."

    show intro tutorial 20 with dissolveM
    dev "Here would be a button to queue this rule to be voted on by the Parent Teacher Association (PTA). But the PTA isn't implemented yet, so this will be added later."
    
    show intro tutorial 21 with dissolveM
    dev "There is also the Clubs page. It is structured exactly the same as the rules page."

    show intro tutorial 22 with dissolveM
    dev "The same applies to the Buildings page."
    if loli_content > 0:
        dev "The only difference is that the buildings page doesn't have the school tabs at the top, as the changes made here affect the whole campus."

    show intro tutorial 1 with dissolveM
    dev "That's all. Thanks for listening. :D"

label .tutorial_3:

    hide screen black_error_screen_text

    if 'kwargs' not in locals() and 'kwargs' not in globals():
        $ kwargs = {}

    $ end_event('none', **kwargs)

    # jump first_week_epilogue_final.skip

    # dev "[intro_dev_message]"

    return

image anim_first_week_epilogue_17 = Movie(play ="images/events/first week/first week epilogue 17.webm", start_image = "images/events/first week/first week epilogue 17_1.webp", loop = True)
image anim_first_week_epilogue_18 = Movie(play ="images/events/first week/first week epilogue 18.webm", start_image = "images/events/first week/first week epilogue 18_1.webp", loop = True)
image anim_first_week_epilogue_19 = Movie(play ="images/events/first week/first week epilogue 19.webm", start_image = "images/events/first week/first week epilogue 19_1.webp", loop = True)
image anim_first_week_epilogue_20 = Movie(play ="images/events/first week/first week epilogue 20.webm", start_image = "images/events/first week/first week epilogue 20_1.webp", loop = True)
image anim_first_week_epilogue_21 = Movie(play ="images/events/first week/first week epilogue 21.webm", start_image = "images/events/first week/first week epilogue 21_1.webp", loop = True)
image anim_first_week_epilogue_22 = Movie(play ="images/events/first week/first week epilogue 22.webm", start_image = "images/events/first week/first week epilogue 22_1.webp", loop = True)
image anim_first_week_epilogue_23 = Movie(play ="images/events/first week/first week epilogue 23.webm", start_image = "images/events/first week/first week epilogue 23_1.webp", loop = True)
image anim_first_week_epilogue_24 = Movie(play ="images/events/first week/first week epilogue 24.webm", start_image = "images/events/first week/first week epilogue 24_1.webp", image = "images/events/first week/first week epilogue 24_2.webp", loop = False)

label first_week_epilogue (**kwargs):

    $ begin_event(**kwargs)

    $ hide_all()

    $ image = Image_Series("images/events/first week/first_week_epilogue <step>.webp")

    $ image.show(0)
    secretary "That was a good first meeting Mr. [headmaster_last_name]. "
    headmaster "Thank you! And please just call me [headmaster_first_name]. It's a bit awkward to be called so formal."

    # first week epilogue 2
    $ image.show(0)
    secretary "Okay [headmaster_first_name]."
    headmaster "Good! Could you please call me a cab? I have to drive into town to prepare some things for my time at the school."
    $ image.show(1)
    secretary "I'll get right on it, but can I ask what you have planned?"
    $ image.show(2)
    headmaster "You can but I can't really answer that. Some of it is classified and the rest isn't secured yet."
    headmaster "If I'm successful, I'll let you know as soon as possible."

    # first week epilogue 3
    $ image.show(3)
    secretary "Okay, I'll go call your cab."
    headmaster "Thank you very much."
    
    call screen black_screen_text ("20 minutes later")

    # first week epilogue 4
    $ image.show(4)
    secretary "[headmaster_first_name]! Your cab just arrived!"
    headmaster "Perfect! I'll be off then. Expect me back early on Monday. I need all the time I can get."

    call screen black_screen_text ("Monday, 8 January 2023")

    show first week epilogue 5 
    # headmaster enters with two boxes
    secretary "Good Morning, welcome back!"
    secretary "These 2 Boxes got delivered just an hour ago!"
    headmaster "Thank you very much!"

    show first week epilogue 6 with dissolveM
    # both put boxes on desk
    secretary "Is this the stuff you had to prepare?"
    headmaster "Yes, at least some of it. Some things take a little more time to prepare."
    secretary "What is it?"
    headmaster "Here I'll show you."

    show first week epilogue 7 with dissolveM
    # headmaster opens one box and reveals multiple bottles
    headmaster "This is a special energizer."
    secretary "Energizer?"
    
    show first week epilogue 8 with dissolveM
    # headmaster takes one bottle
    headmaster "Yes, a close friend of mine is a biochemist and I asked him to put this stuff together."
    headmaster "He has helped me with my previous projects and he is truly a master alchemist."
    headmaster "This drink is a special blend to help students relax and concentrate. Weird, isn't it?"
    secretary "Does it really work?"
    headmaster "Sure I have full faith in my friends abilities, but you can try one if you want."

    show first week epilogue 9 with dissolveM
    # headmaster gives the bottle to the secretary
    secretary "Can I drink it? Is it really safe?"
    headmaster "Absolutely, it is absolutely safe. In fact, it's really healthy. It is practically is a vitamin shake."
    headmaster "It's not a meal replacement, but it's packed with healthy vitamins and protein. It is also low in fat and sugar!"
    secretary "Oh wow, that sounds wonderful! I'd love to try one."

    show first week epilogue 10 with dissolveM
    # secretary drinks potion
    secretary "Oh that's really tasty!"
    show first week epilogue 11 with dissolveM
    secretary "And... Oh wow! The effect is almost immediate. I feel so much better! I don't feel any of the bad sleep I had last night!"
    secretary "Oh wow! That's amazing, I also feel much more focused. For example, I notice that sometimes you look at my breasts."
    headmaster "Oh... Ah... Ehm..."

    show first week epilogue 12 with dissolveM
    # secretary laughs
    secretary "Haha! Don't worry about it! I know I have very big breasts."
    secretary "It's normal for people to stare at them. Do you want to see them?"
    headmaster "..."
    secretary "Don't be so shy. I know you want to!"

    show first week epilogue 13 with dissolveM
    # secretary opens blouse
    secretary "Here! They're bigger than they look in those clothes, aren't they."

    show first week epilogue 14 with dissolveM
    # secretary takes of bra
    secretary "Here, touch them! I'm really proud of them, they're nice and firm even though they're this big."

    show first week epilogue 15 with dissolveM
    # headmaster touches/kneads breasts
    secretary "Yeah that's nice! Mhhh..."

    show first week epilogue 16 with dissolveM
    # secretary touches headmasters crotch
    secretary "Ahh you seem to like them as well."
    secretary "Let me help you out."

    scene anim_first_week_epilogue_17 with dissolveM
    pause

    scene anim_first_week_epilogue_18 with dissolveM
    pause

    scene anim_first_week_epilogue_19 with dissolveM
    pause

    scene anim_first_week_epilogue_20 with dissolveM
    pause

    scene anim_first_week_epilogue_21 with dissolveM
    pause

    scene anim_first_week_epilogue_22 with dissolveM
    pause

    scene anim_first_week_epilogue_23 with dissolveM
    pause

    scene anim_first_week_epilogue_24 with dissolveM
    pause


    # first week epilogue 24
    # floor hardcore

    hide anim_first_week_epilogue_24

    show first week epilogue 25 with dissolveM
    headmaster_thought "Oh seems like I overdid it a little bit. But that was really hot. The effect of the potion lives up to my friend's promise."
    # secretary passes out

    show first week epilogue 26 with dissolveM
    headmaster_thought "Let's get you to the couch."

    show first week epilogue 27 with dissolveM
    # headmaster puts secretary on the couch
    headmaster_thought "Let's see how she feels after she rested. Gotta get her a blanket first though."

    call screen black_screen_text ("Tuesday, 9 January 2023")

    show first week epilogue 28 with dissolveM
    # headmaster enters office
    headmaster "Ahh she's already gone."

    show first week epilogue 29 with dissolveM
    pause
    # headmaster approaches the boxes
    # headmaster starts handling boxes

    show first week epilogue 30 with dissolveM
    # secretary enters office
    headmaster "Ah good morning! ohh..."

    show first week epilogue 31 with dissolveM
    secretary "Good morning [headmaster_first_name]! What's wrong?"
    headmaster "Ehm, nice outfit!"

    show first week epilogue 32 with dissolveM
    # secretary poses
    secretary "Oh yeah, do you like it? This morning I just felt like I would rather wear this than my old outfit."
    show first week epilogue 33 with dissolveM
    headmaster "It fits you really well! So... about yesterday..."
    show first week epilogue 34 with dissolveM
    secretary "Oh when we had sex? Yeah that was nice!"
    secretary "At first I was a little surprised because I would never behave like that, but strangely enough I didn't hate it."
    show first week epilogue 35 with dissolveM
    secretary "It was as if my body was urging me to open up to the situation."
    secretary "And I am really glad that it happened. But is this another effect of the drink I had yesterday?"
    show first week epilogue 36 with dissolveM
    headmaster "Well, I knew it would have a similar effect. I knew the consumer would open up and feel more free, but I didn't expect the effect to be this strong."
    headmaster "As I see, the effect is not as strong now as it was yesterday..."
    show first week epilogue 37 with dissolveM
    secretary "Yes, you're right. Even though I feel freer, I don't feel so overwhelmed anymore."
    show first week epilogue 36 with dissolveM
    headmaster "Mhh... It probably has to do with the change in your mindset. Yesterday it had to adjust to the new influx of emotions and feelings."
    headmaster "But now that your mind is used to the new way, it is calmer. It could also be the drink."
    headmaster "Perhaps it distributes itself the fastest in the libido so it overwhelms the other body mechanisms, and now it is more evenly distributed so you are more calm."
    show first week epilogue 37 with dissolveM
    secretary "I can't really follow, but from what I can see, it works beautifully."
    show first week epilogue 36 with dissolveM
    headmaster "It does, but there is one problem. As you can see, we only have three bottles left. My friend unfortunately had to fly to Brazil so he could only produce 4 bottles."
    show first week epilogue 38 with dissolveM
    secretary "What? And you still gave me a full bottle?"
    show first week epilogue 36 with dissolveM
    headmaster "That is no problem, I was planning to do that anyway."
    headmaster "He said the drink could be diluted down to a 100 drinks. Of course, the effect would be diminished, but it would still have an effect."
    headmaster "So I came up with the following plan. We will take a bottle, dilute it enough, and hand out one of these drinks to every student at recess today."
    headmaster "One thing I have observed at this school is how extremely prudish the students are. They don't just avoid the subject, they outright hate it."
    show first week epilogue 39 with dissolveM
    secretary "Yeah, I always wondered about that..."
    show first week epilogue 36 with dissolveM
    headmaster "So I guess one drink of the diluted potion should be enough to open these kids up to the subject."
    headmaster "After that it should be possible to influence them in more traditional ways in addition to the more exotic ways."
    show first week epilogue 37 with dissolveM
    secretary "What do you mean by 'more exotic ways'?"
    show first week epilogue 36 with dissolveM
    headmaster "Well, I planned to use methods like this potion and hypnosis."
    show first week epilogue 40 with dissolveM
    secretary "Hypnosis?!"
    show first week epilogue 36 with dissolveM
    headmaster "Yeah!"
    show first week epilogue 40 with dissolveM
    secretary "Does that even work?"
    show first week epilogue 36 with dissolveM
    headmaster "Oh yeah, it definitely works, but it takes a lot of preparation, so I couldn't prepare it over the weekend."
    headmaster "For it to work, the students must first be receptive to the subject and then they will be able to be influenced by hypnosis."
    headmaster "But the effects are quite weak so it needs to be set up correctly to provide a constant influence. But for that it will be very cost effective."
    headmaster "So for now we are going to work with basic influences, such as exposure to appropriate material in their free time and classes in a way that doesn't raise suspicion."
    show first week epilogue 37 with dissolveM
    secretary "Sounds like you have a very thorough plan."
    show first week epilogue 36 with dissolveM
    headmaster "Well, I have. I have been working towards my goal for most of my life, and that includes reforming various institutions."
    headmaster "So this school is just a stepping stone in my plan to reform the society."
    show first week epilogue 41 with dissolveM
    secretary "And I'm happy to help you!"
    show first week epilogue 42 with dissolveM
    headmaster "And for that I thank you very much!"
    show first week epilogue 41 with dissolveM
    # headmaster slaps secretaries ass
    secretary "But what do you have planned for the remaining two potions."
    show first week epilogue 42 with dissolveM
    headmaster "Oh yeah I plan to reopen the lab building and to add a private laboratory where I can work on reproducing the potion."
    headmaster "I got some instructions from my buddy, but I still have to work on it and these potions will help me."
    headmaster "Once I have a few prototypes, the process of changing the school should be much faster."
    headmaster "Recreating the potions will probably be quite a task. I'm sure the first iterations will have a much weaker effect, if any effect at all."
    headmaster "But first, let's work on diluting the first potion down for the students. It's getting late and we want to be ready for recess."
    show first week epilogue 35 with dissolveM
    secretary "Yeah let's do it!"

    call screen black_screen_text ("Later at recess")

    show first week epilogue 43 with dissolveM
    headmaster "Phew we just got it finished! Now we have to distribute it."
    show first week epilogue 44 with dissolveM
    secretary "Ah I already organised something!"
    secretary "I asked the kiosk vendor to give one drink out for free for every order."
    secretary "Because it is the only place to get food here, it is guaranteed that every student gets at least one drink."
    secretary "I also asked to make sure to only give out one per person."
    show first week epilogue 45 with dissolveM
    headmaster "Perfect! I'm glad to have you as my secretary!"
    secretary "Well you already thanked me for that."
    show first week epilogue 46 with dissolveM
    headmaster "Öhm... Did I? Ohhhh you mean that time!"
    secretary "Yeah that was really nice."
    headmaster "Alright then let's go eat something as well. I think we aren't needed here for now."
    secretary "Sounds good!"

    # headmaster and secretary take some food from kiosk and sit down among the students and start eating an conversing
    # while they eat, they notice the students get more fidgety

    # some students start to take off some clothes
    # other start groping their own breasts
    # others start kissing each other
    show first week epilogue 47 with dissolveM
    pause
    show first week epilogue 48 with dissolveM
    pause
    show first week epilogue 49 with dissolveM
    pause
    show first week epilogue 50 with dissolveM

    headmaster "Ah the potions seem to start taking effect."
    secretary "Yes! I guess school will be more fun now."

    # for the rest of the day the strong effects can be observed throughout the campus
    
    if not is_in_replay:
        $ set_level_for_char(1, "school", charList)
        $ set_level_for_char(1, "teacher", charList["staff"])
        $ set_level_for_char(1, "parent", charList)
        $ set_level_for_char(5, "secretary", charList["staff"])

        $ set_all_buildings_blocked(False)

        $ set_building_blocked("kiosk")

        $ time.set_time(day = 9, daytime = 3)

    $ end_event('new_daytime', **kwargs)

label first_week_epilogue_final (**kwargs): 
    $ begin_event(**kwargs)

    $ set_all_buildings_blocked(False)

    $ hide_all()
    $ secretary_name = get_name_first('secretary')
    $ headmaster_first_name = get_name_first('headmaster')
    $ headmaster_last_name = get_name_last('headmaster')

    hide screen black_screen_text

    show first week epilogue final 1 with dissolveM
    # headmaster enters campus
    headmaster_thought "Oh hello! The effects seem to have diminished quite a lot."
    show first week epilogue final 2 with dissolveM
    headmaster_thought "I guess the potion seems to have fully settled in their systems and their bodies to have adjusted to the new influx of hormones."
    show first week epilogue final 3 with dissolveM
    headmaster_thought "But I guess that's a good thing. It would be bad if they were constantly horny without adapting to the change."

    # headmaster approaches student
    show first week epilogue final 4 with dissolveM
    headmaster "Oh hello! How are you doing?"
    sgirl "Oh hello Mr. [headmaster_last_name]! I'm doing great! I kinda feel a bit more relaxed than yesterday! I think..." (name='Miwa Igarashi')
    show first week epilogue final 5 with dissolveM
    headmaster "Oh that's good to hear! But what do you mean with you think? Is everything really alright?"
    show first week epilogue final 6 with dissolveM
    sgirl "Oh yeah, yeah! Everything is fine, it's just, I have the feeling there is a gap in my memory. I can't remember anything from yesterday after recess."  (name='Miwa Igarashi')
    show first week epilogue final 7 with dissolveM
    sgirl "I only know to have been extremely happy and relaxed yesterday, but I can't remember anything else." (name='Miwa Igarashi')
    show first week epilogue final 8 with dissolveM
    headmaster "Hmm interesting... Well at least you are feeling fine. Pay the nurse a visit if you start to feel unwell."
    sgirl "Okay, I will! Thank you Mr. [headmaster_last_name]!" (name='Miwa Igarashi')

    # school girl walks off, headmaster stays a little bit in thoughts
    show first week epilogue final 9 with dissolveM
    headmaster_thought "Hmm... that's an interesting effect. She doesn't remember anything that happened yesterday, but the long term effect seems to still be in place."
    show first week epilogue final 10 with dissolveM
    headmaster_thought "[secretary_name] didn't seem to have any memory gaps whatsoever. I wonder if it has to do with the fact that the students go a diluted version."

    # secretary approaches from behind
    show first week epilogue final 11 with dissolveM
    secretary "Oh hello [headmaster_first_name]! How are you doing?"
    headmaster "Oh hello [secretary_name]! I'm doing fine. I was just talking to one of the students."
    headmaster "She said she can't remember anything from yesterday after recess. Do you have any idea how this could have come about?"
    headmaster "I mean you didn't have this problem, did you?"
    show first week epilogue final 13 with dissolveM
    secretary "No I don't think so."
    show first week epilogue final 14 with dissolveM
    headmaster "I think it had to do with the fact that the students were given a diluted version of the potion."
    headmaster "My mate was explaining to me a bit about its effects and mechanics. I couldn't quite follow, but I think he said something about using certain proteins to help the brain cope with the large influx of emotions during the acclimatisation phase."
    headmaster "Maybe the diluted version doesn't have enough of those proteins to help the brain deal with the emotions. I mean, my mate said that if you dilute the potion by 1 to 100, the effects don't diminish that much."
    headmaster "So I think the balance was upset and the students experienced something like a blackout, where the brain just stops storing memories."
    show first week epilogue final 15 with dissolveM
    secretary "Well, at least the side effects weren't more serious."
    show first week epilogue final 16 with dissolveM
    headmaster "When I think about it, it might have been a good thing."
    show first week epilogue final 15 with dissolveM
    secretary "What do you mean?"
    show first week epilogue final 16 with dissolveM
    headmaster "I have noticed that the students are almost back to their old selves. They are more relaxed and not so stuck up, and they already seem to have modified their uniforms, but the actual long term effect seems rather minimal compared to the effect it had on you."
    headmaster "I can't imagine how the students would react in their current state if they could remember everything that happened yesterday."
    show first week epilogue final 15 with dissolveM
    secretary "Oh yes, you're right. That would have been a disaster."
    show first week epilogue final 16 with dissolveM
    headmaster "Well, that's good to know, but until we get the lab back up and running there's nothing we can really do about it."
    headmaster "I need to reproduce the potion first. I'm not sure I can do it the way my buddy did it."
    headmaster "The first iterations are likely to have a much weaker effect, if any."
    show first week epilogue final 15 with dissolveM
    secretary "I guess we'll see when the time comes."
    show first week epilogue final 17 with dissolveM
    headmaster "Oh I guess classes just started. I think I should start my rounds."
    show first week epilogue final 18 with dissolveM
    secretary "Good luck."

    $ end_event('none', **kwargs)

label .skip:

    hide screen black_error_screen_text

    show thanks 1 with dissolveM
    
    # dev "[intro_dev_message]"

    dev "This is where the actual free roaming begins."
    dev "Please keep in mind, that this game is still an early version and thus has a limited amount of events and potential bugs."
    dev "Also try to revisit some events as some have different variants that change randomly."
    show thanks 2 with dissolveM
    dev "I hope you'll still enjoy the game."
    dev "To stay up to date on development visit my {a=[patreon]}Patreon{/a} and {a=[discord]}Discord{/a}."
    dev "I'd be happy if you leave some feedback or some ideas on the Discord so I can work to further improve this game!"

    jump map_overview

##################################
# ----- Daily Check Events ----- #
##################################

label new_week (**kwargs):
    $ change_money_with_modifier(0, 'payroll_weekly')
    return

label end_of_month (**kwargs):
    $ change_money_with_modifier(0, 'payroll_monthly')
    # $ change_stat(MONEY, 1000)

    return
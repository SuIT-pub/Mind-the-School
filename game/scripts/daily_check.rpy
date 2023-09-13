init -1 python:
    def add_temp_event(event):
        temp_time_check_events.add_event(event)
    def remove_temp_event(event):
        temp_time_check_events.remove_event(event)

    after_temp_event_check = Event("after_temp_event_check", "time_event_check.after_temp_event_check", 2)
    after_event_check      = Event("after_event_check",      "time_event_check.after_event_check",      2)

    temp_check_events      = EventStorage("temp_check_events",      "", after_event_check     )
    temp_time_check_events = TempEventStorage("temp_time_check_events", "", after_temp_event_check)

    temp_check_events.add_event(Event("first_day_introduction", "first_day_introduction", 2,
        TimeCondition(day = 1, month = 1, year = 2023, daytime = 1)
    ))

    temp_check_events.add_event(Event("tutorial_1", "tutorial_1", 1,
        TimeCondition(day = 2, month = 1, year = 2023, daytime = 1)
    ))

    temp_check_events.add_event(Event("first_week_epilogue", "first_week_epilogue", 1,
        TimeCondition(day = 5, month = 1, year = 2023, daytime = 1)
    ))

    temp_check_events.add_event(Event("first_week_epilogue_final", "first_week_epilogue_final", 1,
        TimeCondition(day = 10, month = 1, year = 2023, daytime = 1)
    ))

    temp_check_events.add_event(Event("weekly_assembly_first", "weekly_assembly_first", 2,
        TimeCondition(day = 1, month = 1, year = 2023, daytime = 1)
    ))

    # temp_check_events.add_event(Event("weekly_assembly", "weekly_assembly", 2,
    #     TimeCondition(weekday = 1, daytime = 1)
    # ))

    # temp_check_events.add_event(Event("first_pta_meeting", "first_pta_meeting", 1,
    #     TimeCondition(day = 5, month = 1, year = 2023, daytime = 1)
    # ))

    # temp_check_events.add_event(Event("pta_meeting1", "pta_meeting", 2,
    #     TimeCondition(day = 5, daytime = 1)
    # ))

    # temp_check_events.add_event(Event("pta_meeting2", "pta_meeting", 2,
    #     TimeCondition(day = 19, daytime = 1)
    # ))


label time_event_check:

    hide screen school_overview_map
    hide screen school_overview_stats
    hide screen school_overview_buttons
    
    call call_available_event(temp_time_check_events) from time_event_check_1

label .after_temp_event_check:

    call call_available_event(temp_check_events) from time_event_check_2

label .after_event_check:
    return

##################################
# ----- Daily Check Events ----- #
##################################

label tutorial_1:
    show screen black_error_screen_text ("")

    menu:
        subtitles "Play tutorial?"
        "Yes":
            jump .tutorial_2
        "No":
            jump .tutorial_3

label .tutorial_2:
    hide screen black_error_screen_text

    show intro tutorial 1
    dev "Hello, I'm Suit-Kun and welcome to Mind the School. I'm going to explain a few things about the game."
    dev "The game is a simple event-driven sandbox management game. This means that you visit the available locations, an event happens and you get stat points or other effects."
    dev "Then, after fulfilling certain conditions, you can unlock new rules, clubs or buildings for your school."
    if loli_content > 0:
        dev "There are several schools on campus. Each school has its own rules and clubs. So you have to unlock new things for each school individually."
    dev "Now for the game elements."
    dev "In the background you can see a map of the campus."
    dev "Your lovely secretary has probably already shown you the various facilities, so I'll just show you the overlay."
    
    show intro tutorial 2
    dev "These are all the facilities on campus. You can click or tap on them to enter and trigger events."
    
    show intro tutorial 3
    dev "At a facility, you'll be given a selection of activities you can do at the facility. The activities you can do depend on the level of your school and the day and time."

    show intro tutorial 4
    dev "This version has a little extra that will be hidden behind an item in later versions, but keep an eye out for this icon in the top left corner and feel free to click on it."

    show intro tutorial 3
    dev "An activity usually lasts for one time unit."
    
    show intro tutorial 1
    dev "While we're at it. One day is seperated into 7 segments. Morning, Early Noon, Noon, Early Afternoon, Afternoon, Evening and Night."
    
    show intro tutorial 5
    dev "You can see the current date and time up here."
    
    show intro tutorial 6
    dev "And here you can skip to the next time segment."
    
    show intro tutorial 7
    dev "Here you can see your current stats."
    if loli_content > 0:
        dev "Remember that these statistics show the average of all schools. So if one school has 100 points and another has 0 points, this table would show a score of 50."
    dev "I'm not going to explain these stats. You can find a more detailed explanation of the stats in your journal."
    dev "The stats also have no effect on the game at the moment. This will change in future versions." ######## version dependend
    
    show intro tutorial 8
    dev "You can find the journal up here."    

    show intro tutorial 9
    dev "This is the journal. Here you will find all the information you need to manage your school."

    if loli_content > 0:
        show intro tutorial 10
        dev "Here you can switch between the schools."

    show intro tutorial 11
    dev "And here you can change the page."

    show intro tutorial 12
    dev "Here you can see the statistics for the current school."
    
    show intro tutorial 13
    dev "You can click on a stat to get more detailed information on the right hand side of the journal."

    show intro tutorial 14
    dev "The upper part is the description of the stat, divided into three parts."
    dev "The first part describes the level of the stat, the second part describes the stat itself and the last part describes how to increase the stat."

    show intro tutorial 15
    dev "The bottom part would normally be an image showing and representing the current stat level."
    dev "But I haven't made them yet. They will be added later." ######## version dependend

    show intro tutorial 16
    dev "Now we come to the Rules page in your journal. This is where you can manage your school rules."
    dev "It is very similar to the school overview page. On the left you have an overview of all the rules."
    dev "Rules may not be visible until certain conditions are met."
    dev "Rules highlighted in green are already unlocked and active."
    dev "Clicking on a rule will bring up a detail page on the right."

    show intro tutorial 17
    dev "The top part is again a description of the rule and the conditions for unlocking the rule."
    
    show intro tutorial 18
    dev "Below this is another image. You can click on the image to get a full screen view of it."
    dev "The images for some rules change as you progress through the game to better represent the effects behind the rule, according to the school's state."
    dev "So it may be worth revisiting some of the rules after you have upgraded a school. ;)"
    
    show intro tutorial 19
    dev "Next to the image you will see a small overview of the conditions that need to be fulfilled."
    dev "However, only conditions related to the school's statistics are shown here to give a clearer picture of the stats required."
    dev "The list in the description will always include all conditions."

    show intro tutorial 20
    dev "Here would be a button to queue this rule to be voted on by the Parent Teacher Association (PTA). But the PTA isn't implemented yet, so this will be added later."
    
    show intro tutorial 21
    dev "There is also the Clubs page. It is structured exactly the same as the rules page."

    show intro tutorial 22
    dev "The same applies to the Buildings page."
    if loli_content > 0:
        dev "The only difference is that the buildings page doesn't have the school tabs at the top, as the changes made here affect the whole campus."

    show intro tutorial 1
    dev "That's all. Thanks for listening. :D"

label .tutorial_3:

    hide screen black_error_screen_text

    dev "[intro_dev_message]"

    $ time.set_time(day = 2, month = 1, year = 2023, daytime = 1)

    jump map_overview

label first_week_epilogue:

    # first week epilogue 1
    secretary "Good Morning Mr. [principal_last_name]. Could you get a good picture of the situation in the school?"
    principal "Yes thank you! And please just call me [principal_first_name]. It's a bit akward to be called so formal."

    # first week epilogue 2
    secretary "Okay [principal_first_name]."
    principal "Good! Could you please call me a cab? I have to drive into town to prepare some things for my time at the school."
    secretary "I'll get right on it, but can I ask what you have planned?"
    principal "You can but I can't really answer that. Some of it is classified and the rest isn't secured yet."
    principal "If I'm successful, I'll let you know as soon as possible."

    # first week epilogue 3
    secretary "Okay, I'll go call your cab."
    principal "Thank you very much."
    
    call screen black_screen_text ("20 minutes later")

    # first week epilogue 4
    secretary "Izuku! Your cab just arrived!"
    principal "Perfect! I'll be off then. Expect me back early on Monday. I need all the time I can get."

    call screen black_screen_text ("Monday, 8 January 2023")

label .replay:

    show first week epilogue 5
    # principal enters with two boxes
    secretary "Good Morning, welcome back!"
    secretary "These 2 Boxes got delivered just an hour ago!"
    principal "Thank you very much!"

    show first week epilogue 6
    # both put boxes on desk
    secretary "Is this the stuff you had to prepare?"
    principal "Yes, at least some of it. Some things take a little more time to prepare."
    secretary "What is it?"
    principal "Here I'll show you."

    show first week epilogue 7
    # principal opens one box and reveals multiple bottles
    principal "This is a special energizer."
    secretary "Energizer?"
    
    show first week epilogue 8
    # principal takes one bottle
    principal "Yes, a close friend of mine is a biochemist and I asked him to put this stuff together."
    principal "He has helped me with my previous projects and he is truly a master alchemist."
    principal "This drink is a special blend to help students relax and concentrate. Weird, isn't it?"
    secretary "Does it really work?"
    principal "Sure I have full faith in my friends abilities, but you can try one if you want."

    show first week epilogue 9
    # principal gives the bottle to the secretary
    secretary "Can I drink it? Is it really safe?"
    principal "Absolutely, it is absolutely safe. In fact, it's really healthy. It is practically is a vitamin shake."
    principal "It's not a meal replacement, but it's packed with healthy vitamins and protein. It is also low in fat and sugar!"
    secretary "Oh wow, that sounds wonderful! I'd love to try one."

    show first week epilogue 10
    # secretary drinks potion
    secretary "Oh that's really tasty!"
    show first week epilogue 11
    secretary "And... Oh wow! The effect is almost immediate. I feel so much better! I don't feel any of the bad sleep I had last night!"
    secretary "Oh wow! That's amazing, I also feel much more focused. For example, I notice that sometimes you look at my breasts."
    principal "Oh... Ah... Ehm..."

    show first week epilogue 12
    # secretary laughs
    secretary "Haha! Don't worry about it! I know I have very big breasts."
    secretary "It's normal for people to stare at them. Do you want to see them?"
    principal "..."
    secretary "Don't be so shy. I know you want to!"

    show first week epilogue 13
    # secretary opens blouse
    secretary "Here! They're bigger than they look in those clothes, aren't they."

    show first week epilogue 14
    # secretary takes of bra
    secretary "Here, touch them! I'm really proud of them, they're nice and firm even though they're this big."

    show first week epilogue 15
    # principal touches/kneads breasts
    secretary "Yeah that's nice! Mhhh..."

    show first week epilogue 16
    # secretary touches principals crotch
    secretary "Ahh you seem to like them as well."
    secretary "Let me help you out."

    $ renpy.movie_cutscene("images/events/first week/first week epilogue 17.webm", -1, -1)
    # first week epilogue 17
    # secretary pulls out dick
    # secretary gives handjob

    $ renpy.movie_cutscene("images/events/first week/first week epilogue 18.webm", -1, -1)
    # first week epilogue 18
    # secretary gives titjob

    $ renpy.movie_cutscene("images/events/first week/first week epilogue 19.webm", -1, -1)
    # first week epilogue 19
    # secretary gives blowjob
    
    $ renpy.movie_cutscene("images/events/first week/first week epilogue 20.webm", 0, -1)
    # first week epilogue 20
    # cunningulus
    # secretary "Ah please give it to me!"

    $ renpy.movie_cutscene("images/events/first week/first week epilogue 21.webm", -1, -1)
    # first week epilogue 21
    # desk missionary

    $ renpy.movie_cutscene("images/events/first week/first week epilogue 22.webm", -1, -1)
    # first week epilogue 22
    # floor cowgirl

    $ renpy.movie_cutscene("images/events/first week/first week epilogue 23.webm", -1, -1)
    # first week epilogue 23
    # floor doggy

    $ renpy.movie_cutscene("images/events/first week/first week epilogue 24.webm", -1, 0)
    # first week epilogue 24
    # floor hardcore

    show first week epilogue 25
    principal_thought "Oh seems like I overdid it a little bit. But that was really hot. The effect of the potion lives up to my friend's promise."
    # secretary passes out

    show first week epilogue 26
    principal_thought "Let's get you to the couch."

    show first week epilogue 27
    # principal puts secretary on the couch
    principal_thought "Let's see how she feels after she rested. Gotta get her a blanket first though."

    $ renpy.end_replay()

    call screen black_screen_text ("Tuesday, 9 January 2023")

    show first week epilogue 28
    # principal enters office
    principal "Ahh she's already gone."

    show first week epilogue 29
    # principal approaches the boxes
    # principal starts handling boxes

    show first week epilogue 30
    # secretary enters office
    principal "Ah good morning! ohh..."

    show first week epilogue 31
    secretary "Good morning [principal_first_name]! What's wrong?"
    principal "Ehm, nice outfit!"

    show first week epilogue 32
    # secretary poses
    secretary "Oh yeah, do you like it? This morning I just felt like I would rather wear this than my old outfit."
    show first week epilogue 33
    principal "It fits you really well! So... about yesterday..."
    show first week epilogue 34
    secretary "Oh when we had sex? Yeah that was nice!"
    secretary "At first I was a little surprised because I would never behave like that, but strangely enough I didn't hate it."
    show first week epilogue 35
    secretary "It was as if my body was urging me to open up to the situation."
    secretary "And I am really glad that it happened. But is this another effect of the drink I had yesterday?"
    show first week epilogue 36
    principal "Well, I knew it would have a similar effect. I knew the consumer would open up and feel more free, but I didn't expect the effect to be this strong."
    principal "As I see, the effect is not as strong now as it was yesterday..."
    show first week epilogue 37
    secretary "Yes, you're right. Even though I feel freer, I don't feel so overwhelmed anymore."
    show first week epilogue 36
    principal "Mhh... It probably has to do with the change in your mindset. Yesterday it had to adjust to the new influx of emotions and feelings."
    principal "But now that your mind is used to the new way, it is calmer. It could also be the drink."
    principal "Perhaps it distributes itself the fastest in the libido so it overwhelms the other body mechanisms, and now it is more evenly distributed so you are more calm."
    show first week epilogue 37
    secretary "I can't really follow, but from what I can see, it works beautifully."
    show first week epilogue 36
    principal "It does, but there is one problem. As you can see, we only have three bottles left. My friend unfortunately had to fly to Brazil so he could only produce 4 bottles."
    show first week epilogue 38
    secretary "What? And you still gave me a full bottle?"
    show first week epilogue 36
    principal "That is no problem, I was planning to do that anyway."
    principal "He said the drink could be diluted down to a 100 drinks. Of course, the effect would be diminished, but it would still have an effect."
    principal "So I came up with the following plan. We will take a bottle, dilute it enough, and hand out one of these drinks to every student at recess today."
    principal "One thing I have observed at this school is how extremely prudish the students are. They don't just avoid the subject, they outright hate it."
    show first week epilogue 39
    secretary "Yeah, I always wondered about that..."
    show first week epilogue 36
    principal "So I guess one drink of the diluted potion should be enough to open these kids up to the subject."
    principal "After that it should be possible to influence them in more traditional ways in addition to the more exotic ways."
    show first week epilogue 37
    secretary "What do you mean by 'more exotic ways'?"
    show first week epilogue 36
    principal "Well, I planned to use methods like this potion and hypnosis."
    show first week epilogue 40
    secretary "Hypnosis?!"
    show first week epilogue 36
    principal "Yeah!"
    show first week epilogue 40
    secretary "Does that even work?"
    show first week epilogue 36
    principal "Oh yeah, it definitely works, but it takes a lot of preparation, so I couldn't prepare it over the weekend."
    principal "For it to work, the students must first be receptive to the subject and then they will be able to be influenced by hypnosis."
    principal "But the effects are quite weak so it needs to be set up correctly to provide a constant influence. But for that it will be very cost effective."
    principal "So for now we are going to work with basic influences, such as exposure to appropriate material in their free time and classes in a way that doesn't raise suspicion."
    show first week epilogue 37
    secretary "Sounds like you have a very thorough plan."
    show first week epilogue 36
    principal "Well, I have. I have been working towards my goal for most of my life, and that includes reforming various institutions."
    principal "So this school is just a stepping stone in my plan to reform the society."
    show first week epilogue 41
    secretary "And I'm happy to help you!"
    show first week epilogue 42
    principal "And for that I thank you very much!"
    show first week epilogue 41
    # principal slaps secretaries ass
    secretary "But what do you have planned for the remaining two potions."
    show first week epilogue 42
    principal "Oh yeah I plan to reopen the lab building and to add a private laboratory where I can work on reproducing the potion."
    principal "I got some instructions from my buddy, but I still have to work on it and these potions will help me."
    principal "Once I have a few prototypes, the process of changing the school should be much faster."
    principal "But first, let's work on diluting the first potion down for the students. It's getting late and we want to be ready for recess."
    show first week epilogue 35
    secretary "Yeah let's do it!"

    call screen black_screen_text ("Later at recess")

    show first week epilogue 43
    principal "Phew we just got it finished! Now we have to distribute it."
    show first week epilogue 44
    secretary "Ah I already organised something!"
    secretary "I asked the kiosk vendor to give one drink out for free for every order."
    secretary "Because it is the only place to get food here, it is garanteed that every student gets at least one drink."
    secretary "I also asked to make sure to only give out one per person."
    show first week epilogue 45
    principal "Perfect! I'm glad to have you as my secretary!"
    secretary "Well you already thanked me for that."
    show first week epilogue 46
    principal "Öhm... Did I? Ohhhh you mean that time!"
    secretary "Yeah that was really nice."
    principal "Alright then let's go eat something as well. I think we aren't needed here for now."
    secretary "Sounds good!"

    # principal and secretary take some food from kiosk and sit down among the students and start eating an conversing
    # while they eat, they notice the students get more fidgity

    # some students start to take off some clothes
    # other start groping their own breasts
    # others start kissing each other
    show first week epilogue 47
    subtitles_Empty ""
    show first week epilogue 48
    subtitles_Empty ""
    show first week epilogue 49
    subtitles_Empty ""
    show first week epilogue 50

    principal "Ah the potions seem to start taking effect."
    secretary "Yes! I guess school will be more fun now."

    # for the rest of the day the strong effects can be observed throughout the campus
    
    $ set_level_for_char(1, "high_school", charList["schools"])
    $ set_level_for_char(1, "middle_school", charList["schools"])
    $ set_level_for_char(1, "elementary_school", charList["schools"])
    $ set_level_for_char(1, "teacher", charList["staff"])
    $ set_level_for_char(5, "secretary", charList["staff"])

    $ set_all_buildings_blocked(False)

    $ set_building_blocked("kiosk")

    $ time.set_time(day = 9, daytime = 3)

    jump new_daytime

label first_week_epilogue_final:
    show screen black_error_screen_text ("")

    $ set_all_buildings_blocked(False)

    principal_thought "Well as far as I could see, the potion worked perfectly. Even though the potion was diluted, they initial start effect was still very strong."
    principal_thought "Now let's see how the students behave after the potion settled in."

    dev "This is where the content for this version ends. You can still roam around but there are no events for the different locations yet."
    dev "Thank you for playing up to this point. Look forward to the next version."
    dev "And feel free to visit my {a=https://patreon.com/suitji}Patreon{/a} and {a=https://discord.gg/UbHnxnRekA}Discord{/a}."
    dev "I'd be happy if you leave some feedback or some ideas on the Discord so I can work to further improve this game!"

    jump map_overview
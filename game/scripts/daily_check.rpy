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

    temp_check_events.add_event(Event("first_week_epilogue", "first_week_epilogue", 1,
        TimeCondition(day = 5, month = 1, year = 2023, daytime = 2)
    ))

    temp_check_events.add_event(Event("first_week_epilogue_final", "first_week_epilogue_final", 1,
        TimeCondition(day = 10, month = 1, year = 2023)
    ))

    temp_check_events.add_event(Event("weekly_assembly_first", "weekly_assembly_first", 2,
        TimeCondition(day = 1, month = 1, year = 2023, daytime = 1)
    ))

    temp_check_events.add_event(Event("weekly_assembly", "weekly_assembly", 2,
        TimeCondition(weekday = 1, daytime = 1)
    ))

    temp_check_events.add_event(Event("first_pta_meeting", "first_pta_meeting", 1,
        TimeCondition(day = 5, month = 1, year = 2023, daytime = 1)
    ))

    temp_check_events.add_event(Event("pta_meeting1", "pta_meeting", 2,
        TimeCondition(day = 5, daytime = 1)
    ))

    temp_check_events.add_event(Event("pta_meeting2", "pta_meeting", 2,
        TimeCondition(day = 19, daytime = 1)
    ))


label time_event_check:

    hide screen school_overview_map
    hide screen school_overview_stats
    hide screen school_overview_buttons
    
    call call_available_event(temp_time_check_events) from _call_call_available_event_16

label .after_temp_event_check:

    call call_available_event(temp_check_events) from _call_call_available_event_17

label .after_event_check:
    return

label first_week_epilogue:
    secretary "That was a nice introduction, Headmaster!"
    principal "Thank you! Just call me [principal_first_name]. It's a bit akward to be called so formal."
    secretary "Okay [principal_first_name]."
    principal "Good! Could you please call me a cab? I have to drive into town to prepare some things for my time at the school."
    secretary "I'll get right on it, but can I ask what you have planned?"
    principal "You can but I can't really answer that. Some of it is classified and the rest isn't secured yet."
    principal "If I'm successful, I'll let you know as soon as possible."
    secretary "Okay, I'll go call your cab."
    principal "Thank you very much."
    
    call screen black_screen_text ("20 minutes later")

    secretary "Izuku! Your cab just arrived!"
    principal "Perfect! I'll be off then. Expect me back early on Monday. I need all the time I can get."

    call screen black_screen_text ("Monday, 8 January 2023")

label .replay:

    # principal enters with to boxes
    secretary "Good Morning, welcome back!"
    secretary "Oh wow, you have a lot of boxes there! Let me help you!"

    # secretary takes top box
    principal "Thank you very much!"

    # both put boxes on desk
    secretary "Is this the stuff you had to prepare?"
    principal "Yes, at least some of it. Some things take a little more time to prepare."
    secretary "What is it?"
    principal "Here I'll show you."

    # principal opens one box and reveals multiple bottles
    principal "This is a special energizer."
    secretary "Energizer?"
    
    # principal takes one bottle
    principal "Yes, a close friend of mine is a biochemist and I asked him to put this stuff together."
    principal "He has helped me with my previous projects and he is truly a master alchemist."
    principal "This drink is a special blend to help students relax and concentrate. Weird, isn't it?"
    secretary "Does it really work?"
    principal "Sure I have full faith in my friends abilities, but you can try one if you want."

    # principal gives the bottle to the secretary
    secretary "Can I drink it? Is it really safe?"
    principal "Absolutely, it is absolutely safe. In fact, it's really healthy. It is practically is a vitamin shake."
    principal "It's not a meal replacement, but it's packed with healthy vitamins and protein. It is also low in fat and sugar!"
    secretary "Oh wow, that sounds wonderful! I'd love to try one."

    # secretary drinks potion
    secretary "Oh that's really tasty!"
    secretary "And... Oh wow! The effect is almost immediate. I feel so much better! I don't feel any of the bad sleep I had last night!"
    secretary "Oh wow! That's amazing, I also feel much more focused. For example, I notice that sometimes you look at my breasts."
    principal "Oh... Ah... Ehm..."

    # secretary laughs
    secretary "Haha! Don't worry about it! I know I have very big breasts."
    secretary "It's normal for people to stare at them. Do you want to see them?"
    principal "..."
    secretary "Don't be so shy. I know you want to!"

    # secretary opens blouse
    secretary "Here! They're bigger than they look in those clothes, aren't they."

    # secretary takes of bra
    secretary "Here, touch them! I'm really proud of them, they're nice and firm even though they're this big."

    # principal touches/kneads breasts
    secretary "Yeah that's nice! Mhhh..."

    # secretary touches principals crotch
    secretary "Ahh you seem to like them as well."
    secretary "Let me help you out."

    # secretary pulls out dick
    # secretary gives handjob
    # secretary gives blowjob
    
    # cunningulus
    secretary "Ah please give it to me!"

    # desk missionary
    # floor cowgirl
    # floor doggy
    # floor hardcore

    # secretary passes out

    principal_thought "Oh seems like I overdid it a little bit. But that was really hot. The effect of the potion lives up to my friend's promise."

    # principal puts secretary on the couch
    principal_thought "Let's see how she feels after she rested."

    # principal leaves

    $ renpy.end_replay()

    call screen black_screen_text ("Tuesday, 9 January 2023")

    # principal enters office
    principal "Ahh she's already gone."

    # principal approaches the boxes
    # principal starts handling boxes

    # secretary enters office
    principal "Ah good morning! ohh..."
    secretary "Good morning [principal_first_name]! What's wrong?"
    principal "Ehm, nice outfit!"

    # secretary poses
    secretary "Oh yeah, do you like it? This morning I just felt like I would rather wear this than my old outfit."
    principal "It fits you really well! So... about yesterday..."
    secretary "Oh when we had sex? Yeah that was nice!"
    secretary "At first I was a little surprised because I would never behave like that, but strangely enough I didn't hate it."
    secretary "It was as if my body was urging me to open up to the situation."
    secretary "And I am really glad that it happened. But is this another effect of the drink I had yesterday?"
    principal "Well, I knew it would have a similar effect. I knew the consumer would open up and feel more free, but I didn't expect the effect to be this strong."
    principal "As I see, the effect is not as strong now as it was yesterday..."
    secretary "Yes, you're right. Even though I feel freer, I don't feel so overwhelmed anymore."
    principal "Mhh... It probably has to do with the change in your mindset. Yesterday it had to adjust to the new influx of emotions and feelings."
    principal "But now that your mind is used to the new way, it is calmer. It could also be the drink."
    principal "Perhaps it distributes itself the fastest in the libido so it overwhelms the other body mechanisms, and now it is more evenly distributed so you are more calm."
    secretary "I can't really follow, but from what I can see, it works beautifully."
    principal "It does, but there is one problem. As you can see, we only have three bottles left. My friend unfortunately had to fly to Brazil so he could only produce 4 bottles."
    secretary "What? And you still gave me a full bottle?"
    principal "That is no problem, I was planning to do that anyway."
    principal "He said the drink could be diluted down to a 100 drinks. Of course, the effect would be diminished, but it would still have an effect."
    principal "So I came up with the following plan. We will take a bottle, dilute it enough, and hand out one of these drinks to every student at recess today."
    principal "One thing I have observed at this school is how extremely prudish the students are. They don't just avoid the subject, they outright hate it."
    secretary "Yeah, I always wondered about that..."
    principal "So I guess one drink of the diluted potion should be enough to open these kids up to the subject."
    principal "After that it should be possible to influence them in more traditional ways in addition to the more exotic ways."
    secretary "What do you mean by 'more exotic ways'?"
    principal "Well, I planned to use methods like this potion and hypnosis."
    secretary "Hypnosis?!"
    principal "Yeah!"
    secretary "Does that even work?"
    principal "Oh yeah, it definitely works, but it takes a lot of preparation, so I couldn't prepare it over the weekend."
    principal "For it to work, the students must first be receptive to the subject and then they will be able to be influenced by hypnosis."
    principal "But the effects are quite weak so it needs to be set up correctly to provide a constant influence. But for that it will be very cost effective."
    principal "So for now we are going to work with basic influences, such as exposure to appropriate material in their free time and classes in a way that doesn't raise suspicion."
    secretary "Sounds like you have a very thorough plan."
    principal "Well, I have. I have been working towards my goal for most of my life, and that includes reforming various institutions."
    principal "So this school is just a stepping stone in my plan to reform the society."
    secretary "And I'm happy to help you!"
    principal "And for that I thank you very much!"
    # principal slaps secretaries ass
    secretary "But what do you have planned for the remaining two potions."
    principal "Oh yeah I plan to reopen the lab building and to add a private laboratory where I can work on reproducing the potion."
    principal "I got some instructions from my buddy, but I still have to work on it and these potions will help me."
    principal "Once I have a few prototypes, the process of changing the school should be much faster."
    principal "But first, let's work on diluting the first potion down for the students. It's getting late and we want to be ready for recess."
    secretary "Yeah let's do it!"

    call screen black_screen_text ("Later at recess")

    principal "Phew we just got it finished! Now we have to distribute it."
    secretary "Ah I already organised something!"
    secretary "I asked the kiosk vendor to give one drink out for free for every order."
    secretary "Because it is the only place to get food here, it is garanteed that every student gets at least one drink."
    secretary "I also asked to make sure to only give out one per person."
    principal "Perfect! I'm glad to have you as my secretary!"
    secretary "Well you already thanked me for that."
    principal "Öhm... Did I? Ohhhh you mean that time!"
    secretary "Yeah that was really nice."
    principal "Alright then let's go eat something as well. I think we aren't needed here for now."
    secretary "Sounds good!"

    # principal and secretary take some food from kiosk and sit down among the students and start eating an conversing
    # while they eat, they notice the students get more fidgity

    # some students start to take off some clothes
    # other start groping their own breasts
    # others start kissing each other

    principal "Ah the potions seems to start taking effect."
    secretary "Yes! I guess school will be more fun now."

    # for the rest of the day the strong effects can be observed throughout the campus
    
    $ schools["high_school"].set_level(1)
    $ schools["middle_school"].set_level(1)
    $ schools["elementary_school"].set_level(1)

    $ set_all_buildings_blocked(False)

    $ set_building_blocked("kiosk")

    $ time.set_time(day = 9, daytime = 3)

    jump new_daytime

label first_week_epilogue_final:
    $ set_all_buildings_blocked(False)

    principal_thought "Now let's see how the students behave after the effects settled in."
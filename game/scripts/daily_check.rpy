init -1 python:
    set_current_mod('base')
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

    temp_time_check_events = TempEventStorage("temp_time_check_events", "misc", fallback = after_temp_event_check)
    time_check_events      = EventStorage("time_check_events", "misc", fallback = after_event_check)

    

init 1 python:
    set_current_mod('base')
    first_week_epilogue_event = Event(1, "first_week_epilogue", 
        IntroCondition(),
        TimeCondition(day = 5, month = 1, year = 2023, daytime = 2),
        thumbnail = "images/events/first week/first week epilogue 8.webp")

    first_week_epilogue_final_event = Event(1, "first_week_epilogue_final", 
        TimeCondition(day = 10, month = 1, year = 2023, daytime = 1),
        thumbnail = "images/events/first week/first week epilogue final 3.webp")

    first_pta_meeting_event = Event(1, "first_pta_meeting", 
        IntroCondition(),
        TimeCondition(day = 5, month = 1, year = 2023, daytime = 1),
        thumbnail = "images/events/pta/first meeting/first pta meeting 0 0.webp")

    pta_meeting_event = Event(2, "pta_meeting",
        TimeCondition(weekday = 5, daytime = 1))

    new_week_event = Event(2, "new_week",
        TimeCondition(weekday = 1, daytime = 1))

    end_of_month_event = Event(2, "end_of_month",
        TimeCondition(day = 1, daytime = 1))

    event_all_events_seen_event = Event(2,
        "event_all_events_seen",
        GameDataCondition("all_events_seen", True))

    event_reached_max_stats_event = Event(2,
        "event_reached_max_stats",
        StatCondition(inhibition = "90-", corruption = "5+"))

    intro_check_all_facilities_event = Event(2, "intro_check_all_facilities", 
        TimeCondition(day = 2, month = 1, year = 2023, daytime = 1))

    intro_check_all_first_potions_event = Event(2, "intro_check_all_first_potions", 
        TimeCondition(day = 9, month = 1, year = 2023, daytime = 4))

    game_over_happiness_event = Event(1, "game_over_happiness", 
        StatCondition(happiness = "0-"))

    game_over_education_event = Event(1, "game_over_education", 
        StatCondition(education = "0-"))

    game_over_reputation_event = Event(1, "game_over_reputation", 
        StatCondition(reputation = "0-"))

    aona_sports_bra_event_1_event = Event(1, "aona_sports_bra_event_1", 
        ProgressCondition("aona_sports_bra", 1),
        TimeCondition(daytime = 6),
        thumbnail = "images/events/misc/aona_sports_bra_event_1 # 23.webp")

    check_prof_event = Event(2, "check_missing_proficiencies",
        NOT(OR(
            ProficiencyCondition('math'), 
            ProficiencyCondition('history')
        ))
    )

    map_tutorial_event = Event(2, "map_tutorial", 
        NOT(ProgressCondition("map_tutorial")), 
        OR(IntroCondition(True), IntroCondition(False)),
        TutorialCondition(),
        override_intro = True, thumbnail = "images/events/misc/map_tutorial.webp")

    time_check_events.add_event(
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
        aona_sports_bra_event_1_event,
        map_tutorial_event
    )
        # check_prof_event,
    temp_time_check_events.add_event(
        event_all_events_seen_event, 
        event_reached_max_stats_event,
    )

    #############################################
    # DEBUG TEST EVENTS

    frag1 = FragmentStorage("TestFragStorage1")
    frag2 = FragmentStorage("TestFragStorage2")
    frag3 = FragmentStorage("TestFragStorage3")
    frag4 = FragmentStorage("TestFragStorage4")

    frag1.add_event(EventFragment(3, "test_event_frag_1",
        RandomListSelector("1_test", "1-1", "1-2", "1-3", "1-4", "1-5", "1-6", "1-7", "1-8", "1-9", "1-10"),
        RandomListSelector("1_test2", "1-1", "1-2", "1-3", "1-4", "1-5", "1-6", "1-7", "1-8", "1-9", "1-10")))
    frag1.add_event(EventFragment(3, "test_event_frag_1_1",
        RandomListSelector("1_1_test", "1.1-1", "1.1-2", "1.1-3", "1.1-4", "1.1-5", "1.1-6", "1.1-7", "1.1-8", "1.1-9", "1.1-10"),
        RandomListSelector("1_1_test2", "1.1-1", "1.1-2", "1.1-3", "1.1-4", "1.1-5", "1.1-6", "1.1-7", "1.1-8", "1.1-9", "1.1-10")))
    frag2.add_event(EventFragment(3, "test_event_frag_2",
        RandomListSelector("2_test", "2-1", "2-2", "2-3", "2-4", "2-5", "2-6", "2-7", "2-8", "2-9", "2-10"),
        RandomListSelector("2_test2", "2-1", "2-2", "2-3", "2-4", "2-5", "2-6", "2-7", "2-8", "2-9", "2-10")))
    frag2.add_event(EventFragment(3, "test_event_frag_2_1",
        RandomListSelector("2_1_test", "2.1-1", "2.1-2", "2.1-3", "2.1-4", "2.1-5", "2.1-6", "2.1-7", "2.1-8", "2.1-9", "2.1-10"),
        RandomListSelector("2_1_test2", "2.1-1", "2.1-2", "2.1-3", "2.1-4", "2.1-5", "2.1-6", "2.1-7", "2.1-8", "2.1-9", "2.1-10")))
    frag3.add_event(EventFragment(3, "test_event_frag_3",
        RandomListSelector("3_test", "3-1", "3-2", "3-3", "3-4", "3-5", "3-6", "3-7", "3-8", "3-9", "3-10"),
        RandomListSelector("3_test2", "3-1", "3-2", "3-3", "3-4", "3-5", "3-6", "3-7", "3-8", "3-9", "3-10")))
    frag3.add_event(EventFragment(3, "test_event_frag_3_1",
        RandomListSelector("3_1_test", "3.1-1", "3.1-2", "3.1-3", "3.1-4", "3.1-5", "3.1-6", "3.1-7", "3.1-8", "3.1-9", "3.1-10"),
        RandomListSelector("3_1_test2", "3.1-1", "3.1-2", "3.1-3", "3.1-4", "3.1-5", "3.1-6", "3.1-7", "3.1-8", "3.1-9", "3.1-10")))
    frag4.add_event(EventFragment(3, "test_event_frag_4",
        RandomListSelector("4_test", "4-1", "4-2", "4-3", "4-4", "4-5", "4-6", "4-7", "4-8", "4-9", "4-10"),
        RandomListSelector("4_test2", "4-1", "4-2", "4-3", "4-4", "4-5", "4-6", "4-7", "4-8", "4-9", "4-10")))

    test_event = EventComposite(0, "test_normal_test_event", [frag1, frag2, frag4],
        RandomListSelector("test", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"),
        RandomListSelector("test2", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"))
    #############################################

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

label .tutorial_3:

    hide screen black_error_screen_text

    if 'kwargs' not in locals() and 'kwargs' not in globals():
        $ kwargs = {}

    $ end_event('none', **kwargs)

    # jump first_week_epilogue_final.skip

    # dev "[intro_dev_message]"

    return

image anim_first_week_epilogue_17 = Movie(play ="images/events/first week/first week epilogue 17.webm", start_image = "images/events/first week/first week epilogue 17.webp", loop = True)
image anim_first_week_epilogue_18 = Movie(play ="images/events/first week/first week epilogue 18.webm", start_image = "images/events/first week/first week epilogue 18.webp", loop = True)
image anim_first_week_epilogue_19 = Movie(play ="images/events/first week/first week epilogue 19.webm", start_image = "images/events/first week/first week epilogue 19.webp", loop = True)
image anim_first_week_epilogue_20 = Movie(play ="images/events/first week/first week epilogue 20.webm", start_image = "images/events/first week/first week epilogue 20.webp", loop = True)
image anim_first_week_epilogue_21 = Movie(play ="images/events/first week/first week epilogue 21.webm", start_image = "images/events/first week/first week epilogue 21.webp", loop = True)
image anim_first_week_epilogue_22 = Movie(play ="images/events/first week/first week epilogue 22.webm", start_image = "images/events/first week/first week epilogue 22.webp", loop = True)
image anim_first_week_epilogue_23 = Movie(play ="images/events/first week/first week epilogue 23.webm", start_image = "images/events/first week/first week epilogue 23.webp", loop = True)
image anim_first_week_epilogue_24 = Movie(play ="images/events/first week/first week epilogue 24.webm", start_image = "images/events/first week/first week epilogue 24.webp", image = "images/events/first week/first week epilogue 24_1.webp", loop = False)

label first_week_epilogue (**kwargs):

    $ begin_event(**kwargs)

    $ hide_all()

    $ image = Image_Series("images/events/first week/first week epilogue <step>.webp")

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

    $ image.show(5)
    # headmaster enters with two boxes
    secretary "Good Morning, welcome back!"
    secretary "These 2 Boxes got delivered just an hour ago!"
    headmaster "Thank you very much!"

    $ image.show(6)
    # both put boxes on desk
    secretary "Is this the stuff you had to prepare?"
    headmaster "Yes, at least some of it. Some things take a little more time to prepare."
    secretary "What is it?"
    headmaster "Here I'll show you."

    $ image.show(7)
    # headmaster opens one box and reveals multiple bottles
    headmaster "This is a special energizer."
    secretary "Energizer?"
    
    $ image.show(8)
    # headmaster takes one bottle
    headmaster "Yes, a close friend of mine is a biochemist and I asked him to put this stuff together."
    headmaster "He has helped me with my previous projects and he is truly a master alchemist."
    headmaster "This drink is a special blend to help students relax and concentrate. Weird, isn't it?"
    secretary "Does it really work?"
    headmaster "Sure I have full faith in my friends abilities, but you can try one if you want."

    $ image.show(9)
    # headmaster gives the bottle to the secretary
    secretary "Can I drink it? Is it really safe?"
    headmaster "Absolutely, it is absolutely safe. In fact, it's really healthy. It is practically is a vitamin shake."
    headmaster "It's not a meal replacement, but it's packed with healthy vitamins and protein. It is also low in fat and sugar!"
    secretary "Oh wow, that sounds wonderful! I'd love to try one."

    $ image.show(10)
    # secretary drinks potion
    secretary "Oh that's really tasty!"
    $ image.show(11)
    secretary "And... Oh wow! The effect is almost immediate. I feel so much better! I don't feel any of the bad sleep I had last night!"
    secretary "Oh wow! That's amazing, I also feel much more focused. For example, I notice that sometimes you look at my breasts."
    headmaster "Oh... Ah... Ehm..."

    $ image.show(12)
    # secretary laughs
    secretary "Haha! Don't worry about it! I know I have very big breasts."
    secretary "It's normal for people to stare at them. Do you want to see them?"
    headmaster "..."
    secretary "Don't be so shy. I know you want to!"

    $ image.show(13)
    # secretary opens blouse
    secretary "Here! They're bigger than they look in those clothes, aren't they."

    $ image.show(14)
    # secretary takes of bra
    secretary "Here, touch them! I'm really proud of them, they're nice and firm even though they're this big."

    $ image.show(15)
    # headmaster touches/kneads breasts
    secretary "Yeah that's nice! Mhhh..."

    $ image.show(16)
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

    $ image.show(25)
    headmaster_thought "Oh seems like I overdid it a little bit. But that was really hot. The effect of the potion lives up to my friend's promise."
    # secretary passes out

    $ image.show(26)
    headmaster_thought "Let's get you to the couch."

    $ image.show(27)
    # headmaster puts secretary on the couch
    headmaster_thought "Let's see how she feels after she rested. Gotta get her a blanket first though."

    call screen black_screen_text ("Tuesday, 9 January 2023")

    $ image.show(28)
    # headmaster enters office
    headmaster "Ahh she's already gone."

    # headmaster approaches the boxes
    # headmaster starts handling boxes
    # secretary enters office
    call Image_Series.show_image(image, 29, 30) from _call_first_week_epilogue_1
    headmaster "Ah good morning! ohh..."

    $ image.show(31)
    secretary "Good morning [headmaster_first_name]! What's wrong?"
    headmaster "Ehm, nice outfit!"

    $ image.show(32)
    # secretary poses
    secretary "Oh yeah, do you like it? This morning I just felt like I would rather wear this than my old outfit."
    $ image.show(33)
    headmaster "It fits you really well! So... about yesterday..."
    $ image.show(34)
    secretary "Oh when we had sex? Yeah that was nice!"
    secretary "At first I was a little surprised because I would never behave like that, but strangely enough I didn't hate it."
    $ image.show(35)
    secretary "It was as if my body was urging me to open up to the situation."
    secretary "And I am really glad that it happened. But is this another effect of the drink I had yesterday?"
    $ image.show(36)
    headmaster "Well, I knew it would have a similar effect. I knew the consumer would open up and feel more free, but I didn't expect the effect to be this strong."
    headmaster "As I see, the effect is not as strong now as it was yesterday..."
    $ image.show(37)
    secretary "Yes, you're right. Even though I feel freer, I don't feel so overwhelmed anymore."
    $ image.show(36)
    headmaster "Mhh... It probably has to do with the change in your mindset. Yesterday it had to adjust to the new influx of emotions and feelings."
    headmaster "But now that your mind is used to the new way, it is calmer. It could also be the drink."
    headmaster "Perhaps it distributes itself the fastest in the libido so it overwhelms the other body mechanisms, and now it is more evenly distributed so you are more calm."
    $ image.show(37)
    secretary "I can't really follow, but from what I can see, it works beautifully."
    $ image.show(36)
    headmaster "It does, but there is one problem. As you can see, we only have three bottles left. My friend unfortunately had to fly to Brazil so he could only produce 4 bottles."
    $ image.show(38)
    secretary "What? And you still gave me a full bottle?"
    $ image.show(36)
    headmaster "That is no problem, I was planning to do that anyway."
    headmaster "He said the drink could be diluted down to a 100 drinks. Of course, the effect would be diminished, but it would still have an effect."
    headmaster "So I came up with the following plan. We will take a bottle, dilute it enough, and hand out one of these drinks to every student at recess today."
    headmaster "One thing I have observed at this school is how extremely prudish the students are. They don't just avoid the subject, they outright hate it."
    $ image.show(39)
    secretary "Yeah, I always wondered about that..."
    $ image.show(36)
    headmaster "So I guess one drink of the diluted potion should be enough to open these kids up to the subject."
    headmaster "After that it should be possible to influence them in more traditional ways in addition to the more exotic ways."
    $ image.show(37)
    secretary "What do you mean by 'more exotic ways'?"
    $ image.show(36)
    headmaster "Well, I planned to use methods like this potion and hypnosis."
    $ image.show(40)
    secretary "Hypnosis?!"
    $ image.show(36)
    headmaster "Yeah!"
    $ image.show(40)
    secretary "Does that even work?"
    $ image.show(36)
    headmaster "Oh yeah, it definitely works, but it takes a lot of preparation, so I couldn't prepare it over the weekend."
    headmaster "For it to work, the students must first be receptive to the subject and then they will be able to be influenced by hypnosis."
    headmaster "But the effects are quite weak so it needs to be set up correctly to provide a constant influence. But for that it will be very cost effective."
    headmaster "So for now we are going to work with basic influences, such as exposure to appropriate material in their free time and classes in a way that doesn't raise suspicion."
    $ image.show(37)
    secretary "Sounds like you have a very thorough plan."
    $ image.show(36)
    headmaster "Well, I have. I have been working towards my goal for most of my life, and that includes reforming various institutions."
    headmaster "So this school is just a stepping stone in my plan to reform the society."
    $ image.show(41)
    secretary "And I'm happy to help you!"
    $ image.show(42)
    headmaster "And for that I thank you very much!"
    $ image.show(41)
    # headmaster slaps secretaries ass
    secretary "But what do you have planned for the remaining two potions."
    $ image.show(42)
    headmaster "Oh yeah I plan to reopen the lab building and to add a private laboratory where I can work on reproducing the potion."
    headmaster "I got some instructions from my buddy, but I still have to work on it and these potions will help me."
    headmaster "Once I have a few prototypes, the process of changing the school should be much faster."
    headmaster "Recreating the potions will probably be quite a task. I'm sure the first iterations will have a much weaker effect, if any effect at all."
    headmaster "But first, let's work on diluting the first potion down for the students. It's getting late and we want to be ready for recess."
    $ image.show(35)
    secretary "Yeah let's do it!"

    call screen black_screen_text ("Later at recess")

    $ image.show(43)
    headmaster "Phew we just got it finished! Now we have to distribute it."
    $ image.show(44)
    secretary "Ah I already organised something!"
    secretary "I asked the kiosk vendor to give one drink out for free for every order."
    secretary "Because it is the only place to get food here, it is guaranteed that every student gets at least one drink."
    secretary "I also asked to make sure to only give out one per person."
    $ image.show(45)
    headmaster "Perfect! I'm glad to have you as my secretary!"
    secretary "Well you already thanked me for that."
    $ image.show(46)
    headmaster "Öhm... Did I? Ohhhh you mean that time!"
    secretary "Yeah that was really nice."
    headmaster "Alright then let's go eat something as well. I think we aren't needed here for now."
    secretary "Sounds good!"

    # headmaster and secretary take some food from kiosk and sit down among the students and start eating an conversing
    # while they eat, they notice the students get more fidgety

    # some students start to take off some clothes
    # other start groping their own breasts
    # others start kissing each other
    call Image_Series.show_image(image, 47, 48, 49, 50) from _call_first_week_epilogue_2

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

    $ image = Image_Series("/images/events/first week/first week epilogue final <step>.webp", step_start = 1, **kwargs)

    hide screen black_screen_text

    $ image.show(1)
    # show first week epilogue final 1 with dissolveM
    # headmaster enters campus
    headmaster_thought "Oh hello! The effects seem to have diminished quite a lot."
    $ image.show(2)
    headmaster_thought "I guess the potion seems to have fully settled in their systems and their bodies to have adjusted to the new influx of hormones."
    $ image.show(3)
    headmaster_thought "But I guess that's a good thing. It would be bad if they were constantly horny without adapting to the change."

    # headmaster approaches student
    $ image.show(4)
    headmaster "Oh hello! How are you doing?"
    sgirl "Oh hello Mr. [headmaster_last_name]! I'm doing great! I kinda feel a bit more relaxed than yesterday! I think..." (name='Miwa Igarashi')
    $ image.show(5)
    headmaster "Oh that's good to hear! But what do you mean with you think? Is everything really alright?"
    $ image.show(6)
    sgirl "Oh yeah, yeah! Everything is fine, it's just, I have the feeling there is a gap in my memory. I can't remember anything from yesterday after recess."  (name='Miwa Igarashi')
    $ image.show(7)
    sgirl "I only know to have been extremely happy and relaxed yesterday, but I can't remember anything else." (name='Miwa Igarashi')
    $ image.show(8)
    headmaster "Hmm interesting... Well at least you are feeling fine. Pay the nurse a visit if you start to feel unwell."
    sgirl "Okay, I will! Thank you Mr. [headmaster_last_name]!" (name='Miwa Igarashi')

    # school girl walks off, headmaster stays a little bit in thoughts
    $ image.show(9)
    headmaster_thought "Hmm... that's an interesting effect. She doesn't remember anything that happened yesterday, but the long term effect seems to still be in place."
    $ image.show(10)
    headmaster_thought "[secretary_name] didn't seem to have any memory gaps whatsoever. I wonder if it has to do with the fact that the students go a diluted version."

    # secretary approaches from behind
    $ image.show(11)
    secretary "Oh hello [headmaster_first_name]! How are you doing?"
    headmaster "Oh hello [secretary_name]! I'm doing fine. I was just talking to one of the students."
    headmaster "She said she can't remember anything from yesterday after recess. Do you have any idea how this could have come about?"
    headmaster "I mean you didn't have this problem, did you?"
    $ image.show(13)
    secretary "No I don't think so."
    $ image.show(14)
    headmaster "I think it had to do with the fact that the students were given a diluted version of the potion."
    headmaster "My mate was explaining to me a bit about its effects and mechanics. I couldn't quite follow, but I think he said something about using certain proteins to help the brain cope with the large influx of emotions during the acclimatisation phase."
    headmaster "Maybe the diluted version doesn't have enough of those proteins to help the brain deal with the emotions. I mean, my mate said that if you dilute the potion by 1 to 100, the effects don't diminish that much."
    headmaster "So I think the balance was upset and the students experienced something like a blackout, where the brain just stops storing memories."
    $ image.show(15)
    secretary "Well, at least the side effects weren't more serious."
    $ image.show(16)
    headmaster "When I think about it, it might have been a good thing."
    $ image.show(15)
    secretary "What do you mean?"
    $ image.show(16)
    headmaster "I have noticed that the students are almost back to their old selves. They are more relaxed and not so stuck up, and they already seem to have modified their uniforms, but the actual long term effect seems rather minimal compared to the effect it had on you."
    headmaster "I can't imagine how the students would react in their current state if they could remember everything that happened yesterday."
    $ image.show(15)
    secretary "Oh yes, you're right. That would have been a disaster."
    $ image.show(16)
    headmaster "Well, that's good to know, but until we get the lab back up and running there's nothing we can really do about it."
    headmaster "I need to reproduce the potion first. I'm not sure I can do it the way my buddy did it."
    $ image.show(15)
    headmaster "The first iterations are likely to have a much weaker effect, if any."
    secretary "I guess we'll see when the time comes."
    $ image.show(17)
    headmaster "Oh I guess classes just started. I think I should start my rounds."
    $ image.show(18)
    secretary "Good luck."

    $ end_event('none', **kwargs)

label .skip:

    hide screen black_error_screen_text

    call show_image ("images/events/endscreen/thanks 1.webp") from _call_show_image_first_week_epilogue_final_3
    
    # dev "[intro_dev_message]"

    dev "This is where the actual free roaming begins."
    dev "Please keep in mind, that this game is still an early version and thus has a limited amount of events and potential bugs."
    dev "Also try to revisit some events as some have different variants that change randomly."
    call show_image ("images/events/endscreen/thanks 2.webp") from _call_show_image_first_week_epilogue_final_4
    dev "I hope you'll still enjoy the game."
    dev "To stay up to date on development visit my {a=[patreon]}Patreon{/a} and {a=[discord]}Discord{/a}."
    dev "I'd be happy if you leave some feedback or some ideas on the Discord so I can work to further improve this game!"

    jump map_overview

label check_missing_proficiencies:
    # $ begin_event(no_gallery = True, **kwargs)

    $ hide_all()

    if get_headmaster_proficiency_level('pe') == 0:
        $ set_headmaster_proficiency_level('pe', 100)

    $ call_custom_menu_with_text("The headmaster has no proficiencies set. Please assign a proficiency to the headmaster.\nP.E. is pre-selected due to his backstory.", character.subtitles, False, 
        ('Math', SetProficiencyEffect('math', level = 1), "math" not in headmaster_proficiencies.keys()),
        ('History', SetProficiencyEffect('history', level = 1), "history" not in headmaster_proficiencies.keys()), 
    override_menu_exit = "map_overview")
        

##################################
# ----- Daily Check Events ----- #
##################################

label new_week (**kwargs):
    call change_money_with_modifier(0, 'payroll_weekly') from _call_change_money_with_modifier_1
    return

label end_of_month (**kwargs):
    call change_money_with_modifier(0, 'payroll_monthly') from _call_change_money_with_modifier_2
    # $ change_stat(MONEY, 1000)

    return

label aona_sports_bra_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ inhibition = get_stat_value('inhibition', [90, 95, 100], **kwargs)

    $ image = Image_Series("images/events/misc/aona_sports_bra_event_1 <secretary_level> <step>.webp", ['secretary_level'], **kwargs)

    $ store_clerk = Character("Store Clerk", kind = character.vendor)

    $ image.show(0)
    subtitles "*Knock* *Knock*"
    $ image.show(1)
    headmaster "Come in!"
    $ image.show(2)
    secretary "Excuse me Mr. [headmaster_last_name], Mrs. Komuro is here to see you."
    $ image.show(3)
    headmaster "Ah yes, thank you! I'll come out!"
    call Image_Series.show_image(image, 4, 5) from image_aona_sports_bra_event_1_1
    headmaster "Mrs. Langley, I'll be out with Mrs. Komuro for a few hours."
    $ image.show(6)
    secretary "Okay, can I ask what you have planned?"
    $ image.show(7)
    headmaster "Mrs. Komuro unfortunately is missing a sports bra and I'm going to take her get one in the next city."
    $ image.show(8)
    headmaster "She struggles a bit during sports lessons and I want to help her out."
    # secretary looks up and down on Aona
    $ image.show(9)
    secretary "Oh yeah, I see what you mean. She is quite big."
    # Aona blushes
    $ image.show(10)
    headmaster "Yes, she is. I'll be back in a few hours."
    # scene change to inside the car
    call Image_Series.show_image(image, 11, 12, 13) from image_aona_sports_bra_event_1_2
    headmaster "So Aona, how are you doing?"
    $ image.show(14)
    sgirl "I'm doing fine Mr. [headmaster_last_name]." (name='Aona Komuro')
    $ image.show(15)
    headmaster "I'm glad to hear that. I'm sorry that I didn't notice earlier that you were struggling."
    $ image.show(16)
    sgirl "I don't really talk about it. I'm a bit embarrassed about it." (name = "Aona Komuro")
    $ image.show(17)
    headmaster "I understand. But you don't have to be embarrassed. It's a natural thing."
    $ image.show(18)
    sgirl "The other girls are sometimes a bit jealous of me because of my breasts." (name = "Aona Komuro")
    $ image.show(19)
    sgirl "But I hate my breasts. They're too big and I can't do anything about it." (name = "Aona Komuro")
    $ image.show(20)
    headmaster "I understand. I'm sure you have other struggles because of them, don't you?"
    $ image.show(21)
    sgirl "Yes, the worst thing is the constant back pain. I can't even sit properly in class." (name = "Aona Komuro")
    $ image.show(22)
    headmaster "Oh that is no good. A healthy back is important for your general health."
    $ image.show(23)
    headmaster "Ah look. We've arrived. Let's head in."
    
    call Image_Series.show_image(image, 24, 25) from image_aona_sports_bra_event_1_3
    store_clerk "Hello! How can I help you?"
    # scene change to inside the store
    $ image.show(26)
    headmaster "Hello! I'm looking for a sports bra for this young lady."
    $ image.show(25)
    store_clerk "Sure I can help you with that."
    # clerk looks at Aona
    call Image_Series.show_image(image, 27, 28, 29) from image_aona_sports_bra_event_1_4
    store_clerk "Alright. I'll show you some options."
    # they walk to the sports bra section
    $ image.show(30)
    store_clerk "Let's see what we have here."
    $ image.show(31)
    store_clerk "How about this one?"
    $ image.show(32)
    sgirl "That looks good. Can I try it on?" (name = "Aona Komuro")
    $ image.show(33)
    store_clerk "Of course! The changing rooms are over there."
    $ image.show(33)
    # aona goes into the changing room
    $ image.show(34)
    store_clerk "If you need more help, just call me."
    sgirl "Will do!" (name = "Aona Komuro")

    $ call_custom_menu(False,
        ("Wait", "aona_sports_bra_event_1.wait_1"),
        ("Look for a bra for yourself", "aona_sports_bra_event_1.bra_for_self"),
        ("Peek into the changing room", "aona_sports_bra_event_1.peek_1"),
    **kwargs)
label .bra_for_self (**kwargs):

    $ image.show(35)
    headmaster "Hmm, what kind of bras do they have here?"
    $ image.show(36)
    headmaster "Oh that one looks interesting. Maybe I'll get her to pick that one."
    $ kwargs['bra_for_self'] = True

    call .wait_1 (**kwargs) from _call_aona_sports_bra_event_1_wait_1
label .peek_1 (**kwargs):

    $ image.show(37)
    headmaster_thought "Maybe I can sneak a look."
    # looks from neighbouring cabin in from top
    call Image_Series.show_image(image, 37, 38, 39, 40, 41, 42, 43, 44) from image_aona_sports_bra_event_1_5
    headmaster_thought "Nice."
    call Image_Series.show_image(image, 45, 46, 47, 48, 49, 50, 51) from image_aona_sports_bra_event_1_6
    headmaster_thought "Better get back now..."
    
    call .wait_1 (**kwargs) from _call_aona_sports_bra_event_1_wait_1_1
label .wait_1 (**kwargs):

    $ bra = get_kwargs('bra_for_self', False, **kwargs)

    call Image_Series.show_image(image, 52, 53, 54) from image_aona_sports_bra_event_1_7
    sgirl "This one fits quite well. I would like to take it." (name = "Aona Komuro")

    $ call_custom_menu(False,
        ("Buy bra", "aona_sports_bra_event_1.buy_bra"),
        ("Ask to try on your pick", "aona_sports_bra_event_1.try_alt_bra", bra),
    **kwargs)
label .try_alt_bra (**kwargs):

    $ image.show(55)
    headmaster "I found this one, I think that would be a good choice."
    sgirl "Sure, I'll try it out." (name = "Aona Komuro")

    $ call_custom_menu(False,
        ("Peek", "aona_sports_bra_event_1.peek_2"),
        ("Wait", "aona_sports_bra_event_1.wait_2"),
    **kwargs)
label .peek_2 (**kwargs):
    
    $ image.show(56)
    headmaster_thought "I'll take a look."
    # looks from neighbouring cabin in from top
    call Image_Series.show_image(image, 57, 58, 59, 60, 61, 62) from image_aona_sports_bra_event_1_8
    headmaster_thought "Nice."
    
    call .wait_2 (**kwargs) from _call_aona_sports_bra_event_1_wait_2
label .wait_2 (**kwargs):

    $ image.show(63)
    sgirl "Uhm sir? I think this one is a bit too skimpy for me." (name = "Aona Komuro")
    sgirl "I don't think I can wear that." (name = "Aona Komuro")
    $ image.show(64)
    headmaster "Do you care to show what you mean?"
    if inhibition >= 96:
        sgirl "Sorry, but I wouldn't feel comfortable doing that." (name = "Aona Komuro")
        $ image.show(65)
        headmaster "I understand. I'll take it back then."
        headmaster "Could you give me the other bra then? I'll quickly go pay for it."
        call .sneak_bra (**kwargs) from _call_aona_sports_bra_event_1_sneak_bra
    else:
        sgirl "Uhm, okay..." (name = "Aona Komuro")
        # aona steps out of the cabin
        $ image.show(66)
        headmaster "Oh, I see what you mean. But I think it suits you very well."
        $ image.show(67)
        headmaster "I mean it has a good support and has great ventilation, especially good for running."
        $ image.show(68)
        headmaster "Also, if I am allowed to say so, it looks very good on you and sure would provide a good boost in self confidence."
        if inhibition >= 91:
            $ image.show(69)
            sgirl "I understand, but I don't feel comfortable with it." (name = "Aona Komuro")
            $ image.show(70)
            headmaster "I understand. I'll take it back then."
            headmaster "Could you give me the other bra then? I'll quickly go pay for it."
            call .sneak_bra (**kwargs) from _call_aona_sports_bra_event_1_sneak_bra_1
        else:
            $ image.show(71)
            sgirl "Oh thank you for saying that, I guess I could take it." (name = "Aona Komuro")
            $ image.show(72)
            headmaster "Wonderful, let's take it then."
            $ kwargs["skimpy_bra"] = True
    
    call .buy_bra (**kwargs) from _call_aona_sports_bra_event_1_buy_bra
label .sneak_bra (**kwargs):

    $ log_val('character', character.subtitles)

    $ call_custom_menu_with_text("Do you want to swap the bra with the skimpy variant?", character.subtitles, False,
        ("Swap", "aona_sports_bra_event_1.sneak_bra_true"),
        ("Don't swap", "aona_sports_bra_event_1.sneak_buy_bra"),
    **kwargs)
label .sneak_bra_true (**kwargs):
    $ kwargs["skimpy_bra"] = True
    $ kwargs["volunteered"] = False
    call .buy_bra (**kwargs) from _call_aona_sports_bra_event_1_buy_bra_1
label .buy_bra (**kwargs):

    $ image.show(73)
    headmaster "I'll quickly go pay for it."
    $ image.show(74)
    # headmaster goes to the cashier
    headmaster "Okay! I would like to buy this bras. For my student over there."
    $ image.show(75)
    store_clerk "Sure, that will be 100 then."
    $ image.show(76)
    headmaster "Sure, here you go!"
    $ image.show(77)
    store_clerk "Thank you very much!"
    # headmaster goes back to Aona
    $ image.show(78)
    headmaster "Alright that is done. Let's go back to the school."
    $ image.show(79)
    sgirl "Thank you very much Mr. [headmaster_last_name]!" (name = "Aona Komuro")
    $ image.show(80)
    headmaster "You're welcome. I'm glad I could help you out."
    # back in car
    call Image_Series.show_image(image, 81, 82) from image_aona_sports_bra_event_1_9
    headmaster "You know, I had a thought about your back problems."
    $ image.show(83)
    headmaster "Have you tried massages or physiotherapy?"
    $ image.show(84)
    sgirl "Not really, I'm a bit embarrassed about it and my health insurance doesn't cover that." (name = "Aona Komuro")
    $ image.show(85)
    headmaster "I see... You know, in my studies about the human physiology I learned a lot about the human body."
    $ image.show(86)
    headmaster "Which also includes the back and how to treat it."
    $ image.show(85)
    headmaster "Sooo... if you'd like, I could give you a hand with your back pain."
    $ image.show(87)
    sgirl "Oh, I don't know..." (name = "Aona Komuro")
    $ image.show(88)
    headmaster "Don't worry, I'm a professional. I know what I'm doing."
    $ image.show(87)
    sgirl "Yeah, but I don't think that would be good. I wouldn't feel comfortable with that." (name = "Aona Komuro")
    $ image.show(88)
    headmaster "I understand. But if you ever change your mind, just let me know."
    $ image.show(87)
    sgirl "I'll think about it!" (name = "Aona Komuro")
    $ image.show(89)
    subtitles "The rest of the drive, Aona and the headmaster talked about different things concerning her back issues and her breasts."
    # Back at the school
    $ image.show(90)
    headmaster "Alright, we're back. I hope the bra will help you out."
    $ image.show(91)
    sgirl "Thank you very much Mr. [headmaster_last_name]!" (name = "Aona Komuro")
    $ image.show(90)
    headmaster "You're welcome. Have a good night! Don't stay up for too long, it's quite late already."
    $ image.show(91)
    sgirl "Yes, I will! Good night!" (name = "Aona Komuro")
    $ image.show(90)
    headmaster "Good night, see you at the next P.E. lesson."
    $ image.show(92)
    headmaster_thought "I hope that bra will help her out. She really needs it."
    $ image.show(93)
    headmaster_thought "But during that drive, it seems the girls are still missing some crucial information about their own bodies."
    call Image_Series.show_image(image, 94, 95) from image_aona_sports_bra_event_1_10
    headmaster_thought "I mean how conservative have the teacher here been? That's just unacceptable."

    $ bra = 0

    if get_kwargs('skimpy_bra', False, **kwargs):
        $ bra = 1
        if get_kwargs('volunteered', False, **kwargs):
            $ bra = 2

    $ set_game_data("aona_skimpy_sports_bra", bra)

    $ advance_progress("aona_sports_bra")

    $ change_stat(MONEY, -200)

    call change_stats_with_modifier('school',
        happiness = MEDIUM, charm = TINY, reputation = MEDIUM, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_84

    $ end_event('new_daytime', **kwargs)
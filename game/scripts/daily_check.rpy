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
        Pattern("main", "images/events/first week/first week epilogue <step>.webp"),
        thumbnail = "images/events/first week/first week epilogue 8.webp")

    first_week_epilogue_final_event = Event(1, "first_week_epilogue_final", 
        TimeCondition(day = 10, month = 1, year = 2023, daytime = 1),
        Pattern("main", "/images/events/first week/first week epilogue final <step>.webp"),
        thumbnail = "images/events/first week/first week epilogue final 3.webp")

    first_pta_meeting_event = Event(1, "first_pta_meeting", 
        IntroCondition(),
        TimeCondition(day = 5, month = 1, year = 2023, daytime = 1),
        thumbnail = "images/events/pta/first meeting/first pta meeting 0 0.webp")

    new_week_event = Event(2, "new_week",
        TimeCondition(weekday = 1, daytime = 1))

    end_of_month_event = Event(2, "end_of_month",
        TimeCondition(day = 1, daytime = 1))

    intro_check_all_facilities_event = Event(2, "intro_check_all_facilities", 
        IntroCondition(),
        TimeCondition(day = 2, month = 1, year = 2023, daytime = 1))

    intro_check_all_first_potions_event = Event(2, "intro_check_all_first_potions", 
        IntroCondition(),
        TimeCondition(day = 9, month = 1, year = 2023, daytime = 4))

    game_over_happiness_event = Event(1, "game_over_happiness", 
        StatCondition(happiness = "0-"))

    game_over_education_event = Event(1, "game_over_education", 
        StatCondition(education = "0-"))

    game_over_reputation_event = Event(1, "game_over_reputation", 
        StatCondition(reputation = "0-"))

    check_prof_event = Event(2, "check_missing_proficiencies",
        NOT(IntroCondition(True)),
        NOT(OR(
            ProficiencyCondition('math'), 
            ProficiencyCondition('history')
        )))

    time_check_events.add_event(
        first_week_epilogue_event, 
        first_week_epilogue_final_event, 
        first_pta_meeting_event,  
        new_week_event,
        end_of_month_event,
        intro_check_all_facilities_event,
        intro_check_all_first_potions_event,
        game_over_happiness_event,
        game_over_education_event,
        game_over_reputation_event,
    )
    
    #############################################
    # DEBUG TEST EVENTS
    #############################################

############################
# region Daily Check ----- #
############################

label time_event_check ():
    hide screen school_overview_map
    hide screen school_overview_stats
    hide screen school_overview_buttons

    call call_available_event(temp_time_check_events, 0, True, with_removal = True) from time_event_check_1

label .after_temp_event_check (**kwargs):

    call call_available_event(time_check_events, 0, True) from time_event_check_2

label .after_event_check (**kwargs):
    return

# endregion
############################

#############################
# region Intro Events ----- #
#############################

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

    scene school_map

    headmaster_thought "Okay time to check all the facilities and see if they need improvement."
    headmaster_thought "I should try to inspect all the locations until friday where I will have my first PTA meeting."
    headmaster_thought "Hmm, I will probably not be able to check all facilities until then. Better decide which ones are the most important."
    subtitles "You get different stat bonuses depending on which locations you decide to visit until friday."

    jump map_overview

label intro_check_all_first_potions (**kwargs):
    $ begin_event()

    scene school_map

    headmaster_thought "By this time all the students should have eaten."
    headmaster_thought "Time to go around campus and check on the students and the potion's effect."
    headmaster_thought "The immediate effect will probably only last for today, so better decide which locations to visit."

    jump map_overview

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

    $ image = convert_pattern("main", **kwargs)

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

    $ image = convert_pattern("main", step_start = 1, **kwargs)

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
        MenuElement("Math", SetProficiencyEffect('math', level = 1), "math" not in headmaster_proficiencies.keys()),
        MenuElement("History", SetProficiencyEffect('history', level = 1), "history" not in headmaster_proficiencies.keys()), 
    override_menu_exit = "map_overview")

# endregion
#############################

###################################
# region Daily Check Events ----- #
###################################

label new_week (**kwargs):
    call change_money_with_modifier(0, 'payroll_weekly') from _call_change_money_with_modifier_1
    return

label end_of_month (**kwargs):
    call change_money_with_modifier(0, 'payroll_monthly') from _call_change_money_with_modifier_2
    # $ change_stat(MONEY, 1000)

    return

# endregion
###################################
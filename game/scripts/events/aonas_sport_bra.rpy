init 2 python: 
    set_current_mod('base')

    gym_teach_pe_intro_storage.add_event(
        EventFragment(1, "gym_teach_pe_intro_aona_bra",
            ProgressCondition("aona_sports_bra", 2),
            GameDataSelector("skimpy_bra", "aona_skimpy_sports_bra", "False"),
            Pattern("main", "/images/events/gym/gym_teach_pe_intro_aona_bra/gym_teach_pe_intro_aona_bra <skimpy> <step>.webp", 'skimpy')),
    )

    gym_teach_pe_main_storage.add_event(
        EventFragment(3, "gym_teach_pe_main_aona_bra",
            NOT(ProgressCondition("aona_sports_bra")),
            MoneyCondition(200),
            ProgressCondition("first_class", 3),
            Pattern("main", "/images/events/gym/gym_teach_pe_main_aona_bra/gym_teach_pe_main_aona_bra <step>.webp")),
        EventFragment(1, "gym_teach_pe_main_aona_bra_2",
            ProgressCondition("aona_sports_bra", 2),
            GameDataSelector("skimpy_bra", "aona_skimpy_sports_bra"),
            Pattern("main", "/images/events/gym/gym_teach_pe_main_aona_bra_2/gym_teach_pe_main_aona_bra_2 <step>.webp")),
    )

    time_check_events.add_event(
        Event(1, "aona_sports_bra_event_1", 
            ProgressCondition("aona_sports_bra", 1),
            TimeCondition(daytime = 6),
            Pattern("main", "images/events/misc/aona_sports_bra_event_1/aona_sports_bra_event_1 <secretary_level> <step>.webp", 'secretary_level'),
            thumbnail = "images/events/misc/aona_sports_bra_event_1/aona_sports_bra_event_1 # 23.webp"),
    )

label gym_teach_pe_intro_aona_bra (**kwargs):
    $ begin_event(**kwargs)

    $ bra = get_value('skimpy_bra', **kwargs)
    $ skimpy = bra != 0

    $ kwargs = load_kwargs_values(kwargs, skimpy = str(skimpy))
    $ image = convert_pattern("main", skimpy = skimpy, **kwargs)

    $ miwa = get_person("class_3a", "miwa_igarashi").get_character()
    $ aona = get_person("class_3a", "aona_komuro").get_character()

    $ image.show(0)
    miwa "And the headmaster really took you to the city to buy a sports bra?"
    $ image.show(1)
    aona "Yes, he did. He said it was important for my health and performance."
    $ image.show(2)
    aona "It's great that he cares so much about us."
    $ image.show(3)
    miwa "Yes, I didn't think he would be that nice."
    $ image.show(4)
    aona "Didn't you talk to him as well?"
    $ image.show(5)
    miwa "Yeah you're right. He was very empathetic."

    # Aona puts on the bra
    call Image_Series.show_image(image, 6, 7, 8, 9) from image_gym_teach_pe_intro_aona_bra_1
    aona "What do you think?"
    if bra >= 1:
        $ image.show(10)
        miwa "It's a bit skimpy, isn't it?"
        if bra == 2:
            $ image.show(24)
            aona "Yeah, but I think it is quite comfortable and Mr. [headmaster_last_name] said it was good for my health."
            $ image.show(25)
            miwa "I guess you're right. I mean it really does look good on you."
            $ image.show(26)
            aona "Thank you."

            call change_stats_with_modifier('pe',
                happiness = SMALL, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_17
        else:
            $ image.show(12)
            aona "Yeah unfortunately, the headmaster bought the wrong one!"
            $ image.show(13)
            miwa "What do you mean?"
            $ image.show(14)
            aona "He showed me another one to the one I wanted to buy, saying it would be good for my health, but I said I didn't like it."
            $ image.show(15)
            miwa "Quite perverted by him, isn't it?"
            $ image.show(16)
            aona "I don't know, but I think it's quite comfortable."
            $ image.show(17)
            aona "Maybe it was a genuine mistake."
            $ image.show(18)
            miwa "What do you do now?"
            $ image.show(19)
            aona "I don't know. I guess I have to wear it now. I don't want to have to run with these giant things again."
            $ image.show(20)
            miwa "I guess you're right."
            miwa "But I still think these look really nice on you."
            $ image.show(21)
            aona "Really?"
            $ image.show(22)
            miwa "Yes, really."
            $ image.show(23)
            aona "Mhh, thank you."
            
            call change_stats_with_modifier('pe',
                happiness = DEC_SMALL, inhibition = DEC_MEDIUM) from _call_change_stats_with_modifier_18
    else:
        $ image.show(10)
        miwa "Yeah, it looks really nice on you."
        $ image.show(11)
        aona "Yeah, doesn't it? And it's quite comfortable too."
        miwa "Amazing!"

        call change_stats_with_modifier('pe',
            happiness = MEDIUM, inhibition = DEC_TINY) from _call_change_stats_with_modifier_19

    $ end_event('new_daytime', **kwargs)

label gym_teach_pe_main_aona_bra (**kwargs): # Running
    $ begin_event(**kwargs)

    $ aona = get_person("class_3a", "aona_komuro").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Alright, today we will do some running."
    $ image.show(1)
    sgirl "Do we have to? Couldn't we do something else?" (name = "Aona Komuro")
    $ image.show(2)
    headmaster "Yes, it's important to keep your body in shape."
    headmaster "It's also a great way to improve your stamina and to improve your cardiovascular health."
    $ image.show(1)
    sgirl "But I don't like running." (name = "Aona Komuro")
    $ image.show(3)
    headmaster "Why that?"
    $ image.show(4)
    sgirl "Well my... Chest hurts because of... you know why." (name = "Aona Komuro")
    $ image.show(5)
    headmaster "Don't you have a sports bra?"
    $ image.show(6)
    sgirl "No, I don't." (name = "Aona Komuro")
    $ image.show(7)
    headmaster "Hmm, that's quite unfortunate. A state test is coming up and you need to be in shape for it because there will be several running tests."
    headmaster "Unfortunately I can't make an exception for you, so please bear with it for today."
    $ image.show(8)
    sgirl "..." (name = "Aona Komuro")
    $ image.show(9)
    headmaster "Alright, now please line up and let's get started. Today we will be doing sprints."
    call Image_Series.show_image(image, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22) from image_gym_teach_pe_main_aona_bra_1
    # images and animations of the girls running, Aona Komuro is struggling possibly holding her breasts
    
    call screen black_screen_text("1 hour later")

    $ image.show(23)
    headmaster "Alright, that's enough for today."
    headmaster "Don't forget to shower and change your clothes."
    # class leaves the gym
    $ image.show(24)
    headmaster "Aona, can you stay for a moment?"
    $ image.show(25)
    sgirl "Yes, Mr. [headmaster_last_name]?" (name = "Aona Komuro")
    $ image.show(26)
    headmaster "I'm sorry but you need to get a sports bra. It's important for your health and for your performance."
    $ image.show(27)
    sgirl "I know... But I don't have the money for it. Sport bras are terribly expensive for my ... size." (name = "Aona Komuro")
    $ image.show(28)
    headmaster "I see."
    $ image.show(29)
    headmaster "Hmm, I can't just give out money because of the Accounting, but I can get you one if you like."
    $ image.show(30)
    sgirl "Really? That would be great!" (name = "Aona Komuro")
    $ image.show(31)
    headmaster "Alright, let's do it like that, I'm sure I can just write it off as a business expense."
    headmaster "There is no shop nearby, but I could take you to the city after school. Would that be okay for you?"
    $ image.show(30)
    sgirl "Yes, that would be great!" (name = "Aona Komuro")
    sgirl "Thank you so much, Mr. [headmaster_last_name]!" (name = "Aona Komuro")
    $ image.show(31)
    headmaster "Not for that! I became your headmaster to help you all to become the best version of yourself."
    headmaster "And if it means spending a few bucks on a sports bra, then so be it."
    headmaster "Alright, now go and get changed. Come to my office after school, we'll then drive."
    $ image.show(30)
    sgirl "Yes, Mr. [headmaster_last_name]!" (name = "Aona Komuro")
    $ image.show(32)

    $ start_progress("aona_sports_bra")

    call change_stats_with_modifier('pe',
        happiness = TINY, charm = SMALL, reputation = TINY, inhibition = DEC_TINY) from _call_change_stats_with_modifier_23

    $ end_event('new_daytime', **kwargs)

label gym_teach_pe_main_aona_bra_2 (**kwargs):
    $ begin_event(**kwargs)

    $ aona = get_person("class_3a", "aona_komuro").get_character()

    $ bra = get_value('skimpy_bra', **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Alright, today we will do some running."
    sgirl "*MOAN*" (name = "Students", retain = False)
    $ image.show(1)
    headmaster "Yes, Yes! I know! I know! But you know the state test is coming up and you need to be in shape for it."
    $ image.show(2)
    headmaster "So now please line up and let's get started. Today we will be doing laps."
    headmaster "And go!"
    call Image_Series.show_image(image, 3, 4, 5, 6, 7) from image_gym_teach_pe_main_aona_bra_2_1
    headmaster "Alright, that's enough for today. Please shower and change your clothes."
    call Image_Series.show_image(image, 8, pause = True) from image_gym_teach_pe_main_aona_bra_2_2
    if bra == 1:
        call Image_Series.show_image(image, 9, 10, 11) from image_gym_teach_pe_main_aona_bra_2_3
        aona "Mr. [headmaster_last_name], I'm sorry but you bought the wrong bra."
        $ image.show(12)
        headmaster "What do you mean?"
        $ image.show(13)
        aona "This is the bra you offered me, which I didn't want to buy."
        $ image.show(14)
        headmaster "Oh I'm sorry. I must've swapped them by accident."
        headmaster "But why are you wearing it then?"
        $ image.show(15)
        aona "I didn't want to run without a bra again, so I didn't have a choice."
        $ image.show(16)
        headmaster "I see. But how did you feel in it? I mean, it looked like you were much more comfortable than before."
        $ image.show(17)
        aona "Well to be honest, it worked really well. It was quite comfortable and I didn't have any problems with my breasts."
        $ image.show(18)
        headmaster "And nobody cared, did they?"
        $ image.show(19)
        aona "Well... no."
        $ image.show(20)
        headmaster "So how about you try it on for a few more days and see how it goes?"
        $ image.show(21)
        aona "Mhh... Okay, I'll try it for now."
        $ image.show(22)
        headmaster "Alright, now go and get changed. You wouldn't want to miss your break, would you?"
        $ image.show(21)
        aona "No, thanks."

        call change_stats_with_modifier('pe',
            happiness = TINY, charm = SMALL, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_24
    else:
        call change_stats_with_modifier('pe',
            happiness = SMALL, charm = SMALL, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_25
    
    $ advance_progress("aona_sports_bra")

    $ end_event('new_daytime', **kwargs)

label aona_sports_bra_event_1 (**kwargs):
    $ begin_event(**kwargs)

    $ inhibition = get_stat_value('inhibition', [90, 95, 100], **kwargs)

    $ aona = get_person("class_3a", "aona_komuro").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ store_clerk = Character("Store Clerk", kind = character.vendor, retain = False)

    $ image.show(0)
    subtitles "*Knock* *Knock*"
    $ image.show(1)
    headmaster "Come in!"
    $ image.show(2)
    secretary "Excuse me Mr. [headmaster_last_name], Ms. Komuro is here to see you."
    $ image.show(3)
    headmaster "Ah yes, thank you! I'll come out!"
    call Image_Series.show_image(image, 4, 5) from image_aona_sports_bra_event_1_1
    headmaster "Ms. Langley, I'll be out with Ms. Komuro for a few hours."
    $ image.show(6)
    secretary "Okay, can I ask what you have planned?"
    $ image.show(7)
    headmaster "Ms. Komuro unfortunately is missing a sports bra and I'm going to take her get one in the next city."
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
    aona "I'm doing fine Mr. [headmaster_last_name]."
    $ image.show(15)
    headmaster "I'm glad to hear that. I'm sorry that I didn't notice earlier that you were struggling."
    $ image.show(16)
    aona "I don't really talk about it. I'm a bit embarrassed about it."
    $ image.show(17)
    headmaster "I understand. But you don't have to be embarrassed. It's a natural thing."
    $ image.show(18)
    aona "The other girls are sometimes a bit jealous of me because of my breasts."
    $ image.show(19)
    aona "But I hate my breasts. They're too big and I can't do anything about it."
    $ image.show(20)
    headmaster "I understand. I'm sure you have other struggles because of them, don't you?"
    $ image.show(21)
    aona "Yes, the worst thing is the constant back pain. I can't even sit properly in class."
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
    aona "That looks good. Can I try it on?"
    $ image.show(33)
    store_clerk "Of course! The changing rooms are over there."
    $ image.show(33)
    # aona goes into the changing room
    $ image.show(34)
    store_clerk "If you need more help, just call me."
    aona "Will do!"

    $ call_custom_menu(False,
        MenuElement("Wait", "Wait", EventEffect("aona_sports_bra_event_1.wait_1")),
        MenuElement("Look for a bra for yourself", "Look for a bra for yourself", EventEffect("aona_sports_bra_event_1.bra_for_self")),
        MenuElement("Peek into the changing room", "Peek into the changing room", EventEffect("aona_sports_bra_event_1.peek_1")),
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
    aona "This one fits quite well. I would like to take it."

    $ call_custom_menu(False,
        MenuElement("Buy bra", "Buy bra", EventEffect("aona_sports_bra_event_1.buy_bra")),
        MenuElement("Ask to try on your pick", "Ask to try on your pick", EventEffect("aona_sports_bra_event_1.try_alt_bra"), bra),
    **kwargs)
label .try_alt_bra (**kwargs):

    $ image.show(55)
    headmaster "I found this one, I think that would be a good choice."
    aona "Sure, I'll try it out."

    $ call_custom_menu(False,
        MenuElement("Peek", "Peek", EventEffect("aona_sports_bra_event_1.peek_2")),
        MenuElement("Wait", "Wait", EventEffect("aona_sports_bra_event_1.wait_2")),
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
    aona "Uhm sir? I think this one is a bit too skimpy for me."
    aona "I don't think I can wear that."
    $ image.show(64)
    headmaster "Do you care to show what you mean?"
    if inhibition >= 96:
        aona "Sorry, but I wouldn't feel comfortable doing that."
        $ image.show(65)
        headmaster "I understand. I'll take it back then."
        headmaster "Could you give me the other bra then? I'll quickly go pay for it."
        call .sneak_bra (**kwargs) from _call_aona_sports_bra_event_1_sneak_bra
    else:
        aona "Uhm, okay..."
        # aona steps out of the cabin
        $ image.show(66)
        headmaster "Oh, I see what you mean. But I think it suits you very well."
        $ image.show(67)
        headmaster "I mean it has a good support and has great ventilation, especially good for running."
        $ image.show(68)
        headmaster "Also, if I am allowed to say so, it looks very good on you and sure would provide a good boost in self confidence."
        if inhibition >= 91:
            $ image.show(69)
            aona "I understand, but I don't feel comfortable with it."
            $ image.show(70)
            headmaster "I understand. I'll take it back then."
            headmaster "Could you give me the other bra then? I'll quickly go pay for it."
            call .sneak_bra (**kwargs) from _call_aona_sports_bra_event_1_sneak_bra_1
        else:
            $ image.show(71)
            aona "Oh thank you for saying that, I guess I could take it."
            $ image.show(72)
            headmaster "Wonderful, let's take it then."
            $ kwargs["skimpy_bra"] = True
    
    call .buy_bra (**kwargs) from _call_aona_sports_bra_event_1_buy_bra
label .sneak_bra (**kwargs):

    $ call_custom_menu_with_text("Do you want to swap the bra with the skimpy variant?", character.subtitles, False,
        MenuElement("Swap", "Swap", EventEffect("aona_sports_bra_event_1.sneak_bra_true")),
        MenuElement("Don't swap", "Don't swap", EventEffect("aona_sports_bra_event_1.buy_bra")),
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
    aona "Thank you very much Mr. [headmaster_last_name]!"
    $ image.show(80)
    headmaster "You're welcome. I'm glad I could help you out."
    # back in car
    call Image_Series.show_image(image, 81, 82) from image_aona_sports_bra_event_1_9
    headmaster "You know, I had a thought about your back problems."
    $ image.show(83)
    headmaster "Have you tried massages or physiotherapy?"
    $ image.show(84)
    aona "Not really, I'm a bit embarrassed about it and my health insurance doesn't cover that."
    $ image.show(85)
    headmaster "I see... You know, in my studies about the human physiology I learned a lot about the human body."
    $ image.show(86)
    headmaster "Which also includes the back and how to treat it."
    $ image.show(85)
    headmaster "Sooo... if you'd like, I could give you a hand with your back pain."
    $ image.show(87)
    aona "Oh, I don't know..."
    $ image.show(88)
    headmaster "Don't worry, I'm a professional. I know what I'm doing."
    $ image.show(87)
    aona "Yeah, but I don't think that would be good. I wouldn't feel comfortable with that."
    $ image.show(88)
    headmaster "I understand. But if you ever change your mind, just let me know."
    $ image.show(87)
    aona "I'll think about it!"
    $ image.show(89)
    subtitles "The rest of the drive, Aona and the headmaster talked about different things concerning her back issues and her breasts."
    # Back at the school
    $ image.show(90)
    headmaster "Alright, we're back. I hope the bra will help you out."
    $ image.show(91)
    aona "Thank you very much Mr. [headmaster_last_name]!"
    $ image.show(90)
    headmaster "You're welcome. Have a good night! Don't stay up for too long, it's quite late already."
    $ image.show(91)
    aona "Yes, I will! Good night!"
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

    $ advance_progress("aona_sports_bra") # 1 -> 2

    $ change_stat(MONEY, -200)

    call change_stats_with_modifier(
        happiness = MEDIUM, charm = TINY, reputation = MEDIUM, inhibition = DEC_SMALL) from _call_change_stats_with_modifier_84

    $ end_event('new_daytime', **kwargs)


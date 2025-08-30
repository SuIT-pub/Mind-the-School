init -1 python:
    truth_or_dare_storage = FragmentStorage("truth_or_dare", 
        FragmentRepeatOption(RandomValueSelector("", 2, 6, True), False))
    truth_or_dare_end_storage = FragmentStorage("truth_or_dare_end")

init 1 python: 
    set_current_mod('base')

    base_path = "images/events/truth_or_dare/"

    truth_or_dare_event_1 = Event(3, "truth_or_dare_1",
        TimeCondition(daytime = "n"),
        LevelCondition("2,3", char_obj = "school"),
        NOT(ProgressCondition("truth_or_dare")),
        Pattern("main", base_path + "truth_or_dare_1/truth_or_dare_1 <school_level> <step>.webp"),
        thumbnail = base_path + "truth_or_dare_1/truth_or_dare_1 6 2.webp")

    courtyard_events["patrol"].add_event(truth_or_dare_event_1)

    truth_or_dare_event_2 = Event(3, "truth_or_dare_2",
        TimeCondition(daytime = "c", weekday = "d"),
        ProgressCondition("truth_or_dare", 1),
        Pattern("main", base_path + "truth_or_dare_2/truth_or_dare_2 <school_level> <step>.webp"),
        thumbnail = base_path + "truth_or_dare_2/truth_or_dare_2 6 8.webp")

    truth_or_dare_event_3 = Event(3, "truth_or_dare_3",
        TimeCondition(daytime = "c", weekday = "d"),
        ProgressCondition("truth_or_dare", 2),
        Pattern("main", base_path + "truth_or_dare_3/truth_or_dare_3 <school_level> <step>.webp"),
        thumbnail = base_path + "truth_or_dare_3/truth_or_dare_3 6 6.webp")

    sb_events["patrol"].add_event(truth_or_dare_event_2, truth_or_dare_event_3)

    truth_or_dare_event_4 = EventComposite(3, "truth_or_dare_4", [truth_or_dare_storage, truth_or_dare_end_storage], 
        TimeCondition(weekday = "d", daytime = "n"),
        ProgressCondition("truth_or_dare", 3),
        IterativeListSelector("girls", "ikushi_ito", "lin_kato", "miwa_igarashi", "ishimaru_maki", options = [FragmentRerollOption()]),
        Pattern("base", base_path + "truth_or_dare_4/main/truth_or_dare_4_main <school_level> <step>.webp"),
        Pattern("card", base_path + "truth_or_dare_4/card/truth_or_dare_4_card <girls> <school_level> <step>.webp"),
        Pattern("end", base_path + "truth_or_dare_4/card/truth_or_dare_4_end <school_level>.webp"),
        thumbnail = base_path + "truth_or_dare_4/main/truth_or_dare_4_main 6 1.webp")

    sd_events["peek_students"].add_event(truth_or_dare_event_4)

    truth_or_dare_storage.add_event(
        EventFragment(2, "truth_or_dare_truth_1", LevelCondition("2-10"), Pattern("main", base_path + "truth_or_dare_4/truth_1/truth_or_dare_truth_1 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_truth_2", LevelCondition("2-5"),  Pattern("main", base_path + "truth_or_dare_4/truth_2/truth_or_dare_truth_2 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_truth_3", LevelCondition("2-5"),  Pattern("main", base_path + "truth_or_dare_4/truth_3/truth_or_dare_truth_3 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_truth_4", LevelCondition("2-5"),  Pattern("main", base_path + "truth_or_dare_4/truth_4/truth_or_dare_truth_4 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_truth_5", LevelCondition("2-5"),  Pattern("main", base_path + "truth_or_dare_4/truth_5/truth_or_dare_truth_5 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_truth_6", LevelCondition("2-10"), Pattern("main", base_path + "truth_or_dare_4/truth_6/truth_or_dare_truth_6 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_1",  LevelCondition("2-5"),  Pattern("main", base_path + "truth_or_dare_4/dare_1/truth_or_dare_dare_1 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_2",  LevelCondition("2-5"),  Pattern("main", base_path + "truth_or_dare_4/dare_2/truth_or_dare_dare_2 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_3",  LevelCondition("2-10"), Pattern("main", base_path + "truth_or_dare_4/dare_3/truth_or_dare_dare_3 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_4",  LevelCondition("2-5"),  Pattern("main", base_path + "truth_or_dare_4/dare_4/truth_or_dare_dare_4 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_5",  LevelCondition("2-4"),  Pattern("main", base_path + "truth_or_dare_4/dare_5/truth_or_dare_dare_5 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_6",  LevelCondition("2-5"),  Pattern("main", base_path + "truth_or_dare_4/dare_6/truth_or_dare_dare_6 <school_level> <step>.webp"))
    )

    truth_or_dare_end_storage.add_event(
        EventFragment(2, "truth_or_dare_end", Pattern("main", base_path + "truth_or_dare_4/end/truth_or_dare_4_end <school_level>.webp"))
    )

# Planned Content from @Planned Content

# Courtyard: Patrol - Night
label truth_or_dare_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    # headmaster walks over Courtyard
    # headmaster sees girl running in the distance with no top on
    call Image_Series.show_image(image, 0, 1, 2) from _call_show_image_truth_or_dare_1_event_1
    headmaster_thought "Uhm..."

    # girl continues running and then leaves
    $ image.show(3)
    headmaster_thought "Mhh, the dorms should be over there..."
    headmaster_thought "I wonder what that was all about..."

    call change_stats_with_modifier(
        inhibition = DEC_SMALL, corruption = TINY) from _call_change_stats_truth_or_dare_1_1

    $ set_progress("truth_or_dare", 1)

    $ end_event("new_daytime", **kwargs)

# School Building: Patrol - Freetime
label truth_or_dare_2 (**kwargs):
    $ begin_event(**kwargs)

    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")
    $ lin = get_person_char_with_key("class_3a", "lin_kato")

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1) from _call_show_image_truth_or_dare_2_event_1
    miwa "That was crazy, that she really did that..."
    lin "I wouldn't have dared to do that..."
    $ image.show(2)
    miwa "Would you have done the punishment instead?"
    $ image.show(3)
    lin "..."
    $ image.show(4)
    lin "Probably not..."
    $ image.show(5)
    miwa "Yeah, are you there the next time? Ishimaru bought a new card set."
    lin "A new one? Nice, what's the theme?"
    $ image.show(6)
    miwa "She isn't sure. She just grabbed it, she said."
    miwa "I'm sure it's something funny, though."
    $ image.show(7)
    lin "Yeah probably."
    lin "Same time?"
    $ image.show(8)
    miwa "Yes!"

    call change_stats_with_modifier(
        happiness = TINY) from _stats_truth_or_dare_2_1

    $ advance_progress("truth_or_dare") # 1 -> 2

    $ end_event("new_daytime", **kwargs)

# School Building: Patrol - Freetime
label truth_or_dare_3 (**kwargs):
    $ begin_event(**kwargs)

    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    lin "Hey Ikushi, are you coming today?"
    $ image.show(1)
    ikushi "For what?"
    $ image.show(2)
    lin "Truth or Dare, of course!"
    $ image.show(3)
    ikushi "Oh, yeah! In the dorm lounge area again?"
    $ image.show(4)
    lin "Amazing! Yeah."
    $ image.show(5)
    ikushi "Great! I'll be there!"
    $ image.show(6)
    lin "Awesome! See you there!"

    call change_stats_with_modifier(
        happiness = TINY) from _stats_truth_or_dare_3_1

    $ advance_progress("truth_or_dare") # 2 -> 3

    $ end_event("new_daytime", **kwargs)

# School Dorm: Peek - Night
label truth_or_dare_4 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("base", **kwargs)

    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")

    $ image.show(0)
    headmaster_thought "Now let's see what they're up to..."

    $ image.show(1)
    ishimaru "Okay, let's start! Pull a card."

    headmaster_thought "Phew, came just in time."

    call composite_event_runner(**kwargs) from _call_composite_truth_or_dare_4_1

label truth_or_dare_end (**kwargs):
    $ begin_event(**kwargs)

    $ show_pattern("main", **kwargs)
    headmaster_thought "Very interesting..."
    headmaster_thought "I should leave now, before they notice me."
    $ end_event("new_daytime", **kwargs)

#####################
# region Truths --- #
#####################

# ikushi lin miwa ishimaru

# ikushi1 lin2 miwa3 ishimaru4
label truth_or_dare_truth_1 (**kwargs):
    $ begin_event(**kwargs)

    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")
    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")
    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "ikushi_ito"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_1_event_1
    ikushi "\"TRUTH: What's the naughtiest thing you've ever done with another girl?\"" # 1
    $ image.show(0)
    ikushi "Ahh, that's embarrassing..." # 1
    ikushi "I'm not sure if I can say that..." # 1
    $ image.show(1)
    lin "Come on! Tell us!" # 2
    $ image.show(2)
    miwa "Yeah!" # 3
    $ image.show(3)
    ikushi "Well... I once let my crush rub lotion on my back in the locker room during gym class." # 1
    ikushi "I wanted to feel her hands on me..." # 1
    $ image.show(4)
    lin "Uhh!!! Who was it?!" # 2
    $ image.show(5)
    miwa "Nah, that wasn't the question!!!" #1
    $ image.show(6)
    ishimaru "Come on! Tell us!" # 2
    $ image.show(7)
    ikushi "No way! I'm not telling that! Next one!" # 1

    call change_stats_with_modifier(
        inhibition = DEC_TINY) from _stats_truth_or_dare_truth_1_1

    $ end_event("new_daytime", **kwargs)

# lin1 miwa2 ishimaru3 ikushi4
label truth_or_dare_truth_2 (**kwargs):
    $ begin_event(**kwargs)

    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "lin_kato"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_2_event_1
    lin "\"TRUTH: Have you ever touched yourself when no one was looking? If so, where did you do it?\"" # 1
    $ image.show(0)
    lin "I... I haven't done that..." # 1
    lin "I'm not that kind of person..." # 1
    $ image.show(1)
    miwa "You didn't?" # 2
    $ image.show(2)
    lin "No..." # 1
    $ image.show(3)
    miwa "Lame! Next one!" #2
 
    call change_stats_with_modifier(
        corruption = DEC_TINY) from _stats_truth_or_dare_truth_2_1

    $ end_event("new_daytime", **kwargs)

# miwa1 ishimaru2 ikushi3 lin4
label truth_or_dare_truth_3 (**kwargs):
    $ begin_event(**kwargs)

    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")
    $ miwa_whisper = get_person_char_with_key("class_3a", "miwa_igarashi", "whisper")
    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
    $ ishimaru_shout = get_person_char_with_key("class_3a", "ishimaru_maki", "shout")
    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")
    $ lin = get_person_char_with_key("class_3a", "lin_kato")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "miwa_igarashi"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_3_event_1
    miwa "\"TRUTH: Who is your secret crush?\"" # 1
    $ image.show(0)
    miwa "*mumbles*" # 1
    $ image.show(1)
    ishimaru "We can't understand you..." # 2
    $ image.show(2)
    miwa "Ms. *mumbles*..." # 1
    $ image.show(3)
    ishimaru_shout "LOUDER!" # 2
    $ image.show(4)
    miwa_whisper "Ms. Ryan..." # 1
    $ image.show(5)
    ikushi "Ms. Ryan?!" #3
    $ image.show(6)
    ishimaru "Uhh that's crazy!" # 2
    lin "Yeah! But she's kinda hot!" # 4
    miwa "OKAY! Next one!" # 1

    call change_stats_with_modifier(
        charm = TINY, inhibition = DEC_TINY, corruption = TINY) from _stats_truth_or_dare_truth_3_1

    $ end_event("new_daytime", **kwargs)

# ishimaru1 ikushi2 lin3 miwa4
label truth_or_dare_truth_4 (**kwargs):
    $ begin_event(**kwargs)

    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")
    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "ishimaru_maki"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_4_event_1
    ishimaru "\"TRUTH: What's your favorite hobby or activity?\"" 
    $ image.show(0)
    ishimaru "Hah, that's easy!" 
    $ image.show(1)
    ikushi "Dang, why does she get the easy ones?" 
    lin "Yeah totally unfair!" 
    $ image.show(2)
    ishimaru "Of course it's playing guitar!" 
    $ image.show(3)
    miwa "Yeah we all knew that..." 
    $ image.show(4)
    ishimaru "Sucks. Next one!" 

    call change_stats_with_modifier(
        happiness = TINY, charm = TINY) from _stats_truth_or_dare_truth_4_1

    $ end_event("new_daytime", **kwargs)

# ikushi1 lin2 miwa3 ishimaru4
label truth_or_dare_truth_5 (**kwargs):
    $ begin_event(**kwargs)

    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")
    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")
    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "ikushi_ito"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_5_event_1
    ikushi "\"TRUTH: Have you ever fantasized about a teacher or other staff at your school?\"" 
    $ image.show(0)
    ikushi "Yeah, I think Mr [headmaster_last_name] is hot..." 
    $ image.show(1)
    lin "Whaaat?!" 
    $ image.show(2)
    headmaster_thought "Whaaat?!"
    $ image.show(3)
    miwa "No way!" 
    $ image.show(4)
    ishimaru "The headmaster?!" 
    $ image.show(2)
    headmaster_thought "Me?!"
    $ image.show(5)
    ikushi "Yeah! Have you ever seen him without his clothes on?" 
    $ image.show(1)
    lin "Without his clothes on?!" 
    $ image.show(6)
    ikushi "Yeah I once accidentally saw him in the locker rooms..." 
    ikushi "He is very nicely built, you know." 
    $ image.show(7)
    miwa "I wonder if he had many girlfriends..." 
    $ image.show(8)
    ikushi "I'm sure he did!" 
    $ image.show(9)
    lin "Okay, okay! Your turn!" 

    call change_stats_with_modifier(
        happiness = TINY, corruption = TINY, inhibition = DEC_TINY, reputation = SMALL) from _stats_truth_or_dare_truth_5_1

    $ end_event("new_daytime", **kwargs)

# lin1 miwa2 ishimaru3 ikushi4
label truth_or_dare_truth_6 (**kwargs):
    $ begin_event(**kwargs)

    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")
    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
    
    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "lin_kato"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_6_event_1
    lin "\"TRUTH: What's something that always makes you laugh?\"" 
    $ image.show(0)
    miwa "Again so easy..." 
    $ image.show(1)
    lin "I love watching cat videos on the internet..." 
    lin "I'm not even a cat person, but they're so cute, dumb and funny!" 
    miwa "Relatable..." 
    $ image.show(2)
    ishimaru "Oh have you seen the one where..." 
    call screen black_screen_text("Several minutes later...")

    $ image.show(3)
    lin "I'm sorry, I can't help it..." 
    $ image.show(4)
    miwa "I just can't stop laughing!" 
    $ image.show(5)
    ishimaru "Okay, okay! Next turn!" 

    call change_stats_with_modifier(
        happiness = MEDIUM) from _stats_truth_or_dare_truth_6_1

    $ end_event("new_daytime", **kwargs)

#endregion
#####################

####################
# region Dares --- #
####################

# ikushi1 lin2 miwa3 ishimaru4
label truth_or_dare_dare_1 (**kwargs):
    $ begin_event(**kwargs)

    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")
    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "ikushi_ito"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_1_event_1
    ikushi "\"DARE: Show us how you'd seduce a crush only using body language.\"" 
    $ image.show(0)
    ikushi "I'm not sure if I can do that..." 
    $ image.show(1)
    miwa "Is it worse than the punishment?" 
    $ image.show(2)
    ikushi "Ahh, I forgot about that..." 
    $ image.show(3)
    ikushi "..." 
    $ image.show(4)
    ikushi "Alright, here goes nothing..." 
    call Image_Series.show_image(image, 5, 6, 7,8) from _call_show_image_truth_or_dare_dare_1_event_2
    # The student leans in close to her chosen target, gazing into their eyes while slowly tracing a finger along their collarbone and whispering sultry encouragement.
    ikushi "Ah I'm sorry!" 
    $ image.show(9)
    lin "It's okay..." 
    $ image.show(10)
    ikushi "Next one please!" 

    call change_stats_with_modifier(
        happiness = TINY, corruption = TINY) from _stats_truth_or_dare_dare_1_1

    $ end_event("new_daytime", **kwargs)

# lin1 miwa2 ishimaru3 ikushi4
label truth_or_dare_dare_2 (**kwargs):
    $ begin_event(**kwargs)

    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")
    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "lin_kato"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_2_event_1
    lin "\"DARE: Kiss the person next to you.\"" 
    # girl leans over to give her a peck on the cheek
    call Image_Series.show_image(image, 0, 1, 2) from _call_show_image_truth_or_dare_dare_2_event_2
    lin "There, done!" 
    $ image.show(3)
    miwa "Come on, give her a real one!" 
    $ image.show(4)
    ishimaru "Yeah!" 
    $ image.show(5)
    lin "Alright!" 
    call Image_Series.show_image(image, 6, 7, 8, 9, 10, 11) from _call_show_image_truth_or_dare_dare_2_event_3
    # girl leans over to give her a kiss on the lips
    lin "There, pleased?" 
    $ image.show(12)
    miwa "Okay, we'll give it a pass..." 
    $ image.show(13)
    miwa "Next!" 

    call change_stats_with_modifier(
        happiness = TINY, inhibition = DEC_TINY, corruption = TINY) from _stats_truth_or_dare_dare_2_1

    $ end_event("new_daytime", **kwargs)
    
# miwa1 ishimaru2 ikushi3 lin4
label truth_or_dare_dare_3 (**kwargs):
    $ begin_event(**kwargs)

    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")
    $ miwa_shout = get_person_char_with_key("class_3a", "miwa_igarashi", "shout")
    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "miwa_igarashi"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_3_event_1
    miwa "\"DARE: Sing 'Happy Birthday' to yourself at the top of your lungs.\"" 
    $ image.show(0)
    miwa "Alright! *clears throat*" 
    $ image.show(1)
    miwa_shout "Happy birthday to me..." 
    $ image.show(2)
    miwa_shout "Happy birthday to me..." 
    $ image.show(3)
    miwa_shout "Happy birthday dear me..." 
    $ image.show(4)
    miwa_shout "Happy birthday to me..." 
    $ image.show(5)
    miwa "Alright, done! Wasn't it beautiful?" 
    $ image.show(6)
    ishimaru "Nothing more beautiful..." 
    $ image.show(7)
    ikushi "I think the next one should go..." 
    $ image.show(8)
    ishimaru "Yeah, that's probably the best..." 

    call change_stats_with_modifier(
        happiness = TINY, charm = TINY) from _stats_truth_or_dare_dare_3_1

    $ end_event("new_daytime", **kwargs)

# ishimaru1 ikushi2 lin3 miwa4
label truth_or_dare_dare_4 (**kwargs):
    $ begin_event(**kwargs)

    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")
    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "ishimaru_maki"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_4_event_1
    ishimaru "\"DARE: Whisper three naughty things you've thought about doing with someone else into the ear of the person next to you.\"" 
    $ image.show(0)
    ishimaru "I'm not sure if I should do this..." 
    $ image.show(1)
    ishimaru "Well, here goes nothing..." 
    # girl leans over and whispers into the ear of the person next to her
    call Image_Series.show_image(image, 2, 3, 4) from _call_show_image_truth_or_dare_dare_4_event_2
    ikushi "Oh wow, that's a lot..." 
    $ image.show(5)
    ishimaru "I'm sorry, I..." 
    $ image.show(6)
    ikushi "No, no, it's okay! Kinda hot actually..." 
    $ image.show(7)
    lin "Whaaa... What was it?" 
    $ image.show(8)
    ikushi "Nope, I'm not telling you!" 
    $ image.show(9)
    miwa "Come on!" 
    $ image.show(10)
    ikushi "Nope, forget it! Next one!" 

    call change_stats_with_modifier(
        corruption = SMALL) from _stats_truth_or_dare_dare_4_1

    $ end_event("new_daytime", **kwargs)

# ikushi1 lin2 miwa3 ishimaru4    
label truth_or_dare_dare_5 (**kwargs):
    $ begin_event(**kwargs)

    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")
    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")
    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "ikushi_ito"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_5_event_1
    ikushi "\"DARE: Show off your underwear to the other players.\"" 
    $ image.show(0)
    ikushi "What? I can't do that!"
    $ image.show(1)
    lin "Come on, it's just underwear!"
    $ image.show(0)
    ikushi "Yeah, but I'm only wearing my pajamas!"
    $ image.show(1)
    lin "And?"
    $ image.show(2)
    ikushi "And I'm not wearing anything under them!"
    $ image.show(3)
    lin "Oh my god, you're right!"
    $ image.show(4)
    miwa "Well, I guess birthday suits are better than nothing!"
    $ image.show(5)
    ikushi "What?! I'm not stripping!"
    $ image.show(6)
    lin "Then do the punishment!"
    $ image.show(5)
    ikushi "No way!"
    $ image.show(7)
    lin "Well, either way, you have to strip, either as punishment or as a dare!"
    $ image.show(8)
    miwa "And punishment would be running laps around the school!"
    $ image.show(9)
    ikushi "..."
    $ image.show(10)
    ikushi "Fine, I'll do it!"
    $ image.show(11)
    ishimaru "Woohoo!"
    # ikushi strips
    call Image_Series.show_image(image, 12, 13, 14, 15, pause = True) from _call_show_image_truth_or_dare_dare_5_event_2
    ishimaru "Yeah, go girl!"
    lin "Sexy!"
    $ image.show(16)
    ikushi "Okay, you had your fill! Next one!"

    call change_stats_with_modifier(
        happiness = DEC_TINY, inhibition = MEDIUM, corruption = TINY) from _stats_truth_or_dare_dare_5_1

    $ end_event("new_daytime", **kwargs)

# lin1 miwa2 ishimaru3 ikushi4
label truth_or_dare_dare_6 (**kwargs):
    $ begin_event(**kwargs)

    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")
    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")
    $ ikushi = get_person_char_with_key("class_3a", "ikushi_ito")

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern_with_data("card", {"girls": "lin_kato"}, **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_6_event_1
    lin "\"DARE: Wear only your panties to sleep tonight.\"" 
    $ image.show(0)
    lin "Sure, why not?"
    $ image.show(1)
    lin "I'll just sleep in my underwear!"
    $ image.show(2)
    miwa "Not underwear, only panties!"
    $ image.show(3)
    lin "Yeah alright! Anyway, I wonder what it feels like anyway."
    $ image.show(4)
    ikushi "Too bad, we won't be able to see you then!" #:P
    $ image.show(5)
    lin "Sucks! Next one!"

    call change_stats_with_modifier(
        education = TINY, inhibition = DEC_TINY, corruption = TINY) from _stats_truth_or_dare_dare_6_1

    $ end_event("new_daytime", **kwargs)


#endregion
####################

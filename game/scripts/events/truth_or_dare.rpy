init -1 python:
    truth_or_dare_storage = FragmentStorage("truth_or_dare", 
        FragmentRepeatOption(RandomValueSelector("", 2, 6, True), False))
    truth_or_dare_end_storage = FragmentStorage("truth_or_dare_end")

init 1 python: 
    set_current_mod('base')

    base_path = "images/events/truth_or_dare/"

    truth_or_dare_event_1 = Event(3, "truth_or_dare_1",
        TimeCondition(daytime = "c", weekday = "n"),
        LevelCondition("2,3", char_obj = "school"),
        NOT(ProgressCondition("truth_or_dare")),
        Pattern("main", base_path + "truth_or_dare_1/truth_or_dare_1 <school_level> <step>.webp"),
        thumbnail = base_path + "truth_or_dare_1/truth_or_dare_1 6 2.webp")

    courtyard_events["patrol"].add_event(truth_or_dare_event_1)

    truth_or_dare_event_2 = Event(3, "truth_or_dare_2",
        TimeCondition(daytime = "c", weekday = "f"),
        ProgressCondition("truth_or_dare", 1),
        Pattern("main", base_path + "truth_or_dare_2/truth_or_dare_2 <school_level> <step>.webp"),
        thumbnail = base_path + "truth_or_dare_2/truth_or_dare_2 6 8.webp")

    truth_or_dare_event_3 = Event(3, "truth_or_dare_3",
        TimeCondition(daytime = "c", weekday = "f"),
        ProgressCondition("truth_or_dare", 2),
        Pattern("main", base_path + "truth_or_dare_3/truth_or_dare_3 <school_level> <step>.webp"),
        thumbnail = base_path + "truth_or_dare_3/truth_or_dare_3 6 6.webp")

    sb_events["patrol"].add_event(truth_or_dare_event_2, truth_or_dare_event_3)

    truth_or_dare_event_4 = EventComposite(3, "truth_or_dare_4", [truth_or_dare_storage, truth_or_dare_end_storage], 
        TimeCondition(weekday = "d", daytime = "n"),
        ProgressCondition("truth_or_dare", 3),
        IterativeListSelector("girls", "ikushi_ito", "lin_kato", "miwa_igarashi", "ishimaru_maki", options = [FragmentRerollOption()]),
        Pattern("base", base_path + "truth_or_dare_4/main/truth_or_dare_4 <school_level> <step>.webp"),
        Pattern("card", base_path + "truth_or_dare_4/card/truth_or_dare_card <girls> <school_level> <step>.webp"),
        Pattern("end", base_path + "truth_or_dare_4/card/truth_or_dare_4_end <school_level>.webp"),
        thumbnail = base_path + "truth_or_dare_4/main/truth_or_dare_4_main 6 1.webp")

    sd_events["peek_students"].add_event(truth_or_dare_event_4)

    truth_or_dare_storage.add_event(
        EventFragment(2, "truth_or_dare_truth_1", Pattern("main", base_path + "truth_or_dare_4/truth_1/truth_or_dare_truth_1 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_truth_2", Pattern("main", base_path + "truth_or_dare_4/truth_2/truth_or_dare_truth_2 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_truth_3", Pattern("main", base_path + "truth_or_dare_4/truth_3/truth_or_dare_truth_3 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_truth_4", Pattern("main", base_path + "truth_or_dare_4/truth_4/truth_or_dare_truth_4 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_truth_5", Pattern("main", base_path + "truth_or_dare_4/truth_5/truth_or_dare_truth_5 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_truth_6", Pattern("main", base_path + "truth_or_dare_4/truth_6/truth_or_dare_truth_6 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_1", Pattern("main", base_path + "truth_or_dare_4/dare_1/truth_or_dare_dare_1 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_2", Pattern("main", base_path + "truth_or_dare_4/dare_2/truth_or_dare_dare_2 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_3", Pattern("main", base_path + "truth_or_dare_4/dare_3/truth_or_dare_dare_3 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_4", Pattern("main", base_path + "truth_or_dare_4/dare_4/truth_or_dare_dare_4 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_5", Pattern("main", base_path + "truth_or_dare_4/dare_5/truth_or_dare_dare_5 <school_level> <step>.webp")),
        EventFragment(2, "truth_or_dare_dare_6", Pattern("main", base_path + "truth_or_dare_4/dare_6/truth_or_dare_dare_6 <school_level> <step>.webp"))
    )

    truth_or_dare_end_storage.add_event(
        EventFragment(2, "truth_or_dare_end",
            Pattern("main", base_path + "truth_or_dare_4/end/truth_or_dare_end <school_level>.webp"),
        )
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

    call change_stats_with_modifier('school',
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

    $ advance_progress("truth_or_dare") # 2 -> 3

    $ end_event("new_daytime", **kwargs)

# School Dorm: Peek - Night
label truth_or_dare_4 (**kwargs):
    $ begin_event(**kwargs)

    $ girls = ["ikushi_ito", "lin_kato", "miwa_igarashi", "ishimaru_maki"]

    $ girl1_key = get_person_value("girls", "ishimaru_maki", **kwargs)
    $ girl2_key = get_next_in_list(girls, girl1_key)
    $ girl3_key = get_next_in_list(girls, girl2_key)
    $ girl4_key = get_next_in_list(girls, girl3_key)

    $ kwargs = set_kwargs_value("girl1_key", girl1_key, **kwargs)
    $ kwargs = set_kwargs_value("girl2_key", girl2_key, **kwargs)
    $ kwargs = set_kwargs_value("girl3_key", girl3_key, **kwargs)
    $ kwargs = set_kwargs_value("girl4_key", girl4_key, **kwargs)

    $ kwargs = set_kwargs_value("girl1", get_person_char_with_key("class_3a", girl1_key), **kwargs)
    $ kwargs = set_kwargs_value("girl2", get_person_char_with_key("class_3a", girl2_key), **kwargs)
    $ kwargs = set_kwargs_value("girl3", get_person_char_with_key("class_3a", girl3_key), **kwargs)
    $ kwargs = set_kwargs_value("girl4", get_person_char_with_key("class_3a", girl4_key), **kwargs)

    $ image = convert_pattern("base", **kwargs)

    $ ishimaru = get_person_char_with_key("class_3a", "ishimaru_maki")

    $ girl_name = get_person_char_with_key("class_3a", girl1_key).get_first_name()

    $ image.show(0)
    headmaster_thought "Now let's see what they're up to..."

    $ image.show(1)
    ishimaru "Okay [girl_name], you'll start today. Pull a card."

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
    $ card_image = convert_pattern_width_data("card", {"girls": "ikushi_ito"}, **kwargs)

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

    $ end_event("new_daytime", **kwargs)


# lin1 miwa2 ishimaru3 ikushi4
label truth_or_dare_truth_2 (**kwargs):
    $ begin_event(**kwargs)

    $ lin = get_person_char_with_key("class_3a", "lin_kato")
    $ miwa = get_person_char_with_key("class_3a", "miwa_igarashi")

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_2_event_1
    girl1 "\"TRUTH: Have you ever touched yourself when no one was looking? If so, where did you do it?\"" # 1
    $ image.show(0)
    girl1 "I... I haven't done that..." # 1
    girl1 "I'm not that kind of person..." # 1
    $ image.show(1)
    girl2 "You didn't?" # 2
    $ image.show(2)
    girl1 "No..." # 1
    $ image.show(3)
    girl2 "Lame! Next one!" #2
 
    $ end_event("new_daytime", **kwargs)

label truth_or_dare_truth_3 (**kwargs):
    $ begin_event(**kwargs)

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl1_whisper = get_kwargs_value("girl1", **kwargs).get_character("whisper")
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()
    $ girl2_shout = get_kwargs_value("girl2", **kwargs).get_character("shout")
    $ girl3 = get_kwargs_value("girl3", **kwargs).get_character()
    $ girl4 = get_kwargs_value("girl4", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_3_event_1
    girl1 "\"TRUTH: Who is your secret crush?\"" # 1
    girl1 "*mumbles*" # 1
    girl2 "We can't understand you..." # 2
    girl1 "Mrs. *mumbles*..." # 1
    girl2_shout "LOUDER!" # 2
    girl1_whisper "Mrs. Ryan..." # 1
    girl3 "Mrs. Ryan?!" #3
    girl2 "Uhh that's crazy!" # 2
    girl4 "Yeah! But she's kinda hot!" # 4
    girl1 "OKAY! Next one!" # 1

    $ end_event("new_daytime", **kwargs)

label truth_or_dare_truth_4 (**kwargs):
    $ begin_event(**kwargs)

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()
    $ girl3 = get_kwargs_value("girl3", **kwargs).get_character()
    $ girl4 = get_kwargs_value("girl4", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_4_event_1
    girl1 "\"TRUTH: What's your favorite hobby or activity?\"" 
    girl1 "Hah, that's easy!" 
    girl2 "Dang, why does she get the easy ones?" 
    girl3 "Yeah totally unfair!" 
    girl1 "Of course it's playing guitar!" 
    girl4 "Yeah we all knew that..." 
    girl1 "Sucks. Next one!" 

    $ end_event("new_daytime", **kwargs)

label truth_or_dare_truth_5 (**kwargs):
    $ begin_event(**kwargs)

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()
    $ girl3 = get_kwargs_value("girl3", **kwargs).get_character()
    $ girl4 = get_kwargs_value("girl4", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_5_event_1
    girl1 "\"TRUTH: Have you ever fantasized about a teacher or other staff at your school?\"" 
    girl1 "Yeah, I think Mr [headmaster_name] is hot..." 
    girl2 "Whaaat?!" 
    headmaster_thought "Whaaat?!"
    girl3 "No way!" 
    girl4 "The headmaster?!" 
    headmaster_thought "Me?!"
    girl1 "Yeah! Have you ever seen him without his clothes on?" 
    girl2 "Without his clothes on?!" 
    girl1 "Yeah I once accidentally saw him in the locker rooms..." 
    girl1 "He is very nicely built, you know." 
    girl3 "I wonder if he had many girlfriends..." 
    girl1 "I'm sure he did!" 
    girl2 "Okay, okay! Your turn!" 

    $ end_event("new_daytime", **kwargs)

label truth_or_dare_truth_6 (**kwargs):
    $ begin_event(**kwargs)

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()
    $ girl3 = get_kwargs_value("girl3", **kwargs).get_character()
    $ girl4 = get_kwargs_value("girl4", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_truth_6_event_1
    girl1 "\"TRUTH: What's something that always makes you laugh?\"" 
    girl2 "Again so easy..." 
    girl1 "I love watching cat videos on the internet..." 
    girl1 "I'm not even a cat person, but they're so cute, dumb and funny!" 
    girl2 "Relatable..." 
    girl3 "Oh have you seen the one where..." 
    call screen black_screen_text("Several minutes later...")

    girl1 "I'm sorry, I can't help it..." 
    girl2 "I just can't stop laughing!" 
    girl3 "Okay, okay! Next turn!" 

    $ end_event("new_daytime", **kwargs)

#endregion
#####################

####################
# region Dares --- #
####################

label truth_or_dare_dare_1 (**kwargs):
    $ begin_event(**kwargs)

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()
    $ girl3 = get_kwargs_value("girl3", **kwargs).get_character()
    $ girl4 = get_kwargs_value("girl4", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_1_event_1
    girl1 "\"DARE: Show us how you'd seduce a crush only using body language.\"" 
    girl1 "I'm not sure if I can do that..." 
    girl2 "Is it worse than the punishment?" 
    girl1 "Ahh, I forgot about that..." 
    girl1 "..." 
    girl1 "Alright, here goes nothing..." 
    # The student leans in close to her chosen target, gazing into their eyes while slowly tracing a finger along their collarbone and whispering sultry encouragement.
    girl1 "Ah I'm sorry!" 
    girl3 "It's okay..." 
    girl1 "Next one please!" 

    $ end_event("new_daytime", **kwargs)

label truth_or_dare_dare_2 (**kwargs):
    $ begin_event(**kwargs)

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()
    $ girl3 = get_kwargs_value("girl3", **kwargs).get_character()
    $ girl4 = get_kwargs_value("girl4", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_2_event_1
    girl1 "\"DARE: Kiss the person next to you.\"" 
    # girl leans over to give her a peck on the cheek
    girl1 "There, done!" 
    girl2 "Come on, give her a real one!" 
    girl3 "Yeah!" 
    girl1 "Alright!" 
    # girl leans over to give her a kiss on the lips
    girl1 "There, pleased?" 
    girl2 "Okay, we'll give it a pass..." 
    girl2 "It's your turn!" 
    
    $ end_event("new_daytime", **kwargs)
    
label truth_or_dare_dare_3 (**kwargs):
    $ begin_event(**kwargs)

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl1_shout = get_kwargs_value("girl1", **kwargs).get_character("shout")
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()
    $ girl3 = get_kwargs_value("girl3", **kwargs).get_character()
    $ girl4 = get_kwargs_value("girl4", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_3_event_1
    girl1 "\"DARE: Sing 'Happy Birthday' to yourself at the top of your lungs.\"" 
    girl1 "Alright! *clears throat*" 
    girl1_shout "Happy birthday to me..." 
    girl1_shout "Happy birthday to me..." 
    girl1_shout "Happy birthday dear me..." 
    girl1_shout "Happy birthday to me..." 
    girl1 "Alright, done! Wasn't it beautiful?" 
    girl2 "Nothing more beautiful..." 
    girl3 "I think the next one should go..." 
    girl2 "Yeah, that's probably the best..." 

    $ end_event("new_daytime", **kwargs)

label truth_or_dare_dare_4 (**kwargs):
    $ begin_event(**kwargs)

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()
    $ girl3 = get_kwargs_value("girl3", **kwargs).get_character()
    $ girl4 = get_kwargs_value("girl4", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_4_event_1
    girl1 "\"DARE: Whisper three naughty things you've thought about doing with someone else into the ear of the person next to you.\"" 
    girl1 "I'm not sure if I should do this..." 
    girl1 "Well, here goes nothing..." 
    # girl leans over and whispers into the ear of the person next to her
    girl2 "Oh wow, that's a lot..." 
    girl1 "I'm sorry, I can't help it..." 
    girl2 "No, no, it's okay! Kinda hot actually..." 
    girl3 "Whaaa... What was it?" 
    girl2 "Nope, I'm not telling you!" 
    girl4 "Come on!" 
    girl2 "Nope, forget it! Next one!" 

    $ end_event("new_daytime", **kwargs)
    
label truth_or_dare_dare_5 (**kwargs):
    $ begin_event(**kwargs)

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()
    $ girl3 = get_kwargs_value("girl3", **kwargs).get_character()
    $ girl4 = get_kwargs_value("girl4", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_5_event_1
    girl1 "\"DARE: Remove one article of clothing.\"" 
    girl1 "But someone could see us..." 
    girl2 "Come on, don't be shy!" 
    girl3 "Otherwise do the punishment!" 
    girl1 "Okay..." 
    # girl removes one article of clothing
    girl1 "There, done!" 
    girl2 "Whoo, hot!" 
    girl1 "Yeah yeah!" 

    $ end_event("new_daytime", **kwargs)
    
label truth_or_dare_dare_6 (**kwargs):
    $ begin_event(**kwargs)

    $ girl1 = get_kwargs_value("girl1", **kwargs).get_character()
    $ girl1_shout = get_kwargs_value("girl1", **kwargs).get_character("shout")
    $ girl2 = get_kwargs_value("girl2", **kwargs).get_character()
    $ girl3 = get_kwargs_value("girl3", **kwargs).get_character()
    $ girl4 = get_kwargs_value("girl4", **kwargs).get_character()

    $ image = convert_pattern("main", **kwargs)
    $ card_image = convert_pattern("card", **kwargs)

    call Image_Series.show_image(card_image, 0, 1) from _call_show_image_truth_or_dare_dare_6_event_1
    girl1 "\"DARE: Wear provocative underwear to school tomorrow.\"" 
    girl1_shout "WHAT?!" 
    girl2 "No way that's in there!" 
    # girl takes card
    girl3 "OMG! That's awesome!" 
    girl2 "It's really on there!" 
    girl1 "I'm not doing that!" 
    girl2 "Then do the punishment!" 
    girl1 "Do I really have to?" 
    girl3 "You know the rules..." 
    girl1 "Okay, I will wear something sexy tomorrow!" 
    girl2 "Good girl!" 

    girl4 "Next one!" 

    $ end_event("new_daytime", **kwargs)


#endregion
####################

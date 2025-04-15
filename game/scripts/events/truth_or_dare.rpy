init -1 python:
    truth_or_dare_storage = FragmentStorage("truth_or_dare", 
        FragmentRepeatOption(RandomValueSelector("", 2, 6, True), False))
    truth_or_dare_end_storage = FragmentStorage("truth_or_dare_end")

init 1 python: 
    set_current_mod('base')

    truth_or_dare_event_1 = Event(3, "truth_or_dare_1",
        TimeCondition(daytime = "c", weekday = "n"),
        LevelCondition("2,3", char_obj = "school"),
        NOT(ProgressCondition("truth_or_dare")),
        Pattern("main", "images/events/truth_or_dare/truth_or_dare_1/truth_or_dare_1 <school_level> <step>.webp"),
        thumbnail = "images/events/truth_or_dare/truth_or_dare_1/thumbnail.webp")

    courtyard_events["patrol"].add_event(truth_or_dare_event_1)

    truth_or_dare_event_2 = Event(3, "truth_or_dare_2",
        TimeCondition(daytime = "c", weekday = "f"),
        ProgressCondition("truth_or_dare", 1),
        Pattern("main", "images/events/truth_or_dare/truth_or_dare_2/truth_or_dare_2 <school_level> <step>.webp"),
        thumbnail = "images/events/truth_or_dare/truth_or_dare_2/thumbnail.webp")

    truth_or_dare_event_3 = Event(3, "truth_or_dare_3",
        TimeCondition(daytime = "c", weekday = "f"),
        ProgressCondition("truth_or_dare", 2),
        Pattern("main", "images/events/truth_or_dare/truth_or_dare_3/truth_or_dare_3 <step>.webp"),
        thumbnail = "images/events/truth_or_dare/truth_or_dare_3/thumbnail.webp")

    sb_events["patrol"].add_event(truth_or_dare_event_2, truth_or_dare_event_3)

    truth_or_dare_event_4 = EventComposite(3, "truth_or_dare_4", [truth_or_dare_storage, truth_or_dare_end_storage], 
        TimeCondition(weekday = "d", daytime = "n"),
        ProgressCondition("truth_or_dare", 3),
        IterativeListSelector("girls", "ikushi_ito", "lin_kato", "miwa_igarashi", "ishimaru_maki", options = [FragmentRerollOption()]),
        Pattern("base", "images/events/truth_or_dare/truth_or_dare_4/truth_or_dare_4 <school_level> <step>.webp"))

    sd_events["peek_students"].add_event(truth_or_dare_event_4)

    truth_or_dare_storage.add_event(
        EventFragment(2, "truth_or_dare_truth_1"),
        EventFragment(2, "truth_or_dare_dare_1")
    )

    truth_or_dare_end_storage.add_event(
        EventFragment(2, "truth_or_dare_end")
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

    $ miwa = get_person_char("students", "miwa_igarashi")
    $ lin = get_person_char("students", "lin_kato")

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

    $ lin = get_person_char("students", "lin_kato")
    $ ikushi = get_person_char("students", "ikushi_ito")

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

    headmaster_thought "Now let's see what they're up to..."

    sgirl "Okay! You'll start today. Pull a card."

    headmaster_thought "Phew, came just in time."

    call composite_event_runner(**kwargs) from _call_composite_truth_or_dare_4_1

label truth_or_dare_end (**kwargs):
    $ begin_event(**kwargs)

    headmaster_thought "Very interesting..."
    headmaster_thought "I should leave now, before they notice me."
    $ end_event("new_daytime", **kwargs)

#####################
# region Truths --- #
#####################

# Level 2
label truth_or_dare_truth_1 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"TRUTH: What's the naughtiest thing you've ever done with another girl?\"" # 1
    sgirl "Ahh, that's embarrassing..." # 1
    sgirl "I'm not sure if I can say that..." # 1
    sgirl "Come on! Tell us!" # 2
    sgirl "Yeah!" # 3
    sgirl "Well... I once let my crush rub lotion on my back in the locker room during gym class." # 1
    sgirl "I wanted to feel her hands on me..." # 1
    sgirl "Uhh!!! Who was it?!" # 2
    sgirl "Nah, that wasn't the question!!!" #1
    sgirl "Come on! Tell us!" # 2
    sgirl "No way! I'm not telling that! Next one!" # 1

    $ end_event("new_daytime", **kwargs)


# Level 2
label truth_or_dare_truth_2 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"TRUTH: Have you ever touched yourself when no one was looking? If so, where did you do it?\"" # 1
    sgirl "I... I haven't done that..." # 1
    sgirl "I'm not that kind of person..." # 1
    sgirl "You didn't?" # 2
    sgirl "No..." # 1
    sgirl "Lame! Next one!" #2
 
    $ end_event("new_daytime", **kwargs)

label truth_or_dare_truth_3 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"TRUTH: Who is your secret crush?\"" # 1
    sgirl "*mumbles*" # 1
    sgirl "We can't understand you..." # 2
    sgirl "Mrs. *mumbles*..." # 1
    sgirl_shout "LOUDER!" # 2
    sgirl_whisper "Mrs. Ryan..." # 1
    sgirl "Mrs. Ryan?!" #3
    sgirl "Uhh that's crazy!" # 2
    sgirl "Yeah! But she's kinda hot!" # 4
    sgirl "OKAY! Next one!" # 1

    $ end_event("new_daytime", **kwargs)

label truth_or_dare_truth_4 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"TRUTH: What's your favorite hobby or activity?\"" # 1
    sgirl "Hah, that's easy!" # 1
    sgirl "Dang, why does she get the easy ones?" # 2
    sgirl "Yeah totally unfair!" # 3
    sgirl "Of course it's playing guitar!" # 1
    sgirl "Yeah we all knew that..." # 4
    sgirl "Sucks. Next one!" # 1

    $ end_event("new_daytime", **kwargs)

label truth_or_dare_truth_5 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"TRUTH: Have you ever fantasized about a teacher or other staff at your school?\"" # 1
    sgirl "Yeah, I think Mr [headmaster_name] is hot..." # 1
    sgirl "Whaaat?!" # 2
    headmaster_thought "Whaaat?!"
    sgirl "No way!" # 3
    sgirl "The headmaster?!" # 4
    headmaster_thought "Me?!"
    sgirl "Yeah! Have you ever seen him without his clothes on?" # 1
    sgirl "Without his clothes on?!" # 2
    sgirl "Yeah I once accidentally saw him in the locker rooms..." # 1
    sgirl "He is very nicely built, you know." # 1
    sgirl "I wonder if he had many girlfriends..." # 3
    sgirl "I'm sure he did!" # 1
    sgirl "Okay, okay! Your turn!" # 2

    $ end_event("new_daytime", **kwargs)

label truth_or_dare_truth_6 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"TRUTH: What's something that always makes you laugh?\"" # 1
    sgirl "Again so easy..." # 2
    sgirl "I love watching cat videos on the internet..." # 1
    sgirl "I'm not even a cat person, but they're so cute, dumb and funny!" # 1
    sgirl "Relatable..." # 2
    sgirl "Oh have you seen the one where..." # 3
    call screen black_screen_text("Several minutes later...")

    sgirl "I'm sorry, I can't help it..." # 1
    sgirl "I just can't stop laughing!" # 2
    sgirl "Okay, okay! Next turn!" # 3

    $ end_event("new_daytime", **kwargs)

#endregion
#####################

####################
# region Dares --- #
####################

label truth_or_dare_dare_1 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"DARE: Show us how you'd seduce a crush only using body language.\"" # 1
    sgirl "I'm not sure if I can do that..." # 1
    sgirl "Is it worse that the punishment?" # 2
    sgirl "Ahh, I forgot about that..." # 1
    sgirl "..."
    sgirl "Alright, here goes nothing..." # 1
    # The student leans in close to her chosen target, gazing into their eyes while slowly tracing a finger along their collarbone and whispering sultry encouragement.
    sgirl "Ah I'm sorry!" # 1
    sgirl "It's okay..." # 3
    sgirl "Next one please!" # 1

    $ end_event("new_daytime", **kwargs)

label truth_or_dare_dare_2 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"DARE: Kiss the person next to you.\"" # 1
    # girl leans over to give her a peck on the cheek
    sgirl "There, done!" # 1
    sgirl "Come on, give her a real one!" # 2
    sgirl "Yeah!" # 3
    sgirl "Alright!" # 1
    # girl leans over to give her a kiss on the lips
    sgirl "There, pleased?" # 1
    sgirl "Okay, we'll give it a pass..." # 2
    sgirl "It's your turn!" # 2
    
    $ end_event("new_daytime", **kwargs)
    
label truth_or_dare_dare_3 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"DARE: Sing 'Happy Birthday' to yourself at the top of your lungs.\"" # 1
    sgirl "Alright! *clears throat*"
    sgirl_shout "Happy birthday to me..." # 1
    sgirl_shout "Happy birthday to me..." # 1
    sgirl_shout "Happy birthday dear me..." # 1
    sgirl_shout "Happy birthday to me..." # 1
    sgirl "Alright, done! Wasn't it beautiful?" # 1
    sgirl "Nothing more beautiful..." # 2
    sgirl "I think the next one should go..." # 3
    sgirl "Yeah, that's probably the best..." # 2

    $ end_event("new_daytime", **kwargs)

label truth_or_dare_dare_4 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"DARE: Whisper three naughty things you've thought about doing with someone else into the ear of the person next to you.\"" # 1
    sgirl "I'm not sure if I should do this..." # 1
    sgirl "Well, here goes nothing..." # 1
    # girl leans over and whispers into the ear of the person next to her
    sgirl "Oh wow, that's a lot..." # 2
    sgirl "I'm sorry, I can't help it..." # 1
    sgirl "No, no, it's okay! Kinda hot actually..." # 2
    sgirl "Whaaa... What was it?" # 3
    sgirl "Nope, I'm not telling you!" # 2
    sgirl "Come on!" # 4
    sgirl "Nope, forget it! Next one!" # 2

    $ end_event("new_daytime", **kwargs)
    
label truth_or_dare_dare_5 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"DARE: Remove one article of clothing.\"" # 1
    sgirl "But someone could see us..." # 1
    sgirl "Come on, don't be shy!" # 2
    sgirl "Otherwise do the punishment!" # 3
    sgirl "Okay..." # 1
    # girl removes one article of clothing
    sgirl "There, done!" # 1
    sgirl "Whoo, hot!" # 2
    sgirl "Yeah yeah!"

    $ end_event("new_daytime", **kwargs)
    
label truth_or_dare_dare_6 (**kwargs):
    $ begin_event(**kwargs)

    sgirl "\"DARE: Wear provocative underwear to school tomorrow.\"" # 1
    sgirl_shout "WHAT?!" # 1
    sgirl "No way that's in there!" # 2
    # girl takes card
    sgirl "OMG! That's awesome!" # 3
    sgirl "It's really on there!" # 2
    sgirl "I'm not doing that!" # 1
    sgirl "Then do the punishment!" # 2
    sgirl "Do I really have to?" # 1
    sgirl "You know the rules..." # 3
    sgirl "Okay, I will wear something sexy tomorrow!" # 1
    sgirl "Good girl!" # 2

    sgirl "Next one!" # 4

    $ end_event("new_daytime", **kwargs)


#endregion
####################

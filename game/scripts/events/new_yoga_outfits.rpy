init 1 python: 
    set_current_mod('base')

    new_yoga_outfit_1_event = EventFragment(3, "new_yoga_outfit_1",
        RandomCondition(50, 100),
        LevelCondition("2,3", "school"),
        NOT(ProgressCondition("yoga_classes")),
        Pattern("main", "images/events/new_yoga_outfits/new_yoga_outfit_1/new_yoga_outfit_1 <school_level> <step>.webp"),
        thumbnail = "images/events/new_yoga_outfits/new_yoga_outfit_1/thumbnail.webp")

    pta_discussion_storage.add_event(new_yoga_outfit_1_event)

    new_yoga_outfit_2_event = Event(3, "new_yoga_outfit_2",
        TimeCondition(weekday = "d", daytime = "c"),
        ProgressCondition("yoga_classes", 1),
        Pattern("main", "images/events/new_yoga_outfits/new_yoga_outfit_2/new_yoga_outfit_2 <school_level> <step>.webp"),
        thumbnail = "images/events/new_yoga_outfits/new_yoga_outfit_2/thumbnail.webp")

    new_yoga_outfit_3_event = Event(3, "new_yoga_outfit_3",
        TimeCondition(weekday = "d", daytime = "c"),
        ProgressCondition("yoga_classes", 2),
        Pattern("main", "images/events/new_yoga_outfits/new_yoga_outfit_3/new_yoga_outfit_3 <school_level> <step>.webp"),
        thumbnail = "images/events/new_yoga_outfits/new_yoga_outfit_3/thumbnail.webp")

    gym_events["check_pe"].add_event(new_yoga_outfit_2_event, new_yoga_outfit_3_event)

    new_yoga_outfit_4_event = Event(3, "new_yoga_outfit_4",
        TimeCondition(weekday = "d", daytime = "c"),
        ProgressCondition("yoga_classes", 3),
        TimerCondition("new_yoga_outfit_3", day = 4),
        Pattern("main", "images/events/new_yoga_outfits/new_yoga_outfit_4/new_yoga_outfit_4 <school_level> <step>.webp"),
        thumbnail = "images/events/new_yoga_outfits/new_yoga_outfit_4/thumbnail.webp")

    sb_events["check_class"].add_event(new_yoga_outfit_4_event)

    new_yoga_outfit_5_event = Event(3, "new_yoga_outfit_5",
        TimeCondition(weekday = "d", daytime = "6"),
        ProgressCondition("yoga_classes", 4),
        Pattern("main", "images/events/new_yoga_outfits/new_yoga_outfit_5/new_yoga_outfit_5 <school_level> <step>.webp", "school_level"),
        thumbnail = "images/events/new_yoga_outfits/new_yoga_outfit_5/thumbnail.webp")

    new_yoga_outfit_6_event = Event(3, "new_yoga_outfit_6",
        TimeCondition(weekday = "d", daytime = "f"),
        ProgressCondition("yoga_classes", 5),
        Pattern("main", "images/events/new_yoga_outfits/new_yoga_outfit_6/new_yoga_outfit_6 <school_level> <step>.webp"),
        thumbnail = "images/events/new_yoga_outfits/new_yoga_outfit_6/thumbnail.webp")

    new_yoga_outfit_7_event = Event(3, "new_yoga_outfit_7",
        TimeCondition(weekday = "d", daytime = "f"),
        ProgressCondition("yoga_classes", 6),
        RandomCondition(50, 100),
        TimerCondition("new_yoga_outfit_6", day = 4),
        Pattern("main", "images/events/new_yoga_outfits/new_yoga_outfit_7/new_yoga_outfit_7 <school_level> <step>.webp"),
        thumbnail = "images/events/new_yoga_outfits/new_yoga_outfit_7/thumbnail.webp")

    office_building_general_event.add_event(new_yoga_outfit_5_event, new_yoga_outfit_6_event, new_yoga_outfit_7_event)

    new_yoga_outfit_8_event = Event(3, "new_yoga_outfit_8",
        TimeCondition(weekday = "1", daytime = "2"),
        ProgressCondition("yoga_classes", 7),
        Pattern("main", "images/events/new_yoga_outfits/new_yoga_outfit_8/new_yoga_outfit_8 <school_level> <step>.webp"),
        thumbnail = "images/events/new_yoga_outfits/new_yoga_outfit_8/thumbnail.webp")


    new_yoga_outfit_9_event = Event(3, "new_yoga_outfit_9",
        TimeCondition(weekday = "2", daytime = "3"),
        ProgressCondition("yoga_classes", 8),
        Pattern("main", "images/events/new_yoga_outfits/new_yoga_outfit_9/new_yoga_outfit_9 <school_level> <step>.webp"),
        thumbnail = "images/events/new_yoga_outfits/new_yoga_outfit_9/thumbnail.webp")

    time_check_events.add_event(new_yoga_outfit_8_event, new_yoga_outfit_9_event    )

    new_yoga_outfit_10_event = Event(3, "new_yoga_outfit_10",
        TimeCondition(weekday = "d", daytime = "c"),
        ProgressCondition("yoga_classes", 9),
        TimerCondition("new_yoga_outfit_9", day = 4),
        GameDataSelector("yoga_outfit_set", "yoga_outfit_set", 1),
        Pattern("main", "images/events/new_yoga_outfits/new_yoga_outfit_10/new_yoga_outfit_10 <school_level> <yoga_outfit_set> <step>.webp"),
        thumbnail = "images/events/new_yoga_outfits/new_yoga_outfit_10/thumbnail.webp")

    gym_events["check_pe"].add_event(new_yoga_outfit_10_event)

# PTA: during discussion phase
label new_yoga_outfit_1 (**kwargs):
    $ begin_event(**kwargs)

    $ zoe = get_person_char("staff", "zoe_parker")

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    zoe "I just wanted to announce, that I will be adding yoga classes to the curriculum for physical education."
    zoe "I think it's a great way to relax and stay in shape."
    $ image.show(1)
    headmaster "That's a great idea, Zoe. I'm sure the students will appreciate it."

    $ start_progress("yoga_classes") # 0 -> 1

    $ end_event("new_daytime", **kwargs)

# Gym: Check P.E.
label new_yoga_outfit_2 (**kwargs):
    $ begin_event(**kwargs)

    $ zoe = get_person_char("staff", "zoe_parker")

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    zoe "Alright girls, let's start with some basic poses. Just to get you warmed up."
    $ image.show(1)
    zoe "Remember to breathe and relax. It's not a competition."
    $ image.show(2)
    zoe "Just do what you can and don't push yourself too hard. When you force your body to do things it can't, you can get hurt."
    zoe "And that's the last thing we want."
    $ image.show(3)
    zoe "So let's start with the mountain pose. Stand up straight, feet together, arms at your sides."
    $ image.show(4)
    zoe "Like this. This Pose is great for your posture and it helps you to relax. So we'll use it as a warmup."
    
    call Image_Series.show_image(image, 5, 6, 7) from _call_show_image_new_yoga_outfit_2_event_1
    headmaster_thought "Hmm Zoe seems to be quite knowledgeable about yoga. I wonder if she practices it herself."

    $ advance_progress("yoga_classes") # 1 -> 2

    $ end_event("new_daytime", **kwargs)

# Gym: Check P.E.
label new_yoga_outfit_3 (**kwargs):
    $ begin_event(**kwargs)

    $ zoe = get_person_char("staff", "zoe_parker")
    $ sakura = get_person_char("students", "sakura_mori")

    $ image = convert_pattern("main", **kwargs)

    # scene with classes and zoe doing yoga
    # but the students are struggling a bit in their general sport uniforms

    $ image.show(0)
    zoe "Come on! Deeper stretch!"
    $ image.show(1)
    zoe "Deeper!"
    $ image.show(2)
    sakura "I'm trying!"
    $ image.show(3)
    zoe "Come on! You can do it!"
    $ image.show(2)
    sakura "The uniform is too tight!"
    $ image.show(3)
    zoe "Ah I feared that."

    # zoe notices you
    $ image.show(4)
    zoe "Ahh!"

    $ image.show(5)
    zoe "Keep stretching girls. I'll have a quick talk with Mr. [headmaster_last_name]."
    zoe "I'll be right back."
    
    $ image.show(6)
    zoe "Mr. [headmaster_last_name], can I have a word with you?"
    $ image.show(7)
    headmaster "Hm? Oh, Zoe. What's up?"
    $ image.show(8)
    zoe "I was thinking about the yoga classes."
    zoe "The students are doing great and they really like it, but I think they could use some new outfits."
    $ image.show(9)
    headmaster "New outfits? I thought the current ones were elastic enough."
    $ image.show(10)
    zoe "For the more general stances and for general sport, yes. For more advanced poses they get a bit too tight."
    zoe "Also, I think they could use something more... yoga-like."
    $ image.show(11)
    zoe "And I think new outfits would give them more movement and flexibility."
    $ image.show(12)
    headmaster_thought "I guess the girls would also look more sexy in them. That could help me with my plans."
    $ image.show(13)
    headmaster "Alright, I'll look into it. I'll see what I can find."
    $ image.show(14)
    zoe "Thank you, Mr. [headmaster_last_name]."
    $ image.show(15)
    headmaster "Alright. Oh I think one of your students is in trouble."
    # student a bit tangled up
    $ image.show(16)
    zoe "Hm?"
    $ image.show(17)
    zoe "Oh no! Please excuse me, Mr. [headmaster_last_name]."
    $ image.show(18)
    headmaster "No problem, Zoe."
    $ image.show(19)
    headmaster "I'll see you la... Oh, she's already gone."

    $ set_timer("new_yoga_outfit_3", "today")

    $ advance_progress("yoga_classes") # 2 -> 3 

    $ end_event("new_daytime", **kwargs)

# School Building: Check Classes
label new_yoga_outfit_4 (**kwargs):
    $ begin_event(**kwargs)

    $ seraphina = get_person_char("students", "seraphina_clark")
    $ hatano = get_person_char("students", "hatano_miwa")
    $ elsie = get_person_char("students", "elsie_johnson")

    $ image = convert_pattern("main", **kwargs)

    call Image_Series.show_image(image, 0, 1) from _call_show_image_new_yoga_outfit_4_event_1
    headmaster "Good morning! I'm sorry for the interruption. It won't take long."
    $ image.show(2)
    headmaster "Mrs. Parker has requested new outfits for the yoga classes. So now I'm in the process of picking them."
    headmaster "But I want to make sure that the students are comfortable in them. So I would like to ask for your opinion."
    $ image.show(3) 
    headmaster "I need a few volunteers to try them on and give me some feedback. Who would like to help me out?"
    $ image.show(4)
    hatano "Here! I'll do it!"
    $ image.show(5)
    seraphina "I'll help too!"
    $ image.show(6)
    elsie "I want to try them as well!"
    $ image.show(7)
    headmaster "Thank you all! I have gotten some samples from the supplier. So please come to my office after school."
    $ image.show(8)
    hatano "Will do!"

    $ image.show(9)
    headmaster "Thanks! I'll leave you to your classes now."

    $ advance_progress("yoga_classes") # 3 -> 4

    $ end_event("new_daytime", **kwargs)

# Office Building: Evening
label new_yoga_outfit_5 (**kwargs):
    $ begin_event(**kwargs)

    $ seraphina = get_person_char("students", "seraphina_clark")
    $ hatano = get_person_char("students", "hatano_miwa")
    $ elsie = get_person_char("students", "elsie_johnson")

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    secretary "Mr. [headmaster_last_name], the students you requested are here."
    $ image.show(1)
    headmaster "Thank you. Send them in."
    $ image.show(0)
    secretary "Yes, sir."

    $ image.show(3)
    headmaster "Welcome! Thank you for coming."
    $ image.show(4)
    headmaster "Let's directly get to it. I have the outfits on the table over there."
    $ image.show(3)
    headmaster "I prepared three different sets in various sizes. I'll quickly step out so you can change."
    headmaster "Once you've changed, please call me back in and then we can talk about them."

    $ image.show(5)
    seraphina "Got it!"

    $ image.show(2)
    headmaster "Alright then. I'll be waiting outside."
    # headmaster leaves

    $ image.show(6)
    secretary "Mhh, [headmaster_first_name]. How do you feel about three sweet students changing in your office?"
    $ image.show(7)
    headmaster "I'm a professional, Emiko. I can handle it. But I'm also quite intrigued."
    $ image.show(8)
    secretary "Do you want to see?"
    $ image.show(7)
    headmaster "See what?"
    $ image.show(8)
    secretary "The camera feed."
    $ image.show(9)
    headmaster "The what? Why do you have cameras in my office?"
    $ image.show(10)
    secretary "Well I thought it would be nice to have some souvenirs, in case something interesting happens in there."
    secretary "I wanted to surprise you once it happened, but I guess I can show you now."
    $ image.show(11)
    headmaster "Emiko!"
    $ image.show(12)
    headmaster "Of course I want to see!"
    $ image.show(13)
    secretary "Alright! Sit down next to me. I'll show you."
    
    # secretary shows the camera feed
    call Image_Series.show_image(image, 14, 15, 16, 17) from _call_show_image_new_yoga_outfit_5_event_1
    headmaster "Nice!"
    $ image.show(18)
    secretary "Hihi!"

    $ image.show(19)
    seraphina "Mr. [headmaster_last_name], we're ready!"
    $ image.show(20)
    headmaster "Alright, I'll come in."

    # headmaster comes in
    $ image.show(21)
    headmaster "Alright, let's see how they look on you."
    $ image.show(22)
    headmaster "Oh they look great! How do you feel in them?"
    $ image.show(23)
    hatano "They're really comfortable!"
    $ image.show(24)
    seraphina "I agree! They're really nice!"
    $ image.show(25)
    elsie "I like them too!"
    $ image.show(26)
    headmaster "Great! I'm glad you like them. But let's check out the other sets as well."
    headmaster "Please try on the next set."
    
    $ image.show(27)
    headmaster "I'll step out again."
    # headmaster leaves

    call screen black_screen_text("A few minutes later...")
    hatano "Mr. [headmaster_last_name]!"

    # headmaster comes back in
    $ image.show(28)
    headmaster "So?"
    $ image.show(29)
    elsie "They're a bit more revealing, but they're still comfortable!"
    $ image.show(30)
    seraphina "I like that they're a bit more revealing!"
    $ image.show(31)
    hatano "I like them as well!"

    $ image.show(32)
    headmaster "Great! I'm glad you like them. Let's try the last set."
    headmaster "I'll step out again."
    # headmaster leaves

    call screen black_screen_text("A few minutes later...")
    seraphina "We're ready!"

    # headmaster comes back in
    $ image.show(33)
    headmaster "And what do you think about the last set?"
    $ image.show(34)
    hatano "These are the most comfortable!"
    $ image.show(35)
    seraphina "I think they are a bit basic..."
    $ image.show(36)
    elsie "I think they are quite nice."

    $ image.show(37)
    headmaster "Great! Now that you've tried all three sets, which one do you like the most?"

    $ image.show(38)
    seraphina "I like the second set the best. They're the most comfortable and they look the best!"
    $ image.show(39)
    elsie "The second one is too revealing for me, so I like the third one the most!"
    $ image.show(40)
    hatano "I think the first one is better."

    $ image.show(41)
    headmaster "Hmm, so we have a tie. How about I'll decide which one we'll use then?"
    $ image.show(42)
    seraphina "Sounds good!"
    $ image.show(43)
    elsie "Alright!"
    $ image.show(44)
    hatano "Sure!"

    $ image.show(45)
    $ call_custom_menu_with_text("Okay, which outfit will I choose?", character.headmaster, False,
        ("Option 1", (ValueEffect("yoga_outfit_set", 1), EventEffect("new_yoga_outfit_5.after_decision"))),
        ("Option 2", (ValueEffect("yoga_outfit_set", 2), EventEffect("new_yoga_outfit_5.after_decision"))),
        ("Option 3", (ValueEffect("yoga_outfit_set", 3), EventEffect("new_yoga_outfit_5.after_decision"))),
    **kwargs)
label .after_decision (**kwargs):
    $ yoga_set = get_game_data("yoga_outfit_set")

    headmaster "Okay, I've made my decision."
    if yoga_set == 1:
        headmaster "We'll go with the first set."
        hatano "Awesome!"

    elif yoga_set == 2:
        headmaster "We'll go with the second set."
        elsie "I like that choice!"
        
    elif yoga_set == 3:
        headmaster "We'll go with the third set."
        seraphina "Great!"

    headmaster "Thank you for your help. You can change back now."
    headmaster "I'll then go order the outfits."

    # headmaster leaves the office

    headmaster_thought "Hmm, do we even have the sizes for all the students?"

    headmaster "Emiko, do we have the body sizes for the students in the database?"
    secretary "Let me check that for you."
    secretary "Yes, we have them, but they're a bit outdated."
    headmaster "Hmm, that won't do."

    $ advance_progress("yoga_classes") # 4 -> 5

    $ end_event("new_daytime", **kwargs)

# Office Building: Anytime
label new_yoga_outfit_6 (**kwargs):
    $ begin_event(**kwargs)

    $ zoe = get_person_char("staff", "zoe_parker")

    headmaster "Mrs. Parker!"
    zoe "Yes?"
    headmaster "I was just in the process of ordering the new yoga uniforms you asked for."
    zoe "Oh, great!"
    headmaster "I got a few students together to make a selection and we decided for one, but one problem I found was that the sizes in the database are outdated."
    zoe "Oh, I see."
    headmaster "Since these outfits are skin tight, I want to make sure that they fit perfectly."
    headmaster "So I was thinking that would be a great opportunity to do a general health checkup for the students."
    zoe "That is a great idea!"
    headmaster "The question however is, who will do the checkup? Well I could do it, since I obtained a license for it, to help with my studies."
    zoe "I don't think the girls would be comfortable with that."
    headmaster "I see. Do you have any suggestions?"
    zoe "I don't have a license for it as well, but I know someone we could ask for help."
    zoe "I'm friends with a nurse who works at the hospital in the next town. I could ask her if she could help us out."
    headmaster "That sounds good, but we have to mind the budget."
    zoe "I can ask her, maybe she'll do it for free."
    headmaster "That would be great!"
    zoe "I'll ask her right away."

    $ set_timer("new_yoga_outfit_6", "today")

    $ advance_progress("yoga_classes") # 5 -> 6

    $ end_event("new_daytime", **kwargs)

# Office Building: Anytime
label new_yoga_outfit_7 (**kwargs):
    $ begin_event(**kwargs)

    $ zoe = get_person_char("staff", "zoe_parker")

    zoe "Mr. [headmaster_last_name], I have great news!"
    headmaster "What is it?"
    zoe "The nurse agreed to help us out for free this time!"
    headmaster "That's great!"
    zoe "She'll come by Tuesday next week to do the checkups."
    headmaster "That's perfect!"
    zoe "But she said, if you want to do it more often, we'll have to pay her."
    headmaster "I understand. We'll see how it goes."
    zoe "No problem, Mr. [headmaster_last_name]."

    $ advance_progress("yoga_classes") # 6 -> 7

    $ end_event("new_daytime", **kwargs)

# Day Check: Monday - Morning
label new_yoga_outfit_8 (**kwargs):
    $ begin_event(**kwargs)

    headmaster "Good morning class."
    headmaster "I want to announce, that we will be conducting a general health checkup for the students tomorrow during second class."
    headmaster "Attendance is mandatory, so please make sure to be in the gym by that time."
    headmaster "Thank you."

    $ advance_progress("yoga_classes") # 7 -> 8

    $ end_event("new_daytime", **kwargs)

# Day Check: Tuesday - Early Noon
label new_yoga_outfit_9 (**kwargs):
    $ begin_event(**kwargs)

    $ nurse = Character("Nurse", kind = character.vendor, retain = False)
    $ yuriko = get_person_char("staff", "yuriko_oshima")

    headmaster "Good morning everyone!"
    headmaster "I want to introduce you to Nurse [nurse_last_name]. She will be conducting the health checkups today."
    headmaster "These checkups are to make sure that you're all healthy and fit."
    headmaster "Please follow her instructions and answer her questions truthfully."
    headmaster "For these checkups, you will have to take off your clothes, so the nurse can do a thorough examination."

    yuriko "What we have to get naked in front of you!?"

    headmaster "No, please rest assured, I'm just here to make the announcement."
    headmaster "I will be leaving shortly, so you can rest assured that your privacy is protected."

    headmaster "Mrs. [nurse_last_name] is a trained professional and she will treat you with the utmost respect."
    headmaster "If you have any questions or concerns, please don't hesitate to ask her."

    headmaster "Alright, I'll now leave you in her capable hands. Good luck!"
    nurse "Thank you, Mr. [headmaster_last_name]."
    nurse "Now please everyone, take off your clothes and stand in line."
    # headmaster leaves

    call screen black_screen_text("A few hours later...")

    nurse "Mr. [headmaster_last_name], I have finished the checkups."
    headmaster "That's great! How are my students doing?"
    nurse "For the most part, they're doing great. But I have some concerns about a few of them."
    nurse "It is nothing serious and I already talked to them about it. I think you need to be doing these checkups more often."
    nurse "Otherwise I'm worried, that any creeping health issues might be overlooked."
    headmaster "I understand. Would you be willing to come by more often?"
    nurse "I would, but I can't do it that often, and I would have to charge you for it."
    nurse "I have quite a long commute to get here, and I have to take time off from my regular job."
    nurse "As far as I understood from what zoe told me, you have a license yourself. Why don't you do it?"
    headmaster "I thought about it myself, but I worry the students wouldn't be comfortable with it."
    nurse "Hmm, I understand, but I think health comes first. I can come by once in a while, but I think it would be best, if you hire a school nurse."
    headmaster "I understand. I'll see what I can do."
    headmaster "Until then, I have your number, and I thank you for your help."
    nurse "No problem, Mr. [headmaster_last_name]."
    nurse "I'll be on my way then. Have a great day!"
    nurse "Oh and I left the checkup results with your secretary."
    headmaster "Thank you! Have a great day!"

    # headmaster leaves office
    headmaster "Emiko, can you please bring me the checkup results?"
    secretary "Sure, I'll have it in a minute."
    secretary "Here you are [headmaster_first_name]."
    headmaster "Thank you!"
    headmaster "Now let's see, what we have here."
    headmaster "Oh the nurse really did a thorough job. I'm impressed."
    headmaster "Didn't expect her to also make photos of the students."
    # headmaster goes through all the results
    headmaster "So far so good."
    headmaster "Now that that's done, I finally can order the new yoga outfits."
    headmaster "And concerning the health checkups, I guess I have to talk with the PTA about that."

    $ set_timer("new_yoga_outfit_9", "today")

    $ advance_progress("yoga_classes") # 8 -> 9

    $ end_event("new_daytime", **kwargs)

# Gym: Check P.E.
label new_yoga_outfit_10 (**kwargs):
    $ begin_event(**kwargs)

    $ zoe = get_person_char("staff", "zoe_parker")
    $ miwa = get_person_char("students", "miwa_igarashi")

    headmaster "Good morning class."
    headmaster "I have great news!"
    headmaster "The new yoga outfits have arrived!"

    zoe "That's great!"
    headmaster "I want to thank you all for your patience."
    zoe "How about you girls quickly go and try them on?"
    headmaster "That's a great idea!"

    zoe "Wow! You all look great!"
    zoe "How do they feel?"

    miwa "They're great!"
    headmaster "I'm glad to hear that! I hope you enjoy using them."

    zoe "Then let's quickly put them to use!"

    # class processes with the yoga class

    $ advance_progress("yoga_classes") # 9 -> 10

    $ end_event("new_daytime", **kwargs)

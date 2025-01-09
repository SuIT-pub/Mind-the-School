init 1 python: 
    set_current_mod('base')  

    office_building_events["call_secretary"].add_event(Event(1, "office_call_secretary_1",
        NOT(ProgressCondition('start_sex_ed')),
        ProgressCondition('aona_sports_bra', '2+'),
        LevelCondition('secretary', 6),
        TimeCondition(daytime = "6-"),
        Pattern("main", "images/events/office/office_call_secretary_1/<step>.webp"),
    )

    office_building_events["call_secretary"].add_event(
        office_call_secretary_1_event,
    )

    office_teacher_sex_ed_introduction_1_event = Event(1, "office_teacher_sex_ed_introduction_1",
        ProgressCondition('start_sex_ed', 1),
        TimeCondition(daytime = "f", day = "d"),
    )

    office_teacher_sex_ed_introduction_3_event = Event(1, "office_teacher_sex_ed_introduction_3",
        ProgressCondition('start_sex_ed', 3),
        TimeCondition(daytime = "6-"),
    )

    office_building_events["work"].add_event(
        Event(1, "office_teacher_sex_ed_introduction_1",
            ProgressCondition('start_sex_ed', 1),
            TimeCondition(daytime = "d", weekday = "d"),
            Pattern("main", "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_1/office_teacher_sex_ed_introduction_1 <step>.webp"),
            thumbnail = "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_1/office_teacher_sex_ed_introduction_1 4.webp",
        ),
        Event(1, "office_teacher_sex_ed_introduction_3",
            ProgressCondition('start_sex_ed', 3),
            TimeCondition(daytime = "d"),
            Pattern("main", "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_3/office_teacher_sex_ed_introduction_3 <step>.webp"),
            thumbnail = "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_3/office_teacher_sex_ed_introduction_3 3.webp",
        )
    )

    temp_time_check_events.add_event(Event(1, "office_teacher_sex_ed_introduction_2",
        ProgressCondition('start_sex_ed', 2),
        EventSeenCondition(),
        TimeCondition(daytime = "1", weekday = "1-4"),
        Pattern("main", "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_2/office_teacher_sex_ed_introduction_2 <step>.webp"),
        thumbnail = "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_2/office_teacher_sex_ed_introduction_2 4.webp",

    ))

    office_building_events["schedule_meeting"].add_event(Event(1, "office_teacher_sex_ed_introduction_4",
        ProgressCondition('start_sex_ed', 4),
        TimeCondition(daytime = "f", weekday = "d"),
        Pattern("main", "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_4/office_teacher_sex_ed_introduction_4 <step>.webp"),
        thumbnail = "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_4/office_teacher_sex_ed_introduction_4 4.webp",
    ))

    # PTA discussions
    pta_discussion_storage.add_event(EventFragment(1, "pta_discussion_sex_ed_intro_1",
        ProgressCondition('start_sex_ed', 5),
        Pattern("main", "images/events/sex_ed_intro/pta_discussion_sex_ed_intro_1/pta_discussion_sex_ed_intro_1 <step>.webp"),
        thumbnail = "images/events/sex_ed_intro/pta_discussion_sex_ed_intro_1/pta_discussion_sex_ed_intro_1 10.webp",
    ))

    pta_vote_storage.add_event(EventFragment(2, "pta_vote_theoretical_sex_ed_1",
        JournalVoteCondition("theoretical_sex_ed"),
        Pattern("main", "images/events/sex_ed_intro/pta_vote_theoretical_sex_ed_1/pta_vote_theoretical_sex_ed_1 <step>.webp"),
        thumbnail = "images/events/sex_ed_intro/pta_vote_theoretical_sex_ed_1/pta_vote_theoretical_sex_ed_1 10.webp",
    ))

    temp_time_check_events.add_event(Event(1, "theoretical_sex_ed_assembly_1",
        ProgressCondition('start_sex_ed', 7),
        TimeCondition(daytime = "6", weekday = "5"),
        Pattern("main", "images/events/sex_ed_intro/theoretical_sex_ed_assembly_1/theoretical_sex_ed_assembly_1 <step>.webp")),
    )

    courtyard_general_event.add_event(
        Event(3, "sex_ed_intro_mini_courtyard_1",
            ProgressCondition('start_sex_ed', 8),
            TimeCondition(daytime = "d", weekday = "w"),
            EventSeenCondition(),
            PriorityOption(99),
            ForceHighlightOption(),
            Pattern("main", "images/events/sex_ed_intro/mini_courtyard_1/mini_courtyard_1 <step>.webp")),
    )
    sd_general_event.add_event(
        Event(3, "sex_ed_intro_mini_sd_1",
            ProgressCondition('start_sex_ed', 8),
            TimeCondition(daytime = "d", weekday = "w"),
            EventSeenCondition(),
            PriorityOption(99),
            ForceHighlightOption(),
            Pattern("main", "images/events/sex_ed_intro/mini_sd_1/mini_sd_1 <step>.webp")),
        Event(3, "sex_ed_intro_mini_sd_2",
            ProgressCondition('start_sex_ed', 8),
            TimeCondition(daytime = "d", weekday = "w"),
            EventSeenCondition(),
            PriorityOption(99),
            ForceHighlightOption(),
            Pattern("main", "images/events/sex_ed_intro/mini_sd_2/mini_sd_2 <step>.webp")),
    )
    temp_time_check_events.add_event(
        Event(1, "first_sex_ed_day",
            ProgressCondition('start_sex_ed', 8),
            TimeCondition(daytime = 1, weekday = 1),
            Pattern("main", "images/events/sex_ed_intro/first_sex_ed_day/first_sex_ed_day <step>.webp"),
        ),
        Event(1, "first_sex_ed_class_1",
            ProgressCondition('start_sex_ed', 8),
            TimeCondition(daytime = 2, weekday = 1),
            Pattern("main", "images/events/sex_ed_intro/first_sex_ed_class_1/first_sex_ed_class_1 <step>.webp"),
        ),
    )


##############################
# region Sex Ed Introduction #

# region main events

label office_call_secretary_1 (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You call the secretary."
    secretary "Hello, [headmaster_first_name]. How can I help you?"
    headmaster "I need your opinion on something."
    secretary "Sure, what is it?"
    headmaster "I'm thinking of introducing sex education classes in the curriculum. What do you think?"
    secretary "I think it's a great idea. It's important for students to be educated about such topics."
    secretary "But do you think the rest of the staff and also the students would agree?"
    $ image.show(8)
    headmaster """
    Hmm, I guess you're right. That will be quite the hurdle, I think I need to make sure they are ready 
    for it before suggesting it.
    """
    $ image.show(9)
    headmaster "Do you have any suggestions on how to approach this?"
    secretary "I think you should start by talking to the staff and getting their input."
    secretary """
    To actually convince them, you could prepare some teaching material and introductory material on the subject.
    """
    secretary "That way they can see what you have in mind and how you plan to approach it."
    headmaster "That's a good idea. Thank you for your input."
    secretary "You're welcome. Is there anything else?"
    headmaster "No, that's all. Thank you."
    secretary "You're welcome. Have a nice day."
    headmaster_thought "Then, maybe I should start work on some teaching material for the sex ed classes."

    $ start_progress('start_sex_ed') # 0 -> 1

    $ end_event('new_daytime', **kwargs)

label office_teacher_sex_ed_introduction_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster_thought "Hmm, now how do I start this."
    headmaster_thought "My main problem is that the teacher will have reservations about introducing sex ed classes."
    headmaster_thought "So the best way to overcome this, would be to show them the importance of it."
    $ image.show(1)
    headmaster_thought """
    I guess I should talk to them and present them the effects of not giving the students proper sexual education.
    """
    headmaster_thought "If I can relate to them in their own expertise, I guess that would be even better."

    $ image.show(2)
    headmaster "Emiko?"
    $ image.show(3)
    secretary "Yes, [headmaster_first_name]?"
    $ image.show(4)
    if time.get_weekday_num() > 3 or time.get_weekday_num() < 7:
        headmaster "Can you please schedule a meeting with all the teachers for tomorrow?"
    else:
        headmaster "Can you please schedule a meeting with all the teachers for monday?"
    $ image.show(5)
    secretary "Sure, I'll take care of it. At what time?"
    $ image.show(6)
    headmaster "First thing in the morning. I want to discuss the introduction of the sex ed classes with them."
    $ image.show(5)
    secretary "Got it. I'll send out the invites right away."
    $ image.show(4)
    headmaster "Thank you, Emiko."

    $ advance_progress('start_sex_ed') # 1 -> 2

    $ end_event('new_daytime', **kwargs)

label office_teacher_sex_ed_introduction_2 (**kwargs):
    $ begin_event(**kwargs)

    $ finola = get_person("staff", "finola_ryan").get_character()
    $ chloe  = get_person("staff", "chloe_garcia").get_character()
    $ lily   = get_person("staff", "lily_anderson").get_character()
    $ yulan  = get_person("staff", "yulan_chen").get_character()
    $ zoe    = get_person("staff", "zoe_parker").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster """
    I thank you all for coming on such short notice.

    Since I became the new headmaster, I was closely observing the school and the students.

    The school is nothing short but disappointing and the students and their achievements are a direct image of that.
    """
    $ image.show(1)
    headmaster """
    But what shocked me most was the social behaviour of the students.
    
    The students are surprisingly tame. But when it comes to their behaviour related to their bodies and looks, 
    they are quite the opposite.
    """
    $ image.show(2)
    headmaster """
    I heard of bullying and exclusion towards certain students because of their looks or their overall body form.
    I think that this is a direct result of the lack of proper sexual education.
    """
    $ image.show(3)
    headmaster """
    The students became too ignorant. I think they simply don't know why bodies are different and why they are changing.
    
    So they did what most people do when they don't understand something. They fear it. 
    And in conclusion they bully or fight it.
    
    I think that we need to change that. We need to educate the students about their bodies and the bodies of others.
    """
    $ image.show(4)
    headmaster "And for that reason I plan to add Sexual Education to the schools curriculum."
    
    $ image.show(5)
    finola """
    I disagree. I believe that sexual education is not something that should be taught in school. 
    It is a private matter between adults!
    """

    $ image.show(6)
    headmaster """
    I appreciate your concerns, but we cannot ignore the fact that our students are going through puberty and they 
    need to know how their bodies work.
    """

    $ image.show(7)
    headmaster """
    We will provide them with accurate information about sex and relationships without promoting any particular sexual 
    orientation or gender identity.
    """

    $ image.show(8)
    chloe "But what if some of our students get too excited during the lessons? It's completely inappropriate!"

    $ image.show(9)
    headmaster """
    I agree that we need to be sensitive to their emotions, but I am certain that this will only enhance their 
    understanding of sexuality and relationships.

    My research on other schools that have implemented similar programmes has shown that they have seen positive 
    results in terms of decreased rates of teen pregnancy, STIs and sexual assault.
    """

    $ image.show(10)
    lily "But it'll make our students more promiscuous!"

    $ image.show(11)
    headmaster """
    That's a common misconception about sex education. Research has shown that teaching young people about sexual 
    health can actually prevent them from engaging in risky behaviour.
    
    We can empower our students to make informed decisions about their bodies and relationships by providing accurate 
    information and setting clear boundaries.
    """

    $ image.show(12)
    yulan """
    We have to consider the possibility that some students won't be interested. I want to know if they will be forced 
    to attend these classes.
    """

    $ image.show(13)
    headmaster """
    Yes. This subject will be added to the normal curriculum. This is a topic that simply cannot be made optional.

    It is our duty to provide all students with accurate information so that they can make informed choices about their bodies and relationships.
    """

    $ image.show(14)
    zoe "I'm not fully convinced. But what if some students don't listen and still engage in risky behaviour?"

    $ image.show(1)
    headmaster """
    That's a valid concern, but we will provide them with accurate information so that they can make informed choices 
    about their bodies.

    If they choose to engage in risky behaviour despite this knowledge, they will have to take responsibility for their 
    actions.

    We will do our best to provide them with the necessary tools and resources.
    """

    $ image.show(2)
    headmaster """
    I understand that this is a sensitive topic, but I believe that it is our responsibility to provide our students 
    with the knowledge and skills they need to make informed decisions about their bodies and relationships.

    We are running out of time, so I have a proposal.

    I will work out a plan for the introduction of the new subject.

    I'll include the specific topics that will be covered, the teaching methods that will be used, and the resources 
    that will be available to the students.
    """

    $ image.show(3)
    headmaster """
    I will then present this plan to you all for your feedback and suggestions.

    I want to make sure that we are all on the same page and that we can move forward together.
    """

    $ image.show(5)
    finola "I still have my doubts, but I'm willing to give it a chance."
    $ image.show(8)
    chloe "Yeah, let's see what you come up with."

    $ image.show(0)
    headmaster "Thank you all for your time. I'll keep you updated on the progress."

    $ advance_progress('start_sex_ed') # 2 -> 3

    $ end_event('new_daytime')

label office_teacher_sex_ed_introduction_3 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster_thought """
    Now let's start working on the information material for the teachers. 
    This needs to be perfect, so the teachers will be convinced.

    So what do I need to include in the material?
    """

    $ image.show(1)
    headmaster_thought """
    I think I should start with the basics. What is sexual education and why is it important?

    Add some case studies and statistics to show the impact of sexual education on students.

    And maybe some examples of how other schools have successfully implemented sexual education programs.
    """

    $ image.show(2)
    headmaster_thought """
    Then continue with the topics that will be covered in the classes and the teaching methods that will be used.

    That will include the resources that will be available to the students and the teachers.
    """

    $ image.show(3)
    headmaster_thought """
    And finally, I should include a section on how the teachers can support the students and answer their questions.

    I think that should cover everything. Now I just need to put it all together.
    """
    call screen black_screen_text("1h later.")

    $ image.show(4)
    headmaster_thought "Now that's done. I think I should present it to the teachers and get their feedback."
    
    $ advance_progress('start_sex_ed') # 3 -> 4

    $ end_event('new_daytime', **kwargs)

label office_teacher_sex_ed_introduction_4 (**kwargs):
    $ begin_event(**kwargs)

    $ finola = get_person("staff", "finola_ryan").get_character()
    $ chloe  = get_person("staff", "chloe_garcia").get_character()
    $ lily   = get_person("staff", "lily_anderson").get_character()
    $ yulan  = get_person("staff", "yulan_chen").get_character()
    $ zoe    = get_person("staff", "zoe_parker").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster """
    Good morning! Today, I would like to present to you the importance of sexual education and the comprehensive 
    program we are planning to implement.
    """
    $ image.show(1)
    headmaster """
    I understand that there may be concerns and reservations about introducing this topic, but I believe it is crucial 
    for the well-being and development of our students.

    I already prepared some information material for you to review and provide feedback on.
    """
    $ image.show(2)
    headmaster "Let's start with the basics. What is sexual education and why is it important?"

    call screen black_screen_text("15 Minutes later.")

    headmaster "Without proper sexual education, students may rely on misinformation or peer pressure, which can lead to risky behaviors and negative consequences."

    call screen black_screen_text("15 Minutes later.")

    headmaster "These case studies and statistics demonstrate the effectiveness of sexual education in promoting healthy behaviors and reducing negative outcomes."

    call screen black_screen_text("15 Minutes later.")

    headmaster "Now, let's talk about the resources that will be available to both the students and the teachers."

    call screen black_screen_text("15 Minutes later.")

    headmaster "Your support and guidance will be instrumental in addressing their concerns and providing accurate information, even with limited resources."

    call .end_presentation (**kwargs) from call_end_presentation_sex_ed_intro_1
label .skipped_presentation (**kwargs):

    call screen black_screen_text("30 Minutes later.")

    call .end_presentation (**kwargs) from call_end_presentation_sex_ed_intro_2
label .end_presentation (**kwargs):

    $ image.show(7)
    headmaster """
    By working together and making the most of what we have, we can ensure that our students receive the necessary 
    knowledge and skills to make informed decisions and navigate their sexual health and relationships.

    Thank you for your attention. I hope that this presentation has addressed some of your concerns and that we can 
    move forward together in implementing comprehensive sexual education.
    """
    
    $ image.show(8)
    finola """
    Thank you for the presentation, Headmaster. I can see the potential benefits of sexual education, 
    but I would like some time to think about it and discuss it with my colleagues.
    """
    $ image.show(9)
    chloe """
    I agree. It's an important topic, but we need to consider the concerns of parents and the community as 
    well. Perhaps you could bring it up at the next PTA meeting and gather more feedback.
    """
    $ image.show(10)
    lily """
    I appreciate the effort you've put into this presentation, Headmaster. However, I think it would be 
    beneficial to involve parents in the decision-making process. Let's discuss it further at the next PTA meeting.
    """
    $ image.show(11)
    yulan """
    I'm impressed with the research and success stories you've shared, Headmaster. However, 
    I believe it's important to address any potential backlash or resistance from parents. 
    Let's bring it up at the next PTA meeting and have a thorough discussion.
    """
    $ image.show(12)
    zoe """
    Thank you for the detailed presentation, Headmaster. I can see the value of sexual education, but I think it's 
    important to involve parents and the students in the decision-making process. 
    Let's discuss it further at the next PTA meeting.
    """

    $ image.show(13)
    headmaster """
    Thank you for your feedback. That will be all for today then.

    I wish you all a good day and we'll see each other at the next PTA meeting.
    """
    
    # headmaster returns to office, secretary enters

    $ image.show(14)
    secretary "[headmaster_first_name], how did the presentation go?"
    $ image.show(15)
    headmaster "It went well. The teachers had some concerns, but I think we're on the right track."
    $ image.show(16)
    headmaster """
    I probably just need to guide their thoughts in the right direction for them to support me at the pta meeting.

    I don't expect much opposition from the student council, so I think we're good.
    """
    $ image.show(17)
    headmaster "The parents should be no problem when the teachers and students agree to the change."

    $ advance_progress('start_sex_ed') # 4 -> 5

    $ end_event('new_daytime', **kwargs)

label pta_discussion_sex_ed_intro_1 (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ finola = get_person("staff", "finola_ryan").get_character()
    $ chloe  = get_person("staff", "chloe_garcia").get_character()
    $ lily   = get_person("staff", "lily_anderson").get_character()
    $ yulan  = get_person("staff", "yulan_chen").get_character()
    $ zoe    = get_person("staff", "zoe_parker").get_character()

    $ adelaide = get_person("parents", "adelaide_hall").get_character()
    $ nubia    = get_person("parents", "nubia_davis").get_character()
    $ yuki     = get_person("parents", "yuki_yamamoto").get_character()

    $ yuriko = get_person("class_3a", "yuriko_oshima").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Nobody? Alright then, I would like to discuss the introduction of sexual education in our curriculum."
    $ image.show(1)
    yuriko "What? No way! That's totally unnecessary!"
    $ image.show(2)
    adelaide "I agree! This is not something that should be taught in school!"
    $ image.show(3)
    headmaster """
    I believe it is important for our students to be educated about this topic. It is crucial for their development and 
    well-being.
    """
    $ image.show(4)
    yuki "But what about the parents? We should be the ones to teach our children about these things!"
    $ image.show(5)
    headmaster """
    I understand your concerns, but many parents may not feel comfortable discussing these topics with their children.
    """
    $ image.show(6)
    headmaster "Also, no offense, but some parents may not have the right information to share with their children."
    $ image.show(7)
    headmaster """
    I may not be at this school for long, but I have seen enough to know that our students are struggling with these 
    issues.
    """
    $ image.show(8)
    chloe """
    With that I have to agree. I normally wouldn't support this, but I can also see the effects of the lack of sexual 
    education.
    """
    $ image.show(9)
    finola "And I think it is the responsibility of all of us to ensure that our students receive accurate information."
    $ image.show(10)
    yuriko "But is it really necessary? That topic is so embarrassing and uncomfortable!"
    $ image.show(11)
    headmaster """
    That is even more reason to teach it! If we don't, our students will rely on misinformation and peer pressure.
    """
    $ image.show(12)
    headmaster """
    This is a topic that cannot be ignored. You students will come across it sooner or later, and you have to know how 
    to deal with it.
    """
    $ image.show(13)
    headmaster """
    And if you don't learn it here, you will learn it from the wrong sources. And that then will become dangerous.
    """
    $ image.show(14)
    yuki "But what if some students get too excited during the lessons? It's completely inappropriate!"
    $ image.show(15)
    headmaster "I understand your concerns, but I assure you that we will handle this topic with sensitivity and care."
    $ image.show(16)
    nubia """
    Alright, I need time to think about this, but I will agree to have it put to vote after some time to consider it.
    """
    $ image.show(17)
    adelaide "I agree."
    $ image.show(18)
    yuki "I guess I can see the benefits, but I still have my doubts."

    $ image.show(19)
    yuriko "Fine! But I still think it's unnecessary!"

    $ image.show(3)
    headmaster "Great! Then let's move onto the next topic."
    
    $ add_notify_message("Added new rule to journal!")

    $ advance_progress('start_sex_ed') # 5 -> 6

    $ end_event('new_daytime', **kwargs)

label pta_vote_theoretical_sex_ed_1 (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ parent_vote =  get_value("vote_parent", **kwargs)
    $ teacher_vote = get_value("vote_teacher", **kwargs)
    $ student_vote = get_value("vote_student", **kwargs)
    $ end_choice = get_end_choice(parent_vote, teacher_vote, student_vote)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster """
    As previously announced, I would like to put to vote the introduction of theoretical sex education in our 
    curriculum.
    """
    $ image.show(1)
    headmaster "We already discussed the importance of this topic and the benefits it can bring to our students."
    $ image.show(2)
    headmaster "Now I hope you have made up your minds and are ready to cast your votes."

    $ image.show(3)
    headmaster "So when there are no further questions, please cast your vote now."

    # teacher comment on vote
    if teacher_vote == 'yes':
        $ image.show(4)
        teacher """
        We teachers had a discussion about this topic and we came to the conclusion that theoretical sex education is 
        important for the students.

        So we support the introduction of this subject in our curriculum.
        """
    else:
        $ image.show(5)
        teacher """
        We teachers discussed this topic and we still have concerns about the introduction, so we will vote against it 
        for now.
        """

    # student comment on vote
    if student_vote == 'yes':
        $ image.show(6)
        sgirl """
        After thinking about it, I believe that it could be beneficial for us besides being embarrassing. So I vote yes.
        """
    else:
        $ image.show(7)
        sgirl "I still think the topic is embarrassing and unnecessary, so I vote no."

    $ image.show(8)
    parent """
    We believe that the introduction of theoretical sex education is not appropriate and should be discussed at home.
    
    For this reason, we vote against the proposal.
    """

    if end_choice == 'yes':
        $ image.show(9)
        headmaster "With the majority of votes in favor, the proposal is accepted."
        headmaster "Theoretical Sexual Education will be introduced into the curriculum."
        $ image.show(10)
        headmaster """
        I will call for a school assembly this evening after classes to inform the students about the change and to 
        distribute information material for the students and faculty members to prepare themselves over the weekend.
        """
        $ advance_progress('start_sex_ed') # 6 -> 7
    else:
        $ image.show(9)
        headmaster "The proposal is rejected due to the majority of votes against it."

    call pta_vote_result(
        "no", teacher_vote, student_vote, get_value("vote_proposal", **kwargs)
    ) from _call_pta_vote_result_theoretical_sex_ed_1

    $ end_event('new_daytime', **kwargs)

label theoretical_sex_ed_assembly_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Good evening, students. I have an important announcement to make."
    $ image.show(1)
    headmaster """
    After a vote by the teachers, students and parents, the proposal to introduce theoretical sex education into the 
    curriculum has been accepted.
    """
    $ image.show(2)
    headmaster "Therefore, starting next week, we will begin the implementation of this subject in your classes."
    $ image.show(3)
    sgirl "*murmurs* I can't believe they actually voted for it."
    $ image.show(4)
    headmaster """
    I understand that this may be a sensitive topic for some of you, but I assure you that we will handle this subject 
    with care and sensitivity.
    """
    $ image.show(5)
    headmaster "We will provide you with accurate information and resources to help you navigate this topic."
    $ image.show(6)
    headmaster "Mrs. Langley! Please distribute the info material to the students and faculty members."
    $ image.show(7)
    headmaster "These will help you prepare for the upcoming lessons and answer any questions you may have."
    $ image.show(8)
    headmaster """
    I ask you to carefully read through the material over the weekend and if you have any questions, please raise those 
    in the next class.
    """

    $ image.show(9)
    headmaster """
    They include the topics that will be covered in the classes and the teaching methods that will be used.

    They include visual material and extra information on the effects and benefits of sexual education.

    I hope they will help you understand the topic and give you inspiration not only for the lessons but also to 
    improve the relationship with your peers.
    """
    $ image.show(10)
    headmaster """
    Next week, we will start with the first lessons. I will be present in the first lesson to answer any questions you 
    may have.
    """
    $ image.show(11)
    headmaster "That will be all for today. I wish you all a good evening and a good weekend."

    $ advance_progress('start_sex_ed') # 7 -> 8

    $ end_event('new_daytime', **kwargs)

# endregion

# region Mini Events

label sex_ed_intro_mini_sd_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You peek through the door."
    $ image.show(1)
    headmaster_thought "Looks like the students are really reading through the material."

    $ end_event('new_daytime', **kwargs)

label sex_ed_intro_mini_sd_2 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster_thought "Hmm? What's that noise?"
    $ image.show(1)
    headmaster_thought "I think it's coming from this room."
    $ image.show(2)
    subtitles "*KNOCK* *KNOCK*"
    $ image.show(3)
    headmaster "Hello? Ah I was wondering where that noise was coming from."
    $ image.show(4)
    sgirl "Oh, hello Headmaster. We're sorry for the noise."
    $ image.show(5)
    headmaster "It's alright. What are you doing?"
    $ image.show(6)
    sgirl "We're modifying our uniforms. The material you gave us had some really cute ideas."
    $ image.show(7)
    headmaster "I'm glad you like it. I'm happy to see you've gotten inspired by it."
    headmaster "But please don't forget to finish reading the material until the end of the weekend."
    $ image.show(8)
    sgirl "Yes Mr. [headmaster_last_name]."
    $ image.show(9)
    headmaster "Great! I'll leave you to it then. Have a good day."

    $ end_event('new_daytime', **kwargs)

# students sitting in courtyard and discussing the material
label sex_ed_intro_mini_courtyard_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You see the students sitting in the courtyard."
    subtitles "They seem to be discussing the material."

    $ end_event('new_daytime', **kwargs)

# endregion

label first_sex_ed_day(**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster_thought "Big day today. The first sexual education class. I hope the students are ready for it."
    $ image.show(1)
    headmaster_thought "Hmm, I see the students are going more chill with their uniforms now. Looks good on them."
    headmaster_thought "Well, I guess I should go to the classroom now."

    $ get_character_by_key("school").set_level(2)
    $ get_character_by_key("parent").set_level(2)
    $ get_character_by_key("teacher").set_level(2)

    call change_stats_with_modifier('school',
        inhibition = DEC_TINY, happiness = TINY
    ) from _call_first_sex_ed_day_1

    $ end_event("new_daytime", **kwargs)

label first_sex_ed_class_1 (**kwargs):
    $ begin_event(**kwargs)

    $ finola = get_person("staff", "finola_ryan").get_character()

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Good morning, today you will have your first class in sexual education."
    $ image.show(1)
    headmaster_thought "Oh wow, even Finola has gotten more relaxed with her outfit. Not much, but it's a start."
    $ image.show(2)
    headmaster "I know many of you are nervous or uncomfortable about this topic, but I assure you it is important."
    headmaster "For that reason I want to make sure to keep this topic as transparent as possible."
    $ image.show(3)
    headmaster "So that is why I am here today. Today will be no normal class, instead I hope you have worked through the material."
    headmaster "If you have, I want you to ask me questions and issues you have with the material or with the topic in general, so we can discuss then together and give you a good introduction."
    $ image.show(4)
    headmaster "So, who has questions?"
    $ image.show(5)
    headmaster "Nobody? Don't be shy."
    $ image.show(6)
    headmaster "Well that actually is a good entry point into why this topic is necessary."
    $ image.show(7)
    headmaster "Sexual education is not only about learning about your bodies and learning how intercourse works."
    headmaster "It is also about learning about relationships, consent, and respect. It is about making informed decisions and understanding your own and others' boundaries."
    headmaster "Learning to recognise what the other person feels comfortable with and what not. Learning about empathy."
    $ image.show(8)
    headmaster "My aim is to help you have healthier relationships with each other. That way everyone will have a happier life."
    headmaster "So with that, does anyone want to ask a question?"
    $ image.show(9)
    headmaster "No? Would you rather we collect answers anonymously and discuss them together?"
    $ image.show(10)
    subtitles "*energetic nodding from the students*"
    $ image.show(11)
    headmaster "Alright. Then please prepare a few questions. I will collect them in 10 minutes and then we will go through them one by one."
    call screen black_screen_text("10 minutes later.")
    $ image.show(12)
    headmaster "Alright, let's see what you have prepared."
    $ image.show(13)
    headmaster "Let's start with the first question."

    $ image.show(14)
    headmaster "\"What is consent?\""
    $ image.show(15)
    headmaster "That is a good question. Consent can become a complex topic as it is not only about saying yes or no. For that reason you will learn more about it in future lessons."
    headmaster "But basically it is about making sure that all parties agree to any activity and that it's important to communicate clearly and respect each other's boundaries."
    $ image.show(16)
    headmaster "Miss Ryan, do you take notes, so you know what topics to prioritize in the future?"
    $ image.show(17)
    finola "Yes, Mr. [headmaster_last_name]. I'm already on it."
    $ image.show(18)
    headmaster "Excellent!"
    headmaster "Then let's move on to the next question."

    $ image.show(14)
    headmaster "\"What are the types of birth control?\""
    $ image.show(19)
    headmaster "That is a good question. There are many types of birth control, such as condoms, birth control pills, and intrauterine devices."
    headmaster "But all of them have certain aspects that have to be considered. Some of them also should be discussed with the partner because of them."
    headmaster "That topic will be covered in future lessons as well for that reason."
    headmaster "Next question!"

    $ image.show(14)
    headmaster "\"Is it normal to feel nervous about these topics?\""
    $ image.show(15)
    headmaster "Absolutely! It is completely normal to feel nervous or uncomfortable about these topics. It is a sensitive topic and it is okay to feel that way."
    headmaster "Moreover, until now you have not been taught about these topics and have been kept afar from them. So it is not only normal, but also expected."
    headmaster "One more reason for us to be doing this, since you will come across these topics sooner or later. So better to be prepared."

    $ image.show(14)
    headmaster "\"How can I build self-confidence and self-respect?\""
    $ image.show(19)
    headmaster "That is a good question. Building self-confidence and self-respect is an important part of sexual education."
    headmaster "To build self-confidence it helps to put yourself in situations where you can succeed and to set realistic goals for yourself."
    headmaster "But it is also important to put yourself in situations where you can fail and learn from it. Or put yourself in uncomfortable situations, try out new things."
    headmaster "Be a bit more daring and try out new things. For example wearing something more daring and seeing how you feel about it."

    $ image.show(14)
    headmaster "\"What should I do if I have questions about my own body?\""
    $ image.show(15)
    headmaster "You can just come talk to me or your teachers. We will help you as good as we can. I also hold counselling sessions."
    headmaster "There you can come talk to me for any problems or insecurities you have. It's all confidential and I will help you as good as I can."
    headmaster "If you want or need some counselling, just talk to my Secretary Ms. Langley and she will schedule an appointment for you."
    headmaster "Okay, we don't have much time left. So let's take one more question."

    $ image.show(14)
    headmaster "\"What is masturbation?\""
    $ image.show(20)
    headmaster "Oh wow, I guess lessons are really needed for you."
    $ image.show(21)
    headmaster "But that is a really good and important question. Masturbation is a normal and healthy part of human sexuality."
    headmaster "It is a way to explore your body and learn what feels good to you. It is also a way to relieve stress and tension."
    $ image.show(22)
    headmaster "Since it is the first lessons, I won't dive too deep into it."
    $ image.show(23)
    headmaster "But Masturbation is the practice of touching or rubbing your own genitals for sexual pleasure."
    $ image.show(24)
    headmaster "There are many ways of doing it and it is completely normal and healthy."
    headmaster "You should not feel ashamed about it and actually try it out. It is an important part of your sexual development."
    $ image.show(25)
    headmaster "Mrs. Ryan, you masturbate, don't you?"
    $ image.show(26)
    finola "Mr. [headmaster_last_name]!"
    $ image.show(27)
    finola "..."
    $ image.show(28)
    finola "Yes, I do."
    $ image.show(29)
    headmaster "See, even Mrs. Ryan does it. So it is completely normal and healthy."
    $ image.show(30)
    headmaster "Now since I am male and Mrs. Ryan isn't. Please direct your questions about masturbation to her."
    $ image.show(31)
    headmaster "But that is all for today. I hope you have a good day and I hope you learned something new today."
    
    call change_stats_with_modifier('school',
        education = MEDIUM, inhibition = DEC_SMALL, corruption = SMALL, happiness = TINY
    ) from _call_first_sex_ed_class_1_1

    $ end_event('new_daytime', **kwargs)


# endregion
##############################

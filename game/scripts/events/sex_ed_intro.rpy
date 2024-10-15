init 1 python: 
    set_current_mod('base')  

    office_building_events["call_secretary"].add_event(Event(1, "office_call_secretary_1",
        NOT(ProgressCondition('start_sex_ed')),
        ProgressCondition('aona_sports_bra', '2+'),
        LevelCondition('secretary', 6),
        TimeCondition(daytime = "d"),
        Pattern("main", "images/events/sex_ed_intro/office_call_secretary_1/<step>.webp"),
        thumbnail = "images/events/sex_ed_intro/office_call_secretary_1/7.webp",
    ))

    office_building_events["work"].add_event(
        Event(1, "office_teacher_sex_ed_introduction_1",
            ProgressCondition('start_sex_ed', 1),
            TimeCondition(daytime = "f", day = "d"),
            Pattern("main", "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_1/<step>.webp"),
            thumbnail = "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_1/4.webp",
        ),
        Event(1, "office_teacher_sex_ed_introduction_3",
            ProgressCondition('start_sex_ed', 3),
            TimeCondition(daytime = "d"),
            Pattern("main", "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_3/<step>.webp"),
            thumbnail = "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_3/3.webp",
        )
    )

    office_building_timed_event.add_event(Event(1, "office_teacher_sex_ed_introduction_2",
        ProgressCondition('start_sex_ed', 2),
        TimeCondition(daytime = "1", day = "1-4"),
        Pattern("main", "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_2/<step>.webp"),
        thumbnail = "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_2/4.webp",

    ))

    office_building_events["schedule_meeting"].add_event(Event(1, "office_teacher_sex_ed_introduction_4",
        ProgressCondition('start_sex_ed', 4),
        TimeCondition(daytime = "f", day = "d"),
        Pattern("main", "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_4/<step>.webp"),
        thumbnail = "images/events/sex_ed_intro/office_teacher_sex_ed_introduction_4/4.webp",
    ))

    # PTA discussions
    pta_discussion_storage.add_event(EventFragment(2, "pta_discussion_sex_ed_intro_1",
        ProgressCondition('start_sex_ed', 5),
        Pattern("main", "images/events/sex_ed_intro/pta_discussion_sex_ed_intro_1/<step>.webp"),
        thumbnail = "images/events/sex_ed_intro/pta_discussion_sex_ed_intro_1/10.webp",
    ))

    pta_vote_storage.add_event(EventFragment(2, "pta_vote_theoretical_sex_ed_1",
        JournalVoteCondition("theoretical_sex_ed"),
        Pattern("main", "images/events/sex_ed_intro/pta_vote_theoretical_sex_ed_1/<step>.webp"),
        thumbnail = "images/events/sex_ed_intro/pta_vote_theoretical_sex_ed_1/10.webp",
    ))



##############################
# region Sex Ed Introduction #

label office_call_secretary_1 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You call the secretary."

    call Image_Series.show_image(image, 1, 2, 3) from _call_show_image_office_call_secretary_1_1
    secretary "Hello, [headmaster_first_name]. How can I help you?"
    $ image.show(4)
    headmaster "I need your opinion on something."
    $ image.show(3)
    secretary "Sure, what is it?"
    $ image.show(5)
    headmaster "I'm thinking of introducing sex education classes in the curriculum. What do you think?"
    $ image.show(6)
    secretary "I think it's a great idea. It's important for students to be educated about such topics."
    $ image.show(7)
    secretary "But do you think the rest of the staff and also the students would agree?"
    $ image.show(8)
    headmaster "Hmm, I guess you're right. That will be quite the hurdle, I think I need to make sure they are ready for it before suggesting it."
    $ image.show(9)
    headmaster "Do you have any suggestions on how to approach this?"
    $ image.show(10)
    secretary "I think you should start by talking to the staff and getting their input."
    secretary "To actually convince them, you could prepare some teaching material and introductory material on the subject."
    secretary "That way they can see what you have in mind and how you plan to approach it."
    $ image.show(11)
    headmaster "That's a good idea. Thank you for your input."
    $ image.show(12)
    secretary "You're welcome. Is there anything else?"
    $ image.show(11)
    headmaster "No, that's all. Thank you."
    $ image.show(13)
    secretary "You're welcome. Have a nice day."
    $ image.show(14)
    headmaster_thought "Then, maybe I should start work on some teaching material for the sex ed classes."

    $ start_progress('start_sex_ed') # 0 -> 1

    $ end_event('new_daytime', **kwargs)

label office_teacher_sex_ed_introduction_1(**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster_thought "Hmm, now how do I start this."
    headmaster_thought "My main problem is that the teacher will have reservations about introducing sex ed classes."
    headmaster_thought "So the best way to overcome this, would be to show them the importance of it."
    $ image.show(1)
    headmaster_thought "I guess I should talk to them and present them the effects of not giving the students proper sexual education."
    headmaster_thought "If I can relate to them in their own expertise, I guess that would be even better."

    $ image.show(2)
    headmaster "Emiko?"
    $ image.show(3)
    secretary "Yes, [headmaster_first_name]?"
    $ image.show(4)
    if time.get_weekday() > 3 or time.get_weekday() < 7:
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

    $ finola = Character("Finola Ryan",   kind = character.teacher)
    $ chloe  = Character("Chloe Garcia",  kind = character.teacher)
    $ lily   = Character("Lily Anderson", kind = character.teacher)
    $ yulan  = Character("Yulan Chen",    kind = character.teacher)
    $ zoe    = Character("Zoe Parker",    kind = character.teacher)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "I thank you all for coming on such short notice."
    headmaster "Since I became the new headmaster, I was closely observing the school and the students."
    headmaster "The school is nothing short but disappointing and the students and their achievements are a direct image of that."
    $ image.show(1)
    headmaster "But what shocked me most was the social behaviour of the students."
    headmaster "The students are surprisingly tame. But when it comes to their behaviour related to their bodies and looks, they are quite the opposite."
    $ image.show(2)
    headmaster "I heard of bullying and exclusion towards certain students because of their looks or their overall body form."
    headmaster "I think that this is a direct result of the lack of proper sexual education."
    $ image.show(3)
    headmaster "The students became too ignorant. I think they simply don't know why bodies are different and why they are changing."
    headmaster "So they did what most people do when they don't understand something. They fear it. And in conclusion they bully or fight it."
    headmaster "I think that we need to change that. We need to educate the students about their bodies and the bodies of others."
    $ image.show(4)
    headmaster "And for that reason I plan to add Sexual Education to the schools curriculum."
    
    $ image.show(5)
    finola "I disagree. I believe that sexual education is not something that should be taught in school. It is a private matter between adults!"

    $ image.show(6)
    headmaster "I appreciate your concerns, but we cannot ignore the fact that our students are going through puberty and they need to know how their bodies work."
    $ image.show(7)
    headmaster "We will provide them with accurate information about sex and relationships without promoting any particular sexual orientation or gender identity."

    $ image.show(8)
    chloe "But what if some of our students get too excited during the lessons? It's completely inappropriate!"

    $ image.show(9)
    headmaster "I agree that we need to be sensitive to their emotions, but I am certain that this will only enhance their understanding of sexuality and relationships."
    headmaster "My research on other schools that have implemented similar programmes has shown that they have seen positive results in terms of decreased rates of teen pregnancy, STIs and sexual assault."

    $ image.show(10)
    lily "But it'll make our students more promiscuous!"

    $ image.show(11)
    headmaster "That's a common misconception about sex education. Research has shown that teaching young people about sexual health can actually prevent them from engaging in risky behaviour."
    headmaster "We can empower our students to make informed decisions about their bodies and relationships by providing accurate information and setting clear boundaries."

    $ image.show(12)
    yulan "We have to consider the possibility that some students won't be interested. I want to know if they will be forced to attend these classes."

    $ image.show(13)
    headmaster "Yes. This subject will be added to the normal curriculum. This is a topic that simply cannot be made optional."
    headmaster "It is our duty to provide all students with accurate information so that they can make informed choices about their bodies and relationships."

    $ image.show(14)
    zoe "I'm not fully convinced. But what if some students don't listen and still engage in risky behaviour?"

    $ image.show(1)
    headmaster "That's a valid concern, but we will provide them with accurate information so that they can make informed choices about their bodies."
    headmaster "If they choose to engage in risky behaviour despite this knowledge, they will have to take responsibility for their actions."
    headmaster "We will do our best to provide them with the necessary tools and resources."

    $ image.show(2)
    headmaster "I understand that this is a sensitive topic, but I believe that it is our responsibility to provide our students with the knowledge and skills they need to make informed decisions about their bodies and relationships."
    headmaster "We are running out of time, so I have a proposal."
    headmaster "I will work out a plan for the introduction of the new subject."
    headmaster "I'll include the specific topics that will be covered, the teaching methods that will be used, and the resources that will be available to the students."

    $ image.show(3)
    headmaster "I will then present this plan to you all for your feedback and suggestions."
    headmaster "I want to make sure that we are all on the same page and that we can move forward together."

    $ image.show(5)
    finola "I still have my doubts, but I'm willing to give it a chance."
    $ image.show(8)
    chloe "Yeah, let's see what you come up with."

    $ image.show(0)
    headmaster "Thank you all for your time. I'll keep you updated on the progress."

    $ add_notify_message("Added new rule to journal!")

    $ advance_progress('start_sex_ed') # 2 -> 3

    $ end_event('new_daytime')

label office_teacher_sex_ed_introduction_3 (**kwargs):
    $ begin_event(**kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster_thought "Now let's start working on the information material for the teachers. This needs to be perfect, so the teachers will be convinced."
    headmaster_thought "So what do I need to include in the material?"

    $ image.show(1)
    headmaster_thought "I think I should start with the basics. What is sexual education and why is it important?"
    headmaster_thought "Add some case studies and statistics to show the impact of sexual education on students."
    headmaster_thought "And maybe some examples of how other schools have successfully implemented sexual education programs."

    $ image.show(2)
    headmaster_thought "Then continue with the topics that will be covered in the classes and the teaching methods that will be used."
    headmaster_thought "That will include the resources that will be available to the students and the teachers."

    $ image.show(3)
    headmaster_thought "And finally, I should include a section on how the teachers can support the students and answer their questions."
    headmaster_thought "I think that should cover everything. Now I just need to put it all together."
    call screen black_screen_text("1h later.")

    $ image.show(4)
    headmaster_thought "Now that's done. I think I should present it to the teachers and get their feedback."
    
    $ advance_progress('start_sex_ed') # 3 -> 4

    $ end_event('new_daytime', **kwargs)

label office_teacher_sex_ed_introduction_4 (**kwargs):
    $ begin_event(**kwargs)

    $ finola = Character("Finola Ryan",   kind = character.teacher)
    $ chloe  = Character("Chloe Garcia",  kind = character.teacher)
    $ lily   = Character("Lily Anderson", kind = character.teacher)
    $ yulan  = Character("Yulan Chen",    kind = character.teacher)
    $ zoe    = Character("Zoe Parker",    kind = character.teacher)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Good morning! Today, I would like to present to you the importance of sexual education and the comprehensive program we are planning to implement."
    $ image.show(1)
    headmaster "I understand that there may be concerns and reservations about introducing this topic, but I believe it is crucial for the well-being and development of our students."
    headmaster "I already prepared some information material for you to review and provide feedback on."
    $ image.show(2)
    headmaster "Let's start with the basics. What is sexual education and why is it important?"

    call screen black_screen_text("15 Minutes later.")

    $ image.show(3)
    headmaster "Without proper sexual education, students may rely on misinformation or peer pressure, which can lead to risky behaviors and negative consequences."

    call screen black_screen_text("15 Minutes later.")

    $ image.show(4)
    headmaster "These case studies and statistics demonstrate the effectiveness of sexual education in promoting healthy behaviors and reducing negative outcomes."

    call screen black_screen_text("15 Minutes later.")

    $ image.show(5)
    headmaster "Now, let's talk about the resources that will be available to both the students and the teachers."

    call screen black_screen_text("15 Minutes later.")

    $ image.show(6)
    headmaster "Your support and guidance will be instrumental in addressing their concerns and providing accurate information, even with limited resources."

    call screen black_screen_text("15 Minutes later.")

    $ image.show(7)
    headmaster "By working together and making the most of what we have, we can ensure that our students receive the necessary knowledge and skills to make informed decisions and navigate their sexual health and relationships."
    headmaster "Thank you for your attention. I hope that this presentation has addressed some of your concerns and that we can move forward together in implementing comprehensive sexual education."
    
    $ image.show(8)
    finola "Thank you for the presentation, Headmaster. I can see the potential benefits of sexual education, but I would like some time to think about it and discuss it with my colleagues."
    $ image.show(9)
    chloe "I agree. It's an important topic, but we need to consider the concerns of parents and the community as well. Perhaps you could bring it up at the next PTA meeting and gather more feedback."
    $ image.show(10)
    lily "I appreciate the effort you've put into this presentation, Headmaster. However, I think it would be beneficial to involve parents in the decision-making process. Let's discuss it further at the next PTA meeting."
    $ image.show(11)
    yulan "I'm impressed with the research and success stories you've shared, Headmaster. However, I believe it's important to address any potential backlash or resistance from parents. Let's bring it up at the next PTA meeting and have a thorough discussion."
    $ image.show(12)
    zoe "Thank you for the detailed presentation, Headmaster. I can see the value of sexual education, but I think it's important to involve parents and the students in the decision-making process. Let's discuss it further at the next PTA meeting."

    $ image.show(13)
    headmaster "Thank you for your feedback. That will be all for today then."
    headmaster "I wish you all a good day and we'll see each other at the next PTA meeting."
    
    # headmaster returns to office, secretary enters

    $ image.show(14)
    secretary "[headmaster_first_name], how did the presentation go?"
    $ image.show(15)
    headmaster "It went well. The teachers had some concerns, but I think we're on the right track."
    $ image.show(16)
    headmaster "I probably just need to guide their thoughts in the right direction for them to support me at the pta meeting."
    headmaster "I don't expect much opposition from the student council, so I think we're good."
    $ image.show(17)
    headmaster "The parents should be no problem when the teachers and students agree to the change."

    $ advance_progress('start_sex_ed') # 4 -> 5

    $ end_event('new_daytime', **kwargs)

label pta_discussion_sex_ed_intro_1 (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ finola = Character("Finola Ryan",   kind = character.teacher)
    $ chloe  = Character("Chloe Garcia",  kind = character.teacher)
    $ lily   = Character("Lily Anderson", kind = character.teacher)
    $ yulan  = Character("Yulan Chen",    kind = character.teacher)
    $ zoe    = Character("Zoe Parker",    kind = character.teacher)

    $ adelaide = Character("Adelaide Hall", kind = character.parent)
    $ nubia    = Character("Nubia Davis",   kind = character.parent)
    $ yuki     = Character("Yuki Yamamoto", kind = character.parent)

    $ yuriko = Character("Yuriko Oshima", kind = character.sgirl)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    headmaster "Nobody? Alright then, I would like to discuss the introduction of sexual education in our curriculum."
    $ image.show(1)
    yuriko "What? No way! That's totally unnecessary!"
    $ image.show(2)
    adelaide "I agree! This is not something that should be taught in school!"
    $ image.show(3)
    headmaster "I believe it is important for our students to be educated about this topic. It is crucial for their development and well-being."
    $ image.show(4)
    yuki "But what about the parents? We should be the ones to teach our children about these things!"
    $ image.show(5)
    headmaster "I understand your concerns, but many parents may not feel comfortable discussing these topics with their children."
    $ image.show(6)
    headmaster "Also, no offense, but some parents may not have the right information to share with their children."
    $ image.show(7)
    headmaster "I may not be at this school for long, but I have seen enough to know that our students are struggling with these issues."
    $ image.show(8)
    chloe "With that I have to agree. I normally wouldn't support this, but I can also see the effects of the lack of sexual education."
    $ image.show(9)
    finola "And I think it is the responsibility of all of us to ensure that our students receive accurate information."
    $ image.show(10)
    yuriko "But is it really necessary? That topic is so embarrassing and uncomfortable!"
    $ image.show(11)
    headmaster "That is even more reason to teach it! If we don't, our students will rely on misinformation and peer pressure."
    $ image.show(12)
    headmaster "This is a topic that cannot be ignored. You students will come across it sooner or later, and you have to know how to deal with it."
    $ image.show(13)
    headmaster "And if you don't learn it here, you will learn it from the wrong sources. And that then will become dangerous."
    $ image.show(14)
    yuki "But what if some students get too excited during the lessons? It's completely inappropriate!"
    $ image.show(15)
    headmaster "I understand your concerns, but I assure you that we will handle this topic with sensitivity and care."
    $ image.show(16)
    nubia "Alright, I need time to think about this, but I will agree to have it put to vote after some time to consider it."
    $ image.show(17)
    adelaide "I agree."
    $ image.show(18)
    yuki "I guess I can see the benefits, but I still have my doubts."

    $ image.show(19)
    yuriko "Fine! But I still think it's unnecessary!"

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
    headmaster "As previously announced, I would like to put to vote the introduction of theoretical sex education in our curriculum."
    $ image.show(1)
    headmaster "We already discussed the importance of this topic and the benefits it can bring to our students."
    $ image.show(2)
    headmaster "Now I hope you have made up your minds and are ready to cast your votes."

    $ image.show(3)
    headmaster "So when there are no further questions, please cast your vote now."

    # teacher comment on vote
    if teacher_vote == 'yes':
        $ image.show(4)
        teacher "We teachers had a discussion about this topic and we came to the conclusion that theoretical sex education is important for the students."
        teacher "So we support the introduction of this subject in our curriculum."
    else:
        $ image.show(5)
        teacher "We teachers discussed this topic and we still have concerns about the introduction, so we will vote against it for now."

    # student comment on vote
    if student_vote == 'yes':
        $ image.show(6)
        sgirl "After thinking about it, I believe that it could be beneficial for us besides being embarrassing. So I vote yes."
    else:
        $ image.show(7)
        sgirl "I still think the topic is embarrassing and unnecessary, so I vote no."

    $ image.show(8)
    parent "We believe that the introduction of theoretical sex education is not appropriate and should be discussed at home."
    parent "For this reason, we vote against the proposal."

    if end_choice == 'yes':
        $ image.show(9)
        headmaster "With the majority of votes in favor, the proposal is accepted."
        headmaster "Theoretical Sexual Education will be introduced into the curriculum."
        $ image.show(10)
        headmaster "I will call for a school assembly this afternoon to inform the students about the change and to distribute information material for the students and faculty members to prepare themselves over the weekend."
    else:
        $ image.show(9)
        headmaster "The proposal is rejected due to the majority of votes against it."

    call pta_vote_result("no", teacher_vote, student_vote, get_value("vote_proposal", **kwargs)) from _call_pta_vote_result_theoretical_sex_ed_1

    $ end_event('new_daytime', **kwargs)

# endregion
##############################

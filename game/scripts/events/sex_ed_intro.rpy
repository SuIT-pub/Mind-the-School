init 1 python: 
    set_current_mod('base')  

    office_call_secretary_1_event = Event(1, "office_call_secretary_1",
        NOT(ProgressCondition('start_sex_ed')),
        ProgressCondition('aona_sports_bra', '2+'),
        TimeCondition(daytime = "6-"),
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
        office_teacher_sex_ed_introduction_1_event,
        office_teacher_sex_ed_introduction_3_event,
    )

    office_teacher_sex_ed_introduction_2_event = Event(1, "office_teacher_sex_ed_introduction_2",
        ProgressCondition('start_sex_ed', 2),
        TimeCondition(daytime = "f", day = "d"),
    )

    office_building_timed_event.add_event(
        office_teacher_sex_ed_introduction_2_event,
    )

    office_teacher_sex_ed_introduction_4_event = Event(1, "office_teacher_sex_ed_introduction_4",
        ProgressCondition('start_sex_ed', 4),
        TimeCondition(daytime = "f", day = "d"),
    )

    office_building_events["schedule_meeting"].add_event(
        office_teacher_sex_ed_introduction_4_event,
    )


##############################
# region Sex Ed Introduction #

label office_call_secretary_1 (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You call the secretary."
    secretary "Hello, [headmaster_first_name]. How can I help you?"
    headmaster "I need your opinion on something."
    secretary "Sure, what is it?"
    headmaster "I'm thinking of introducing sex education classes in the curriculum. What do you think?"
    secretary "I think it's a great idea. It's important for students to be educated about such topics."
    secretary "But do you think the rest of the staff and also the students would agree?"
    headmaster "Hmm, I guess you're right. That will be quite the hurdle, I think I need to make sure they are ready for it before suggesting it."
    headmaster "Do you have any suggestions on how to approach this?"
    secretary "I think you should start by talking to the staff and getting their input."
    secretary "To actually convince them, you could prepare some teaching material and introductory material on the subject."
    secretary "That way they can see what you have in mind and how you plan to approach it."
    headmaster "That's a good idea. Thank you for your input."
    secretary "You're welcome. Is there anything else?"
    headmaster "No, that's all. Thank you."
    secretary "You're welcome. Have a nice day."
    headmaster_thought "Then, maybe I should start work on some teaching material for the sex ed classes."


    $ start_progress('start_sex_ed') # 0 -> 1

    $ end_event('new_daytime', **kwargs)

label office_teacher_sex_ed_introduction_1(**kwargs):
    $ begin_event(**kwargs)

    headmaster_thought "Hmm, now how do I start this."
    headmaster_thought "My main problem is that the teacher will have reservations about introducing sex ed classes."
    headmaster_thought "So the best way to overcome this, would be to show them the importance of it."
    headmaster_thought "I should talk to each one of them and present them the effects of not giving the students proper sexual education."
    headmaster_thought "If I can relate to them in their own expertise, I guess that would be even better."
    headmaster_thought "But first I should meet up with them and find out what they think in general about the idea of introducing sex ed classes"

    headmaster "Emiko?"
    secretary "Yes, [headmaster_first_name]?"
    headmaster "Can you please schedule a meeting with all the teachers for tomorrow?"
    secretary "Sure, I'll take care of it. At what time?"
    headmaster "First thing in the morning. I want to discuss the introduction of the sex ed classes with them."
    secretary "Got it. I'll send out the invites right away."
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

    headmaster "I thank you all for coming on such short notice."
    headmaster "Since I became the new headmaster, I was closely observing the school and the students."
    headmaster "The school is nothing short but disappointing and the students and their achievements are a direct image of that."
    headmaster "But what shocked me most was the social behaviour of the students."
    headmaster "The students are surprisingly tame. But when it comes to their behaviour related to their bodies and looks, they are quite the opposite."
    headmaster "I heard of bullying and exclusion towards certain students because of their looks or their overall body form."
    headmaster "I think that this is a direct result of the lack of proper sexual education."
    headmaster "The students became too ignorant. I think they simply don't know why bodies are different and why they are changing."
    headmaster "So they did what most people do when they don't understand something. They fear it. And in conclusion they bully or fight it."
    headmaster "I think that we need to change that. We need to educate the students about their bodies and the bodies of others."
    headmaster "And for that reason I plan to add Sexual Education to the schools curriculum."
    
    finola "I disagree. I believe that sexual education is not something that should be taught in school. It is a private matter between adults!"

    headmaster "I appreciate your concerns, but we cannot ignore the fact that our students are going through puberty and they need to know how their bodies work."
    headmaster "We will provide them with accurate information about sex and relationships without promoting any particular sexual orientation or gender identity."

    chloe "But what if some of our students get too excited during the lessons? It's completely inappropriate!"

    headmaster "I agree that we need to be sensitive to their emotions, but I am certain that this will only enhance their understanding of sexuality and relationships."
    headmaster "Our research on other schools that have implemented similar programmes has shown that they have seen positive results in terms of decreased rates of teen pregnancy, STIs and sexual assault."

    lily "But it'll make our students more promiscuous!"

    headmaster "That's a common misconception about sex education. Research has shown that teaching young people about sexual health can actually prevent them from engaging in risky behaviour."
    headmaster "We can empower our students to make informed decisions about their bodies and relationships by providing accurate information and setting clear boundaries."

    yulan "We have to consider the possibility that some students won't be interested. I want to know if they will be forced to attend these classes."

    headmaster "Yes. This subject will be added to the normal curriculum. This is a topic that simply cannot be made optional."
    headmaster "It is our duty to provide all students with accurate information so that they can make informed choices about their bodies and relationships."

    zoe "I'm not fully convinced. But what if some students don't listen and still engage in risky behaviour?"

    headmaster "That's a valid concern, but we will provide them with accurate information so that they can make informed choices about their bodies."
    headmaster "If they choose to engage in risky behaviour despite this knowledge, they will have to take responsibility for their actions."
    headmaster "We will do our best to provide them with the necessary tools and resources."

    headmaster "I understand that this is a sensitive topic, but I believe that it is our responsibility to provide our students with the knowledge and skills they need to make informed decisions about their bodies and relationships."
    headmaster "We are running out of time, so I have a proposal."
    headmaster "I will work out a plan for the introduction of the new subject."
    headmaster "I'll include the specific topics that will be covered, the teaching methods that will be used, and the resources that will be available to the students."

    headmaster "I will then present this plan to you all for your feedback and suggestions."
    headmaster "I want to make sure that we are all on the same page and that we can move forward together."

    finola "I still have my doubts, but I'm willing to give it a chance."
    chloe "Yeah, let's see what you come up with."

    headmaster "Thank you all for your time. I'll keep you updated on the progress."

    $ add_notify_message("Added new rule to journal!")

    $ advance_progress('start_sex_ed') # 2 -> 3

    $ end_event('new_daytime')

label office_teacher_sex_ed_introduction_3 (**kwargs):
    $ begin_event(**kwargs)

    headmaster_thought "Now let's start working on the information material for the teachers. This needs to be perfect, so the teachers will be convinced."
    headmaster_thought "So what do I need to include in the material?"
    headmaster_thought "I think I should start with the basics. What is sexual education and why is it important?"
    headmaster_thought "Add some case studies and statistics to show the impact of sexual education on students."
    headmaster_thought "And maybe some examples of how other schools have successfully implemented sexual education programs."
    headmaster_thought "Then continue with the topics that will be covered in the classes and the teaching methods that will be used."
    headmaster_thought "That will include the resources that will be available to the students and the teachers."
    headmaster_thought "And finally, I should include a section on how the teachers can support the students and answer their questions."
    headmaster_thought "I think that should cover everything. Now I just need to put it all together."
    call screen black_screen_text("1h later.")
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

    headmaster "Good morning, teachers. Today, I would like to present to you the importance of sexual education and the comprehensive program we are planning to implement."
    headmaster "I understand that there may be concerns and reservations about introducing this topic, but I believe it is crucial for the well-being and development of our students."
    headmaster "Let's start with the basics. What is sexual education and why is it important?"

    $ call_custom_menu_with_text("Do you want to read the entire presentation?", character.subtitles, False,
        ("Read full presentation", "office_teacher_sex_ed_introduction_4.presentation"),
        ("Skip presentation", "office_teacher_sex_ed_introduction_4.skipped_presentation"), 
    **kwargs)
label .presentation (**kwargs):
    headmaster "Sexual education is a comprehensive program that provides students with accurate and age-appropriate information about human sexuality, relationships, and reproductive health."
    headmaster "Now, you may wonder why it is important. Well, it equips students with the knowledge and skills they need to make informed decisions about their bodies, relationships, and sexual health."
    headmaster "Without proper sexual education, students may rely on misinformation or peer pressure, which can lead to risky behaviors and negative consequences."
    headmaster "But by providing accurate information, we can empower our students to develop healthy attitudes towards their bodies and relationships."
    headmaster "Now, let's dive deeper. Allow me to share some case studies and statistics to address your concerns and demonstrate the potential benefits of sexual education."
    headmaster "Research has shown that comprehensive sexual education programs can have a positive impact on students' knowledge, attitudes, and behaviors."
    headmaster "For example, a study conducted by XYZ University found that schools with comprehensive sexual education programs had lower rates of teen pregnancy and sexually transmitted infections (STIs)."
    headmaster "Another study by ABC Institute showed that students who received sexual education were more likely to delay sexual activity and use contraception when they did become sexually active."
    headmaster "These case studies and statistics demonstrate the effectiveness of sexual education in promoting healthy behaviors and reducing negative outcomes."
    headmaster "Now, let's take a look at some successful implementations of sexual education programs in other schools."
    headmaster "I understand that you may have concerns about how this program will be implemented. However, there are many schools across the country that have successfully introduced sexual education programs."
    headmaster "For instance, XYZ High School in Cityville implemented a comprehensive sexual education curriculum that included interactive classroom activities, guest speakers, and access to resources."
    headmaster "They reported positive outcomes such as increased knowledge, improved communication skills, and reduced rates of teen pregnancy and STIs."
    headmaster "By sharing these success stories, I hope to address your concerns and show that sexual education can make a positive difference in students' lives."
    headmaster "Now, let's move on to the topics that will be covered in the classes and the teaching methods that will be used."
    headmaster "I understand that you may have questions about the content and teaching methods. The sexual education classes will cover a range of topics, including but not limited to: human anatomy and reproductive systems, consent and healthy relationships, contraception and STI prevention, gender and sexual orientation, and communication skills."
    headmaster "As for the teaching methods, they will be interactive and engaging, incorporating a variety of strategies such as group discussions, role-playing, multimedia presentations, and guest speakers."
    headmaster "These methods will ensure that students actively participate in their learning and have opportunities to ask questions and share their perspectives."
    headmaster "Now, let's talk about the resources that will be available to both the students and the teachers."
    headmaster "I understand that you may have concerns about the resources and support available. Given our narrow budget, we will make the most of the limited resources we have to support students' learning."
    headmaster "While we may not have access to extensive textbooks or online materials, we will ensure that the information provided is accurate and age-appropriate."
    headmaster "In addition, we will collaborate with local health organizations and community centers to provide guest speakers and workshops on sexual education."
    headmaster "Furthermore, we have plans to renovate our school library to provide students with a comfortable space for learning and research."
    headmaster "The renovated library will be equipped with a variety of resources, including books, magazines, and reference materials."
    headmaster "We will also create dedicated areas for studying and quiet reading to enhance the learning environment."
    headmaster "By improving our library facilities, we aim to encourage students to utilize this valuable resource for their academic needs."
    headmaster "As for teacher support, we will explore free online training programs and workshops to enhance your knowledge and skills in delivering sexual education effectively."
    headmaster "Your dedication and creativity in delivering the curriculum will be crucial in overcoming the resource limitations."
    headmaster "Lastly, I would like to emphasize the importance of your role as teachers in creating a safe and inclusive learning environment for students to discuss sensitive topics related to sexual education."
    headmaster "Your support and guidance will be instrumental in addressing their concerns and providing accurate information, even with limited resources."

    call .end_presentation (**kwargs) from call_end_presentation_sex_ed_intro_1
label .skipped_presentation (**kwargs):

    call screen black_screen_text("30 Minutes later.")

    call .end_presentation (**kwargs) from call_end_presentation_sex_ed_intro_2
label .end_presentation (**kwargs):

    headmaster "By working together and making the most of what we have, we can ensure that our students receive the necessary knowledge and skills to make informed decisions and navigate their sexual health and relationships."
    headmaster "Thank you for your attention. I hope that this presentation has addressed some of your concerns and that we can move forward together in implementing comprehensive sexual education."
    
    finola "Thank you for the presentation, Headmaster. I can see the potential benefits of sexual education, but I would like some time to think about it and discuss it with my colleagues."
    chloe "I agree. It's an important topic, but we need to consider the concerns of parents and the community as well. Perhaps you could bring it up at the next PTA meeting and gather more feedback."
    lily "I appreciate the effort you've put into this presentation, Headmaster. However, I think it would be beneficial to involve parents in the decision-making process. Let's discuss it further at the next PTA meeting."
    yulan "I'm impressed with the research and success stories you've shared, Headmaster. However, I believe it's important to address any potential backlash or resistance from parents. Let's bring it up at the next PTA meeting and have a thorough discussion."
    zoe "Thank you for the detailed presentation, Headmaster. I can see the value of sexual education, but I think it's important to involve parents and the students in the decision-making process. Let's discuss it further at the next PTA meeting."

    headmaster "Thank you for your feedback. That will be all for today then."
    headmaster "I wish you all a good day and we'll see each other at the next PTA meeting."
    
    # headmaster returns to office, secretary enters

    secretary "[headmaster_first_name], how did the presentation go?"
    headmaster "It went well. The teachers had some concerns, but I think we're on the right track."
    headmaster "I probably just need to guide their thoughts in the right direction for them to support me at the pta meeting."
    headmaster "I don't expect much opposition from the student council, so I think we're good."
    headmaster "The parents should be no problem when the teachers and students agree to the change."

    $ advance_progress('start_sex_ed') # 4 -> 5

    $ end_event('new_daytime', **kwargs)

# endregion
##############################

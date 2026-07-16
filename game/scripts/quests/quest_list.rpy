label load_quests:
    $ set_current_mod('base')

    if not quest_manager:
        $ quest_manager = QuestManager()

    ########################
    # region Normal Quests #

    # Aona's New Bra
    $ quest_manager.load_quest(
        Quest("aonas_new_bra", "Aona's New Bra", "School",
            "Aona is having trouble during P.E. at the Gym. Teach a P.E. class there to find out what's wrong, then help her get a proper sports bra.",
            "Aona has her new sports bra and is ready for P.E. classes.",
            "images/events/misc/aona_sports_bra_event_1/aona_sports_bra_event_1 $ 23.webp",
            {"init": [QuestVisibleEffect("quest", "aonas_new_bra")]},
            Goal("aona_bra_event_1", "Find out what's wrong",
                "Go to the Gym and teach a P.E. class. You'll learn what's bothering Aona during the lesson.",
                {
                    "init": [QuestVisibleEffect("goal", "aona_bra_event_1")],
                    "complete": [QuestVisibleEffect("goal", "aona_bra_event_2")],
                },
                EventTask("aona_bra_task_1", "Teach P.E. at the Gym", "Go to the Gym and teach a P.E. class. The story will advance during the lesson.",
                    {
                        "init": [QuestVisibleEffect("task", "aona_bra_task_1"), QuestActivateEffect("aona_bra_task_1")],
                        "complete": [NotificationEffect("Goal completed!")],
                    },
                    "gym_teach_pe_main_aona_bra",
                ),
            ),
            Goal("aona_bra_event_2", "Take Aona to the shop",
                "Drive Aona to the shop so she can buy a new sports bra. Do this when the opportunity is available.",
                {
                    "visible": [QuestVisibleEffect("task", "aona_bra_task_2"), QuestActivateEffect("aona_bra_task_2")],
                    "complete": [QuestVisibleEffect("goal", "aona_bra_event_3"), NotificationEffect("Goal completed!")],
                },
                EventTask("aona_bra_task_2", "Drive Aona to the shop", "Take Aona to the shop to buy her new sports bra. Complete the trip when it's available.", {}, "aona_sports_bra_event_1"),
            ),
            Goal("aona_bra_event_3", "See Aona with her new bra",
                "Go to the Gym and teach P.E. again to see Aona in her new bra and confirm she's happy with it.",
                {
                    "visible": [QuestVisibleEffect("task", "aona_bra_task_3"), QuestActivateEffect("aona_bra_task_3")],
                    "complete": [NotificationEffect("Goal completed!")],
                },
                EventTask("aona_bra_task_3", "Teach P.E. and check on Aona", "Go to the Gym and teach a P.E. class to see Aona in her new bra and finish the quest.", {}, "gym_teach_pe_main_aona_bra_2"),
            ),
        )
    )

    # Truth or Dare
    $ quest_manager.load_quest(
        Quest("truth_or_dare", "Truth or Dare", "School",
            "Some students are secretly playing a daring game together. I should watch and listen around the school to find out what the game is and how they play it.",
            "Now I know when and where they play and can enjoy watching their evening games.",
            "images/events/truth_or_dare/truth_or_dare_4/card/truth_or_dare_4_card ikushi_ito 4 1.webp",
            {},
            Goal("truth_or_dare_goal_1", "Truth or Dare: First clue", "I saw one of the girls suddenly run off about something. I should look around the school again and see what that was about.",
                {},
                EventTask("truth_or_dare_task_1", "Investigate the strange incident", "Walk around the school until I run into that situation again and find out what the girls are up to.",
                    {
                        "init": [QuestActivateEffect("truth_or_dare_task_1")],
                        "complete": [
                            QuestVisibleEffect("quest", "truth_or_dare"),
                            QuestVisibleEffect("goal", "truth_or_dare_goal_1"),
                            QuestVisibleEffect("task", "truth_or_dare_task_1"),
                            QuestVisibleEffect("goal", "truth_or_dare_goal_2"),
                            QuestVisibleEffect("task", "truth_or_dare_task_2"),
                            NotificationEffect("New quest available!"),
                        ],
                    },
                    "truth_or_dare_1",
                ),
            ),
            Goal("truth_or_dare_goal_2", "Truth or Dare: Gossip in the halls", "The girls were talking about some kind of game in the halls. I should hang around there and listen in on their conversations.",
                {},
                EventTask("truth_or_dare_task_2", "Listen to the girls", "Stay in the school halls and eavesdrop on the girls until I learn more about their secret game.",
                    {
                        "complete": [
                            QuestVisibleEffect("goal", "truth_or_dare_goal_3"),
                            QuestVisibleEffect("task", "truth_or_dare_task_3"),
                            QuestActivateEffect("truth_or_dare_task_3"),
                            NotificationEffect("Goal completed!"),
                        ]
                    },
                    "truth_or_dare_2",
                ),
            ),
            Goal("truth_or_dare_goal_3", "Truth or Dare: Find the meeting", "They said they'll continue playing soon. I need to find out when and where they'll meet next.",
                {},
                EventTask("truth_or_dare_task_3", "Figure out time and place", "Pay attention when the girls talk about continuing the game so I learn the time and place of their next round.",
                    {
                        "complete": [
                            QuestVisibleEffect("goal", "truth_or_dare_goal_4"),
                            QuestVisibleEffect("task", "truth_or_dare_task_4"),
                            QuestActivateEffect("truth_or_dare_task_4"),
                            NotificationEffect("Goal completed!"),
                        ],
                    },
                    "truth_or_dare_3",
                ),
            ),
            Goal("truth_or_dare_goal_4", "Truth or Dare: Night in the dorm", "They regularly play this at night in the dorm. I should sneak around there and watch.",
                {},
                EventTask("truth_or_dare_task_4", "Watch the dorm game", "Visit the dorm at night and snoop around until I can watch them play their truth-or-dare game.", {"complete": [NotificationEffect("Quest completed!")]}, "truth_or_dare_4"),
            ),
        )
    )

    # start sex ed
    $ quest_manager.load_quest(
        Quest("start_sex_ed", "Introduce Theoretical Sex Education", "School",
            "The students' knowledge about bodies, puberty, and reproduction is clearly lacking. Work with staff and the PTA to add a theoretical sex education unit to the school curriculum.",
            "The theoretical sex education unit has been approved and announced. The next step is holding the first lesson.",
            "images/events/sex_ed_intro/mini_sd_2/mini_sd_2 5.webp",
            {
                "visible": [QuestVisibleEffect("goal", "start_sex_ed_1"), NotificationEffect("New Quest available1")], 
                "complete": [NotificationEffect("Goal completed!")]
            },
            EventTask("start_sex_ed_intro", "", "",
                {
                    "init": [QuestActivateEffect("start_sex_ed_intro")],
                    "complete": [QuestVisibleEffect("quest", "start_sex_ed")]
                },
                "aona_sports_bra_event_1"
            ),
            Goal("start_sex_ed_1", "Ask Emiko for Advice",
                ["Talk to Emiko and ask how to approach the topic at school.", "(Try calling her from your office.)"],
                {
                    "visible": [QuestVisibleEffect("task", "start_sex_ed_1_task_1"), QuestActivateEffect("start_sex_ed_1_task_1")], 
                    "complete": [NotificationEffect("Goal completed!")]
                },
                EventTask("start_sex_ed_1_task_1", "Call Emiko",
                    "From your office, call Emiko to ask for her opinion on introducing sex education.",
                    {"complete": [QuestVisibleEffect("goal", "start_sex_ed_2")]},
                    "office_call_secretary_1"
                )
            ),
            Goal("start_sex_ed_2", "Plan How to Approach the Teachers",
                "Speak with the teachers about introducing sex education. Start by bringing it up in your office when you have a moment.",
                {
                    "visible": [QuestVisibleEffect("task", "start_sex_ed_2_task_1"), QuestActivateEffect("start_sex_ed_2_task_1")], 
                    "complete": [NotificationEffect("Goal completed!")]
                },
                EventTask("start_sex_ed_2_task_1", "Bring It Up with the Teachers",
                    "In your office, start the conversation with the teachers about adding theoretical sex education.",
                    {"complete": [QuestVisibleEffect("goal", "start_sex_ed_3")]},
                    "office_teacher_sex_ed_introduction_1"
                )
            ),
            Goal("start_sex_ed_3", "Hold a Morning Staff Meeting",
                "Meet the teachers in the morning and formally propose adding theoretical sex education to the curriculum.",
                {
                    "visible": [QuestVisibleEffect("task", "start_sex_ed_3_task_1"), QuestActivateEffect("start_sex_ed_3_task_1")], 
                    "complete": [NotificationEffect("Goal completed!")]
                },
                EventTask("start_sex_ed_3_task_1", "Morning Teacher Meeting",
                    "Attend the morning meeting with the teachers to propose the new curriculum topic.",
                    {"complete": [QuestVisibleEffect("goal", "start_sex_ed_4")]},
                    "office_teacher_sex_ed_introduction_2"
                )
            ),
            Goal("start_sex_ed_4", "Prepare Supporting Material",
                "The teachers want proof and reassurance. Gather convincing information and prepare a short case you can present to them.",
                {
                    "visible": [QuestVisibleEffect("task", "start_sex_ed_4_task_1"), QuestActivateEffect("start_sex_ed_4_task_1")], 
                    "complete": [NotificationEffect("Goal completed!")]
                },
                EventTask("start_sex_ed_4_task_1", "Work on the Data",
                    "Prepare the material you'll use to convince the teachers (data, arguments, and examples).",
                    {"complete": [QuestVisibleEffect("goal", "start_sex_ed_5")]},
                    "office_teacher_sex_ed_introduction_3"
                )
            ),
            Goal("start_sex_ed_5", "Present the Case to the Teachers",
                "Return to the teachers and present your prepared material. (Do this from your office.)",
                {
                    "visible": [QuestVisibleEffect("task", "start_sex_ed_5_task_1"), QuestActivateEffect("start_sex_ed_5_task_1")], 
                    "complete": [NotificationEffect("Goal completed!")]
                },
                EventTask("start_sex_ed_5_task_1", "Present Your Findings",
                    "In your office, present your prepared arguments and data to the teachers.",
                    {"complete": [QuestVisibleEffect("goal", "start_sex_ed_6")]},
                    "office_teacher_sex_ed_introduction_4"
                )
            ),
            Goal("start_sex_ed_6", "Discuss It with the PTA",
                "The teachers agreed to try—if the PTA approves. Arrange a discussion with the PTA and make your case.",
                {
                    "visible": [QuestVisibleEffect("task", "start_sex_ed_6_task_1"), QuestActivateEffect("start_sex_ed_6_task_1")], 
                    "complete": [NotificationEffect("Goal completed!")]
                },
                EventTask("start_sex_ed_6_task_1", "PTA Discussion",
                    "Meet with the PTA and discuss introducing theoretical sex education at school.",
                    {"complete": [QuestVisibleEffect("goal", "start_sex_ed_7")]},
                    "pta_discussion_sex_ed_intro_1"
                )
            ),
            Goal("start_sex_ed_7", "Strengthen PTA Support",
                "The PTA needs time. Use this time to improve your chances—work on building support for the topic before they decide.",
                {
                    "visible": [QuestVisibleEffect("task", "start_sex_ed_7_task_1"), QuestActivateEffect("start_sex_ed_7_task_1")], 
                    "complete": [NotificationEffect("Goal completed!")]
                },
                JournalUnlockTask("start_sex_ed_7_task_1", "Prepare the Curriculum Entry",
                    "Work on the official curriculum/journal entry so the proposal looks organized and professional.",
                    {"complete": [QuestVisibleEffect("goal", "start_sex_ed_8")]},
                    "theoretical_sex_ed"
                )
            ),
            Goal("start_sex_ed_8", "Make the School Announcement",
                "The PTA approved the trial. Make an official announcement to the students (assembly).",
                {
                    "visible": [QuestVisibleEffect("task", "start_sex_ed_8_task_1"), QuestActivateEffect("start_sex_ed_8_task_1")], 
                    "complete": [NotificationEffect("Goal completed!")]
                },
                EventTask("start_sex_ed_8_task_1", "Hold an Assembly",
                    "Hold an assembly and announce the new theoretical sex education unit.",
                    {"complete": [QuestVisibleEffect("goal", "start_sex_ed_9")]},
                    "theoretical_sex_ed_assembly_1"
                )
            ),
            Goal("start_sex_ed_9", "See How Students React",
                "After the announcement, walk around campus and listen to what students are saying. When you're ready, proceed to the first day.",
                {
                    "visible": [
                        QuestVisibleEffect("task", "start_sex_ed_9_task_1"), QuestActivateEffect("start_sex_ed_9_task_1"),
                        QuestVisibleEffect("task", "start_sex_ed_9_task_2"), QuestActivateEffect("start_sex_ed_9_task_2")
                    ], "complete": [NotificationEffect("Goal completed!")]
                },
                TaskOptionalGroup("start_sex_ed_9_task_1", "Check Student Reactions",
                    "Explore the campus and listen in on different student conversations about the new curriculum.",
                    {
                        "visible": [
                            QuestVisibleEffect("task", "start_sex_ed_9_task_1_1"),
                            QuestVisibleEffect("task", "start_sex_ed_9_task_1_2"),
                            QuestVisibleEffect("task", "start_sex_ed_9_task_1_3"),
                        ]
                    },
                    EventTask("start_sex_ed_9_task_1_1", "Hallway Talk",
                        "Listen to a student conversation in the hallway.", {"visible": [QuestActivateEffect("start_sex_ed_9_task_1_1")]}, "sex_ed_intro_mini_sd_1"),
                    EventTask("start_sex_ed_9_task_1_2", "Gym Talk",
                        "Listen to a student conversation near the gym.", {"visible": [QuestActivateEffect("start_sex_ed_9_task_1_2")]}, "sex_ed_intro_mini_sd_2"),
                    EventTask("start_sex_ed_9_task_1_3", "Courtyard Talk",
                        "Listen to a student conversation in the courtyard.", {"visible": [QuestActivateEffect("start_sex_ed_9_task_1_3")]}, "sex_ed_intro_mini_courtyard_1"),
                ),
                EventTask("start_sex_ed_9_task_2", "Proceed to the First Day", "Advance to the first day of theoretical sex education.",
                    {"complete": [QuestVisibleEffect("goal", "start_sex_ed_10")]},
                    "first_sex_ed_day"
                )
            ),
            Goal("start_sex_ed_10", "Hold the First Lesson",
                "Go to class and start the first theoretical sex education lesson.",
                {
                    "visible": [QuestVisibleEffect("task", "start_sex_ed_10_task_1"), QuestActivateEffect("start_sex_ed_10_task_1")], 
                    "complete": [NotificationEffect("Goal completed!")]
                },
                EventTask("start_sex_ed_10_task_1", "Teach the First Class", "Begin the first theoretical sex education class session.", {}, "first_sex_ed_class_1")
            )
        )
    )

    # Yoga Outfits
    $ quest_manager.load_quest(
        Quest("yoga_outfit", "New Yoga Outfit", "School",
            "Ms. Parker wants to start yoga classes during P.E., but the current outfits are inappropriate. Help her organize proper yoga outfits and prepare the students.",
            "The new yoga outfits have been ordered and distributed. Yoga classes can now continue properly.",
            "images/journal/journal/test_image.webp",
            {
                "init": [QuestVisibleEffect("quest", "yoga_outfit")],
                "complete": [NotificationEffect("Quest completed!")],
            },
            EventTask("yoga_outfit_task_1", "Yoga Outfit", "Yoga Outfit",
                {
                    "init": [QuestActivateEffect("yoga_outfit_task_1")],
                    "complete": [QuestVisibleEffect("quest", "yoga_outfit"), QuestVisibleEffect("goal", "yoga_outfit_goal_2"), NotificationEffect("New quest available!")],
                },
                "new_yoga_outfit_1",
            ),
            Goal("yoga_outfit_goal_2", "Observe the Yoga Class",
                "Go to the school gym during P.E. time and watch Ms. Parker's yoga class.",
                {
                    "visible": [QuestVisibleEffect("task", "yoga_outfit_task_2"), QuestActivateEffect("yoga_outfit_task_2")],
                    "complete": [QuestVisibleEffect("goal", "yoga_outfit_goal_3"), QuestVisibleEffect("task", "yoga_outfit_task_3"), QuestActivateEffect("yoga_outfit_task_3"), NotificationEffect("Goal completed!")],
                },
                EventTask("yoga_outfit_task_2", "", "I should have a look at her yoga classes, and see how she's doing.",{},"new_yoga_outfit_2"),
            ),
            Goal("yoga_outfit_goal_3", "Return to the Gym Later",
                "Visit the gym again on another P.E. day to see how the yoga class is progressing.",
                {
                    "visible": [QuestVisibleEffect("task", "yoga_outfit_task_3"), QuestActivateEffect("yoga_outfit_task_3")],
                    "complete": [QuestVisibleEffect("goal", "yoga_outfit_goal_4"), QuestVisibleEffect("task", "yoga_outfit_task_4"), QuestActivateEffect("yoga_outfit_task_4"), NotificationEffect("Goal completed!")],
                },
                EventTask("yoga_outfit_task_3", "", "Parker seems to be doing a great job. I should check back later.", {}, "new_yoga_outfit_3"),
            ),
            Goal("yoga_outfit_goal_4", "Find Better Outfit Options",
                "Talk to students at school and look for volunteers willing to try new yoga outfit samples.",
                {
                    "visible": [QuestVisibleEffect("task", "yoga_outfit_task_4"), QuestActivateEffect("yoga_outfit_task_4")],
                    "complete": [QuestVisibleEffect("goal", "yoga_outfit_goal_5"), QuestVisibleEffect("task", "yoga_outfit_task_5"), QuestActivateEffect("yoga_outfit_task_5"), NotificationEffect("Goal completed!")],
                },
                EventTask("yoga_outfit_task_4", "", "Ms. Parker asked for proper yoga outfits. The current ones seem to be a bit too tight. But I need to find the right. Maybe some students like to help with that.", {}, "new_yoga_outfit_4"),
            ),
            Goal("yoga_outfit_goal_5", "Meet Volunteers in Your Office",
                "Go to your office in the afternoon and wait for the student volunteers to arrive to try on the samples.",
                {
                    "visible": [QuestVisibleEffect("task", "yoga_outfit_task_5"), QuestActivateEffect("yoga_outfit_task_5")],
                    "complete": [QuestVisibleEffect("goal", "yoga_outfit_goal_6"), QuestVisibleEffect("task", "yoga_outfit_task_6"), QuestActivateEffect("yoga_outfit_task_6"), NotificationEffect("Goal completed!")],
                },
                EventTask("yoga_outfit_task_5", "", "I've found a few volunteers to try on my samples. They should come to my office later.", {}, "new_yoga_outfit_5"),
            ),
            Goal("yoga_outfit_goal_6", "Discuss Outfit Sizes with Ms. Parker",
                "Find Ms. Parker at school and talk to her about what sizes should be ordered.",
                {
                    "visible": [QuestVisibleEffect("task", "yoga_outfit_task_6"), QuestActivateEffect("yoga_outfit_task_6")],
                    "complete": [QuestVisibleEffect("goal", "yoga_outfit_goal_7"), QuestVisibleEffect("task", "yoga_outfit_task_7"), QuestActivateEffect("yoga_outfit_task_7"), NotificationEffect("Goal completed!")],
                },
                EventTask("yoga_outfit_task_6", "", "Now I have an outfit, but I have no idea, what size to order. I should talk to Ms. Parker.", {}, "new_yoga_outfit_6"),
            ),
            Goal("yoga_outfit_goal_7", "Wait for the Nurse",
                "Progress time at school until Ms. Parker's nurse friend arrives for the health checkups.",
                {
                    "visible": [QuestVisibleEffect("task", "yoga_outfit_task_7"), QuestActivateEffect("yoga_outfit_task_7")],
                    "complete": [QuestVisibleEffect("goal", "yoga_outfit_goal_8"), QuestVisibleEffect("task", "yoga_outfit_task_8"), QuestActivateEffect("yoga_outfit_task_8"), NotificationEffect("Goal completed!")],
                },
                EventTask("yoga_outfit_task_7", "", "Ms. Parker agreed to ask her friend to help with the checkups. I should wait for her to come by.", {}, "new_yoga_outfit_7"),
            ),
            Goal("yoga_outfit_goal_8", "Announce Checkup Day",
                "Go to the gym during a yoga class and inform the students about the upcoming health checkup day.",
                {
                    "visible": [QuestVisibleEffect("task", "yoga_outfit_task_8"), QuestActivateEffect("yoga_outfit_task_8")],
                    "complete": [QuestVisibleEffect("goal", "yoga_outfit_goal_9"), QuestVisibleEffect("task", "yoga_outfit_task_9"), QuestActivateEffect("yoga_outfit_task_9"), NotificationEffect("Goal completed!")],
                },
                EventTask("yoga_outfit_task_8", "", "The nurse agreed to do a general health checkup. I should now go to the classes and announce the checkup-day.", {}, "new_yoga_outfit_8"),
            ),
            Goal("yoga_outfit_goal_9", "Attend Checkup Day",
                "Go to the gym on Tuesday morning during class time to oversee the health checkups.",
                {
                    "visible": [QuestVisibleEffect("task", "yoga_outfit_task_9"), QuestActivateEffect("yoga_outfit_task_9")],
                    "complete": [QuestVisibleEffect("goal", "yoga_outfit_goal_10"), QuestVisibleEffect("task", "yoga_outfit_task_10"), QuestActivateEffect("yoga_outfit_task_10"), NotificationEffect("Goal completed!")],
                },
                EventTask("yoga_outfit_task_9", "", "Okay, checkup-day starts on Tuesday during morning classes.", {}, "new_yoga_outfit_9"),
            ),
            Goal("yoga_outfit_goal_10", "Distribute the New Outfits",
                "Visit the gym after the outfits arrive and hand them out to the students.",
                {
                    "visible": [QuestVisibleEffect("task", "yoga_outfit_task_10"), QuestActivateEffect("yoga_outfit_task_10")],
                    "complete": [NotificationEffect("Goal completed!")],
                },
                EventTask("yoga_outfit_task_10", "", "Now with the results and the outfits ordered, I can finally give them to the students.", {}, "new_yoga_outfit_10"),
            ),
        )
    )

    # endregion
    ########################

    ######################
    # region Help Quests #

    # Max Stats
    $ quest_manager.load_quest(
        Quest("max_stats", "Max Stats Overview", "MaxGame",
            "Shows which values you need for certain stats to experience all current content.\nRaising these stats beyond the listed values will not unlock anything new in this version.\nUse this quest as a checklist to see which stats you are still missing.",
            "You have reached all required stat values and seen all stat-based content in this version.",
            "images/journal/journal/test_image.webp",
            {
                "hint": [
                    QuestVisibleEffect("quest", "max_stats"),
                    QuestVisibleEffect("goal", "max_stats_goal_1"),
                    QuestVisibleEffect("task", "max_stats_task_1"),
                    QuestActivateEffect("max_stats_task_1"),
                ],
                "complete": [NotificationEffect("Quest completed!")],
            },
            Goal("max_stats_goal_1", "Reach the Required Stats", "Raise your stats until they meet the listed thresholds.",
                {},
                ConditionTask("max_stats_task_1", "Check Your Stats", "stats", "Make sure your inhibition is at least 90 and your corruption is at least 5 to complete this goal.", {}, StatCondition(inhibition = "90-", corruption = "5+"))
            )
        )
    )

    # Max Events
    $ quest_manager.load_quest(
        Quest("max_events", "Max Events Overview", "MaxGame",
            "Shows all events that currently exist in the game and which ones you have already seen.\nThis quest does NOT track different variants or choices inside an event, only whether each base event has been triggered at least once.\nIt also only covers events that can occur during the free roam phase after the introduction is finished.",
            "You have seen every tracked event in the current version!",
            "images/journal/journal/test_image.webp",
            {
                "hint": [QuestVisibleEffect("quest", "max_events")],
                "complete": [NotificationEffect("Quest completed!")],
            },
            Goal("max_events_cafeteria", "Cafeteria Events", "Tracks all cafeteria events listed below. Visit the cafeteria at different times and with different conditions until each one has been triggered at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_cafeteria")]},
                EventTask("max_events_cafeteria_task_1", "Cafeteria Event 1", "Trigger and watch the first cafeteria event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_cafeteria_task_1"), QuestActivateEffect("max_events_cafeteria_task_1")]}, "cafeteria_event_1"),
                EventTask("max_events_cafeteria_task_2", "Cafeteria Event 2", "Trigger and watch the second cafeteria event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_cafeteria_task_2"), QuestActivateEffect("max_events_cafeteria_task_2")]}, "cafeteria_event_2"),
                EventTask("max_events_cafeteria_task_3", "Cafeteria Event 3", "Trigger and watch the third cafeteria event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_cafeteria_task_3"), QuestActivateEffect("max_events_cafeteria_task_3")]}, "cafeteria_event_3"),
                EventTask("max_events_cafeteria_task_4", "Cafeteria Event 4", "Trigger and watch the fourth cafeteria event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_cafeteria_task_4"), QuestActivateEffect("max_events_cafeteria_task_4")]}, "cafeteria_event_4"),
                EventTask("max_events_cafeteria_task_5", "Cafeteria Event 5", "Trigger and watch the fifth cafeteria event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_cafeteria_task_5"), QuestActivateEffect("max_events_cafeteria_task_5")]}, "cafeteria_event_5"),
                EventTask("max_events_cafeteria_task_6", "Cafeteria Event 6", "Trigger and watch the sixth cafeteria event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_cafeteria_task_6"), QuestActivateEffect("max_events_cafeteria_task_6")]}, "cafeteria_event_6"),
                EventTask("max_events_cafeteria_task_7", "Cafeteria Event 7", "Trigger and watch the seventh cafeteria event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_cafeteria_task_7"), QuestActivateEffect("max_events_cafeteria_task_7")]}, "cafeteria_event_7"),
            ),
            Goal("max_events_courtyard", "Courtyard Events", "Tracks all courtyard events listed below. Visit the courtyard at different times and on different days until each event has been triggered at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_courtyard")]},
                EventTask("max_events_courtyard_task_1", "Courtyard Event 1", "Trigger and watch the first courtyard event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_courtyard_task_1"), QuestActivateEffect("max_events_courtyard_task_1")]}, "courtyard_event_1"),
                EventTask("max_events_courtyard_task_2", "Courtyard Event 2", "Trigger and watch the second courtyard event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_courtyard_task_2"), QuestActivateEffect("max_events_courtyard_task_2")]}, "courtyard_event_2"),
                EventTask("max_events_courtyard_task_3", "Courtyard Event 3", "Trigger and watch the third courtyard event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_courtyard_task_3"), QuestActivateEffect("max_events_courtyard_task_3")]}, "courtyard_event_3"),
                EventTask("max_events_courtyard_task_4", "Courtyard Event 4", "Trigger and watch the fourth courtyard event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_courtyard_task_4"), QuestActivateEffect("max_events_courtyard_task_4")]}, "courtyard_event_4"),
                EventTask("max_events_courtyard_task_5", "Courtyard Event 5", "Trigger and watch the fifth courtyard event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_courtyard_task_5"), QuestActivateEffect("max_events_courtyard_task_5")]}, "courtyard_event_5"),
                EventTask("max_events_courtyard_task_6", "Courtyard Event 6", "Trigger and watch the sixth courtyard event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_courtyard_task_6"), QuestActivateEffect("max_events_courtyard_task_6")]}, "courtyard_event_6"),
                EventTask("max_events_courtyard_task_7", "Courtyard Event 7", "Trigger and watch the seventh courtyard event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_courtyard_task_7"), QuestActivateEffect("max_events_courtyard_task_7")]}, "courtyard_event_7"),
            ),
            Goal("max_events_gym", "Gym Events", "Tracks all gym events listed below. Visit the gym during different times and activities until each event has been triggered at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_gym")]},
                EventTask("max_events_gym_task_1", "Gym Event 1", "Trigger and watch the first gym event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_gym_task_1"), QuestActivateEffect("max_events_gym_task_1")]}, "gym_event_1"),
                EventTask("max_events_gym_task_2", "Gym Event 2", "Trigger and watch the second gym event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_gym_task_2"), QuestActivateEffect("max_events_gym_task_2")]}, "gym_event_2"),
                EventTask("max_events_gym_task_3", "Gym Event 3", "Trigger and watch the third gym event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_gym_task_3"), QuestActivateEffect("max_events_gym_task_3")]}, "gym_event_3"),
            ),
            Goal("max_events_kiosk", "Kiosk Events", "Tracks all kiosk events listed below. Visit the kiosk at different times and circumstances until each event has been triggered at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_kiosk")]},
                EventTask("max_events_kiosk_task_1", "Kiosk Event 1", "Trigger and watch the first kiosk event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_kiosk_task_1"), QuestActivateEffect("max_events_kiosk_task_1")]}, "kiosk_event_1"),
                EventTask("max_events_kiosk_task_2", "Kiosk Event 2", "Trigger and watch the second kiosk event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_kiosk_task_2"), QuestActivateEffect("max_events_kiosk_task_2")]}, "kiosk_event_2"),
                EventTask("max_events_kiosk_task_3", "Kiosk Event 3", "Trigger and watch the third kiosk event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_kiosk_task_3"), QuestActivateEffect("max_events_kiosk_task_3")]}, "kiosk_event_3"),
            ),
            Goal("max_events_office", "Office Building Events", "Tracks all office building events listed below. Spend time in and around the office building until each event has been triggered at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_office")]},
                EventTask("max_events_office_task_1", "Office Event 1", "Trigger and watch the first office building event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_office_task_1"), QuestActivateEffect("max_events_office_task_1")]}, "office_event_1"),
                EventTask("max_events_office_task_2", "Office Event 2", "Trigger and watch the second office building event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_office_task_2"), QuestActivateEffect("max_events_office_task_2")]}, "office_event_2"),
                EventTask("max_events_office_task_3", "Office Event 3", "Trigger and watch the third office building event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_office_task_3"), QuestActivateEffect("max_events_office_task_3")]}, "office_event_3"),
                EventTask("max_events_office_task_4", "Office Event 4", "Trigger and watch the fourth office building event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_office_task_4"), QuestActivateEffect("max_events_office_task_4")]}, "office_event_4"),
                EventTask("max_events_office_task_5", "Office Work Event: First Naughty Session", "Trigger and watch the first naughty office work session event.", {"hint":[QuestVisibleEffect("task", "max_events_office_task_5"), QuestActivateEffect("max_events_office_task_5")]}, "work_office_session_event_first_naughty"),
                EventTask("max_events_office_task_6", "Office Work Event: Regular Session", "Trigger and watch a regular office work session event.", {"hint":[QuestVisibleEffect("task", "max_events_office_task_6"), QuestActivateEffect("max_events_office_task_6")]}, "work_office_session_event_1"),
                EventTask("max_events_office_task_7", "Office Work Event: Reputation", "Trigger and watch the office reputation-related work event.", {"hint":[QuestVisibleEffect("task", "max_events_office_task_7"), QuestActivateEffect("max_events_office_task_7")]}, "work_office_reputation_event_1"),
                EventTask("max_events_office_task_8", "Office Work Event: Money", "Trigger and watch the office money-related work event.", {"hint":[QuestVisibleEffect("task", "max_events_office_task_8"), QuestActivateEffect("max_events_office_task_8")]}, "work_office_money_event_1"),
                EventTask("max_events_office_task_9", "Office Work Event: Education", "Trigger and watch the office education-related work event.", {"hint":[QuestVisibleEffect("task", "max_events_office_task_9"), QuestActivateEffect("max_events_office_task_9")]}, "work_office_education_event_1"),
            ),
            Goal("max_events_school_building", "School Building Events", "Tracks all school building events listed below. Explore the school building during free roam until each event has been triggered at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_school_building")]},
                EventTask("max_events_school_building_task_1", "School Building Event 1", "Trigger and watch the first school building event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_school_building_task_1"), QuestActivateEffect("max_events_school_building_task_1")]}, "sb_event_1"),
                EventTask("max_events_school_building_task_3", "School Building Event 3", "Trigger and watch the third school building event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_school_building_task_3"), QuestActivateEffect("max_events_school_building_task_3")]}, "sb_event_3"),
                EventTask("max_events_school_building_task_4", "School Building Event 4", "Trigger and watch the fourth school building event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_school_building_task_4"), QuestActivateEffect("max_events_school_building_task_4")]}, "sb_event_4"),
                EventTask("max_events_school_building_task_5", "School Building Event 5", "Trigger and watch the fifth school building event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_school_building_task_5"), QuestActivateEffect("max_events_school_building_task_5")]}, "sb_event_5"),
                EventTask("max_events_school_building_task_6", "School Building Event 6", "Trigger and watch the sixth school building event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_school_building_task_6"), QuestActivateEffect("max_events_school_building_task_6")]}, "sb_event_6"),
                EventTask("max_events_school_building_task_7", "School Building Event 7", "Trigger and watch the seventh school building event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_school_building_task_7"), QuestActivateEffect("max_events_school_building_task_7")]}, "sb_event_7"),
            ),
            Goal("max_events_school_dormitory", "School Dormitory Events", "Tracks all school dormitory events listed below. Visit the dormitory, especially in the evenings and at night, until each event has been triggered at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_school_dormitory")]},
                EventTask("max_events_school_dormitory_task_1", "Dormitory Event 1", "Trigger and watch the first dormitory event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_school_dormitory_task_1"), QuestActivateEffect("max_events_school_dormitory_task_1")]}, "sd_event_1"),
                EventTask("max_events_school_dormitory_task_3", "Dormitory Event 3", "Trigger and watch the third dormitory event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_school_dormitory_task_3"), QuestActivateEffect("max_events_school_dormitory_task_3")]}, "sd_event_3"),
                EventTask("max_events_school_dormitory_task_4", "Dormitory Event 4", "Trigger and watch the fourth dormitory event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_school_dormitory_task_4"), QuestActivateEffect("max_events_school_dormitory_task_4")]}, "sd_event_4"),
                EventTask("max_events_school_dormitory_task_5", "Dormitory Event 5", "Trigger and watch the fifth dormitory event during free roam.", {"hint":[QuestVisibleEffect("task", "max_events_school_dormitory_task_5"), QuestActivateEffect("max_events_school_dormitory_task_5")]}, "sd_event_5"),
            ),
            Goal("max_events_truth_or_dare", "Truth or Dare Events", "Tracks all Truth or Dare events and fragments listed below. Progress the Truth or Dare quest and revisit the dorm at night until every entry here has been triggered at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_truth_or_dare")]},
                EventTask("max_events_truth_or_dare_task_1", "Truth or Dare Event 1", "Trigger and watch the first Truth or Dare event.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_1"), QuestActivateEffect("max_events_truth_or_dare_task_1")]}, "truth_or_dare_1"),
                EventTask("max_events_truth_or_dare_task_2", "Truth or Dare Event 2", "Trigger and watch the second Truth or Dare event.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_2"), QuestActivateEffect("max_events_truth_or_dare_task_2")]}, "truth_or_dare_2"),
                EventTask("max_events_truth_or_dare_task_3", "Truth or Dare Event 3", "Trigger and watch the third Truth or Dare event.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_3"), QuestActivateEffect("max_events_truth_or_dare_task_3")]}, "truth_or_dare_3"),
                TaskGroup("max_events_truth_or_dare_task_group_1", "Truth Fragments", "Tracks all 'truth' mini-scenes that can appear during the Truth or Dare game.",
                    {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_1")]},
                    EventTask("max_events_truth_or_dare_task_group_1_task_1", "Truth Fragment 1", "Trigger and watch the first 'truth' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_1_task_1"), QuestActivateEffect("max_events_truth_or_dare_task_group_1_task_1")]}, "truth_or_dare_truth_1"),
                    EventTask("max_events_truth_or_dare_task_group_1_task_2", "Truth Fragment 2", "Trigger and watch the second 'truth' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_1_task_2"), QuestActivateEffect("max_events_truth_or_dare_task_group_1_task_2")]}, "truth_or_dare_truth_2"),
                    EventTask("max_events_truth_or_dare_task_group_1_task_3", "Truth Fragment 3", "Trigger and watch the third 'truth' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_1_task_3"), QuestActivateEffect("max_events_truth_or_dare_task_group_1_task_3")]}, "truth_or_dare_truth_3"),
                    EventTask("max_events_truth_or_dare_task_group_1_task_4", "Truth Fragment 4", "Trigger and watch the fourth 'truth' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_1_task_4"), QuestActivateEffect("max_events_truth_or_dare_task_group_1_task_4")]}, "truth_or_dare_truth_4"),
                    EventTask("max_events_truth_or_dare_task_group_1_task_5", "Truth Fragment 5", "Trigger and watch the fifth 'truth' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_1_task_5"), QuestActivateEffect("max_events_truth_or_dare_task_group_1_task_5")]}, "truth_or_dare_truth_5"),
                    EventTask("max_events_truth_or_dare_task_group_1_task_6", "Truth Fragment 6", "Trigger and watch the sixth 'truth' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_1_task_6"), QuestActivateEffect("max_events_truth_or_dare_task_group_1_task_6")]}, "truth_or_dare_truth_6"),
                ),
                TaskGroup("max_events_truth_or_dare_task_group_2", "Dare Fragments", "Tracks all 'dare' mini-scenes that can appear during the Truth or Dare game.",
                    {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_2")]},
                    EventTask("max_events_truth_or_dare_task_group_2_task_1", "Dare Fragment 1", "Trigger and watch the first 'dare' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_2_task_1"), QuestActivateEffect("max_events_truth_or_dare_task_group_2_task_1")]}, "truth_or_dare_dare_1"),
                    EventTask("max_events_truth_or_dare_task_group_2_task_2", "Dare Fragment 2", "Trigger and watch the second 'dare' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_2_task_2"), QuestActivateEffect("max_events_truth_or_dare_task_group_2_task_2")]}, "truth_or_dare_dare_2"),
                    EventTask("max_events_truth_or_dare_task_group_2_task_3", "Dare Fragment 3", "Trigger and watch the third 'dare' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_2_task_3"), QuestActivateEffect("max_events_truth_or_dare_task_group_2_task_3")]}, "truth_or_dare_dare_3"),
                    EventTask("max_events_truth_or_dare_task_group_2_task_4", "Dare Fragment 4", "Trigger and watch the fourth 'dare' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_2_task_4"), QuestActivateEffect("max_events_truth_or_dare_task_group_2_task_4")]}, "truth_or_dare_dare_4"),
                    EventTask("max_events_truth_or_dare_task_group_2_task_5", "Dare Fragment 5", "Trigger and watch the fifth 'dare' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_2_task_5"), QuestActivateEffect("max_events_truth_or_dare_task_group_2_task_5")]}, "truth_or_dare_dare_5"),
                    EventTask("max_events_truth_or_dare_task_group_2_task_6", "Dare Fragment 6", "Trigger and watch the sixth 'dare' fragment during the Truth or Dare game.", {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_2_task_6"), QuestActivateEffect("max_events_truth_or_dare_task_group_2_task_6")]}, "truth_or_dare_dare_6"),
                ),
            ),
            Goal("max_events_new_yoga_outfit", "New Yoga Outfit Events", "Tracks all events from the 'New Yoga Outfit' quest. Progress that quest and revisit the gym and office until every event below has been triggered at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_new_yoga_outfit")]},
                EventTask("max_events_new_yoga_outfit_task_1",  "New Yoga Outfit Event 1", "Trigger and watch the first event in the 'New Yoga Outfit' quest line.", {"hint":[QuestVisibleEffect("task", "max_events_new_yoga_outfit_task_1"),  QuestActivateEffect("max_events_new_yoga_outfit_task_1")]},  "new_yoga_outfit_1"),
                EventTask("max_events_new_yoga_outfit_task_2",  "New Yoga Outfit Event 2", "Trigger and watch the second event in the 'New Yoga Outfit' quest line.", {"hint":[QuestVisibleEffect("task", "max_events_new_yoga_outfit_task_2"),  QuestActivateEffect("max_events_new_yoga_outfit_task_2")]},  "new_yoga_outfit_2"),
                EventTask("max_events_new_yoga_outfit_task_3",  "New Yoga Outfit Event 3", "Trigger and watch the third event in the 'New Yoga Outfit' quest line.", {"hint":[QuestVisibleEffect("task", "max_events_new_yoga_outfit_task_3"),  QuestActivateEffect("max_events_new_yoga_outfit_task_3")]},  "new_yoga_outfit_3"),
                EventTask("max_events_new_yoga_outfit_task_4",  "New Yoga Outfit Event 4", "Trigger and watch the fourth event in the 'New Yoga Outfit' quest line.", {"hint":[QuestVisibleEffect("task", "max_events_new_yoga_outfit_task_4"),  QuestActivateEffect("max_events_new_yoga_outfit_task_4")]},  "new_yoga_outfit_4"),
                EventTask("max_events_new_yoga_outfit_task_5",  "New Yoga Outfit Event 5", "Trigger and watch the fifth event in the 'New Yoga Outfit' quest line.", {"hint":[QuestVisibleEffect("task", "max_events_new_yoga_outfit_task_5"),  QuestActivateEffect("max_events_new_yoga_outfit_task_5")]},  "new_yoga_outfit_5"),
                EventTask("max_events_new_yoga_outfit_task_6",  "New Yoga Outfit Event 6", "Trigger and watch the sixth event in the 'New Yoga Outfit' quest line.", {"hint":[QuestVisibleEffect("task", "max_events_new_yoga_outfit_task_6"),  QuestActivateEffect("max_events_new_yoga_outfit_task_6")]},  "new_yoga_outfit_6"),
                EventTask("max_events_new_yoga_outfit_task_7",  "New Yoga Outfit Event 7", "Trigger and watch the seventh event in the 'New Yoga Outfit' quest line.", {"hint":[QuestVisibleEffect("task", "max_events_new_yoga_outfit_task_7"),  QuestActivateEffect("max_events_new_yoga_outfit_task_7")]},  "new_yoga_outfit_7"),
                EventTask("max_events_new_yoga_outfit_task_8",  "New Yoga Outfit Event 8", "Trigger and watch the eighth event in the 'New Yoga Outfit' quest line.", {"hint":[QuestVisibleEffect("task", "max_events_new_yoga_outfit_task_8"),  QuestActivateEffect("max_events_new_yoga_outfit_task_8")]},  "new_yoga_outfit_8"),
                EventTask("max_events_new_yoga_outfit_task_9",  "New Yoga Outfit Event 9", "Trigger and watch the ninth event in the 'New Yoga Outfit' quest line.", {"hint":[QuestVisibleEffect("task", "max_events_new_yoga_outfit_task_9"),  QuestActivateEffect("max_events_new_yoga_outfit_task_9")]},  "new_yoga_outfit_9"),
                EventTask("max_events_new_yoga_outfit_task_10", "New Yoga Outfit Event 10", "Trigger and watch the final event in the 'New Yoga Outfit' quest line.", {"hint":[QuestVisibleEffect("task", "max_events_new_yoga_outfit_task_10"), QuestActivateEffect("max_events_new_yoga_outfit_task_10")]}, "new_yoga_outfit_10"),
            ),
            Goal("max_events_teaching_sex_ed", "Sex Education Teaching Events", "Tracks all classroom sex education teaching events. Teach sex ed lessons and replay classes until each fragment below has occurred at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_teaching_sex_ed")]},
                TaskGroup("max_events_teaching_sex_ed_task_group_1", "Intro Fragments", "Tracks the introductory sex education classroom fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_truth_or_dare_task_group_1")]},
                    EventTask("max_events_teaching_sex_ed_task_group_1_task_1", "Intro Fragment: Anatomy", "Trigger and watch the introductory anatomy-focused sex ed fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_sex_ed_task_group_1_task_1"), QuestActivateEffect("max_events_teaching_sex_ed_task_group_1_task_1")]}, "sb_teach_sex_ed_intro_anatomy"),
                    EventTask("max_events_teaching_sex_ed_task_group_1_task_2", "Intro Fragment: Curiosity", "Trigger and watch the introductory curiosity-focused sex ed fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_sex_ed_task_group_1_task_2"), QuestActivateEffect("max_events_teaching_sex_ed_task_group_1_task_2")]}, "sb_teach_sex_ed_intro_sex_curiosity"),
                ),
                TaskGroup("max_events_teaching_sex_ed_task_group_2", "Main Fragments", "Tracks the main sex education classroom fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_sex_ed_task_group_2")]},
                    EventTask("max_events_teaching_sex_ed_task_group_2_task_1", "Main Fragment: Anatomy", "Trigger and watch a main anatomy-focused sex ed fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_sex_ed_task_group_2_task_1"), QuestActivateEffect("max_events_teaching_sex_ed_task_group_2_task_1")]}, "sb_teach_sex_ed_main_anatomy_1"),
                    EventTask("max_events_teaching_sex_ed_task_group_2_task_2", "Main Fragment: Curiosity", "Trigger and watch a main curiosity-focused sex ed fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_sex_ed_task_group_2_task_2"), QuestActivateEffect("max_events_teaching_sex_ed_task_group_2_task_2")]}, "sb_teach_sex_ed_main_sex_curiosity_1"),
                ),
                TaskGroup("max_events_teaching_sex_ed_task_group_3", "QA Fragments", "Tracks the sex education Q&A classroom fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_sex_ed_task_group_3")]},
                    EventTask("max_events_teaching_sex_ed_task_group_3_task_1", "Q&A Fragment 1", "Trigger and watch the first sex ed Q&A fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_sex_ed_task_group_3_task_1"), QuestActivateEffect("max_events_teaching_sex_ed_task_group_3_task_1")]}, "sb_teach_sex_ed_qa_1"),
                    EventTask("max_events_teaching_sex_ed_task_group_3_task_2", "Q&A Fragment 2", "Trigger and watch the second sex ed Q&A fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_sex_ed_task_group_3_task_2"), QuestActivateEffect("max_events_teaching_sex_ed_task_group_3_task_2")]}, "sb_teach_sex_ed_qa_2"),
                ),
            ),
            Goal("max_events_teaching_pe", "PE Teaching Events", "Tracks all P.E. teaching events. Teach P.E. classes and repeat them until each fragment below has occurred at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_teaching_pe")]},
                TaskGroup("max_events_teaching_pe_task_group_1", "Intro Fragments", "Tracks introductory P.E. teaching fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_1")]},
                    EventTask("max_events_teaching_pe_task_group_1_task_1", "Intro Fragment: P.E. Lesson", "Trigger and watch an introductory P.E. teaching fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_1_task_1"), QuestActivateEffect("max_events_teaching_pe_task_group_1_task_1")]}, "gym_teach_pe_intro_2"),
                    EventTask("max_events_teaching_pe_task_group_1_task_2", "Intro Fragment: Aona's Bra", "Trigger and watch the introductory P.E. fragment involving Aona's bra.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_1_task_2"), QuestActivateEffect("max_events_teaching_pe_task_group_1_task_2")]}, "gym_teach_pe_intro_aona_bra"),
                ),
                TaskGroup("max_events_teaching_pe_task_group_2", "Entrance Fragments", "Tracks P.E. entrance-related teaching fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_2")]},
                    EventTask("max_events_teaching_pe_task_group_2_task_1", "Entrance Fragment 1", "Trigger and watch a P.E. entrance fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_2_task_1"), QuestActivateEffect("max_events_teaching_pe_task_group_2_task_1")]}, "gym_teach_pe_entrance_1"),
                ),
                TaskGroup("max_events_teaching_pe_task_group_3", "Warm Up Fragments", "Tracks P.E. warm-up teaching fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_3")]},
                    EventTask("max_events_teaching_pe_task_group_3_task_1", "Warm Up Fragment 1", "Trigger and watch a P.E. warm-up fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_3_task_1"), QuestActivateEffect("max_events_teaching_pe_task_group_3_task_1")]}, "gym_teach_pe_warm_up_1"),
                ),
                TaskGroup("max_events_teaching_pe_task_group_4", "Main Fragments", "Tracks the main P.E. teaching fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_4")]},
                    EventTask("max_events_teaching_pe_task_group_4_task_1", "Main Fragment 1", "Trigger and watch a main P.E. teaching fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_4_task_1"), QuestActivateEffect("max_events_teaching_pe_task_group_4_task_1")]}, "gym_teach_pe_main_1"),
                    EventTask("max_events_teaching_pe_task_group_4_task_2", "Main Fragment: Aona's Bra", "Trigger and watch the main P.E. teaching fragment involving Aona's bra.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_4_task_2"), QuestActivateEffect("max_events_teaching_pe_task_group_4_task_2")]}, "gym_teach_pe_main_aona_bra"),
                ),
                TaskGroup("max_events_teaching_pe_task_group_5", "End Fragments", "Tracks the ending P.E. teaching fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_5")]},
                    EventTask("max_events_teaching_pe_task_group_5_task_1", "End Fragment 1", "Trigger and watch a P.E. class ending fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_pe_task_group_5_task_1"), QuestActivateEffect("max_events_teaching_pe_task_group_5_task_1")]}, "gym_teach_pe_end_1"),
                ),
            ),
            Goal("max_events_teaching_math", "Math Teaching Events", "Tracks all math teaching events. Teach math lessons and replay them until each fragment below has occurred at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_teaching_math")]},
                TaskGroup("max_events_teaching_math_task_group_1", "Intro Fragments", "Tracks introductory math teaching fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_math_task_group_1")]},
                    EventTask("max_events_teaching_math_task_group_1_task_1", "Intro Fragment: Math 1", "Trigger and watch the first introductory math class fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_math_task_group_1_task_1"), QuestActivateEffect("max_events_teaching_math_task_group_1_task_1")]}, "sb_teach_math_ld_1"),
                    EventTask("max_events_teaching_math_task_group_1_task_2", "Intro Fragment: Math 2", "Trigger and watch the second introductory math class fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_math_task_group_1_task_2"), QuestActivateEffect("max_events_teaching_math_task_group_1_task_2")]}, "sb_teach_math_ld_2"),
                    EventTask("max_events_teaching_math_task_group_1_task_3", "Intro Fragment: Math 3", "Trigger and watch the third introductory math class fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_math_task_group_1_task_3"), QuestActivateEffect("max_events_teaching_math_task_group_1_task_3")]}, "sb_teach_math_ld_3"),
                ),
                TaskGroup("max_events_teaching_math_task_group_2", "Main Fragments", "Tracks the main math teaching fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_math_task_group_2")]},
                    EventTask("max_events_teaching_math_task_group_2_task_1", "Main Fragment: Math 1", "Trigger and watch the first main math class fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_math_task_group_2_task_1"), QuestActivateEffect("max_events_teaching_math_task_group_2_task_1")]}, "sb_teach_math_main_1"),
                    EventTask("max_events_teaching_math_task_group_2_task_2", "Main Fragment: Math 2", "Trigger and watch the second main math class fragment.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_math_task_group_2_task_2"), QuestActivateEffect("max_events_teaching_math_task_group_2_task_2")]}, "sb_teach_math_main_2"),
                ),
            ),
            Goal("max_events_teaching_history", "History Teaching Events", "Tracks all history teaching events. Teach history lessons and replay them until each fragment below has occurred at least once.",
                {"hint":[QuestVisibleEffect("goal", "max_events_teaching_history")]},
                TaskGroup("max_events_teaching_history_task_group_1", "Intro Fragments", "Tracks introductory history teaching fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_history_task_group_1")]},
                    EventTask("max_events_teaching_history_task_group_1_task_1", "Intro Fragment: Revolution", "Trigger and watch the introductory history class fragment about the revolution.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_history_task_group_1_task_1"), QuestActivateEffect("max_events_teaching_history_task_group_1_task_1")]}, "sb_teach_history_intro_f_revolution_1"),
                ),
                TaskGroup("max_events_teaching_history_task_group_2", "Main Fragments", "Tracks main history teaching fragments.",
                    {"hint":[QuestVisibleEffect("task", "max_events_teaching_history_task_group_2")]},
                    EventTask("max_events_teaching_history_task_group_2_task_1", "Main Fragment: Revolution 1", "Trigger and watch the first main history class fragment about the revolution.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_history_task_group_2_task_1"), QuestActivateEffect("max_events_teaching_history_task_group_2_task_1")]}, "sb_teach_history_main_f_revolution_1"),
                    EventTask("max_events_teaching_history_task_group_2_task_2", "Main Fragment: Revolution 2", "Trigger and watch the second main history class fragment about the revolution.", {"hint":[QuestVisibleEffect("task", "max_events_teaching_history_task_group_2_task_2"), QuestActivateEffect("max_events_teaching_history_task_group_2_task_2")]}, "sb_teach_history_main_f_revolution_2"),
                ),
            ),
            Goal("max_events_aonas_new_bra", "Aona needs a new Bra!", "Tracks all events connected to Aona's sports bra and replacement.",
                {"hint":[QuestVisibleEffect("goal", "max_events_aonas_new_bra")]},
                EventTask("max_events_aonas_new_bra_task_1", "Aona Bra Event 1", "Trigger and watch the first P.E. event involving Aona's bra.", {"hint":[QuestVisibleEffect("task", "max_events_aonas_new_bra_task_1"), QuestActivateEffect("max_events_aonas_new_bra_task_1")]}, "gym_teach_pe_intro_anoa_bra"),
                EventTask("max_events_aonas_new_bra_task_2", "Aona Bra Event 2", "Trigger and watch the main P.E. event involving Aona's bra.", {"hint":[QuestVisibleEffect("task", "max_events_aonas_new_bra_task_2"), QuestActivateEffect("max_events_aonas_new_bra_task_2")]}, "gym_teach_pe_main_aona_bra"),
                EventTask("max_events_aonas_new_bra_task_3", "Aona Bra Event 3", "Trigger and watch the follow-up P.E. event involving Aona's bra.", {"hint":[QuestVisibleEffect("task", "max_events_aonas_new_bra_task_3"), QuestActivateEffect("max_events_aonas_new_bra_task_3")]}, "gym_teach_pe_main_aona_bra_2"),
                EventTask("max_events_aonas_new_bra_task_4", "Aona Bra Event 4", "Trigger and watch the office event connected to Aona's sports bra.", {"hint":[QuestVisibleEffect("task", "max_events_aonas_new_bra_task_4"), QuestActivateEffect("max_events_aonas_new_bra_task_4")]}, "aona_sports_bra_event_1"),
            ),
            Goal("max_events_sex_ed_intro", "Sex Education Intro Events", "Tracks all introductory events that unlock theoretical sex education at the school.",
                {"hint":[QuestVisibleEffect("goal", "max_events_sex_ed_intro")]},
                EventTask("max_events_sex_ed_intro_task_1",  "Intro: Call Emiko", "Trigger and watch the office call with Emiko about sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_1"),  QuestActivateEffect("max_events_sex_ed_intro_task_1")]},  "office_call_secretary_1"),
                EventTask("max_events_sex_ed_intro_task_2",  "Intro: Teacher Meeting 1", "Trigger and watch the first office meeting with the teachers about sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_2"),  QuestActivateEffect("max_events_sex_ed_intro_task_2")]},  "office_teacher_sex_ed_introduction_1"),
                EventTask("max_events_sex_ed_intro_task_3",  "Intro: Teacher Meeting 2", "Trigger and watch the second office meeting with the teachers about sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_3"),  QuestActivateEffect("max_events_sex_ed_intro_task_3")]},  "office_teacher_sex_ed_introduction_2"),
                EventTask("max_events_sex_ed_intro_task_4",  "Intro: Teacher Meeting 3", "Trigger and watch the third office meeting with the teachers about sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_4"),  QuestActivateEffect("max_events_sex_ed_intro_task_4")]},  "office_teacher_sex_ed_introduction_3"),
                EventTask("max_events_sex_ed_intro_task_5",  "Intro: Teacher Meeting 4", "Trigger and watch the final office meeting with the teachers about sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_5"),  QuestActivateEffect("max_events_sex_ed_intro_task_5")]},  "office_teacher_sex_ed_introduction_4"),
                EventTask("max_events_sex_ed_intro_task_6",  "Intro: PTA Discussion", "Trigger and watch the PTA discussion about theoretical sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_6"),  QuestActivateEffect("max_events_sex_ed_intro_task_6")]},  "pta_discussion_sex_ed_intro_1"),
                EventTask("max_events_sex_ed_intro_task_7",  "Intro: PTA Vote", "Trigger and watch the PTA vote on theoretical sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_7"),  QuestActivateEffect("max_events_sex_ed_intro_task_7")]},  "pta_vote_theoretical_sex_ed_1"),
                EventTask("max_events_sex_ed_intro_task_8",  "Intro: School Assembly", "Trigger and watch the school assembly announcing theoretical sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_8"),  QuestActivateEffect("max_events_sex_ed_intro_task_8")]},  "theoretical_sex_ed_assembly_1"),
                EventTask("max_events_sex_ed_intro_task_9",  "Mini Scene: Sex Ed Hallway 1", "Trigger and watch the first hallway mini-scene reacting to sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_9"),  QuestActivateEffect("max_events_sex_ed_intro_task_9")]},  "sex_ed_intro_mini_sd_1"),
                EventTask("max_events_sex_ed_intro_task_10", "Mini Scene: Sex Ed Hallway 2", "Trigger and watch the second hallway mini-scene reacting to sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_10"), QuestActivateEffect("max_events_sex_ed_intro_task_10")]}, "sex_ed_intro_mini_sd_2"),
                EventTask("max_events_sex_ed_intro_task_11", "Mini Scene: Sex Ed Courtyard", "Trigger and watch the courtyard mini-scene reacting to sex education.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_11"), QuestActivateEffect("max_events_sex_ed_intro_task_11")]}, "sex_ed_intro_mini_courtyard_1"),
                EventTask("max_events_sex_ed_intro_task_12", "First Sex Ed Day", "Trigger and watch the first in-school sex education day event.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_12"), QuestActivateEffect("max_events_sex_ed_intro_task_12")]}, "first_sex_ed_day"),
                EventTask("max_events_sex_ed_intro_task_13", "First Sex Ed Class", "Trigger and watch the first theoretical sex education class.", {"hint":[QuestVisibleEffect("task", "max_events_sex_ed_intro_task_13"), QuestActivateEffect("max_events_sex_ed_intro_task_13")]}, "first_sex_ed_class_1"),
            ),
            Goal("max_events_naughty", "Naughty Sandbox Events", "Tracks the special naughty sandbox office call event.",
                {"hint":[QuestVisibleEffect("goal", "max_events_naughty")]},
                EventTask("max_events_naughty_task_1", "Naughty Sandbox Call", "Trigger and watch the office call that unlocks the naughty sandbox.", {"hint":[QuestVisibleEffect("task", "max_events_naughty_task_1"), QuestActivateEffect("max_events_naughty_task_1")]}, "office_call_secretary_naughty_sandbox"),
            ),
        )
    )

    # Unlock School Jobs
    $ quest_manager.load_quest(
        Quest("unlock_school_jobs", "Unlock School jobs", "Help Quests",
            "This quest is a help that shows how to unlock the school jobs rule.",
            "The school jobs rule is now unlocked.",
            "images/journal/rules/school_jobs_1.webp",
            {
                "hint": [QuestVisibleEffect("quest", "unlock_school_jobs"), QuestActivateEffect("complete_unlock_school_jobs")],
            },
            JournalUnlockTask("complete_unlock_school_jobs", "", "",
                {
                    "complete": [
                        QuestCompleteEffect("quest", "unlock_school_jobs"),
                        QuestCompleteEffect("goal", "unlock_school_jobs_1"),
                        QuestCompleteEffect("task", "unlock_school_jobs_1_task_1"),
                        QuestCompleteEffect("goal", "unlock_school_jobs_2"),
                        QuestCompleteEffect("task", "unlock_school_jobs_2_task_1"),
                        QuestCompleteEffect("goal", "unlock_school_jobs_3"),
                        QuestCompleteEffect("task", "unlock_school_jobs_3_task_1"),
                    ],
                },
                "school_jobs"
            ),
            Goal("unlock_school_jobs_1", "", "Reopen the Cafeteria.",
                {"hint": [QuestVisibleEffect("goal", "unlock_school_jobs_1")]},
                JournalUnlockTask("unlock_school_jobs_1_task_1", "", "", 
                    {"hint": [QuestVisibleEffect("task", "unlock_school_jobs_1_task_1"), QuestActivateEffect("unlock_school_jobs_1_task_1")]}, 
                    "cafeteria"
                )
            ),
            Goal("unlock_school_jobs_2", "", "Order some Food in the Cafeteria and observe Adelaide getting a bit overwhelmed.",
                {"hint": [QuestVisibleEffect("goal", "unlock_school_jobs_2")]},
                EventValueTask("unlock_school_jobs_2_task_1", "", "", 
                    {"hint": [QuestVisibleEffect("task", "unlock_school_jobs_2_task_1"), QuestActivateEffect("unlock_school_jobs_2_task_1")]}, 
                    "cafeteria", 3, {"topic": "overwhelmed"}
                )
            ),
            Goal("unlock_school_jobs_3", "", "Get the PTA to vote for the introduction of jobs for the students.",
                {"hint": [QuestVisibleEffect("goal", "unlock_school_job_3")]},
                JournalUnlockTask("unlock_school_jobs_3_task_1", "", "", 
                    {"hint": [QuestVisibleEffect("task", "unlock_school_jobs_3_task_1"), QuestActivateEffect("unlock_school_jobs_3_task_1")]}, 
                    "school_jobs"
                )
            )
        )
    )

    # Unlock Cafeteria
    $ quest_manager.load_quest(
        Quest("unlock_cafeteria", "Unlock Cafeteria", "Help Quests",
            "This quest is a help to show how to unlock the cafeteria.",
            "The cafeteria is now completed.",
            "images/journal/buildings/cafeteria 1 0_full.webp",
            {
                "hint": [QuestVisibleEffect("quest", "unlock_cafeteria"), QuestActivateEffect("complete_unlock_cafeteria")],
            },
            JournalUnlockTask("complete_unlock_cafeteria", "", "",
                {
                    "complete": [
                        QuestCompleteEffect("quest", "unlock_cafeteria"),
                        QuestCompleteEffect("quest", "unlock_cafeteria_1"),
                    ]
                },
                "cafeteria"
            ),
            Goal("unlock_cafeteria_1", "", "Get yourself a snack at the kiosk.",
                {"hint": [QuestVisibleEffect("goal", "unlock_cafeteria_1")]},
                TriggerTask("unlock_cafeteria_1_task_1", "Observe the Kindness of the Kiosk Clerk.", 
                    {"hint": [QuestVisibleEffect("task", "unlock_cafeteria_1_task_1"), QuestActivateEffect("unlock_cafeteria_1_task_1")]}
                )
            ),
            Goal("unlock_cafeteria_2", "", "Get the PTA to vote for the renovation and reopening of the cafeteria.",
                {"hint": [QuestVisibleEffect("goal", "unlock_cafeteria_2")]},
                JournalUnlockTask("unlock_cafeteria_2_task_1", "", "Unlock the Cafeteria Building in PTA.", 
                    {"hint": [QuestVisibleEffect("task", "unlock_cafeteria_2_task_1"), QuestActivateEffect("unlock_cafeteria_2_task_1")]},
                    "cafeteria"
                )
            ),
            Goal("unlock_cafeteria_3", "", "Wait for the Cafeteria to be finished.",
                {"hint": [QuestVisibleEffect("goal", "unlock_cafeteria_3")]},
                TriggerTask("unlock_cafeteria_3_task_1", "Wait for the Cafeteria to be finished.", 
                    {"hint": [QuestVisibleEffect("task", "unlock_cafeteria_3_task_1"), QuestActivateEffect("unlock_cafeteria_3_task_1")]}
                )
            ),
        )
    )

    # Unlock Student Relationships
    $ quest_manager.load_quest(
        Quest("unlock_student_relations", "Unlock Student Relations", "Help Quests",
            "This quest is a help that shows how to unlock the rule allowing students to have a relationship between each other.",
            "The rule for student relationships is now unlocked",
            "images/journal/rules/student_student_relation 1 0_full.webp",
            {
                "hint": [QuestVisibleEffect("quest", "unlocks_students_relations"), QuestActivateEffect("complete_unlock_student_relations")]
            },
            JournalUnlockTask("complete_unlock_student_relations", "", "",
                {
                    "complete": [
                        QuestCompleteEffect("quest", "unlock_student_relations"),
                        QuestCompleteEffect("goal", "unlock_student_relations_1"),
                        QuestCompleteEffect("task", "unlock_student_relations_1_task_1"),
                        QuestCompleteEffect("goal", "unlock_student_relations_2"),
                        QuestCompleteEffect("task", "unlock_student_relations_2_task_1"),
                        QuestCompleteEffect("goal", "unlock_student_relations_3"),
                        QuestCompleteEffect("task", "unlock_student_relations_3_task_1"),
                    ]
                },
                "student_student_relation"
            ),
            Goal("unlock_student_relations_1", "", "Look around the office for a bit.",
                {"hint": [QuestVisibleEffect("goal", "unlock_student_relations_1")]},
                EventTask("unlock_student_relations_1_task_1", "", "Look around the office for a bit.", 
                    {"hint": [QuestVisibleEffect("task", "unlock_student_relations_1_task_1"), QuestActivateEffect("unlock_student_relations_1_task_1")]},
                    "office_event_3"
                )
            ),
            Goal("unlock_student_relations_2", "", "Find two students sitting there because of the relationship.",
                {"hint": [QuestVisibleEffect("goal", "unlock_student_relations_2")]},
                TriggerTask("unlock_student_relations_2_task_1", "find two students sitting there because of the relationship.", 
                    {"hint": [QuestVisibleEffect("task", "unlock_student_relations_2_task_1"), QuestActivateEffect("unlock_student_relations_2_task_1")]}
                )
            ),
            Goal("unlock_student_relations_3", "", "Get the PTA to Vote for removal of the students relationship prohibition",
                {"hint": [QuestVisibleEffect("goal", "unlock_student_relations_3")]},
                JournalUnlockTask("unlock_student_relations_3_task_1", "", "Unlock the Student Relationship Rule in PTA.", 
                    {"hint": [QuestVisibleEffect("task", "unlock_student_relations_3_task_1"), QuestActivateEffect("unlock_student_relations_3_task_1")]}, 
                    "student_student_relation"
                ),
            ),
        )
    )

    # endregion
    ######################

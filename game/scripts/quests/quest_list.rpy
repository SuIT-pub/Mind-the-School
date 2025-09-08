init 1 python:

    def load_quest(quest: Quest):
        """
        Loads a quest into the game.

        ### Parameters:
        1. quest: Quest
            - The quest to be loaded
        """
        
        if not is_mod_active(active_mod_key):
            return

        global quests
        global quests_register
        category = quest.get_category()
        if category not in quests:
            quests[category] = {}
        if quest.get_key() not in quests[category].keys():
            quests[category][quest.get_key()] = quest
        else:
            quests[category][quest.get_key()].update_data(quest)

    def activate_quest(category: str, key: str):
        """
        Activates a quest for the player.

        ### Parameters:
        1. category: str
            - The category of the quest.
        2. key: str
            - The key of the quest.
        """

        if category in quests and key in quests[category]:
            quests[category][key].activate()
            add_notify_message(f"New Quest added for {get_translation(category)}!")

    def activate_goal(category: str, key: str, goal_key: str):
        """
        Activates a goal for a quest.

        ### Parameters:
        1. category: str
            - The category of the quest.
        2. key: str
            - The key of the quest.
        3. goal_key: str
            - The key of the goal.
        """

        if category in quests and key in quests[category]:
            quests[category][key].activate_goal(goal_key)

    def get_quest(category: str, key: str) -> Quest:
        """
        Returns a quest by its category and key.

        ### Parameters:
        1. category: str
            - The category of the quest.
        2. key: str
            - The key of the quest.

        ### Returns:
        1. Quest: 
            - The quest with the given category and key.
            - None if the quest doesn't exist.
        """

        if category in quests and key in quests[category]:
            return quests[category][key]
        return None

    def get_quests(category: str) -> Dict[str, Quest]:
        """
        Returns all quests of a category.

        ### Parameters:
        1. category: str
            - The category of the quests.

        ### Returns:
        1. Dict[str, Quest]:
            - A dictionary of quests with their keys as the keys.
            - None if the category doesn't exist.
        """

        if category in quests:
            return quests[category]
        return None

    def get_goal(category: str, key: str, goal_key: str) -> Goal:
        """
        Returns a goal of a quest by its category, key, and goal key.

        ### Parameters:
        1. category: str
            - The category of the quest.
        2. key: str
            - The key of the quest.
        3. goal_key: str
            - The key of the goal.

        ### Returns:
        1. Goal:
            - The goal with the given category, key, and goal key.
            - None if the goal doesn't exist.
        """

        if category in quests and key in quests[category]:
            return quests[category][key].get_goal(goal_key)
        return None

    def update_quest(key: str, **kwargs):
        """
        Updates the progress of a quest for all tasks registered under the key.

        ### Parameters:
        1. key: str
            - The key of the quest.
            - globally available keys: "event", "event_end", "trigger", "journal_unlock", "journal_upgrade", "schedule_voting", "stats", "map", "day_change", "daytime_change"
        2. **kwargs: dict
            - The parameters to be passed to the update method of the task.
        """

        for category in quests.keys():
            quests_list = [quests[category][quest] for quest in quests[category].keys() if (quests[category][quest].is_active() or (quests[category][quest].show_prematurely() and get_setting("journal_goals_show_note_setting")) or quests[category][quest].get_start_trigger()) and not quests[category][quest].all_active_done()]
            for quest in quests_list:
                quest.update(key, **kwargs)

    def update_all_quests(**kwargs):
        update_quest("x", **kwargs)

label load_quests:
    $ set_current_mod('base')

    ########################
    # region Normal Quests #

    # Aona's New Bra
    $ load_quest(
        Quest(
            "aonas_new_bra",
            "School",
            "Aona seems to be struggling during P.E. classes. Maybe you can help her out? Find out what's the Problem!",
            "images/events/misc/aona_sports_bra_event_1/aona_sports_bra_event_1 # 23.webp",
            "Aona got her new bra and is now ready for P.E. classes!",
            Goal(
                "aona_bra_event_1",
                "Teach some P.E. until you find out, what's the Problem.",
                EventTask("gym_teach_pe_main_aona_bra", check_history = True),
                trigger_activate = True,
                activate_next = True
            ),
            Goal(
                "aona_bra_event_2",
                "Drive Aona to the Shop.",
                EventTask("aona_sports_bra_event_1", check_history = True),
                activate_next = True,
                trigger_activate = True,
            ),
            Goal(
                "aona_bra_event_3",
                "Check if Aona is happy with her new bra.",
                EventTask("gym_teach_pe_main_aona_bra_2", check_history = True),
                trigger_activate = True,
            ),
            premature_visibility = True
        )
    )

    $ load_quest(
        Quest(
            "truth_or_dare",
            "School",
            "Some students seem to be playing some kind of game with each other. You should find out what it is. Best you snoop around a bit.",
            "images/events/truth_or_dare/truth_or_dare_4/card/truth_or_dare_4_card ikushi_ito 4 1.webp",
            "Great, now you can enjoy a nice show in the evening.",
            Goal(
                "truth_or_dare_1",
                "I wonder what that runner was about...",
                EventTask("truth_or_dare_1", check_history = True),
                premature_visibility = True,
                trigger_activate = True,
                activate_next = True
            ),
            Goal(
                "truth_or_dare_2",
                "The girls were talking about some kind of game in the halls. I should listen around a bit.",
                EventTask("truth_or_dare_2", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "truth_or_dare_3",
                "They seems to continue playing very soon. Now to find out where and when...",
                EventTask("truth_or_dare_3", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "truth_or_dare_4",
                "They regularly play this at night in the dorm. I should snoop a bit. Sounds interesting.",
                EventTask("truth_or_dare_4", check_history = True),
                trigger_activate = True
            ),
            premature_visibility = True
        )
    )

    $ load_quest(
        Quest(
            "yoga_outfit",
            "School",
            "Ms. Parker want's to hold yoga classes during P.E.. I should definitely support her.",
            "images/journal/journal/test_image.webp",
            "The new yoga outfits look very nice, and yoga is a really good way to stay fit.",
            Goal(
                "yoga_outfit_1",
                "Parker announced her yoga classes. I should stop by and check how she does.",
                EventTask("new_yoga_outfit_1", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "yoga_outfit_2",
                "I should have a look at her yoga classes, and see how she's doing.",
                EventTask("new_yoga_outfit_2", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "yoga_outfit_3",
                "Parker seems to be doing a great job. I should check back later.",
                EventTask("new_yoga_outfit_3", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "yoga_outfit_4",
                "Ms. Parker asked for proper yoga outfits. The current ones seem to be a bit too tight. But I need to find the right. Maybe some students like to help with that.",
                EventTask("new_yoga_outfit_4", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "yoga_outfit_5",
                "I've found a few volunteers to try on my samples. They should come to my office later.",
                EventTask("new_yoga_outfit_5", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "yoga_outfit_6",
                "Now I have an outfit, but I have no idea, what size to order. I should talk to Ms. Parker.",
                EventTask("new_yoga_outfit_6", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "yoga_outfit_7",
                "Ms. Parker agreed to ask her friend to help with the checkups. I should wait for her to come by.",
                EventTask("new_yoga_outfit_7", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "yoga_outfit_8",
                "The nurse agreed to do a general health checkup. I should now go to the classes and announce the checkup-day.",
                EventTask("new_yoga_outfit_8", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "yoga_outfit_9",
                "Okay, checkup-day starts on Tuesday during morning classes.",
                EventTask("new_yoga_outfit_9", check_history = True),
                activate_next = True,
                trigger_activate = True
            ),
            Goal(
                "yoga_outfit_10",
                "Now with the results and the outfits ordered, I can finally give them to the students.",
                EventTask("new_yoga_outfit_10", check_history = True),
            ),
            premature_visibility = True
        )
    )

    # endregion
    ########################

    ########################
    # region Helper Quests #

    # Max Stats
    $ load_quest(
        Quest(
            "max_stats",
            "MaxGame",
            "This is an overview of what values for certain stats you need to reach to have seen everything in the game. \nProgressing the stats further won't make a difference in the current version.\nThis quest is only for giving you an overview, of what stats you still have missed.",
            "images/journal/journal/test_image.webp",
            "You have reached the maximum stats!",
            Goal(
                "max_stats",
                "Stats",
                ConditionTask("stats", "max_stats", StatCondition(inhibition = "90-", corruption = "5+")),
                premature_visibility = True
            ),
            premature_visibility = True
        )
    )

    # All Events
    $ load_quest(
        Quest(
            "all_events",
            "MaxGame",
            "This is an overview of all events that exist in the game. This quest is only for giving you an overview, of what events you still have missed.\n\nIt however doesn't track the different variants and decision possibilities of the events, since many events can differ from their last run.\n\nThis quest also only tracks the events you can see during the free roam phase after the introduction finished.",
            "images/journal/journal/test_image.webp",
            "You have seen all events!",
            Goal(
                "all_events_cafeteria",
                "Cafeteria Events",
                EventTask("cafeteria_event_1", check_history = True),
                EventTask("cafeteria_event_2", check_history = True),
                EventTask("cafeteria_event_3", check_history = True),
                EventTask("cafeteria_event_4", check_history = True),
                EventTask("cafeteria_event_5", check_history = True),
                EventTask("cafeteria_event_6", check_history = True),
                EventTask("cafeteria_event_7", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_courtyard",
                "Courtyard Events",
                EventTask("courtyard_event_1", check_history = True),
                EventTask("courtyard_event_2", check_history = True),
                EventTask("courtyard_event_3", check_history = True),
                EventTask("courtyard_event_4", check_history = True),
                EventTask("courtyard_event_5", check_history = True),
                EventTask("courtyard_event_6", check_history = True),
                EventTask("courtyard_event_7", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_gym",
                "Gym Events",
                EventTask("gym_event_1", check_history = True),
                EventTask("gym_event_2", check_history = True),
                EventTask("gym_event_3", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_kiosk",
                "Kiosk Events",
                EventTask("kiosk_event_1", check_history = True),
                EventTask("kiosk_event_2", check_history = True),
                EventTask("kiosk_event_3", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_office",
                "Office Building Events",
                EventTask("office_event_1", check_history = True),
                EventTask("office_event_2", check_history = True),
                EventTask("office_event_3", check_history = True),
                EventTask("office_event_4", check_history = True),
                EventTask("work_office_session_event_first_naughty", check_history = True),
                EventTask("work_office_session_event_1", check_history = True),
                EventTask("work_office_reputation_event_1", check_history = True),
                EventTask("work_office_money_event_1", check_history = True),
                EventTask("work_office_education_event_1", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_school_building",
                "School Building Events",
                EventTask("first_class_sb_event", check_history = True),
                EventTask("sb_event_1", check_history = True),
                EventTask("sb_event_3", check_history = True),
                EventTask("sb_event_4", check_history = True),
                EventTask("sb_event_5", check_history = True),
                EventTask("sb_event_6", check_history = True),
                EventTask("sb_event_7", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_school_dormitory",
                "School Dormitory Events",
                EventTask("sd_event_1", check_history = True),
                EventTask("sd_event_2", check_history = True),
                EventTask("sd_event_3", check_history = True),
                EventTask("sd_event_4", check_history = True),
                EventTask("sd_event_5", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_truth_or_dare",
                "Truth or Dare Events",
                EventTask("truth_or_dare_1", check_history = True),
                EventTask("truth_or_dare_2", check_history = True),
                EventTask("truth_or_dare_3", check_history = True),
                LabelTask("all_events_truth_or_dare_truth", "-- Truth Fragments"),
                EventTask("truth_or_dare_truth_1", check_history = True),
                EventTask("truth_or_dare_truth_2", check_history = True),
                EventTask("truth_or_dare_truth_3", check_history = True),
                EventTask("truth_or_dare_truth_4", check_history = True),
                EventTask("truth_or_dare_truth_5", check_history = True),
                EventTask("truth_or_dare_truth_6", check_history = True),
                LabelTask("all_events_truth_or_dare_dare", "-- Dare Fragments"),
                EventTask("truth_or_dare_dare_1", check_history = True),
                EventTask("truth_or_dare_dare_2", check_history = True),
                EventTask("truth_or_dare_dare_3", check_history = True),
                EventTask("truth_or_dare_dare_4", check_history = True),
                EventTask("truth_or_dare_dare_5", check_history = True),
                EventTask("truth_or_dare_dare_6", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_new_yoga_outfit",
                "New Yoga Outfit Events",
                EventTask("new_yoga_outfit_1", check_history = True),
                EventTask("new_yoga_outfit_2", check_history = True),
                EventTask("new_yoga_outfit_3", check_history = True),
                EventTask("new_yoga_outfit_4", check_history = True),
                EventTask("new_yoga_outfit_5", check_history = True),
                EventTask("new_yoga_outfit_6", check_history = True),
                EventTask("new_yoga_outfit_7", check_history = True),
                EventTask("new_yoga_outfit_8", check_history = True),
                EventTask("new_yoga_outfit_9", check_history = True),
                EventTask("new_yoga_outfit_10", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_teaching_sex_ed",
                "Sex Education Teaching Events",
                LabelTask("all_events_teaching_sex_ed_intro", "-- Intro Fragments"),
                EventTask("sb_teach_sex_ed_intro_anatomy", check_history = True),
                EventTask("sb_teach_sex_ed_intro_sex_curiosity", check_history = True),
                LabelTask("all_events_teaching_sex_ed_main", "-- Main Fragments"),
                EventTask("sb_teach_sex_ed_main_anatomy_1", check_history = True),
                EventTask("sb_teach_sex_ed_main_sex_curiosity_1", check_history = True),
                LabelTask("all_events_teaching_sex_ed_qa", "-- Q&A Fragments"),
                EventTask("sb_teach_sex_ed_qa_1", check_history = True),
                EventTask("sb_teach_sex_ed_qa_2", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_teaching_pe",
                "P.E. Teaching Events",
                LabelTask("all_events_teaching_gym_intro", "-- Intro Fragments"),
                EventTask("gym_teach_pe_intro_2", check_history = True),
                EventTask("gym_teach_pe_intro_aona_bra", check_history = True),
                LabelTask("all_events_teaching_gym_entrance", "-- Entrance Fragments"),
                EventTask("gym_teach_pe_entrance_1", check_history = True),
                LabelTask("all_events_teaching_gym_warm_up", "-- Warm Up Fragments"),
                EventTask("gym_teach_pe_warm_up_1", check_history = True),
                LabelTask("all_events_teaching_gym_main", "-- Main Fragments"),
                EventTask("gym_teach_pe_main_1", check_history = True),
                EventTask("gym_teach_pe_main_aona_bra", check_history = True),
                LabelTask("all_events_teaching_gym_main", "-- End Fragments"),
                EventTask("gym_teach_pe_end_1", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_teaching_math",
                "Math Teaching Events",
                LabelTask("all_events_teaching_math_intro", "-- Intro Fragments"),
                EventTask("sb_teach_math_ld_1", check_history = True),
                EventTask("sb_teach_math_ld_2", check_history = True),
                EventTask("sb_teach_math_ld_3", check_history = True),
                LabelTask("all_events_teaching_math_main", "-- Main Fragments"),
                EventTask("sb_teach_math_main_1", check_history = True),
                EventTask("sb_teach_math_main_2", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_teaching_history",
                "History Teaching Events",
                LabelTask("all_events_teaching_history_intro", "-- Intro Fragments"),
                EventTask("sb_teach_history_intro_f_revolution_1", check_history = True),
                LabelTask("all_events_teaching_history_main", "-- Main Fragments"),
                EventTask("sb_teach_history_main_f_revolution_1", check_history = True),
                EventTask("sb_teach_history_main_f_revolution_2", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_event_aonas_new_bra",
                "Aona's New Bra Events",
                EventTask("gym_teach_pe_intro_aona_bra", check_history = True),
                EventTask("gym_teach_pe_main_aona_bra", check_history = True),
                EventTask("gym_teach_pe_main_aona_bra_2", check_history = True),
                EventTask("aona_sports_bra_event_1", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_event_sex_ed_intro",
                "Sex Education Introduction Events",
                EventTask("office_call_secretary_1", check_history = True),
                EventTask("office_teacher_sex_ed_introduction_1", check_history = True),
                EventTask("office_teacher_sex_ed_introduction_2", check_history = True),
                EventTask("office_teacher_sex_ed_introduction_3", check_history = True),
                EventTask("office_teacher_sex_ed_introduction_4", check_history = True),
                EventTask("pta_discussion_sex_ed_intro_1", check_history = True),
                EventTask("pta_vote_theoretical_sex_ed_1", check_history = True),
                EventTask("theoretical_sex_ed_assembly_1", check_history = True),
                EventTask("sex_ed_intro_mini_sd_1", check_history = True),
                EventTask("sex_ed_intro_mini_sd_2", check_history = True),
                EventTask("sex_ed_intro_mini_courtyard_1", check_history = True),
                EventTask("first_sex_ed_day", check_history = True),
                EventTask("first_sex_ed_class_1", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_naughty",
                "Naughty Sandbox Events",
                EventTask("office_call_secretary_naughty_sandbox", check_history = True),
                premature_visibility = True
            ),
            premature_visibility = True
        )
    )

    # Unlock Cafeteria
    $ load_quest(
        Quest(
            "unlock_cafeteria",
            "Help Quests",
            "This quest is a help that shows how to unlock the cafeteria.",
            "images/journal/buildings/cafeteria 1 0_full.webp",
            "The cafeteria is now unlocked!",
            Goal(
                "unlock_cafeteria_1",
                "Get yourself a snack at the kiosk.",
                TriggerTask("kiosk_observe_kindness", "Observe the Kindness of the Kiosk Clerk."),
                premature_visibility = True,
                activate_next = True
            ),
            Goal(
                "unlock_cafeteria_2",
                "Get the PTA to vote for the renovation and reopening of the cafeteria.",
                ScheduleVotingTask("cafeteria", "unlock"),
                JournalUnlockTask("cafeteria"),
                activate_next = True
            ),
            Goal("unlock_cafeteria_3", 
                "Wait for the Cafeteria to be finished.",
                TriggerTask("cafeteria_opening", "Visit the cafeteria after 7 days.")
            ),
            premature_visibility = True
        )
    )

    # Unlock School Jobs
    $ load_quest(
        Quest(
            "unlock_school_jobs",
            "Help Quests",
            "This quest is a help that shows how to unlock the school jobs rule.",
            "images/journal/rules/school_jobs_1_full.webp",
            "The school jobs rule is now unlocked!",
            Goal(
                "unlock_school_jobs_0",
                "Unlock the Cafeteria.",
                JournalUnlockTask("cafeteria"),
                premature_visibility = True,
                activate_next = True
            ),
            Goal(
                "unlock_school_jobs_1",
                "Order some Food in the Cafeteria and observe Adelaide getting a bit overwhelmed.",
                EventValueTask("cafeteria_event_3", min_seen = 3, topic = "overwhelmed"),
                activate_next = True
            ),
            Goal(
                "unlock_school_jobs_2",
                "Get the PTA to vote for the introduction of jobs for the students.",
                ScheduleVotingTask("school_jobs", "unlock"),
                JournalUnlockTask("school_jobs"),
                activate_next = True
            ),
            premature_visibility = True
        )
    )

    # Unlock Student Relations
    $ load_quest(
        Quest(
            "unlock_student_relations",
            "Help Quests",
            "This quest is a help that shows how to unlock the rule allowing students to have a relationship between each other.",
            "images/journal/rules/student_student_relation 1 0_full.webp",
            "The rule for student relationships is now unlocked!",
            Goal(
                "unlock_student_relations_1",
                "Look around the Office for a bit.",
                EventTask("office_event_3"),
                premature_visibility = True,
                activate_next = True
            ),
            Goal(
                "unlock_student_relations_2",
                "Find two students sitting there because of the relationship.",
                TriggerTask("trigger_unlock_student_relations_1", "Promise the students to take care of the situation."),
                activate_next = True
            ),
            Goal(
                "unlock_student_relations_3",
                "Get the PTA to vote for removal of the students relationships prohibition.",
                ScheduleVotingTask("student_student_relation", "unlock"),
                JournalUnlockTask("student_student_relation"),
                activate_next = True
            ),
            premature_visibility = True
        )
    )

    # endregion
    ########################

    #####################################
    # region Quests Intro Sex Education #

    $ load_quest(
        Quest(
            "start_sex_ed",
            "School",
            "It is time to start teaching the school girls about their bodies, sexuality and reproduction.\nLet's try to add theoretical sex education to the schools curriculum.",
            "images/events/sex_ed_intro/mini_sd_2/mini_sd_2 5.webp",
            "Theoretical Sex Education is now part of the schools curriculum. How do we proceed now?",
            Goal(
                "start_sex_ed_1",
                "Talk with Aona on your way back from shopping and find out about some problem at the school.",
                EventTask("aona_sports_bra_event_1", check_history = True),
                premature_visibility = True,
                trigger_activate = True,
                activate_next = True
            ),
            Goal(
                "start_sex_ed_2",
                "The knowledge about that topic is definitely lacking. Let's ask Emiko for opinion.",
                EventTask("office_call_secretary_1", check_history = True),
                trigger_activate = True,
                activate_next = True
            ),
            Goal(
                "start_sex_ed_3",
                "Emiko suggested talking to the teachers about the topic. But how would I approach them about it. I should think about it a bit.",
                EventTask("office_teacher_sex_ed_introduction_1", check_history = True),
                activate_next = True
            ),
            Goal(
                "start_sex_ed_4",
                "I called for a meeting with the teachers first thing in the morning. I hope they are open to the idea.",
                ConditionTask("daytime_change", "is_morning", TimeCondition(daytime = 1)),
                EventTask("office_teacher_sex_ed_introduction_2", check_history = True),
                activate_next = True
            ),
            Goal(
                "start_sex_ed_5",
                "The teachers were relatively negative about the topic. But I convinced them to reevaluate their opinions after I present them with convincing data.\nLet's start working on it.",
                EventTask("office_teacher_sex_ed_introduction_3", check_history = True),
                activate_next = True
            ),
            Goal(
                "start_sex_ed_6",
                "I'm prepared to present the teachers with the data. Let's see how they react.",
                EventTask("office_teacher_sex_ed_introduction_4", check_history = True),
                activate_next = True
            ),
            Goal(
                "start_sex_ed_7",
                "I managed to convince the teachers to give it a try. But they set the condition to first discuss it with the PTA.",
                OptionalTask("daytime_change", ConditionTask("daytime_change", "friday_pta", TimeCondition(weekday = 5, daytime = 1))),
                EventTask("pta_discussion_sex_ed_intro_1", check_history = True),
                activate_next = True
            ),
            Goal(
                "start_sex_ed_8",
                "The PTA asked for a bit of time to think about it. I could work on pushing their opinions a bit more until that.",
                OptionalTask("stat", ConditionTask("stat", "sex_ed_stats", StatCondition(char_obj = "school", corruption = "10+", inhibition = "90-"))),
                JournalUnlockTask("theoretical_sex_ed"),
                activate_next = True
            ),
            Goal(
                "start_sex_ed_9",
                "The PTA agreed to give it a try. Gonna make an announcement to the school.",
                EventTask("theoretical_sex_ed_assembly_1", check_history = True),
            ),
            Goal(
                "start_sex_ed_10",
                "The announcement is done. Let's see how the students react to it.",
                OptionalTask("event", EventTask("sex_ed_intro_mini_sd_1")),
                OptionalTask("event", EventTask("sex_ed_intro_mini_sd_2")),
                OptionalTask("event", EventTask("sex_ed_intro_mini_courtyard_1")),
                EventTask("first_sex_ed_day", check_history = True),
            ),
            Goal(
                "Well the change seems well received. Now on to the first lesson.",
                EventTask("first_sex_ed_class_1", check_history = True),
            ),
            premature_visibility = True
        )
    )
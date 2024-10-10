init 1 python:

    def load_quest(quest: Quest):
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
        if category in quests and key in quests[category]:
            quests[category][key].activate()
            add_notify_message(f"New Quest added for {get_translation(category)}!")

    def activate_goal(category: str, key: str, goal_key: str):
        if category in quests and key in quests[category]:
            quests[category][key].activate_goal(goal_key)

    def get_quest(category: str, key: str):
        if category in quests and key in quests[category]:
            return quests[category][key]
        return None

    def get_quests(category: str):
        if category in quests:
            return quests[category]
        return None

    def get_goal(category: str, key: str, goal_key: str):
        if category in quests and key in quests[category]:
            return quests[category][key].get_goal(goal_key)
        return None

    def update_quest(key: str, **kwargs):
        """
        Updates the progress of a quest for all tasks registered under the key.

        ### Parameters:
        1. key: str
            - The key of the quest.
        2. **kwargs: dict
            - The parameters to be passed to the update method of the task.
        """

        for category in quests.keys():
            quests_list = [quests[category][quest] for quest in quests[category].keys() if (quests[category][quest].is_active() or (quests[category][quest].show_prematurely() and get_setting("journal_goals_show_note_setting")) or quests[category][quest].get_start_trigger()) and not quests[category][quest].all_active_done()]
            for quest in quests_list:
                quest.update(key, **kwargs)

label load_quests:
    $ load_quest(
        Quest(
            "all_events",
            "ObserveAllEvents",
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
                premature_visibility = True
            ),
            Goal(
                "all_events_school_dormitory",
                "School Dormitory Events",
                EventTask("sd_event_1", check_history = True),
                EventTask("sd_event_2", check_history = True),
                EventTask("sd_event_3", check_history = True),
                premature_visibility = True
            ),
            Goal(
                "all_events_teaching_pe",
                "P.E. Teaching Events",
                LabelTask("all_events_teaching_gym_intro", "-- Intro Fragments"),
                EventTask("gym_teach_pe_intro_1", check_history = True),
                EventTask("gym_teach_pe_intro_aona_bra", check_history = True),
                LabelTask("all_events_teaching_gym_warm_up", "-- Warm Up Fragments"),
                EventTask("gym_teach_pe_warm_up_1", check_history = True),
                LabelTask("all_events_teaching_gym_main", "-- Main Fragments"),
                EventTask("gym_teach_pe_main_1", check_history = True),
                EventTask("gym_teach_pe_main_2", check_history = True),
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
                "all_events_misc",
                "Miscellaneous Events",
                EventTask("aona_sports_bra_event_1", check_history = True),
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

    $ load_quest(
        Quest(
            "aonas_new_bra",
            "School",
            "Aona seems to be struggling during P.E. classes. Maybe you can help her out? Find out what's the Problem!",
            "images/events/misc/aona_sports_bra_event_1 # 23.webp",
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
                activate_next = True
            ),
            Goal(
                "aona_bra_event_3",
                "Check if Aona is happy with her new bra.",
                EventTask("gym_teach_pe_main_aona_bra_2", check_history = True)
            ),
            premature_visibility = True
        )
    )

    ########################
    # region Helper Quests #

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

    $ load_quest(
        Quest(
            "unlock_school_jobs",
            "Help Quests",
            "This quest is a help that shows how to unlock the school jobs rule.",
            "images/journal/rules/school_jobs_1_full.webp",
            "The school jobs rule is now unlocked!",
            Goal(
                "unlock_school_jobs_1",
                "Order some Food in the Cafeteria and observe Adelaide getting a bit overwhelmed.",
                EventValueTask("cafeteria_event_3", min_seen = 3, topic = "overwhelmed"),
                premature_visibility = True,
                activate_next = True
            ),
            Goal(
                "unlock_school_jobs_2",
                "Get the PTA to vote for the introduction of jobs for the students.",
                ScheduleVotingTask("school_jobs", "unlock"),
                JournalUnlockTask("school_jobs"),
                activate_next = True
            ),
        )
    )

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
        )
    )

    # endregion
    ########################

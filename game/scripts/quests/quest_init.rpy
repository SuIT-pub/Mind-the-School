label load_new_quests:
    $ set_current_mod('base')

    $ global quest_manager

    $ quest_manager.add_quest(QuestObj(
        "aonas_new_bra", 
        "School", 
        "Aona seems to be struggling during P.E. classes. Maybe you can help her out? Find out what's the Problem!",
        "Aona got her new bra and is now ready for P.E. classes!",
        "images/events/misc/aona_sports_bra_event_1/aona_sports_bra_event_1 # 23.webp",
        GoalObj(
            "aona_bra_event_1",
            "Teach some P.E. until you find out, what's the Problem.",
            EventTaskObj("gym_teach_pe_main_aona_bra", "aona_bra_event_1_1",
                QuestWorkerShow("complete", 
                    "quest_aonas_new_bra", 
                    "goal_aona_bra_event_1", "goal_aona_bra_event_2",
                    "task_aona_bra_event_1_1", "task_aona_bra_event_2_1"),
                QuestWorkerActivate("insert", "task_aona_bra_event_1_1"),
                QuestWorkerActivate("complete", "task_aona_bra_event_2_1"),
            ),
        ),
        GoalObj(
            "aona_bra_event_2",
            "Drive Aona to the Shop.",
            EventTaskObj("aona_sports_bra_event_1", "aona_bra_event_2_1",
                QuestWorkerShow("complete", "goal_aona_bra_event_3", "task_aona_bra_event_3_1"),
                QuestWorkerActivate("complete", "task_aona_bra_event_3_1")
            ),
        ),
        GoalObj(
            "aona_bra_event_3",
            "Check if Aona is happy with her new bra.",
            EventTaskObj("gym_teach_pe_main_aona_bra_2", "aona_bra_event_3_1")
        ),
        helper = True))
        

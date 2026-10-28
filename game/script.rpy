# The game starts here.

label start ():

    $ set_dissolve()

    $ open_mod_content_recording()
    $ lifecycle_registry.begin_check()

    call load_stats from start_1
    call load_schools from start_2
    call load_characters from start_7
    call load_items from start_8
    call load_pictograms from start_11
    call load_situations from start_9
    call load_unlockables from start_10
    call load_buildings from start_3
    call load_maps from start_12
    call load_collectibles from start_13

    $ fix_modifier()

    $ check_event_selectors()
    $ check_registered_events()

    $ i = 0
    while i < len(start_methods):
        call expression start_methods[i] from _call_expression_2
        $ i += 1
    $ close_mod_content_recording()

    # after the mod loaders, so mod-defined items still have their definitions
    $ inventory_manager.check_missing_items()

    if situation_manager is not None:
        $ situation_manager.reconcile_orphan_situations()
    $ lifecycle_registry.finalize_check()

    $ update_intro_flag()

    # label intro is no event, so begin_event hasn't bound the Person speakers yet
    $ bind_event_speakers()

    call intro from _call_intro
label splashscreen:
    menu:
        "This game is not suitable for children or those who are easily disturbed.\n\nBy playing this game you agree that you are 18 years of age or older and are not offended by adult content."

        "I am 18 years of age or older.":
            pass
        "I am not 18 years of age or older.":
            $ renpy.quit()

    subtitles "The game downloads the current list of {a=[patreon]}Patreon{/a} supporters every time the game starts. The file's size is max 1KB. If you don't want the game to download this file, you can disable it in the options menu."
    subtitles "For everyone with an old save-game from the previous version:\nYou can still open the game with the old save-game. If you encounter an error after loading because of a missing image, just press 'Ignore' and the game will continue normally."

    # without it, execution runs past the init block below into label after_load
    return

init python:
    
    ###########################################
    # --- Version Compatibility Functions --- #
    ###########################################

    def fix_modifier():
        """
        Fix the modifiers for the new version
        """

        # add weekly cost for cafeteria if not already added
        if (is_unlockable_unlocked('cafeteria') and
            get_modifier('weekly_cost_cafeteria', 'money', 'payroll_weekly') == None
        ):
            set_modifier('weekly_cost_cafeteria', Modifier_Obj('Cafeteria', "+", -100), stat = 'money', collection = 'payroll_weekly')

        if get_modifier('monthly_budget', 'money', 'payroll_monthly') == None:
            set_modifier('monthly_budget', Modifier_Obj('Budget', "+", 1000), stat = 'money', collection = 'payroll_monthly')

        if get_modifier('teacher_pay', 'money', 'payroll_weekly') == None:
            set_modifier('teacher_pay', Modifier_Obj('Teacher', "+", -150), stat = 'money', collection = 'payroll_weekly')
    
    def check_event_selectors():
        for event in event_register.values():
            event.check_selectors()

    ###########################################

label after_load:
    $ log_separator()
    $ log_separator()

    $ open_mod_content_recording()
    $ lifecycle_registry.begin_check()
    # before anything checks EventSeenConditions (teasers, situation syncs)
    $ restore_seen_events()

    call load_stats from after_load_1
    call load_schools from after_load_2
    call load_characters from after_load_7
    call load_items from after_load_8
    call load_pictograms from after_load_11
    call load_situations from after_load_9
    call load_unlockables from after_load_10
    call load_buildings from after_load_4
    call load_maps from after_load_12
    call load_collectibles from after_load_13

    $ clean_legacy_journal_objects()
    $ clean_legacy_quests()
    # an old PTAProposal would hold the vote slot and block every Schedule Vote
    $ clean_legacy_vote_proposal()

    $ check_event_selectors()
    $ check_registered_events()

    # also creates the budget and payroll modifiers, so it runs for every save
    $ fix_modifier()

    $ i = 0
    while i < len(start_methods):
        call expression start_methods[i] from _call_expression_3
        $ i += 1
    $ close_mod_content_recording()

    # after the mod loaders, so mod-defined items still have their definitions
    $ inventory_manager.check_missing_items()

    if situation_manager is not None:
        $ situation_manager.reconcile_orphan_situations()
    $ lifecycle_registry.finalize_check()
    
    if contains_game_data("names") and "headmaster" in get_game_data("names"):
        $ headmaster_first_name = get_game_data("names")["headmaster"][0]
        $ headmaster_last_name = get_game_data("names")["headmaster"][1]

    $ update_intro_flag()
    # a save made outside an event may still hold the static Character speakers
    $ bind_event_speakers()
    # situation flags may have changed in code since the save
    if situation_manager is not None:
        $ situation_manager.sync_flag_pauses()

    return

label open_patreon_link_from_menu():
    # """
    # Opens the patreon page in the default browser
    # """

    $ renpy.run(OpenURL(patreon))
    call screen main_menu


label open_discord_link_from_menu():
    # """
    # Opens the patreon page in the default browser
    # """

    $ renpy.run(OpenURL(discord))
    call screen main_menu


label open_wiki_link_from_menu():
    # """
    # Opens the patreon page in the default browser
    # """

    $ renpy.run(OpenURL(wiki))
    call screen main_menu
# The game starts here.

label start ():

    $ set_dissolve()

    call load_stats from start_1
    call load_schools from start_2
    call load_buildings from start_3
    call load_clubs from start_4
    call load_rules from start_5

    jump ask_age

    return

label after_load:
    call load_stats from after_load_1
    call load_schools from after_load_2
    call load_rules from after_load_3
    call load_buildings from after_load_4
    call load_clubs from after_load_5
    
    $ check_old_versions()

    if contains_game_data("names") and "headmaster" in get_game_data("names"):
        $ headmaster_first_name = get_game_data("names")["headmaster"][0]
        $ headmaster_last_name = get_game_data("names")["headmaster"][1]

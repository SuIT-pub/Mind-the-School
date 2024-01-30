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

init python:
    def check_stats_compatibility():
        school = get_character_by_key("school")
        parents = get_character_by_key("parents")
        teacher = get_character_by_key("teacher")
        secretary = get_character_by_key("secretary")

        map(lambda: x._repair(), school.get_stats().values())
        map(lambda: x._repair(), parents.get_stats().values())
        map(lambda: x._repair(), teacher.get_stats().values())
        map(lambda: x._repair(), secretary.get_stats().values())

label after_load:
    call load_stats from after_load_1
    call load_schools from after_load_2
    call load_rules from after_load_3
    call load_buildings from after_load_4
    call load_clubs from after_load_5
    
    $ check_old_versions()

    $ check_stats_compatibility()

    if contains_game_data("names") and "headmaster" in get_game_data("names"):
        $ headmaster_first_name = get_game_data("names")["headmaster"][0]
        $ headmaster_last_name = get_game_data("names")["headmaster"][1]

    $ after_load_event_check('daily', None, time_check_events, temp_time_check_events)
    $ after_load_event_check('bath', bath_events, bath_general_event, bath_timed_event)
    $ after_load_event_check('cafeteria', cafeteria_events, cafeteria_general_event, cafeteria_timed_event)
    $ after_load_event_check('courtyard', courtyard_events, courtyard_general_event, courtyard_timed_event)
    $ after_load_event_check('gym', gym_events, gym_general_event, gym_timed_event)
    $ after_load_event_check('kiosk', kiosk_events, kiosk_general_event, kiosk_timed_event)
    $ after_load_event_check('labs', labs_events, labs_general_event, labs_timed_event)
    $ after_load_event_check('office_building', office_building_events, office_building_general_event, office_building_timed_event)
    $ after_load_event_check('school_building', sb_events, sb_general_event, sb_timed_event)
    $ after_load_event_check('school_dormitory', sd_events, sd_general_event, sd_timed_event)
    $ after_load_event_check('sports_field', sports_field_events, sports_field_general_event, sports_field_timed_event)
    $ after_load_event_check('swimming_pool', swimming_pool_events, swimming_pool_general_event, swimming_pool_timed_event)
    $ after_load_event_check('tennis_court', tennis_court_events, tennis_court_general_event, tennis_court_timed_event)

# The game starts here.

label start:

    call load_stats from _call_load_stats
    call load_schools from _call_load_schools
    call load_buildings from _call_load_buildings
    call load_clubs from _call_load_clubs
    call load_rules from _call_load_rules

    jump ask_age

    return

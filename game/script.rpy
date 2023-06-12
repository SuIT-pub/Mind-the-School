# The game starts here.

label start:

    call load_stats
    call load_schools
    call load_buildings
    call load_clubs
    call load_rules

    jump ask_age

    return

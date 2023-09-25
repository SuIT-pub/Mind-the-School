# The game starts here.

label start:

    $ set_dissolve()

    call load_stats from start_1
    call load_schools from start_2
    call load_buildings from start_3
    call load_clubs from start_4
    call load_rules from start_5

    jump ask_age

    return

init -97 python:
    register_mod(
        "cheat_suit",
        "CheatMod", 
        "1", 
        "CheatMod",
        description = "Activates the Cheat Menu in the Journal.",
        author = "SuIT-Ji",
    )

init 1 python:
    set_current_mod('cheat_suit')  

    register_start_method("activate_cheat_mode")

label activate_cheat_mode():
    python:
        global cheat_mode
        cheat_mode = True
    return
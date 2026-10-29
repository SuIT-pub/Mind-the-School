init -9:
    
    $ CORRUPTION = "corruption"
    $ INHIBITION = "inhibition"
    $ HAPPINESS = "happiness"
    $ EDUCATION = "education"
    $ CHARM = "charm"
    $ REPUTATION = "reputation"
    $ LEVEL = "level"
    $ MONEY = "money"

    $ TINY = "tiny"
    $ SMALL = "small"
    $ MEDIUM = "medium"
    $ LARGE = "large"
    $ GIANT = "giant"

    $ DEC_TINY = "dec_tiny"
    $ DEC_SMALL = "dec_small"
    $ DEC_MEDIUM = "dec_medium"
    $ DEC_LARGE = "dec_large"
    $ DEC_GIANT = "dec_giant"

    $ UNLOCK = "unlock"
    $ UPGRADE = "upgrade"

    $ SHOW = "show"
    $ SCENE = "scene"

    $ YES = "yes"
    $ NO = "no"

    $ CHAR = "char_obj"

    # Event priority, the first argument of Event / EventComposite / EventFragment / EventSelect
    $ EVENT_BLOCKING = 1    # the first available one runs and blocks all others (story beats)
    $ EVENT_ALWAYS = 2      # every available one runs, one after another
    $ EVENT_RANDOM = 3      # one of the available ones is picked at random (ambient)

    # Where end_event goes after the scene
    $ END_NEW_DAYTIME = "new_daytime"   # advance to the next daytime
    $ END_NEW_DAY = "new_day"           # skip to the next morning
    $ END_MAP = "map_entry"             # back to the map, same daytime
    $ END_NONE = "none"                 # return to the caller (situation scenes, chains)
    $ END_CUSTOM = "custom"             # call the label in kwargs["return_label"]

    $ DEFAULT_NUDE = 0

    $ ICON_XSMALL = "20"
    $ ICON_SMALL = "50"
    $ ICON_LARGE = "511"
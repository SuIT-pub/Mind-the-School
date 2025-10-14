default time_freeze = False
default debug_mode = False

init -100 python:
    import pprint

    def log_separator():
        print("##################################################")

    def log_json(key: str, value: Dict[string, Any]):
        print(key + ":", end="")
        pprint.pprint(value, compact = False)

    def log_val(key: str, *values: Any):
        """
        Prints a key and value

        ### Parameters:
        1. key: str
            - The key to print
        2. value: Any
            - The value to print
        """

        value = ", ".join(map(str, values))

        print(key + ": " + str(value))
        return

    def log(msg: str):
        """
        Prints a message

        ### Parameters:
        1. msg: str
            - The message to print
        """

        print(str(msg))
        return

    def log_error(code: int, msg: str):
        """
        Prints an error message

        ### Parameters:
        1. msg: str
            - The message to print
        """

        print(f"|ERROR[{str(code)}]| {str(msg)}")
        add_notify_message("|ERROR| " + str(msg))
        return

    log_number = 0

    def log_count(msg: str, start = False):
        if start:
            log_number = 0
        
        log_number += 1
        log_val(msg, log_number)

init -1 python:
    test_events = EventStorage("test_events", "misc")

init 1 python:
    test_events.add_event(
        Event(3, "test_event",
            Pattern("main", "images/background/school building/9 0 1.webp"),
            thumbnail = "images/background/school building/9 0 1.webp"),
    )

label test_label():

    $ hide_all()

    $ test_events.call_available_event()

    jump map_entry

   
label test_event (**kwargs):
    $ begin_event(**kwargs)

    $ luna_char = get_person("class_3a", "luna_clark")
    $ luna_char.register_dialogue(**kwargs)
    
    # $ show_pattern("main", **kwargs)
    $ luna_char.display(
        Action("image", mood = "happy", outfit = "uniform", pose = 1, level = 5),
        Action("pos", alignX = 0.3)
    )
    dev "Test 1"

    $ luna_char.display(
        Action("pos", alignX = 0.8)
    )
    dev "Test 2"

    $ luna_char.display(
        Action("image", mood = "sad", level = 8)
    )
    dev "Test 3"

    $ luna_char.display(
        Action("image", mouth = "open", level = 9),
        Action("pos", alignX = 0.3, duration = 0.01)
    )
    dev "Test 4"

    $ luna_char.display(
        Action("image", mood = "pout", level = 7),
        Action("pos_rotate", alignX = 0.8, degree = 180)
    )
    dev "Test 5"

    $ luna_char.display(
        Action("rotate", degree = 720)
    )
    dev "Test 6"

    $ luna_char.display(
        Action("image", outfit = "nude"),
        Action("pause", duration = 0.2),
        Action("image", outfit = "uniform", level = 9),
    )
    dev "Test 7"

    $ luna_char.display(
        Action("shake", max_distance = 30)
    )
    dev "Test 8"

    $ luna_char.display(
        Action("pos", alignX = -0.5)
    )
    dev "Test 9"

    $ renpy.pause()

    $ end_event('new_daytime', **kwargs)
    

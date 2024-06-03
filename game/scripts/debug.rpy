default time_freeze = False
default debug_mode = False

init -100 python:
    def log_val(key: str, value: Any):
        """
        Prints a key and value

        ### Parameters:
        1. key: str
            - The key to print
        2. value: Any
            - The value to print
        """

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

label test_label():
    
    $ test_event.call()

    return

label test_event_frag_1(**kwargs):
    $ begin_event(**kwargs)
    $ test1 = get_value('1_test', **kwargs)
    $ test2 = get_value('1_test2', **kwargs)
    $ old_test1 = get_value('test', no_register = True, **kwargs)
    $ old_test2 = get_value('test2', no_register = True, **kwargs)
    subtitles "Test Event Fragment 1 [test1] [test2] [old_test1] [old_test2]"
    if is_replay(**kwargs):
        $ log_val('kwargs', kwargs)
    $ call_custom_menu_with_text("Test Menu", character.subtitles, False,
        ("Decision1", "test_event_frag_1.decision1"),
        ("Decision2", "test_event_frag_1.decision2"),
        ("Decision3", "test_event_frag_1.decision3"),
    **kwargs)
label .decision1(**kwargs):
    $ end_event("map_overview", **kwargs)
label .decision2(**kwargs):
    $ end_event("map_overview", **kwargs)
label .decision3(**kwargs):
    $ end_event("map_overview", **kwargs)

label test_event_frag_1_1(**kwargs):
    $ begin_event(**kwargs)
    $ test1 = get_value('1_1_test', **kwargs)
    $ test2 = get_value('1_1_test2', **kwargs)
    subtitles "Test Event Fragment 1.1 [test1] [test2]"
    $ end_event("map_overview", **kwargs)

label test_event_frag_2(**kwargs):
    $ begin_event(**kwargs)
    $ test1 = get_value('2_test', **kwargs)
    $ test2 = get_value('2_test2', **kwargs)
    subtitles "Test Event Fragment 2 [test1] [test2]"
    if is_replay(**kwargs):
        $ log_val('kwargs', kwargs)
    $ call_custom_menu_with_text("Test Menu", character.subtitles, False,
        ("Decision1", "test_event_frag_2.decision1"),
        ("Decision2", "test_event_frag_2.decision2"),
        ("Decision3", "test_event_frag_2.decision3"),
    **kwargs)
label .decision1(**kwargs):
    $ end_event("map_overview", **kwargs)
label .decision2(**kwargs):
    $ end_event("map_overview", **kwargs)
label .decision3(**kwargs):
    $ end_event("map_overview", **kwargs)

label test_event_frag_2_1(**kwargs):
    $ begin_event(**kwargs)
    $ test1 = get_value('2_1_test', **kwargs)
    $ test2 = get_value('2_1_test2', **kwargs)
    subtitles "Test Event Fragment 2.1 [test1] [test2]"
    $ end_event("map_overview", **kwargs)

label test_event_frag_3(**kwargs):
    $ begin_event(**kwargs)
    $ test1 = get_value('3_test', **kwargs)
    $ test2 = get_value('3_test2', **kwargs)
    subtitles "Test Event Fragment 3 [test1] [test2]"
    $ end_event("map_overview", **kwargs)

label test_event_frag_3_1(**kwargs):
    $ begin_event(**kwargs)
    $ test1 = get_value('3_1_test', **kwargs)
    $ test2 = get_value('3_1_test2', **kwargs)
    subtitles "Test Event Fragment 3.1 [test1] [test2]"
    $ end_event("map_overview", **kwargs)

label test_event_frag_4(**kwargs):
    $ begin_event(**kwargs)
    $ test1 = get_value('4_test', **kwargs)
    $ test2 = get_value('4_test2', **kwargs)
    $ log_val("kwargs", kwargs)
    subtitles "Test Event Fragment 4 [test1] [test2]"
    $ end_event("map_overview", **kwargs)
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


label test_label():
    
    $ test_event.call()

    return

label test_event_frag_1(**kwargs):
    $ begin_event(**kwargs)
    $ get_value('test', **kwargs)
    $ get_value('test2', **kwargs)
    $ log("Test Event Fragment 1")
    $ end_event("map_overview", **kwargs)

label test_event_frag_1_1(**kwargs):
    $ begin_event(**kwargs)
    $ get_value('test', **kwargs)
    $ get_value('test2', **kwargs)
    $ log("Test Event Fragment 1.1")
    $ end_event("map_overview", **kwargs)

label test_event_frag_2(**kwargs):
    $ begin_event(**kwargs)
    $ get_value('test', **kwargs)
    $ get_value('test2', **kwargs)
    $ log("Test Event Fragment 2")
    $ end_event("map_overview", **kwargs)

label test_event_frag_2_1(**kwargs):
    $ begin_event(**kwargs)
    $ get_value('test', **kwargs)
    $ get_value('test2', **kwargs)
    $ log("Test Event Fragment 2.1")
    $ end_event("map_overview", **kwargs)

label test_event_frag_3(**kwargs):
    $ begin_event(**kwargs)
    $ get_value('test', **kwargs)
    $ get_value('test2', **kwargs)
    $ log("Test Event Fragment 3")
    $ end_event("map_overview", **kwargs)

label test_event_frag_3_1(**kwargs):
    $ begin_event(**kwargs)
    $ get_value('test', **kwargs)
    $ get_value('test2', **kwargs)
    $ log("Test Event Fragment 3.1")
    $ end_event("map_overview", **kwargs)
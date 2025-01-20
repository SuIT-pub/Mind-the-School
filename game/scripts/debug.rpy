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

label test_label():
    return

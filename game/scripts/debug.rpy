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

        print(key + ": " + str(value) + "\n")

    def log(msg: str):
        """
        Prints a message

        ### Parameters:
        1. msg: str
            - The message to print
        """

        print(str(msg) + "\n")

        return

    def log_error(code: int, msg: str):
        """
        Prints an error message

        ### Parameters:
        1. msg: str
            - The message to print
        """

        print(f"|ERROR[{str(code)}]| {str(msg)}\n")
        # renpy.notify("|ERROR| " + str(msg))
        return


label test_label():
    call multi_notify_example
    return
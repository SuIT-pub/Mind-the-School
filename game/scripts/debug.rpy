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

    $ hide_all()

    call show_image("images/events/new_yoga_outfits/new_yoga_outfit_5/new_yoga_outfit_5 # 45.webp")

    $ call_custom_menu(False, 
        MenuElement("Outfit 1", "Outfit 1", ChangeKwargsEffect("Outfit", 1), EventEffect("test_label.test"), overwrite_position = ( 330, 950)),
        MenuElement("Outfit 2", "Outfit 2", ChangeKwargsEffect("Outfit", 2), EventEffect("test_label.test"), overwrite_position = ( 800, 950)),
        MenuElement("Outfit 3", "Outfit 3", ChangeKwargsEffect("Outfit", 3), EventEffect("test_label.test"), overwrite_position = (1250, 950)),
    )
label .test(**kwargs):
    $ add_notify_message("Test successful! " + str(kwargs["Outfit"]))

    jump map_overview

###################################
# region Wiki Screenshots ----- #
###################################

# Developer tool: renders a fixed list of UI states and saves them as PNGs
# into wiki/screenshots/. Start from a loaded save via the console
# (Shift+O):  jump wiki_screenshots
# The inventory and shopping cart are restored afterwards.

init python:
    import copy
    import os

    WIKI_SCREENSHOT_DIR = os.path.join(config.basedir, "wiki", "screenshots")

    def wiki_screenshot(name: str):
        """
        Saves the currently displayed frame to wiki/screenshots/<name>.png.

        ### Parameters:
        1. name: str
            - File name without extension.
        """

        if not os.path.isdir(WIKI_SCREENSHOT_DIR):
            os.makedirs(WIKI_SCREENSHOT_DIR)
        path = os.path.join(WIKI_SCREENSHOT_DIR, name + ".png")
        # fixed size, independent of the current window size
        with open(path, "wb") as f:
            f.write(renpy.screenshot_to_bytes((config.screen_width, config.screen_height)))
        log("Wiki screenshot saved: " + path)

# Wraps the target screen so the shot is taken by a timer inside the
# interaction. A plain renpy.pause() never times out under a modal screen
# (journal_inventory is modal), so the label would hang.
screen wiki_shot_frame(shot_name, screen_name, *args):
    use expression screen_name pass (*args)

    timer 1.0 action Function(wiki_screenshot, shot_name)
    timer 1.3 action Return()

label wiki_screenshots():
    python:
        _wiki_shot_inventory = copy.deepcopy(inventory_manager.inventory)
        _wiki_shot_cart = dict(shopping_cart)
        _wiki_shot_notify = list(notify_messages)
        _wiki_shot_quick_menu = quick_menu
        quick_menu = False

    $ hide_all()

    # 1. school map with stats and building buttons
    $ update_available_highlights()
    $ update_available_events()
    scene expression map_manager.get_current_map().get_map_path() as map_image
    show screen school_overview_stats
    call screen wiki_shot_frame("map_overview", "school_overview_buttons", True)
    $ hide_all()

    # 2. journal inventory page with a few items
    python:
        for _key in ("lab_mortar_and_pestle", "lab_glassware", "lab_gas_burner", "lab_chemicals", "lab_test_potion"):
            if _key not in inventory_manager.inventory:
                inventory_manager.inventory[_key] = Item(_key, 1)
        inventory_manager.inventory["lab_test_potion"].amount = 3
    $ char = "school"
    call screen wiki_shot_frame("journal_inventory", "journal_inventory", "lab_test_potion", 10)
    $ hide_all()

    # 3. computer shop and shopping cart
    python:
        inventory_manager.inventory = copy.deepcopy(_wiki_shot_inventory)
        shopping_cart.clear()
        shopping_cart["lab_chemicals"] = 1
    scene black
    call screen wiki_shot_frame("computer_shop", "office_building_computer_shopping_screen", 0)
    $ hide_all()

    call screen wiki_shot_frame("computer_shop_cart", "office_building_computer_shopping_cart_screen", 0)
    $ hide_all()

    python:
        inventory_manager.inventory = _wiki_shot_inventory
        shopping_cart.clear()
        shopping_cart.update(_wiki_shot_cart)
        notify_messages[:] = _wiki_shot_notify
        quick_menu = _wiki_shot_quick_menu

    subtitles "Wiki screenshots saved to wiki/screenshots/."
    jump map_entry

# endregion
###################################

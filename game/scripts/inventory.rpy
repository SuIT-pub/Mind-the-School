init -98 python:
    from abc import ABC

    class Item:
        def __init__(self, key: str, amount: int = 1):
            self.key = key
            self.amount = amount

        def data(self) -> ItemData:
            global inventory_manager
            return inventory_manager.get_item_data(self.key)

        def get_name(self) -> str:
            global inventory_manager
            return inventory_manager.get_item_data(self.key).get_name()

        def get_description(self) -> List[str]:
            global inventory_manager
            return inventory_manager.get_item_data(self.key).get_description()

        def get_image(self) -> str:
            global inventory_manager
            return inventory_manager.get_item_data(self.key).get_image()

    class ItemData(ABC):
        def __init__(self, key: str, name: str, description: Union[str, List[str]], image: str):
            self.key = key
            self.name = name
            self.description = description if isinstance(description, list) else [description]
            self.image = get_mod_path(active_mod_key) + image

        def _update(self, item: ItemData):
            self.name = item.name
            self.description = item.description if isinstance(item.description, list) else [item.description]
            self.image = item.image

        def get_name(self) -> str:
            return self.name

        def get_description(self) -> List[str]:
            return self.description

        def get_image(self) -> str:
            if renpy.loadable(self.image):
                return self.image
            return "images/journal/empty_image.webp"

    class ShopItemData(ItemData):
        def __init__(self, key: str, name: str, description: Union[str, List[str]], image: str, price: int, max_possession: int = 1, max_purchase: int = 1):
            super().__init__(key, name, description, image)
            self.price = price
            self.max_possession = max_possession
            self.max_purchase = max_purchase
            self.bought = 0

        def get_price(self) -> int:
            return self.price

        def get_max_possession(self) -> int:
            return self.max_possession

        def get_max_purchase(self) -> int:
            return self.max_purchase

        def get_bought(self) -> int:
            return self.bought

        def _update(self, item: ShopItemData):
            super()._update(item)
            self.price = item.price
            self.max_possession = item.max_possession
            self.max_purchase = item.max_purchase

    class InventoryManager:
        def __init__(self):
            self.inventory = {}
            self.item_data = {}
            self.shop_item_data = {}

        def init(self):
            self.item_data = {}
            self.shop_item_data = {}

        def check_missing_items(self):
            new_inventory = {}
            for item in self.inventory.keys():
                if item in self.item_data.keys():
                    new_inventory[item] = self.inventory[item]

            self.inventory = new_inventory

        def remove_item(self, key: str, amount: int = -1):
            """
            Remove a specified amount of an item from the inventory.
            If the amount after removal is zero or less, the item is deleted from inventory.
            """
            
            if is_replay():
                return

            if key in self.inventory and amount > 0:
                self.inventory[key].amount -= amount
                if self.inventory[key].amount <= 0:
                    del self.inventory[key]
            elif key in self.inventory and amount == -1:
                del self.inventory[key]

        def add_item(self, item: Union[Item, str]):
            if is_replay():
                return

            item_obj = item

            if isinstance(item, str):
                item_obj = Item(item)

            add_notify_message("Added " + str(item_obj.amount) + "x " + item_obj.get_name())

            if item_obj.key not in self.inventory.keys():
                self.inventory[item_obj.key] = item_obj
            else:
                self.inventory[item_obj.key].amount += item_obj.amount

        def get_item(self, key: str) -> Item:
            if key in self.inventory.keys():
                return self.inventory[key]
            return None

        def has_item_data(self, key: str) -> bool:
            if key in self.item_data.keys():
                return True
            return False

        def get_item_data(self, key: str) -> ItemData:
            if key in self.item_data.keys():
                return self.item_data[key]
            return None

        def has_item(self, key: str) -> bool:
            if key in self.inventory.keys():
                return True
            return False

        def get_item_count(self, key: str) -> int:
            if key in self.inventory.keys():
                return self.inventory[key].amount
            return 0

        def get_all_shop_items(self, ignore_possession: bool = False, ignore_purchase: bool = False) -> List[ShopItemData]:
            items = []
            for item in self.shop_item_data.values():
                if not ignore_possession and item.get_max_possession() <= self.get_item_count(item.key):
                    continue
                if not ignore_purchase and item.get_max_purchase() <= item.get_bought():
                    continue
                items.append(item)
            return items

        def get_inventory(self) -> List[Item]:
            return list(self.inventory.values())

    def has_delivery_today() -> bool:
        for time_str in item_delivery.keys():
            day, month, year = time_str.split(".")
            if time.compare_today(int(day), int(month), int(year)) >= 0:
                return True
        return False

    def get_delivery_today() -> List[str]:
        deliveries = []
        for time_str in item_delivery.keys():
            day, month, year = time_str.split(".")
            if time.compare_today(int(day), int(month), int(year)) >= 0:
                deliveries.extend(item_delivery[time_str])
        return deliveries

    def remove_old_deliveries():
        remaining_deliveries = {}
        for time_str in item_delivery.keys():
            day, month, year = time_str.split(".")
            if time.compare_today(int(day), int(month), int(year)) < 0:
                remaining_deliveries[time_str] = item_delivery[time_str]

        global item_delivery
        item_delivery = remaining_deliveries

    def load_item(item: ItemData):
        inventory_manager.item_data[item.key] = item

        if isinstance(item, ShopItemData):
            inventory_manager.shop_item_data[item.key] = item

########################
# region Computer Shop #

init 1 python:    
    office_building_computer_event["shopping"].add_event(Event(3, "office_building_computer_shopping_event"))

    time_check_events.add_event(
        Event(2, "office_building_computer_shopping_delivery_event",
            TimeCondition(weekday = "1-4", daytime = 1),
            DeliveryCondition(),
        )   
    )


style computer_shop_text:
    color "#000"
    size 20

style computer_shop_text_white take computer_shop_text:
    color "#fff"

label open_office_building_computer_shopping_screen(viewport_value = 0, **kwargs):
    call screen office_building_computer_shopping_screen(viewport_value, **kwargs)
    return

screen office_building_computer_shopping_screen(viewport_value = 0, **kwargs):
    add "images/computer/computer_shop_bg.png"

    $ shop_items = inventory_manager.get_all_shop_items(ignore_possession = True, ignore_purchase = True)
    $ shopping_cart_amount = get_dict_total_count(shopping_cart)

    $ school_money = "Budget: ${:,.2f}".format(money.get_value())

    button:
        xalign 0.1
        ypos 108
        action Call("office_building_computer_shopping_event.after_computer_shopping_screen", **kwargs)
        add "images/icons/stop_idle.webp":
            xsize 100
            ysize 100

    button:
        xalign 0.65
        ypos 108
        ysize 100
        text school_money:
            style "computer_shop_text_white"
            yalign 0.5
        action Return()

    button:
        xalign 0.775
        ypos 108
        add "images/computer/computer_shop_cart_idle.png":
            xsize 100
            ysize 100
        action Call("open_office_building_computer_shopping_cart_screen", **kwargs)

    if len(shopping_cart) > 0:
        add "images/computer/computer_shop_indicator.png":
            xalign 0.785
            ypos 108
            xsize 40
            ysize 40

        $ cart_size = str(shopping_cart_amount) if shopping_cart_amount < 10 else "9+"

        button:
            xalign 0.786
            ypos 110
            xsize 40
            ysize 40
            text cart_size:
                xalign 0.5
                style "computer_shop_text_white"

    python:
        def viewport_change(value):
            viewport_value = value

    frame:
        area(390, 215, 1150, 745)
        background Solid("#fff0")
        viewport id "ComputerShopViewport":
            yadjustment ui.adjustment(range=1, value=viewport_value, changed=viewport_change(value))
            mousewheel True
            draggable "touch"

            $ grid_y = (len(shop_items) + 3) // 4

            grid 4 grid_y:
                xsize 1150
                for i in range(grid_y * 4):
                    if i < len(shop_items):
                        $ item = shop_items[i]

                        $ item_image = item.get_image()
                        $ item_key = item.key
                        $ item_name = item.get_name()
                        $ item_price = "$" + str(item.get_price()) if item.get_price() > 0 else "{color=#00a000}Free{/color}"

                        $ item_max_possession = item.get_max_possession()
                        $ item_max_purchase = item.get_max_purchase()

                        $ item_bought_count = item.get_bought()
                        $ item_in_cart = get_dict_key_count(shopping_cart, item_key)

                        $ item_in_stock = True
                        if item_max_possession <= inventory_manager.get_item_count(item_key) + item_in_cart:
                            $ item_in_stock = False
                        if item_max_purchase <= item_in_cart + item_bought_count:
                            $ item_in_stock = False
                        
                        frame:
                            area(0, 0, 280, 401)
                            background Solid("#fff0")
                            add "images/computer/computer_shop_card.png"
                            add item_image:
                                xalign 0.5
                                ypos 15
                                xsize 235
                                ysize 235
                            text item_name:
                                xalign 0.5
                                ypos 255
                                xsize 235
                                ysize 20
                                style "computer_shop_text"
                            text item_price:
                                xalign 0.5
                                ypos 280
                                xsize 235
                                ysize 20
                                style "computer_shop_text"

                            if item_in_cart == 0:
                                if item_in_stock:
                                    button:
                                        background Solid("#0ab4ddff")
                                        xalign 0.5
                                        ypos 330
                                        xsize 235
                                        ysize 40
                                        action Call("office_building_computer_shopping_screen_change_cart", item, 1, viewport_value, "office_building_computer_shopping_screen", **kwargs)
                                        text "Add to Cart":
                                            xalign 0.5
                                            style "computer_shop_text"
                                else:
                                    button:
                                        background Solid("#222222ff")
                                        xalign 0.5
                                        ypos 330
                                        xsize 235
                                        ysize 40
                                        text "Out of Stock":
                                            xalign 0.5
                                            style "computer_shop_text_white"
                            else:
                                hbox:
                                    xalign 0.5
                                    ypos 330
                                    xsize 235
                                    ysize 40
                                    null width 4
                                    if item_in_cart > 1:
                                        button:
                                            yalign 0.5
                                            xsize 25
                                            action Call("office_building_computer_shopping_screen_change_cart", item, -1, viewport_value, "office_building_computer_shopping_screen", **kwargs)
                                            text "-":
                                                style "computer_shop_text"
                                    else:
                                        button:
                                            yalign 0.5
                                            xsize 25
                                            ysize 40
                                            action Call("office_building_computer_shopping_screen_change_cart", item, -1, viewport_value, "office_building_computer_shopping_screen", **kwargs)
                                            add "images/computer/computer_shop_trash.png":
                                                yalign 0.5
                                                xpos -10
                                                xsize 25
                                                ysize 25
                                    null width 5
                                    button:
                                        xsize 25
                                        ysize 40
                                        text str(item_in_cart):
                                            xalign 0.5
                                            yalign 0.5
                                            style "computer_shop_text"
                                    null width 5
                                    if item_in_stock:
                                        button:
                                            yalign 0.5
                                            xsize 25
                                            action Call("office_building_computer_shopping_screen_change_cart", item, 1, viewport_value, "office_building_computer_shopping_screen", **kwargs)
                                            text "+":
                                                style "computer_shop_text"
                                    else:
                                        null width 25

                    else:
                        null
                        

        vbar value YScrollValue("ComputerShopViewport"):
            unscrollable "hide"
            xalign 1.035

label open_office_building_computer_shopping_cart_screen(viewport_value = 0, **kwargs):
    call screen office_building_computer_shopping_cart_screen(viewport_value, **kwargs)
    return

screen office_building_computer_shopping_cart_screen(viewport_value = 0, **kwargs):
    add "images/computer/computer_shop_cart_bg.png"

    $ shop_items = inventory_manager.get_all_shop_items(ignore_possession = True, ignore_purchase = True)
    $ shopping_cart_amount = get_dict_total_count(shopping_cart)

    $ school_money = "Budget: ${:,.2f}".format(money.get_value())

    button:
        xalign 0.1
        ypos 108
        action Call("office_building_computer_shopping_event.after_computer_shopping_screen", **kwargs)
        add "images/icons/stop_idle.webp":
            xsize 100
            ysize 100

    button:
        xalign 0.65
        ypos 108
        ysize 100
        text school_money:
            style "computer_shop_text_white"
            yalign 0.5
        action Return()

    button:
        xalign 0.775
        ypos 108
        add "images/computer/computer_shop_cart_highlight.png":
            xsize 100
            ysize 100
        action Call("open_office_building_computer_shopping_screen", **kwargs)

    python:
        def viewport_change(value):
            viewport_value = value

    frame:
        area(1260, 215, 250, 740)
        background Solid("#8880")

        $ product_total = 0
        for item_key in shopping_cart.keys():
            $ item = inventory_manager.get_item_data(item_key)
            $ item_price = item.get_price()
            $ item_in_cart = shopping_cart[item_key]
            $ product_total += item_price * item_in_cart if item_price > 0 else 0

        $ shipping_cost = 5 if product_total > 0 else 0.0
        $ full_total = product_total + shipping_cost

        vbox:
            spacing 12
            xsize 250
            # Products-Subtotal
            text "Products:":
                color "#000"
                xalign 0.0
                size 26
            $ products_price_text = "${:,.2f}".format(product_total)
            text products_price_text:
                color "#000"
                xalign 1.0
                size 26

            # Shipping costs
            text "Shipping:":
                color "#000"
                xalign 0.0
                size 26
            text "${:,.2f}".format(shipping_cost):
                color "#000"
                xalign 1.0
                size 26

            # Border line
            add "gui/border_line.png":
                xsize 200
                xalign 0.5
                ysize 1

            # Total
            text "Total:":
                color "#000"
                xalign 0.0
                size 26
            $ total_text = "${:,.2f}".format(full_total)
            text total_text:
                color "#1e90ff"
                xalign 1.0
                size 30
                bold True

            null height 30

            # Checkout button at the bottom, blue, disables if money less than total


        button:
            background Solid("#0ab4ddff")
            xalign 0.5
            yalign 0.95
            
            xsize 235
            ysize 40
            sensitive money.get_value() >= full_total
            action Call("office_building_computer_shopping_screen_checkout", **kwargs)
            text "Checkout":
                xalign 0.5
                yalign 0.5
                style "computer_shop_text"
        


        

    frame:
        area(390, 215, 850, 740)
        background Solid("#8880")
        viewport id "ComputerShopCartViewport":
            yadjustment ui.adjustment(range=1, value=viewport_value, changed=viewport_change(value))
            mousewheel True
            draggable "touch"

            vbox:
                for i, item_key in enumerate(shopping_cart.keys()):
                    $ item = inventory_manager.get_item_data(item_key)
                    
                    $ item_name = item.get_name()
                    $ item_price = item.get_price()
                    $ item_in_cart = shopping_cart[item_key]
                    
                    $ item_max_possession = item.get_max_possession()
                    $ item_max_purchase = item.get_max_purchase()
                    $ item_bought_count = item.get_bought()

                    $ item_price_text = "$" + str(item_price * item_in_cart) if item_price > 0 else "{color=#00a000}Free{/color}"

                    $ item_in_stock = True
                    if item_max_possession <= inventory_manager.get_item_count(item_key) + item_in_cart:
                        $ item_in_stock = False
                    if item_max_purchase <= item_in_cart + item_bought_count:
                        $ item_in_stock = False
                    
                    hbox:
                        xalign 0.0
                        yalign 0.0
                        add item.get_image():
                            xsize 100
                            ysize 100
                        null width 5
                        button:
                            xsize 500
                            ysize 100
                            text item_name:
                                yalign 0.5
                                style "computer_shop_text"
                        null width 5
                        button:
                            xsize 100
                            ysize 100
                            text item_price_text:
                                yalign 0.5
                                style "computer_shop_text"
                        null width 10
                        if item_in_cart > 1:
                            button:
                                yalign 0.5
                                xsize 25
                                action Call("office_building_computer_shopping_screen_change_cart", item, -1, viewport_value, "office_building_computer_shopping_cart_screen", **kwargs)
                                text "-":
                                    style "computer_shop_text"
                        else:
                            button:
                                yalign 0.5
                                xsize 25
                                ysize 100
                                action Call("office_building_computer_shopping_screen_change_cart", item, -1, viewport_value, "office_building_computer_shopping_cart_screen", **kwargs)
                                add "images/computer/computer_shop_trash.png":
                                    yalign 0.5
                                    xpos -10
                                    xsize 25
                                    ysize 25
                        null width 5
                        button:
                            xsize 25
                            ysize 100
                            text str(item_in_cart):
                                xalign 0.5
                                yalign 0.5
                                style "computer_shop_text"
                        null width 5
                        if item_in_stock:
                            button:
                                yalign 0.5
                                xsize 25
                                action Call("office_building_computer_shopping_screen_change_cart", item, 1, viewport_value, "office_building_computer_shopping_cart_screen", **kwargs)
                                text "+":
                                    style "computer_shop_text"

                    if i < len(shopping_cart.keys()) - 1:
                        add "gui/border_line.png":
                            xsize 800
                            xalign 0.5
                            ysize 1
                        

        vbar value YScrollValue("ComputerShopCartViewport"):
            unscrollable "hide"
            xalign 1.035

label office_building_computer_shopping_screen_change_cart(item, delta, viewport_value = 0, label_dest = "office_building_computer_shopping_screen", **kwargs):
    if item.key in shopping_cart.keys():
        $ shopping_cart[item.key] += delta
    elif delta > 0:
        $ shopping_cart[item.key] = delta
    else:
        $ shopping_cart[item.key] = 0
    if shopping_cart[item.key] <= 0:
        $ del shopping_cart[item.key]
    $ renpy.call_screen(label_dest, viewport_value, **kwargs)

label office_building_computer_shopping_screen_checkout(**kwargs):
    python:
        total_price = 0
        for item_key in shopping_cart.keys():
            item = inventory_manager.get_item_data(item_key)
            item_price = item.get_price()
            item_in_cart = shopping_cart[item_key]
            total_price += item_price * item_in_cart if item_price > 0 else 0

        money.change_value(-total_price)
        delivery_time = Time("now")
        delivery_time.add_time(day = 3)

        delivered_items = []
        for item_key in shopping_cart.keys():
            for i in range(shopping_cart[item_key]):
                delivered_items.append(item_key)

        if delivery_time.today() in item_delivery.keys():
            item_delivery[delivery_time.today()].extend(delivered_items)
        else:
            item_delivery[delivery_time.today()] = delivered_items

    call office_building_computer_shopping_event.after_computer_shopping_screen(**kwargs)

label office_building_computer_shopping_delivery_event(**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ deliveries = get_delivery_today()

    secretary "[headmaster_first_name], a package came for you."

    python:
        for item_key in deliveries:
            inventory_manager.add_item(Item(item_key, 1))
    
        remove_old_deliveries()

    $ end_event("map_overview", **kwargs)

# endregion
########################

label load_items:
    $ set_current_mod('base')

    python:
        global inventory_manager
        if inventory_manager is None:
            inventory_manager = InventoryManager()
        inventory_manager.init()
    
    $ load_item(ItemData(
        "generic_bra",
        "Generic Bra",
        "A generic bra that can be used to cover up the breasts.",
        "images/items/generic-bra.png",
    ))
    $ load_item(ItemData(
        "lab_mortar_and_pestle",
        "Mortar and Pestle",
        [
            "A mortar and pestle that can be used to grind ingredients.",
            "",
            "Quest item: Headmaster's Lab Intro",
        ],
        "images/items/mortar-pestle.png",
    ))
    $ load_item(ItemData(
        "lab_distilled_water",
        "Distilled Water",
        [
            "Distilled water that can be used to clean wounds.",
            "",
            "Quest item: Headmaster's Lab Intro",
        ],
        "images/items/distilled-water.png",
    ))
    $ load_item(ItemData(
        "lab_glassware",
        "Glassware",
        [
            "Glassware that can be used to store liquids.",
            "",
            "Quest item: Headmaster's Lab Intro",
        ],
        "images/items/glassware.png",
    ))
    $ load_item(ItemData(
        "lab_utensils",
        "Utensils",
        [
            "Utensils that can be used to cook food.",
            "",
            "Quest item: Headmaster's Lab Intro",
        ],
        "images/items/utensils.png",
    ))
    $ load_item(ItemData(
        "lab_gas_burner",
        "Gas Burner",
        [
            "A gas burner typically used in a laboratory.",
            "",
            "Quest item: Headmaster's Lab Intro",
        ],
        "images/items/gas-burner.png",
    ))
    $ load_item(ItemData(
        "lab_office_supplies",
        "Office Supplies",
        [
            "Office supplies that can be used to write on paper.",
            "",
            "Quest item: Headmaster's Lab Intro",
        ],
        "images/items/office-supplies.png",
    ))
    $ load_item(ShopItemData(
        "lab_chemicals",
        "Chemicals",
        [
            "Chemicals that can be used to create potions.",
            "",
            "Quest item: Headmaster's Lab Intro",
        ],
        "images/items/lab-chemicals.png",
        150,
    ))
    $ load_item(ItemData(
        "lab_furniture",
        "Furniture",
        [
            "Furniture that can be used to set up a lab.",
            "",
            "Quest item: Headmaster's Lab Intro",
        ],
        "images/items/lab-furniture.png",
    ))
    $ load_item(ItemData(
        "lab_test_potion",
        "Test Potion",
        [
            "A test potion that can be used to test the potion. Duh.",
            "",
            "Quest item: Headmaster's Lab Intro",
        ],
        "images/items/lab-test-potion.png",
    ))

    $ inventory_manager.check_missing_items()
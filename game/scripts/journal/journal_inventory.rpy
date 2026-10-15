##############################################################################
# Journal: Inventory (pages 2 and 10)
#
# Left page: a stock list, grouped by the quest an item belongs to.
# Right page: the selected item with its photo, the figures on file and
# its description.
#
# display = "<item key>"
##############################################################################

init python:
    JOURNAL_QUEST_ITEM_PREFIX = "Quest item:"

    def journal_item_details(item_data):
        """
        Splits an item description into its text and the quest it belongs to
        (the "Quest item: <quest>" line), so the quest can head a group on the
        list instead of repeating in every description.

        ### Returns:
        1. Tuple[List[str], str]
            - paragraphs (empty lines dropped), quest name or ""
        """

        paragraphs = []
        quest = ""
        for line in item_data.get_description():
            line = str(line).strip()
            if line.startswith(JOURNAL_QUEST_ITEM_PREFIX):
                quest = line[len(JOURNAL_QUEST_ITEM_PREFIX):].strip()
            elif line:
                paragraphs.append(line)
        return paragraphs, quest

    def journal_inventory_groups(items):
        """
        Items grouped by quest, general items first; order inside a group
        stays the order they were picked up in.
        """

        groups = {}
        for item in items:
            quest = journal_item_details(item.data())[1]
            groups.setdefault(quest, []).append(item)
        order = sorted(groups.keys(), key = lambda quest: (quest != "", quest))
        return [(quest or "General", groups[quest]) for quest in order]

screen journal_inventory(display, page = 10):
    # """
    # Inventory page.
    # """

    tag interaction_overlay
    modal True

    python:
        inventory_items = inventory_manager.get_inventory()
        selected_item = None
        if display != "" and inventory_manager.has_item_data(display) and inventory_manager.has_item(display):
            selected_item = inventory_manager.get_item(display)
        # nothing picked yet: show the first item instead of an empty page
        if selected_item is None and inventory_items:
            selected_item = inventory_items[0]

    use journal_backdrop

    use journal_page_selector(page, display)

    key "K_ESCAPE" action [With(dissolveM), Jump("map_entry")]

    use journal_inventory_list(page, inventory_items, selected_item)

    if selected_item is not None:
        use journal_inventory_item(selected_item)

    use journal_tooltip

screen journal_inventory_list(page, inventory_items, selected_item):
    # """
    # Left page: one ledger row per item, a small print of its photo, the
    # name and the quantity on hand.
    # """

    $ row_h = 58
    $ thumb = 46

    use jr_page("journal_inventory_list", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W

            fixed:
                xysize (JR_LEFT_W, 66)
                text "Inventory" style "jr_title" yalign 1.0
                text ("1 item" if len(inventory_items) == 1 else "{} items".format(len(inventory_items))):
                    style "jr_typed_small"
                    xalign 1.0
                    yalign 1.0
                    yoffset -8
            null height 4
            use jr_double_rule(JR_LEFT_W)

            if not inventory_items:
                null height 22
                text "Nothing in stock yet. Whatever I buy or pick up gets listed here." style "jr_small"

            for group_title, items in journal_inventory_groups(inventory_items):
                null height 22
                use jr_rubric(group_title, JR_LEFT_W)
                null height 4
                for item in items:
                    $ amount_text = "× {}".format(item.amount)
                    $ name = item.data().get_name()
                    fixed:
                        xysize (JR_LEFT_W, row_h)
                        # the leader tile is drawn for a 32px row; centre one in the taller row
                        fixed:
                            xysize (JR_LEFT_W, 32)
                            yalign 0.5
                            # name starts after the button padding (6), thumbnail and spacing
                            use jr_leader(6 + thumb + 16 + journal_text_width(name, size = 22),
                                JR_LEFT_W - journal_text_width(amount_text, style = "jr_value", size = 22))
                        button:
                            style "jr_entry_button"
                            yalign 0.5
                            selected (item is selected_item)
                            action [With(dissolveM), Call("open_journal", page, item.key)]
                            hbox:
                                spacing 16
                                fixed:
                                    xysize (thumb, thumb)
                                    yalign 0.5
                                    add Solid("#00000024") pos (1, 2) xysize (thumb, thumb)
                                    add Solid("#faf7f0") xysize (thumb, thumb)
                                    $ thumb_image = item.data().get_image()
                                    if not journal_is_placeholder_image(thumb_image):
                                        add journal_cover(thumb_image, thumb - 6, thumb - 6) pos (3, 3)
                                text name style "jr_entry_button_text" size 22 yalign 0.5
                        text amount_text style "jr_value" size 22 xalign 1.0 yalign 0.5

screen journal_inventory_item(item):
    # """
    # Right page: photo, figures on file and the description of one item.
    # """

    python:
        item_data = item.data()
        paragraphs, quest = journal_item_details(item_data)
        facts = [("On hand", str(item.amount))]
        if isinstance(item_data, ShopItemData):
            facts.append(("Price", "{:,}".format(item_data.get_price())))
        if quest:
            facts.append(("Needed for", quest))
        item_image = item_data.get_image()
        has_photo = not journal_is_placeholder_image(item_image)
        photo_w = 240
        photo_h = 286
        facts_w = JR_RIGHT_W - photo_w - 28 if has_photo else JR_RIGHT_W

    use jr_page("journal_inventory_item", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W

            text item_data.get_name() style "jr_title"
            null height 4
            use jr_double_rule(JR_RIGHT_W)

            null height 22
            hbox:
                spacing 28
                if has_photo:
                    fixed:
                        # fixed size: the tilted polaroid's bounding box is wider than its frame
                        xysize (photo_w, photo_h)
                        use journal_polaroid(item_image, photo_w, photo_h, 1.5)
                vbox:
                    xsize facts_w
                    use jr_rubric("On file", facts_w)
                    null height 4
                    for label, value in facts:
                        # long values (quest names) get their own line instead of a leader
                        if journal_text_width(label, size = 22) + journal_text_width(value, style = "jr_value", size = 22) + 40 > facts_w:
                            text label style "jr_text" size 22
                            text value style "jr_value" size 22 xalign 1.0 textalign 1.0 xmaximum facts_w
                            null height 6
                        else:
                            fixed:
                                xysize (facts_w, 32)
                                use jr_leader(journal_text_width(label, size = 22),
                                    facts_w - journal_text_width(value, style = "jr_value", size = 22))
                                text label style "jr_text" size 22 yalign 0.5
                                text value style "jr_value" size 22 xalign 1.0 yalign 0.5

            if paragraphs:
                null height 24
                use jr_rubric("Description", JR_RIGHT_W)
                null height 6
                for paragraph in paragraphs:
                    text paragraph style "jr_body"
                    null height 6

##############################################################################
# Collectibles
#
# Photos hidden as small polaroids on location backgrounds. A Collectible has
# one or more CollectibleSpots; each spot names the backgrounds it lies on by
# background key pattern ("school_building_v1_*", see BGImage key) and has its
# own position, tilt, polaroid style and conditions. Clicking the polaroid
# collects the photo: it goes into the journal's Collectibles section (page
# 12) and disappears from every spot. Found photos are kept per save.
#
# Register base collectibles in label load_collectibles, mod collectibles in
# a register_start_method loader, both with register_collectibles(...).
##############################################################################

init -1 python:
    COLLECTIBLE_STYLES = (
        "classic_white", "classic_cream", "classic_faded", "classic_black",
        "instax_mint", "instax_pink", "instax_sky", "taped", "dog_eared",
    )

    # sub pages of the Collectibles section per group type; other group types
    # get a page named after them
    COLLECTIBLE_GROUP_LABELS = {
        "location": "Places",
        "character": "People",
    }

    class CollectibleSpot:
        """
        One place a collectible lies.

        ### Parameters:
        1. background: str
            - Background key pattern: "*" any text, "?" one character,
                "[1-5]" one of those ("school_building_v1_*").
        2. pos: Tuple[int, int]
            - Centre of the polaroid on the 1920x1080 background.
        3. angle: float (default 0)
            - Tilt in degrees.
        4. style: str (default "classic_white")
            - Polaroid sprite, see COLLECTIBLE_STYLES.
        5. *conditions: Condition
            - Only lies here while all of them hold.
        6. zoom: float (default 1.0)
            - Size of the polaroid.
        """

        def __init__(self, background: str, pos: Tuple[int, int], angle: float = 0, style: str = "classic_white", *conditions: Condition, zoom: float = 1.0):
            self.background = background
            self.pos = (int(pos[0]), int(pos[1]))
            self.angle = angle
            self.style = style if style in COLLECTIBLE_STYLES else "classic_white"
            self.conditions = ConditionStorage(*conditions)
            self.zoom = zoom

        def fits(self, background_key: str, **kwargs) -> bool:
            return match_bg_key(self.background, background_key) and self.conditions.is_fulfilled(**kwargs)

        def get_sprite(self) -> str:
            return "gui/journal/collectibles/polaroid_{}.webp".format(self.style)

    class Collectible:
        """
        A photo to find.

        ### Parameters:
        1. key: str
            - Unique key; prefix mod collectibles with the mod key.
        2. image: str
            - The photo; redirected into the current mod's folder.
        3. *elements: CollectibleSpot | Condition
            - Where it lies, and conditions that hold for every spot.
        4. title: str
            - Its name in the album.
        5. description: str (default "")
            - A line under the photo in the album.
        6. groups: Dict[str, str | List[str]] (default None)
            - Album pages it is listed on, e.g. {"location": "school_building",
                "character": ["aona_komuro"]}; values are shown through
                get_translation.
        """

        def __init__(self, key: str, image: str, *elements: CollectibleSpot | Condition, title: str = "", description: str = "", groups: Dict[str, Any] = None):
            self.key = key
            self.image = get_mod_path(active_mod_key) + image
            self.title = title or key
            self.description = description
            self.groups = {}
            for group_type, values in (groups or {}).items():
                self.groups[group_type] = [values] if isinstance(values, str) else list(values)
            self.spots = [element for element in elements if isinstance(element, CollectibleSpot)]
            self.conditions = ConditionStorage(*[element for element in elements if isinstance(element, Condition)])
            self.mod_key = active_mod_key

        def is_found(self) -> bool:
            return self.key in get_found_collectibles()

        def get_spot(self, background_key: str, **kwargs) -> CollectibleSpot:
            """
            The first spot lying on this background, or None.
            """

            if not self.conditions.is_fulfilled(**kwargs):
                return None
            for spot in self.spots:
                if spot.fits(background_key, **kwargs):
                    return spot
            return None

    # filled by every start/after-load wave; definitions are never saved
    collectible_register = {}

    def register_collectibles(*collectibles: Collectible):
        """
        Load or update collectibles. Gated on the current mod being active.
        """

        for collectible in collectibles:
            record_mod_content("collectible", collectible.key)
        if not is_mod_active(active_mod_key):
            return
        for collectible in collectibles:
            collectible_register[collectible.key] = collectible

    def get_collectibles() -> List[Collectible]:
        return list(collectible_register.values())

    def get_found_collectibles() -> List[str]:
        return get_game_data("collectibles_found", None) or []

    def collect_collectible(key: str):
        """
        Puts a photo into the album: a short notification, no time passes.
        """

        if key in get_found_collectibles() or key not in collectible_register:
            return
        set_game_data("collectibles_found", get_found_collectibles() + [key])
        show_notify_message("Photo added to your collection", 12, "")
        renpy.restart_interaction()

    def get_collectible_spots(background_key: str) -> List[Tuple[Collectible, CollectibleSpot]]:
        """
        The polaroids lying on the background on screen.
        """

        if background_key is None or is_in_replay:
            return []
        found = get_found_collectibles()
        spots = []
        for collectible in collectible_register.values():
            if collectible.key in found:
                continue
            spot = collectible.get_spot(background_key)
            if spot is not None:
                spots.append((collectible, spot))
        return spots

    def copy_collectible_spot():
        """
        Cheat mode: puts a CollectibleSpot line for the mouse position on the
        current background into the clipboard, for placing collectibles.
        """

        x, y = renpy.get_mouse_pos()
        line = 'CollectibleSpot("{}", ({}, {}), 0, "classic_white"),'.format(current_bg_key, x, y)
        try:
            import pygame_sdl2
            pygame_sdl2.scrap.put(pygame_sdl2.scrap.SCRAP_TEXT, line.encode("utf-8"))
            renpy.notify("Copied: " + line)
        except Exception as error:
            renpy.notify(line)
            log(f"Could not copy to the clipboard: {error}", log_type="error", category="collectibles")

    def journal_collectible_group_types() -> List[str]:
        types = []
        for collectible in collectible_register.values():
            for group_type in collectible.groups:
                if group_type not in types:
                    types.append(group_type)
        order = list(COLLECTIBLE_GROUP_LABELS.keys())
        return sorted(types, key = lambda group_type: (order.index(group_type) if group_type in order else len(order), group_type))

    def journal_collectible_sections(group_type: str) -> List[Tuple[str, List[Collectible]]]:
        """
        The album's sections for a sub page: one per group value, then the
        collectibles that have no value of that type ("Elsewhere").
        """

        collectibles = sorted(collectible_register.values(), key = lambda collectible: collectible.title)
        if group_type == "all":
            return [("All photos", collectibles)]
        sections = {}
        rest = []
        for collectible in collectibles:
            values = collectible.groups.get(group_type, [])
            if not values:
                rest.append(collectible)
            for value in values:
                sections.setdefault(value, []).append(collectible)
        result = [(get_translation(value), sections[value]) for value in sorted(sections, key = get_translation)]
        if rest:
            result.append(("Elsewhere", rest))
        return result

    def journal_collectibles_display(display: str) -> Tuple[str, str]:
        """
        Splits the page's display string "<group type>|<collectible key>".
        """

        group_type, _, key = (display or "").partition("|")
        if group_type != "all" and group_type not in journal_collectible_group_types():
            group_type = "all"
        return group_type, key

label load_collectibles:
    $ set_current_mod('base')

    $ register_collectibles(
        # placeholder: swap the image for the real photo and place the spot with
        # a middle click in cheat mode (copies the line to the clipboard)
        Collectible("after_lab_intro_10", "images/collectibles/placeholder.webp",
            EventSeenCondition(True, "lab_intro_10"),
            # one spot per corridor view, on floor that stays free at every level;
            # first match wins, so the night shot comes before its view
            CollectibleSpot("school_building_v0_*", (1564, 960), -9, "classic_faded"),
            CollectibleSpot("school_building_v1_night", (1048, 960), 12, "classic_black"),
            CollectibleSpot("school_building_v1_*", (1048, 960), 12, "classic_faded"),
            CollectibleSpot("school_building_v2_*", (964, 888), -6, "classic_faded"),
            title = "After lab intro 10",
            description = "Lying on the floor of the school corridor.",
            groups = {"location": "school_building"}),
    )

    return

##############################
# region Location overlay -- #
##############################

transform collectible_spot_hover:
    on idle:
        easein 0.12 yoffset 0
    on hover:
        easein 0.12 yoffset -3

# Polaroids on the location background while its action menu is open. Shown by
# call_event_menu, hidden by begin_event and the map. No tooltip: finding them
# is the point. The background is itself a screen (image_with_nude_var, zorder
# 0), so this sits at the same zorder and is shown after it: above the
# background, below the menu that call_menu shows next.
screen collectible_spots():
    zorder 0

    for collectible, spot in get_collectible_spots(current_bg_key):
        button at collectible_spot_hover:
            style "empty"
            pos spot.pos
            anchor (0.5, 0.5)
            add Transform(spot.get_sprite(), rotate = spot.angle, zoom = spot.zoom)
            action Function(collect_collectible, collectible.key)

    if cheat_mode:
        key "mouseup_2" action Function(copy_collectible_spot)

# endregion
##############################

#######################
# region Journal --- #
#######################

screen journal_collectibles(display):
    # """
    # Collectibles (page 12): the album on the left, grouped by the open sub
    # page; the picked photo on the right. display = "<group type>|<key>".
    # """

    tag interaction_overlay
    modal True

    default zoomed_image = None

    python:
        group_type, picked_key = journal_collectibles_display(display)
        found = get_found_collectibles()
        sub_entries = [("All", group_type == "all", [With(dissolveM), Call("open_journal", 12, "all|" + picked_key)])]
        for entry_type in journal_collectible_group_types():
            sub_entries.append((COLLECTIBLE_GROUP_LABELS.get(entry_type, entry_type.replace("_", " ").title()), entry_type == group_type,
                [With(dissolveM), Call("open_journal", 12, entry_type + "|" + picked_key)]))
        picked = collectible_register.get(picked_key)
        if picked is None or picked.key not in found:
            picked = next((collectible_register[key] for key in found if key in collectible_register), None)

    use journal_backdrop

    if zoomed_image is None:
        key "K_ESCAPE" action journal_close_action()

    use journal_page_selector(12, display, sub_entries = sub_entries)

    use journal_collectibles_album(group_type, picked, found)
    use journal_collectibles_detail(picked)

    use journal_tooltip

    if zoomed_image is not None:
        use jr_zoom_overlay(zoomed_image)

screen journal_collectibles_detail(picked):
    # """
    # Right page: the picked photo, click to see it big.
    # """

    use jr_page("journal_collectibles_detail", JR_RIGHT_X, JR_RIGHT_W):
        vbox:
            xsize JR_RIGHT_W
            if picked is None:
                text "No photos yet" style "jr_title"
                null height 4
                use jr_double_rule(JR_RIGHT_W)
                null height 14
                text "Photos turn up around the campus once something has happened there. They are small and easy to miss." style "jr_body"
            else:
                text picked.title style "jr_title"
                null height 4
                use jr_double_rule(JR_RIGHT_W)
                null height 22
                button:
                    style "empty"
                    xalign 0.5
                    action SetScreenVariable("zoomed_image", picked.image)
                    use journal_polaroid(picked.image, 500, 430, 1.2)
                if picked.description:
                    null height 22
                    text picked.description style "jr_body"
                for picked_type, values in picked.groups.items():
                    null height 10
                    use journal_credit_row(COLLECTIBLE_GROUP_LABELS.get(picked_type, picked_type.replace("_", " ").title()),
                        ", ".join(get_translation(value) for value in values))

screen journal_collectibles_album(group_type, picked, found):
    # """
    # Left page: small polaroids in rows, an empty frame for every photo not
    # found yet.
    # """

    $ sections = journal_collectible_sections(group_type)
    $ total = len(collectible_register)
    $ found_count = len([key for key in found if key in collectible_register])

    use jr_page("journal_collectibles_album", JR_LEFT_X, JR_LEFT_W):
        vbox:
            xsize JR_LEFT_W
            text "Collectibles" style "jr_title"
            null height 4
            use jr_double_rule(JR_LEFT_W)
            null height 8
            text "{} of {} found".format(found_count, total) style "jr_typed_small"

            for section_title, collectibles in sections:
                null height 22
                use jr_rubric(section_title, JR_LEFT_W)
                null height 12
                vpgrid:
                    cols 4
                    xspacing 16
                    yspacing 18
                    for collectible in collectibles:
                        if collectible.key in found:
                            button:
                                style "empty"
                                xysize (126, 140)
                                selected (picked is not None and picked.key == collectible.key)
                                action [With(dissolveM), Call("open_journal", 12, group_type + "|" + collectible.key)]
                                tooltip collectible.title
                                at collectible_spot_hover
                                use journal_polaroid(collectible.image, 118, 134, (-2.0 if collectible.key == (picked.key if picked else None) else 1.5))
                        else:
                            fixed:
                                xysize (126, 140)
                                add Solid(JR_PENCIL + "30") pos (4, 4) xysize (118, 134)
                                add Solid("#00000000") xysize (118, 134)
                                text "?" style "jr_title" color JR_PENCIL xpos 59 ypos 60 anchor (0.5, 0.5)

# endregion
#######################

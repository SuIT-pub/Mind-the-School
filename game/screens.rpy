################################################################################
# region Initialization
################################################################################

init 0:
    $ set_dissolve()
    $ changelog_shown = True

init offset = -1

# endregion

################################################################################
# region Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

style hide_text:
    color "#00000000"

# endregion

################################################################################
# region In-game screens
################################################################################

init -1 python:
    hidden_zoom_image = None

    def find_zoomed_image():
        """
        The image a journal page is currently showing enlarged, or None.
        The page screens keep it in `zoomed_image` / `zoomed_portrait`, the
        old full-image screen gets it as `image_path`.
        """

        for tag in renpy.get_showing_tags("screens"):
            screen = renpy.get_screen(tag, "screens")
            if screen is None:
                continue
            if screen.screen_name[0] == "max_image_from_journal":
                return screen.scope.get("image_path")
            for name in ("zoomed_image", "zoomed_portrait"):
                if screen.scope.get(name) is not None:
                    return screen.scope[name]
        return None

    def remember_zoomed_image():
        global hidden_zoom_image
        hidden_zoom_image = find_zoomed_image()

    def HideInterface():
        """
        The hide action. Calling trigger_hide ends the called journal screen,
        so an enlarged image has to be grabbed before that and redrawn by
        wait_hide, or hiding the UI would hide the picture too.
        """

        return [Function(remember_zoomed_image), Call("trigger_hide")]

screen wait_hide(image_path = None):
    modal True

    key "h" action Return()
    key "mouseup_2" action Return()

    button:
        xpos 0 ypos 0
        xsize 1920 ysize 1080
        if image_path is not None:
            background Solid("#0b0806")
            add Transform(image_path, fit = "contain", xysize = (1920, 1080)) align (0.5, 0.5)
        action Return()

label trigger_hide():
    if not hide_gui:
        $ hide_gui = True
        window hide
        hide screen custom_menu_choice
        $ quick_menu = False
        call screen wait_hide(hidden_zoom_image)
        $ quick_menu = True
        window show
        $ snapshot_audio_for_rollback()
        $ renpy.rollback(checkpoints = 2, label = "restore_audio_after_rollback")
        $ hide_gui = False
        return

# endregion

# region Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

init python:
    def journal_dialog_box_height(what):
        """
        Height of the dialogue box for a line: at least gui.textbox_height
        (three lines), taller for the rare longer ones so nothing is cut off.
        Measured with the dialogue font at the dialogue width; the box grows
        upwards (it is bottom-aligned).
        """

        minimum = gui.textbox_height
        if not what:
            return minimum
        try:
            _, text_h = Text(what, style = "say_dialogue", size = 33).size(gui.dialogue_width)
        except Exception:
            return minimum
        return int(max(minimum, text_h + gui.dialogue_ypos + 34))

    def shown_dialog_box_height():
        """
        Height of the dialogue box that is on screen right now, or the
        three-line minimum when none is. A menu caption longer than three
        lines grows the box, and the choices have to sit above that, not
        above the minimum.
        """

        # read the text off the say screen itself: a menu caption doesn't
        # always pass through _last_say_what
        say_screen = renpy.get_screen("say")
        if say_screen is None:
            return gui.textbox_height
        return journal_dialog_box_height(say_screen.scope.get("what"))

screen say(who, what, speaker = None):
    style_prefix "say"

    zorder 1

    $ box_height = journal_dialog_box_height(what)

    window:
        ysize box_height

        if renpy.android or renpy.ios:
            if persistent.display_textbox == 0:
                style "window_android"
            elif persistent.display_textbox == 1:
                style "window_1_android"
            else:
                style "window_2"
        else:
            if persistent.display_textbox == 0:
                style "window"
            elif persistent.display_textbox == 1:
                style "window_1"
            else:
                style "window_2"

        # the speaker's roster photo, pinned in the empty space left of the text
        # (people from the character register only; off on phones and in Settings)
        if speaker and persistent.dialog_speaker_photo is not False and not renpy.variant("small") and persistent.display_textbox != 2:
            use dialog_speaker_photo(speaker)

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who"

        # on the full leather box the text needs no outline; at 50% and 0% the
        # scene shows through and the outline keeps it readable
        text what id "what":
            if persistent.display_textbox == 0:
                outlines []
                
    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label:
    outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]
style say_dialogue:
    outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


# The dialogue box matches the journal: a band of the binder's leather with its
# seam (gui/journal/ui/dialog_band*, tools/journal_assets/build_ui.py), the speaker's
# name on an anthracite ribbon, the text in Crimson Pro. The Frame keeps the seam
# at the top when the box is taller (phones).
style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Frame("gui/journal/ui/dialog_band.webp", 0, 30, 0, 0)

style window_1 is window:
    background Frame("gui/journal/ui/dialog_band_50.webp", 0, 30, 0, 0)

style window_2 is window:
    background None

style window_android is window:
    ysize 300

style window_1_android is window_android:
    background Frame("gui/journal/ui/dialog_band_50.webp", 0, 30, 0, 0)

# the ribbon lies across the top edge of the box, like a bookmark
style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos -26
    ysize 62

    background Frame("gui/journal/ui/dialog_name.webp", 16, 0, 34, 0)
    padding (24, 0, 46, 8)

style say_label:
    properties gui.text_properties("name", accent=True)
    font "fonts/CrimsonPro-SemiBold.ttf"
    size 34
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")
    font "fonts/CrimsonPro-Regular.ttf"

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

# endregion

# region Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            spacing 12

            text prompt style "input_prompt"

            # the answer is typed onto a paper slip lying on the leather
            frame:
                style "input_slip"
                input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    font "fonts/CrimsonPro-Regular.ttf"
    size 33
    color "#f4ead6"

style input_slip is empty:
    background Frame("gui/journal/ui/choice_slip.webp", 12, 12)
    padding (22, 10, 26, 18)
    xminimum 560
    xmaximum gui.dialogue_width

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width - 48
    font "fonts/SpecialElite-Regular.ttf"
    size 34
    color "#262428"

# endregion

# region Choice screen ################################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    # Ren'Py's own menu statement, in the same look as the custom menus: paper
    # strips stacked right-aligned on top of the dialogue box (scripts/menu.rpy).
    style_prefix "choice"

    frame:
        background None
        area (0, 0, 1880, 1080 - shown_dialog_box_height() - 6)
        vbox:
            xalign 1.0
            yalign 1.0
            spacing 4
            for index, item in enumerate(items):
                $ stagger = [0, 16, 6, 22, 2, 14, 8][index % 7]
                fixed:
                    fit_first True
                    xalign 1.0
                    xoffset -stagger
                    use jr_choice_slip(item.caption, -1, (item.action is not None), False, item.action)


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")

# endregion

# region Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

init python:
    def quick_menu_entries(touch = False):
        """
        The quick menu's buttons as (icon, tooltip, action, alternate), in the
        order they sit on the patch. Phones get the short list with one
        Menu button, the full journal menu covers the rest there.
        """

        skip = Skip()
        skip_fast = Skip(fast = True, confirm = True)
        auto = Preference("auto-forward", "toggle")
        if touch:
            entries = [
                ("back", _("Back"), Rollback(), None),
                ("skip", _("Skip"), skip, skip_fast),
                ("auto", _("Auto-forward"), auto, None),
                ("menu", _("Menu"), ShowMenu(), None),
                ("hide", _("Hide the interface"), HideInterface(), None),
            ]
        else:
            entries = [
                ("back", _("Back"), Rollback(), None),
                ("history", _("History"), ShowMenu("history"), None),
                ("skip", _("Skip"), skip, skip_fast),
                ("auto", _("Auto-forward"), auto, None),
                ("hide", _("Hide the interface"), HideInterface(), None),
            ]
            if not is_in_replay:
                entries += [
                    ("save", _("Save"), ShowMenu("save"), None),
                    ("qsave", _("Quick save"), QuickSave(), None),
                    ("qload", _("Quick load"), QuickLoad(), None),
                ]
            entries.append(("prefs", _("Settings"), ShowMenu("preferences"), None))
        if is_in_replay:
            entries.append(("end", _("End replay"), Function(end_event, "none", **replay_data), None))
        return entries

    def quick_menu_reserved_height():
        """
        How far up from the bottom edge the quick menu patch reaches (plus a
        small gap), so choice menus without a dialogue box stay clear of it.
        0 while the quick menu is hidden.
        """

        if not store.quick_menu:
            return 0
        return 116 if renpy.variant("touch") else 150

# A stitched leather patch in the bottom right corner of the dialogue box,
# its icons blind-stamped into it (gui/journal/ui/quick_*, leather_patch;
# tools/journal_assets/build_ui.py). It carries its own leather, so it still
# reads when the box is hidden or set to 0%.
screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        $ entries = quick_menu_entries()
        $ columns = 5
        $ rows = (len(entries) + columns - 1) // columns

        frame:
            style "quick_patch"

            grid columns rows:
                for icon, tip, button_action, alternate_action in entries:
                    use quick_menu_button(icon, tip, button_action, alternate_action)
                for i in range(columns * rows - len(entries)):
                    null

        $ tooltip = GetTooltip("quick_menu")
        if tooltip:
            nearrect:
                focus "tooltip"
                prefer_top True

                frame:
                    style "jr_tooltip_frame"
                    xalign 0.5
                    text tooltip style "jr_tooltip_text"

screen quick_menu_button(icon, tip, button_action, alternate_action = None, zoom_factor = 1.0):
    imagebutton:
        style "quick_icon_button"
        idle "gui/journal/ui/quick_{}_idle.webp".format(icon)
        hover "gui/journal/ui/quick_{}_hover.webp".format(icon)
        selected_idle "gui/journal/ui/quick_{}_active.webp".format(icon)
        selected_hover "gui/journal/ui/quick_{}_active.webp".format(icon)
        at Transform(zoom = zoom_factor)
        tooltip tip
        action button_action
        alternate alternate_action


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    outlines [(1, "#000", 0, 0)]
    properties gui.button_text_properties("quick_button")

style quick_patch is empty:
    background Frame("gui/journal/ui/leather_patch.webp", 20, 20, tile = True)
    padding (20, 10, 22, 16)
    xalign 1.0
    yalign 1.0
    offset (-18, -12)

style quick_patch:
    variant "touch"
    padding (24, 14, 26, 20)
    offset (-14, -10)

style quick_icon_button is empty:
    xysize (48, 48)

# endregion

################################################################################
# region Main and Game Menu Screens
################################################################################

#region Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu and refresh_game:
            text "Mod changes detected!\nPlease restart the game!":
                style "mod_menu_description"
                color "#a00000"
                size 24

        if main_menu:
            if not refresh_game:
                textbutton _("New Game") action Start()
            else:
                textbutton _("New Game")
        else:
            textbutton _("History") action ShowMenu("history")
            textbutton _("Save") action ShowMenu("save")

        if not refresh_game or not main_menu:
            textbutton _("Load") action ShowMenu("load")
        else:
            textbutton _("Load")
        textbutton _("Preferences") action ShowMenu("preferences")
        
        if main_menu:
            textbutton _("Mod Manager") action ShowMenu("mod_manager")

        if not main_menu:
            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):
            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            textbutton _("Quit") action Quit(confirm=not main_menu)
    

style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")

# endregion

#region Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

# screen main_menu: the title screen now lives in scripts/journal/journal_title.rpy

style main_menu_board:
    size 35
    font "eraser.regular.ttf"
    hover_color "#a00000"

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")
    font "eraser.regular.ttf"
    outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]

style main_menu_version:
    properties gui.text_properties("version")
    font "eraser.regular.ttf"
    outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]

style main_menu_changelog:
    outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]
style main_menu_changelog_title is main_menu_changelog:
    size 40
    underline True
style main_menu_changelog_subtitle is main_menu_changelog:
    size 25
style main_menu_changelog_text is main_menu_changelog:
    size 18

# endregion

# region Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When
## this screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45

# endregion

# region About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("A Game by Su.iT")
            text _("Version [config.version!t]\n")

            text _("Visit my {a=" + patreon + "}Patreon{/a}")
            text _("Visit my {a=" + discord + "}Discord{/a}")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")
            null height 20
            text _("{b}{u}Assets{/u}{/b}")
            text _("Game artwork © 2023 SuIT-JI, licensed under {a=https://creativecommons.org/licenses/by/4.0/}Creative Commons Attribution 4.0 (CC BY 4.0){/a}.")
            text _("{a=https://icons8.com/icon/82787/externer-link}External Link{/a} Icon by {a=https://icons8.com}Icons8{/a}")
            text _("Icons by {a=https://game-icons.net/}Game-icons.net{/a}")
            text _("Notepad Png vectors by {a=https://lovepik.com/images/png-notepad.html}Lovepik.com{/a}")
            text _("Journal and Main Menu icons created by {a=https://www.flaticon.com/}Flaticon{/a}")
            text _("Crowd ambience \"adult_crowd_ambiance\" by {a=https://freesound.org/people/joedeshon/sounds/119412/}joedeshon{/a}, licensed under {a=https://creativecommons.org/licenses/by/4.0/}CC BY 4.0{/a} (trimmed to a loop, volume changed).")
            text _("Further ambience from {a=https://freesound.org/}Freesound{/a} (CC0).")
            text _("Music by {a=https://freemusicarchive.org/music/purrple-cat/}Purrple Cat{/a}, licensed under {a=https://creativecommons.org/licenses/by/4.0/}CC BY 4.0{/a} and {a=https://creativecommons.org/licenses/by-sa/4.0/}CC BY-SA 4.0{/a}.")
            text _("Journal sounds \"Open and Close a Diary Book\" by {a=https://freesound.org/people/Sabacky/sounds/774136/}Sabacky{/a}, licensed under {a=https://creativecommons.org/licenses/by/4.0/}CC BY 4.0{/a} (split in two, volume changed).")
            text _("Photo sound \"Deal\" by {a=https://freesound.org/people/egomassive/sounds/536784/}egomassive{/a}, from \"Card Flip\" by F4ngy, licensed under {a=https://creativecommons.org/licenses/by/3.0/}CC BY 3.0{/a} (volume changed).")
            text _("Level-up sound \"Tibetan Singing Bowl\" by {a=https://freesound.org/people/Valerie-Vivegnis/sounds/864397/}Valerie-Vivegnis{/a}, licensed under {a=https://creativecommons.org/licenses/by/4.0/}CC BY 4.0{/a} (first strike only, volume changed).")
            text _("Further interface sounds from {a=https://freesound.org/}Freesound{/a} (CC0).")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size

# endregion

# region Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))

screen load():

    tag menu

    use file_slots(_("Load"))

screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            if title == "Save":
                style "page_label"
                xalign 0.9
                textbutton _("Upload Saves") action UploadSync()
            if title == "Load":
                style "page_label"
                xalign 0.9
                textbutton _("Download Saves") action DownloadSync()

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")

# endregion

# region Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

init python:
    def set_dissolve():
        if persistent == None or persistent.transitionSpeed == None:
            persistent.transitionSpeed = 1.75
        dissolveM = Dissolve(0.5 * persistent.transitionSpeed)

    def get_textbox():
        if persistent != None and persistent.display_textbox == None:
            persistent.display_textbox = True
        if persistent == None or persistent.display_textbox:
            return "gui/textbox.png"
        return None

screen preferences():

    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                vbox:
                    style_prefix "radio"
                    label _("Text Box Transparency")
                    textbutton _("100%") action SetField(persistent, "display_textbox", 0)
                    textbutton _("50%") action SetField(persistent, "display_textbox", 1)
                    textbutton _("0%") action SetField(persistent, "display_textbox", 2)

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                if not renpy.android and not renpy.ios:
                    vbox:
                        style_prefix "check"
                        label _("Keyboard Shortcuts")
                        textbutton _("Active") action SetField(persistent, "shortcuts", 0)
                        textbutton _("Hidden") action SetField(persistent, "shortcuts", 1)
                        textbutton _("Disabled") action SetField(persistent, "shortcuts", 2)

                vbox:
                    style_prefix "check"
                    label _("Load Supporter")
                    textbutton _("From Web") action SetField(persistent, "load_supporter", 1)
                    textbutton _("Local only") action SetField(persistent, "load_supporter", 0)

                vbox:
                    style_prefix "check"
                    label _("Tutorial")
                    textbutton _("Enabled") action SetField(persistent, "tutorial", True) 
                    textbutton _("Disabled") action SetField(persistent, "tutorial", False) 

            null height (4 * gui.pref_spacing)


            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Auto-Forward Time")
                    bar value Preference("auto-forward time")

                    label _("Text Speed")
                    bar value Preference("text speed")

                    if preferences.transitions == 2:
                        label _("Transition Speed")
                        bar value FieldValue(
                            persistent, 
                            'transitionSpeed', 
                            2.0, 
                            max_is_zero=False, 
                            style='slider', 
                            offset=0, 
                            step=.2, 
                            action=SetVariable("dissolveM", Dissolve(0.5 * (2.0 - persistent.transitionSpeed)))
                        ) xmaximum 525 alt "Transition Speed"

                vbox:

                    if config.has_music:
                        label _("Music Volume")
                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:
                        label _("Sound Volume")
                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")
                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 675

# endregion

#region History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")

## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }

style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5

# endregion

# region Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Mods"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:
                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help

screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+A"
        text _("Opens the accessibility menu.")

screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up\nClick Rollback Side")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")

screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")


    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()

style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.button_text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0

# endregion

# region Mod screen #################################################################
##
## A screen that gives information about active mods and allows the player to
## enable or disable them.

init -99 python:
    refresh_game = False

screen mod_manager():

    tag menu

    default device = "keyboard"

    use game_menu(_("Mod Manager"), scroll="viewport"):

        vbox:
            text "After activating or deactivating any mods, you have to restart the game to apply changes.\nOnly install mods you trust. Mods can contain malicious code.\nI am not responsible for any damage caused by third-party mods.":
                style "mod_menu_description"
                color "#fff"
            null height 20

            if refresh_game:
                text "Please restart the game to apply changes!":
                    style "mod_menu_description"
                    color "#a00000"
                    size 24
                null height 20

            for mod_key in persistent.modList.keys():
                python:
                    mod = persistent.modList[mod_key]
                    # if not mod['available']:
                        # continue

                    mod_name = mod['name']
                    mod_author = "by " + mod['author']
                    mod_version = "Version " + mod['version']

                if not mod['available']:
                    continue
                # null width 1600
                hbox:
                    text mod_name:
                        style "mod_menu_title"
                    null width 5
                    text mod_author:
                        style "mod_menu_author"
                        yalign 1.0
                    null width 50
                    text mod_version:
                        style "mod_menu_version"
                        yalign 1.0
                
                null height 5

                $ mod_description = mod['description']
                text mod_description:
                    style "mod_menu_description"
                    xpos 20
                
                null height 5

                $ mod_stats = "Events: " + str(get_mod_content_counts(mod_key).get("event", 0)) + "    Translation files: " + str(len(mod['translations']))
                text mod_stats:
                    style "mod_menu_description"
                    xpos 20

                if mod['key'] != "base":
                    null height 5
                    if not mod['active']:
                        text "This mod is not enabled!":
                            style "mod_menu_description"
                            xpos 20

                        button:
                            xpos 20
                            text _("Enable Mod"):
                                style "mod_menu_button"
                            action [Function(activate_mod, mod['key']), SetVariable("refresh_game", True)]
                    else:
                        button:
                            xpos 20
                            text _("Disable Mod"):
                                style "mod_menu_button"
                            action [Function(deactivate_mod, mod['key']), SetVariable("refresh_game", True)]

                null height 20




style mod_menu_title:
    properties gui.button_text_properties("help_button")
    size 32
style mod_menu_author:
    properties gui.button_text_properties("help_button")
    size 18
    color "#888"
style mod_menu_version:
    properties gui.button_text_properties("help_button")
    size 24
    color "#aaa"
style mod_menu_description:
    properties gui.button_text_properties("help_button")
    size 18
    color "#ccc"
style mod_menu_button:
    properties gui.button_properties("help_button")
    size 24

# endregion

################################################################################
# region Additional screens
################################################################################


# region Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    # a paper slip like the journal's notes; works on the title screen and in game
    add Solid("#140d08a8")

    frame:
        xalign 0.5
        yalign 0.45
        xmaximum 760
        background Frame("gui/journal/ui/foldout_panel.webp", 12, 12)
        padding (48, 36, 48, 34)
        at Transform(rotate = -0.8, rotate_pad = False)

        vbox:
            spacing 30
            text _(message):
                style "jr_text"
                size 30
                xalign 0.5
                textalign 0.5
                layout "subtitle"

            hbox:
                xalign 0.5
                spacing 90
                textbutton _("Yes ›"):
                    style "jr_entry_button"
                    text_style "jr_value"
                    text_size 30
                    text_color JR_ACCENT
                    action yes_action
                textbutton _("No"):
                    style "jr_entry_button"
                    text_style "jr_entry_button_text"
                    text_size 30
                    action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")

# endregion

# region Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"

## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat

style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

# skipping: a small leather patch, like the quick menu's
style skip_frame:
    ypos gui.skip_ypos
    xpos 14
    background Frame("gui/journal/ui/leather_patch.webp", 20, 20, tile = True)
    padding (20, 8, 24, 14)

style skip_text:
    font "fonts/CrimsonPro-SemiBold.ttf"
    color "#f4ead6"
    size 22

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"

# endregion

# region Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0

style notify_frame is empty
style notify_text is gui_text

# Ren'Py's own notices ("Quick save complete" ...): the same paper slip as the game's notifications
style notify_frame:
    ypos gui.notify_ypos
    xpos 14

    background Frame("gui/journal/ui/choice_slip.webp", 12, 12)
    padding (20, 9, 24, 17)

style notify_text:
    font "fonts/CrimsonPro-SemiBold.ttf"
    color "#342820"
    size 21

# endregion

# region NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0

screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id

## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")

# endregion
# endregion

################################################################################
# region Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        # one row of bigger icons, no tooltips (nothing hovers on a touch screen)
        frame:
            style "quick_patch"

            hbox:
                spacing 6
                for icon, tip, button_action, alternate_action in quick_menu_entries(touch = True):
                    use quick_menu_button(icon, tip, button_action, alternate_action, 1.25)


style window:
    variant "small"
    background Frame("gui/journal/ui/dialog_band.webp", 0, 30, 0, 0)

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900

# endregion
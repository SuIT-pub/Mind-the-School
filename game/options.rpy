## This file contains options that can be changed to customize your game.
##
## Lines beginning with two '#' marks are comments, and you shouldn't uncomment
## them. Lines beginning with a single '#' mark are commented-out code, and you
## may want to uncomment them when appropriate.

define build.itch_project = "Suit-Ji/mind-the-school"


## Basics ######################################################################

## A human-readable name of the game. This is used to set the default window
## title, and shows up in the interface and error reports.
##
## The _() surrounding the string marks it as eligible for translation.

define config.name = _("Mind the School")


## Determines if the title given above is shown on the main menu screen. Set
## this to False to hide the title.

define gui.show_name = True


## The version of the game.

define config.version = "0.2.1A"


## Text that is placed on the game's about screen. Place the text between the
## triple-quotes, and leave a blank line between paragraphs.

define gui.about = _p("""
""")


## A short name for the game used for executables and directories in the built
## distribution. This must be ASCII-only, and must not contain spaces, colons,
## or semicolons.

define build.name = "MindTheSchool"


## Sounds and music ############################################################

## These three variables control, among other things, which mixers are shown
## to the player by default. Setting one of these to False will hide the
## appropriate mixer.

define config.has_sound = True
define config.has_music = False
define config.has_voice = False


## To allow the user to play a test sound on the sound or voice channel,
## uncomment a line below and use it to set a sample sound to play.

# define config.sample_sound = "sample-sound.ogg"
# define config.sample_voice = "sample-voice.ogg"


## Uncomment the following line to set an audio file that will be played while
## the player is at the main menu. This file will continue playing into the
## game, until it is stopped or another file is played.

# define config.main_menu_music = "main-menu-theme.ogg"


## Transitions #################################################################
##
## These variables set transitions that are used when certain events occur.
## Each variable should be set to a transition, or None to indicate that no
## transition should be used.

default persistent.transition_speed = 1.75
default dissolveM = Dissolve(0.5 * (2.0 - persistent.transition_speed))

default persistent.display_textbox = 0

default persistent.tutorial = True

## Entering or exiting the game menu.

define config.enter_transition = dissolve
define config.exit_transition = dissolve


## Between screens of the game menu.

define config.intra_transition = dissolve


## A transition that is used after a game has been loaded.

define config.after_load_transition = None


## Used when entering the main menu after the game has ended.

define config.end_game_transition = None


## A variable to set the transition used when the game starts does not exist.
## Instead, use a with statement after showing the initial scene.


## Window management ###########################################################
##
## This controls when the dialogue window is displayed. If "show", it is always
## displayed. If "hide", it is only displayed when dialogue is present. If
## "auto", the window is hidden before scene statements and shown again once
## dialogue is displayed.
##
## After the game has started, this can be changed with the "window show",
## "window hide", and "window auto" statements.

define config.window = "auto"

## Transitions used to show and hide the dialogue window

define config.window_show_transition = Dissolve(0.5 * (2.0 - persistent.transition_speed))
define config.window_hide_transition = Dissolve(0.5 * (2.0 - persistent.transition_speed))

default persistent.shortcuts = 0
default persistent.load_supporter = 1

## Preference defaults #########################################################

## Controls the default text speed. The default, 0, is infinite, while any other
## number is the number of characters per second to type out.

default preferences.text_cps = 0


## The default auto-forward delay. Larger numbers lead to longer waits, with 0
## to 30 being the valid range.

default preferences.afm_time = 15


default persistent.modList = {
    'base': {'key': 'base', 'version': '1', 'name': 'Base Mod', 'description': 'The base mod for the game.', 'author': 'SuIT-Ji', 'active': True, 'path': ''},
}

## Save directory ##############################################################
##
## Controls the platform-specific place Ren'Py will place the save files for
## this game. The save files will be placed in:
##
## Windows: %APPDATA\RenPy\<config.save_directory>
##
## Macintosh: $HOME/Library/RenPy/<config.save_directory>
##
## Linux: $HOME/.renpy/<config.save_directory>
##
## This generally should not be changed, and if it is, should always be a
## literal string, not an expression.

define config.save_directory = "MindtheSchool-1679668774"


## Icon ########################################################################
##
## The icon displayed on the taskbar or dock.

define config.window_icon = "gui/window_icon.png"


## Gallery #####################################################################
##
## The persistent variable that stores gallery images.

default persistent.gallery = {}
default persistent.gallery_version = ""
default persistent.fragment_gallery = {}


## Build configuration #########################################################
##
## This section controls how Ren'Py turns your project into distribution files.

init python:

    ## The following functions take file patterns. File patterns are case-
    ## insensitive, and matched against the path relative to the base directory,
    ## with and without a leading /. If multiple patterns match, the first is
    ## used.
    ##
    ## In a pattern:
    ##
    ## / is the directory separator.
    ##
    ## * matches all characters, except the directory separator.
    ##
    ## ** matches all characters, including the directory separator.
    ##
    ## For example, "*.txt" matches txt files in the base directory, "game/
    ## **.ogg" matches ogg files in the game directory or any of its
    ## subdirectories, and "**.psd" matches psd files anywhere in the project.

    ## Classify files as None to exclude them from the built distributions.

    ## Classify files as None to exclude them from the built distributions.

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**.psd', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/**.ini', None)
    build.classify('**/thumbs.db', None)
    build.classify("game/**.rpy", None)
    build.classify("game/saves", None)
    build.classify("game/classes_patch.rpyc", None)
    build.classify("game/cheat_patch.rpyc", None)
    build.classify("event backup/**", None)
    build.classify("*android.json", None)
    build.classify("Members", None)
    build.classify("Test", None)
    build.classify("Image Converter", None)
    build.classify("cspell.json", None)

    ## Files matching documentation patterns are duplicated in a mac app
    ## build, so they appear in both the app and the zip file.

    build.documentation('docs/html/**')
    build.classify('*.txt', None)
    build.classify('*.docx', None)
    build.classify('*.xlsx', None)
    build.classify('*.xlsm', None)
    build.classify('**.xcf', None)

    # Declare three archives.
    build.archive("scripts", "all")
    build.archive("images", "all")
    build.archive("sounds", "all")
    build.archive("data", "all")
    build.archive("mods", "all")

    # Put script files into the scripts archive.
    build.classify("game/**.ttf", "scripts")
    build.classify("game/*.rpyc", "scripts")
    build.classify("game/scripts/**.rpyc", "scripts")
    build.classify("game/python-packages/**", "scripts")

    build.classify("game/**.rpym", "data")
    build.classify("game/members.csv", "data")
    build.classify("game/translations.csv", "data")
    build.classify("game/loli_filter", "data")
    build.classify("LICENSE", "data")
    build.classify("README.md", "data")

    # Put images into the images archive.
    build.classify("game/**.jpg", "images")
    build.classify("game/**.png", "images")
    build.classify("game/**.avi", "images")
    build.classify("game/**.webp", "images")
    build.classify("game/**.webm", "images")

    # Put sounds into the sounds archive.
    build.classify("game/**.ogg", "sounds")
    build.classify("game/**.wav", "sounds")
    build.classify("game/**.mp3", "sounds")

    build.classify("game/mods/**", "mods")


    build.include_i686 = False

init python:
    config.keymap["hide_windows"] = []
    
    config.underlay.append(
        renpy.Keymap( 
            K_h = renpy.curry(renpy.run)( Call("trigger_hide") )
        )
    )
    config.underlay.append(
        renpy.Keymap( 
            mouseup_2 = renpy.curry(renpy.run)( Call("trigger_hide") )
        )
    )
            

## A Google Play license key is required to download expansion files and perform
## in-app purchases. It can be found on the "Services & APIs" page of the Google
## Play developer console.

# define build.google_play_key = "..."


## The username and project name associated with an itch.io project, separated
## by a slash.

# define build.itch_project = "renpytom/test-project"


    

define discord = 'https://discord.suit-ji.com'
define patreon = 'https://patreon.suit-ji.com'
define wiki    = 'https://wiki.suit-ji.com'
##############################################################################
# The base game's interface sounds (system: audio.rpy, guide: wiki/Audio.md).
#
# All from Freesound, CC0 / CC BY 3.0 / CC BY 4.0 (game/audio/ui/CREDITS.txt).
# The files are already levelled against each other; volume= is the ear pass.
##############################################################################

init 1 python:
    set_current_mod('base')

    register_ui_sound("journal_open", "audio/ui/journal-open.ogg")
    register_ui_sound("journal_close", "audio/ui/journal-close.ogg")
    register_ui_sound("page_turn", "audio/ui/page-turn.ogg")
    # choice, notify and journal_entry are the same pencil: what the player
    # writes, what the school slips in, and the journal filling up
    register_ui_sound("choice", "audio/ui/choice.ogg")
    register_ui_sound("notify", "audio/ui/notify.ogg")
    register_ui_sound("journal_entry", "audio/ui/journal-entry.ogg")
    register_ui_sound("collect", "audio/ui/collect.ogg")
    register_ui_sound("gift", "audio/ui/gift.ogg")
    register_ui_sound("milestone", "audio/ui/milestone.ogg")

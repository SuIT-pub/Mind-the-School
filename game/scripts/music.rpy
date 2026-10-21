##############################################################################
# The base game's music (system: audio.rpy, guide: wiki/Audio.md).
#
# All tracks: Purrple Cat, freemusicarchive.org, CC BY 4.0 or CC BY-SA 4.0
# (game/audio/music/CREDITS.txt). The files are only converted to Ogg, never
# edited: loudness is matched with loudness=, end silence skipped with end=.
# loudness = integrated LUFS (ITU-R BS.1770), measured 2026-10-21.
##############################################################################

init 1 python:
    set_current_mod('base')

    # one track per part of the day, played once when that daytime begins
    register_map_music("school", MusicStorage(None,
        MusicTrack("audio/music/look-on-the-bright-side.ogg", 1, TimeCondition(daytime = "1,2"), loudness = -12.1),
        MusicTrack("audio/music/coffee-jelly.ogg", 1, TimeCondition(daytime = "3,4,5"), loudness = -11.0),
        MusicTrack("audio/music/the-golden-ratio.ogg", 1, TimeCondition(daytime = 6), loudness = -13.0),
        MusicTrack("audio/music/walking-to-the-park-at-3-a-m.ogg", 1, TimeCondition(daytime = 7), loudness = -16.7),
    ))

    # the quiet bed under every scene; kept plain on purpose, so it can run
    # under hundreds of events without being noticed as a loop
    register_music_pool("bed",
        MusicTrack("audio/music/brain-fog.ogg", loudness = -14.5, end = 135.3),
        MusicTrack("audio/music/im-lost-but-thats-ok.ogg", loudness = -14.2, end = 156.3),
        MusicTrack("audio/music/bookworm.ogg", loudness = -9.6, end = 185.5),
    )

    # tea, blanket, a quiet evening: for scenes that want to feel snug
    register_music_pool("cozy",
        MusicTrack("audio/music/cold-rainy.ogg", loudness = -12.0, end = 155.3),
    )

    register_menu_music(MusicTrack("audio/music/coffee-jelly.ogg", loudness = -11.0))

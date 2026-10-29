## Incest Content: scenes in which family members are intimate together.
## Kept out of the base game; everything here is gated on the "incest" kink,
## so players with the mod can still turn it off.

init -97 python:
    register_mod(
        "incest_content",
        "Incest Content",
        "1",
        "IncestContent",
        description = "Adds the scenes in which family members are intimate together. Everything it adds can be switched off with the Incest content preference.",
        author = "SuIT-Ji",
        kinks = [
            Kink("incest", "Incest", "Scenes in which family members are intimate together."),
        ],
    )

# init 2: the base game creates its building events in init 1, and at the same
# priority this file would run first (mods/ sorts before scripts/)
init 2 python:
    set_current_mod('incest_content')

    # Twins changing (school dormitory): from level 7 both twins invite him in.
    # The base event keeps its conditions and its stills up to level 6; this
    # mod plays its own scene, with the level-7+ stills and videos it ships.
    set_event_label("sd_event_5", "incest_sd_event_5", title = "Twins changing (Incest Content)")
    incest_sd_event_5_pattern = Pattern("main", "images/events/school dormitory/sd_event_5/sd_event_5 <school_level> <step>.webp", "school_level")

#####################################
# region Twins changing (sd_event_5) #

define incest_sde5_path = "mods/IncestContent/images/events/school dormitory/sd_event_5/sd_event_5 "
image anim_sd_event_5_7_5   = Movie(play = incest_sde5_path + "7 5.webm",   start_image = incest_sde5_path + "7 5.webp", loop = True)
image anim_sd_event_5_7_6   = Movie(play = incest_sde5_path + "7 6.webm",   start_image = incest_sde5_path + "7 6.webp", loop = True)
image anim_sd_event_5_7_7   = Movie(play = incest_sde5_path + "7 7.webm",   start_image = incest_sde5_path + "7 7.webp", loop = True)
image anim_sd_event_5_7_8   = Movie(play = incest_sde5_path + "7 8.webm",   start_image = incest_sde5_path + "7 8.webp")
image anim_sd_event_5_7_9   = Movie(play = incest_sde5_path + "7 9.webm",   start_image = incest_sde5_path + "7 9.webp")
image anim_sd_event_5_7_10  = Movie(play = incest_sde5_path + "7 10.webm",  start_image = incest_sde5_path + "7 10.webp", loop = True)
image anim_sd_event_5_8_5   = Movie(play = incest_sde5_path + "8 5.webm",   start_image = incest_sde5_path + "8 5.webp", loop = True)
image anim_sd_event_5_8_6   = Movie(play = incest_sde5_path + "8 6.webm",   start_image = incest_sde5_path + "8 6.webp", loop = True)
image anim_sd_event_5_8_7   = Movie(play = incest_sde5_path + "8 7.webm",   start_image = incest_sde5_path + "8 7.webp", loop = True)
image anim_sd_event_5_8_8   = Movie(play = incest_sde5_path + "8 8.webm",   start_image = incest_sde5_path + "8 8.webp", loop = True)
image anim_sd_event_5_8_9   = Movie(play = incest_sde5_path + "8 9.webm",   start_image = incest_sde5_path + "8 9.webp", loop = True)
image anim_sd_event_5_8_10  = Movie(play = incest_sde5_path + "8 10.webm",  start_image = incest_sde5_path + "8 10.webp", loop = True)
image anim_sd_event_5_8_11  = Movie(play = incest_sde5_path + "8 11.webm",  start_image = incest_sde5_path + "8 11.webp")
image anim_sd_event_5_8_12  = Movie(play = incest_sde5_path + "8 12.webm",  start_image = incest_sde5_path + "8 12.webp", loop = True)
image anim_sd_event_5_9_5   = Movie(play = incest_sde5_path + "9 5.webm",   start_image = incest_sde5_path + "9 5.webp", loop = True)
image anim_sd_event_5_9_6   = Movie(play = incest_sde5_path + "9 6.webm",   start_image = incest_sde5_path + "9 6.webp", loop = True)
image anim_sd_event_5_9_7   = Movie(play = incest_sde5_path + "9 7.webm",   start_image = incest_sde5_path + "9 7.webp", loop = True)
image anim_sd_event_5_9_8   = Movie(play = incest_sde5_path + "9 8.webm",   start_image = incest_sde5_path + "9 8.webp", loop = True)
image anim_sd_event_5_9_9   = Movie(play = incest_sde5_path + "9 9.webm",   start_image = incest_sde5_path + "9 9.webp", loop = True)
image anim_sd_event_5_9_10  = Movie(play = incest_sde5_path + "9 10.webm",  start_image = incest_sde5_path + "9 10.webp", loop = True)
image anim_sd_event_5_9_11  = Movie(play = incest_sde5_path + "9 11.webm",  start_image = incest_sde5_path + "9 11.webp")
image anim_sd_event_5_9_12  = Movie(play = incest_sde5_path + "9 12.webm",  start_image = incest_sde5_path + "9 12.webp", loop = True)
image anim_sd_event_5_10_5  = Movie(play = incest_sde5_path + "10 5.webm",  start_image = incest_sde5_path + "10 5.webp", loop = True)
image anim_sd_event_5_10_6  = Movie(play = incest_sde5_path + "10 6.webm",  start_image = incest_sde5_path + "10 6.webp", loop = True)
image anim_sd_event_5_10_7  = Movie(play = incest_sde5_path + "10 7.webm",  start_image = incest_sde5_path + "10 7.webp", loop = True)
image anim_sd_event_5_10_8  = Movie(play = incest_sde5_path + "10 8.webm",  start_image = incest_sde5_path + "10 8.webp", loop = True)
image anim_sd_event_5_10_9  = Movie(play = incest_sde5_path + "10 9.webm",  start_image = incest_sde5_path + "10 9.webp", loop = True)
image anim_sd_event_5_10_10 = Movie(play = incest_sde5_path + "10 10.webm", start_image = incest_sde5_path + "10 10.webp", loop = True)
image anim_sd_event_5_10_11 = Movie(play = incest_sde5_path + "10 11.webm", start_image = incest_sde5_path + "10 11.webp")
image anim_sd_event_5_10_12 = Movie(play = incest_sde5_path + "10 12.webm", start_image = incest_sde5_path + "10 12.webp", loop = True)

# The opening is the base scene's, word for word; only "Stay watching" leads
# into this mod's version.
label incest_sd_event_5 (**kwargs):
    $ begin_event(**kwargs)

    $ school_level = get_level('school_level', **kwargs)
    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)
    subtitles "You peek into a room."
    $ image.show(1)
    headmaster.think "Oh the siblings are changing."
    $ image.show(2)
    headmaster.think "But nice view!"

    $ call_custom_menu_with_text("Continue watching?", character.subtitles, False,
        MenuElement("Leave", "Leave", EventEffect("sd_event_5.leave")),
        MenuElement("Stay watching", "Stay watching", EventEffect("incest_sd_event_5.stay")),
    **kwargs)

label .stay (**kwargs):
    # below level 7, or with the kink turned down: the base game's version
    if school_level < 7 or not kink_check("incest"):
        $ renpy.call("sd_event_5.stay", **kwargs)

    $ begin_event(**kwargs)

    # the level-7+ stills and videos ship with this mod, from step 3 on (steps
    # 0-2 stay in the base game, and a series counts up from its first step)
    $ image = Image_Series_Pattern(incest_sd_event_5_pattern, step_start = 3, **kwargs)

    if school_level >= 8:
        $ image.show(3)
        luna "Oh Mr. [headmaster_last_name], you're watching?"
        $ image.show(4)
        seraphina "Why not join us?"
        $ image.show_video(5)
        seraphina "Ahh, you're so big!"
        $ image.show_video(6, pause = True)
        $ image.show_video(7, pause = True)
        $ image.show_video(8, pause = True)
        $ image.show_video(9, pause = True)
        $ image.show_video(10, pause = True)
        $ image.show_video(11)
        $ renpy.pause(5.3333)
        $ image.show_video(12)
        luna "Mr. [headmaster_last_name], that was amazing!"

        call change_stats_with_modifier(
            inhibition = DEC_SMALL, corruption = SMALL, charm = TINY, happiness = SMALL
        ) from _call_incest_sd_event_5_stay_2
    else:
        $ image.show(3)
        luna "Oh Mr. [headmaster_last_name], you're watching?"
        $ image.show(4)
        seraphina "Do you like what you see?"
        luna "Why not make it fair and show us yours?"
        $ image.show_video(5)
        seraphina "Wow Mr. [headmaster_last_name], you're quite big!"
        $ image.show_video(6)
        seraphina "Hmm, you like that?"
        $ image.show_video(7, pause = True)
        $ image.show_video(8)
        $ renpy.pause(7.61)
        $ image.show_video(9)
        $ renpy.pause(5.3333)
        $ image.show_video(10, pause = True)
        luna "Thanks for the meal!"

        call change_stats_with_modifier(
            inhibition = DEC_SMALL, corruption = SMALL, charm = TINY, happiness = SMALL
        ) from _call_incest_sd_event_5_stay_1

    $ end_event(END_NEW_DAYTIME, **kwargs)

# endregion
#####################################

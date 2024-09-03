init 2 python:
    set_current_mod('version_0_1_5')

    # overwrite_event_image('sb_event_5', 'main', Pattern('main', 'images/test_image <step>.png'))
    mod_sb_event5 = Event(3, "sb_event_6",
        TimeCondition(daytime = "c", weekday = "d"),
        RandomListSelector('girls', 'Ikushi Ito', 'Soyoon Yamamoto', 'Yuriko Oshima'),
        Pattern('main', "/images/events/school building/sb_event_5 <school_level> <girls> <step>.webp",'school_level', 'girls', key = 'version_0_1_5'),
        thumbnail = "images/events/school building/sb_event_5 1 Soyoon Yamamoto 11.webp")

    sb_events["patrol"].add_event(mod_sb_event5)
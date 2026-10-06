init 1 python:
    set_current_mod('base')

    # Threshold reactions are real events (gallery / seen / begin_event), but they
    # are only fired by AutoThreshold EventEffects — not from a map location pool.
    nm_threshold_events = EventStorage("nm_thresholds", "misc")
    nm_threshold_events.add_event(
        Event(2, "nm_thresh_emiko_nudge", override_location="misc"),
        Event(2, "nm_thresh_district_letter", override_location="misc"),
        Event(2, "nm_thresh_first_warmth", override_location="misc"),
        Event(2, "nm_thresh_yulan_thaw", override_location="misc"),
        Event(2, "nm_thresh_adelaide_note", override_location="misc"),
        Event(2, "nm_thresh_near_end", override_location="misc"),
    )

    # Resolution scenes are events too (begin_event/end_event, gallery, patterns); they
    # are only fired by the Situation's resolution EventEffect, never from a pool.
    nm_resolution_events = EventStorage("nm_resolutions", "misc")
    nm_resolution_events.add_event(
        Event(2, "new_management_positive_resolve",
            Pattern("main", "images/events/new_management/new_management_positive_resolve/new_management_positive_resolve 1.webp"),
            override_location="misc"),
    )

    # --- nm_ghost_office (-25 ... -8) ---
    # TEMPLATE BAND. This band is the reference build for the redesign: it uses
    # Selectors (variety), Conditions on menu choices (earned/reactive options),
    # paperdoll portraits + reused backgrounds (visuals with zero new art), and
    # GameData flags (cross-event memory) so the four scenes read as one arc.
    office_building_events["look_around"].add_event(Event(
        3,
        "nm_ghost_office_nameplate",
        TimeCondition(weekday="d", daytime="f"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_ghost_office"),
        # Variety: the way the campus mislabels the office changes each visit.
        RandomListSelector("wrong_name", "HEADMSTER", "H. MASTAR", "MR. HEADMAN", "THE NEW GUY", "MR. WHATSHISNAME"),
        # Gallery-registered readings: Standing (reactive line) + Charm (gated choice).
        # Key for the bar selector MUST match get_bar_value's composite key.
        SituationBarSelector("situation:new_management:main", "new_management", "main"),
        StatSelector("charm", CHARM, "school", [20, 100]),
        # Scene image for the non-dialogue establishing beat (the door itself).
        # show_pattern() degrades gracefully: nothing shows until the file exists.
        Pattern("bg", "images/background/office building/f.webp"),
        Pattern("main", "images/events/new_management/nm_ghost_office_nameplate/nm_ghost_office_nameplate <wrong_name> <step>.webp", "wrong_name")))
    office_building_events["call_secretary"].add_event(Event(
        3,
        "nm_ghost_office_private_line",
        TimeCondition(weekday="d", daytime="d"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_ghost_office"),
        # Variety: which "loud" item sits on top of the stack she's holding back.
        RandomListSelector("loud_slip", "a third call from a parent", "a teacher complaint", "a note that just says 'concerned observer'", "a district reminder"),
        # Gallery-registered readings: Standing gates the "honest" choice; flags drive
        # the conditional plaque line and the guided-tutorial companion line.
        SituationBarSelector("situation:new_management:main", "new_management", "main"),
        GameDataSelector("door_claimed", "nm_door_claimed", 0),
        GameDataSelector("guided", "new_management_guided", 0)))
    courtyard_events["patrol"].add_event(Event(
        3,
        "nm_ghost_office_janitor",
        OR(TimeCondition(daytime="f", weekday="d"), TimeCondition(daytime="d", weekday="w")),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_ghost_office"),
        # Variety: a random classmate stands with Aona, and the role they mistake
        # him for rerolls — so the "janitor" beat is not the same joke twice.
        RandomListSelector("bystander", "ikushi_ito", "lin_kato", "ishimaru_maki"),
        RandomListSelector("wrong_role", "the maintenance guy", "a substitute", "somebody's dad", "the new caretaker"),
        # Gallery-registered reading: did the player already claim the office door?
        GameDataSelector("door_claimed", "nm_door_claimed", 0),
        # Scene image for the establishing beat (the group sizing him up).
        Pattern("main", "images/events/new_management/nm_ghost_office_janitor/nm_ghost_office_janitor <step>.webp")))
    sb_events["patrol"].add_event(Event(
        3,
        "nm_ghost_office_empty_corridor",
        TimeCondition(weekday="d", daytime="f"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_ghost_office"),
        # Variety: what Yulan is buried in when he passes.
        RandomListSelector("folder_topic", "a history outline for 3A", "a politics seminar plan", "a stack of marked essays", "a staff-meeting agenda"),
        # Gallery-registered readings: Education gates the "talk shop" choice;
        # the face flag decides whether Yulan's freeze half-melts.
        StatSelector("education", EDUCATION, "school", [20, 100]),
        GameDataSelector("face_known", "nm_face_introduced", 0),
        # Scene image for the establishing beat (empty hallway, Yulan not looking up).
        Pattern("main", "images/events/new_management/nm_ghost_office_empty_corridor/nm_ghost_office_empty_corridor.webp")))

    # --- nm_potion_hangover (-20 ... +5) ---
    sb_events["check_class"].add_event(Event(
        3,
        "nm_potion_hangover_miwa",
        TimeCondition(weekday="d", daytime="c"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_potion_hangover"),
        # The sensory fragment she almost catches through the gap (rerolls).
        RandomListSelector("memory_scrap", "someone laughing too close", "a warm hand on her shoulder", "a smell like cut flowers", "a song she can't place"),
        # Cross-band callback: did Emiko flag this girl to you on the phone?
        GameDataSelector("emiko_close", "nm_emiko_close", 0),
        # Establishing object beat (the one shut notebook in a room of open ones).
        Pattern("main", "images/events/new_management/nm_potion_hangover_miwa/nm_potion_hangover_miwa 1.webp")))
    office_building_work_event["counselling"].add_event(Event(
        3,
        "nm_potion_hangover_lily",
        TimeCondition(weekday="d", daytime="f"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_potion_hangover"),
        # What specifically rattled her (rerolls the confession).
        RandomListSelector("unnerved", "the girls keep flushing at nothing and can't say why", "there's a whole period she simply can't account for", "she found a note in her own handwriting she doesn't remember writing"),
        # A relationship-gated option (loop Emiko's records in) — different axis than
        # band 1's stat/standing gates — plus the guided companion line.
        GameDataSelector("emiko_close", "nm_emiko_close", 0),
        GameDataSelector("guided", "new_management_guided", 0),
        # Object beat: the trembling mug against the saucer.
        Pattern("main", "images/events/new_management/nm_potion_hangover_lily/nm_potion_hangover_lily 1.webp")))
    courtyard_events["search"].add_event(Event(
        3,
        "nm_potion_hangover_vial",
        OR(TimeCondition(daytime="f", weekday="d"), TimeCondition(daytime="d", weekday="w")),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_potion_hangover"),
        # Varies the find.
        RandomListSelector("residue_detail", "a thumbprint pressed into the sticky neck", "a strip of label, half-dissolved past reading", "a second vial too, crushed to green powder"),
        # The two classmates drifting through the greyed flashback corridor (space-separated pair).
        RandomListSelector("flash_pair", "ikushi_ito lin_kato", "lin_kato ishimaru_maki", "ishimaru_maki ikushi_ito"),
        # The find itself (scene image; solo investigation, no paperdoll).
        Pattern("main", "images/events/new_management/nm_potion_hangover_vial/nm_potion_hangover_vial 1.webp")))

    # --- nm_testing_the_waters (-5 ... +20) ---
    courtyard_events["patrol"].add_event(Event(
        3,
        "nm_testing_the_waters_clipboard",
        OR(TimeCondition(daytime="f", weekday="d"), TimeCondition(daytime="d", weekday="w")),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_testing_the_waters"),
        # Her headline grey-area question (rerolls). Charm gates the "turnaround".
        RandomListSelector("grey_area", "whether the weekend dress code still holds off campus", "if phones are really banned in free periods", "whether 'dating on campus' is a thing that's allowed now"),
        StatSelector("charm", CHARM, "school", [20, 100]),
        Pattern("main", "images/events/new_management/nm_testing_the_waters_clipboard/nm_testing_the_waters_clipboard 1.webp")))
    office_building_work_event["reputation"].add_event(Event(
        3,
        "nm_testing_the_waters_memo",
        TimeCondition(weekday="d", daytime="d"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_testing_the_waters"),
        GameDataSelector("guided", "new_management_guided", 0),
        # Object beat: the blank memo form squared to the blotter.
        Pattern("main", "images/events/new_management/nm_testing_the_waters_memo/nm_testing_the_waters_memo 1.webp")))

    # --- nm_rumors_in_bloom (0 ... +25) ---
    kiosk_events["get_snack"].add_event(Event(
        3,
        "nm_rumors_in_bloom_kiosk",
        OR(TimeCondition(weekday="d", daytime="1,3"), TimeCondition(weekday="w", daytime="4-")),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_rumors_in_bloom"),
        # Overheard intel on "listen"; a classmate voice; band-1 callbacks.
        RandomListSelector("rumor", "a parent who keeps ringing about the science wing", "two teachers who haven't spoken since the potion week", "someone's older brother swearing the place is cursed"),
        RandomListSelector("bystander", "ikushi_ito", "lin_kato", "ishimaru_maki"),
        GameDataSelector("snapped", "nm_snapped", 0),
        GameDataSelector("face_known", "nm_face_introduced", 0),
        Pattern("main", "images/events/new_management/nm_rumors_in_bloom_kiosk/nm_rumors_in_bloom_kiosk 1.webp")))
    courtyard_events["search"].add_event(Event(
        3,
        "nm_rumors_in_bloom_chalk",
        OR(TimeCondition(daytime="f", weekday="d"), TimeCondition(daytime="d", weekday="w")),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_rumors_in_bloom"),
        # How the portrait flatters him (rerolls). Solo image-led beat.
        RandomListSelector("exaggeration", "the jaw squared off like a statue's", "shoulders about three sizes too heroic", "a little crown, for some reason"),
        Pattern("main", "images/events/new_management/nm_rumors_in_bloom_chalk/nm_rumors_in_bloom_chalk 1.webp")))

    # --- nm_quiet_endorsements (+10 ... +30) ---
    sb_events["check_class"].add_event(Event(
        3,
        "nm_quiet_endorsements_after_bell",
        TimeCondition(weekday="d", daytime="c"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_quiet_endorsements"),
        # Payoff of the band-2 memory-gap beat; Zoe hallway tip under Guided.
        GameDataSelector("miwa_helped", "nm_miwa_helped", 0),
        GameDataSelector("guided", "new_management_guided", 0)))
    office_building_work_event["counselling"].add_event(Event(
        3,
        "nm_quiet_endorsements_second_coffee",
        TimeCondition(weekday="d", daytime="f"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_quiet_endorsements"),
        # Reacts to band-2 Lily; object beat bookends her rattling mug.
        GameDataSelector("lily_witnessed", "nm_lily_witnessed", 0),
        Pattern("main", "images/events/new_management/nm_quiet_endorsements_second_coffee/nm_quiet_endorsements_second_coffee 1.webp")))
    office_building_work_event["education"].add_event(Event(
        3,
        "nm_quiet_endorsements_curriculum",
        TimeCondition(weekday="d", daytime="d"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_quiet_endorsements"),
        # Object beat: your outline back with her one approving margin tick.
        Pattern("main", "images/events/new_management/nm_quiet_endorsements_curriculum/nm_quiet_endorsements_curriculum 1.webp")))

    # --- nm_welcome_committee (+22 ... +40) ---
    sb_events["teach_class"].add_event(Event(
        3,
        "nm_welcome_committee_mug",
        TimeCondition(weekday="d", daytime="c"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_welcome_committee"),
        # Bookends the band-1 corridor freeze-out.
        GameDataSelector("yulan_thawed", "nm_yulan_thawed", 0),
        Pattern("main", "images/events/new_management/nm_welcome_committee_mug/nm_welcome_committee_mug 1.webp")))
    office_building_events["look_around"].add_event(Event(
        3,
        "nm_welcome_committee_plaque",
        TimeCondition(weekday="d", daytime="f"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_welcome_committee"),
        # Bookends the nameplate; reacts to whether you claimed the door early.
        GameDataSelector("door_claimed", "nm_door_claimed", 0),
        GameDataSelector("guided", "new_management_guided", 0),
        Pattern("main", "images/events/new_management/nm_welcome_committee_plaque/nm_welcome_committee_plaque 1.webp")))
    courtyard_events["patrol"].add_event(Event(
        3,
        "nm_welcome_committee_assembly",
        TimeCondition(weekday="d", daytime="1"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_welcome_committee"),
        # Bookends the janitor beat: Yuriko helped (ally flag), Aona greets by title.
        GameDataSelector("yuriko_ally", "nm_yuriko_ally", 0),
        GameDataSelector("face_known", "nm_face_introduced", 0),
        Pattern("main", "images/events/new_management/nm_welcome_committee_assembly/nm_welcome_committee_assembly 1.webp")))


#######################################
# region Ghost Office ----------------- #
#######################################

# region SCENE · nm_ghost_office_nameplate ══════════════════════════════════════
#  At the door of the headmaster's office. The previous headmaster's name is still on
#  the brass plaque; a printout with the new headmaster's name — misspelled — is taped
#  crookedly over half of it. Emiko (the secretary) is there and they talk about it;
#  she mentions she ordered the proper plaque a week ago but it's stuck "in process."
#  Over the scene the taped printout can come off. The misspelling varies (<wrong_name>:
#  HEADMSTER / H. MASTAR / MR. HEADMAN / THE NEW GUY / MR. WHATSISNAME).
#
#  Wired: stepped door images via convert_pattern("main") (steps 0-3); Emiko paperdoll
#  over the blurred office/secretary background.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_ghost_office_nameplate (**kwargs):
    $ begin_event(**kwargs)

    $ wrong_name = get_value("wrong_name", **kwargs)
    $ plate_note = get_value("plate_note", **kwargs)
    # Read Standing through the gallery getter so replays have the value (Events guide §8/§16).
    $ standing = get_bar_value("new_management", "main", 0, **kwargs)

    # images/events/new_management/nm_ghost_office_nameplate/nm_ghost_office_nameplate <wrong_name> <step>.webp
    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)

    subtitles "The office door still carries the old headmaster's name, cut deep into the brass like it means to stay there."
    subtitles "Someone's taped a printout over half of it — your name, on printer paper, spelled {i}[wrong_name]{/i}. It's crooked, and one corner is already peeling loose."
    $ image.show(1)
    headmaster.think "Three weeks now, and I still catch myself slowing down at my own door. His name's the one cut deep into the brass. Mine's the strip of paper somebody taped up and couldn't even be bothered to keep straight."

    if standing <= -18:
        headmaster.think "I keep waiting for it to start feeling like mine. It doesn't. Most mornings I still feel like I'm covering a shift for a man who's coming back any day now to want his chair."

    # Emiko leans in → hand off to conversation (paperdoll over the blurred office).
    $ emiko.register_paperdoll()
    $ paperdoll_manager.set_background(image[1], blur = True, **kwargs)
    $ emiko.display(PDAImage(pose = "10", outfit = "uniform", level = 5, mood = "shining", mouth = "open"),
        PDAPreset("close_body_center", duration = 0.4)),
    emiko.say "Caught you glaring at it. Don't worry — everyone glares at it."
    $ emiko.display(PDAImage(pose = "34", mood = "neutral", mouth = "open"))
    emiko.say "I put in for the proper plaque a week ago. Every day since, it's been 'in process.' I'm starting to think that's just where brass goes to quietly die."

    # Stat-gated choice: a warmer, better option only unlocks once you've got some charm.
    # Read through the gallery getter so the value replays correctly (Events guide §8/§16).
    $ high_charm = get_stat_value("charm", [20, 100], **kwargs) >= 20

    $ emiko.display(PDAImage(mouth = "closed"), PDAMove(alignX = -0.2, duration = 1.0))
    $ call_custom_menu_with_text("What do you do with the nameplate?", character.subtitles, False,
        MenuElement("fix", "Tear it down and order the real thing", EventEffect("nm_ghost_office_nameplate.fix")),
        MenuElement("charm_fix", "Make a joke of it over coffee", EventEffect("nm_ghost_office_nameplate.charm_fix"), high_charm),
        MenuElement("leave_it", "Leave the printout for now", EventEffect("nm_ghost_office_nameplate.leave_it")),
        MenuElement("walk_away", "Walk away", EventEffect("nm_ghost_office_nameplate.walk_away")),
        menu_anchor = MENU_ANCHOR_MIDDLE_RIGHT,
    **kwargs)

label .fix (**kwargs):

    $ emiko.display(PDAMove(alignX = 0.5, duration = 1.0))
    headmaster "Then let's stop waiting on it. Chase the plaque today — and make sure they spell me right this time."
    $ emiko.display(PDAImage(pose = "2", mood = "shining", mouth = "open"))
    emiko.say "Finally. Consider it chased. And this—"
    $ image.show(2)
    emiko.say "—goes in the bin before it ends up on somebody's phone."
    $ paperdoll_manager.set_background(image[2], blur = True, **kwargs)
    $ emiko.display(PDAImage(pose = "6", mood = "happy", mouth = "closed"))
    headmaster.think "There. Torn down. It's a strip of paper in the bin, nothing — but it's my name they'll chase now, spelled right, instead of his that I keep flinching past every morning."

    $ set_game_data("nm_door_claimed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(reputation=TINY, charm=TINY) from _nm_go_np_fix
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .charm_fix (**kwargs):

    $ emiko.display(PDAMove(alignX = 0.5, duration = 1.0))
    headmaster "Put two names on that requisition. Mine — spelled correctly, in nice big letters — and whoever keeps typing 'in process.'"
    $ emiko.display(PDAImage(pose = "12", mood = "shining", mouth = "open"))
    emiko.say "Ha! I'll cc them a dictionary. Bold it, even."
    $ image.show(3)
    subtitles "She pours a second coffee without being asked and nudges the order form across the desk with one finger."
    headmaster.think "She poured that second cup without even looking, like she's done it a hundred times. When did that start? I don't know. But God, it's good to have one person in this building already standing in my corner before I've had to ask."

    $ set_game_data("nm_door_claimed", 1)
    $ set_game_data("nm_emiko_close", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=TINY, charm=SMALL, happiness=TINY) from _nm_go_np_charm
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .leave_it (**kwargs):

    $ emiko.display(PDAMove(alignX = 0.5, duration = 1.0))
    headmaster "Leave it for now. There are bigger fires than a nameplate."
    $ emiko.display(PDAImage(pose = "21", mood = "neutral", mouth = "open"))
    emiko.say "Mm. Your call. Just don't act surprised when the kids keep calling you the wrong thing — they read the door, not the memo."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster.think "I keep telling myself it's temporary. Emiko's right, though, isn't she — the kids don't read the memo, they read the door. And right now the door says I couldn't be bothered to put my own name on it."

    $ situation_manager.apply_progress_change("situation:new_management:main", 0)
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .walk_away (**kwargs):

    $ emiko.display(PDAMove(alignX = 0.5, duration = 1.0))
    subtitles "You turn back down the hall, leaving the tape exactly where it is."
    $ emiko.display(PDAImage(pose = "23", mood = "sad", mouth = "closed"))
    emiko.say "...Right. I'll keep chasing it on my own, then."
    headmaster.think "I should turn round. Say something. She's going to keep chasing that plaque on her own now because I couldn't be bothered to stop walking. God. If I won't even put my name on my own door, why would anyone in here trust me with the room behind it?"

    $ situation_manager.apply_progress_change("situation:new_management:main", -1)
    call change_stats_with_modifier(reputation=DEC_TINY) from _nm_go_np_walk
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

# endregion ═════════════════════════════════════════════════════════════════════

# region SCENE · nm_ghost_office_janitor ════════════════════════════════════════
#  Daytime in the school courtyard, by one of the paths. Aona (a 3rd-year student)
#  is standing with one classmate. The two of them are talking and glancing over at
#  the headmaster, who is a few steps away, and gossiping about him: Aona is sure he's
#  just the maintenance man, while the other girl thinks he might be the man who gave
#  the assembly speech. Neither of them realises he's the new headmaster. Light, sunny,
#  everyday — two students sizing up a stranger.
#
#  The classmate is picked at random each playthrough (ikushi_ito / lin_kato /
#  ishimaru_maki), so keep any drawing of her generic enough to fit any of them.
#
#  Currently wired: one optional full-screen image (1920×1080 .webp) via
#  show_pattern("main") at
#  images/events/new_management/nm_ghost_office_janitor/nm_ghost_office_janitor 1.webp.
#  The overheard gossip plays over that image (no paperdolls). Aona + classmate
#  paperdolls appear only in the branches where he speaks to them and they turn to
#  face him. Background: courtyard/1 0 1.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_ghost_office_janitor (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ aona = Person["aona_komuro"]
    $ ikushi = Person["ikushi_ito"]
    $ wrong_role = get_value("wrong_role", **kwargs)

    # images/events/new_management/nm_ghost_office_janitor/nm_ghost_office_janitor 1.webp
    $ image = convert_pattern("main", **kwargs)

    # OVERHEARD gossip: the two girls are talking to EACH OTHER about him — he's just
    # close enough to catch it. NO paperdolls here (paperdolls face the player, and
    # these two aren't talking to him); the scene image shows them, he watches.
    
    $ aona.register_paperdoll()
    $ ikushi.register_paperdoll()

    $ register_temp_preset("cbl", PDAMove(alignX = 0.0))
    $ register_temp_preset("cbr", PDAMove(alignX = 1.0))

    $ aona.display(PDAImage(outfit = "uniform", level = 1), PDAMove(alignX = -1.5, zoom = 2.0, alignY = -0.1, duration = 0.0))
    $ ikushi.display(PDAImage(outfit = "uniform", level = 1), PDAMove(alignX = 2.5, zoom = 2.0, alignY = -0.1, duration = 0.0))

    $ image.show(0)
    subtitles "By the courtyard path, Aona has an audience of exactly one classmate, and she is making the absolute most of it."
    aona.say "—so yeah, there's a new headmaster now. We sat through the whole speech in the gym, remember?"
    aona.say "But {i}that{/i} guy? Nah. That's [wrong_role]. Look at the way he walks — that is not a headmaster walk."

    $ image.show(1)
    ikushi.say "...you sure, though? He kinda looks like the one who gave the speech."
    aona.say "Trust me. That whole assembly was a total blur. Could've been anybody up on that stage."

    headmaster.think "There's a headmaster, they're sure of that much. They just haven't worked out he's the bloke standing close enough to hear every word. Three weeks in and I'm still a rumour to my own students."

    # Callback choice: only offered if you already claimed the office door.
    # Read through the gallery getter (paired with the GameDataSelector) so it replays.
    $ door_claimed = get_value("door_claimed", 0, **kwargs) == 1

    $ call_custom_menu_with_text("They're ranking you — three feet away.", character.subtitles, False,
        MenuElement("introduce", "Introduce yourself", EventEffect("nm_ghost_office_janitor.introduce")),
        MenuElement("door", "Send them to read the door", EventEffect("nm_ghost_office_janitor.door"), door_claimed),
        MenuElement("slip_past", "Slip past quietly", EventEffect("nm_ghost_office_janitor.slip_past")),
        MenuElement("snap", "Snap at them", EventEffect("nm_ghost_office_janitor.snap")),
    **kwargs)

label .introduce (**kwargs):
    $ paperdoll_manager.set_background(image[1], blur = True)
    headmaster "Good morning. For the record — headmaster. Not [wrong_role]."
    # He's spoken to them → they both turn to face him. Now it's a player-facing
    # exchange, so paperdolls fit.
    $ aona.display(PDAImage(pose = "7", mood = "suprised", mouth = "open"), PDAMove(alignX = 0.0, duration = 1.0))
    $ ikushi.display(PDAImage(pose = "1", mood = "neutral", mouth = "closed"), PDAFlip(True), PDAMove(alignX = 1.0, duration = 1.0))
    aona.say "..."
    aona.say "Oh my— you're real. You're an actual person."
    $ aona.display(PDAImage(mood = "sad", mouth = "closed"))
    $ ikushi.display(PDAImage(pose = "8", mood = "shining"))
    subtitles "Ikushi turns a laugh into a cough. Aona's ears go bright pink and she suddenly finds her own shoes fascinating."
    headmaster.think "Poor kid's ears are on fire. She'll be telling this one at lunch for a week — the day she called the headmaster a maintenance man to his face. Let her. If it's the story that finally sticks my face to the title, she can tell it as often as she likes."

    $ set_game_data("nm_face_introduced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY, happiness=TINY) from _nm_go_jan_intro
    $ end_event('new_daytime', **kwargs)

label .door (**kwargs):
    $ paperdoll_manager.set_background(image[1], blur = True)
    
    $ aona.display(PDAImage(pose = "7", mood = "suspicious"), PDAMove(alignX = 0.0, duration = 1.0))
    $ ikushi.display(PDAImage(pose = "7", mood = "suprised"), PDAFlip(True), PDAMove(alignX = 1.0, duration = 1.0))
    headmaster "Corner office, end of that corridor. Go read the door, then come back and tell me who I am. I'll wait."
    
    $ ikushi.display(
        PDAFlip(False, 0.2),
        PDAPause(0.2),
        PDAMove(alignX = 2.5, duration = 1.0),
        PDAPause(1.0)
    )
    $ aona.display(
        PDAImage(pose = "23", mood = "sad", mouth = "closed"),
        PDAPause(1.0),
        PDAImage(mood = "happy"),
        PDAPause(1.0),
        PDAImage(mood="sad"),
        PDAPause(1.0)
    )
    $ ikushi.display(
        PDAFlip(True),
        PDAImage(mood = "sad"),
        PDAMove(alignX = 1.0, duration = 1.0)
    )
    subtitles "Her friend actually takes the dare and jogs off. She comes back a few shades paler and a great deal quieter."
    $ ikushi.display(PDAImage(mouth = "open"))
    ikushi.say "...it's got your name on it. Spelled right and everything. Sorry, headmaster."
    headmaster.think "Ha. Didn't have to argue a single point. Sent her to read the door and she came back three shades paler than she left. Turns out the brass makes my case better than I ever could standing here."

    $ set_game_data("nm_face_introduced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY) from _nm_go_jan_door
    $ end_event('new_daytime', **kwargs)

label .slip_past (**kwargs):
    # No paperdoll — he keeps walking; they're behind him, not facing him.
    $ image.show(2)
    subtitles "You keep walking, unhurried. Their voices thin out behind you, still arguing about who you are."
    headmaster.think "No sense making a thing of it. They'll see me tomorrow, and the day after, and the one after that. It sinks in eventually. ...It has to. I don't have a faster way than just turning up until they can't not know me."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _nm_go_jan_slip
    $ end_event('new_daytime', **kwargs)

label .snap (**kwargs):
    $ image.show(3)
    headmaster "If you've got time to hand out jobs I don't have, you've got time to be in class."
    $ paperdoll_manager.set_background(image[3], blur = True)
    $ aona.display(PDAImage(pose = "1", mood = "sad", mouth = "open"),
        PDAPreset("close_body_left", duration = 0.0))
    $ ikushi.display(PDAImage(pose = "23", mood = "sad", mouth = "closed"), PDAFlip(True),
        PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 1.0))
    aona.say "We— we weren't— sorry."
    headmaster.think "That shut them up. Look at them — gone stiff, staring at their shoes, just waiting for me to be done and gone. That's not respect on their faces. That's wanting me to leave. Damn it. That is not what I came over here for."

    $ set_game_data("nm_snapped", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", -2)
    call change_stats_with_modifier(happiness=DEC_SMALL, reputation=DEC_TINY) from _nm_go_jan_snap
    $ aona.clear_display()
    $ end_event('new_daytime', **kwargs)

# endregion ═════════════════════════════════════════════════════════════════════

# region SCENE · nm_ghost_office_private_line ═══════════════════════════════════
#  A phone call: the headmaster rings Emiko from the office line, so the two of them
#  are in different rooms. She answers warmly — too warmly, caught off guard — then
#  turns crisp and professional the instant footsteps pass in her outer office. She's
#  at her desk. The item on top of the stack of messages she's holding back varies
#  (<loud_slip>).
#
#  Wired: split-screen background (his side left, her side right) — both halves
#  currently the same office bg, the left half in black & white; Emiko paperdoll on
#  the right (colour) side.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_ghost_office_private_line (**kwargs):
    $ begin_event(**kwargs)

    $ loud_slip = get_value("loud_slip", **kwargs)
    $ standing = get_bar_value("new_management", "main", 0, **kwargs)

    $ paperdoll_manager.set_background("images/background/office building/c teacher.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "35", outfit = "uniform", level = 5), PDAPreset("upper_body"), PDAMove(alignX = -1.5, alignY = -0.3, duration = 0.0))

    subtitles "You dial Emiko from the office line."
    $ emiko.display(PDAImage(mood = "shining", mouth = "open"), PDAMove(alignX = 0.5, duration = 1.0))
    emiko.say "Well. Look who remembers he has a phone."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster.think "God, that voice. Warm, easy, a little teasing — the one she keeps for when there's nobody in the outer office to overhear it. I don't think she even knows she's got two."
    subtitles "Footsteps cross the outer office. Between one breath and the next, her voice buttons itself all the way up."
    $ emiko.display(PDAImage(mood = "neutral", mouth = "open"))
    emiko.say "—and how can I help you today, headmaster?"

    if get_value("door_claimed", 0, **kwargs) == 1:
        $ emiko.display(PDAImage(mood = "happy", mouth = "closed"))
        emiko.say "Oh — and your plaque's finally moving, for what it's worth. The door should know your name by Friday."

    if get_value("guided", 0, **kwargs) == 1:
        $ emiko.display(PDAImage(mood = "neutral", mouth = "open"))
        emiko.say "You know, the last one walked the courtyard every morning. Rain or shine. ...Just putting that out there."

    # Gated choice: when you're near the floor, she'll drop the mask if you ask straight.
    $ deep_hole = True #standing <= -18

    $ emiko.display(PDAImage(mouth = "closed"))
    $ call_custom_menu_with_text("How do you use the call?", character.subtitles, False,
        MenuElement("triage", "Ask what needs you today", EventEffect("nm_ghost_office_private_line.triage")),
        MenuElement("honest", "Ask, off the record, how bad it is", EventEffect("nm_ghost_office_private_line.honest"), deep_hole),
        MenuElement("short", "Keep it brief", EventEffect("nm_ghost_office_private_line.short")),
        MenuElement("distant", "Keep it distant", EventEffect("nm_ghost_office_private_line.distant")),
    **kwargs)

label .triage (**kwargs):
    headmaster "Give me whatever can't wait. Parent calls, complaints, anything that's actually on fire."
    $ emiko.display(PDAImage(mood = "neutral", mouth = "open"))
    emiko.say "Three parents, one teacher with a grievance, and [loud_slip] sitting right on top like it pays rent."
    $ emiko.display(PDAImage(mood = "happy"))
    emiko.say "I'll sort them and line them up. You just decide who's worth showing your face to."
    headmaster.think "She's been carrying half of this herself and never once mentioned it. Least I can do is turn up for the other half. And they do notice the second I walk in — I keep forgetting that showing up is most of the job."

    $ set_game_data("nm_emiko_close", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, education=TINY) from _nm_go_pl_triage
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .honest (**kwargs):
    headmaster "Emiko. No routing, no softening it. How bad is it, really?"
    subtitles "A pause. When she answers, her voice has dropped low enough that the outer office won't catch a word of it."
    $ emiko.display(PDAImage(mood = "sad", mouth = "open"))
    emiko.say "Bad enough that I've stopped tucking the slips where you won't see them. And [loud_slip]? That one's new. I don't like it."
    emiko.say "It's fixable. But it gets fixed by them {i}seeing{/i} you — not by me quietly plugging the holes. So go do that. Be seen. Please."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster.think "She said please. Emiko. She actually said please, and I sat here and made her spell the whole thing out first. ...She's right, though. She's always right about this. Fine — the second we hang up, I go."

    $ set_game_data("nm_emiko_close", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL, happiness=TINY) from _nm_go_pl_honest
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .short (**kwargs):
    headmaster "Anything urgent this morning?"
    $ emiko.display(PDAImage(mood = "happy", mouth = "open"))
    emiko.say "Nothing that won't keep till the afternoon."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "Good. Thanks."
    $ emiko.display(PDAImage(mood = "neutral"))
    emiko.say "..."
    $ emiko.display(PDAImage(mouth = "open"))
    emiko.say "Of course. Anytime."
    $ emiko.display(PDAImage(mouth = "closed"), PDAMove(alignX = -1.5, duration = 1.0))
    headmaster.think "And that's that. ...There was a gap at the end there, wasn't there — that little pause where she wanted to say something more. And I filled it with 'good, thanks' and hung up. Didn't even hear it until just now."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _nm_go_pl_short
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .distant (**kwargs):
    headmaster "Just making sure the line's working. That's all."
    $ emiko.display(PDAImage(mood = "sad", mouth = "open"))
    emiko.say "...It's working. Line's fine."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster.think "She reached out and I gave her the phone company. 'Making sure the line works.' God. She's sitting at that desk right now feeling stupid for picking up warm, and I'm the one who did that to her."

    $ situation_manager.apply_progress_change("situation:new_management:main", 0)
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

# endregion ═════════════════════════════════════════════════════════════════════

# region SCENE · nm_ghost_office_empty_corridor ═════════════════════════════════
#  Just after the bell, a school corridor emptying of students. Yulan Chen (a teacher)
#  walks through reading from an open folder. The headmaster greets her; she doesn't
#  look up and keeps reading. What she's buried in varies (<folder_topic>).
#
#  Wired: one image via show_pattern("main"); Yulan paperdoll over the blurred
#  school-building corridor background.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_ghost_office_empty_corridor (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ yulan = Person["yulan_chen"]
    $ folder_topic = get_value("folder_topic", **kwargs)
    $ face_known = get_value("face_known", 0, **kwargs) == 1

    # Establishing beat: the emptying hallway, Yulan mid-stride not looking up → scene image.
    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ show_pattern("main", **kwargs)
    subtitles "The bell has just finished ringing. The corridor empties in pieces."
    subtitles "Yulan Chen walks with [folder_topic] open, reading as she moves."

    # Hand off to the exchange (paperdoll over the blurred hallway).
    $ yulan.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/school building/f.webp", blur = True)
    $ yulan.display(PDAImage(pose = "39", look = "avert"),
        PDAPreset("outside", duration = 0.0))
    $ yulan.display(PDAMove(alignX = 0.0, duration = 1.0))
    headmaster "Ms. Chen."
    $ yulan.display(PDAMove(alignX = 0.2, duration = 1.0))
    yulan.say "..."
    $ yulan.display(PDAMove(alignX = 0.4, duration = 1.0))
    subtitles "She doesn't look up. A page turns, unhurried, as if your greeting had been delivered to the wrong desk."

    if face_known:
        $ yulan.display(PDAImage(mood = "neutral", mouth = "open"))
        yulan.say "...Headmaster."
        subtitles "One word — but she said it. The students have started using your name in class, apparently, and things like that climb the stairs eventually."
        headmaster.think "She used my name. It made it all the way from the courtyard up to the staff corridor without me carrying it a single step. Small thing. But it means the thing's spreading on its own now, and that's new."
    else:
        headmaster.think "...Right. Loud and clear. Learning her name in a corridor doesn't buy me anything with her — she wants the work to be good, and the manners are just noise. Fair enough."

    # Gated choice: a genuinely informed note lands harder — but only if you can give one.
    # Read through the gallery getter so the value replays correctly (Events guide §8/§16).
    $ can_talk_shop = get_stat_value("education", [20, 100], **kwargs) >= 20
    $ shop_title = "Weigh in on " + folder_topic

    $ call_custom_menu_with_text("Yulan kept walking.", character.subtitles, False,
        MenuElement("acknowledge", "Acknowledge her work", EventEffect("nm_ghost_office_empty_corridor.acknowledge")),
        MenuElement("shop", shop_title, EventEffect("nm_ghost_office_empty_corridor.shop"), can_talk_shop),
        MenuElement("greet", "Greet her and keep moving", EventEffect("nm_ghost_office_empty_corridor.greet")),
        MenuElement("force", "Stride past her", EventEffect("nm_ghost_office_empty_corridor.force")),
    **kwargs)

label .acknowledge (**kwargs):
    $ yulan = Person["yulan_chen"]
    $ folder_topic = get_value("folder_topic", **kwargs)

    $ yulan.display(PDAMove(zoom = 2.0, alignX = 0.6, duration = 1.0))
    headmaster "Your work on [folder_topic] — the revisions were solid. Genuinely."
    yulan.say "..."
    $ yulan.display(PDAImage(mood = "neutral", mouth = "open"))
    yulan.say "...Thank you."
    $ yulan.display(PDAImage(mouth = "closed"))
    subtitles "Still no eye contact. But the next page turns a little slower than the last one did."
    $ yulan.display(PDAMove(alignX = 1.0, duration = 1.0))
    headmaster.think "Was that— yeah. That page turned slower than the last one. It's nothing, really, it's a page turning. But from her that's the first inch of ground she's given me, and I'll take an inch."

    $ set_game_data("nm_yulan_thawed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(education=TINY, reputation=TINY) from _nm_go_cor_ack
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

label .shop (**kwargs):
    $ yulan = Person["yulan_chen"]
    $ folder_topic = get_value("folder_topic", **kwargs)

    $ yulan.display(PDAImage(pose = "7"), PDAMove(zoom = 2.0, alignX = 0.5, duration = 1.0))
    headmaster "On [folder_topic] — your second section is doing the real work. I'd put it {i}before{/i} the summary, not after. Let the argument land before you tell them what it was."
    subtitles "For the first time, she stops walking. She looks — actually looks — at the page you mean."
    $ yulan.display(PDAImage(pose = "8", mood = "suprised", mouth = "open", look = "follow"))
    yulan.say "...That is the exact note I'd have made. I simply didn't expect you to have read closely enough to make it."
    $ yulan.display(PDAImage(mood = "happy", mouth = "closed"))
    headmaster.think "There it is — she actually looked at me. Try to charm her and it slides straight off; talk about the real work, and know it as well as she does, and she stops walking. So that's how you get to Yulan. Good to know."

    $ set_game_data("nm_yulan_thawed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=SMALL, reputation=TINY) from _nm_go_cor_shop
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

label .greet (**kwargs):
    $ yulan = Person["yulan_chen"]

    $ yulan.display(PDAMove(alignX = 0.6, duration = 1.0))
    headmaster "Good afternoon, Ms. Chen."
    $ yulan.display(PDAImage(mood = "neutral", mouth = "open"), PDAMove(alignX = 0.8, duration = 1.0))
    yulan.say "Headmaster."
    $ yulan.display(PDAImage(mouth = "closed"), PDAMove(alignX = 1.5, duration = 1.0))
    headmaster.think "One word, flat as the floor, not a scrap of warmth on it. Still — it's a word. Last week I'd have got a turned page and nothing else, so I'll count it."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

label .force (**kwargs):
    $ yulan = Person["yulan_chen"]

    $ yulan.display(PDAMove(alignX = 0.6, duration = 1.0))
    subtitles "You lengthen your stride and go straight past her. Behind you, a folder snaps shut like a small, final verdict."
    $ yulan.display(PDAImage(mood = "angry", mouth = "closed"), PDAMove(alignX = 0.8, duration = 1.0))
    headmaster.think "...I just walked straight past her like she was a coat rack. And that folder snapping shut behind me — that's her filing it away somewhere she won't lose it. Ten seconds, and I've probably set myself back a month with her."

    $ situation_manager.apply_progress_change("situation:new_management:main", -1)
    call change_stats_with_modifier(reputation=DEC_TINY, happiness=DEC_TINY) from _nm_go_cor_force
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

# region ════════════════════════════════════════════════════════════════════════

# endregion
#######################################


#######################################
# region Potion Hangover -------------- #
#######################################

# ═══ SCENE · nm_potion_hangover_miwa ══════════════════════════════════════════
#  A 3rd-year classroom, mid-lesson. Everyone is working with their notebooks open
#  except Miwa, who sits apart with hers shut. The headmaster checks on her; she can't
#  remember Tuesday morning at all — a blank where the week should be. When she tries
#  to reach for it she briefly goes absent, staring at nothing, then comes back. The
#  sensory scrap she almost catches varies (<memory_scrap>).
#
#  Wired: one image via show_pattern("main") (no art yet → blurred classroom bg);
#  Miwa paperdoll at close_body. She starts eyes-down over the notebook (pose 12),
#  flinches when addressed, and for the blank-out the frame creeps in to upper_body
#  while she drains to greyscale and softens; she snaps back with a jolt into a
#  self-hug (13) and braces (23) for the menu.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_potion_hangover_miwa (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ miwa = Person["miwa_igarashi"]
    $ memory_scrap = get_value("memory_scrap", **kwargs)
    $ emiko_close = get_value("emiko_close", 0, **kwargs) == 1

    # Establishing object beat: a room of open notebooks, and the one that isn't.
    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "3A is deep in a lesson — heads down, pens moving, the ordinary hum of a room that remembers what day it is."
    subtitles "Every notebook on the row is open. Miwa's lies shut under her folded hands, like she's holding it closed on purpose."

    if emiko_close:
        headmaster.think "Emiko rang about this one. 'The Igarashi girl — keep half an eye on her.' She never says that about the loud ones."

    # She hasn't noticed him: hands pinned over the shut notebook, eyes down and away.
    # Placed directly, no slide — she's withdrawn, not arriving.
    $ miwa.register_paperdoll()
    $ miwa.display(PDAImage(pose = "12", outfit = "uniform", level = 1, mood = "sad", mouth = "closed", look = "avert"),
        PDAPreset("close_body_center", duration = 0.0))
    headmaster "Miwa. You still with us?"
    # A small flinch, then she looks up at him.
    $ miwa.display(PDAShake(duration = 0.3, max_distance = 6), PDAPause(0.3),
        PDAImage(mouth = "open", look = "follow"))
    miwa.say "...I can't remember Tuesday morning. Any of it."
    $ miwa.display(PDAImage(pose = "14", look = "avert"))
    miwa.say "Everyone keeps saying 'last week' like it's normal, and I just— there's a blank where the whole week's supposed to be."

    $ miwa.display(PDAImage(mouth = "closed", look = "follow"))
    headmaster "Okay. Don't force it. Just the edges — what's the last thing that's actually {i}there{/i}?"
    # The reach: she thinks, then drifts out of the room — the frame creeps in,
    # the colour drains, the edges go soft.
    $ miwa.display(PDAImage(pose = "7", mood = "neutral", look = "avert"),
        PDAPreset("upper_body_center", duration = 1.2), PDAPause(1.2),
        PDABw(True, duration = 0.8), PDAPause(0.8),
        PDABlur(3.0, duration = 0.6))
    subtitles "For a moment she isn't in the room at all. Her eyes go somewhere the rest of her can't follow."
    subtitles "Something surfaces — [memory_scrap] — and then the grey closes back over it before she can hold on."
    # Back with a jolt: colour and focus snap in, frame pulls back, arms close round herself.
    $ miwa.display(PDABlur(0.0), PDABw(False),
        PDAImage(pose = "13", mood = "sad", mouth = "open", look = "follow"),
        PDAPreset("close_body_center"),
        PDAShake(duration = 0.25, max_distance = 8))
    miwa.say "...sorry. It's like the morning just isn't {i}in{/i} me anymore."

    $ miwa.display(PDAImage(mouth = "closed", look = "avert"))
    headmaster.think "Same blank as the day the whole wing went strange. That was weeks ago."
    headmaster.think "...Weeks. And nobody's asked her if she's alright? Not one of us?"

    # Braced for the verdict.
    $ miwa.display(PDAImage(pose = "23", look = "follow"))
    $ call_custom_menu_with_text("Miwa is holding very still, braced to be told she's broken.", character.subtitles, False,
        MenuElement("counsel", "Tell her she isn't broken", EventEffect("nm_potion_hangover_miwa.counsel")),
        MenuElement("structure", "Give her one small thing to do", EventEffect("nm_potion_hangover_miwa.structure")),
        MenuElement("press", "Push her to remember", EventEffect("nm_potion_hangover_miwa.press")),
    **kwargs)

label .counsel (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    headmaster "Listen to me. You're not broken, and you're not in trouble. Something scrambled that morning for a lot of people — you're just the only one honest enough to say the page came back blank."
    $ miwa.display(PDAImage(pose = "20", mood = "suprised", mouth = "open"))
    miwa.say "...I'm not the only one?"
    $ miwa.display(PDAImage(pose = "12", mood = "neutral", mouth = "closed"))
    headmaster "Not even close. Come by the office whenever you're ready — no quiz, no notes. A chair, and someone who takes it seriously."
    $ miwa.display(PDAImage(pose = "1", mood = "happy", mouth = "open", look = "avert"))
    miwa.say "Okay. ...Okay."
    $ miwa.display(PDAImage(look = "follow"))
    miwa.say "Thank you."
    # She stops standing guard: hands loosen, eyes drop to the page, the frame eases back.
    $ miwa.display(PDAImage(pose = "12", mouth = "closed", look = "avert"),
        PDAMove(zoom = "-0.2", duration = 0.8))
    subtitles "She opens the notebook at last. The page is still empty — but she stops standing guard over it."

    $ set_game_data("nm_miwa_helped", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(happiness=SMALL, reputation=TINY) from _nm_ph_miwa_counsel
    $ end_event('new_daytime', **kwargs)

label .structure (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    headmaster "Here's the whole assignment. Write down what you {i}do{/i} have — even if it starts at lunch. We'll look at it together after class. Tuesday can stay lost for today."
    $ miwa.display(PDAImage(pose = "7", mood = "neutral", mouth = "open"))
    miwa.say "Just... the parts that are there? And check later?"
    $ miwa.display(PDAImage(mouth = "closed"))
    headmaster "Just the parts that are there. That's it."
    # Eyes down to the page, hands busy with the pen.
    $ miwa.display(PDAImage(pose = "12", look = "avert"))
    subtitles "She uncaps a pen. It isn't much — but it's the first thing all day with edges she can actually hold onto."

    $ set_game_data("nm_miwa_helped", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(happiness=TINY, education=TINY) from _nm_ph_miwa_structure
    $ end_event('new_daytime', **kwargs)

label .press (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    headmaster "Try harder, Miwa. Something has to be in there — a smell, a voice, anything. Concentrate."
    $ miwa.display(PDAImage(pose = "13", mood = "sad", mouth = "open"),
        PDAShake(duration = 0.3, max_distance = 6))
    miwa.say "I {i}am{/i} — I told you, I can't—"
    # The door shuts: arms locked across herself, eyes away, the light goes out of her.
    $ miwa.display(PDAImage(pose = "16", mood = "angry", mouth = "closed", look = "avert"),
        PDAColor("black:0.25", duration = 0.6))
    subtitles "Her hands close over the notebook again. Whatever door had cracked open just quietly latched shut."
    headmaster.think "...She's shut. Completely. There's nothing down there for her to find, and I just stood over her demanding she find it."

    $ situation_manager.apply_progress_change("situation:new_management:main", -2)
    call change_stats_with_modifier(happiness=DEC_MEDIUM, reputation=DEC_TINY) from _nm_ph_miwa_press
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_potion_hangover_lily ══════════════════════════════════════════
#  The counselling office. Lily Anderson (a teacher) turns up without an appointment,
#  hovering in the doorway, apologetic and half-ready to leave. She sits; when she sets
#  her coffee mug down it rattles once against the saucer. Shaken, she asks the
#  headmaster if last week was real. What specifically unnerved her varies (<unnerved>).
#
#  Wired: one image via show_pattern("main"); Lily paperdoll over the blurred
#  teacher-office background. She starts at the door turned away (flipped walking
#  pose), turns back and comes in; the mug rattle is a small shake; she asks with a
#  half-covered hunch (14), then leans in for "You." (38); a long fine tremble under
#  "she's actually shaking". Leans in for the folder in .loop_in; relaxes back (zoom
#  out) in .sit; walks back out in .deflect before his closing thoughts.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_potion_hangover_lily (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ lily = Person["lily_anderson"]
    $ unnerved = get_value("unnerved", **kwargs)
    $ emiko_close = get_value("emiko_close", 0, **kwargs) == 1

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/teacher 1 1 0.webp", blur = True)
    subtitles "A knock — too soft to be official. Lily Anderson is already half-turned back toward the corridor by the time you look up."
    # She's at the door, already half-leaving: walking pose, turned away, eyes on the corridor.
    $ lily.register_paperdoll()
    $ lily.display(PDAImage(pose = "39", outfit = "uniform", level = 1, mood = "sad", mouth = "closed", look = "avert"),
        PDAPreset("close_body", duration = 0.0),
        PDAMove(alignX = 0.1, duration = 0.0),
        PDAFlip(True))
    # ...then she turns back, caught.
    $ lily.display(PDAFlip(False, duration = 0.3), PDAPause(0.3),
        PDAImage(pose = "12", mouth = "open", look = "follow"))
    lily.say "I— sorry. This is silly, you're busy, I shouldn't have—"
    $ lily.display(PDAImage(mouth = "closed"))
    headmaster "Ms. Anderson. Sit. The coffee's already poured."
    $ lily.display(PDAImage(pose = "1"), PDAMove(alignX = 0.5, duration = 0.8), PDAPause(0.8))

    # The tell. (Object-beat art slot; until it exists, the rattle plays on her.)
    $ show_pattern("main", **kwargs)
    $ lily.display(PDAImage(pose = "12", look = "avert"), PDAShake(duration = 0.2, max_distance = 4))
    subtitles "She sits. When she sets her mug down it rattles once against the saucer — a small, betraying sound she pretends not to hear."
    $ paperdoll_manager.set_background("images/background/office building/teacher 1 1 0.webp", blur = True)
    $ lily.display(PDAImage(pose = "14", mood = "sad", mouth = "open", look = "avert"))
    lily.say "Was last week... {i}real{/i}? I keep teaching like nothing happened, and [unnerved], and I—"
    # The actual ask — she leans in, hands open, eyes on him.
    $ lily.display(PDAImage(pose = "38", look = "follow"))
    lily.say "I don't want a diagnosis. I want one sane person to say it out loud with me so I know I haven't come unstitched. Not the staffroom. Not gossip. You."
    $ lily.display(PDAImage(pose = "12", mouth = "closed"),
        PDAShake(duration = 1.2, max_distance = 3))

    headmaster.think "God, she's actually shaking."
    headmaster.think "...Just say it straight. Don't make it any stranger for her than it already is."

    if get_value("guided", 0, **kwargs) == 1:
        $ lily.display(PDAImage(pose = "21", mood = "neutral", mouth = "open"))
        lily.say "The girls settle the instant someone actually looks {i}at{/i} them instead of past them. I've been meaning to say."

    # Both hands around the mug.
    $ lily.display(PDAImage(pose = "12", mood = "sad", mouth = "closed"))
    $ call_custom_menu_with_text("Lily has both hands around the mug now, waiting.", character.subtitles, False,
        MenuElement("sit", "Say it out loud with her", EventEffect("nm_potion_hangover_lily.sit")),
        MenuElement("loop_in", "Put Emiko's record in her hands", EventEffect("nm_potion_hangover_lily.loop_in"), emiko_close),
        MenuElement("maybe", "Offer a careful maybe", EventEffect("nm_potion_hangover_lily.maybe")),
        MenuElement("deflect", "Wave it off — blame the coffee", EventEffect("nm_potion_hangover_lily.deflect")),
    **kwargs)

label .sit (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "Then here it is, out loud: something happened last week. You're not imagining it, and you're not fragile for being the one who noticed."
    $ lily.display(PDAImage(pose = "20", mood = "suprised", mouth = "closed"))
    lily.say "..."
    $ lily.display(PDAImage(pose = "31", mood = "happy", mouth = "open"))
    lily.say "Thank you. God — that's all it— I can go back to third period now. I actually think I can."
    $ lily.display(PDAImage(pose = "1", mouth = "closed"))
    subtitles "The mug doesn't rattle when she lifts it this time. She just looks tired, and a great deal lighter for it."
    headmaster.think "That was all she needed. Somebody else saying yes, it happened."
    # Shoulders down: the frame eases back with her.
    $ lily.display(PDAMove(zoom = "-0.2", duration = 0.8))
    headmaster.think "Her shoulders just came down about an inch."

    $ set_game_data("nm_lily_witnessed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(happiness=MEDIUM, reputation=SMALL) from _nm_ph_lily_sit
    $ end_event('new_daytime', **kwargs)

label .loop_in (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "You're not imagining it — and you don't have to take just my word for it, either."
    # She leans in to take the folder, then straightens with it.
    $ lily.display(PDAImage(pose = "38", mood = "suprised", mouth = "closed", look = "avert"),
        PDAMove(zoom = 2.3, alignY = -0.15, duration = 0.5), PDAPause(0.5))
    subtitles "You slide a thin folder across: Emiko's quiet log of the week nobody will discuss. Dates. A line about the smell. Corroboration, in a second person's handwriting."
    $ lily.display(PDAImage(mouth = "open"))
    lily.say "...so it {i}is{/i} written down. Somewhere real. I'm not the only one who thought to."
    $ lily.display(PDAImage(pose = "31", mood = "happy", look = "follow"),
        PDAPreset("close_body", duration = 0.5))
    lily.say "That helps more than you know. Thank you — both of you."
    $ lily.display(PDAImage(mouth = "closed"))
    headmaster.think "Emiko won't mind. Not for this."
    headmaster.think "Dates, in somebody else's handwriting. She can hold onto that a lot longer than she could hold onto me saying so."

    $ set_game_data("nm_lily_witnessed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(happiness=MEDIUM, reputation=SMALL, education=TINY) from _nm_ph_lily_loop
    $ end_event('new_daytime', **kwargs)

label .maybe (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "Maybe it was real. Maybe your body's still catching up on something. I won't pretend to know which — but come back Thursday, same time, and we'll keep a proper eye on it together."
    $ lily.display(PDAImage(pose = "7", mood = "neutral", mouth = "open", look = "avert"))
    lily.say "Thursday. All right."
    # She takes hold of the date like a handrail.
    $ lily.display(PDAImage(pose = "12", look = "follow"))
    lily.say "That's... something to hold onto, at least."
    $ lily.display(PDAImage(mouth = "closed"))
    headmaster.think "That's not much of an answer, and we both know it."
    headmaster.think "...But it's a day on the calendar. Maybe that gets her as far as Thursday."

    $ set_game_data("nm_lily_witnessed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(happiness=SMALL) from _nm_ph_lily_maybe
    $ end_event('new_daytime', **kwargs)

label .deflect (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "Ah — stress does funny things to all of us. Honestly, it's probably just the coffee."
    $ lily.display(PDAImage(pose = "23", mood = "sad", mouth = "open", look = "avert"))
    lily.say "...Right. Of course. The coffee."
    $ lily.display(PDAImage(pose = "12", mouth = "closed"))
    subtitles "She picks the mug back up. It's steady now — but only because she's holding it too tightly to let it shake."
    # She leaves the way she came in: turns away and is out the door — his thoughts land on the empty doorway.
    $ lily.display(PDAImage(pose = "39"), PDAFlip(True, duration = 0.3), PDAPause(0.3),
        PDAMove(alignX = -1.5, duration = 1.2), PDAPause(1.2))
    headmaster.think "...Why did I say that? She worked up the nerve all morning to ask me one honest question, and I made a joke about coffee."
    headmaster.think "She won't be back. Would I be?"

    $ situation_manager.apply_progress_change("situation:new_management:main", 0)
    call change_stats_with_modifier(happiness=DEC_SMALL) from _nm_ph_lily_deflect
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_potion_hangover_vial ══════════════════════════════════════════
#  The courtyard, behind the bike rack. Alone, the headmaster finds a broken green
#  vial, still sticky at the neck. Its detail varies (<residue_detail>). The sweet
#  smell off it throws him into a brief flashback of the same smell in a school
#  corridor last Tuesday, students moving oddly — then he's back at the bike rack. If
#  he bags it and phones Emiko, it cuts briefly to her at her desk.
#
#  Wired: one image via show_pattern("main"); the flashback is an existing corridor
#  background shown in greyscale, with two classmates (<flash_pair>) drifting through
#  it as greyed, blurred paperdolls — one stalls mid-step and stares, one trails too
#  slowly behind. On "bag", Emiko on the phone (pose 35) slides in over the office bg
#  and back out when she hangs up.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_potion_hangover_vial (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ residue_detail = get_value("residue_detail", **kwargs)
    $ flash_a, flash_b = [Person[name] for name in get_value("flash_pair", **kwargs).split()]

    # The find — object beat, scene image, no one else out here.
    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "Behind the bike rack, something small catches the light: a broken vial, green glass gone cloudy, the neck still sticky where it snapped clean off."
    subtitles "You crouch. Up close there's [residue_detail]."
    headmaster.think "...So it never actually stopped. It just went quiet."

    # The smell triggers the flashback — existing corridor bg, blurred and drained.
    subtitles "Then the smell reaches you — sweet, cloying, sitting at the back of the throat — and all at once you aren't behind the bike rack at all."
    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True, bw = True)
    # Memory figures: greyed and soft like the corridor, parked off-screen at register
    # (config) so nothing flashes at the default position. One near, one further back.
    $ flash_a.register_paperdoll(blur = 4.0, config = {"alignX": -1.5, "bw": True, "blur": 4.0})
    $ flash_b.register_paperdoll(blur = 5.0, behind = True, config = {"alignX": 2.5, "bw": True, "blur": 5.0})
    $ flash_a.display(PDAImage(pose = "39", mood = "neutral", mouth = "closed", look = "avert"),
        PDAMove(alignY = -0.1, zoom = 2.0))
    $ flash_b.display(PDAImage(pose = "39", mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAMove(alignY = 0.05, zoom = 1.5))
    # Near one walks in and stops short; far one drifts the other way, too slow.
    $ flash_a.display(PDAMove(alignX = 0.3, duration = 2.0))
    $ flash_b.display(PDAMove(alignX = 0.65, duration = 3.5))
    subtitles "{i}Last Tuesday. That same corridor-sweetness hanging in the air. A whole wing of students moving a half-second out of step with themselves, and not one of them able to say why.{/i}"
    # Stalled mid-step, she turns her head and looks straight through you.
    $ flash_a.display(PDAImage(look = "follow"))
    headmaster.think "That smell. It's the same one. Exactly the same."
    # ...and walks on as if nothing happened. The other keeps trailing off.
    $ flash_a.display(PDAImage(look = "avert"), PDAMove(alignX = 2.5, duration = 2.0))
    $ flash_b.display(PDAMove(alignX = -1.5, duration = 4.0))
    headmaster.think "We all breathed it in that day, the whole wing, and just... carried on."
    # Snap back to the bike rack.
    $ paperdoll_manager.clear()
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "You blink the corridor away. Just the bike rack again. Just the glass, and whatever's still clinging to it."

    $ call_custom_menu_with_text("The vial's still there, catching the light. Someone will kick it into a drain if you don't move first.", character.subtitles, False,
        MenuElement("bag", "Bag it and call Emiko", EventEffect("nm_potion_hangover_vial.bag")),
        MenuElement("note", "Log it quietly", EventEffect("nm_potion_hangover_vial.note")),
        MenuElement("ignore", "Leave it where it is", EventEffect("nm_potion_hangover_vial.ignore")),
    **kwargs)

label .bag (**kwargs):

    subtitles "You fold the glass into a handkerchief, corner by corner, and dial the office."
    # Cut to her end of the line: phone at her ear, sliding in like private_line.
    $ emiko.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/secretary 5 1 0.webp", blur = True)
    $ emiko.display(PDAImage(pose = "35", outfit = "uniform", level = 5, mood = "suspicious", mouth = "closed", look = "avert"),
        PDAPreset("upper_body"), PDAMove(alignX = -1.5, alignY = -0.3, duration = 0.0))
    $ emiko.display(PDAMove(alignX = 0.5, duration = 0.8), PDAPause(0.8),
        PDAImage(mouth = "open"))
    emiko.say "Green glass. Sweet-smelling."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster "...I didn't say what colour it was."
    # A hitch on the line — caught. Then the professional voice, eyes on him.
    $ emiko.display(PDAShake(duration = 0.2, max_distance = 4), PDAPause(0.2),
        PDAImage(mood = "neutral", look = "follow"), PDAPause(0.4),
        PDAImage(mouth = "open"))
    emiko.say "Bring it straight up. Back stairs, not the courtyard. And for heaven's sake don't let a student get a look at it."
    # She hangs up; his thoughts land on the empty office.
    $ emiko.display(PDAImage(mouth = "closed"), PDAMove(alignX = -1.5, duration = 0.8), PDAPause(0.8))
    headmaster.think "She named the colour before I did. Didn't even blink."
    headmaster.think "...How long has she been waiting for one of these to turn up? And why the back stairs?"

    $ set_game_data("nm_vial_traced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=TINY, reputation=TINY) from _nm_ph_vial_bag
    $ end_event('new_daytime', **kwargs)

label .note (**kwargs):
    subtitles "You sketch the spot in your pocket notebook — distance from the rack, the angle of the light — and nudge a fallen leaf over the smear with your shoe."
    headmaster.think "There. A date, in my own handwriting. If anyone ever tells me this didn't happen, I'll have that."

    $ set_game_data("nm_vial_traced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(education=TINY) from _nm_ph_vial_note
    $ end_event('new_daytime', **kwargs)

label .ignore (**kwargs):
    subtitles "You straighten up and walk on. The sweet smell trails you for three steps, then the wind takes it and the courtyard is only a courtyard again."
    headmaster.think "...And I'm just going to walk past it. Right."
    headmaster.think "If this ever turns into something, I'll be the man who saw it behind the bike rack and kept walking."

    $ situation_manager.apply_progress_change("situation:new_management:main", -1)
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Testing the Waters ----------- #
#######################################

# ═══ SCENE · nm_testing_the_waters_clipboard ══════════════════════════════════
#  The courtyard. Yuriko Oshima (a student rep) steps into the headmaster's path with
#  a clipboard and pen ready and fires off grey-area policy questions — dress code,
#  phones, dating — writing his answers down as he gives them. Her opening question
#  varies (<grey_area>).
#
#  Wired: one image via show_pattern("main"); Yuriko paperdoll over the blurred
#  courtyard background. She cuts in from the right (walk pose) to close_body, briefs
#  with the clipboard (12), counts off "first one" (37), waits arms-crossed (34); at
#  the menu the frame presses in to upper_body. Each branch ends with her walking off
#  left before his closing thought.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_testing_the_waters_clipboard (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ yuriko = Person["yuriko_oshima"]
    $ grey_area = get_value("grey_area", **kwargs)

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "You've barely cleared the courtyard arch before Yuriko Oshima steps neatly into your path, clipboard already uncapped. This was planned."
    # Parked off the right edge at register so nothing flashes; she cuts across into his path.
    $ yuriko.register_paperdoll(config = {"alignX": 2.5})
    $ yuriko.display(PDAImage(pose = "39", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed"),
        PDAFlip(True), PDAPreset("close_body"))
    $ yuriko.display(PDAPreset("close_body_center", duration = 0.4), PDAPause(0.4),
        PDAFlip(False), PDAImage(pose = "12", mouth = "open"))
    yuriko.say "Headmaster. Some of the others wanted me to ask you a few things. Grey areas. I said I'd ask, so. I'm asking."
    $ yuriko.display(PDAImage(pose = "37", mood = "suspicious"))
    yuriko.say "First one: [grey_area]. And I'm writing down whatever you say, word for word. So you might want to think about it first."
    $ yuriko.display(PDAImage(pose = "34", mouth = "closed"))
    headmaster.think "Whatever I say here, every year group's going to be quoting back at me by lunch."

    $ high_charm = get_stat_value("charm", [20, 100], **kwargs) >= 20

    # Pen poised — the frame presses in while he decides.
    $ yuriko.display(PDAImage(pose = "12"), PDAPreset("upper_body_center", duration = 1.5))
    $ call_custom_menu_with_text("The pen is hovering.", character.subtitles, False,
        MenuElement("precise", "Give her a clean, clear answer", EventEffect("nm_testing_the_waters_clipboard.precise")),
        MenuElement("turnaround", "Turn it around — ask what they assume", EventEffect("nm_testing_the_waters_clipboard.turnaround"), high_charm),
        MenuElement("hedge", "Duck it — 'case by case'", EventEffect("nm_testing_the_waters_clipboard.hedge")),
    **kwargs)

label .precise (**kwargs):
    $ yuriko = Person["yuriko_oshima"]

    headmaster "On the record, then. Uniform's optional off campus — neat if you're representing us. Phones, free periods only, on silent. No PDA on school grounds. Simple as that."
    # Writing it down, eyes on the board.
    $ yuriko.display(PDAImage(mood = "neutral", look = "avert"))
    subtitles "The pen moves fast — three clean lines, underlined once each. The corner of her mouth does something that isn't quite a smile."
    $ yuriko.display(PDAImage(pose = "34", mouth = "open", look = "follow"))
    yuriko.say "...Huh. That's annoyingly clear."
    $ yuriko.display(PDAImage(pose = "2", mood = "happy"))
    yuriko.say "I was sort of hoping you'd waffle."
    # Off she goes with her three clean lines.
    $ yuriko.display(PDAImage(pose = "39", mouth = "closed"), PDAFlip(True, duration = 0.3), PDAPause(0.3),
        PDAMove(alignX = -1.5, duration = 1.2), PDAPause(1.2))
    headmaster.think "If it's going round the school anyway, at least it's going round in my words."

    $ set_game_data("nm_yuriko_ally", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, education=TINY) from _nm_tw_clip_precise
    $ end_event('new_daytime', **kwargs)

label .turnaround (**kwargs):
    $ yuriko = Person["yuriko_oshima"]

    headmaster "Before I answer — what do the students already think the rule is? You'd know better than the handbook does."
    $ yuriko.display(PDAImage(pose = "19", mood = "suprised", mouth = "open"))
    yuriko.say "...What? Why are you asking {i}me?{/i}"
    $ yuriko.display(PDAImage(pose = "21", mood = "neutral", look = "avert"))
    yuriko.say "...Fine. Most of them assume the sensible version, obviously."
    $ yuriko.display(PDAImage(look = "follow"))
    yuriko.say "It's only the grey bits they poke at, to see what happens."
    $ yuriko.display(PDAImage(mouth = "closed"))
    headmaster "Then let's make the sensible version the official one — and you get to tell them it came from asking you, not guessing."
    $ yuriko.display(PDAImage(pose = "4", mood = "pout", mouth = "open"))
    yuriko.say "Don't think this makes us friends."
    $ yuriko.display(PDAImage(pose = "34", mood = "happy", look = "avert"))
    yuriko.say "...I'll pass it on. Properly. Because if I don't, somebody else will, and they'll get it wrong."
    $ yuriko.display(PDAImage(pose = "39", mouth = "closed"), PDAFlip(True, duration = 0.3), PDAPause(0.3),
        PDAMove(alignX = -1.5, duration = 1.2), PDAPause(1.2))
    headmaster.think "She came out here to catch me out. I think she's going back slightly annoyed that she couldn't."

    $ set_game_data("nm_yuriko_ally", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL, charm=SMALL) from _nm_tw_clip_turn
    $ end_event('new_daytime', **kwargs)

label .hedge (**kwargs):
    $ yuriko = Person["yuriko_oshima"]

    headmaster "It, ah— depends. Case by case, really. Let me get back to you on that one."
    $ yuriko.display(PDAImage(pose = "25", mood = "suspicious", mouth = "open"))
    yuriko.say "So. Un-de-fined."
    # Writing it big, eyes on the board — then the pen clicks shut, smug, and she's gone.
    $ yuriko.display(PDAImage(pose = "12", mouth = "closed", look = "avert"))
    subtitles "She writes the word out slowly, larger than the rest, and caps the pen like she's got exactly what she came for."
    $ yuriko.display(PDAImage(pose = "2", mood = "happy", look = "follow"), PDAPause(0.6),
        PDAImage(pose = "39"), PDAFlip(True, duration = 0.3), PDAPause(0.3),
        PDAMove(alignX = -1.5, duration = 1.2), PDAPause(1.2))
    headmaster.think "'Un-de-fined.' In letters twice the size of everything else."
    headmaster.think "...Whatever she writes underneath that, the whole school's going to read it as mine."

    $ situation_manager.apply_progress_change("situation:new_management:main", -3)
    call change_stats_with_modifier(reputation=DEC_SMALL) from _nm_tw_clip_hedge
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_testing_the_waters_memo ═══════════════════════════════════════
#  At the headmaster's desk. A blank school-wide memo form sits squared on the blotter
#  — Emiko left it for him to write the school's first message from him, in his own
#  words. Mostly he's alone with the form; Emiko steps in only briefly (under Guided)
#  to nudge him, then he writes it — well, or blandly.
#
#  Wired: one image via show_pattern("main"); Emiko (level 5) paperdoll over the blurred
#  office/secretary background — a lean-in through the door under Guided, then she
#  comes in to read the finished memo and walks off with it (or away from it).
# ═══════════════════════════════════════════════════════════════════════════════
label nm_testing_the_waters_memo (**kwargs):
    $ begin_event(version = "2", **kwargs)


    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/secretary 5 1 0.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "A blank school-wide memo form waits on your blotter, edges squared to the wood. You didn't put it there."
    headmaster.think "Emiko. Of course."
    headmaster.think "The first thing the whole school reads in my own words. ...She wants to see what I do with it. So do I, honestly."

    $ emiko.register_paperdoll(config = {"alignX": 2.5})

    if get_value("guided", 0, **kwargs) == 1:
        # She leans in through the doorway on the right, never fully entering.
        $ emiko.display(PDAImage(pose = "21", outfit = "uniform", level = 5, mood = "happy", mouth = "open", look = "follow"),
            PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 2.5))
        $ emiko.display(PDAMove(alignX = 1.1, duration = 0.5))
        $ emiko.display(PDAPause(0.5))
        emiko.say "Template's on the left, your words on the right. ...Go on."
        $ emiko.display(PDAImage(pose = "10", mouth = "open", look = "avert"))
        emiko.say "I won't read over your shoulder. Much."
        $ emiko.display(PDAImage(mouth = "closed"), PDAMove(alignX = 2.5, duration = 0.6))
        $ emiko.display(PDAPause(0.6))

    $ call_custom_menu_with_text("The form is blank. The pen is yours.", character.subtitles, False,
        MenuElement("own", "Write it in your own voice", EventEffect("nm_testing_the_waters_memo.own")),
        MenuElement("vague", "Fill the boxes, say nothing", EventEffect("nm_testing_the_waters_memo.vague")),
    **kwargs)

label .own (**kwargs):

    subtitles "You write about being present. About office hours that actually mean something. About a door — correctly labelled now — that stays open."
    subtitles "It takes three drafts. The third one finally sounds like a person instead of a form."

    # She comes round the desk and reads it off the blotter.
    $ emiko.display(PDAImage(pose = "39", outfit = "uniform", level = 5, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body", duration = 0.0), PDAMove(alignX = 2.5))
    $ emiko.display(PDAPreset("close_body_center", duration = 0.8))
    $ emiko.display(PDAPause(0.8))
    $ emiko.display(PDAFlip(False), PDAImage(pose = "9", mood = "neutral", mouth = "closed", look = "avert"))
    $ emiko.display(PDAPause(1.2))
    $ emiko.display(PDAImage(pose = "2", mood = "shining", mouth = "open", look = "follow"))
    emiko.say "...Huh. That actually sounds like you."
    emiko.say "I'll run copies before the last bell."
    $ emiko.display(PDAImage(pose = "39", mouth = "closed", look = "avert"), PDAFlip(True, 0.3))
    $ emiko.display(PDAPause(0.3))
    $ emiko.display(PDAMove(alignX = -1.5, duration = 1.2))
    $ emiko.display(PDAPause(1.2))
    headmaster.think "...It does, actually. Sound like me. Three drafts, but it does."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=MEDIUM, education=TINY) from _nm_tw_memo_own
    $ end_event('new_daytime', **kwargs)

label .vague (**kwargs):

    subtitles "You tick the required boxes, sign the bottom, and leave the body of it saying almost nothing at all."

    $ emiko.display(PDAImage(pose = "39", outfit = "uniform", level = 5, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body", duration = 0.0), PDAMove(alignX = 2.5))
    $ emiko.display(PDAPreset("close_body_center", duration = 0.8))
    $ emiko.display(PDAPause(0.8))
    $ emiko.display(PDAFlip(False), PDAImage(pose = "9", mood = "neutral", mouth = "closed", look = "avert"))
    $ emiko.display(PDAPause(1.2))
    $ emiko.display(PDAImage(pose = "34", mood = "neutral", mouth = "open", look = "follow"))
    emiko.say "Mm. Safe."
    $ emiko.display(PDAImage(mouth = "closed", look = "avert"))
    $ emiko.display(PDAPause(0.6))
    $ emiko.display(PDAImage(pose = "39"), PDAFlip(True, 0.3))
    $ emiko.display(PDAPause(0.3))
    $ emiko.display(PDAMove(alignX = -1.5, duration = 1.4))
    headmaster.think "'Safe.' She only says it in that voice when she means empty."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _nm_tw_memo_vague
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Rumors in Bloom -------------- #
#######################################

# ═══ SCENE · nm_rumors_in_bloom_kiosk ═════════════════════════════════════════
#  The kiosk at break, in the queue crush. Aona and a classmate are ranking the staff
#  out loud like a leaderboard when Aona spots the headmaster and, this time, recognises
#  him from the assembly. Depending on their earlier run-ins she's friendly or wary. If
#  he just listens, he overhears a piece of gossip that varies (<rumor>). The classmate
#  is random each time (ikushi_ito / lin_kato / ishimaru_maki).
#
#  Wired: one image via show_pattern("main"); the overheard gossip plays over it (no
#  paperdolls). In the branches where he speaks to her, Aona turns round (close_body
#  center) with the classmate half in frame behind her on the right; on "break" both
#  turn their backs and walk off. Background: kiosk/1 1 1.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_rumors_in_bloom_kiosk (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ aona = Person["aona_komuro"]
    $ bystander = get_person_value("bystander", **kwargs)
    $ rumor = get_value("rumor", **kwargs)
    $ snapped = get_value("snapped", 0, **kwargs) == 1
    $ face_known = get_value("face_known", 0, **kwargs) == 1

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/kiosk/1 1 1.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "The kiosk line is its usual break-time crush. Somewhere in the thick of it, Aona is holding court again — ranking the staff out loud like a league table."
    # OVERHEARD: Aona is ranking the staff to her group, not talking to him — he just
    # catches it in the queue. NO paperdolls here (paperdolls face the player); the
    # scene image shows them and he watches.
    aona.say "Number three, and that's generous— oh. {i}Oh.{/i} Hang on."
    aona.say "That's him. From the assembly. I actually recognise him now."
    if face_known:
        aona.say "...the one who told me off for the 'janitor' thing. Yeah. Definitely him."
        headmaster.think "It stuck. A couple of weeks ago I was the maintenance man. Now she's picking me out of the crisps queue."
    else:
        bystander.say "Told you it was the headmaster."
        headmaster.think "She's placed me. In the crisps queue, of all places."
        headmaster.think "...I'll take it."

    if snapped:
        subtitles "She drops her voice a notch when she clocks you're in earshot. She hasn't forgotten getting snapped at."

    $ call_custom_menu_with_text("You're three back in the queue — and squarely in the ranking.", character.subtitles, False,
        MenuElement("intervene", "Step in, light and easy", EventEffect("nm_rumors_in_bloom_kiosk.intervene")),
        MenuElement("listen", "Say nothing and listen", EventEffect("nm_rumors_in_bloom_kiosk.listen")),
        MenuElement("break", "Cut it off — 'line's moving'", EventEffect("nm_rumors_in_bloom_kiosk.break")),
    **kwargs)

label .intervene (**kwargs):
    $ aona = Person["aona_komuro"]
    $ bystander = get_person_value("bystander", **kwargs)
    $ snapped = get_value("snapped", 0, **kwargs) == 1

    headmaster "If you're going to rank me, at least rank me by the right job. Headmaster. Not a number on your list."
    # He's stepped in and spoken to her → Aona turns to face him; the classmate hangs back.
    $ aona.register_paperdoll()
    $ bystander.register_paperdoll(behind = True)
    $ bystander.display(PDAImage(pose = "14", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 1.0))
    if snapped:
        $ aona.display(PDAImage(pose = "23", outfit = "uniform", level = 1, mood = "suspicious", mouth = "closed", look = "follow"),
            PDAPreset("close_body_center", duration = 0.0))
        $ aona.display(PDAPause(0.8))
    else:
        $ aona.display(PDAImage(pose = "19", outfit = "uniform", level = 1, mood = "suprised", mouth = "$", look = "follow"),
            PDAPreset("close_body_center", duration = 0.0), PDAShake(0.25, 4))
        $ aona.display(PDAPause(0.6))
    $ aona.display(PDAImage(pose = "2", mood = "happy", mouth = "open", look = "follow"))
    aona.say "...okay, that's fair."
    $ aona.display(PDAImage(pose = "37", mouth = "open", look = "avert"))
    aona.say "Headmaster. Noted."
    $ aona.display(PDAImage(pose = "2", mood = "happy", mouth = "closed", look = "follow"))
    $ bystander.display(PDAImage(pose = "1", mood = "happy", mouth = "closed", look = "follow"))
    subtitles "The game folds up on its own. The grin doesn't — but now it's pointed with you, not at you."
    headmaster.think "She's still grinning. At least now I'm in on the joke."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY) from _nm_rb_kiosk_intervene
    $ end_event('new_daytime', **kwargs)

label .listen (**kwargs):
    # No paperdoll — he hangs back and overhears; nobody's talking to him.
    subtitles "You stay put and let the queue carry you. The talk washes past — names, small grievances — and then something snags: [rumor]."
    headmaster.think "Half of that's nonsense. That last bit, though, the one they all dropped their voices for..."
    headmaster.think "I'm keeping that."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _nm_rb_kiosk_listen
    $ end_event('new_daytime', **kwargs)

label .break (**kwargs):
    $ aona = Person["aona_komuro"]
    $ bystander = get_person_value("bystander", **kwargs)

    headmaster "Line's moving. Save the gossip for your own time."
    # He's cut in and addressed her → Aona turns, sulks, and both turn their backs on him.
    $ aona.register_paperdoll()
    $ bystander.register_paperdoll(behind = True)
    $ bystander.display(PDAImage(pose = "14", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 1.0))
    $ aona.display(PDAImage(pose = "19", outfit = "uniform", level = 1, mood = "suprised", mouth = "$", look = "follow"),
        PDAPreset("close_body_center", duration = 0.0), PDAShake(0.2, 4))
    $ aona.display(PDAPause(0.5))
    $ aona.display(PDAImage(pose = "25", mood = "pout", mouth = "$", look = "avert"))
    aona.say "...sheesh. Fine."
    $ aona.display(PDAImage(pose = "39", mood = "neutral", mouth = "closed", look = "avert"), PDAFlip(True, 0.3))
    $ aona.display(PDAPause(0.3))
    $ aona.display(PDAMove(alignX = -1.5, duration = 1.2))
    $ bystander.display(PDAPause(0.4))
    $ bystander.display(PDAImage(pose = "39"), PDAMove(alignX = -1.5, duration = 1.6))
    $ bystander.display(PDAPause(1.6))
    headmaster.think "'Sheesh.' ...Next time I'm in this queue, they'll all just go quiet until I've gone."

    $ situation_manager.apply_progress_change("situation:new_management:main", -1)
    call change_stats_with_modifier(happiness=DEC_TINY) from _nm_rb_kiosk_break
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_rumors_in_bloom_chalk ═════════════════════════════════════════
#  Behind the bike shed. Someone has chalked a portrait of the headmaster on the brick
#  wall — rough, but flattering. How it flatters him varies (<exaggeration>: a heroic
#  square jaw / oversized shoulders / a little crown). No one is around at first; if he
#  touches the drawing up himself, a student (Aona) catches him at it.
#
#  Wired: one image via show_pattern("main"); on "correct", Aona catches him (close-up,
#  startled → leaning in → grin) and runs off to spread it, over the courtyard background.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_rumors_in_bloom_chalk (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ exaggeration = get_value("exaggeration", **kwargs)

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "Behind the bike shed, someone's chalked a portrait onto the brick. It's roughly you — and, weirdly, flattering: [exaggeration]."
    headmaster.think "That's... me. Roughly."
    headmaster.think "A month ago half of them weren't sure I even worked here."

    $ call_custom_menu_with_text("Nobody's around. Just you and the wall.", character.subtitles, False,
        MenuElement("leave", "Leave it be", EventEffect("nm_rumors_in_bloom_chalk.leave")),
        MenuElement("correct", "Add one small touch of your own", EventEffect("nm_rumors_in_bloom_chalk.correct")),
        MenuElement("erase", "Scrub it off", EventEffect("nm_rumors_in_bloom_chalk.erase")),
    **kwargs)

label .leave (**kwargs):
    subtitles "You leave it be and walk on. Let it keep grinning at the bike racks."
    headmaster.think "I could do worse than spend the rest of the year trying to live up to that."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(happiness=TINY, charm=TINY) from _nm_rb_chalk_leave
    $ end_event('new_daytime', **kwargs)

label .correct (**kwargs):
    $ aona = Person["aona_komuro"]

    subtitles "There's a nub of chalk in the dirt. You crouch, soften the jaw a touch, and add the one honest smile-line the artist was too shy to draw."
    subtitles "A footstep scuffs behind you. A student — of course — has caught the headmaster vandalising his own portrait."
    $ aona.register_paperdoll()
    $ aona.display(PDAImage(pose = "19", outfit = "uniform", level = 1, mood = "suprised", mouth = "$", look = "follow"),
        PDAPreset("upper_body_center", duration = 0.0), PDAShake(0.25, 4))
    $ aona.display(PDAPause(0.6))
    $ aona.display(PDAImage(pose = "38", mood = "suspicious", mouth = "open", look = "follow"))
    aona.say "...did you just {i}improve{/i} it?"
    $ aona.display(PDAImage(mouth = "closed"))
    headmaster "It needed a smile. Don't tell anyone."
    $ aona.display(PDAImage(pose = "2", mood = "happy", mouth = "closed", look = "follow"))
    $ aona.display(PDAPause(0.8))
    $ aona.display(PDAImage(pose = "20", look = "avert"))
    $ aona.display(PDAPause(0.4))
    # Off she goes to tell everyone — the rumour literally running away from him.
    $ aona.display(PDAImage(pose = "39"), PDAMove(alignX = 2.5, duration = 0.9))
    headmaster.think "That'll be round the whole year group by tomorrow."
    headmaster.think "...Good."

    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(charm=SMALL, happiness=TINY) from _nm_rb_chalk_correct
    $ end_event('new_daytime', **kwargs)

label .erase (**kwargs):
    subtitles "You scrub it off with your sleeve until there's nothing but a grey smear and chalk dust on your cuff. The shed goes very quiet."
    headmaster.think "...Somebody drew me because they liked me. And I just rubbed it out with my sleeve."

    $ situation_manager.apply_progress_change("situation:new_management:main", -2)
    call change_stats_with_modifier(happiness=DEC_SMALL, reputation=DEC_TINY) from _nm_rb_chalk_erase
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Quiet Endorsements ----------- #
#######################################

# ═══ SCENE · nm_quiet_endorsements_after_bell ═════════════════════════════════
#  Just after the bell, at a classroom doorway as students file out. Miwa hangs back
#  against the flow to thank the headmaster for helping her the other day, then hurries
#  off before it gets awkward. Under Guided, Zoe Parker (the PE teacher) leans out of
#  the gym doorway as she passes with a quick word.
#
#  Wired: no establishing image (paperdoll-only) over the blurred school-building
#  background. Two blurred classmates stream past behind (the "tide"), Miwa holds her
#  ground in front, then turns half to the door for the menu; Zoe leans in from the
#  right under Guided. Each branch turns Miwa back, then walks her off left.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_quiet_endorsements_after_bell (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ miwa = Person["miwa_igarashi"]
    $ miwa_helped = get_value("miwa_helped", 0, **kwargs) == 1
    $ tide_a = Person["lin_kato"]
    $ tide_b = Person["ishimaru_maki"]

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True)

    # The tide: two blurred classmates file past behind, heading out.
    $ tide_a.register_paperdoll(blur = 3.0, behind = True, config = {"alignX": 2.5, "blur": 3.0})
    $ tide_b.register_paperdoll(blur = 4.0, behind = True, config = {"alignX": 2.5, "blur": 4.0})
    $ tide_a.display(PDAImage(pose = "39", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAMove(alignY = 0.0, zoom = 1.7))
    $ tide_b.display(PDAImage(pose = "39", outfit = "uniform", level = 1, mood = "happy", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAMove(alignY = 0.05, zoom = 1.5))
    $ tide_a.display(PDAMove(alignX = -1.5, duration = 2.5))
    $ tide_b.display(PDAPause(0.6))
    $ tide_b.display(PDAMove(alignX = -1.5, duration = 3.2))
    subtitles "The bell cuts the period short. Bags zip, chairs scrape — and against the tide, Miwa hangs back a second by the door."

    $ miwa.register_paperdoll()
    $ miwa.display(PDAImage(pose = "12", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAPreset("close_body_center", duration = 0.0))
    $ miwa.display(PDAPause(0.5))
    if miwa_helped:
        $ miwa.display(PDAImage(pose = "31", mood = "happy", mouth = "open", look = "avert"))
        miwa.say "Um— thanks. For actually taking it seriously. When I couldn't remember."
        $ miwa.display(PDAImage(look = "follow"))
        miwa.say "It— it helped, more than I said."
        $ miwa.display(PDAImage(pose = "1", mood = "happy", mouth = "closed", look = "avert"))
        headmaster.think "She swam against the whole class just to say that."
        headmaster.think "...God."
    else:
        $ miwa.display(PDAImage(pose = "12", mood = "neutral", mouth = "open", look = "avert"))
        miwa.say "Um— thanks. For not making it weird the other day. When I was all... out of it."
        $ miwa.display(PDAImage(pose = "1", mood = "happy", mouth = "closed", look = "avert"))
        headmaster.think "I barely did anything for her that day. She's remembered it as kind anyway."
    $ miwa.display(PDAImage(pose = "14", mood = "sad", mouth = "open", look = "avert"))
    miwa.say "I— I have to go, I can't stay, but— yeah. Thanks."
    # Already turning for the door — half out of frame for the menu.
    $ miwa.display(PDAImage(pose = "39", mood = "neutral", mouth = "closed", look = "avert"), PDAFlip(True, 0.3))
    $ miwa.display(PDAPause(0.3))
    $ miwa.display(PDAMove(alignX = 0.3, duration = 0.8))

    if get_value("guided", 0, **kwargs) == 1:
        $ zoe = Person["zoe_parker"]
        $ zoe.register_paperdoll(config = {"alignX": 2.5})
        $ zoe.display(PDAImage(pose = "2", outfit = "uniform", level = 1, mood = "happy", mouth = "closed", look = "follow"),
            PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 2.5))
        $ zoe.display(PDAMove(alignX = 1.1, duration = 0.5))
        $ zoe.display(PDAPause(0.5))
        subtitles "Zoe Parker leans out of the gym doorway as she passes, half a grin on."
        $ zoe.display(PDAImage(mouth = "open"))
        zoe.say "Place runs quieter when you actually drop by, y'know. Just saying."
        $ zoe.display(PDAImage(mouth = "closed"), PDAMove(alignX = 2.5, duration = 0.6))
        $ zoe.display(PDAPause(0.6))

    $ call_custom_menu_with_text("Miwa's already half through the door.", character.subtitles, False,
        MenuElement("pace", "Keep it light and let her go", EventEffect("nm_quiet_endorsements_after_bell.pace")),
        MenuElement("followup", "One gentle question before she goes", EventEffect("nm_quiet_endorsements_after_bell.followup")),
        MenuElement("assign", "Remind her not to be late", EventEffect("nm_quiet_endorsements_after_bell.assign")),
    **kwargs)

label .pace (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    $ miwa.display(PDAFlip(False, 0.3), PDAImage(pose = "1", mood = "happy", mouth = "closed", look = "follow"))
    headmaster "Go on, you'll be late. Door's open if you ever need it — that's all."
    $ miwa.display(PDAImage(mouth = "open", look = "avert"))
    miwa.say "Okay. ...Okay."
    $ miwa.display(PDAImage(pose = "39", mouth = "closed"), PDAFlip(True, 0.2))
    $ miwa.display(PDAPause(0.2))
    $ miwa.display(PDAMove(alignX = -1.5, duration = 0.8))
    subtitles "And she's gone — quick and light, before the thank-you can curdle into something awkward. Exactly the way she needed it to go."

    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(happiness=MEDIUM, charm=TINY) from _nm_qe_bell_pace
    $ end_event('new_daytime', **kwargs)

label .followup (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    $ miwa.display(PDAFlip(False, 0.3), PDAImage(pose = "19", mood = "suprised", mouth = "$", look = "follow"))
    headmaster "Quick one — sleeping any better these days?"
    $ miwa.display(PDAImage(pose = "7", mood = "neutral", mouth = "open", look = "avert"))
    miwa.say "A bit."
    $ miwa.display(PDAImage(pose = "1", mood = "happy", mouth = "open", look = "follow"))
    miwa.say "...I'll tell you about it next time. Promise."
    $ miwa.display(PDAImage(pose = "39", mouth = "closed", look = "avert"), PDAFlip(True, 0.3))
    $ miwa.display(PDAPause(0.3))
    $ miwa.display(PDAMove(alignX = -1.5, duration = 1.0))
    $ miwa.display(PDAPause(1.0))
    headmaster.think "'Next time.' She said that all by herself."
    headmaster.think "A few weeks ago she couldn't get a word out."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(happiness=SMALL) from _nm_qe_bell_follow
    $ end_event('new_daytime', **kwargs)

label .assign (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    $ miwa.display(PDAFlip(False, 0.3), PDAImage(pose = "12", mood = "neutral", mouth = "closed", look = "follow"))
    headmaster "Good. Now don't be late to your next class."
    $ miwa.display(PDAImage(pose = "12", mood = "sad", mouth = "open", look = "avert"))
    miwa.say "...yes, sir."
    # She shrinks away slowly while he catches up with what he just did.
    $ miwa.display(PDAImage(pose = "39", mouth = "closed"), PDAFlip(True, 0.3))
    $ miwa.display(PDAPause(0.3))
    $ miwa.display(PDAMove(alignX = -1.5, duration = 2.0))
    headmaster.think "'Yes, sir.' ...She worked up the nerve to thank me, and I reminded her about the bell."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(education=TINY) from _nm_qe_bell_assign
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_quiet_endorsements_second_coffee ══════════════════════════════
#  The counselling office again, some time later and much calmer. Lily is back for a
#  follow-up — steadier now, here by choice rather than in a panic. When she sets her
#  coffee mug down this time it doesn't rattle; it just sits still. (Bookends her
#  earlier shaken visit.)
#
#  Wired: one image via show_pattern("main"); Lily paperdoll over the blurred
#  teacher-office background. Deliberately mirrors her first visit: same pose-12 mug
#  hold, but no shake; she settles back (zoom out) from the start; on "advice" she
#  leaves quietly, like the bad exit of the first visit.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_quiet_endorsements_second_coffee (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ lily = Person["lily_anderson"]
    $ lily_witnessed = get_value("lily_witnessed", 0, **kwargs) == 1

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/teacher 1 1 0.webp", blur = True)
    subtitles "Second coffee, same desk — but the air in the room has changed. Lighter."
    $ show_pattern("main", **kwargs)
    # Same mug hold as last time — and this time, no shake. The stillness is the point.
    $ lily.register_paperdoll()
    $ lily.display(PDAImage(pose = "12", outfit = "uniform", level = 1, mood = "happy", mouth = "closed", look = "avert"),
        PDAPreset("close_body_center", duration = 0.0))
    subtitles "When she sets the mug down, it doesn't rattle. It just sits there, steady, like it never did anything else."
    if lily_witnessed:
        $ lily.display(PDAImage(pose = "7", mood = "happy", mouth = "open", look = "avert"))
        lily.say "I keep coming back to what you did last week. Just — saying it out loud with me. It steadied more than I let on."
        $ lily.display(PDAImage(pose = "1", mood = "happy", mouth = "open", look = "follow"))
        lily.say "And I'm not falling apart this time, before you ask. I just... like it in here."
        $ lily.display(PDAImage(pose = "14", mood = "happy", mouth = "open", look = "avert"))
        lily.say "Is that weird? It's a bit weird. It's nice to sit somewhere and not be in a hurry for once."
    else:
        $ lily.display(PDAImage(pose = "38", mood = "neutral", mouth = "open", look = "follow"))
        lily.say "We didn't really get to talk properly last time. I wanted to try again, if the offer still stands."
        $ lily.display(PDAImage(pose = "12", mood = "happy", mouth = "open", look = "avert"))
        lily.say "I'm not in crisis. I'd just... like somewhere steady to think out loud. If that's allowed."
    $ lily.display(PDAImage(pose = "12", mood = "happy", mouth = "closed", look = "follow"), PDAMove(zoom = "-0.2", duration = 1.0))
    headmaster.think "She's here on a good day. ...That's new."

    $ call_custom_menu_with_text("She's settled in, in no hurry.", character.subtitles, False,
        MenuElement("attend", "Just be present", EventEffect("nm_quiet_endorsements_second_coffee.attend")),
        MenuElement("summarize", "Listen, then set the next date", EventEffect("nm_quiet_endorsements_second_coffee.summarize")),
        MenuElement("advice", "Hand her some brisk advice", EventEffect("nm_quiet_endorsements_second_coffee.advice")),
    **kwargs)

label .attend (**kwargs):
    $ lily = Person["lily_anderson"]

    $ lily.display(PDAImage(pose = "7", mood = "happy", mouth = "closed", look = "avert"))
    subtitles "You don't rush to fill the silences. You let them stretch, and she steps into them when she's ready — which she does, easily now."
    $ lily.display(PDAImage(pose = "38", mood = "happy", mouth = "open", look = "follow"))
    lily.say "...same time next week?"
    $ lily.display(PDAImage(mouth = "closed"))
    headmaster "Same time."
    $ lily.display(PDAImage(pose = "1", mood = "happy", mouth = "closed", look = "avert"))
    headmaster.think "Same time next week. She means it."
    headmaster.think "...Huh. So do I. I'm actually looking forward to it."

    $ set_game_data("nm_care_channel", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(happiness=MEDIUM, reputation=TINY) from _nm_qe_coffee_attend
    $ end_event('new_daytime', **kwargs)

label .summarize (**kwargs):
    $ lily = Person["lily_anderson"]

    $ lily.display(PDAImage(pose = "12", mood = "neutral", mouth = "closed", look = "follow"))
    headmaster "Next Thursday, free period. And if anything spikes before then, put a note through Emiko and I'll make room sooner."
    $ lily.display(PDAImage(pose = "31", mood = "happy", mouth = "open", look = "follow"))
    lily.say "Clear. Thank you — it helps, honestly, just knowing the door's got hours on it."

    $ set_game_data("nm_care_channel", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(happiness=SMALL, education=TINY) from _nm_qe_coffee_sum
    $ end_event('new_daytime', **kwargs)

label .advice (**kwargs):
    $ lily = Person["lily_anderson"]

    $ lily.display(PDAImage(pose = "12", mood = "neutral", mouth = "closed", look = "follow"))
    headmaster "Sleep schedule, plenty of water, and stop grading past midnight. You'll feel worlds better."
    $ lily.display(PDAImage(pose = "23", mood = "sad", mouth = "open", look = "avert"))
    lily.say "I... yes. I do know those things."
    $ lily.display(PDAImage(pose = "13", mood = "sad", mouth = "closed", look = "avert"))
    headmaster.think "Water, sleep, stop marking late. She could've written that pamphlet herself."
    # She sets the mug down and slips out — the first visit's bad exit, quieter.
    $ lily.display(PDAImage(pose = "39"), PDAFlip(True, 0.3))
    $ lily.display(PDAPause(0.3))
    $ lily.display(PDAMove(alignX = -1.5, duration = 1.6))
    headmaster.think "...She wanted somebody to listen, and I started fixing her before she'd finished a sentence."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_quiet_endorsements_curriculum ═════════════════════════════════
#  At the headmaster's desk. His lesson outline is back in the tray with a small
#  approving pen-tick in the margin and an apologetic sticky note. Lily is there and,
#  flustered, rambles her way through admitting the pacing is "actually better" — then
#  catches herself and braces to be told off for it.
#
#  Wired: one image via show_pattern("main"); Lily paperdoll over the blurred office
#  background. She peeks in from the right, steps in, and pushes closer and closer as
#  she rambles (upper_body), then snaps back when she catches herself.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_quiet_endorsements_curriculum (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ lily = Person["lily_anderson"]

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/f.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "Your lesson outline is back in the tray. In the margin of the third block there's a single, very careful pen-tick, and a sticky note beside it in Lily's tiny handwriting: {i}Sorry!! Hope it's ok that I looked.{/i}"

    # She peeks in from the doorway on the right.
    $ lily.register_paperdoll(config = {"alignX": 2.5})
    $ lily.display(PDAImage(pose = "14", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 2.5))
    $ lily.display(PDAMove(alignX = 1.0, duration = 0.5))
    $ lily.display(PDAPause(0.5))
    $ lily.display(PDAImage(mouth = "open"))
    lily.say "Oh— you found it. Sorry. I didn't mean to scribble on your outline,"
    # Steps in as the point takes over.
    $ lily.display(PDAFlip(False, 0.3), PDAImage(pose = "21", mood = "happy", mouth = "open", look = "follow"),
        PDAPreset("close_body_center", duration = 0.6))
    lily.say "I just— the pacing on that third block. It's actually better. Really better."
    # And closer, and closer.
    $ lily.display(PDAImage(pose = "20", mood = "shining", mouth = "open", look = "follow"),
        PDAPreset("upper_body_center", duration = 1.5))
    lily.say "The way you've split the hard bit over two lessons, they'll actually have time to get it before the test, instead of—"
    # Catches herself — snap back.
    $ lily.display(PDAImage(pose = "14", mood = "sad", mouth = "open", look = "avert"),
        PDAPreset("close_body_center", duration = 0.3))
    lily.say "Sorry. I'm rambling. It works, is what I mean. It works."
    $ lily.display(PDAImage(pose = "12", mood = "sad", mouth = "closed", look = "avert"))
    headmaster.think "She's gone pink. I don't think she's ever said anything nice to me out loud before."
    $ lily.display(PDAImage(pose = "23", look = "follow"))
    headmaster.think "...She looks like she's waiting to be told off for it."

    $ call_custom_menu_with_text("The tick is still sitting there in the margin.", character.subtitles, False,
        MenuElement("adjust", "Take the note and rebuild the block", EventEffect("nm_quiet_endorsements_curriculum.adjust")),
        MenuElement("credit", "Promise to credit her publicly", EventEffect("nm_quiet_endorsements_curriculum.credit")),
        MenuElement("shrug", "File it and move on", EventEffect("nm_quiet_endorsements_curriculum.shrug")),
    **kwargs)

label .adjust (**kwargs):
    $ lily = Person["lily_anderson"]

    $ lily.display(PDAImage(pose = "19", mood = "suprised", mouth = "$", look = "follow"))
    headmaster "Then I'll rebuild the third block around it. Send me the rest of your notes, if you've got them."
    $ lily.display(PDAImage(pose = "12", mood = "happy", mouth = "open", look = "avert"))
    lily.say "I— already did, actually. They're in your tray, under the outline."
    $ lily.display(PDAImage(pose = "38", mood = "neutral", mouth = "open", look = "follow"))
    lily.say "Sorry, is that too much? I can take them back if it's too much."
    $ lily.display(PDAImage(pose = "1", mood = "happy", mouth = "closed", look = "avert"))
    headmaster.think "Of course they're already in my tray. ...All right, Lily."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(education=MEDIUM, reputation=TINY) from _nm_qe_curr_adjust
    $ end_event('new_daytime', **kwargs)

label .credit (**kwargs):
    $ lily = Person["lily_anderson"]

    $ lily.display(PDAImage(pose = "12", mood = "neutral", mouth = "closed", look = "follow"))
    headmaster "At the next staff brief, I'm saying the outline got better because of you. One sentence."
    $ lily.display(PDAImage(pose = "16", mood = "suprised", mouth = "$", look = "follow"))
    lily.say "Oh God, please don't. Not in front of everyone."
    $ lily.display(PDAImage(pose = "14", mood = "sad", mouth = "open", look = "avert"))
    lily.say "I'll go red. I'll go completely red, and then Chloe will make a face."
    $ lily.display(PDAImage(pose = "25", mood = "pout", mouth = "$", look = "avert"))
    headmaster "One sentence. I promise."
    $ lily.display(PDAImage(pose = "37", mood = "pout", mouth = "$", look = "follow"))
    lily.say "...One. And don't say 'excellent' or anything. Just— normal words."
    $ lily.display(PDAImage(pose = "1", mood = "happy", mouth = "closed", look = "avert"))
    headmaster.think "She's negotiating the adjectives out of her own compliment."
    headmaster.think "...She'll remember it for a year."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=SMALL, happiness=TINY, reputation=TINY) from _nm_qe_curr_credit
    $ end_event('new_daytime', **kwargs)

label .shrug (**kwargs):
    $ lily = Person["lily_anderson"]

    $ lily.display(PDAImage(pose = "12", mood = "sad", mouth = "closed", look = "avert"))
    $ lily.display(PDAPause(0.6))
    # She slips out while he's looking at the next form.
    $ lily.display(PDAImage(pose = "39"), PDAFlip(True, 0.3))
    $ lily.display(PDAPause(0.3))
    $ lily.display(PDAMove(alignX = -1.5, duration = 2.0))
    subtitles "You murmur a thanks, file the outline under 'done', and reach for the next form. When you glance up again, she's already gone."
    headmaster.think "...She left the sticky note on the corner of the desk. I didn't even see her put it there."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(education=TINY) from _nm_qe_curr_shrug
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Welcome Committee ------------ #
#######################################

# ═══ SCENE · nm_welcome_committee_mug ═════════════════════════════════════════
#  The staff room, after a class. A full mug of coffee sits waiting in the middle of
#  the circle for the headmaster. Finola Ryan (a teacher) raises it in a toast to him
#  surviving his first week; Yulan is there too, more reserved, and — if she's warmed
#  to him — offers a stiff, backhanded bit of praise.
#
#  Wired: one image via show_pattern("main"); Finola (left) + Yulan (right, behind)
#  paperdolls over the blurred staff-room background. Finola gets shoved forward into
#  frame; Yulan's smile only shows on his thought after the "hmph"; on "brief" he walks
#  away (both zoom out + blur), on "miss" Yulan turns her back on him.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_welcome_committee_mug (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ finola = Person["finola_ryan"]
    $ yulan = Person["yulan_chen"]
    $ yulan_thawed = get_value("yulan_thawed", 0, **kwargs) == 1

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/teacher 1 1 0.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "You come off a class into the staff room and there's a full mug waiting in the middle of the circle, steam still rising off it, like it grew there overnight."
    # Yulan already at the edge of the circle; Finola gets shoved forward into frame.
    $ yulan.register_paperdoll(behind = True)
    $ finola.register_paperdoll()
    $ yulan.display(PDAImage(pose = "34", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 1.0))
    $ finola.display(PDAImage(pose = "12", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAPreset("close_body_left", duration = 0.0), PDAMove(alignX = "-0.15"))
    $ finola.display(PDAMove(alignX = "+0.15", duration = 0.3))
    $ finola.display(PDAPause(0.3))
    $ finola.display(PDAShake(0.2, 4))
    subtitles "Finola Ryan has very clearly been pushed to the front. She's holding the mug in both hands, and she's gone a bit pink."
    $ finola.display(PDAImage(mouth = "open"))
    finola.say "Um. Right. The others— we wanted to— I said I'd do this bit."
    $ finola.display(PDAImage(pose = "20", mood = "happy", mouth = "open", look = "follow"))
    finola.say "To your first proper week, headmaster. And to the rest of it. Hopefully."
    $ finola.display(PDAImage(pose = "14", mood = "happy", mouth = "open", look = "avert"))
    finola.say "...Sorry, it sounded much better in my head."
    $ finola.display(PDAImage(pose = "12", mouth = "closed"))
    if yulan_thawed:
        $ yulan.display(PDAImage(mouth = "open"))
        yulan.say "...It's a decent outline he's running, for what it's worth. Don't let it go to his head."
        $ yulan.display(PDAImage(mouth = "closed"))
        $ finola.display(PDAImage(mood = "happy", look = "avert"))
        headmaster.think "Yulan. Saying something almost kind. Out loud, in front of people."
        headmaster.think "...'Don't let it go to his head.' From her, that's practically a hug."
    else:
        $ yulan.display(PDAImage(look = "follow"))
        yulan.say "..."
        $ yulan.display(PDAImage(look = "avert"))
        headmaster.think "Nothing from Yulan. ...But she's here, in the circle. Last month she'd have found somewhere else to be."
    $ finola.display(PDAImage(pose = "12", mood = "happy", mouth = "closed", look = "follow"))

    $ call_custom_menu_with_text("Finola's got the mug half-raised, waiting on you.", character.subtitles, False,
        MenuElement("warm", "Take the toast properly", EventEffect("nm_welcome_committee_mug.warm")),
        MenuElement("brief", "Thank her, keep it short", EventEffect("nm_welcome_committee_mug.brief")),
        MenuElement("miss", "Bury yourself in paperwork", EventEffect("nm_welcome_committee_mug.miss")),
    **kwargs)

label .warm (**kwargs):
    $ finola = Person["finola_ryan"]
    $ yulan = Person["yulan_chen"]

    headmaster "I'll take that toast, gladly. Thank you — all of you. It's been a long few weeks to get to a mug in a circle."
    $ finola.display(PDAImage(pose = "31", mood = "shining", mouth = "open", look = "follow"))
    finola.say "Oh, good. Oh, thank goodness. I was so worried you'd just say 'noted' or something."
    $ finola.display(PDAImage(mouth = "closed"))
    $ yulan.display(PDAImage(mood = "neutral", mouth = "open", look = "avert"))
    yulan.say "...Hmph."
    # The smile he's betting the office on.
    $ yulan.display(PDAImage(mood = "happy", mouth = "closed"))
    headmaster.think "There was a smile behind that 'hmph'. I'd bet the office on it."

    $ situation_manager.apply_progress_change("situation:new_management:main", 6)
    call change_stats_with_modifier(happiness=MEDIUM, reputation=SMALL, charm=SMALL) from _nm_wc_mug_warm
    $ end_event('new_daytime', **kwargs)

label .brief (**kwargs):
    $ finola = Person["finola_ryan"]
    $ yulan = Person["yulan_chen"]

    headmaster "Thank you, Finola — truly. I've got papers with my name on them shouting from the office, though."
    $ finola.display(PDAImage(pose = "14", mood = "neutral", mouth = "open", look = "avert"))
    finola.say "Oh— of course, yes. Sorry."
    $ finola.display(PDAImage(pose = "12", mood = "happy", mouth = "open", look = "follow"))
    finola.say "We'll, um. Keep it warm. For next time."
    # He walks away; the circle shrinks behind him.
    $ finola.display(PDAImage(mouth = "closed"), PDAMove(zoom = "-0.4", duration = 1.2))
    $ yulan.display(PDAMove(zoom = "-0.4", duration = 1.2))
    $ yulan.display(PDAPause(1.2))
    $ finola.display(PDABlur(2.0, 0.6))
    $ yulan.display(PDABlur(2.0, 0.6))
    headmaster.think "There was a chair free at that table. I could have sat in it for ten minutes."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL, happiness=TINY) from _nm_wc_mug_brief
    $ end_event('new_daytime', **kwargs)

label .miss (**kwargs):
    $ finola = Person["finola_ryan"]
    $ yulan = Person["yulan_chen"]

    $ finola.display(PDAImage(pose = "12", mood = "sad", mouth = "closed", look = "avert"))
    $ yulan.display(PDAImage(pose = "34", mood = "suspicious", mouth = "closed", look = "follow"))
    subtitles "You make a show of a stack of forms and don't look up. The mug lowers, quietly, without a clink. Someone changes the subject to spare you."
    $ finola.display(PDAImage(pose = "14", mood = "sad", mouth = "open", look = "avert"))
    finola.say "...Oh. Sorry. You're busy, of course you are. Sorry."
    $ finola.display(PDAImage(pose = "13", mouth = "closed"))
    $ yulan.display(PDAImage(look = "avert"), PDAFlip(False, 0.4))
    headmaster.think "She practised that toast. I could tell. And I hid behind a stack of forms."

    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(happiness=DEC_TINY) from _nm_wc_mug_miss
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_welcome_committee_plaque ══════════════════════════════════════
#  At the office. The engraved brass nameplate has finally arrived, packed in a crate
#  of straw — the headmaster's name cut into it and, this time, spelled right. Emiko is
#  there and they share a warm moment over it; he can hang it now, taking the old one
#  down for good. (Payoff to the wrong-nameplate scene at the very start.)
#
#  Wired: one image via show_pattern("main"); Emiko (level 5) paperdoll over the blurred
#  office/secretary background. On "real" the scene moves to the office door (blurred
#  callback to the nm_ghost_office_nameplate door art) for the hanging sequence.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_welcome_committee_plaque (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ door_claimed = get_value("door_claimed", 0, **kwargs) == 1

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/secretary 5 1 0.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "The crate's finally here. Inside, packed in straw like something precious, is a slab of engraved brass — your name cut deep, and this time spelled exactly right."
    # She's been bent over the crate right beside him.
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "9", outfit = "uniform", level = 5, mood = "happy", mouth = "closed", look = "avert"),
        PDAPreset("close_body_center", duration = 0.0))
    subtitles "You realise you've been standing over it a beat too long. So, you notice, has Emiko."
    $ emiko.display(PDAImage(pose = "2", mood = "shining", mouth = "open", look = "follow"))
    emiko.say "Heh. You're staring."
    if door_claimed:
        $ emiko.display(PDAImage(pose = "21", mood = "happy", mouth = "open", look = "follow"))
        emiko.say "Told you it'd come. Weeks of 'in process', and here it is. I'm framing the delivery note."
    else:
        $ emiko.display(PDAImage(pose = "7", mood = "happy", mouth = "open", look = "avert"))
        emiko.say "Better late than never."
        $ emiko.display(PDAImage(pose = "1", mood = "happy", mouth = "open", look = "follow"))
        emiko.say "...It's a good door. It's waited long enough."

    if get_value("guided", 0, **kwargs) == 1:
        $ emiko.display(PDAImage(pose = "31", mood = "happy", mouth = "open", look = "avert"))
        emiko.say "Your name. Spelled right, for once. ...Suits the place."
    $ emiko.display(PDAImage(mouth = "closed", look = "follow"))

    $ call_custom_menu_with_text("The brass is heavier than it looks.", character.subtitles, False,
        MenuElement("real", "Hang it now, together", EventEffect("nm_welcome_committee_plaque.real")),
        MenuElement("joke", "Deflect the moment", EventEffect("nm_welcome_committee_plaque.joke")),
    **kwargs)

label .real (**kwargs):

    $ emiko.display(PDAImage(pose = "19", mood = "suprised", mouth = "$", look = "follow"))
    headmaster "Help me hang it. Right now — while the screws are still in the bag and I've still got the nerve."
    $ emiko.display(PDAImage(pose = "31", mood = "shining", mouth = "open", look = "follow"))
    emiko.say "Yes, headmaster."

    # Out to the door — the same door from the very first morning.
    $ paperdoll_manager.set_background("images/events/new_management/nm_ghost_office_nameplate/nm_ghost_office_nameplate $ 0.png", blur = True)
    $ emiko.display(PDAImage(pose = "39", mood = "happy", mouth = "closed", look = "avert"),
        PDAPreset("close_body_right", duration = 1.0))
    $ emiko.display(PDAPause(1.0))
    # Old plate off...
    $ emiko.display(PDAShake(0.3, 5))
    $ emiko.display(PDAPause(0.8))
    # ...new brass on.
    $ emiko.display(PDAShake(0.3, 5))
    $ emiko.display(PDAPause(0.6))
    # Step back beside him to look at it.
    $ emiko.display(PDAImage(pose = "12", look = "avert"), PDAPreset("close_body_center", duration = 0.8))
    subtitles "The old man's plate comes down. The last curl of that taped printout goes in the bin for good. The new brass goes up straight, and catches the hall light like it's been waiting years to."
    $ emiko.display(PDAPreset("upper_body_center", duration = 2.0))
    headmaster.think "My name. Spelled right."
    $ emiko.display(PDAImage(pose = "1", mood = "shining", mouth = "closed", look = "follow"))
    headmaster.think "...It's my room. I think it has been for a while."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY) from _nm_wc_plaque_real
    $ end_event('new_daytime', **kwargs)

label .joke (**kwargs):

    $ emiko.display(PDAImage(pose = "9", mood = "shining", mouth = "closed", look = "follow"))
    headmaster "Don't look at me like that."
    $ emiko.display(PDAImage(pose = "10", mood = "happy", mouth = "open", look = "avert"))
    emiko.say "Like what? I'm admiring the brass."
    $ emiko.display(PDAImage(pose = "21", mood = "neutral", mouth = "open", look = "follow"))
    emiko.say "Purely professional interest in good brass."
    $ emiko.display(PDAImage(pose = "2", mood = "happy", mouth = "closed", look = "avert"))
    headmaster.think "'Purely professional.' Sure."
    headmaster.think "...The plate can wait until tomorrow. If we hang it together today, one of us might end up saying something."

    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(reputation=TINY, happiness=TINY) from _nm_wc_plaque_joke
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_welcome_committee_assembly ════════════════════════════════════
#  Morning assembly in the courtyard. The student line is calm and orderly, everyone
#  finding their places without being herded. Yuriko is there (she quietly organised it
#  if she's on side), and Aona greets the headmaster — by his title now if she's learned
#  his face, otherwise just "sir".
#
#  Wired: one image via show_pattern("main"); Yuriko (left) + Aona (right, behind)
#  paperdolls over the blurred courtyard background. "gentle" pulls back to take in the
#  line, "routine" pans past them as he walks it, "strict" flinches and dims them.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_welcome_committee_assembly (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ yuriko = Person["yuriko_oshima"]
    $ aona = Person["aona_komuro"]
    $ yuriko_ally = get_value("yuriko_ally", 0, **kwargs) == 1
    $ face_known = get_value("face_known", 0, **kwargs) == 1

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "Morning assembly. The courtyard line is quieter than it has any right to be — students finding their places without a single teacher barking them into rows."
    # Both on screen — Yuriko (left), Aona (right, a step back in the line).
    $ aona.register_paperdoll(behind = True)
    $ yuriko.register_paperdoll()
    $ aona.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "happy", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 1.0))
    $ yuriko.display(PDAImage(pose = "12", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAPreset("close_body_left", duration = 0.0))
    if yuriko_ally:
        $ yuriko.display(PDAImage(pose = "34", mouth = "open"))
        yuriko.say "They lined up before I said anything."
        $ yuriko.display(PDAImage(pose = "4", mood = "pout", mouth = "$"))
        yuriko.say "...Fine. I might have mentioned you'd be here. Don't read into it."
        $ yuriko.display(PDAImage(pose = "34", mood = "neutral", mouth = "closed", look = "avert"))
        headmaster.think "The girl with the clipboard. Lining up the whole school for me, and acting like it happened by accident."
    else:
        $ yuriko.display(PDAImage(mouth = "open", look = "follow"))
        yuriko.say "Everyone's in place. Go on, then."
        $ yuriko.display(PDAImage(mouth = "closed"))
    if face_known:
        $ aona.display(PDAImage(pose = "20", mood = "happy", mouth = "open", look = "follow"), PDAMove(alignX = 0.9, duration = 0.4))
        aona.say "Morning, headmaster!"
        $ aona.display(PDAImage(pose = "1", mouth = "closed"))
        headmaster.think "'Morning, headmaster.' From the girl who had me down as the maintenance man."
        headmaster.think "...I'll almost miss that one."
    else:
        $ aona.display(PDAImage(pose = "12", mood = "neutral", mouth = "open", look = "follow"))
        aona.say "Morning, sir."
        $ aona.display(PDAImage(mouth = "closed"))
    $ yuriko.display(PDAImage(mouth = "closed", look = "follow"))
    $ aona.display(PDAImage(look = "follow"))

    $ call_custom_menu_with_text("The whole line is waiting on you.", character.subtitles, False,
        MenuElement("gentle", "Keep it warm and brief", EventEffect("nm_welcome_committee_assembly.gentle")),
        MenuElement("routine", "Let it pass, easy and ordinary", EventEffect("nm_welcome_committee_assembly.routine")),
        MenuElement("strict", "Snap them into line", EventEffect("nm_welcome_committee_assembly.strict")),
    **kwargs)

label .gentle (**kwargs):
    $ yuriko = Person["yuriko_oshima"]
    $ aona = Person["aona_komuro"]

    $ aona.display(PDAImage(mood = "happy", mouth = "closed"))
    headmaster "Morning, everyone. Short brief, then you're off to first period. Thank you for being on time — it doesn't go unnoticed."
    $ yuriko.display(PDAImage(pose = "2", mood = "happy", mouth = "open", look = "avert"))
    yuriko.say "...Don't look so pleased with yourself. They'd have lined up anyway."
    $ yuriko.display(PDAImage(mouth = "closed"))
    headmaster.think "A month ago I couldn't convince a single one of them I worked here."
    # Pull back to take in the whole line.
    $ yuriko.display(PDAMove(zoom = "-0.3", duration = 1.5))
    $ aona.display(PDAMove(zoom = "-0.3", duration = 1.5))
    headmaster.think "...Look at them."

    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(reputation=MEDIUM, education=TINY, happiness=SMALL) from _nm_wc_assy_gentle
    $ end_event('new_daytime', **kwargs)

label .routine (**kwargs):
    $ yuriko = Person["yuriko_oshima"]
    $ aona = Person["aona_komuro"]

    # He walks the line — the camera pans past them.
    $ yuriko.display(PDAImage(look = "avert"), PDAMove(alignX = -1.5, duration = 2.5))
    $ aona.display(PDAImage(look = "avert"), PDAMove(alignX = -1.5, duration = 3.5))
    subtitles "You nod, walk the length of the line once at an easy pace, and hand the morning off to the teachers. Nothing showy. It doesn't need to be."
    headmaster.think "It feels like my courtyard. ...When did that happen?"

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL) from _nm_wc_assy_routine
    $ end_event('new_daytime', **kwargs)

label .strict (**kwargs):
    $ yuriko = Person["yuriko_oshima"]
    $ aona = Person["aona_komuro"]

    headmaster "Silence. Straighten those lines. Now."
    $ yuriko.display(PDAShake(0.2, 4))
    $ aona.display(PDAShake(0.2, 4))
    $ aona.display(PDAPause(0.3))
    $ yuriko.display(PDAImage(pose = "34", mood = "sad", mouth = "closed", look = "avert"), PDAColor("black:0.25", 0.6))
    $ aona.display(PDAImage(pose = "13", mood = "sad", mouth = "closed", look = "avert"), PDAColor("black:0.25", 0.6))
    subtitles "The line snaps tighter on instinct — neater in a heartbeat. Also colder. A few faces close over, the easy morning gone out of them."
    headmaster.think "Neat as anything. And every face in that line just shut."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=SMALL, happiness=DEC_TINY, reputation=TINY) from _nm_wc_assy_strict
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Threshold reactions ---------- #
#######################################

label nm_thresh_emiko_nudge (**kwargs):
    $ begin_event(**kwargs)

    $ paperdoll_manager.set_background("images/background/office building/secretary 5 1 0.webp", blur = True)
    # She walks in from the right and sets the coffee down.
    $ emiko.register_paperdoll(config = {"alignX": 2.5})
    $ emiko.display(PDAImage(pose = "39", outfit = "uniform", level = 5, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body", duration = 0.0), PDAMove(alignX = 2.5))
    $ emiko.display(PDAPreset("close_body_center", duration = 0.8))
    $ emiko.display(PDAPause(0.8))
    $ emiko.display(PDAFlip(False), PDAImage(pose = "12"))
    subtitles "Emiko sets a coffee on your desk. She doesn't say why. She doesn't have to."
    $ emiko.display(PDAImage(pose = "34", mood = "neutral", mouth = "open", look = "follow"))
    emiko.say "The pink slips aren't going anywhere. And neither, at this rate, is your attention."
    $ emiko.display(PDAImage(pose = "21", mood = "suspicious", mouth = "open", look = "follow"))
    emiko.say "Patrol. The desk. A class. The counselling chair."
    # Leans in on "today".
    $ emiko.display(PDAImage(pose = "38"), PDAPreset("upper_body_center", duration = 0.6))
    emiko.say "Pick one the school can actually {i}see{/i} you doing — today."
    $ emiko.display(PDAImage(pose = "34", mood = "neutral", mouth = "closed"), PDAPreset("close_body_center", duration = 0.6))
    headmaster.think "She didn't even raise her voice."
    $ emiko.display(PDAImage(pose = "2", mood = "suspicious", look = "follow"))
    headmaster.think "...She's waiting to see if I'll bother."
    $ end_event('none', **kwargs)
    return

label nm_thresh_district_letter (**kwargs):
    $ begin_event(**kwargs)

    $ paperdoll_manager.set_background("images/background/office building/secretary 5 1 0.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "12", outfit = "uniform", level = 5, mood = "neutral", mouth = "closed", look = "avert"),
        PDAPreset("close_body_center", duration = 0.0))
    subtitles "Emiko is holding an envelope the way you'd hold something that might bite."
    $ emiko.display(PDAImage(mouth = "open"))
    emiko.say "District office. Again. Dressed up as a polite letter — but there are teeth in it."
    # The worry slips through.
    $ emiko.display(PDAImage(pose = "23", mood = "sad", mouth = "open", look = "follow"), PDAPreset("upper_body_center", duration = 1.0))
    emiko.say "One more empty stretch like this and somebody up there stops writing and picks up the phone. For real, this time."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster.think "For a second there she just looked worried. For the school. ...Maybe for me."
    # Professional face back — and gone before he can answer.
    $ emiko.display(PDAImage(pose = "34", mood = "neutral", look = "avert"), PDAPreset("close_body_center", duration = 0.3))
    $ emiko.display(PDAPause(0.6))
    $ emiko.display(PDAImage(pose = "39"), PDAFlip(True, 0.3))
    $ emiko.display(PDAPause(0.3))
    $ emiko.display(PDAMove(alignX = -1.5, duration = 1.2))
    headmaster.think "Then the professional face was back, before I'd thought of a single thing to say."
    $ end_event('none', **kwargs)
    return

label nm_thresh_first_warmth (**kwargs):
    $ begin_event(**kwargs)

    $ paperdoll_manager.set_background("images/background/office building/secretary 5 1 0.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 5, mood = "happy", mouth = "open", look = "avert"),
        PDAPreset("upper_body_center", duration = 0.0))
    emiko.say "...Good luck today."
    # She catches herself.
    $ emiko.display(PDAImage(pose = "14", mouth = "closed", look = "follow"))
    headmaster.think "'Good luck today.' ...I don't think she meant to say that out loud."
    # Half a pace back — secretary again.
    $ emiko.display(PDAImage(pose = "12", mood = "neutral", mouth = "closed", look = "avert"), PDAPreset("close_body_center", duration = 0.4))
    subtitles "Footsteps in the outer office. She straightens, half a pace back, secretary again in the space of a single breath."
    $ emiko.display(PDAImage(mouth = "open", look = "follow"))
    emiko.say "Your nine-thirty's early, headmaster."
    $ end_event('none', **kwargs)
    return

label nm_thresh_yulan_thaw (**kwargs):
    $ begin_event(**kwargs)
    $ yulan = Person["yulan_chen"]

    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True)
    # She steps into his path from the right.
    $ yulan.register_paperdoll(config = {"alignX": 2.5})
    $ yulan.display(PDAImage(pose = "39", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body", duration = 0.0), PDAMove(alignX = 2.5))
    $ yulan.display(PDAPreset("close_body_center", duration = 0.8))
    $ yulan.display(PDAPause(0.8))
    $ yulan.display(PDAFlip(False), PDAImage(pose = "34"))
    subtitles "Yulan stops you between periods. Her folder is closed, for once, tucked under one arm."
    $ yulan.display(PDAImage(mouth = "open"))
    yulan.say "The students are settling. Quietly, but they're settling."
    $ yulan.display(PDAImage(look = "follow"))
    yulan.say "I thought you should hear it from someone who isn't paid to flatter you."
    $ yulan.display(PDAImage(pose = "12", mood = "sad", mouth = "open", look = "avert"), PDAMove(zoom = "+0.2", duration = 1.0))
    yulan.say "...Be patient with the parts of them that still shake. That's all."
    # A curt nod, and she's off down the corridor.
    $ yulan.display(PDAImage(mouth = "closed", look = "follow"))
    $ yulan.display(PDAShake(0.15, 2))
    $ yulan.display(PDAPause(0.4))
    $ yulan.display(PDAImage(pose = "39", mood = "neutral", look = "avert"), PDAFlip(True, 0.3))
    $ yulan.display(PDAPause(0.3))
    $ yulan.display(PDAMove(alignX = -1.5, duration = 1.4))
    headmaster.think "She's been carrying that around for a week. Waiting for the right corridor."
    headmaster.think "...Folder closed, and everything."
    $ set_game_data("nm_yulan_thawed", 1)
    $ end_event('none', **kwargs)
    return

label nm_thresh_adelaide_note (**kwargs):
    $ begin_event(**kwargs)
    $ adelaide = Person["adelaide_hall"]

    $ paperdoll_manager.set_background("images/background/office building/secretary 5 1 0.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "12", outfit = "uniform", level = 5, mood = "happy", mouth = "open", look = "follow"),
        PDAPreset("close_body_center", duration = 0.0))
    emiko.say "Adelaide Hall sent a follow-up. The tone's... warmer than last week's, put it that way."
    $ emiko.display(PDAImage(mood = "neutral", mouth = "closed", look = "avert"))
    subtitles "She reads a line aloud, and for once the PTA doesn't come out sounding like a threat."
    # Adelaide isn't here — it's her letter, in Emiko's voice (so Emiko's mouth is open).
    $ emiko.display(PDAImage(mouth = "open"))
    adelaide.say "{i}If you're still steering the ship — keep her steady. We're watching. Supportively, this time.{/i}"
    $ emiko.display(PDAImage(pose = "34", mood = "happy", mouth = "open", look = "follow"))
    emiko.say "She cares more than she'll ever put in writing."
    $ set_game_data("pta_aware", 1)
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster.think "'Supportively, this time.' The PTA. Supportively."
    $ emiko.display(PDAImage(pose = "1", mood = "shining", look = "avert"))
    headmaster.think "...She didn't call me the new headmaster. When did they stop doing that?"
    $ end_event('none', **kwargs)
    return

label nm_thresh_near_end (**kwargs):
    $ begin_event(**kwargs)
    $ finola = Person["finola_ryan"]

    $ paperdoll_manager.set_background("images/background/office building/f.webp", blur = True)
    # Finola brings the form in and lingers to read it over.
    $ finola.register_paperdoll(config = {"alignX": 2.5})
    $ finola.display(PDAImage(pose = "39", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body", duration = 0.0), PDAMove(alignX = 2.5))
    $ finola.display(PDAPreset("close_body_center", duration = 0.8))
    $ finola.display(PDAPause(0.8))
    $ finola.display(PDAFlip(False), PDAImage(pose = "12"))
    subtitles "A form crosses your desk for signing. The line at the bottom just reads: Headmaster. No 'acting'. No 'interim'. No qualifiers at all."
    $ finola.display(PDAImage(pose = "7", mouth = "open"))
    finola.say "Headmaster."
    $ finola.display(PDAImage(pose = "1", mood = "happy", mouth = "open", look = "follow"))
    finola.say "...Yeah. That sounds about right now, doesn't it."
    $ finola.display(PDAImage(mouth = "closed"))
    headmaster.think "Just 'Headmaster'. No 'acting', no 'interim'."
    # She takes the signed form and goes.
    $ finola.display(PDAImage(pose = "39", look = "avert"), PDAFlip(True, 0.3))
    $ finola.display(PDAPause(0.3))
    $ finola.display(PDAMove(alignX = -1.5, duration = 1.4))
    headmaster.think "...The paperwork worked it out before I did."
    $ end_event('none', **kwargs)
    return

# endregion
#######################################


#######################################
# region Resolutions ------------------ #
#######################################

label new_management_positive_resolve (**kwargs):
    $ begin_event(version = "2", **kwargs)
    $ yulan = Person["yulan_chen"]

    $ change_stat("charm", 5)

    # Fallback bg: always an image before the first text (works before the hero art exists).
    # The hero image carries the opening beat on its own — no paperdoll over it.
    $ paperdoll_manager.set_background("images/background/office building/secretary 5 1 0.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "Two coffees on the desk this morning. Emiko doesn't explain the second one. She doesn't need to anymore."

    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "31", outfit = "uniform", level = 5, mood = "shining", mouth = "open", look = "follow"),
        PDAPreset("close_body_center", duration = 0.0))
    emiko.say "For being patient. And for actually being here. Both."
    $ emiko.display(PDAImage(pose = "2", mood = "happy", mouth = "open", look = "avert"))
    emiko.say "...Don't let it go to your head."

    # Yulan at the doorway: Emiko makes room, Yulan slows to a stop on the right.
    $ emiko.display(PDAImage(mouth = "closed"), PDAPreset("close_body_left", duration = 0.6))
    $ yulan.register_paperdoll(config = {"alignX": 2.5})
    $ yulan.display(PDAImage(pose = "39", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed", look = "avert"),
        PDAFlip(True), PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 2.5))
    $ yulan.display(PDAMove(alignX = 1.1, duration = 1.4))
    $ yulan.display(PDAPause(1.4))
    $ yulan.display(PDAImage(pose = "34"))
    subtitles "Yulan passes the doorway, slows — and, miracle of miracles, stops."
    $ yulan.display(PDAImage(look = "follow"))
    yulan.say "..."
    $ yulan.display(PDAImage(pose = "12", mood = "happy", mouth = "open", look = "follow"))
    yulan.say "Welcome to the job, headmaster. Properly, this time."
    $ yulan.display(PDAImage(mouth = "closed"))
    $ emiko.display(PDAImage(mood = "shining", look = "follow"))
    headmaster.think "Two coffees. And nobody's looking at me like I'm keeping the chair warm for someone else."
    $ emiko.display(PDAMove(zoom = "-0.2", duration = 1.5))
    $ yulan.display(PDAMove(zoom = "-0.2", duration = 1.5))
    headmaster.think "...Their headmaster. Huh."
    $ end_event('none', **kwargs)
    return

label game_over_new_management (**kwargs):
    $ begin_event()

    show screen black_error_screen_text ("")
    nvl clear
    nv_text "In the end, your authority never quite grew a face for anyone to hold onto."
    nv_text "So the school board reached for the explanation that fit the emptiest chair: absence. The new man was simply never really there."
    nv_text "Down in the office, Emiko packs the two coffee cups back into the cupboard — carefully, the way you'd return something that belonged to someone else all along."
    nv_text "She doesn't slam the door on her way out. Somehow that's the part that stays with you."

    $ MainMenu(confirm=False)()

# endregion
#######################################

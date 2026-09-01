init 1 python:
    set_current_mod('base')

    # Threshold reactions are real events (gallery / seen / begin_event), but they
    # are only fired by AutoThreshold EventEffects — not from a map location pool.
    nm_threshold_events = EventStorage("nm_thresholds", "misc")
    nm_threshold_events.add_event(
        Event(2, "nm_thresh_emiko_nudge", override_intro=True, override_location="misc"),
        Event(2, "nm_thresh_district_letter", override_intro=True, override_location="misc"),
        Event(2, "nm_thresh_first_warmth", override_intro=True, override_location="misc"),
        Event(2, "nm_thresh_yulan_thaw", override_intro=True, override_location="misc"),
        Event(2, "nm_thresh_adelaide_note", override_intro=True, override_location="misc"),
        Event(2, "nm_thresh_near_end", override_intro=True, override_location="misc"),
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
        Pattern("main", "images/events/new_management/nm_ghost_office_empty_corridor/nm_ghost_office_empty_corridor 1.webp")))

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

    $ emiko = Person["emiko_langley"]
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
    headmaster_thought "Three weeks now, and I still catch myself slowing down at my own door. His name's the one cut deep into the brass. Mine's the strip of paper somebody taped up and couldn't even be bothered to keep straight."

    if standing <= -18:
        headmaster_thought "I keep waiting for it to start feeling like mine. It doesn't. Most mornings I still feel like I'm covering a shift for a man who's coming back any day now to want his chair."

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
    $ emiko = Person["emiko_langley"]

    $ emiko.display(PDAMove(alignX = 0.5, duration = 1.0))
    headmaster "Then let's stop waiting on it. Chase the plaque today — and make sure they spell me right this time."
    $ emiko.display(PDAImage(pose = "2", mood = "shining", mouth = "open"))
    emiko.say "Finally. Consider it chased. And this—"
    $ image.show(2)
    emiko.say "—goes in the bin before it ends up on somebody's phone."
    $ paperdoll_manager.set_background(image[2], blur = True, **kwargs)
    $ emiko.display(PDAImage(pose = "6", mood = "happy", mouth = "closed"))
    headmaster_thought "There. Torn down. It's a strip of paper in the bin, nothing — but it's my name they'll chase now, spelled right, instead of his that I keep flinching past every morning."

    $ set_game_data("nm_door_claimed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(reputation=TINY, charm=TINY) from _nm_go_np_fix
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .charm_fix (**kwargs):
    $ emiko = Person["emiko_langley"]

    $ emiko.display(PDAMove(alignX = 0.5, duration = 1.0))
    headmaster "Put two names on that requisition. Mine — spelled correctly, in nice big letters — and whoever keeps typing 'in process.'"
    $ emiko.display(PDAImage(pose = "12", mood = "shining", mouth = "open"))
    emiko.say "Ha! I'll cc them a dictionary. Bold it, even."
    $ image.show(3)
    subtitles "She pours a second coffee without being asked and nudges the order form across the desk with one finger."
    headmaster_thought "She poured that second cup without even looking, like she's done it a hundred times. When did that start? I don't know. But God, it's good to have one person in this building already standing in my corner before I've had to ask."

    $ set_game_data("nm_door_claimed", 1)
    $ set_game_data("nm_emiko_close", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=TINY, charm=SMALL, happiness=TINY) from _nm_go_np_charm
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .leave_it (**kwargs):
    $ emiko = Person["emiko_langley"]

    $ emiko.display(PDAMove(alignX = 0.5, duration = 1.0))
    headmaster "Leave it for now. There are bigger fires than a nameplate."
    $ emiko.display(PDAImage(pose = "21", mood = "neutral", mouth = "open"))
    emiko.say "Mm. Your call. Just don't act surprised when the kids keep calling you the wrong thing — they read the door, not the memo."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster_thought "I keep telling myself it's temporary. Emiko's right, though, isn't she — the kids don't read the memo, they read the door. And right now the door says I couldn't be bothered to put my own name on it."

    $ situation_manager.apply_progress_change("situation:new_management:main", 0)
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .walk_away (**kwargs):
    $ emiko = Person["emiko_langley"]

    $ emiko.display(PDAMove(alignX = 0.5, duration = 1.0))
    subtitles "You turn back down the hall, leaving the tape exactly where it is."
    $ emiko.display(PDAImage(pose = "23", mood = "sad", mouth = "closed"))
    emiko.say "...Right. I'll keep chasing it on my own, then."
    headmaster_thought "I should turn round. Say something. She's going to keep chasing that plaque on her own now because I couldn't be bothered to stop walking. God. If I won't even put my name on my own door, why would anyone in here trust me with the room behind it?"

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

    headmaster_thought "There's a headmaster, they're sure of that much. They just haven't worked out he's the bloke standing close enough to hear every word. Three weeks in and I'm still a rumour to my own students."

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
    $ ikushi.display(PDAImage(pose = "8", mood = "shining", mouth = "closed"))
    subtitles "Ikushi turns a laugh into a cough. Aona's ears go bright pink and she suddenly finds her own shoes fascinating."
    headmaster_thought "Poor kid's ears are on fire. She'll be telling this one at lunch for a week — the day she called the headmaster a maintenance man to his face. Let her. If it's the story that finally sticks my face to the title, she can tell it as often as she likes."

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
        PDAImage(pose = "23", mood = "happy"),
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
    $ ikushi.display(PDAImage(mood = "sad", mouth = "open"))
    ikushi.say "...it's got your name on it. Spelled right and everything. Sorry, headmaster."
    $ aona.display(PDAImage(mood = "sad", mouth = "closed"))
    headmaster_thought "Ha. Didn't have to argue a single point. Sent her to read the door and she came back three shades paler than she left. Turns out the brass makes my case better than I ever could standing here."

    $ set_game_data("nm_face_introduced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY) from _nm_go_jan_door
    $ end_event('new_daytime', **kwargs)

label .slip_past (**kwargs):
    # No paperdoll — he keeps walking; they're behind him, not facing him.
    $ image.show(2)
    subtitles "You keep walking, unhurried. Their voices thin out behind you, still arguing about who you are."
    headmaster_thought "No sense making a thing of it. They'll see me tomorrow, and the day after, and the one after that. It sinks in eventually. ...It has to. I don't have a faster way than just turning up until they can't not know me."

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
    headmaster_thought "That shut them up. Look at them — gone stiff, staring at their shoes, just waiting for me to be done and gone. That's not respect on their faces. That's wanting me to leave. Damn it. That is not what I came over here for."

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

    $ emiko = Person["emiko_langley"]
    $ loud_slip = get_value("loud_slip", **kwargs)
    $ standing = get_bar_value("new_management", "main", 0, **kwargs)

    $ paperdoll_manager.set_background("images/background/office building/c teacher.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "35", outfit = "uniform", level = 5), PDAPreset("upper_body"), PDAMove(alignX = -1.5, alignY = -0.3, duration = 0.0))

    subtitles "You dial Emiko from the office line."
    $ emiko.display(PDAImage(mood = "shining", mouth = "open"), PDAMove(alignX = 0.5, duration = 1.0))
    emiko.say "Well. Look who remembers he has a phone."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster_thought "God, that voice. Warm, easy, a little teasing — the one she keeps for when there's nobody in the outer office to overhear it. I don't think she even knows she's got two."
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
    headmaster_thought "She's been carrying half of this herself and never once mentioned it. Least I can do is turn up for the other half. And they do notice the second I walk in — I keep forgetting that showing up is most of the job."

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
    headmaster_thought "She said please. Emiko. She actually said please, and I sat here and made her spell the whole thing out first. ...She's right, though. She's always right about this. Fine — the second we hang up, I go."

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
    headmaster_thought "And that's that. ...There was a gap at the end there, wasn't there — that little pause where she wanted to say something more. And I filled it with 'good, thanks' and hung up. Didn't even hear it until just now."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _nm_go_pl_short
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .distant (**kwargs):
    headmaster "Just making sure the line's working. That's all."
    $ emiko.display(PDAImage(mood = "sad", mouth = "open"))
    emiko.say "...It's working. Line's fine."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster_thought "She reached out and I gave her the phone company. 'Making sure the line works.' God. She's sitting at that desk right now feeling stupid for picking up warm, and I'm the one who did that to her."

    $ situation_manager.apply_progress_change("situation:new_management:main", 0)
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

# endregion ═════════════════════════════════════════════════════════════════════

# ═══ SCENE · nm_ghost_office_empty_corridor ═══════════════════════════════════
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
    $ yulan.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed"),
        PDAPreset("close_body_center", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ yulan.display(PDAPreset("close_body_center", duration = 1.0))
    headmaster "Ms. Chen."
    yulan.say "..."
    subtitles "She doesn't look up. A page turns, unhurried, as if your greeting had been delivered to the wrong desk."

    if face_known:
        $ yulan.display(PDAImage(mood = "neutral", mouth = "open"))
        yulan.say "...Headmaster."
        subtitles "One word — but she said it. The students have started using your name in class, apparently, and things like that climb the stairs eventually."
        headmaster_thought "She used my name. It made it all the way from the courtyard up to the staff corridor without me carrying it a single step. Small thing. But it means the thing's spreading on its own now, and that's new."
    else:
        headmaster_thought "...Right. Loud and clear. Learning her name in a corridor doesn't buy me anything with her — she wants the work to be good, and the manners are just noise. Fair enough."

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

    headmaster "Your work on [folder_topic] — the revisions were solid. Genuinely."
    yulan.say "..."
    $ yulan.display(PDAImage(mood = "neutral", mouth = "open"))
    yulan.say "...Thank you."
    subtitles "Still no eye contact. But the next page turns a little slower than the last one did."
    headmaster_thought "Was that— yeah. That page turned slower than the last one. It's nothing, really, it's a page turning. But from her that's the first inch of ground she's given me, and I'll take an inch."

    $ set_game_data("nm_yulan_thawed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(education=TINY, reputation=TINY) from _nm_go_cor_ack
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

label .shop (**kwargs):
    $ yulan = Person["yulan_chen"]
    $ folder_topic = get_value("folder_topic", **kwargs)

    headmaster "On [folder_topic] — your second section is doing the real work. I'd put it {i}before{/i} the summary, not after. Let the argument land before you tell them what it was."
    subtitles "For the first time, she stops walking. She looks — actually looks — at the page you mean."
    $ yulan.display(PDAImage(mood = "suprised", mouth = "closed"))
    yulan.say "...That is the exact note I'd have made. I simply didn't expect you to have read closely enough to make it."
    $ yulan.display(PDAImage(mood = "neutral", mouth = "closed"))
    headmaster_thought "There it is — she actually looked at me. Try to charm her and it slides straight off; talk about the real work, and know it as well as she does, and she stops walking. So that's how you get to Yulan. Good to know."

    $ set_game_data("nm_yulan_thawed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=SMALL, reputation=TINY) from _nm_go_cor_shop
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

label .greet (**kwargs):
    $ yulan = Person["yulan_chen"]

    headmaster "Good afternoon, Ms. Chen."
    $ yulan.display(PDAImage(mood = "neutral", mouth = "open"))
    yulan.say "Headmaster."
    headmaster_thought "One word, flat as the floor, not a scrap of warmth on it. Still — it's a word. Last week I'd have got a turned page and nothing else, so I'll count it."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

label .force (**kwargs):
    $ yulan = Person["yulan_chen"]

    subtitles "You lengthen your stride and go straight past her. Behind you, a folder snaps shut like a small, final verdict."
    $ yulan.display(PDAImage(mood = "angry", mouth = "closed"))
    headmaster_thought "...I just walked straight past her like she was a coat rack. And that folder snapping shut behind me — that's her filing it away somewhere she won't lose it. Ten seconds, and I've probably set myself back a month with her."

    $ situation_manager.apply_progress_change("situation:new_management:main", -1)
    call change_stats_with_modifier(reputation=DEC_TINY, happiness=DEC_TINY) from _nm_go_cor_force
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

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
#  Wired: one image via show_pattern("main"); Miwa paperdoll over the blurred classroom
#  background; her portrait drains to greyscale for the blank-out beat, then returns to
#  colour.
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
        headmaster_thought "Emiko rang about this one — 'the Igarashi girl, keep half an eye on her.' She never says that about the loud ones. It's always the quiet kid holding herself too still, and she's always right about which one."

    # Withdrawn, not arriving — placed directly, no slide.
    $ miwa.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True)
    $ miwa.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "sad", mouth = "closed"),
        PDAPreset("upper_body_center", duration = 0.0))
    headmaster "Miwa. You still with us?"
    $ miwa.display(PDAImage(mood = "sad", mouth = "open"))
    miwa.say "...I can't remember Tuesday morning. Any of it."
    miwa.say "Everyone keeps saying 'last week' like it's normal, and I just— there's a blank where the whole week's supposed to be."

    # The memory-reach: she tries, and drops out of the room. Portrait greys.
    headmaster "Okay. Don't force it. Just the edges — what's the last thing that's actually {i}there{/i}?"
    $ miwa.display(PDABw(True, duration = 0.6))
    subtitles "For a moment she isn't in the room at all. Her eyes go somewhere the rest of her can't follow."
    subtitles "Something surfaces — [memory_scrap] — and then the grey closes back over it before she can hold on."
    $ miwa.display(PDABw(False, duration = 0.6))
    miwa.say "...sorry. It's like the morning just isn't {i}in{/i} me anymore."

    headmaster_thought "Same gap she had the day the whole wing went strange. That was weeks ago. Weeks — and she's been sitting here with a shut notebook and her hands folded over it, and not one adult in this building thought to just ask the girl if she was all right. God."

    $ call_custom_menu_with_text("Miwa is holding very still, braced to be told she's broken.", character.subtitles, False,
        MenuElement("counsel", "Tell her she isn't broken", EventEffect("nm_potion_hangover_miwa.counsel")),
        MenuElement("structure", "Give her one small thing to do", EventEffect("nm_potion_hangover_miwa.structure")),
        MenuElement("press", "Push her to remember", EventEffect("nm_potion_hangover_miwa.press")),
    **kwargs)

label .counsel (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    headmaster "Listen to me. You're not broken, and you're not in trouble. Something scrambled that morning for a lot of people — you're just the only one honest enough to say the page came back blank."
    $ miwa.display(PDAImage(mood = "suprised", mouth = "open"))
    miwa.say "...I'm not the only one?"
    headmaster "Not even close. Come by the office whenever you're ready — no quiz, no notes. A chair, and someone who takes it seriously."
    $ miwa.display(PDAImage(mood = "happy", mouth = "closed"))
    miwa.say "Okay. ...Okay. Thank you."
    subtitles "She opens the notebook at last. The page is still empty — but she stops standing guard over it."

    $ set_game_data("nm_miwa_helped", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(happiness=SMALL, reputation=TINY) from _nm_ph_miwa_counsel
    $ miwa.clear_display()
    $ end_event('new_daytime', **kwargs)

label .structure (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    headmaster "Here's the whole assignment. Write down what you {i}do{/i} have — even if it starts at lunch. We'll look at it together after class. Tuesday can stay lost for today."
    $ miwa.display(PDAImage(mood = "neutral", mouth = "open"))
    miwa.say "Just... the parts that are there? And check later?"
    headmaster "Just the parts that are there. That's it."
    $ miwa.display(PDAImage(mood = "neutral", mouth = "closed"))
    subtitles "She uncaps a pen. It isn't much — but it's the first thing all day with edges she can actually hold onto."

    $ set_game_data("nm_miwa_helped", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(happiness=TINY, education=TINY) from _nm_ph_miwa_structure
    $ miwa.clear_display()
    $ end_event('new_daytime', **kwargs)

label .press (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    headmaster "Try harder, Miwa. Something has to be in there — a smell, a voice, anything. Concentrate."
    $ miwa.display(PDAImage(mood = "sad", mouth = "open"))
    miwa.say "I {i}am{/i} — I told you, I can't—"
    $ miwa.display(PDAImage(mood = "angry", mouth = "closed"))
    subtitles "Her hands close over the notebook again. Whatever door had cracked open just quietly latched shut."
    headmaster_thought "I leaned on her and she shut like a book. Of course she did — there's nothing down there for her to reach, and me standing over her demanding it just makes the empty spot feel bigger to her. Well done. Really."

    $ situation_manager.apply_progress_change("situation:new_management:main", -2)
    call change_stats_with_modifier(happiness=DEC_MEDIUM, reputation=DEC_TINY) from _nm_ph_miwa_press
    $ miwa.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_potion_hangover_lily ══════════════════════════════════════════
#  The counselling office. Lily Anderson (a teacher) turns up without an appointment,
#  hovering in the doorway, apologetic and half-ready to leave. She sits; when she sets
#  her coffee mug down it rattles once against the saucer. Shaken, she asks the
#  headmaster if last week was real. What specifically unnerved her varies (<unnerved>).
#
#  Wired: one image via show_pattern("main"); Lily paperdoll over the blurred
#  teacher-office background.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_potion_hangover_lily (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ lily = Person["lily_anderson"]
    $ unnerved = get_value("unnerved", **kwargs)
    $ emiko_close = get_value("emiko_close", 0, **kwargs) == 1

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/teacher 1 1 0.webp", blur = True)
    subtitles "A knock — too soft to be official. Lily Anderson is already half-turned back toward the corridor by the time you look up."
    $ lily.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/teacher 1 1 0.webp", blur = True)
    $ lily.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "sad", mouth = "open"),
        PDAPreset("upper_body", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ lily.display(PDAPreset("upper_body_center", duration = 0.4))
    lily.say "I— sorry. This is silly, you're busy, I shouldn't have—"
    headmaster "Ms. Anderson. Sit. The coffee's already poured."

    # The tell.
    $ show_pattern("main", **kwargs)
    subtitles "She sits. When she sets her mug down it rattles once against the saucer — a small, betraying sound she pretends not to hear."
    $ lily.display(PDAImage(mood = "sad", mouth = "open"))
    lily.say "Was last week... {i}real{/i}? I keep teaching like nothing happened, and [unnerved], and I—"
    lily.say "I don't want a diagnosis. I want one sane person to say it out loud with me so I know I haven't come unstitched. Not the staffroom. Not gossip. You."

    headmaster_thought "God, she's actually shaking. She didn't come here to gossip — she came because she needs one person to tell her she isn't cracking up. I can do that much. Just say it straight, don't dress it up, don't make it any stranger than it already is for her."

    if get_value("guided", 0, **kwargs) == 1:
        $ lily.display(PDAImage(mood = "neutral", mouth = "open"))
        lily.say "The girls settle the instant someone actually looks {i}at{/i} them instead of past them. I've been meaning to say."

    $ call_custom_menu_with_text("Lily has both hands around the mug now, waiting.", character.subtitles, False,
        MenuElement("sit", "Say it out loud with her", EventEffect("nm_potion_hangover_lily.sit")),
        MenuElement("loop_in", "Put Emiko's record in her hands", EventEffect("nm_potion_hangover_lily.loop_in"), emiko_close),
        MenuElement("maybe", "Offer a careful maybe", EventEffect("nm_potion_hangover_lily.maybe")),
        MenuElement("deflect", "Wave it off — blame the coffee", EventEffect("nm_potion_hangover_lily.deflect")),
    **kwargs)

label .sit (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "Then here it is, out loud: something happened last week. You're not imagining it, and you're not fragile for being the one who noticed."
    $ lily.display(PDAImage(mood = "suprised", mouth = "open"))
    lily.say "..."
    $ lily.display(PDAImage(mood = "happy", mouth = "closed"))
    lily.say "Thank you. God — that's all it— I can go back to third period now. I actually think I can."
    subtitles "The mug doesn't rattle when she lifts it this time. She just looks tired, and a great deal lighter for it."
    headmaster_thought "That was all she wanted. Not a fix, not a plan — just one other voice in the room saying yes, it was real, you're not mad. Look at her, sitting up straight again. Her whole set of shoulders came down an inch."

    $ set_game_data("nm_lily_witnessed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(happiness=MEDIUM, reputation=SMALL) from _nm_ph_lily_sit
    $ lily.clear_display()
    $ end_event('new_daytime', **kwargs)

label .loop_in (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "You're not imagining it — and you don't have to take just my word for it, either."
    subtitles "You slide a thin folder across: Emiko's quiet log of the week nobody will discuss. Dates. A line about the smell. Corroboration, in a second person's handwriting."
    $ lily.display(PDAImage(mood = "suprised", mouth = "open"))
    lily.say "...so it {i}is{/i} written down. Somewhere real. I'm not the only one who thought to."
    $ lily.display(PDAImage(mood = "happy", mouth = "closed"))
    lily.say "That helps more than you know. Thank you — both of you."
    headmaster_thought "Emiko won't mind me handing over the file, not for this. Saying I believe her is one thing — but letting her hold it, dates and all, in someone else's handwriting? Now it isn't just my word propping her up. There's something solid under her feet."

    $ set_game_data("nm_lily_witnessed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(happiness=MEDIUM, reputation=SMALL, education=TINY) from _nm_ph_lily_loop
    $ lily.clear_display()
    $ end_event('new_daytime', **kwargs)

label .maybe (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "Maybe it was real. Maybe your body's still catching up on something. I won't pretend to know which — but come back Thursday, same time, and we'll keep a proper eye on it together."
    $ lily.display(PDAImage(mood = "neutral", mouth = "open"))
    lily.say "Thursday. All right. That's... something to hold onto, at least."
    headmaster_thought "It's not much of an answer and we both know it. But it's a day on the calendar with my name next to it, and sometimes that's the whole thing people need — somewhere to aim for. Maybe it gets her to Thursday. Maybe that's enough for now."

    $ set_game_data("nm_lily_witnessed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(happiness=SMALL) from _nm_ph_lily_maybe
    $ lily.clear_display()
    $ end_event('new_daytime', **kwargs)

label .deflect (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "Ah — stress does funny things to all of us. Honestly, it's probably just the coffee."
    $ lily.display(PDAImage(mood = "sad", mouth = "closed"))
    lily.say "...Right. Of course. The coffee."
    subtitles "She picks the mug back up. It's steady now — but only because she's holding it too tightly to let it shake."
    headmaster_thought "...why did I say that. Blame the coffee. She spent all morning working up the nerve to ask me one honest question and I handed her a punchline. Look at her holding that mug so tight it can't shake. She's not coming back to this office. I wouldn't."

    $ situation_manager.apply_progress_change("situation:new_management:main", 0)
    call change_stats_with_modifier(happiness=DEC_SMALL) from _nm_ph_lily_deflect
    $ lily.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_potion_hangover_vial ══════════════════════════════════════════
#  The courtyard, behind the bike rack. Alone, the headmaster finds a broken green
#  vial, still sticky at the neck. Its detail varies (<residue_detail>). The sweet
#  smell off it throws him into a brief flashback of the same smell in a school
#  corridor last Tuesday, students moving oddly — then he's back at the bike rack. If
#  he bags it and phones Emiko, it cuts briefly to her at her desk.
#
#  Wired: one image via show_pattern("main"); the flashback is an existing corridor
#  background shown in greyscale; on "bag", a brief Emiko paperdoll over the office bg.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_potion_hangover_vial (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ residue_detail = get_value("residue_detail", **kwargs)

    # The find — object beat, scene image, no one else out here.
    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "Behind the bike rack, something small catches the light: a broken vial, green glass gone cloudy, the neck still sticky where it snapped clean off."
    subtitles "You crouch. Up close there's [residue_detail]."
    headmaster_thought "So it never actually stopped. It just got quiet enough that nobody had to look straight at it — me most of all. It's been out here the whole time, behind the bike racks, waiting for somebody to bother crouching down."

    # The smell triggers the flashback — existing corridor bg, blurred and drained.
    subtitles "Then the smell reaches you — sweet, cloying, sitting at the back of the throat — and all at once you aren't behind the bike rack at all."
    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True, bw = True)
    subtitles "{i}Last Tuesday. That same corridor-sweetness hanging in the air. A whole wing of students moving a half-second out of step with themselves, and not one of them able to say why.{/i}"
    headmaster_thought "That smell. It's the same one — not close, the same. This stuff's been through the school before, a whole corridor of it, and every one of us just breathed it in and walked on like nothing was wrong with the day."
    $ paperdoll_manager.hide_background()
    subtitles "You blink the corridor away. Just the bike rack again. Just the glass, and whatever's still clinging to it."

    $ call_custom_menu_with_text("The vial's still there, catching the light. Someone will kick it into a drain if you don't move first.", character.subtitles, False,
        MenuElement("bag", "Bag it and call Emiko", EventEffect("nm_potion_hangover_vial.bag")),
        MenuElement("note", "Log it quietly", EventEffect("nm_potion_hangover_vial.note")),
        MenuElement("ignore", "Leave it where it is", EventEffect("nm_potion_hangover_vial.ignore")),
    **kwargs)

label .bag (**kwargs):
    $ emiko = Person["emiko_langley"]

    subtitles "You fold the glass into a handkerchief, corner by corner, and dial the office."
    $ emiko.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "suspicious", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    emiko.say "Green glass. Sweet-smelling."
    headmaster "...I didn't say what colour it was."
    $ emiko.display(PDAImage(mood = "neutral", mouth = "closed"))
    emiko.say "Bring it straight up. Back stairs, not the courtyard. And for heaven's sake don't let a student get a look at it."
    headmaster_thought "She named the colour before I did. Didn't even blink at it. ...How long has she known to expect one of these to turn up? And why's it me she's telling to use the back stairs, and not the district?"

    $ set_game_data("nm_vial_traced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=TINY, reputation=TINY) from _nm_ph_vial_bag
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .note (**kwargs):
    subtitles "You sketch the spot in your pocket notebook — distance from the rack, the angle of the light — and nudge a fallen leaf over the smear with your shoe."
    headmaster_thought "There. Down on paper, leaf nudged over the smear, out of sight for now. It's not a fire yet. But if it turns into one, at least there's a date in my own handwriting from before anyone starts swearing it never happened."

    $ set_game_data("nm_vial_traced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(education=TINY) from _nm_ph_vial_note
    $ end_event('new_daytime', **kwargs)

label .ignore (**kwargs):
    subtitles "You straighten up and walk on. The sweet smell trails you for three steps, then the wind takes it and the courtyard is only a courtyard again."
    headmaster_thought "...and I'm just going to walk on. Right. Except pretending I didn't see it is still a choice I'm making, isn't it. Keep making it and one day it's not my call anymore — it's somebody upstairs deciding what happens to this place, and I won't like their answer."

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
#  courtyard background.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_testing_the_waters_clipboard (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ yuriko = Person["yuriko_oshima"]
    $ grey_area = get_value("grey_area", **kwargs)

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "You've barely cleared the courtyard arch before Yuriko Oshima steps neatly into your path, clipboard already uncapped. This was planned."
    $ yuriko.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ yuriko.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "neutral", mouth = "open"),
        PDAPreset("upper_body", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ yuriko.display(PDAPreset("upper_body_center", duration = 0.4))
    yuriko.say "Headmaster. A few quick ones, if you don't mind. Grey areas, mostly."
    $ yuriko.display(PDAImage(mood = "suspicious", mouth = "open"))
    yuriko.say "Top of the list: [grey_area]. Officially. On the record."
    headmaster_thought "That pen's not taking notes, it's taking down law. Whatever I say standing here in the courtyard gets quoted back at me by every year group before lunch. Better get it right the first time — there won't be a quiet correction later."

    $ high_charm = get_stat_value("charm", [20, 100], **kwargs) >= 20

    $ call_custom_menu_with_text("The pen is hovering.", character.subtitles, False,
        MenuElement("precise", "Give her a clean, clear answer", EventEffect("nm_testing_the_waters_clipboard.precise")),
        MenuElement("turnaround", "Turn it around — ask what they assume", EventEffect("nm_testing_the_waters_clipboard.turnaround"), high_charm),
        MenuElement("hedge", "Duck it — 'case by case'", EventEffect("nm_testing_the_waters_clipboard.hedge")),
    **kwargs)

label .precise (**kwargs):
    $ yuriko = Person["yuriko_oshima"]

    headmaster "On the record, then. Uniform's optional off campus — neat if you're representing us. Phones, free periods only, on silent. No PDA on school grounds. Simple as that."
    $ yuriko.display(PDAImage(mood = "neutral", mouth = "closed"))
    subtitles "The pen moves fast — three clean lines, underlined once each. The corner of her mouth does something that isn't quite a smile."
    yuriko.say "Clear. That's... refreshingly clear, actually."
    headmaster_thought "Good. If it's going to travel anyway, let it travel in my own words — clean and clear — and not some garbled version half-invented in a stairwell. Better she carries the real thing."

    $ set_game_data("nm_yuriko_ally", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, education=TINY) from _nm_tw_clip_precise
    $ yuriko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .turnaround (**kwargs):
    $ yuriko = Person["yuriko_oshima"]

    headmaster "Before I answer — what do the students already think the rule is? You'd know better than the handbook does."
    $ yuriko.display(PDAImage(mood = "suprised", mouth = "open"))
    yuriko.say "...huh. Nobody's ever asked me that. Honestly? They assume the sensible version. It's only the grey bits they push at."
    headmaster "Then let's make the sensible version the official one — and you get to tell them it came from asking you, not guessing."
    $ yuriko.display(PDAImage(mood = "happy", mouth = "closed"))
    yuriko.say "...I can work with that. I'll pass it on. Properly."
    headmaster_thought "She came out here to pin me down and she's leaving as my messenger, telling herself it was her idea. Honestly? Let her have it. I'll trade a little credit for a student rep on my side any day of the week."

    $ set_game_data("nm_yuriko_ally", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL, charm=SMALL) from _nm_tw_clip_turn
    $ yuriko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .hedge (**kwargs):
    $ yuriko = Person["yuriko_oshima"]

    headmaster "It, ah— depends. Case by case, really. Let me get back to you on that one."
    $ yuriko.display(PDAImage(mood = "suspicious", mouth = "closed"))
    yuriko.say "So. Un-de-fined."
    subtitles "She writes the word out slowly, larger than the rest, and caps the pen like she's got exactly what she came for."
    headmaster_thought "...I just gave her a blank page with my signature on the bottom. 'Un-de-fined.' She's going to write in whatever suits her and the whole school's going to read it as policy — mine. That's not ducking the question. That's handing her the pen."

    $ situation_manager.apply_progress_change("situation:new_management:main", -3)
    call change_stats_with_modifier(reputation=DEC_SMALL) from _nm_tw_clip_hedge
    $ yuriko.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_testing_the_waters_memo ═══════════════════════════════════════
#  At the headmaster's desk. A blank school-wide memo form sits squared on the blotter
#  — Emiko left it for him to write the school's first message from him, in his own
#  words. Mostly he's alone with the form; Emiko steps in only briefly (under Guided)
#  to nudge him, then he writes it — well, or blandly.
#
#  Wired: one image via show_pattern("main"); brief Emiko paperdoll over the blurred
#  office/secretary background.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_testing_the_waters_memo (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ emiko = Person["emiko_langley"]

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "A blank school-wide memo form waits on your blotter, edges squared to the wood. You didn't put it there."
    headmaster_thought "This didn't square itself on my blotter by accident. Emiko left it here. First thing the whole school's going to hear straight from me, in my words — and she wants to see which version of me picks up the pen. So do I, if I'm honest with myself."

    if get_value("guided", 0, **kwargs) == 1:
        $ emiko.register_paperdoll()
        $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
        $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "happy", mouth = "open"),
            PDAPreset("upper_body_center", duration = 0.0))
        emiko.say "Template's on the left, your words on the right. ...Go on. I won't read over your shoulder. Much."
        $ emiko.clear_display()

    $ call_custom_menu_with_text("The form is blank. The pen is yours.", character.subtitles, False,
        MenuElement("own", "Write it in your own voice", EventEffect("nm_testing_the_waters_memo.own")),
        MenuElement("vague", "Fill the boxes, say nothing", EventEffect("nm_testing_the_waters_memo.vague")),
    **kwargs)

label .own (**kwargs):
    $ emiko = Person["emiko_langley"]

    subtitles "You write about being present. About office hours that actually mean something. About a door — correctly labelled now — that stays open."
    subtitles "It takes three drafts. The third one finally sounds like a person instead of a form."
    $ emiko.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "shining", mouth = "closed"),
        PDAPreset("upper_body_center", duration = 0.0))
    emiko.say "...Huh. That actually sounds like you. I'll run copies before the last bell."
    headmaster_thought "Three drafts, but there it is. When they read that, they'll hear an actual person sitting in this chair, not a blank office with a letterhead and a signature at the bottom. It sounds like me. Took me long enough to write something that did."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=MEDIUM, education=TINY) from _nm_tw_memo_own
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .vague (**kwargs):
    $ emiko = Person["emiko_langley"]

    subtitles "You tick the required boxes, sign the bottom, and leave the body of it saying almost nothing at all."
    $ emiko.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "neutral", mouth = "closed"),
        PDAPreset("upper_body_center", duration = 0.0))
    emiko.say "Mm. Safe."
    headmaster_thought "'Safe.' She never means safe when she says it in that tone. She means empty, and she's right — I filled a whole page and still managed to say nothing worth reading. She knew I would before I ever picked up the pen."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _nm_tw_memo_vague
    $ emiko.clear_display()
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
#  paperdolls); Aona's paperdoll appears only in the branches where he speaks to her.
#  Background: kiosk/1 1 1.
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
        headmaster_thought "It stuck. A couple of weeks ago she had me down as the maintenance man, and now she's picking my face out of a crowd in the snack queue. That's the whole thing right there — I just had to keep turning up until I was somebody she recognised."
    else:
        bystander.say "Told you it was the headmaster."
        headmaster_thought "And there it is — she's placed me. The face finally caught up with the title, and it happened in the crisps queue of all the places. Not the assembly, not the office. Buying a drink at break. I'll take it wherever it decides to land."

    if snapped:
        subtitles "She drops her voice a notch when she clocks you're in earshot. She hasn't forgotten getting snapped at."

    $ call_custom_menu_with_text("You're three back in the queue — and squarely in the ranking.", character.subtitles, False,
        MenuElement("intervene", "Step in, light and easy", EventEffect("nm_rumors_in_bloom_kiosk.intervene")),
        MenuElement("listen", "Say nothing and listen", EventEffect("nm_rumors_in_bloom_kiosk.listen")),
        MenuElement("break", "Cut it off — 'line's moving'", EventEffect("nm_rumors_in_bloom_kiosk.break")),
    **kwargs)

label .intervene (**kwargs):
    $ aona = Person["aona_komuro"]

    headmaster "If you're going to rank me, at least rank me by the right job. Headmaster. Not a number on your list."
    # He's stepped in and spoken to her → Aona turns to face him; paperdoll fits now.
    $ aona.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/kiosk/1 1 1.webp", blur = True)
    $ aona.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "happy", mouth = "open"),
        PDAPreset("close_body_center", duration = 0.0))
    aona.say "...okay, that's fair. Headmaster. Noted."
    subtitles "The game folds up on its own. The grin doesn't — but now it's pointed with you, not at you."
    headmaster_thought "Didn't have to shut her down at all. I stepped in, took the title and the teasing both, and now she's grinning with me instead of at me. I think I'm finally learning how to handle this one."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY) from _nm_rb_kiosk_intervene
    $ aona.clear_display()
    $ end_event('new_daytime', **kwargs)

label .listen (**kwargs):
    # No paperdoll — he hangs back and overhears; nobody's talking to him.
    subtitles "You stay put and let the queue carry you. The talk washes past — names, small grievances — and then something snags: [rumor]."
    headmaster_thought "This queue's better than any staff meeting for finding out what's actually going on in here. Half of it's nonsense, sure — but that last bit, the thing they're all careful not to say too loud? That one I'm keeping in my back pocket."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _nm_rb_kiosk_listen
    $ end_event('new_daytime', **kwargs)

label .break (**kwargs):
    $ aona = Person["aona_komuro"]

    headmaster "Line's moving. Save the gossip for your own time."
    # He's cut in and addressed her → Aona faces him; paperdoll fits now.
    $ aona.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/kiosk/1 1 1.webp", blur = True)
    $ aona.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "pout", mouth = "closed"),
        PDAPreset("close_body_center", duration = 0.0))
    aona.say "...sheesh. Fine."
    headmaster_thought "And there it goes. I had one opening to be part of it — the headmaster who can take a joke — and I stepped right on it. Back to being the man they lower their voices around. Nice work."

    $ situation_manager.apply_progress_change("situation:new_management:main", -1)
    call change_stats_with_modifier(happiness=DEC_TINY) from _nm_rb_kiosk_break
    $ aona.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_rumors_in_bloom_chalk ═════════════════════════════════════════
#  Behind the bike shed. Someone has chalked a portrait of the headmaster on the brick
#  wall — rough, but flattering. How it flatters him varies (<exaggeration>: a heroic
#  square jaw / oversized shoulders / a little crown). No one is around at first; if he
#  touches the drawing up himself, a student (Aona) catches him at it.
#
#  Wired: one image via show_pattern("main"); on "correct", an Aona paperdoll over the
#  courtyard background.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_rumors_in_bloom_chalk (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ exaggeration = get_value("exaggeration", **kwargs)

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "Behind the bike shed, someone's chalked a portrait onto the brick. It's roughly you — and, weirdly, flattering: [exaggeration]."
    headmaster_thought "A month ago half of them weren't sure I worked here. Now somebody's chalked me up on the brick — and flattering, at that. Whatever I've been doing, it's landing somewhere. They're drawing me in. Literally, apparently."

    $ call_custom_menu_with_text("Nobody's around. Just you and the wall.", character.subtitles, False,
        MenuElement("leave", "Leave it be", EventEffect("nm_rumors_in_bloom_chalk.leave")),
        MenuElement("correct", "Add one small touch of your own", EventEffect("nm_rumors_in_bloom_chalk.correct")),
        MenuElement("erase", "Scrub it off", EventEffect("nm_rumors_in_bloom_chalk.erase")),
    **kwargs)

label .leave (**kwargs):
    subtitles "You leave it be and walk on. Let it keep grinning at the bike racks."
    headmaster_thought "That's a version of me they actually like up there on the wall. Steady, kind, a bit heroic round the jaw. I could do a lot worse than spend the rest of the year trying to be the man in the drawing."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(happiness=TINY, charm=TINY) from _nm_rb_chalk_leave
    $ end_event('new_daytime', **kwargs)

label .correct (**kwargs):
    $ aona = Person["aona_komuro"]

    subtitles "There's a nub of chalk in the dirt. You crouch, soften the jaw a touch, and add the one honest smile-line the artist was too shy to draw."
    subtitles "A footstep scuffs behind you. A student — of course — has caught the headmaster vandalising his own portrait."
    $ aona.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ aona.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "suprised", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    aona.say "...did you just {i}improve{/i} it?"
    headmaster "It needed a smile. Don't tell anyone."
    $ aona.display(PDAImage(mood = "happy", mouth = "closed"))
    headmaster_thought "Well, that's all over the year group by tomorrow — the headmaster who caught someone's chalk drawing of him and made it better instead of scrubbing it off. Let it go round. It's the best rumour I've had since I got here."

    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(charm=SMALL, happiness=TINY) from _nm_rb_chalk_correct
    $ aona.clear_display()
    $ end_event('new_daytime', **kwargs)

label .erase (**kwargs):
    subtitles "You scrub it off with your sleeve until there's nothing but a grey smear and chalk dust on your cuff. The shed goes very quiet."
    headmaster_thought "...chalk dust all down my cuff and a grey smear where a kind thing used to be. Somebody drew me because they liked me, and I rubbed it out like it was a crime scene. That doesn't teach anyone respect. It just teaches them to keep their heads down when I walk past."

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
#  Wired: no establishing image (paperdoll-only); Miwa paperdoll over the blurred
#  school-building background; Zoe leans in from the right under Guided.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_quiet_endorsements_after_bell (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ miwa = Person["miwa_igarashi"]
    $ miwa_helped = get_value("miwa_helped", 0, **kwargs) == 1

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True)
    subtitles "The bell cuts the period short. Bags zip, chairs scrape — and against the tide, Miwa hangs back a second by the door."
    $ miwa.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True)
    $ miwa.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "happy", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    if miwa_helped:
        miwa.say "Um— thanks. For actually taking it seriously. When I couldn't remember. It— it helped, more than I said."
        headmaster_thought "She held back against the whole tide of the class just to say that. No panic this time, no shut notebook — a kid who went out of her way to find me and say thank you. God. That right there is the entire job, and it fits in a doorway."
    else:
        miwa.say "Um— thanks. For not making it weird the other day. When I was all... out of it."
        headmaster_thought "Honestly don't think I did much for her that day. But she's remembered it as a kindness anyway, and she came back to say so. I'll take the credit she's handing me — and try to actually earn it with the next kid who comes in like she did."
    $ miwa.display(PDAImage(mood = "sad", mouth = "open"))
    miwa.say "I— I have to go, I can't stay, but— yeah. Thanks."

    if get_value("guided", 0, **kwargs) == 1:
        $ zoe = Person["zoe_parker"]
        $ zoe.register_paperdoll()
        $ zoe.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "happy", mouth = "open"),
            PDAPreset("close_body_right", duration = 0.4), PDAMove(alignX = 1.1))
        subtitles "Zoe Parker leans out of the gym doorway as she passes, half a grin on."
        zoe.say "Place runs quieter when you actually drop by, y'know. Just saying."
        $ zoe.display(PDAImage(mood = "happy", mouth = "closed"))

    $ call_custom_menu_with_text("Miwa's already half through the door.", character.subtitles, False,
        MenuElement("pace", "Keep it light and let her go", EventEffect("nm_quiet_endorsements_after_bell.pace")),
        MenuElement("followup", "One gentle question before she goes", EventEffect("nm_quiet_endorsements_after_bell.followup")),
        MenuElement("assign", "Remind her not to be late", EventEffect("nm_quiet_endorsements_after_bell.assign")),
    **kwargs)

label .pace (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    headmaster "Go on, you'll be late. Door's open if you ever need it — that's all."
    $ miwa.display(PDAImage(mood = "happy", mouth = "closed"))
    miwa.say "Okay. ...Okay."
    subtitles "And she's gone — quick and light, before the thank-you can curdle into something awkward. Exactly the way she needed it to go."

    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(happiness=MEDIUM, charm=TINY) from _nm_qe_bell_pace
    $ miwa.clear_display()
    $ end_event('new_daytime', **kwargs)

label .followup (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    headmaster "Quick one — sleeping any better these days?"
    $ miwa.display(PDAImage(mood = "neutral", mouth = "open"))
    miwa.say "A bit. ...I'll tell you about it next time. Promise."
    headmaster_thought "'Next time,' she said. She left that door open herself this time — I didn't have to prop it for her. A few weeks ago she couldn't get the words out at all. Now she's promising me a next time. That's new, and it's good."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(happiness=SMALL) from _nm_qe_bell_follow
    $ miwa.clear_display()
    $ end_event('new_daytime', **kwargs)

label .assign (**kwargs):
    $ miwa = Person["miwa_igarashi"]

    headmaster "Good. Now don't be late to your next class."
    $ miwa.display(PDAImage(mood = "sad", mouth = "closed"))
    miwa.say "...yes, sir."
    headmaster_thought "'Yes, sir.' There goes the light right out of her. She worked up the nerve to thank me and I answered with a note about the register. Smooth. Took the one brave thing she managed all day and turned it into a telling-off."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(education=TINY) from _nm_qe_bell_assign
    $ miwa.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_quiet_endorsements_second_coffee ══════════════════════════════
#  The counselling office again, some time later and much calmer. Lily is back for a
#  follow-up — steadier now, here by choice rather than in a panic. When she sets her
#  coffee mug down this time it doesn't rattle; it just sits still. (Bookends her
#  earlier shaken visit.)
#
#  Wired: one image via show_pattern("main"); Lily paperdoll over the blurred
#  teacher-office background.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_quiet_endorsements_second_coffee (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ lily = Person["lily_anderson"]
    $ lily_witnessed = get_value("lily_witnessed", 0, **kwargs) == 1

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/teacher 1 1 0.webp", blur = True)
    subtitles "Second coffee, same desk — but the air in the room has changed. Lighter."
    $ show_pattern("main", **kwargs)
    subtitles "When she sets the mug down, it doesn't rattle. It just sits there, steady, like it never did anything else."
    $ lily.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/teacher 1 1 0.webp", blur = True)
    $ lily.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "happy", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    if lily_witnessed:
        lily.say "I keep coming back to what you did last week. Just — saying it out loud with me. It steadied more than I let on."
        lily.say "I'm not here because I'm falling apart. I'm here because I've decided this chair is safe. That's a different thing entirely."
    else:
        lily.say "We didn't really get to talk properly last time. I wanted to try again, if the offer still stands."
        lily.say "I'm not in crisis. I'd just... like somewhere steady to think out loud. If that's allowed."
    headmaster_thought "She's here on a good day this time, not a bad one — that's the whole tell right there. The office stopped being the door she bolts through in a crisis. It's just a chair she decided she likes sitting in. That took weeks. It was worth every one of them."

    $ call_custom_menu_with_text("She's settled in, in no hurry.", character.subtitles, False,
        MenuElement("attend", "Just be present", EventEffect("nm_quiet_endorsements_second_coffee.attend")),
        MenuElement("summarize", "Listen, then set the next date", EventEffect("nm_quiet_endorsements_second_coffee.summarize")),
        MenuElement("advice", "Hand her some brisk advice", EventEffect("nm_quiet_endorsements_second_coffee.advice")),
    **kwargs)

label .attend (**kwargs):
    $ lily = Person["lily_anderson"]

    subtitles "You don't rush to fill the silences. You let them stretch, and she steps into them when she's ready — which she does, easily now."
    $ lily.display(PDAImage(mood = "happy", mouth = "closed"))
    lily.say "...same time next week?"
    headmaster "Same time."
    headmaster_thought "No breakthrough, no big moment. Just — same time next week, and she means it, and so do I. ...Huh. Somewhere along the line this hour with her stopped being a duty and turned into the part of the day I actually look forward to."

    $ set_game_data("nm_care_channel", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(happiness=MEDIUM, reputation=TINY) from _nm_qe_coffee_attend
    $ lily.clear_display()
    $ end_event('new_daytime', **kwargs)

label .summarize (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "Next Thursday, free period. And if anything spikes before then, put a note through Emiko and I'll make room sooner."
    $ lily.display(PDAImage(mood = "neutral", mouth = "closed"))
    lily.say "Clear. Thank you — it helps, honestly, just knowing the door's got hours on it."

    $ set_game_data("nm_care_channel", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(happiness=SMALL, education=TINY) from _nm_qe_coffee_sum
    $ lily.clear_display()
    $ end_event('new_daytime', **kwargs)

label .advice (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "Sleep schedule, plenty of water, and stop grading past midnight. You'll feel worlds better."
    $ lily.display(PDAImage(mood = "sad", mouth = "closed"))
    lily.say "I... yes. I do know those things."
    headmaster_thought "Water, sleep, stop grading late — I handed her a pamphlet she could've written herself. She only wanted to think out loud in a room with somebody in it. Now she's gone quiet, staring at the floor. Since when do I start fixing people before I've bothered to hear a word they're saying?"

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    $ lily.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_quiet_endorsements_curriculum ═════════════════════════════════
#  At the headmaster's desk. His lesson outline is back in the tray with a small
#  approving pen-tick in the margin. Lily is there and, dryly and a little awkwardly,
#  admits the pacing is "actually better" — praise she plainly hates saying out loud.
#
#  Wired: one image via show_pattern("main"); Lily paperdoll over the blurred
#  office background.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_quiet_endorsements_curriculum (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ lily = Person["lily_anderson"]

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/f.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "Your lesson outline is back in the tray — and there, in the margin of the third block, a single pen-tick. From Lily, that's practically a standing ovation."
    $ lily.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/f.webp", blur = True)
    $ lily.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "neutral", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    lily.say "The pacing on that. It's... actually better. There."
    $ lily.display(PDAImage(mood = "pout", mouth = "closed"))
    lily.say "Don't make me say it twice. It works."
    headmaster_thought "'Actually better.' From anyone else that's nothing. From Lily it's a bouquet with a ribbon on it — she'd sooner grade a hundred essays than say a kind thing to my face, and she just did it, out loud, and hated every second. I'm not going to let on how much it lands."

    $ call_custom_menu_with_text("The tick is still sitting there in the margin.", character.subtitles, False,
        MenuElement("adjust", "Take the note and rebuild the block", EventEffect("nm_quiet_endorsements_curriculum.adjust")),
        MenuElement("credit", "Promise to credit her publicly", EventEffect("nm_quiet_endorsements_curriculum.credit")),
        MenuElement("shrug", "File it and move on", EventEffect("nm_quiet_endorsements_curriculum.shrug")),
    **kwargs)

label .adjust (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "Then I'll rebuild the third block around it. Send me the rest of your notes, if you've got them."
    $ lily.display(PDAImage(mood = "happy", mouth = "closed"))
    lily.say "Already did. Check your tray — under the outline. I don't do things by halves."
    headmaster_thought "Of course the rest of the notes are already in my tray. She wasn't fishing for a thank-you — she was putting better work in front of me and daring me to actually do something with it. All right, Lily. Challenge taken."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(education=MEDIUM, reputation=TINY) from _nm_qe_curr_adjust
    $ lily.clear_display()
    $ end_event('new_daytime', **kwargs)

label .credit (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "At the next staff brief, I'm saying the outline got better because of you. One sentence."
    $ lily.display(PDAImage(mood = "suprised", mouth = "open"))
    lily.say "Please don't make a speech of it."
    headmaster "One sentence. I promise."
    $ lily.display(PDAImage(mood = "pout", mouth = "closed"))
    lily.say "...fine. One. And no adjectives."
    headmaster_thought "Look at her, negotiating the adjectives out of her own praise before I've even said it. She's going to hate standing there while I credit her in front of the staff — and she'll remember it for a year anyway. One plain sentence, no adjectives. Fine. She's earned every second of the squirming."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=SMALL, happiness=TINY, reputation=TINY) from _nm_qe_curr_credit
    $ lily.clear_display()
    $ end_event('new_daytime', **kwargs)

label .shrug (**kwargs):
    $ lily = Person["lily_anderson"]

    $ lily.display(PDAImage(mood = "sad", mouth = "closed"))
    subtitles "You murmur a thanks, file the outline under 'done', and reach for the next form. When you glance up again, she's already gone."
    headmaster_thought "Filed her best work under 'done' without a second look, muttered a thanks I didn't even mean. Glanced up and she was already gone — took the smile out the door with her. That's a woman who won't hand me anything in a hurry again. Can't say I blame her."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(education=TINY) from _nm_qe_curr_shrug
    $ lily.clear_display()
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
#  Wired: one image via show_pattern("main"); Finola (left) + Yulan (right) paperdolls
#  over the blurred staff-room background.
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
    # Both staff on screen — Finola warm on the left, Yulan reserved on the right.
    $ finola.register_paperdoll()
    $ yulan.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/teacher 1 1 0.webp", blur = True)
    $ finola.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "happy", mouth = "open"),
        PDAPreset("close_body_left", duration = 0.0))
    $ yulan.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed"),
        PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 1.0))
    finola.say "There he is. To surviving your first proper week, headmaster — and the best of luck with the rest of the job. God knows you'll need it."
    if yulan_thawed:
        $ yulan.display(PDAImage(mood = "neutral", mouth = "open"))
        yulan.say "...It's a decent outline he's running, for what it's worth. Don't let it go to his head."
        headmaster_thought "Yulan. Saying something almost kind, in the staff room, where people can hear it. It's backhanded, obviously — 'don't let it go to his head' — but a month ago the woman wouldn't slow her stride for me in a corridor. We've come a fair way, the two of us, whether she'd ever admit it or not."
    else:
        yulan.say "..."
        headmaster_thought "Nothing from Yulan, same as always. But she's standing in the circle, isn't she — not out in the corridor finding somewhere else to be. For her, just choosing to be in the room is its own kind of answer."

    $ call_custom_menu_with_text("Finola's got the mug half-raised, waiting on you.", character.subtitles, False,
        MenuElement("warm", "Take the toast properly", EventEffect("nm_welcome_committee_mug.warm")),
        MenuElement("brief", "Thank her, keep it short", EventEffect("nm_welcome_committee_mug.brief")),
        MenuElement("miss", "Bury yourself in paperwork", EventEffect("nm_welcome_committee_mug.miss")),
    **kwargs)

label .warm (**kwargs):
    $ finola = Person["finola_ryan"]
    $ yulan = Person["yulan_chen"]

    headmaster "I'll take that toast, gladly. Thank you — all of you. It's been a long few weeks to get to a mug in a circle."
    $ finola.display(PDAImage(mood = "shining", mouth = "open"))
    finola.say "See? Told you there was a human in there somewhere."
    $ yulan.display(PDAImage(mood = "happy", mouth = "closed"))
    yulan.say "...Hmph."
    headmaster_thought "There was a smile hiding behind that 'hmph.' I'd bet the office on it. Whatever 'the new headmaster' used to mean a month ago — the stranger, the placeholder — it's finally starting to wear off. And for once that's the good kind of wearing off."

    $ situation_manager.apply_progress_change("situation:new_management:main", 6)
    call change_stats_with_modifier(happiness=MEDIUM, reputation=SMALL, charm=SMALL) from _nm_wc_mug_warm
    $ finola.clear_display()
    $ end_event('new_daytime', **kwargs)

label .brief (**kwargs):
    $ finola = Person["finola_ryan"]

    headmaster "Thank you, Finola — truly. I've got papers with my name on them shouting from the office, though."
    $ finola.display(PDAImage(mood = "happy", mouth = "closed"))
    finola.say "Off you pop, then. We'll keep the coffee warm for the next time you surface."
    headmaster_thought "Took the toast, said the right things, kept one foot pointed at the door the whole time. It wasn't a snub, exactly. But there was warmth on that table I could've sat down in for ten minutes, and I chose the paperwork instead. I always seem to choose the paperwork."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL, happiness=TINY) from _nm_wc_mug_brief
    $ finola.clear_display()
    $ end_event('new_daytime', **kwargs)

label .miss (**kwargs):
    $ finola = Person["finola_ryan"]

    subtitles "You make a show of a stack of forms and don't look up. The mug lowers, quietly, without a clink. Someone changes the subject to spare you."
    $ finola.display(PDAImage(mood = "sad", mouth = "closed"))
    finola.say "...Right. Course. Busy man."
    headmaster_thought "They poured a mug and raised it to let me in, and I answered by hiding behind a stack of forms. Standing here acting like I've got somewhere better to be than the one room in this school that just tried to make me welcome. Damn it. They won't say a word about it. They'll just remember."

    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(happiness=DEC_TINY) from _nm_wc_mug_miss
    $ finola.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_welcome_committee_plaque ══════════════════════════════════════
#  At the office. The engraved brass nameplate has finally arrived, packed in a crate
#  of straw — the headmaster's name cut into it and, this time, spelled right. Emiko is
#  there and they share a warm moment over it; he can hang it now, taking the old one
#  down for good. (Payoff to the wrong-nameplate scene at the very start.)
#
#  Wired: one image via show_pattern("main"); Emiko paperdoll over the blurred
#  office/secretary background.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_welcome_committee_plaque (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ emiko = Person["emiko_langley"]
    $ door_claimed = get_value("door_claimed", 0, **kwargs) == 1

    # Fallback bg: always an image before the first text (works before the hero art exists).
    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ show_pattern("main", **kwargs)
    subtitles "The crate's finally here. Inside, packed in straw like something precious, is a slab of engraved brass — your name cut deep, and this time spelled exactly right."
    $ emiko.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "happy", mouth = "closed"),
        PDAPreset("upper_body_center", duration = 0.0))
    subtitles "You realise you've been standing over it a beat too long. So, you notice, has Emiko."
    $ emiko.display(PDAImage(mood = "shining", mouth = "open"))
    emiko.say "Heh. You're staring."
    if door_claimed:
        emiko.say "Told you it'd come. Weeks of 'in process' — and here it is. The door catching up with the man who already decided he owned the room."
    else:
        emiko.say "Better late than never. It's a good door. It only ever needed someone to decide it was theirs."

    if get_value("guided", 0, **kwargs) == 1:
        $ emiko.display(PDAImage(mood = "happy", mouth = "open"))
        emiko.say "Your name. Spelled right, for once. ...Suits the place."

    $ call_custom_menu_with_text("The brass is heavier than it looks.", character.subtitles, False,
        MenuElement("real", "Hang it now, together", EventEffect("nm_welcome_committee_plaque.real")),
        MenuElement("joke", "Deflect the moment", EventEffect("nm_welcome_committee_plaque.joke")),
    **kwargs)

label .real (**kwargs):
    $ emiko = Person["emiko_langley"]

    headmaster "Help me hang it. Right now — while the screws are still in the bag and I've still got the nerve."
    $ emiko.display(PDAImage(mood = "shining", mouth = "closed"))
    emiko.say "Yes, headmaster."
    subtitles "The old man's plate comes down. The last curl of that taped printout goes in the bin for good. The new brass goes up straight, and catches the hall light like it's been waiting years to."
    headmaster_thought "There it is, up straight and catching the hall light. His plate's down, that awful strip of tape's finally in the bin, and my name's cut into the brass where anyone can read it. It's my room. Has been for a while, if I'm honest — took me until right now to actually believe it."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY) from _nm_wc_plaque_real
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .joke (**kwargs):
    $ emiko = Person["emiko_langley"]

    headmaster "Don't look at me like that."
    $ emiko.display(PDAImage(mood = "happy", mouth = "open"))
    emiko.say "Like what? I'm admiring the brass. Purely professional interest in good brass."
    headmaster_thought "'Purely professional interest in good brass.' Sure. We both know it wasn't the brass she was looking at. The plate can wait till tomorrow. Hang it together today and one of us ends up saying the thing out loud — and neither of us is ready for that yet. Tomorrow's kinder to us both."

    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(reputation=TINY, happiness=TINY) from _nm_wc_plaque_joke
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ SCENE · nm_welcome_committee_assembly ════════════════════════════════════
#  Morning assembly in the courtyard. The student line is calm and orderly, everyone
#  finding their places without being herded. Yuriko is there (she quietly organised it
#  if she's on side), and Aona greets the headmaster — by his title now if she's learned
#  his face, otherwise just "sir".
#
#  Wired: one image via show_pattern("main"); Yuriko (left) + Aona (right) paperdolls
#  over the blurred courtyard background.
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
    # Both on screen — Yuriko (left), Aona (right).
    $ yuriko.register_paperdoll()
    $ aona.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ yuriko.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "neutral", mouth = "open"),
        PDAPreset("close_body_left", duration = 0.0))
    $ aona.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "happy", mouth = "closed"),
        PDAPreset("close_body_right", duration = 0.0), PDAMove(alignX = 1.0))
    if yuriko_ally:
        yuriko.say "They were lined up before I said a word. I may have... primed them. Precedents travel fast when they come from the top."
        headmaster_thought "Weeks ago this girl ambushed me with a clipboard to work out whether I was worth anything. Now she's lining the whole school up before I've said a word, telling herself it was her own idea. Best deal I've made since I walked through the gate — and she thinks she got the better end of it."
    else:
        yuriko.say "Everyone's in place. You're on, headmaster."
    if face_known:
        $ aona.display(PDAImage(mood = "happy", mouth = "open"))
        aona.say "Morning, headmaster!"
        headmaster_thought "'Morning, headmaster' — bright as anything, from the exact girl who once told her mate I was the maintenance man. The janitor story's dead and buried at last. Don't think I've ever been so glad to lose a nickname."
    else:
        $ aona.display(PDAImage(mood = "neutral", mouth = "open"))
        aona.say "Morning, sir."

    $ call_custom_menu_with_text("The whole line is waiting on you.", character.subtitles, False,
        MenuElement("gentle", "Keep it warm and brief", EventEffect("nm_welcome_committee_assembly.gentle")),
        MenuElement("routine", "Let it pass, easy and ordinary", EventEffect("nm_welcome_committee_assembly.routine")),
        MenuElement("strict", "Snap them into line", EventEffect("nm_welcome_committee_assembly.strict")),
    **kwargs)

label .gentle (**kwargs):
    $ yuriko = Person["yuriko_oshima"]

    headmaster "Morning, everyone. Short brief, then you're off to first period. Thank you for being on time — it doesn't go unnoticed."
    $ yuriko.display(PDAImage(mood = "happy", mouth = "closed"))
    yuriko.say "...they lined up before I even asked, you know. That's you, that is."
    headmaster_thought "A month ago I couldn't convince one student I even worked here. This morning the whole courtyard fell into line and ran itself, and all I did was show up and mean it. That was the trick the entire time, wasn't it. No speeches. Just being here, and meaning it."

    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(reputation=MEDIUM, education=TINY, happiness=SMALL) from _nm_wc_assy_gentle
    $ yuriko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .routine (**kwargs):
    $ yuriko = Person["yuriko_oshima"]

    $ yuriko.clear_display()
    subtitles "You nod, walk the length of the line once at an easy pace, and hand the morning off to the teachers. Nothing showy. It doesn't need to be."
    headmaster_thought "No speech, no theatre, and no need for any. Just a man walking the length of his own courtyard at an easy pace because he belongs there. Which — somewhere in the last few weeks, without my noticing the day it happened — I actually started to."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL) from _nm_wc_assy_routine
    $ end_event('new_daytime', **kwargs)

label .strict (**kwargs):
    $ yuriko = Person["yuriko_oshima"]

    headmaster "Silence. Straighten those lines. Now."
    $ yuriko.display(PDAImage(mood = "sad", mouth = "closed"))
    subtitles "The line snaps tighter on instinct — neater in a heartbeat. Also colder. A few faces close over, the easy morning gone out of them."
    headmaster_thought "Snapped into line in a heartbeat, neat as you like — and cold with it. Half those faces just closed over the second I raised my voice. I had a warm morning going and I turned it into a parade ground. I knew better, too. Did it anyway."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=SMALL, happiness=DEC_TINY, reputation=TINY) from _nm_wc_assy_strict
    $ yuriko.clear_display()
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Threshold reactions ---------- #
#######################################

label nm_thresh_emiko_nudge (**kwargs):
    $ begin_event(**kwargs)
    $ emiko = Person["emiko_langley"]

    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "neutral", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    subtitles "Emiko sets a coffee on your desk. She doesn't say why. She doesn't have to."
    emiko.say "The pink slips aren't going anywhere. And neither, at this rate, is your attention."
    $ emiko.display(PDAImage(mood = "suspicious", mouth = "open"))
    emiko.say "Patrol. The desk. A class. The counselling chair. Pick one the school can actually {i}see{/i} you doing — today."
    headmaster_thought "Patrol, the desk, a class, the counselling chair — pick one. She didn't raise her voice, didn't scold me, just set the choices down in front of me flat and even, like she was telling me it might rain later. Somehow that lands harder than any telling-off could. She's not angry. She's just waiting to see whether I'll bother."
    $ emiko.clear_display()
    $ end_event('none', **kwargs)
    return

label nm_thresh_district_letter (**kwargs):
    $ begin_event(**kwargs)
    $ emiko = Person["emiko_langley"]

    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "sad", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    subtitles "Emiko is holding an envelope the way you'd hold something that might bite."
    emiko.say "District office. Again. Dressed up as a polite letter — but there are teeth in it."
    emiko.say "One more empty stretch like this and somebody up there stops writing and picks up the phone. For real, this time."
    $ emiko.display(PDAImage(mood = "neutral", mouth = "closed"))
    headmaster_thought "For half a second there the professional face slipped, and underneath it she just looked... worried. For the school. Maybe a little for me. Then it snapped back into place before I'd found a single thing to say — and now I'm sitting here wishing I'd been faster."
    $ emiko.clear_display()
    $ end_event('none', **kwargs)
    return

label nm_thresh_first_warmth (**kwargs):
    $ begin_event(**kwargs)
    $ emiko = Person["emiko_langley"]

    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "happy", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    emiko.say "...Good luck today."
    headmaster_thought "'Good luck today.' Quiet, half to herself, before she quite caught herself doing it. Just three words. But she offered them without me fishing for anything, and from Emiko that's not a small thing at all. I'll be turning them over at nine-thirty."
    subtitles "Footsteps in the outer office. She straightens, half a pace back, secretary again in the space of a single breath."
    $ emiko.display(PDAImage(mood = "neutral", mouth = "open"))
    emiko.say "Your nine-thirty's early, headmaster."
    $ emiko.clear_display()
    $ end_event('none', **kwargs)
    return

label nm_thresh_yulan_thaw (**kwargs):
    $ begin_event(**kwargs)
    $ yulan = Person["yulan_chen"]

    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True)
    $ yulan.register_paperdoll()
    $ yulan.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "neutral", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    subtitles "Yulan stops you between periods. Her folder is closed, for once, tucked under one arm."
    yulan.say "The students are settling. Quietly, but they're settling. I thought you should hear it from someone who isn't paid to flatter you."
    yulan.say "...Be patient with the parts of them that still shake. That's all."
    headmaster_thought "She said it like she'd been carrying the words around for a week, waiting for the right corridor to set them down in. 'Be patient with the parts of them that still shake.' From Yulan — folder closed, actually stopping to talk to me — that's about as close to a hug as I'm ever going to get."
    $ set_game_data("nm_yulan_thawed", 1)
    $ yulan.clear_display()
    $ end_event('none', **kwargs)
    return

label nm_thresh_adelaide_note (**kwargs):
    $ begin_event(**kwargs)
    $ emiko = Person["emiko_langley"]
    $ adelaide = Person["adelaide_hall"]

    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "happy", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    emiko.say "Adelaide Hall sent a follow-up. The tone's... warmer than last week's, put it that way."
    subtitles "She reads a line aloud, and for once the PTA doesn't come out sounding like a threat."
    adelaide.say "{i}If you're still steering the ship — keep her steady. We're watching. Supportively, this time.{/i}"
    $ emiko.display(PDAImage(mood = "neutral", mouth = "closed"))
    emiko.say "She cares more than she'll ever put in writing."
    $ set_game_data("pta_aware", 1)
    headmaster_thought "'Supportively, this time.' The PTA. Being kind, or the closest thing they do to it. And somewhere along the way they quietly stopped putting 'new' in front of my title. I'm just the headmaster to them now. When did that happen? I never felt the day it turned over."
    $ emiko.clear_display()
    $ end_event('none', **kwargs)
    return

label nm_thresh_near_end (**kwargs):
    $ begin_event(**kwargs)
    $ finola = Person["finola_ryan"]

    $ paperdoll_manager.set_background("images/background/office building/f.webp", blur = True)
    subtitles "A form crosses your desk for signing. The line at the bottom just reads: Headmaster. No 'acting'. No 'interim'. No qualifiers at all."
    $ finola.register_paperdoll()
    $ finola.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "happy", mouth = "open"),
        PDAPreset("upper_body_center", duration = 0.0))
    finola.say "Headmaster. ...Yeah. That sounds about right now, doesn't it."
    headmaster_thought "Just 'Headmaster' on the line. No 'acting,' no 'interim,' nothing hedging it. The paperwork worked it out before I did. The plaque, the coffee, the courtyard falling into line — all of it was just the rest of me slowly catching up to a word that had already quietly become true."
    $ finola.clear_display()
    $ end_event('none', **kwargs)
    return

# endregion
#######################################


#######################################
# region Resolutions ------------------ #
#######################################

label new_management_positive_resolve (**kwargs):
    $ emiko = Person["emiko_langley"]
    $ yulan = Person["yulan_chen"]

    $ change_stat("charm", 5)

    $ paperdoll_manager.set_background("images/background/office building/secretary 6 1 0.webp", blur = True)
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "shining", mouth = "closed"),
        PDAPreset("upper_body_center", duration = 0.0))
    subtitles "Two coffees on the desk this morning. Emiko doesn't explain the second one. She doesn't need to anymore."
    $ emiko.display(PDAImage(mood = "happy", mouth = "open"))
    emiko.say "For being patient. And for actually being here. Both. ...Don't let it go to your head."
    subtitles "Yulan passes the doorway, slows — and, miracle of miracles, stops."
    $ yulan.register_paperdoll()
    $ yulan.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "neutral", mouth = "open"),
        PDAPreset("close_body_right", duration = 0.4), PDAMove(alignX = 1.1))
    yulan.say "..."
    $ yulan.display(PDAImage(mood = "happy", mouth = "open"))
    yulan.say "Welcome to the job, headmaster. Properly, this time."
    headmaster_thought "Nobody's looking at me like I'm keeping the seat warm for someone else anymore. Somewhere between that crooked bit of tape on the door and this second cup of coffee I didn't have to ask for, I stopped being the new man they couldn't quite place. I'm the headmaster now. Not just the word on the form. Theirs."
    $ emiko.clear_display()
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

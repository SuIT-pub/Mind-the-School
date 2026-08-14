init 1 python:
    set_current_mod('base')

    # Dummy Event objects so set_event_seen() works for threshold scenes
    # triggered via SituationThreshold EventEffects (not EventStorage).
    Event(3, "nm_thresh_emiko_nudge", register_self=True, override_intro=True)
    Event(3, "nm_thresh_district_letter", register_self=True, override_intro=True)
    Event(3, "nm_thresh_first_warmth", register_self=True, override_intro=True)
    Event(3, "nm_thresh_yulan_thaw", register_self=True, override_intro=True)
    Event(3, "nm_thresh_adelaide_note", register_self=True, override_intro=True)
    Event(3, "nm_thresh_near_end", register_self=True, override_intro=True)

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
        RandomListSelector("wrong_name", "HEADMSTER", "H. MASTAR", "MR. HEADMAN", "THE NEW GUY", "MR. WHATSISNAME"),
        RandomListSelector("plate_note", "in biro", "in fat marker", "on a sticky note", "on printer paper"),
        # Gallery-registered readings: Standing (reactive line) + Charm (gated choice).
        # Key for the bar selector MUST match get_bar_value's composite key.
        SituationBarSelector("situation:new_management:main", "new_management", "main"),
        StatSelector("charm", CHARM, "school", [20, 100]),
        # Scene image for the non-dialogue establishing beat (the door itself).
        # show_pattern() degrades gracefully: nothing shows until the file exists.
        Pattern("bg", "images/background/office building/f.webp"),
        Pattern("main", "images/events/new_management/nm_ghost_office_nameplate/nm_ghost_office_nameplate 1.webp")))
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
        Pattern("main", "images/events/new_management/nm_ghost_office_janitor/nm_ghost_office_janitor 1.webp")))
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
        SituationPoolCondition("new_management", "nm_testing_the_waters")))
    office_building_work_event["reputation"].add_event(Event(
        3,
        "nm_testing_the_waters_memo",
        TimeCondition(weekday="d", daytime="d"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_testing_the_waters")))

    # --- nm_rumors_in_bloom (0 ... +25) ---
    kiosk_events["get_snack"].add_event(Event(
        3,
        "nm_rumors_in_bloom_kiosk",
        OR(TimeCondition(weekday="d", daytime="1,3"), TimeCondition(weekday="w", daytime="4-")),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_rumors_in_bloom")))
    courtyard_events["search"].add_event(Event(
        3,
        "nm_rumors_in_bloom_chalk",
        OR(TimeCondition(daytime="f", weekday="d"), TimeCondition(daytime="d", weekday="w")),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_rumors_in_bloom")))

    # --- nm_quiet_endorsements (+10 ... +30) ---
    sb_events["check_class"].add_event(Event(
        3,
        "nm_quiet_endorsements_after_bell",
        TimeCondition(weekday="d", daytime="c"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_quiet_endorsements")))
    office_building_work_event["counselling"].add_event(Event(
        3,
        "nm_quiet_endorsements_second_coffee",
        TimeCondition(weekday="d", daytime="f"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_quiet_endorsements")))
    office_building_work_event["education"].add_event(Event(
        3,
        "nm_quiet_endorsements_curriculum",
        TimeCondition(weekday="d", daytime="d"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_quiet_endorsements")))

    # --- nm_welcome_committee (+22 ... +40) ---
    sb_events["teach_class"].add_event(Event(
        3,
        "nm_welcome_committee_mug",
        TimeCondition(weekday="d", daytime="c"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_welcome_committee")))
    office_building_events["look_around"].add_event(Event(
        3,
        "nm_welcome_committee_plaque",
        TimeCondition(weekday="d", daytime="f"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_welcome_committee")))
    courtyard_events["patrol"].add_event(Event(
        3,
        "nm_welcome_committee_assembly",
        TimeCondition(weekday="d", daytime="1"),
        LevelCondition("1-", "school"),
        SituationPoolCondition("new_management", "nm_welcome_committee")))


#######################################
# region Ghost Office ----------------- #
#######################################

# ═══ ASSET NOTES · nm_ghost_office_nameplate ═══════════════════════════════════
#  SCENE IMAGE (non-dialogue establishing beat) — WIRED via show_pattern("main"):
#    images/events/new_management/nm_ghost_office_nameplate/nm_ghost_office_nameplate 1.webp
#    Close-up of the office door: dull brass plaque with the OLD headmaster's
#    engraved name, half-covered by a crooked taped printout showing the
#    misspelled <wrong_name>. Cold hall light, one thumbtack askew. Borrowed,
#    provisional. (Add the same path as the event `thumbnail=` once it exists.)
#  DIALOGUE : Emiko via paperdoll over blurred office building/secretary 6 1 0;
#             moods neutral→suspicious→happy(fix)/shining(charm)/pout/sad.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_ghost_office_nameplate (**kwargs):
    $ begin_event(**kwargs)

    $ emiko = Person["emiko_langley"]
    $ wrong_name = get_value("wrong_name", **kwargs)
    $ plate_note = get_value("plate_note", **kwargs)
    # Read Standing through the gallery getter so replays have the value (Events guide §8/§16).
    $ standing = get_bar_value("new_management", "main", 0, **kwargs)

    $ image = convert_pattern("main", **kwargs)

    $ image.show(0)

    subtitles "The office door still carries the old headmaster's name, cut deep into the brass like it means to stay there."
    subtitles "Someone's taped a printout over half of it — your name, [plate_note], spelled {i}[wrong_name]{/i}. It's crooked, and one corner is already peeling loose."
    $ image.show(1)
    headmaster_thought "Three weeks in, and the door still hasn't decided I actually live here."

    if standing <= -18:
        headmaster_thought "I keep waiting to feel like the room is mine. Mostly I feel like I'm covering someone else's shift."

    # Emiko leans in → hand off to conversation (paperdoll over the blurred office).
    $ emiko.register_paperdoll(level = 5)
    $ paperdoll_manager.set_background("bg", blur = True, **kwargs)
    $ emiko.display(PDAImage(pose = "10", outfit = "uniform", level = 5, mood = "shining", mouth = "open"),
        PDAPreset("close_body_center", duration = 0.4)),
    emiko.say "Caught you glaring at it. Don't worry — everyone glares at it."
    $ emiko.display(PDAImage(pose = "34", mood = "neutral", mouth = "open"))
    emiko.say "I put in for the proper plaque a week ago. Every day since, it's been 'in process.' I'm starting to think that's just where brass goes to quietly die."

    # Stat-gated choice: a warmer, better option only unlocks once you've got some charm.
    # Read through the gallery getter so the value replays correctly (Events guide §8/§16).
    $ high_charm = get_stat_value("charm", [20, 100], **kwargs) >= 20

    $ emiko.display(PDAImage(mouth = "closed"))
    $ call_custom_menu_with_text("What do you do with the nameplate?", character.subtitles, False,
        MenuElement("fix", "Pull the printout and ask Emiko to chase the right plaque", EventEffect("nm_ghost_office_nameplate.fix")),
        MenuElement("charm_fix", "Make a joke of it — draft the order with her over a coffee", EventEffect("nm_ghost_office_nameplate.charm_fix"), high_charm),
        MenuElement("leave_it", "Leave the taped printout — temporary is temporary", EventEffect("nm_ghost_office_nameplate.leave_it")),
        MenuElement("walk_away", "Walk away. You'll deal with it later", EventEffect("nm_ghost_office_nameplate.walk_away")),
    **kwargs)

label .fix (**kwargs):
    $ emiko = Person["emiko_langley"]

    headmaster "Then let's stop waiting on it. Chase the plaque today — and make sure they spell me right this time."
    $ emiko.display(PDAImage(pose = "2", mood = "shining", mouth = "open"))
    emiko.say "Finally. Consider it chased. And this—"
    $ image.show(2)
    subtitles "She peels the printout off in one clean strip."
    $ image.show(3)
    emiko.say "—goes in the bin before it ends up on somebody's phone."
    $ emiko.display(PDAImage(pose = "6", mood = "happy", mouth = "closed"))
    headmaster_thought "There — done. Let people read the right name on the way in for once, instead of the last man's."

    $ set_game_data("nm_door_claimed", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(reputation=TINY, charm=TINY) from _nm_go_np_fix
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .charm_fix (**kwargs):
    $ emiko = Person["emiko_langley"]

    headmaster "Put two names on that requisition. Mine — spelled correctly, in nice big letters — and whoever keeps typing 'in process.'"
    $ emiko.display(PDAImage(mood = "shining", mouth = "open"))
    emiko.say "Ha! I'll cc them a dictionary. Bold it, even."
    $ paperdoll_manager.cl
    $ image.show(4)
    subtitles "She pours a second coffee without being asked and nudges the order form across the desk with one finger."
    headmaster_thought "She poured that second cup without even thinking about it. ...When did that start? Whatever it is — I'll take it. God knows I could use someone in my corner."

    $ set_game_data("nm_door_claimed", 1)
    $ set_game_data("nm_emiko_close", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=TINY, charm=SMALL, happiness=TINY) from _nm_go_np_charm
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .leave_it (**kwargs):
    $ emiko = Person["emiko_langley"]

    headmaster "Leave it for now. There are bigger fires than a nameplate."
    $ emiko.display(PDAImage(pose = "21", mood = "neutral", mouth = "open"))
    emiko.say "Mm. Your call. Just don't act surprised when the kids keep calling you the wrong thing — they read the door, not the memo."
    $ emiko.display(PDAImage(mouth = "closed"))
    headmaster_thought "I keep calling it temporary. ...I wonder if anyone else hears it that way — or if they just hear that I couldn't be bothered."

    $ situation_manager.apply_progress_change("situation:new_management:main", 0)
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .walk_away (**kwargs):
    $ emiko = Person["emiko_langley"]

    subtitles "You turn back down the hall, leaving the tape exactly where it is."
    $ emiko.display(PDAImage(pose = "23", mood = "sad", mouth = "closed"))
    emiko.say "...Right. I'll keep chasing it on my own, then."
    headmaster_thought "I should turn around and deal with that. ...I'm not going to, though, am I. And if I won't even claim my own door, why would any of them hand me the room behind it?"

    $ situation_manager.apply_progress_change("situation:new_management:main", -1)
    call change_stats_with_modifier(reputation=DEC_TINY) from _nm_go_np_walk
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ ASSET NOTES · nm_ghost_office_janitor ═════════════════════════════════════
#  SCENE IMAGE (establishing) — WIRED via show_pattern("main"):
#    images/events/new_management/nm_ghost_office_janitor/nm_ghost_office_janitor 1.webp
#    Two girls by the courtyard path glancing sidelong at the headmaster — one
#    smirking, one uncertain; he reads as "staff-adjacent, not staff." Sunlit,
#    gossipy, low-stakes cruelty. (Add as event `thumbnail=` once it exists.)
#  DIALOGUE : Aona via paperdoll over blurred courtyard/1 0 1; neutral→suspicious
#             →happy/suprised/sad. <bystander> (random 3A) speaks one line by name.
#  Selectors: <bystander>, <wrong_role> (mistaken job).
# ═══════════════════════════════════════════════════════════════════════════════
label nm_ghost_office_janitor (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ aona = Person["aona_komuro"]
    $ bystander = get_person_value("bystander", **kwargs)
    $ wrong_role = get_value("wrong_role", **kwargs)

    # Establishing beat: the two girls sizing him up from across the path → scene image.
    $ show_pattern("main", **kwargs)
    subtitles "By the courtyard path, Aona has an audience of exactly one classmate, and she is making the absolute most of it."

    # Hand off to the conversation (paperdoll over the blurred courtyard).
    $ aona.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/courtyard/1 0 1.webp", blur = True)
    $ aona.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "neutral", mouth = "open"),
        PDAPreset("upper_body", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ aona.display(PDAPreset("upper_body_center", duration = 0.4))
    aona.say "—so yeah, there's a new headmaster now. We sat through the whole speech in the gym, remember?"
    $ aona.display(PDAImage(mood = "suspicious", mouth = "open"))
    aona.say "But {i}that{/i} guy? Nah. That's [wrong_role]. Look at the way he walks — that is not a headmaster walk."
    bystander.say "...you sure, though? He kinda looks like the one who gave the speech."
    $ aona.display(PDAImage(mood = "happy", mouth = "open"))
    aona.say "Trust me. That whole assembly was a total blur. Could've been anybody up on that stage."

    headmaster_thought "They know there's a headmaster somewhere out there. They just have no idea he's the man standing three feet away from them."

    # Callback choice: only offered if you already claimed the office door.
    # Read through the gallery getter (paired with the GameDataSelector) so it replays.
    $ door_claimed = get_value("door_claimed", 0, **kwargs) == 1

    $ call_custom_menu_with_text("They're ranking you — three feet away.", character.subtitles, False,
        MenuElement("introduce", "Introduce yourself. Make the title stick to a face", EventEffect("nm_ghost_office_janitor.introduce")),
        MenuElement("door", "Tell them whose office the corner one is — go read the door", EventEffect("nm_ghost_office_janitor.door"), door_claimed),
        MenuElement("slip_past", "Slip past quietly. Let recognition catch up on its own", EventEffect("nm_ghost_office_janitor.slip_past")),
        MenuElement("snap", "Snap at them for gossiping", EventEffect("nm_ghost_office_janitor.snap")),
    **kwargs)

label .introduce (**kwargs):
    $ aona = Person["aona_komuro"]

    headmaster "Good morning. For the record — headmaster. Not [wrong_role]."
    $ aona.display(PDAImage(mood = "suprised", mouth = "open"))
    aona.say "..."
    aona.say "Oh my— you're real. You're an actual person."
    subtitles "Her friend turns a laugh into a cough. Aona's ears go bright pink and she suddenly finds her own shoes fascinating."
    headmaster_thought "Oh, she is going to be telling that one at lunch all week. ...Good. Let them laugh — as long as they finally remember the face."

    $ set_game_data("nm_face_introduced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY, happiness=TINY) from _nm_go_jan_intro
    $ aona.clear_display()
    $ end_event('new_daytime', **kwargs)

label .door (**kwargs):
    $ aona = Person["aona_komuro"]

    headmaster "Corner office, end of that corridor. Go read the door, then come back and tell me who I am. I'll wait."
    $ aona.display(PDAImage(mood = "suprised", mouth = "open"))
    subtitles "Her friend actually takes the dare and jogs off. She comes back a few shades paler and a great deal quieter."
    $ aona.display(PDAImage(mood = "sad", mouth = "closed"))
    aona.say "...it's got your name on it. Spelled right and everything. Sorry, headmaster."
    headmaster_thought "Ha. Didn't have to say a single word. Some days the door does the arguing better than I could."

    $ set_game_data("nm_face_introduced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY) from _nm_go_jan_door
    $ aona.clear_display()
    $ end_event('new_daytime', **kwargs)

label .slip_past (**kwargs):
    $ aona = Person["aona_komuro"]

    subtitles "You keep walking, unhurried. Their voices thin out behind you, still arguing about who you are."
    headmaster_thought "No sense making a scene of it. They'll see me tomorrow, and the day after that. It sinks in eventually... it has to."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _nm_go_jan_slip
    $ aona.clear_display()
    $ end_event('new_daytime', **kwargs)

label .snap (**kwargs):
    $ aona = Person["aona_komuro"]

    headmaster "If you've got time to hand out jobs I don't have, you've got time to be in class."
    $ aona.display(PDAImage(mood = "sad", mouth = "open"))
    aona.say "We— we weren't— sorry."
    headmaster_thought "Well, that shut them up fast. ...Too fast. That was fear, not respect — and it's not what I wanted. Damn it."

    $ set_game_data("nm_snapped", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", -2)
    call change_stats_with_modifier(happiness=DEC_SMALL, reputation=DEC_TINY) from _nm_go_jan_snap
    $ aona.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ ASSET NOTES · nm_ghost_office_private_line ════════════════════════════════
#  SPLIT BACKGROUND (phone call): left half = his end in B/W (abstract "ghost"
#  headmaster), right half = her end in colour. Currently the same office bg
#  (secretary 6 1 0) fills both halves; drop a dedicated headmaster-office bg and
#  swap the left pattern in set_background_split for a true two-room split.
#  DIALOGUE : Emiko via paperdoll positioned in the colour (right) half;
#             happy→neutral (the L5→L1 mask snap)→sad (honest/distant).
#  Selector <loud_slip> drives her line; "honest" choice gated on Standing <= -18.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_ghost_office_private_line (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ emiko = Person["emiko_langley"]
    $ loud_slip = get_value("loud_slip", **kwargs)
    # Read Standing through the gallery getter so replays have the value (Events guide §8/§16).
    $ standing = get_bar_value("new_management", "main", 0, **kwargs)

    # Phone call → split background: his (colourless, abstract) end of the line on
    # the left in b/w, her end on the right in colour. Uses the same office bg for
    # both halves until a dedicated headmaster-office background exists — swap the
    # left pattern then. Split degrades gracefully if either image is missing.
    $ paperdoll_manager.set_background_split(
        "images/background/office building/secretary 6 1 0.webp",
        "images/background/office building/secretary 6 1 0.webp",
        blur = True, bw_left = True)

    subtitles "You dial Emiko from the office line."
    # Emiko sits in the colour (right) half; the greyed left half is his silent end.
    $ emiko.register_paperdoll()
    $ emiko.display(PDAImage(pose = "1", outfit = "uniform", level = 6, mood = "happy", mouth = "open"),
        PDAPreset("upper_body", duration = 0.0),
        PDAMove(alignX = 1.4, duration = 0.0))
    $ emiko.display(PDAMove(alignX = 0.68, duration = 0.4))
    emiko.say "Well. Look who remembers he has a phone."
    headmaster_thought "God, that voice. She only ever lets it out when there's no one else in the room to hear it."
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
    $ deep_hole = standing <= -18

    $ call_custom_menu_with_text("How do you use the call?", character.subtitles, False,
        MenuElement("triage", "Ask her for triage — what needs you today", EventEffect("nm_ghost_office_private_line.triage")),
        MenuElement("honest", "Ask her, off the record, how bad it actually is", EventEffect("nm_ghost_office_private_line.honest"), deep_hole),
        MenuElement("short", "Ask briefly, then accept the short answers", EventEffect("nm_ghost_office_private_line.short")),
        MenuElement("distant", "Keep it distant. Don't pull her into it", EventEffect("nm_ghost_office_private_line.distant")),
    **kwargs)

label .triage (**kwargs):
    $ emiko = Person["emiko_langley"]

    headmaster "Give me whatever can't wait. Parent calls, complaints, anything that's actually on fire."
    $ emiko.display(PDAImage(mood = "neutral", mouth = "closed"))
    emiko.say "Three parents, one teacher with a grievance, and [loud_slip] sitting right on top like it pays rent."
    $ emiko.display(PDAImage(mood = "happy", mouth = "open"))
    emiko.say "I'll sort them and line them up. You just decide who's worth showing your face to."
    headmaster_thought "She's already carrying half of this on her own. Least I can do is turn up for the rest — and they notice the second I do. Funny how that works."

    $ set_game_data("nm_emiko_close", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, education=TINY) from _nm_go_pl_triage
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .honest (**kwargs):
    $ emiko = Person["emiko_langley"]

    headmaster "Emiko. No routing, no softening it. How bad is it, really?"
    subtitles "A pause. When she answers, her voice has dropped low enough that the outer office won't catch a word of it."
    $ emiko.display(PDAImage(mood = "sad", mouth = "open"))
    emiko.say "Bad enough that I've stopped tucking the slips where you won't see them. And [loud_slip]? That one's new. I don't like it."
    $ emiko.display(PDAImage(mood = "neutral", mouth = "closed"))
    emiko.say "It's fixable. But it gets fixed by them {i}seeing{/i} you — not by me quietly plugging the holes. So go do that. Be seen. Please."
    headmaster_thought "No lecture. No 'I told you so.' She just said it, quiet and kind — and it landed like a fist anyway. I almost wish she'd shouted."

    $ set_game_data("nm_emiko_close", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL, happiness=TINY) from _nm_go_pl_honest
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .short (**kwargs):
    $ emiko = Person["emiko_langley"]

    headmaster "Anything urgent this morning?"
    emiko.say "Nothing that won't keep till the afternoon."
    headmaster "Good. Thanks."
    $ emiko.display(PDAImage(mood = "neutral", mouth = "closed"))
    emiko.say "...Of course. Anytime."
    headmaster_thought "And that's that, then. ...She left a little gap at the end there, like she wanted to say more. And I walked right past it, didn't I."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _nm_go_pl_short
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .distant (**kwargs):
    $ emiko = Person["emiko_langley"]

    headmaster "Just making sure the line's working. That's all."
    $ emiko.display(PDAImage(mood = "sad", mouth = "closed"))
    emiko.say "...It's working. Line's fine."
    headmaster_thought "She reached out, and I answered like a dial tone. ...That was unkind of me. She'll be sitting with that now, and I'm the one who put it there."

    $ situation_manager.apply_progress_change("situation:new_management:main", 0)
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ ASSET NOTES · nm_ghost_office_empty_corridor ══════════════════════════════
#  SCENE IMAGE (establishing) — WIRED via show_pattern("main"):
#    images/events/new_management/nm_ghost_office_empty_corridor/nm_ghost_office_empty_corridor 1.webp
#    Emptying hallway after the bell; Yulan mid-stride, folder open, gaze down,
#    deliberately not looking up. (Add as event `thumbnail=` once it exists.)
#  DIALOGUE : Yulan via paperdoll over blurred school building/1 0 1; guarded
#             neutral, opens a fraction (suprised) only on the education "shop" beat.
#  Selector <folder_topic> drives dialogue; face-known flag half-melts her freeze;
#  "shop" choice gated on Education >= 20.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_ghost_office_empty_corridor (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ yulan = Person["yulan_chen"]
    $ folder_topic = get_value("folder_topic", **kwargs)
    # Read through the gallery getter (paired with the GameDataSelector) so it replays.
    $ face_known = get_value("face_known", 0, **kwargs) == 1

    # Establishing beat: the emptying hallway, Yulan mid-stride not looking up → scene image.
    $ show_pattern("main", **kwargs)
    subtitles "The bell has just finished ringing. The corridor empties in pieces."
    subtitles "Yulan Chen walks with [folder_topic] open, reading as she moves."

    # Hand off to the exchange (paperdoll over the blurred hallway).
    $ yulan.register_paperdoll()
    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True)
    $ yulan.display(PDAImage(pose = "1", outfit = "uniform", level = 1, mood = "neutral", mouth = "closed"),
        PDAPreset("upper_body", duration = 0.0),
        PDAPreset("outside", duration = 0.0))
    $ yulan.display(PDAPreset("upper_body_center", duration = 0.4))
    headmaster "Ms. Chen."
    yulan.say "..."
    subtitles "She doesn't look up. A page turns, unhurried, as if your greeting had been delivered to the wrong desk."

    if face_known:
        $ yulan.display(PDAImage(mood = "neutral", mouth = "open"))
        yulan.say "...Headmaster."
        subtitles "One word — but she said it. The students have started using your name in class, apparently, and things like that climb the stairs eventually."
        headmaster_thought "So it made it all the way up here from the courtyard on its own. ...Good. Saved me dragging it up the stairs myself."
    else:
        headmaster_thought "...Right. Message received. She's not going to hand me anything just because I've learned to say her name in a corridor."

    # Gated choice: a genuinely informed note lands harder — but only if you can give one.
    # Read through the gallery getter so the value replays correctly (Events guide §8/§16).
    $ can_talk_shop = get_stat_value("education", [20, 100], **kwargs) >= 20
    $ shop_title = "Offer a specific, informed note on " + folder_topic

    $ call_custom_menu_with_text("Yulan kept walking.", character.subtitles, False,
        MenuElement("acknowledge", "Slow down and acknowledge her work", EventEffect("nm_ghost_office_empty_corridor.acknowledge")),
        MenuElement("shop", shop_title, EventEffect("nm_ghost_office_empty_corridor.shop"), can_talk_shop),
        MenuElement("greet", "Offer a short greeting and keep moving", EventEffect("nm_ghost_office_empty_corridor.greet")),
        MenuElement("force", "Ignore it and force your pace past her", EventEffect("nm_ghost_office_empty_corridor.force")),
    **kwargs)

label .acknowledge (**kwargs):
    $ yulan = Person["yulan_chen"]
    $ folder_topic = get_value("folder_topic", **kwargs)

    headmaster "Your work on [folder_topic] — the revisions were solid. Genuinely."
    yulan.say "..."
    $ yulan.display(PDAImage(mood = "neutral", mouth = "open"))
    yulan.say "...Thank you."
    subtitles "Still no eye contact. But the next page turns a little slower than the last one did."
    headmaster_thought "Was that— yeah. The page turned slower that time. It's almost nothing. But it's the first inch she's given me."

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
    headmaster_thought "There it is. Charm slides straight off her — but talk about the actual work, know it as well as she does, and she looks up. ...Noted."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=SMALL, reputation=TINY) from _nm_go_cor_shop
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

label .greet (**kwargs):
    $ yulan = Person["yulan_chen"]

    headmaster "Good afternoon, Ms. Chen."
    $ yulan.display(PDAImage(mood = "neutral", mouth = "open"))
    yulan.say "Headmaster."
    headmaster_thought "One word, not a degree of warmth in it. ...Still. I'll take it. Last week I wouldn't have gotten even that."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

label .force (**kwargs):
    $ yulan = Person["yulan_chen"]

    subtitles "You lengthen your stride and go straight past her. Behind you, a folder snaps shut like a small, final verdict."
    $ yulan.display(PDAImage(mood = "angry", mouth = "closed"))
    headmaster_thought "...I just walked straight past her like she was part of the wall, didn't I. She won't forget that. Not her."

    $ situation_manager.apply_progress_change("situation:new_management:main", -1)
    call change_stats_with_modifier(reputation=DEC_TINY, happiness=DEC_TINY) from _nm_go_cor_force
    $ yulan.clear_display()
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Potion Hangover -------------- #
#######################################

# ═══ ASSET NOTES · nm_potion_hangover_miwa ═════════════════════════════════════
#  SCENE IMAGE (establishing object beat) — WIRED via show_pattern("main"):
#    images/events/new_management/nm_potion_hangover_miwa/nm_potion_hangover_miwa 1.webp
#    A busy 3A row of open notebooks — and Miwa's, shut under her folded hands.
#    Quiet, isolating. (Add as event `thumbnail=` once it exists.)
#  DIALOGUE : Miwa via paperdoll over blurred school building/1 0 1 — placed
#    directly, NO entrance slide (she's withdrawn, not arriving).
#  B/W DEVICE (art-free): her portrait desaturates via PDABw for the dissociation
#    beat and returns to colour when she does — the memory-gap on the character.
#  Selector <memory_scrap> = the fragment she almost catches.
# ═══════════════════════════════════════════════════════════════════════════════
label nm_potion_hangover_miwa (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ miwa = Person["miwa_igarashi"]
    $ memory_scrap = get_value("memory_scrap", **kwargs)
    $ emiko_close = get_value("emiko_close", 0, **kwargs) == 1

    # Establishing object beat: a room of open notebooks, and the one that isn't.
    $ show_pattern("main", **kwargs)
    subtitles "3A is deep in a lesson — heads down, pens moving, the ordinary hum of a room that remembers what day it is."
    subtitles "Every notebook on the row is open. Miwa's lies shut under her folded hands, like she's holding it closed on purpose."

    if emiko_close:
        headmaster_thought "Emiko flagged this one on the phone — 'the Igarashi girl, keep half an eye on her.' She's usually right about who's about to slip through a crack."

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

    headmaster_thought "It's the same gap she talked about the day the potion went round. Weeks later — and not one person has thought to just... give the girl her morning back. God."

    $ call_custom_menu_with_text("Miwa is holding very still, braced to be told she's broken.", character.subtitles, False,
        MenuElement("counsel", "Tell her plainly she isn't broken — and open a real door", EventEffect("nm_potion_hangover_miwa.counsel")),
        MenuElement("structure", "Give her one small, doable thing. No pressure", EventEffect("nm_potion_hangover_miwa.structure")),
        MenuElement("press", "Push her to dig for details she plainly can't reach", EventEffect("nm_potion_hangover_miwa.press")),
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
    headmaster_thought "I pushed, and she just closed right up. Of course she did. There's nothing down there to find — leaning on it only makes the hole deeper."

    $ situation_manager.apply_progress_change("situation:new_management:main", -2)
    call change_stats_with_modifier(happiness=DEC_MEDIUM, reputation=DEC_TINY) from _nm_ph_miwa_press
    $ miwa.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ ASSET NOTES · nm_potion_hangover_lily ═════════════════════════════════════
#  SCENE IMAGE (object beat) — WIRED via show_pattern("main"):
#    images/events/new_management/nm_potion_hangover_lily/nm_potion_hangover_lily 1.webp
#    Close-up: her coffee mug rattling once against the saucer as she sets it
#    down — the tell she pretends not to hear. (Add as event `thumbnail=` later.)
#  DIALOGUE : Lily via paperdoll over blurred office building/teacher 1 1 0. She
#    half-enters, apologetic, ready to leave — the scene is coaxing her to stay.
#  Selector <unnerved> rerolls her confession. "loop_in" choice gated on the
#    RELATIONSHIP flag nm_emiko_close (a different gate axis than band 1's stats).
# ═══════════════════════════════════════════════════════════════════════════════
label nm_potion_hangover_lily (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ lily = Person["lily_anderson"]
    $ unnerved = get_value("unnerved", **kwargs)
    $ emiko_close = get_value("emiko_close", 0, **kwargs) == 1

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

    headmaster_thought "God, she's genuinely shaken. This isn't gossip — she just needs to hear she isn't losing her mind. I can give her that much. Just say it plainly, don't make it strange."

    if get_value("guided", 0, **kwargs) == 1:
        $ lily.display(PDAImage(mood = "neutral", mouth = "open"))
        lily.say "The girls settle the instant someone actually looks {i}at{/i} them instead of past them. I've been meaning to say."

    $ call_custom_menu_with_text("Lily has both hands around the mug now, waiting.", character.subtitles, False,
        MenuElement("sit", "Give her the witness she asked for — steady, unhurried", EventEffect("nm_potion_hangover_lily.sit")),
        MenuElement("loop_in", "Believe her, then quietly put Emiko's own record in her hands", EventEffect("nm_potion_hangover_lily.loop_in"), emiko_close),
        MenuElement("maybe", "Offer a careful maybe and a firm next appointment", EventEffect("nm_potion_hangover_lily.maybe")),
        MenuElement("deflect", "Wave it off with a joke. Blame the coffee", EventEffect("nm_potion_hangover_lily.deflect")),
    **kwargs)

label .sit (**kwargs):
    $ lily = Person["lily_anderson"]

    headmaster "Then here it is, out loud: something happened last week. You're not imagining it, and you're not fragile for being the one who noticed."
    $ lily.display(PDAImage(mood = "suprised", mouth = "open"))
    lily.say "..."
    $ lily.display(PDAImage(mood = "happy", mouth = "closed"))
    lily.say "Thank you. God — that's all it— I can go back to third period now. I actually think I can."
    subtitles "The mug doesn't rattle when she lifts it this time. She just looks tired, and a great deal lighter for it."
    headmaster_thought "That was all it took. She didn't want me to fix anything — she just needed to hear it out loud from someone who isn't her. Look at her. Already lighter."

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
    headmaster_thought "Emiko won't begrudge me the file for this. Telling Lily I believe her is one thing — but putting it in her hands, in black and white? Now she's got something solid under her feet."

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
    headmaster_thought "It's not really an answer. But it's a date on the calendar, something to hold onto — and maybe that's enough to carry her through to Thursday."

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
    headmaster_thought "...why did I do that. She worked up the nerve to ask me one honest thing, and I turned it into a joke. She won't be back. Would you be?"

    $ situation_manager.apply_progress_change("situation:new_management:main", 0)
    call change_stats_with_modifier(happiness=DEC_SMALL) from _nm_ph_lily_deflect
    $ lily.clear_display()
    $ end_event('new_daytime', **kwargs)


# ═══ ASSET NOTES · nm_potion_hangover_vial ═════════════════════════════════════
#  Deliberately NOT a conversation — a solo investigation vignette: scene images
#  + inner monologue, almost no paperdoll.
#  SCENE IMAGE (the find) — WIRED via show_pattern("main"):
#    images/events/new_management/nm_potion_hangover_vial/nm_potion_hangover_vial 1.webp
#    Broken green vial / sticky residue behind the bike rack, catching the light.
#  B/W MEMORY (art-free): the smell drags him to last Tuesday's corridor —
#    rendered by reusing an existing corridor bg in blurred greyscale
#    (set_background bw=True), so it reads today and only deepens with real art.
#  Selector <residue_detail> varies the find. "bag" cuts briefly to Emiko's voice
#    (a plain single portrait — NOT the ghost-office split-screen call).
# ═══════════════════════════════════════════════════════════════════════════════
label nm_potion_hangover_vial (**kwargs):
    $ begin_event(version = "2", **kwargs)

    $ residue_detail = get_value("residue_detail", **kwargs)

    # The find — object beat, scene image, no one else out here.
    $ show_pattern("main", **kwargs)
    subtitles "Behind the bike rack, something small catches the light: a broken vial, green glass gone cloudy, the neck still sticky where it snapped clean off."
    subtitles "You crouch. Up close there's [residue_detail]."
    headmaster_thought "So it never actually went anywhere. It just stopped being obvious enough for anyone to trip over — myself included."

    # The smell triggers the flashback — existing corridor bg, blurred and drained.
    subtitles "Then the smell reaches you — sweet, cloying, sitting at the back of the throat — and all at once you aren't behind the bike rack at all."
    $ paperdoll_manager.set_background("images/background/school building/1 0 1.webp", blur = True, bw = True)
    subtitles "{i}Last Tuesday. That same corridor-sweetness hanging in the air. A whole wing of students moving a half-second out of step with themselves, and not one of them able to say why.{/i}"
    headmaster_thought "That smell. It's the same — exactly the same. Whatever this stuff is, it's been through here before. Right under all our noses."
    $ paperdoll_manager.hide_background()
    subtitles "You blink the corridor away. Just the bike rack again. Just the glass, and whatever's still clinging to it."

    $ call_custom_menu_with_text("The vial's still there, catching the light. Someone will kick it into a drain if you don't move first.", character.subtitles, False,
        MenuElement("bag", "Bag it properly and get Emiko on the line", EventEffect("nm_potion_hangover_vial.bag")),
        MenuElement("note", "Log the spot and the smell. Don't raise alarms yet", EventEffect("nm_potion_hangover_vial.note")),
        MenuElement("ignore", "Leave it. You didn't see anything", EventEffect("nm_potion_hangover_vial.ignore")),
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
    headmaster_thought "She didn't even blink. Knew the colour before I said it. ...How long has she been waiting for one of these to turn up again?"

    $ set_game_data("nm_vial_traced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=TINY, reputation=TINY) from _nm_ph_vial_bag
    $ emiko.clear_display()
    $ end_event('new_daytime', **kwargs)

label .note (**kwargs):
    subtitles "You sketch the spot in your pocket notebook — distance from the rack, the angle of the light — and nudge a fallen leaf over the smear with your shoe."
    headmaster_thought "There. Written down, out of sight for now. It's not a crisis yet — but if it becomes one, at least it's on paper before anyone can pretend it never happened."

    $ set_game_data("nm_vial_traced", 1)
    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(education=TINY) from _nm_ph_vial_note
    $ end_event('new_daytime', **kwargs)

label .ignore (**kwargs):
    subtitles "You straighten up and walk on. The sweet smell trails you for three steps, then the wind takes it and the courtyard is only a courtyard again."
    headmaster_thought "...I'm really just going to walk past it. Fine. Except looking away is still a choice — and if I keep making it, sooner or later someone else makes the worse ones for me."

    $ situation_manager.apply_progress_change("situation:new_management:main", -1)
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Testing the Waters ----------- #
#######################################

label nm_testing_the_waters_clipboard (**kwargs):
    $ begin_event(**kwargs)

    $ yuriko = Person["yuriko_oshima"]

    subtitles "Yuriko Oshima intercepts you at the courtyard edge with a clipboard already uncapped."
    yuriko.say "Quick questions. Grey ones."
    yuriko.say "Dress code on weekends — phones in free periods — and dating. What counts, officially?"
    headmaster_thought "She's not curious. She's mapping the office. My answers become precedents before lunch."

    $ call_custom_menu_with_text("Yuriko's pen is waiting.", character.subtitles, False,
        MenuElement("precise", "Answer precisely. Set clear precedents", EventEffect("nm_testing_the_waters_clipboard.precise")),
        MenuElement("hedge", "Hedge and wiggle away from a hard answer", EventEffect("nm_testing_the_waters_clipboard.hedge")),
    **kwargs)

label .precise (**kwargs):
    $ begin_event(**kwargs)
    $ yuriko = Person["yuriko_oshima"]

    headmaster "Weekends: uniform optional off campus, neat if you're representing us. Phones: free periods only, silent. Dating: no PDA on campus. Full stop."
    yuriko.say "Got it."
    subtitles "Three neat lines appear on her clipboard. She almost smiles."
    headmaster_thought "She'll circulate that. Better my words than a rumor version."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, education=TINY) from _call_nm_clip_precise
    $ end_event('new_daytime', **kwargs)

label .hedge (**kwargs):
    $ begin_event(**kwargs)
    $ yuriko = Person["yuriko_oshima"]

    headmaster "It depends. Case by case. I'll... get back to you."
    yuriko.say "So: undefined."
    subtitles "She writes that word larger than the others."
    headmaster_thought "Undefined becomes a playground. She'll fill the blank for me."

    $ situation_manager.apply_progress_change("situation:new_management:main", -3)
    call change_stats_with_modifier(reputation=DEC_SMALL) from _call_nm_clip_hedge
    $ end_event('new_daytime', **kwargs)


label nm_testing_the_waters_memo (**kwargs):
    $ begin_event(**kwargs)

    $ emiko = Person["emiko_langley"]

    subtitles "On your desk: a blank school-wide memo form, edges already aligned to your blotter."
    headmaster_thought "Emiko slid the template. She wants to see what tone I choose to own."

    if get_game_data("new_management_guided") == 1:
        emiko.say "Template on one side. Your words on the other. Go on."

    $ call_custom_menu_with_text("How do you write the first memo?", character.subtitles, False,
        MenuElement("own", "Write a real draft. Own the tone", EventEffect("nm_testing_the_waters_memo.own")),
        MenuElement("vague", "Keep it vague. Let the template do the speaking", EventEffect("nm_testing_the_waters_memo.vague")),
    **kwargs)

label .own (**kwargs):
    $ begin_event(**kwargs)
    $ emiko = Person["emiko_langley"]

    subtitles "You write about presence, office hours, and that the door — correctly labeled — is open."
    emiko.say "I'll run copies before last bell."
    headmaster_thought "Desk work as authorial voice. The school will hear this version of me."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=MEDIUM, education=TINY) from _call_nm_memo_own
    $ end_event('new_daytime', **kwargs)

label .vague (**kwargs):
    $ begin_event(**kwargs)
    $ emiko = Person["emiko_langley"]

    subtitles "You fill the minimum fields and leave the body almost empty."
    emiko.say "Mm. Safe."
    headmaster_thought "Safe reads as absent. Same problem, nicer paper."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _call_nm_memo_vague
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Rumors in Bloom -------------- #
#######################################

label nm_rumors_in_bloom_kiosk (**kwargs):
    $ begin_event(**kwargs)

    $ aona = Person["aona_komuro"]

    subtitles "The kiosk line is its usual crush. Aona's group ranks staff like a game."
    aona.say "Number three — wait."
    aona.say "That's him from the assembly. I recognize him now."
    headmaster_thought "Callback to the janitor beat. The face finally caught the title."

    if get_game_data("new_management_guided") == 1:
        $ emiko = Person["emiko_langley"]
        emiko.say "Kiosk hears everything. So do I."

    $ call_custom_menu_with_text("They've spotted you in the ranking.", character.subtitles, False,
        MenuElement("intervene", "Intervene politely. Claim the title gently", EventEffect("nm_rumors_in_bloom_kiosk.intervene")),
        MenuElement("listen", "Listen without correcting — take the intel", EventEffect("nm_rumors_in_bloom_kiosk.listen")),
        MenuElement("break", "Break up the scene before it hardens into truth", EventEffect("nm_rumors_in_bloom_kiosk.break")),
    **kwargs)

label .intervene (**kwargs):
    $ begin_event(**kwargs)
    $ aona = Person["aona_komuro"]

    headmaster "If you're ranking staff, put me by title. Headmaster. Not a number."
    aona.say "Yes, headmaster."
    subtitles "The joke dies. The recognition stays."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY) from _call_nm_kiosk_intervene
    $ end_event('new_daytime', **kwargs)

label .listen (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You buy a drink and stay in earshot. Names, soft complaints, one parent rumor that might matter."
    headmaster_thought "Ambient intel. The kiosk is a newspaper with sugar."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(reputation=TINY) from _call_nm_kiosk_listen
    $ end_event('new_daytime', **kwargs)

label .break (**kwargs):
    $ begin_event(**kwargs)
    $ aona = Person["aona_komuro"]

    headmaster "Line's moving. Gossip later."
    aona.say "Sheesh."
    headmaster_thought "I killed the moment. Also the chance to own it."

    $ situation_manager.apply_progress_change("situation:new_management:main", -1)
    call change_stats_with_modifier(happiness=DEC_TINY) from _call_nm_kiosk_break
    $ end_event('new_daytime', **kwargs)


label nm_rumors_in_bloom_chalk (**kwargs):
    $ begin_event(**kwargs)

    subtitles "Behind the bike shed: a chalk portrait on the wall. Roughly you — and, oddly, flattering."
    headmaster_thought "Aona's circle energy. The world is drawing me back in."

    $ call_custom_menu_with_text("What do you do with the chalk portrait?", character.subtitles, False,
        MenuElement("leave", "Leave it. Feedback, not harm", EventEffect("nm_rumors_in_bloom_chalk.leave")),
        MenuElement("correct", "Add one small correction. Keep it human", EventEffect("nm_rumors_in_bloom_chalk.correct")),
        MenuElement("erase", "Erase it. Make a point", EventEffect("nm_rumors_in_bloom_chalk.erase")),
    **kwargs)

label .leave (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You walk past. The chalk stays."
    headmaster_thought "If the sketch is kind, legitimacy has a mirror."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(happiness=TINY, charm=TINY) from _call_nm_chalk_leave
    $ end_event('new_daytime', **kwargs)

label .correct (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You fix the jawline with a stub of chalk and add a tiny smile line."
    headmaster_thought "Participation without a lecture. Someone will notice the edit."

    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(charm=TINY, happiness=TINY) from _call_nm_chalk_correct
    $ end_event('new_daytime', **kwargs)

label .erase (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You scrub the wall clean with your sleeve. Dust on your cuff. Silence in the shed."
    headmaster_thought "I made the portrait a crime. That teaches fear, not respect."

    $ situation_manager.apply_progress_change("situation:new_management:main", -2)
    call change_stats_with_modifier(happiness=DEC_SMALL, reputation=DEC_TINY) from _call_nm_chalk_erase
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Quiet Endorsements ----------- #
#######################################

label nm_quiet_endorsements_after_bell (**kwargs):
    $ begin_event(**kwargs)

    $ miwa = Person["miwa_igarashi"]

    subtitles "The period bell cuts the lesson short. Bags zip. Chairs scrape."
    miwa.say "Thanks... for checking. Earlier."
    miwa.say "I'll— I have to go. I just... can't stay long."
    headmaster_thought "Emotional payoff with no demand attached. Care returning."

    if get_game_data("new_management_guided") == 1:
        $ zoe = Person["zoe_parker"]
        zoe.say "Gym's quieter when you drop in."

    $ call_custom_menu_with_text("Miwa is already half out the door.", character.subtitles, False,
        MenuElement("pace", "Match her pace. Let it be quick", EventEffect("nm_quiet_endorsements_after_bell.pace")),
        MenuElement("followup", "Ask one careful follow-up — not too much", EventEffect("nm_quiet_endorsements_after_bell.followup")),
        MenuElement("assign", "Treat it like an assignment and move on", EventEffect("nm_quiet_endorsements_after_bell.assign")),
    **kwargs)

label .pace (**kwargs):
    $ begin_event(**kwargs)
    $ miwa = Person["miwa_igarashi"]

    headmaster "Go. Door's open if you need it."
    miwa.say "Okay."
    subtitles "She's gone before the thank-you can get awkward."

    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(happiness=MEDIUM, charm=TINY) from _call_nm_bell_pace
    $ end_event('new_daytime', **kwargs)

label .followup (**kwargs):
    $ begin_event(**kwargs)
    $ miwa = Person["miwa_igarashi"]

    headmaster "Sleep any better?"
    miwa.say "A little. I'll tell you next time. Promise."
    headmaster_thought "One question. She kept the door cracked."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(happiness=SMALL) from _call_nm_bell_follow
    $ end_event('new_daytime', **kwargs)

label .assign (**kwargs):
    $ begin_event(**kwargs)
    $ miwa = Person["miwa_igarashi"]

    headmaster "Good. Don't be late to your next class."
    miwa.say "...Yes, sir."
    headmaster_thought "I turned thanks into attendance. Cheap."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(education=TINY) from _call_nm_bell_assign
    $ end_event('new_daytime', **kwargs)


label nm_quiet_endorsements_second_coffee (**kwargs):
    $ begin_event(**kwargs)

    $ lily = Person["lily_anderson"]

    subtitles "Second coffee. Same desk. Different air."
    lily.say "I kept thinking about the weekend. It helped... more than I expected."
    lily.say "I'm not here because I'm breaking. I'm here because I trust the chair."
    headmaster_thought "Counseling as relationship track — not crisis."

    $ call_custom_menu_with_text("How do you hold the session?", character.subtitles, False,
        MenuElement("attend", "Stay attentive. Don't chase intensity", EventEffect("nm_quiet_endorsements_second_coffee.attend")),
        MenuElement("summarize", "Listen, then summarize the next appointment clearly", EventEffect("nm_quiet_endorsements_second_coffee.summarize")),
        MenuElement("advice", "Turn it into advice only", EventEffect("nm_quiet_endorsements_second_coffee.advice")),
    **kwargs)

label .attend (**kwargs):
    $ begin_event(**kwargs)
    $ lily = Person["lily_anderson"]

    subtitles "You let the silence work. She fills it when she's ready."
    lily.say "Same time next week?"
    headmaster "Same time."
    headmaster_thought "Trust compounds quietly."

    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(happiness=MEDIUM, reputation=TINY) from _call_nm_coffee_attend
    $ end_event('new_daytime', **kwargs)

label .summarize (**kwargs):
    $ begin_event(**kwargs)
    $ lily = Person["lily_anderson"]

    headmaster "Next Thursday, free period. If anything spikes before then, send a note through Emiko."
    lily.say "Clear. Thank you."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(happiness=SMALL, education=TINY) from _call_nm_coffee_sum
    $ end_event('new_daytime', **kwargs)

label .advice (**kwargs):
    $ begin_event(**kwargs)
    $ lily = Person["lily_anderson"]

    headmaster "Sleep schedule. Water. Don't grade past midnight."
    lily.say "I... know those things."
    headmaster_thought "Advice without listening is a pamphlet."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    $ end_event('new_daytime', **kwargs)


label nm_quiet_endorsements_curriculum (**kwargs):
    $ begin_event(**kwargs)

    $ lily = Person["lily_anderson"]

    subtitles "Lily returns your outline with a pen mark in the margin you recognize as approval."
    lily.say "Actually... better."
    lily.say "Don't make me say it twice. The pacing works."
    headmaster_thought "Awkward praise from Level 1. It lands like care."

    $ call_custom_menu_with_text("How do you take the feedback?", character.subtitles, False,
        MenuElement("adjust", "Accept it and adjust the next lesson", EventEffect("nm_quiet_endorsements_curriculum.adjust")),
        MenuElement("credit", "Credit her publicly, briefly", EventEffect("nm_quiet_endorsements_curriculum.credit")),
        MenuElement("shrug", "Take it as extra work and move on", EventEffect("nm_quiet_endorsements_curriculum.shrug")),
    **kwargs)

label .adjust (**kwargs):
    $ begin_event(**kwargs)
    $ lily = Person["lily_anderson"]

    headmaster "I'll revise the third block. Send me your notes if you have more."
    lily.say "Already did. Check your tray."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(education=MEDIUM, reputation=TINY) from _call_nm_curr_adjust
    $ end_event('new_daytime', **kwargs)

label .credit (**kwargs):
    $ begin_event(**kwargs)
    $ lily = Person["lily_anderson"]

    headmaster "At the next staff brief — I'll say the outline improved because of you."
    lily.say "Please don't make a speech."
    headmaster "One sentence."
    lily.say "...Fine."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=SMALL, happiness=TINY, reputation=TINY) from _call_nm_curr_credit
    $ end_event('new_daytime', **kwargs)

label .shrug (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You file the outline under 'done' and open the next form."
    headmaster_thought "She offered authorship. I treated it like mail."

    $ situation_manager.apply_progress_change("situation:new_management:main", 1)
    call change_stats_with_modifier(education=TINY) from _call_nm_curr_shrug
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Welcome Committee ------------ #
#######################################

label nm_welcome_committee_mug (**kwargs):
    $ begin_event(**kwargs)

    $ finola = Person["finola_ryan"]
    $ yulan = Person["yulan_chen"]

    subtitles "After class, the staff room has a mug waiting in the circle like it grew there."
    finola.say "To surviving your first real week. Good luck with the job, headmaster."
    yulan.say "..."
    headmaster_thought "Yulan almost smiles. Then she remembers herself."

    $ call_custom_menu_with_text("Finola's mug is raised.", character.subtitles, False,
        MenuElement("warm", "Accept warmly. Don't make it awkward", EventEffect("nm_welcome_committee_mug.warm")),
        MenuElement("brief", "Thank her quickly and return to work", EventEffect("nm_welcome_committee_mug.brief")),
        MenuElement("miss", "Pretend you didn't notice", EventEffect("nm_welcome_committee_mug.miss")),
    **kwargs)

label .warm (**kwargs):
    $ begin_event(**kwargs)
    $ finola = Person["finola_ryan"]
    $ yulan = Person["yulan_chen"]

    headmaster "I'll take that toast. Thank you — both of you."
    finola.say "See? He can be human."
    yulan.say "...Hmph."
    headmaster_thought "Social payoff. The word 'new' is already thinning."

    $ situation_manager.apply_progress_change("situation:new_management:main", 6)
    call change_stats_with_modifier(happiness=MEDIUM, reputation=SMALL, charm=SMALL) from _call_nm_mug_warm
    $ end_event('new_daytime', **kwargs)

label .brief (**kwargs):
    $ begin_event(**kwargs)
    $ finola = Person["finola_ryan"]

    headmaster "Thank you, Finola. I've got papers waiting."
    finola.say "Go on then. We'll keep the coffee warm."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL, happiness=TINY) from _call_nm_mug_brief
    $ end_event('new_daytime', **kwargs)

label .miss (**kwargs):
    $ begin_event(**kwargs)
    $ finola = Person["finola_ryan"]

    subtitles "You busy yourself with a stack of forms. The mug lowers without a clink."
    finola.say "...Right."
    headmaster_thought "I snubbed a ritual. Rituals remember."

    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(happiness=DEC_TINY) from _call_nm_mug_miss
    $ end_event('new_daytime', **kwargs)


label nm_welcome_committee_plaque (**kwargs):
    $ begin_event(**kwargs)

    $ emiko = Person["emiko_langley"]

    subtitles "Engraved brass arrives in a crate like it always should have."
    emiko.say "Heh... you're staring."
    headmaster_thought "She watches too long — Level 5 warmth — then jokes it off before anyone else enters."

    if get_game_data("new_management_guided") == 1:
        emiko.say "Your name. Spelled right this time."

    $ call_custom_menu_with_text("The plaque is finally here.", character.subtitles, False,
        MenuElement("real", "Treat it like real — hang it today", EventEffect("nm_welcome_committee_plaque.real")),
        MenuElement("joke", "Smile back and let her pretend it's funny", EventEffect("nm_welcome_committee_plaque.joke")),
    **kwargs)

label .real (**kwargs):
    $ begin_event(**kwargs)
    $ emiko = Person["emiko_langley"]

    headmaster "Help me hang it. Now. While the screws are still in the bag."
    emiko.say "Yes, headmaster."
    subtitles "The old plaque comes down. The tape printout goes in the bin. Brass catches the light."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(reputation=SMALL, charm=TINY) from _call_nm_plaque_real
    $ end_event('new_daytime', **kwargs)

label .joke (**kwargs):
    $ begin_event(**kwargs)
    $ emiko = Person["emiko_langley"]

    headmaster "Don't look at me like that."
    emiko.say "Like what? I'm looking at brass."
    headmaster_thought "We both know she wasn't. The plaque still goes up — tomorrow."

    $ situation_manager.apply_progress_change("situation:new_management:main", 2)
    call change_stats_with_modifier(reputation=TINY, happiness=TINY) from _call_nm_plaque_joke
    $ end_event('new_daytime', **kwargs)


label nm_welcome_committee_assembly (**kwargs):
    $ begin_event(**kwargs)

    $ yuriko = Person["yuriko_oshima"]
    $ aona = Person["aona_komuro"]

    subtitles "Morning line in the courtyard. Quieter. Cleaner. Students find their places without being herded."
    yuriko.say "You're here. By title, today."
    aona.say "Morning, headmaster."
    headmaster_thought "Not 'maintenance guy'. The janitor beat ends here."

    $ call_custom_menu_with_text("The morning assembly is waiting on you.", character.subtitles, False,
        MenuElement("gentle", "Take the ritual seriously. Keep it gentle", EventEffect("nm_welcome_committee_assembly.gentle")),
        MenuElement("routine", "Let it pass as routine presence", EventEffect("nm_welcome_committee_assembly.routine")),
        MenuElement("strict", "Over-correct. Make it too strict", EventEffect("nm_welcome_committee_assembly.strict")),
    **kwargs)

label .gentle (**kwargs):
    $ begin_event(**kwargs)
    $ yuriko = Person["yuriko_oshima"]

    headmaster "Good morning. Short day brief, then classes. Thank you for being on time."
    yuriko.say "They lined up before I asked."
    headmaster_thought "Ceremonial patrol. Title fully earned."

    $ situation_manager.apply_progress_change("situation:new_management:main", 5)
    call change_stats_with_modifier(reputation=MEDIUM, education=TINY, happiness=SMALL) from _call_nm_assy_gentle
    $ end_event('new_daytime', **kwargs)

label .routine (**kwargs):
    $ begin_event(**kwargs)

    subtitles "You nod, walk the line once, and hand the morning to the teachers."
    headmaster_thought "Presence without theater. Still counts."

    $ situation_manager.apply_progress_change("situation:new_management:main", 4)
    call change_stats_with_modifier(reputation=SMALL) from _call_nm_assy_routine
    $ end_event('new_daytime', **kwargs)

label .strict (**kwargs):
    $ begin_event(**kwargs)

    headmaster "Silence. Straighten. Now."
    subtitles "The line snaps tighter. A few faces harden."
    headmaster_thought "They obey. They don't welcome. Close — not the same."

    $ situation_manager.apply_progress_change("situation:new_management:main", 3)
    call change_stats_with_modifier(education=SMALL, happiness=DEC_TINY, reputation=TINY) from _call_nm_assy_strict
    $ end_event('new_daytime', **kwargs)

# endregion
#######################################


#######################################
# region Threshold reactions ---------- #
#######################################

label nm_thresh_emiko_nudge (**kwargs):
    $ set_event_seen("nm_thresh_emiko_nudge")
    $ emiko = Person["emiko_langley"]

    subtitles "Emiko sets a coffee on your desk like a quiet decision."
    emiko.say "The pink slips aren't going anywhere. Neither is your attention."
    emiko.say "Patrol. Desk. Class. Counseling. Pick something the school can see today."
    headmaster_thought "She didn't scold. She named the verbs like weather."
    return

label nm_thresh_district_letter (**kwargs):
    $ set_event_seen("nm_thresh_district_letter")
    $ emiko = Person["emiko_langley"]

    subtitles "Emiko holds an envelope like it might bite."
    emiko.say "District line. Again. Framed as a letter with teeth."
    emiko.say "One more empty stretch and someone picks up the phone for real."
    headmaster_thought "Her L5 mask slips — private worry, then the professional smile returns."
    return

label nm_thresh_first_warmth (**kwargs):
    $ set_event_seen("nm_thresh_first_warmth")
    $ emiko = Person["emiko_langley"]

    emiko.say "Good luck today."
    headmaster_thought "She said it without being asked. Small thing. Not nothing."
    subtitles "Footsteps in the outer office. She steps half a pace back, secretary again."
    emiko.say "Your nine-thirty is early."
    return

label nm_thresh_yulan_thaw (**kwargs):
    $ set_event_seen("nm_thresh_yulan_thaw")
    $ yulan = Person["yulan_chen"]

    subtitles "Yulan stops you between periods — folder closed, for once."
    yulan.say "The students are settling. Quietly."
    yulan.say "Be patient with the parts that still shake."
    headmaster_thought "She sounded like she'd been holding her breath. Counseling just got an open door."
    return

label nm_thresh_adelaide_note (**kwargs):
    $ set_event_seen("nm_thresh_adelaide_note")
    $ emiko = Person["emiko_langley"]
    $ adelaide = Person["adelaide_hall"]

    emiko.say "Adelaide Hall. Follow-up note. Tone's... warmer than last week."
    adelaide.say "If you're still there, please keep the school steady. We're watching — supportively."
    emiko.say "She cares more than she admits."
    $ set_game_data("pta_aware", 1)
    headmaster_thought "They've dropped the word 'new'. I'm just the headmaster now."
    return

label nm_thresh_near_end (**kwargs):
    $ set_event_seen("nm_thresh_near_end")
    $ finola = Person["finola_ryan"]

    subtitles "A form crosses your desk. Signature line: Headmaster. No qualifiers."
    finola.say "Headmaster. Yes — that sounds right."
    headmaster_thought "Paperwork got there first. The plaque and the mug were only catching up."
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

    subtitles "Two coffees on the desk. Emiko doesn't explain."
    emiko.say "For being patient. And present."
    yulan.say "..."
    yulan.say "Welcome to the job. Properly."
    headmaster_thought "The school treats me like the headmaster — not a placeholder."
    return

label game_over_new_management (**kwargs):
    $ begin_event()

    show screen black_error_screen_text ("")
    nvl clear
    nv_text "Your authority never quite became a face."
    nv_text "The school board picked the explanation that fit easiest: absence."
    nv_text "Emiko packed the coffee cups like she was returning someone else's mistake."

    $ MainMenu(confirm=False)()

# endregion
#######################################

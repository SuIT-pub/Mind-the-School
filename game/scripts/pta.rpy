init -6 python:
    import re
    from itertools import product
    from deprecated import deprecated

    registered_vote_events = []

    def vote_registration_key(unlockable_key: str, group_index: int = -1) -> str:
        """Key a story vote claims in registered_vote_events: the whole group, or one member as ``key:index``."""
        if group_index == -1:
            return unlockable_key
        return f"{unlockable_key}:{group_index}"

    ##########################
    # region vote speakers --- #
    ##########################

    # Who may speak for a faction bar at the generic vote: the stat character whose
    # level picks the render, and the members with a `pta_vote <level> <Name>` image.
    PTA_FACTION_SPEAKERS = {
        "Teachers": ("teacher", ["lily_anderson", "yulan_chen", "finola_ryan", "chloe_garcia", "zoe_parker"]),
        "Parents": ("parent", ["adelaide_hall", "nubia_davis", "yuki_yamamoto"]),
        "Students": ("school", ["yuriko_oshima"]),
    }

    # Level-neutral on purpose: they have to fit any proposal at any school level.
    # An Unlockable's vote_comments= replaces them for its own vote.
    PTA_STOCK_VOTE_COMMENTS = {
        "lily_anderson": {
            "yes": "I've gone over it twice, and— well, I still have a list of questions, but none of them are reasons to say no. So yes. The teachers are in favour.",
            "no": "I'm sorry, I just can't see how we'd manage this on top of everything else. We're stretched thin as it is. The teachers vote no.",
        },
        "yulan_chen": {
            "yes": "We went through the proposal point by point in the staff room. It holds up. The teachers vote in favour.",
            "no": "There are too many open questions. Who supervises it, what happens when it goes wrong, who answers to the parents. Until someone can answer those, the teachers vote against.",
        },
        "finola_ryan": {
            "yes": "We talked it over properly, and I'll be honest, not everyone was comfortable at first. But we agreed it's the right thing for the students. The teachers vote yes.",
            "no": "I'd rather be honest than polite about this: most of us don't think it's ready. So the teachers vote no. For now.",
        },
        "chloe_garcia": {
            "yes": "I'll admit I came in expecting to argue against this. But the more we talked about it, the less I could find wrong with it. The teachers are in favour.",
            "no": "Personally, I don't mind it. But we have to think about how this looks from outside these walls, and right now it doesn't look good. The teachers vote no.",
        },
        "zoe_parker": {
            "yes": "As long as somebody keeps an eye on how the girls are actually doing with it, I don't see a problem. The teachers vote yes.",
            "no": "Nobody's convinced me yet that it's good for the students, and that's the only thing that counts for me. The teachers vote no.",
        },
        "adelaide_hall": {
            "yes": "I can't say I love every part of it. But I've seen the girls lately, and I'd be lying if I said things weren't getting better. The parents vote yes.",
            "no": "I'm sorry, but this goes further than I'm comfortable with. We trusted the school to be careful, and this doesn't feel careful to me. The parents vote no.",
        },
        "nubia_davis": {
            "yes": "We've talked this to death. It makes sense, so let's stop going in circles. The parents say yes.",
            "no": "No. I've heard the pitch, I've read the paper, and I'm still not buying it. The parents vote no, and I'd like us to move on.",
        },
        "yuki_yamamoto": {
            "yes": "I had my doubts, and I told my daughter as much. But you've explained it well enough, and I can see what it would do for them. The parents agree.",
            "no": "Some things are better left to the families. I'm not convinced the school should be the one deciding this. The parents vote no.",
        },
        "yuriko_oshima": {
            "yes": "I asked around. Most of them want it, and the rest don't care either way. So, yes. The students vote in favour.",
            "no": "Half of them laughed when I brought it up, and the other half didn't want to talk about it. That's a no from the students.",
        },
    }

    def get_pta_vote_turn(unlockable, bar_key: str, vote: str):
        """
        Pick who speaks for one faction bar at the generic PTA vote, and what she says.

        Args:
            unlockable (Unlockable): The proposal being voted on.
            bar_key (str): Key of the bar the vote was rolled from.
            vote (str): ``"yes"`` or ``"no"``.

        Returns:
            dict | None: ``person`` (Person), ``name`` (image token), ``level``
            (image level) and ``lines`` (list[str]); None for a bar without a
            faction speaker (custom mod bars just count silently).
        """
        faction = PTA_FACTION_SPEAKERS.get(bar_key)
        if faction is None:
            return None
        char_key, person_keys = faction
        people = [(key, Person[key]) for key in person_keys if Person[key] is not None]
        if not people:
            return None
        person_key, person = renpy.random.choice(people)

        lines = unlockable.get_vote_comment(bar_key, vote)
        if not lines:
            lines = [PTA_STOCK_VOTE_COMMENTS.get(person_key, {}).get(vote, "")]
        lines = [line for line in lines if line]
        if not lines:
            return None

        char = get_character_by_key(char_key)
        level = char.get_level() if char is not None else 1
        return {
            "person": person,
            "name": person.first_name,
            "level": clamp_value(level, 1, 10),
            "lines": lines,
        }

    # endregion
    ##########################

    ########################
    # region legacy stubs -- #
    ########################

    @deprecated(version='0.2.3', reason="Legacy journal vote proposal; kept for save compatibility.")
    class PTAProposal:
        """
        Legacy PTA proposal wrapper for old journal vote scheduling.

        Kept so existing saves can unpickle. Cleared on load via
        ``clean_legacy_vote_proposal``. New content stores a live
        ``Unlockable`` in ``voteProposal`` instead.
        """

        def __init__(self, journal_obj=None, action: str = "unlock"):
            self._journal_obj = journal_obj
            self._action = action

    def clean_legacy_vote_proposal():
        """
        Drop legacy ``PTAProposal`` (or other non-Unlockable) values from
        ``voteProposal`` so old saves do not keep obsolete scheduled votes.

        The old journal reserved the vote's money under ``vote_<condition>_<name>``
        when it scheduled the vote. With only one proposal at a time, every ``vote_``
        stash next to a legacy proposal is that vote's, so it goes back to the wallet.
        """
        proposal = get_game_data("voteProposal")
        if proposal is None or isinstance(proposal, Unlockable):
            return
        for stash_key in [key for key in reserved_money.keys() if key.startswith("vote_")]:
            release_money(stash_key)
        set_game_data("voteProposal", None)

    # endregion
    ########################

    ##############################
    # region probability methods #
    ##############################

    def get_end_choice(*votes: str) -> str:
        """
        Gets the end choice based on the votes.

        Args:
            *votes (str): ``\"yes\"``, ``\"no\"``, ``\"ignore\"``, or ``\"veto\"``.

        Returns:
            str: ``\"yes\"``, ``\"no\"``, or ``\"veto\"``.
        """

        if len(votes) == 0:
            return 'no'
        if 'veto' in votes:
            return 'veto'
        elif votes.count('yes') + votes.count('ignore') >= len(votes) / 2:
            return 'yes'
        else:
            return 'no'

    # endregion
    ##############################

###################################
# region PTA Event Registry ----- #
###################################

init -1 python:
    pta_discussion_storage = FragmentStorage("pta_discussion")
    pta_vote_storage = FragmentStorage("pta_vote")
    pta_end_storage = FragmentStorage("pta_end")

init 1 python:

    pta_meeting_event = EventComposite(2, "pta_meeting", [pta_discussion_storage, pta_vote_storage, pta_end_storage], 
        TimeCondition(weekday = 5, daytime = 1),
        PTAObjectSelector("vote_proposal"),
        Pattern("base", "images/events/pta/regular meeting/pta <secretary_level> <school_level> <step>.webp"))

    # PTA discussions
    pta_discussion_1_event = EventFragment(3, "pta_discussion_1")
    
    pta_discussion_storage.add_event(
        pta_discussion_1_event
    )

    pta_vote_unregistered_1_event = EventFragment(2, "pta_vote_unregistered_1",
        JournalNRVoteCondition(),
        # one render per speaker; <level> is her faction's level (get_pta_vote_turn)
        Pattern("vote", "images/events/pta/regular meeting/pta_vote <level> <name>.webp"))

    pta_vote_nothing_1_event = EventFragment(2, "pta_vote_nothing_1",
        CompareCondition("vote_proposal", None))

    pta_vote_storage.add_event(
        pta_vote_unregistered_1_event,
        pta_vote_nothing_1_event,
    )

    # PTA end meeting
    pta_end_meeting_1_event = EventFragment(2, "pta_end_meeting_1")
    
    pta_end_storage.add_event(
        pta_end_meeting_1_event
    )


    time_check_events.add_event(
        pta_meeting_event, 
    )

# endregion
###################################

#############################
# region Intro Events ----- #
#############################

label first_pta_meeting (**kwargs):
    $ begin_event(**kwargs)

    $ hide_all()

    $ image = Image_Series("images/events/pta/first meeting/first pta meeting <nude> <step>.webp", **kwargs)

    $ image.show(0)
    subtitles "You enter the conference room."
    subtitles "All representatives already gathered and wait for you."

    $ image.show(1)
    headmaster """
        Thank you all for gathering today.

        Please allow me to introduce myself as the new headmaster of this institution from Monday.

        I'm aware that many of you probably don't know me yet, but I hope to change that soon.
    """

    $ image.show(2)
    headmaster """
        During my first week, I've taken the time to find out about the current state of the school, and it's clear 
        that there's a lot of work to be done. 

        Rest assured, my aim is to get this school back on track and establish it as one of the leading academic 
        institutions in the country. 
    """

    $ image.show(3)
    headmaster """
        My theory on how to improve the education system has been criticised by established psychologists and teachers. 
        But I can guarantee its effectiveness.

        To give you a better understanding of me. 15 years ago I obtained my diploma in psychology, specifically in 
        educational psychology. And for the last few years I have been working to revolutionise the education system in 
        this country.

        My methods have not yet been accepted by the masses, but this is largely due to the conservative views of the 
        community and their unwillingness to change their habits and adapt to new approaches.

        To briefly summarise my theory. I want to use the parts of the human body that no system has used before.
    """

    $ image.show(4)
    headmaster """
        The human body is a complex biological machine designed to survive in a harsh and dangerous ecosystem. So it 
        was originally built to learn new patterns and methods to give it a better chance of survival.

        So the human body treats information and actions that do not seem to be useful as unnecessary. And the human 
        body has developed a relatively simple system for signalling all kinds of information. Hormones.

        Hormones are used to send certain messages throughout the body. And I want to focus on the hormone dopamine.

        Dopamine is one of the happy hormones, and high levels of dopamine make you feel happy. Dopamine also helps to 
        transfer memories from short-term to long-term memory. This is where my theory comes in.

        The easiest way to produce dopamine is to be intimate. Sure, to some this sounds like I am just trying to 
        create a giant harem school, and sure there are other ways, but I assure you that my intentions are as sincere 
        as they can be, and I think this is a great opportunity to solve many of the problems that occur in our society.

        Problems that are the result of old educational methods and techniques.
    """

    $ image.show(2)
    headmaster """
        One of the main problems is the increasing alienation of individuals in our society. Loneliness is becoming 
        more common, often due to social isolation caused by a lack of interpersonal skills and inadequate support from 
        the community.

        Unfortunately, it's more likely that people who are unable to socialise become outcasts with little or no 
        chance of rehabilitation.

        My aim is to create a form of kinship and a deeper form of intimacy between the students. In a way that 
        emotional and physical support becomes the norm and helps people to become more sociable and easier to 
        integrate into society.

        It was difficult to apply my theory in a large case study, but the investors in this school complex approached 
        me and gave me the opportunity to show the effectiveness of this new method. And that will make these schools 
        the best in the country.
    """

    $ image.show(5)
    headmaster """
        If you want to know more about my theory, please read my book. I'll be happy to give it to you if you're 
        interested.

        Of course, I'm not planning to run these schools alone. I wouldn't be able to handle it. That's why I've called 
        this group together, so that we can work together to improve these schools!

        I plan to hold this meeting every Friday evening so that we can share ideas, talk about the current state of 
        the schools and discuss and vote on changes that are planned for the schools.

        Here's to working together and thank you all for listening.

        Now that I have finished my {i}small{/i} introduction, please introduce yourselves.
    """

    $ image.show(6)
    $ secretary_name = get_name_str('secretary')
    emiko """
        Hello everyone, I am [secretary_name], the headmasters secretary and I will be in 
        charge some organisational tasks like managing the schedule and lower beraucracy tasks.

        I already worked for the last headmaster and observed the decline of our school with my own eyes.

        If you got any questions or issues for the headmaster, please contact me. Thanks.
    """

    $ image.show(7)
    teacher2 "Hello I am Yulan Chen. I am the History and Politics teacher. I also represent the teachers in this school."

    $ image.show(8)
    teacher1 "Hello Lily Anderson, I teach Math and Sciences at this school."

    $ image.show(9)
    teacher3 "I am Finola Ryan, I teach English and History. Pleasure."

    $ image.show(10)
    teacher4 "Chloe Garcia, I teach Arts and Music."

    $ image.show(11)
    teacher5 "And I am Zoe Parker, I teach Physical Education and Health. A pleasure to meet you all."

    $ image.show(12)
    teacher2 """
        First we are glad to have a new headmaster and we hope you bring this school back to what it once was.
        
        As you can see, we are way understaffed and we sometimes have to teach subjects we don't even specialize in.

        We hope you will be able to hire more teachers to ease our workload and support your school reform efforts.

        Now our role during these meetings will be to ensure that new policies and ideas continue to benefit the 
        students.
    """
    
    $ image.show(13)
    parent "Hello, I am Adelaide Hall, a concerned parent of one of the students attending this school and I speak for all parents when I say that we are worried about the recent changes." (name = 'Adelaide Hall')
    parent "However, we trust that you will handle your job competently and we will observe closely to ensure the well-being of our daughters." (name = 'Adelaide Hall')
    
    $ image.show(14)
    parent "I am Nubia Davis. A Pleasure." (name = 'Nubia Davis')

    $ image.show(15)
    parent "Yuki Yamamoto." (name = 'Yuki Yamamoto')

    headmaster.think "Oh quite the cold introduction..."
    
    $ image.show(16)
    sgirl "Hello, I am Yuriko Oshima, the student representative of this school and I am here to make sure that the students of this school are not let out of the decision making and to act as the Mouthpiece of the students issues and suggestions." (name = 'Yuriko Oshima')

    $ image.show(17)
    headmaster "Thank you all for your introductions. With that out of the way, let's wrap up this meeting."
    headmaster "I wish you a good weekend and I hope to see you all next friday."

    $ add_all_buildings_collection_key("closed", "pta_lock")
    $ remove_building_collection_key("office_building", "closed", "pta_lock")
    
    $ end_event('new_daytime', **kwargs)

# endregion
#############################

###############################
# region Regular Events ----- #
###############################

label pta_meeting (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ schoolLevel = get_level("school_level")
    $ secretaryLevel = get_level("secretary_level")

    $ kwargs = load_kwargs_values(kwargs, schoolLevel = schoolLevel, secretaryLevel = secretaryLevel)
    $ image = convert_pattern("base", **kwargs)

    $ image.show(0)
    subtitles "You enter the conference room."
    subtitles "All representatives already gathered and wait for you."
    $ image.show(1)
    headmaster "Thank you all for gathering today."

    $ image.show(2)
    headmaster "First point for today. Does someone have anything to discuss today?"

    call composite_event_runner(**kwargs) from _call_composite_event_runner_pta_meeting_1

#####################
# region DISCUSSION #

label pta_discussion_1 (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)


    $ image.show(3)
    headmaster "No? Alright then lets jump straight to the next point."

    $ end_event('new_daytime', **kwargs)

# endregion
#####################

###############
# region VOTE #

label pta_vote_nothing_1 (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ end_event('new_daytime', **kwargs)

label pta_vote_unregistered_1 (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ unlockable = get_value("vote_proposal", **kwargs)
    if not isinstance(unlockable, Unlockable):
        $ end_event('new_daytime', **kwargs)

    $ votes = unlockable.roll_votes()
    $ end_choice = get_end_choice(*votes)
    $ obj_title = unlockable.get_title()
    $ obj_type = unlockable.type_key
    $ obj_pitch = unlockable.get_vote_pitch()
    $ vote_probability = int(unlockable.get_vote_probability() * 100)

    $ image = convert_pattern("base", **kwargs)

    $ image.show(4)
    if obj_type == "rule":
        headmaster "The next point is a change to the school rules. I'd like us to vote on [obj_title] today."
    elif obj_type == "club":
        headmaster "The next point is a new club. I'd like us to vote on opening the [obj_title] today."
    elif obj_type == "building":
        headmaster "The next point concerns the campus itself. I'd like us to vote on the [obj_title] today."
    else:
        headmaster "The next point is [obj_title], and I'd like us to vote on it today."

    $ image.show(5)
    $ pta_pitch_i = 0
    while pta_pitch_i < len(obj_pitch):
        $ pitch_text = obj_pitch[pta_pitch_i]
        headmaster "[pitch_text]"
        $ pta_pitch_i += 1

    $ image.show(6)
    headmaster "Support among the stakeholders sits at about [vote_probability] percent."
    headmaster "Please cast your vote now."

    # one speaker per faction bar, in bar order (the order roll_votes used)
    $ pta_bars = unlockable.get_bars()
    $ pta_bar_i = 0
    while pta_bar_i < len(pta_bars):
        $ pta_turn = get_pta_vote_turn(unlockable, pta_bars[pta_bar_i].key, votes[pta_bar_i])
        if pta_turn is not None:
            call show_image(get_pattern_from_kwargs("vote", **kwargs).get_path(), **with_values(kwargs, level = pta_turn["level"], name = pta_turn["name"])) from _call_show_image_pta_vote_unregistered_1
            $ pta_speaker = pta_turn["person"]
            $ pta_line_i = 0
            while pta_line_i < len(pta_turn["lines"]):
                $ pta_line = pta_turn["lines"][pta_line_i]
                pta_speaker "[pta_line]"
                $ pta_line_i += 1
        $ pta_bar_i += 1

    $ image.show(7)
    $ yes_count = votes.count("yes")
    $ no_count = votes.count("no")
    headmaster "The ballots are in. [yes_count] in favor, [no_count] against."

    call pta_vote_result(unlockable, end_choice, True) from _call_pta_vote_result_unregistered_1

    $ end_event('new_daytime', **kwargs)

# endregion
###############

##############
# region END #

label pta_end_meeting_1 (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ image = convert_pattern("base", **kwargs)

    $ image.show(7)
    headmaster "It seems like that's all we have for today."
    headmaster "I thank you all for coming."

    $ end_event('new_daytime', **kwargs)

# endregion
##############

label pta_vote_result (unlockable, end_choice, with_comment = False):

    if not isinstance(unlockable, Unlockable):
        $ set_game_data('voteProposal', None)
        return

    $ obj_title = unlockable.get_title()

    if end_choice == 'yes':
        if with_comment:
            headmaster "With the majority of votes in favor, the proposal is accepted."

        $ set_game_data(unlockable.key + "_vote_won", True)
        $ unlockable.check_resolutions()
        if unlockable.is_unlocked():
            $ show_notify_message(f"{obj_title} has been unlocked.")
    else:
        if with_comment:
            headmaster "The proposal is rejected due to the majority of votes against it."
        $ unlockable.release_vote_money()
        $ unlockable.apply_vote_failure_penalty()

    $ unlockable.release_schedule_vote_measure()
    $ set_game_data('voteProposal', None)

    return

# endregion
###############################

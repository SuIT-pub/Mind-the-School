init -6 python:
    import re
    from itertools import product

    registered_vote_events = []

    ########################
    # region CLASSES ----- #
    ########################

    class PTAProposal:
        """
        A class that represents a proposal for the PTA meeting.

        ### Attributes:
        1. _journal_obj : Journal_Obj
            - The journal object that represents the proposal.
        2. _action: str
            - The action that should be performed on the proposal.
            - Can be "unlock" or "upgrade"
        3. _school: str
            - The name of the school that the proposal is for.
        """

        def __init__(self, journal_obj: Journal_Obj, action: str):
            self._journal_obj = journal_obj
            self._action = action

    # endregion
    ########################

    ###################################
    # region Probability calculations #
    ###################################

    def calculateProbabilitySum(conditions: ConditionStorage, *char_obj_list: Char, is_in_pta = False) -> float:
        """
        Calculates the probability of a character voting yes for a proposal.

        ### Parameters:
        1. conditions: ConditionStorage
            - The conditions that decide the success of the proposal.
            - These are used to calculate the probability depending on the difference from expected values
        2. char_obj_list: Char
            - The characters that should vote on the proposal.
            - If None, the default characters will be used.

        ### Returns:
        1. float
            - The probability of the proposal being accepted.
            - The range goes from 0.0 to 100.0
        """

        if conditions == None:
            return 0.0

        if char_obj_list == None or len(char_obj_list) == 0:
            char_obj_list = [
                get_character_by_key("teacher"),
                get_character_by_key("parent"),
                get_character_by_key("school"),
            ]

        overall_probability = 1.0

        probabilities = [calculateProbabilityValue(conditions, char_obj) / 100 for char_obj in char_obj_list]

        transformed_probabilities = [(p + 1) / 2 if p >= -1 else 0 for p in probabilities]

        n = len(transformed_probabilities)
        majority_count = (n // 2) + 1  # Number of approvals for a majority
        
        total_probability = 0.0
        
        # Iterate through all combinations of approvals and rejections
        for outcome in product([0, 1], repeat=n):
            if sum(outcome) >= majority_count:  # If majority reached
                prob = 1.0
                # Calculate the probability of this specific combination
                for i in range(n):
                    if outcome[i] == 1:
                        prob *= transformed_probabilities[i]  # Consent
                    else:
                        prob *= (1 - transformed_probabilities[i])  # Rejection
                total_probability += prob

        return total_probability * 100

    def calculateProbabilityValue(conditions: ConditionStorage, char_obj: Char, is_in_pta = False) -> float:

        probability = calculateProbability(conditions, char_obj, is_in_pta)

        if isinstance(probability, str):
            if probability == 'yes':
                return 100.0
            elif probability == 'no':
                return -100.0
            elif probability == 'veto':
                return -5000.0
        else:
            return probability

    def calculateProbability(conditions: ConditionStorage, char_obj: Char, is_in_pta = False) -> float | str:
        """
        Calculates the probability of a character voting yes for a proposal.

        ### Parameters:
        1. conditions: ConditionStorage
            - The conditions that decide the success of the proposal.
            - These are used to calculate the probability depending on the difference from expected values
        2. char_obj: Char
            - The character that should vote on the proposal.

        ### Returns:
        1. float
            - The probability of the proposal being accepted.
            - The range goes from 0.0 to 100.0
        """

        voteConditions = conditions.get_conditions()
        probability = 100.0
        for condition in voteConditions:
            if isinstance(condition, PTAOverride):
                if condition.char == char_obj.get_name():
                    return condition.accept

            if is_in_pta and isinstance(condition, MoneyCondition):
                continue
            probability += condition.get_diff(char_obj)
        return probability

    # endregion
    ###################################

    ##############################
    # region probability methods #
    ##############################

    def voteCharacter(conditions: ConditionStorage, char_obj: Char) -> str:
        """
        Lets a character vote on a proposal.

        ### Parameters:
        1. conditions: ConditionStorage
            - The conditions that decide the success of the proposal.
            - These are used to calculate the probability depending on the difference from expected values
        2. char_obj: Char
            - The character that should vote on the proposal.

        ### Returns:
        1. str
            - The vote of the character.
            - Can be "yes", "no" or "veto"
        """

        probability = calculateProbability(conditions, char_obj, is_in_pta = True)

        voteDiff = 0

        if isinstance(probability, str):
            return probability
        else:
            vote = renpy.random.random() * 100
            voteDiff = probability - vote

            if probability >= 100 or voteDiff >= 0:
                return 'yes'
            elif probability <= 0 and voteDiff <= -50:
                return 'veto'
            else:
                return 'no'

    def get_end_choice(*votes: str) -> str:
        """
        Gets the end choice based on the votes of the characters.

        ### Parameters:
        1. votes: str
            - The votes of the characters.
            - Can be "yes", "no" or "veto"

        ### Returns:
        1. str
            - The end choice based on the votes.
            - Can be "yes", "no" or "veto"
        """

        if 'veto' in votes:
            return 'veto'
        elif votes.count('yes') >= len(votes) / 2:
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
        PTAVoteSelector("vote_parent", "parent"),
        PTAVoteSelector("vote_teacher", "teacher"),
        PTAVoteSelector("vote_student", "school"),
        Pattern("base", "images/events/pta/regular meeting/pta <secretary_level> <school_level> <step>.webp"))

    # PTA discussions
    pta_discussion_1_event = EventFragment(2, "pta_discussion_1")
    
    pta_discussion_storage.add_event(
        pta_discussion_1_event
    )

    # PTA votes
    pta_vote_school_jobs_event = EventFragment(2, "pta_vote_school_jobs",
        JournalVoteCondition("school_jobs"))

    pta_vote_student_relationships_event = EventFragment(2, "pta_vote_student_relationships_1",
        JournalVoteCondition("student_student_relation"))

    pta_vote_unregistered_1_event = EventFragment(2, "pta_vote_unregistered_1",
        JournalNRVoteCondition(),
        RandomListSelector("speaking_teacher", "Lily Anderson", "Yulan Chen", "Finola Ryan", "Chloe Garcia", "Zoe Parker"),
        RandomListSelector("speaking_parent", "Yuki Yamamoto", "Adelaide Hall", "Nubia Davis"),
        RandomListSelector("speaking_student", "Yuriko Oshima"),
        Pattern("vote", "images/events/pta/regular meeting/pta_vote <level> <name>.webp"))

    pta_vote_nothing_1_event = EventFragment(2, "pta_vote_nothing_1",
        CompareCondition("vote_proposal", None))

    pta_vote_storage.add_event(
        pta_vote_unregistered_1_event,
        pta_vote_nothing_1_event,
        pta_vote_school_jobs_event,
        pta_vote_student_relationships_event
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
    secretary """
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
    parent "However, we trust that you will handle your job competently and we will observe closely to ensure the well-being of our children." (name = 'Adelaide Hall')
    
    $ image.show(14)
    parent "I am Nubia Davis. A Pleasure." (name = 'Nubia Davis')

    $ image.show(15)
    parent "Yuki Yamamoto." (name = 'Yuki Yamamoto')

    headmaster_thought "Oh quite the cold introduction..."
    
    $ image.show(16)
    sgirl "Hello, I am Yuriko Oshima, the student representative of this school and I am here to make sure that the students of this school are not let out of the decision making and to act as the Mouthpiece of the students issues and suggestions." (name = 'Yuriko Oshima')

    $ image.show(17)
    headmaster "Thank you all for your introductions. With that out of the way, let's wrap up this meeting."
    headmaster "I wish you a good weekend and I hope to see you all next friday."

    $ set_all_buildings_blocked(True)
    $ set_building_blocked("office_building", False)
    
    $ end_event('new_daytime', **kwargs)

# endregion
#############################

###############################
# region Regular Events ----- #
###############################

label pta_meeting (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

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

label pta_vote_school_jobs (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ parent_vote  = get_value("vote_parent", **kwargs)
    $ teacher_vote = get_value("vote_teacher", **kwargs)
    $ student_vote = get_value("vote_student", **kwargs)
    $ end_choice = get_end_choice(parent_vote, teacher_vote, student_vote)

    headmaster "Today I want to put to vote if we want to allow students to work here at the school."

    headmaster "The students get an opportunity to work or help out in certain facilities of the school."
    headmaster "This not only helps the facilities to run more smoothly, but also gives the students a chance to learn new skills and to earn some money."

    headmaster "Please cast your vote now."

    # teacher comment on vote
    if teacher_vote == 'yes':
        teacher "I think it is a good idea to let the students work here. It will help them to learn new skills and to earn some money."
        teacher "I vote yes."
    elif teacher_vote == 'veto':
        teacher "I strongly oppose this proposal. Allowing students to work here will severely distract them from their studies. I veto."
    else:
        teacher "I don't think it is a good idea to let the students work here. It will distract them from their studies."
        teacher "I vote against it."

    # student comment on vote
    if student_vote == 'yes':
        sgirl "I think it's a great idea to let us work here. It would help us learn new skills and earn some money."
        sgirl "I vote yes."
    elif student_vote == 'veto':
        sgirl "Absolutely not! Letting us work here would totally mess up our studies. I veto this proposal."
    else:
        sgirl "I don't think it's a good idea for us to work here. It would distract us from our studies."
        sgirl "I vote against it."

    # parent comment on vote
    if parent_vote == 'yes':
        parent "As a mother, I believe it's a wonderful opportunity for our children to gain practical experience and earn some money. I wholeheartedly support this initiative."
    elif parent_vote == 'veto':
        parent "As a mother, I strongly oppose this proposal. Allowing students to work here will severely distract them from their studies. I veto."
    else:
        parent "As a mother, I don't think it's a good idea for our children to work here. It will distract them from their studies."

    if end_choice == 'yes':
        headmaster "With the majority of votes in favor, the proposal is accepted."
        headmaster "The students will be allowed to work here at the school."
    elif end_choice == 'veto':
        headmaster "The proposal is rejected due to a veto by one of the representatives."
    else:
        headmaster "The proposal is rejected due to the majority of votes against it."

    call pta_vote_result(parent_vote, teacher_vote, student_vote, get_value("vote_proposal", **kwargs)) from _call_pta_vote_result_school_jobs_1

    $ end_event('new_daytime', **kwargs)

label pta_vote_student_relationships_1 (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ parent_vote = get_value("vote_parent", **kwargs)
    $ teacher_vote = get_value("vote_teacher", **kwargs)
    $ student_vote = get_value("vote_student", **kwargs)
    $ end_choice = get_end_choice(parent_vote, teacher_vote, student_vote)

    headmaster "The topic for today's vote is whether to allow students to have relationships with each other."
    headmaster "This proposal aims to recognize and support student relationships, while also providing guidance on maintaining healthy and respectful interactions."

    headmaster "Please cast your vote now."

    # teacher comment on vote
    if teacher_vote == 'yes':
        teacher "I believe that allowing students to have relationships with each other can be a positive experience."
        teacher "It helps them learn about social interactions and emotional connections in a controlled environment. So I vote yes."
    elif teacher_vote == 'veto':
        teacher "I am strongly opposed to allowing students to have relationships with each other."
        teacher "Such relationships can lead to distractions and complications that are not suitable for the school environment. I veto this proposal."
    else:
        teacher "I have concerns about allowing students to have relationships with each other."
        teacher "While it can be a learning experience, it can also lead to issues that may disrupt their education. Therefore, I vote against this proposal."

    # student comment on vote
    if student_vote == 'yes':
        sgirl "As a student, I think it's important for us to be allowed to have relationships with each other."
        sgirl "It helps us understand how to interact with others and build meaningful connections. Therefore, I vote yes on this proposal."
    elif student_vote == 'veto':
        sgirl "I don't think it's a good idea to allow students to have relationships with each other."
        sgirl "It could lead to unnecessary drama and distractions from our studies. I veto this proposal."
    else:
        sgirl "I have mixed feelings about allowing students to have relationships with each other."
        sgirl "While it can be beneficial, it can also cause problems that might affect our education. Therefore, I vote no on this proposal."

    # parent comment on vote
    if parent_vote == 'yes':
        parent "As a parent, I believe that allowing students to have relationships with each other can be beneficial."
        parent "It helps them learn about social dynamics and emotional connections in a safe environment. That's why I vote yes."
    elif parent_vote == 'veto':
        parent "I am opposed to allowing students to have relationships with each other."
        parent "Such relationships can lead to distractions and issues that are not appropriate for the school setting. I veto this proposal."
    else:
        parent "I have reservations about allowing students to have relationships with each other."
        parent "While it can be a learning experience, it can also lead to complications that may disrupt their education. Therefore, I vote against this proposal."

    if end_choice == 'yes':
        headmaster "With the majority of votes in favor, the proposal is accepted."
        headmaster "The students will be allowed to work here at the school."
    elif end_choice == 'veto':
        headmaster "The proposal is rejected due to a veto by one of the representatives."
    else:
        headmaster "The proposal is rejected due to the majority of votes against it."
    
    call pta_vote_result(parent_vote, teacher_vote, student_vote, get_value("vote_proposal", **kwargs)) from _call_pta_vote_result_student_relationships_1
    
    $ end_event('new_daytime', **kwargs)

label pta_vote_unregistered_1 (**kwargs):
    $ begin_event(no_gallery = True, **kwargs)

    $ vote_proposal = get_value("vote_proposal", **kwargs)
    $ vote_object = vote_proposal._journal_obj
    $ vote_action = vote_proposal._action
    
    $ speaking_teacher = get_value("speaking_teacher", **kwargs)
    $ speaking_parent = get_value("speaking_parent", **kwargs)
    $ speaking_student = get_value("speaking_student", **kwargs)

    $ parent_vote  = get_value("vote_parent", **kwargs)
    $ teacher_vote = get_value("vote_teacher", **kwargs)
    $ student_vote = get_value("vote_student", **kwargs)
    $ end_choice = get_end_choice(parent_vote, teacher_vote, student_vote)

    $ teacher_response = vote_object.get_vote_comments("teacher", teacher_vote)
    $ student_response = vote_object.get_vote_comments("student", student_vote)
    $ parent_response  = vote_object.get_vote_comments("parent", parent_vote)

    $ obj_title = vote_object.get_title()
    $ obj_type = vote_object.get_type()
    $ obj_desc = vote_object.get_description()

    $ image = convert_pattern("base", **kwargs)

    $ image.show(4)
    if obj_type == "rule":
        headmaster "Today I want to put to vote a change in the schools ruleset."
        headmaster "I want to implement the Rule: [obj_title]."
    elif obj_type == "club":
        headmaster "Today I want to put to vote if we want to open a new club at the school."
        headmaster "I want to open the [obj_title]."
    elif obj_type == "building" and vote_action == "unlock":
        headmaster "Today I want to put to vote if we want to restore the [obj_title]."
    elif obj_type == "building" and vote_action == "upgrade":
        headmaster "Today I want to put to vote if we want to upgrade the [obj_title]."

    $ image.show(5)
    $ i = 0
    while i < len(obj_desc):
        $ desc_text = obj_desc[i]
        headmaster "[desc_text]"
        $ i += 1

    $ image.show(6)
    headmaster "Please cast your vote now."
    
    $ show_pattern("vote", level = get_character_by_key("teacher").get_level(), name = split_name_first(speaking_teacher), **kwargs)
    if isinstance(teacher_response, str):
        teacher "[teacher_response]" (name = speaking_teacher)
    else:
        $ i = 0
        while i < len(teacher_response):
            $ response_text = teacher_response[i]
            teacher "[response_text]" (name = speaking_teacher)
            $ i += 1

    $ show_pattern("vote", level = get_character_by_key("school").get_level(), name = split_name_first(speaking_student), **kwargs)
    if isinstance(student_response, str):
        sgirl "[student_response]" (name = speaking_student)
    else:
        $ i = 0
        while i < len(student_response):
            $ response_text = student_response[i]
            sgirl "[response_text]" (name = speaking_student)
            $ i += 1

    $ show_pattern("vote", level = get_character_by_key("parent").get_level(), name = split_name_first(speaking_parent), **kwargs)
    if isinstance(parent_response, str):
        parent "[parent_response]" (name = speaking_parent)
    else:
        $ i = 0
        while i < len(parent_response):
            $ response_text = parent_response[i]
            parent "[response_text]" (name = speaking_parent)
            $ i += 1

    call pta_vote_result(parent_vote, teacher_vote, student_vote, vote_proposal) from _call_pta_vote_result_unregistered_1

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

label pta_vote_result (parent_vote, teacher_vote, student_vote, proposal):
    $ vote_object = proposal._journal_obj
    $ vote_action = proposal._action
    $ obj_title = vote_object.get_title()
    $ end_choice = get_end_choice(parent_vote, teacher_vote, student_vote)

    $ money_conditions = [condition for condition in vote_object.get_conditions() if isinstance(condition, MoneyCondition)]

    if end_choice == 'yes':
        if vote_action == "unlock":
            $ vote_object.unlock(True, True)
            $ add_notify_message(f"{obj_title} has been unlocked.")
        if vote_action == "upgrade":
            $ vote_object.upgrade(True)
            $ add_notify_message(f"{obj_title} has been upgraded.")

        python:
            for condition in money_conditions:
                spend_reserved_money("vote_" + condition.get_name() + "_" + vote_object.get_name())
    python:
        for condition in money_conditions:
            release_money("vote_" + condition.get_name() + "_" + vote_object.get_name())
    $ set_game_data('voteProposal', None)

    return

# endregion
###############################
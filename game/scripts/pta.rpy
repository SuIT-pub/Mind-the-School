init -6 python:
    import re
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

    def calculateProbabilitySum(conditions: ConditionStorage, *char_obj_list: Char) -> float:
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
                get_character("teacher", charList["staff"]),
                charList["parents"],
            ]
            char_obj_list.extend(get_school())

        probability = 0.0

        for char_obj in char_obj_list:
            calc = calculateProbability(conditions, char_obj)
            probability += calc

        return probability / len(char_obj_list)

    def calculateProbability(conditions: ConditionStorage, char_obj: Char) -> float:
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
        probability = 25.0
        for condition in voteConditions:
            probability += condition.get_diff(char_obj)
        return probability

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

        probability = calculateProbability(conditions, char_obj)
        vote = renpy.random.random() * 100
        voteDiff = probability - vote

        if probability >= 100 or voteDiff >= 0:
            return 'yes'
        elif probability <= 0 or voteDiff <= -50:
            return 'veto'
        else:
            return 'no'
    

label pta_meeting (**kwargs):
    # """
    # The main label for the PTA meeting.
    # Here the player can vote on proposals and discuss issues.
    # """
    
    $ proposal = get_game_data('voteProposal')
    $ obj_school = get_school()
    $ obj_parent = get_character("parents", charList)
    $ obj_teacher = get_character("teacher", charList["staff"])
    $ obj_secretary = get_character("secretary", charList["staff"])
    
    $ obj = None
    $ obj_type = None
    $ obj_title = None
    $ obj_desc = None
    $ obj_action = None

    if proposal != None:
        $ obj = proposal._journal_obj
        $ obj_type = obj.get_type()
        $ obj_title = obj.get_title()
        $ obj_desc = obj.get_description()
        $ obj_action = proposal._action

    $ obj_school_name = obj_school.get_name()
    $ obj_school_title = obj_school.get_title()

    if proposal != None:
        $ forNum = 0
        
        $ teacher_obj = get_character("teacher", charList["staff"])
        $ teacher_vote = voteCharacter(
            obj.get_condition_storage(), 
            teacher_obj,
        )
        $ teacher_response = obj.get_vote_comments("teacher", teacher_vote)
        if teacher_vote == 'yes':
            $ forNum += 1
        elif teacher_vote == 'veto':
            $ forNum = -3
            
        $ school_obj = get_school()
        $ student_vote = voteCharacter(
            obj.get_condition_storage(), 
            school_obj,
        )
        $ student_response = obj.get_vote_comments("student", student_vote)
        if student_vote == 'yes':
            $ forNum += 1
        elif student_vote == 'veto':
            $ forNum = -3
            
        $ parent_obj = charList["parents"]
        $ parent_vote = voteCharacter(
            obj.get_condition_storage(), 
            parent_obj, 
        )
        $ parent_response = obj.get_vote_comments("parent", parent_vote)
        if parent_vote == 'yes':
            $ forNum += 1
        elif parent_vote == 'veto':
            $ forNum = -3

    
    $ image = Image_Series("images/events/pta/regular meeting/pta_1 <secretary_level> <teacher_level> <student_level> <parent_level> <step>.webp", 
        secretary_level = obj_secretary.get_level(),
        teacher_level = obj_teacher.get_level(),
        student_level = obj_school.get_level(), 
        parent_level = obj_parent.get_level()
    )

    # $ speaking_teacher = get_random_choice("Lily Anderson", "Yulan Chen", "Finola Ryan", "Chloe Garcia", "Zoe Parker")
    # $ speaking_parent = get_random_choice("Yuki Yamamoto", "Adelaide Hall", "Nubia Davis")

    $ speaking_teacher = "Yulan Chen"
    $ speaking_parent = "Adelaide Hall"
    $ speaking_student = get_random_choice("Yuriko Oshima")

    $ begin_event()

    $ image.show(0)
    subtitles "You enter the conference room."
    subtitles "All representatives already gathered and wait for you."
    $ image.show(1)
    headmaster "Thank you all for gathering today."

    $ image.show(2)
    headmaster "First point for today. Does someone have anything to discuss today?"

    if "pta-issues" in gameData and len(gameData["pta-issues"]) != 0:
        subtitles "todo: add pta-issues"
    else:
        $ image.show(3)
        headmaster "No? Alright then lets jump straight to the next point."

    if proposal != None:
        $ image.show(4)
        if obj_type == "rule":
            headmaster "Today I want to put to vote a change in the schools ruleset."
            headmaster "I want to implement the Rule: [obj_title]."
        elif obj_type == "club":
            headmaster "Today I want to put to vote if we want to open a new club at the school."
            headmaster "I want to open the [obj_title]."
        elif obj_type == "building" and obj_action == "unlock":
            headmaster "Today I want to put to vote if we want to restore the [obj_title]."
        elif obj_type == "building" and obj_action == "upgrade":
            headmaster "Today I want to put to vote if we want to upgrade the [obj_title]."

        $ image.show(5)
        $ i = 0
        while i < len(obj_desc):
            $ desc_text = obj_desc[i]
            headmaster "[desc_text]"
            $ i += 1

        $ image.show(6)
        headmaster "Please cast your vote now."

        call show_image("images/events/pta/regular meeting/pta_2 <secretary_level> <teacher_level> <student_level> <parent_level> <teacher> <vote>.webp",
            secretary_level = obj_secretary.get_level(),
            teacher_level = obj_teacher.get_level(), 
            student_level = obj_school.get_level(), 
            parent_level = obj_parent.get_level(),
            teacher = speaking_teacher,
            vote = teacher_vote
        ) from _call_show_image_3
        teacher "[teacher_response]" (name = speaking_teacher)

        call show_image("images/events/pta/regular meeting/pta_2 <secretary_level> <teacher_level> <student_level> <parent_level> <student> <vote>.webp",
            secretary_level = obj_secretary.get_level(),
            teacher_level = obj_teacher.get_level(),
            student_level = obj_school.get_level(), 
            parent_level = obj_parent.get_level(),
            student = speaking_student,
            vote = student_vote
        ) from _call_show_image_4
        sgirl "[student_response]" (name = speaking_student)

        call show_image("images/events/pta/regular meeting/pta_2 <secretary_level> <teacher_level> <student_level> <parent_level> <parent> <vote>.webp",
            secretary_level = obj_secretary.get_level(),
            teacher_level = obj_teacher.get_level(),
            student_level = obj_school.get_level(), 
            parent_level = obj_parent.get_level(),
            parent = speaking_parent,
            vote = parent_vote
        ) from _call_show_image_5
        parent "[parent_response]" (name = speaking_parent)

        $ image.show(7)
        if forNum >= 2:
            headmaster "The vote was successful. The [obj_title] will be implemented."
            $ obj.unlock(obj_school_name, True, True)
        else:
            headmaster "The vote was unsuccessful. The [obj_title] will not be implemented."

        $ set_game_data("voteProposal", None)

        
    headmaster "It seems like that's all we have for today."
    headmaster "I thank you all for coming."

    jump new_daytime
    
label first_pta_meeting (**kwargs):
    $ hide_all()

    call show_image("images/events/pta/first meeting/first pta meeting 0.webp") from first_pta_meeting_0

    subtitles "You enter the conference room."
    subtitles "All representatives already gathered and wait for you."

    call show_image(f"images/events/pta/first meeting/first pta meeting 1 0 <nude>.webp") from first_pta_meeting_1
    headmaster """
        Thank you all for gathering today.

        Please allow me to introduce myself as the new headmaster of this institution from Monday.

        I'm aware that many of you probably don't know me yet, but I hope to change that soon.
    """

    hide screen image_with_nude_var
    scene expression "events/pta/first meeting/first pta meeting 2 0.webp"
    headmaster """
        During my first week, I've taken the time to find out about the current state of the school, and it's clear 
        that there's a lot of work to be done. 

        Rest assured, my aim is to get this school back on track and establish it as one of the leading academic 
        institutions in the country. 
    """

    scene expression "events/pta/first meeting/first pta meeting 3 0.webp"
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
 
    scene expression "events/pta/first meeting/first pta meeting 4 0.webp"
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

    scene expression "events/pta/first meeting/first pta meeting 2 0.webp"
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

    call show_image(f"images/events/pta/first meeting/first pta meeting 5 <loli_content> <nude>.webp", loli_content = 0) from first_pta_meeting_2
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

    hide screen image_with_nude_var
    scene first pta meeting 6
    secretary """
        Hello everyone, I am [secretary_first_name] [secretary_last_name], the headmasters secretary and I will be in 
        charge some organisational tasks like managing the schedule and lower beraucracy tasks.

        I already worked for the last headmaster and observed the decline of our school with my own eyes.

        If you got any questions or issues for the headmaster, please contact me. Thanks.
    """

    scene first pta meeting 7
    teacher2 """
        Hello I am [teacher_2_first_name] [teacher_2_last_name] and today I represent the teachers of this school.

        First we are glad to have a new headmaster and we hope you bring this school back to what it once was.
        
        As you can see, we are way understaffed and we sometimes have to teach subjects we don't even specialize in.

        We hope you will be able to hire more teachers to ease our workload and support your school reform efforts.

        Now our role during these meetings will be to ensure that new policies and ideas continue to benefit the 
        students.

        That's all from our side. Thank you very much.
    """
    
    call show_image(f"images/events/pta/first meeting/first pta meeting 8 <nude>.webp", loli_content = 0) from first_pta_meeting_3
    parent """
        Hello, I am a concerned parent of one of the students attending this school and I speak for all parents when I 
        say that we are worried about the recent changes. 
        
        However, we trust that you will handle your job competently and we will observe closely to ensure the 
        well-being of our children.
    """
    
    hide screen image_with_nude_var
    call show_image(f"images/events/pta/first meeting/first pta meeting 9 <loli_content> <nude>.webp", loli_content = 0) from first_pta_meeting_4
    sgirl """
        Hello, I am the student representative of this school and I am here to make sure that the students of this 
        school are not let out of the decision making and to act as the Mouthpiece of the students issues and 
        suggestions.
    """

    hide screen image_with_nude_var
    scene first pta meeting 10 #
    headmaster "Thank you all for your introductions. With that out of the way, let's wrap up this meeting."
    headmaster "I wish you a good weekend and I hope to see you all next friday."

    $ set_all_buildings_blocked(True)
    $ set_building_blocked("office_building", False)
    
    jump new_daytime
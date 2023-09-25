
init -6 python:
    import re
    class voteProposal:
        def __init__(self, journal_obj, action, school):
            self._journal_obj = journal_obj
            self._action = action
            self._school = school

    def calculateProbabilitySum(conditions, char_obj_list = None):
        if char_obj_list == None or len(char_obj_list) == 0:
            char_obj_list = [
                get_character("teacher", charList["staff"]),
                get_character(school, charList["schools"]),
                charList["parents"],
            ]

        probability = 0.0

        for char_obj in char_obj_list:
            calc = calculateProbability(conditions, char_obj)
            print("char: " + char_obj.get_title() + ", calc: " + str(calc))
            probability += calc

        return probability / len(char_obj_list)

    def calculateProbability(conditions, char_obj):
        voteConditions = conditions.get_conditions()
        print("voteConditions: " + str(voteConditions))
        probability = 50.0
        for condition in voteConditions:
            probability += condition.get_diff(char_obj)
        return probability

    def voteCharacter(conditions, char_obj):
        probability = calculateProbability(conditions, char_obj)
        vote = renpy.random.random() * 100
        voteDiff = probability - vote

        print("char: " + char_obj.get_title() + ", probability: " + str(probability) + ", vote: " + str(vote) + ", voteDiff: " + str(voteDiff))

        if probability >= 100 or voteDiff >= 0:
            return 'yes'
        elif probability <= 0 or voteDiff <= -50:
            return 'veto'
        else:
            return 'no'
    

label pta_meeting:
    subtitles "You enter the conference room."
    subtitles "All representatives already gathered and wait for you."
    headmaster "Thank you all for gathering today."

    headmaster "First point for today. Does someone have anything to discuss today?"

    if "pta-issues" in gameData and len(gameData["pta-issues"]) != 0:
        subtitles "todo: add pta-issues"
    else:
        headmaster "No? Alright then lets jump straight to the next point."

    if "voteProposal" in gameData and gameData["voteProposal"] != None:
        $ obj = gameData["voteProposal"]._journal_obj
        $ obj_type = obj.get_type()
        $ obj_title = obj.get_title()
        $ obj_desc = obj.get_description()
        $ obj_action = gameData["voteProposal"]._action

        $ obj_school = get_character(gameData["voteProposal"]._school, charList["schools"])
        $ obj_school_name = obj_school.get_name()
        $ obj_school_title = obj_school.get_title()

        if obj_type == "rule":
            headmaster "Today I want to put to vote a change in the [obj_school_title]s ruleset."
            headmaster "I want to implement the Rule: [obj_title]."
        elif obj_type == "club":
            headmaster "Today I want to put to vote if we want to open a new club at the [obj_school_title]."
            headmaster "I want to open the [obj_title]."
        elif obj_type == "building" and obj_action == "unlock":
            headmaster "Today I want to put to vote if we want to restore the [obj_title]."
        elif obj_type == "building" and obj_action == "upgrade":
            headmaster "Today I want to put to vote if we want to upgrade the [obj_title]."

        $ i = 0
        while i < len(obj_desc):
            $ desc_text = obj_desc[i]
            headmaster "[desc_text]"
            $ i += 1

        headmaster "Please cast your vote now."

        $ forNum = 0

        $ teacher_obj = get_character("teacher", charList["staff"])
        $ teacher_vote = voteCharacter(
            obj.get_condition_storage(), 
            teacher_obj,
            obj_school_name,
        )
        $ teacher_response = obj.get_vote_comments("teacher", teacher_vote)
        teacher "[teacher_response]"
        if teacher_vote == 'yes':
            $ forNum += 1
        elif teacher_vote == 'veto':
            $ forNum = -3

        $ school_obj = get_character(obj_school_name, charList["schools"])
        $ student_vote = voteCharacter(
            obj.get_condition_storage(), 
            school_obj,
            obj_school_name,
        )
        $ student_response = obj.get_vote_comments("student", student_vote)
        sgirl "[student_response]"
        if student_vote == 'yes':
            $ forNum += 1
        elif student_vote == 'veto':
            $ forNum = -3

        $ parent_obj = charList["parents"]
        $ parent_vote = voteCharacter(
            obj.get_condition_storage(), 
            parent_obj, 
            obj_school_name,
        )
        $ parent_response = obj.get_vote_comments("parent", parent_vote)
        parent "[parent_response]"
        if parent_vote == 'yes':
            $ forNum += 1
        elif parent_vote == 'veto':
            $ forNum = -3

        if forNum >= 2:
            headmaster "The vote was successful. The [obj_title] will be implemented."
            $ obj.unlock(obj_school_name, True, True)
        else:
            headmaster "The vote was unsuccessful. The [obj_title] will not be implemented."

    jump new_daytime

init -6 python:
    import re
    class voteProposal:
        def __init__(self, journal_obj, action, school):
            self._journal_obj = journal_obj
            self._action = action
            self._school = school

    def calculateProbability(conditions, char_obj, school = None):
        voteConditions = conditions.get_votable_conditions(school)
        print("voteConditions: " + str(voteConditions))
        probability = 75.0
        for condition in voteConditions:
            probability += condition.get_diff(char_obj)
        return probability

    def voteCharacter(conditions, char_obj, school = None):
        probability = calculateProbability(conditions, char_obj, school)
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
    principal "Thank you all for gathering today."

    principal "First point for today. Does someone have anything to discuss today?"

    if "pta-issues" in gameData and len(gameData["pta-issues"]) != 0:
        subtitles "todo: add pta-issues"
    else:
        principal "No? Alright then lets jump straight to the next point."

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
            principal "Today I want to put to vote a change in the [obj_school_title]s ruleset."
            principal "I want to implement the Rule: [obj_title]."
        elif obj_type == "club":
            principal "Today I want to put to vote if we want to open a new club at the [obj_school_title]."
            principal "I want to open the [obj_title]."
        elif obj_type == "building" and obj_action == "unlock":
            principal "Today I want to put to vote if we want to restore the [obj_title]."
        elif obj_type == "building" and obj_action == "upgrade":
            principal "Today I want to put to vote if we want to upgrade the [obj_title]."

        $ i = 0
        while i < len(obj_desc):
            $ desc_text = obj_desc[i]
            principal "[desc_text]"
            $ i += 1

        principal "Please cast your vote now."

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
            principal "The vote was successful. The [obj_title] will be implemented."
            $ obj.unlock(obj_school_name, True, True)
        else:
            principal "The vote was unsuccessful. The [obj_title] will not be implemented."

    jump new_daytime
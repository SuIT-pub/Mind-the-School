init python:
    import re
    class Rule:
        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.description = ""
            self.image_path = "images/journal/empty_image.png"
            self.unlocked = {
                "high_school": False,
                "middle_school": False,
                "elementary_school": False,
            }
            self.unlock_conditions = []
        
        def get_name(self):
            return self.name

        def get_title(self):
            return self.title

        def get_type(self):
            return "rule"

        def unlock(self, school):
            if school in self.unlocked:
                self.unlocked[school] = True

        def is_unlocked(self, school):
            if school in self.unlocked:
                return self.unlocked[school]
            else:
                return False

        def is_visible(self, school):
            for condition in self.unlock_conditions:
                if condition.is_blocking(school):
                    return False
            return True

        def can_be_unlocked(self, school):
            if school not in schools.keys():
                return False

            for condition in self.unlock_conditions:
                if condition.is_fullfilled(school):
                    continue
                return False

            return True

    def get_unlocked_rules_by_school(school):
        output = []

        for rule in rules.values():
            if rule.is_unlocked(school) and rule.get_name() not in output:
                output.append(rule.get_name())
        
        return output

    def get_visible_rules_by_school(school, include_unlocked = False):
        output = []

        for rule in rules.values():
            print(str(rule.is_visible(school)) + ":" + str(rule.is_unlocked(school)) + ":" + str(include_unlocked))
            if (rule.is_visible(school) and 
            (not rule.is_unlocked(school) or include_unlocked) and
            rule.name not in output):
                output.append(rule.name)

        print(output)

        return output

    def get_visible_rules(include_unlocked = False):
        output = []

        for rule in rules.values():
            if (rule.is_visible("high_school") and 
            (not rule.is_unlocked("high_school") or include_unlocked) and
            rule.name not in output):
                output.append(rule.name)
                continue
            
            if loli_content >= 1:
                if (rule.is_visible("middle_school") and 
                (not rule.is_unlocked("middle_school") or include_unlocked) and
                rule.name not in output):
                    output.append(rule.name)
                    continue

            if loli_content == 2:
                if (rule.is_visible("elementary_school") and 
                (not rule.is_unlocked("elementary_school") or include_unlocked) and
                rule.name not in output):   
                    output.append(rule.name)
                    continue

        return output

    def get_unlockable_rules():
        output = []

        for rule in rules.values():
            high_unlock = rule.can_be_unlocked("high_school")
            high_unlocked = rule.is_unlocked("high_school")

            if (high_unlock and 
            not high_unlocked and 
            rule.name not in output):
                output.append(rule.name)
                continue

            if loli_content >= 1:
                middle_unlock = rule.can_be_unlocked("middle_school")
                middle_unlocked = rule.is_unlocked("middle_school")

                if (middle_unlock and 
                not middle_unlocked and 
                rule.name not in output):
                    output.append(rule.name)
                    continue

            if loli_content == 2:
                elementary_unlock = rule.can_be_unlocked("elementary_school")
                elementary_unlocked = rule.is_unlocked("elementary_school")

                if (elementary_unlock and 
                not elementary_unlocked and 
                rule.name not in output):
                    output.append(rule.name)
                    continue

        return output

    def get_unlockable_rules_by_school(school):
        output = []

        for rule in rules.values():
            unlock = rule.can_be_unlocked(school)
            unlocked = rule.is_unlocked(school)

            if (unlock and not unlocked and rule.name not in output):
                output.append(rule.name)
                continue

        return output

    def get_rule(rule_name):
        if rule_name not in rules.keys():
            return None
        return rules[rule_name]

    def is_rule_unlocked(rule_name, school):
        if rule_name not in rules.keys():
            return False
        return rules[rule_name].is_unlocked(school)

    def is_rule_visible(rule_name, school):
        if rule_name not in rules.keys():
            return False
        return rules[rule_name].is_visible(school)

    def load_rule(name, title, data = None):
        if name not in rules.keys():
            rules[name] = Rule(name, title)

        rules[name].title = title

        if data != None:
            rules[name].__dict__.update(data)

label load_rules:
    $ load_rule(
        "theoretical_sex_ed", 
        "Theoretical Sex Education",{
            'description': ("Students get a new subject in which they deal with the"
                " topic of the human body and human reproduction."
                " All on a theoretical basis, of course."),
            'unlock_conditions': [
                # LevelCondition("0+"),
                # StatCondition("0+", "corruption"),
                # LockCondition()
            ],
            'image_path': 'images/journal/rules/theoretical_sex_ed.png',
        }
    )
    $ load_rule(
        "theoretical_digital_material", 
        "Digital Material", {
            'description': "The Theoretical Sex Education-Class gets expanded " +
                "by using digital reference material like educational videos " +
                "about reproduction.",
            'unlock_conditions': [
                # LevelCondition("3+"),
                # RuleCondition("theoretical_sex_ed"),
                # LockCondition()
            ],
            'image_path': 'images/journal/rules/theoretical_digital_sex_ed.png',
        }
    )
    $ load_rule(
        "theoretical_teacher_material", 
        "Use Teacher for learning", {
            'description': "The teacher volunteer to use their own bodies to " +
                "give the students the best way to show them the human body.",
            'unlock_conditions': [
                # RuleCondition("theoretical_digital_material"),
                # LockCondition()
            ],
            'image_path': 'images/journal/rules/theoretical_teacher_sex_ed.png',
        }
    )
    $ load_rule(
        "theoretical_student_material", 
        "Use Students for learning", {
            'description': "The students learn about the human body, and the " +
                "differences each individual has, by presenting them with " +
                "their own bodies.\n\nWhile it may be a bit shameful for the " +
                "students, it also is a great way to build some confidence " +
                "over their own bodies and to accept that every body is " +
                "beautiful and should be displayed as such.",
            'unlock_conditions': [
                # RuleCondition("theoretical_teacher_material"),
                # LockCondition()
            ],
            'image_path': 'images/journal/rules/theoretical_student_sex_ed.png',
        }
    )

    $ load_rule(
        "practical_sex_ed", 
        "Practical Sex Education", {
            'description': "Everyone who wanted some hands-on experience " +
                "during Sex Ed now has the chance!\n\nIn the Practical Sex " + 
                "Ed-Classes students now get the chance to experiment " +
                "actively by exploring ways of masturbation. Even though " +
                "it's still limited to self-pleasuring out of safety concerns.",
            'unlock_conditions': [
                # LevelCondition("4+"),
                # RuleCondition("theoretical_sex_ed"),
                # LockCondition()
            ],
            'image_path': 'images/journal/rules/practical_sex_ed.png',
        }
    )

    $ load_rule(
        "practical_teacher_material", 
        "Use Teacher for learning", {
            'description': "The teachers once again volunteer to help give " +
                "the students the best learning experience as possible.\n\n" +
                "Now the students get the opportunity to sexually experiment " +
                "with their teacher. Nobody can teach sex better than someone " +
                "in bed with years of hands-on experience.",
            'unlock_conditions': [
                # LevelCondition("3+"),
                # RuleCondition("practical_sex_ed"),
                # LockCondition()
            ],
            'image_path': 'images/journal/rules/practical_teacher_sex_ed.png',
        }
    )

    $ load_rule(
        "practical_student_material", 
        "Use Students for learning", {
            'description': "After learning from the teachers how to have sex, " +
                "the students now learn how to learn the preferences of your " +
                "sex partner.\nSo the students now get to experiment on " +
                "each other.",
            'unlock_conditions': [
                # RuleCondition("practical_teacher_material"),
                # LockCondition()
            ],
            'image_path': 'images/journal/rules/practical_student_sex_ed.png',
        }
    )

    $ load_rule(
        "student_student_relation", 
        "Students Relations", {
            'description': ("Allows for students to have a relationship between"
                " each other and to openly show it."),
            'unlock_conditions':[
                # LockCondition()
            ]
        }
    )

    $ load_rule(
        "student_teacher_relation", 
        "Students-Teacher Relations", {
            'description': ("Allows for teacher to engage in a relationship with"
                " students."),
            'unlock_conditions':[
                # LockCondition()
            ]
        }
    )

    $ load_rule(
        "relaxed_uniform",
        "Relaxed Uniform", {
            'description': "The students are free to be more relaxed about how to wear the uniform.",
            'unlock_conditions': [

            ],
            'image_path': 'images/journal/rules/relaxed_uniform.png',
        }
    )

    $ load_rule(
        "sexy_uniform",
        "Sexy Uniform", {
            'description': "A new uniform rule with a minimum amount of skin that has to be shown",
            'unlock_conditions': [
                
            ],
            'image_path': 'images/journal/rules/sexy_uniform.png',
        }
    )

    $ load_rule(
        "service_uniform",
        "Service Uniform", {
            'description': "A Uniform designed to make the spontaneous servicing to other students " +
                "more easy by providing as little clothing as possible and " +
                "making the important parts easily accessible.",
            'unlock_conditions': [
                
            ],
            'image_path': 'images/journal/rules/service_uniform.png',
        }
    )

    $ load_rule(
        "nude_uniform",
        "Nude Uniform", {
            'description': "The best uniform there is with covering as little as possible.",
            'unlock_conditions': [
                
            ],
            'image_path': 'images/journal/rules/nude_uniform.png',
        }
    )

    return
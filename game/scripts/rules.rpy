init python:
    import re
    class Rule:
        unlock_conditions = []

        unlocked = {
            "high_school": False,
            "middle_school": False,
            "elementary_school": False,
        }

        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.description = ""
            self.image_path = "images/journal/empty_image.png"
        
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

    def get_visible_rules_by_school(school):
        output = []

        for rule in rules.values():
            if (rule.is_visible(school) and 
            not rule.is_unlocked(school) and
            rule.name not in output):
                output.append(rule.name)
                continue

        return output

    def get_visible_rules():
        output = []

        for rule in rules.values():
            if (rule.is_visible("high_school") and 
            not rule.is_unlocked("high_school") and
            rule.name not in output):
                output.append(rule.name)
                continue
            
            if loli_content >= 1:
                if (rule.is_visible("middle_school") and 
                not rule.is_unlocked("middle_school") and
                rule.name not in output):
                    output.append(rule.name)
                    continue

            if loli_content == 2:
                if (rule.is_visible("elementary_school") and 
                not rule.is_unlocked("elementary_school") and
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
                LevelCondition("0+"),
                StatCondition("0+", "corruption"),
                # LockCondition()
            ],
            'image_path': 'images/journal/rules/theoretical_sex_ed.png',
        }
    )
    $ load_rule(
        "theoretical_digital_material", 
        "Use Digital Material for study in Theoretical Sex Ed",{
            'unlock_conditions': [
                LevelCondition("3+"),
                RuleCondition("theoretical_sex_ed"),
                # LockCondition()
            ],
            'image_path': 'images/journal/rules/theoretical_digital_sex_ed.png',
        }
    )
    $ load_rule(
        "theoretical_teacher_material", 
        "Use Teacher for study in Theoretical Sex Ed", {
            'unlock_conditions': [
                RuleCondition("theoretical_digital_material"),
                # LockCondition()
            ],
            'image_path': 'images/journal/rules/theoretical_teacher_sex_ed.png',
        }
    )
    $ load_rule(
        "theoretical_student_material", 
        "Use Students for study in Theoretical Sex Ed", {
            'unlock_conditions': [
                RuleCondition("theoretical_teacher_material"),
                # LockCondition()
            ]
        }
    )

    $ load_rule(
        "practical_sex_ed", 
        "Practical Sex Education", {
            'unlock_conditions': [
                LevelCondition("4+"),
                RuleCondition("theoretical_sex_ed"),
                # LockCondition()
            ]
        }
    )

    $ load_rule(
        "practical_teacher_material", 
        "Use Teacher for study in Practical Sex Ed", {
            'unlock_conditions': [
                LevelCondition("3+"),
                RuleCondition("practical_sex_ed"),
                # LockCondition()
            ]
        }
    )

    $ load_rule(
        "practical_student_material", 
        "Use Students for study in Practical Sex Ed", {
            'unlock_conditions': [
                RuleCondition("practical_teacher_material"),
                # LockCondition()
            ]
        }
    )

    $ load_rule(
        "student_student_relation", 
        "Allowed Relationships between Students", {
            'description': ("Allows for students to have a relationship between"
                " each other and to openly show it."),
            'unlock_conditions':[
                # LockCondition()
            ]
        }
    )

    $ load_rule(
        "student_teacher_relation", 
        "Allowed Relationships between Students and Teacher", {
            'description': ("Allows for teacher to engage in a relationship with"
                " students."),
            'unlock_conditions':[
                # LockCondition()
            ]
        }
    )

    return
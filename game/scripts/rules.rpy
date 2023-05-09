init python:
    import re
    class Rule:
        unlock_conditions = []

        unlocked = {
            "high_school": False,
            "middle_school": False,
            "middle_school": False,
        }

        def __init__(self, name, title):
            self.name = name
            self.title = title
        
        def canBeUnlocked(self, school):
            print("test")
            for condition in self.unlock_conditions:
                if condition["type"] == "stat":
                    stat = condition["stat"]
                    value = condition["value"]

                    if (schools[school].stats[stat] == value or 
                        str(schools[school].stats[stat]) == value):
                        continue

                    value_num_l = re.findall('\d+', value)
                    if value_num_l:
                        value_num = int(''.join(value_num_l))

                        if ((value.endswith('+') and schools[school].stats[stat] >= value_num) or
                            (value.endswith('-') and schools[school].stats[stat] <= value_num)):
                                continue
                        else:
                            if '-' in value:
                                if (len(value_num_l) == 2 and 
                                    value_num_l[0].isdecimal() and 
                                    value_num_l[1].isdecimal() and
                                    int(value_num_l[0]) <= schools[school].stats[stat] <= int(value_num_l[1])
                                ):
                                    continue
                            elif ',' in value:
                                if str(schools[school].stats[stat]) in value_num_l:
                                    continue
                if condition["type"] == "unlocked":
                    value = condition["rule"]
                    if rules[value].unlocked[school]:
                        continue
                if condition["type"] == "level":
                    stat = condition["stat"]
                    value = condition["value"]

                    print("stat: " + stat + " value: " + value + " level: " + level_to_string(stat, school))

                    if level_to_num(stat, school) == value or level_to_string(stat, school) == value:
                        continue

                    value_num_l = re.findall('\d+', value)
                    if value_num_l:
                        value_num = int(''.join(value_num_l))

                        if ((value.endswith('+') and level_to_num(stat, school) >= value_num) or
                            (value.endswith('-') and level_to_num(stat, school) <= value_num)):
                                continue
                        else:
                            if '-' in value:
                                if (len(value_num_l) == 2 and 
                                    value_num_l[0].isdecimal() and 
                                    value_num_l[1].isdecimal() and
                                    int(value_num_l[0]) <= level_to_num(stat, school) <= int(value_num_l[1])
                                ):
                                    continue
                            elif ',' in value:
                                if level_to_string(stat, school) in value_num_l:
                                    continue
                return False
            return True

label load_rules:
    if "theoretical_sex_ed" not in rules.keys():
        $ rules["theoretical_sex_ed"] = Rule("theoretical_sex_ed", "Theoretical Sex Education")
    $ rules["theoretical_sex_ed"].__dict__.update({
        'unlock_conditions': [
            {
                "type": "level",
                "stat": "high_school",
                "value": "2+",
            },
        ]
    })
    if "theoretical_digital_material" not in rules.keys():
        $ rules["theoretical_digital_material"] = Rule("theoretical_digital_material", "Use Digital Material for study in Theoretical Sex Ed")
    $ rules["theoretical_digital_material"].__dict__.update({
        'unlock_conditions': [
            {
                "type": "level",
                "stat": "high_school",
                "value": "3+",
            },
            {
                "type": "unlocked",
                "rule": "theoretical_sex_ed",
            }
        ]
    })
    if "theoretical_teacher_material" not in rules.keys():
        $ rules["theoretical_teacher_material"] = Rule("theoretical_teacher_material", "Use Teacher for study in Theoretical Sex Ed")
    $ rules["theoretical_teacher_material"].__dict__.update({
        'unlock_conditions': [
            {
                "type": "unlocked",
                "rule": "theoretical_digital_material",
            }
        ]
    })
    if "theoretical_student_material" not in rules.keys():
        $ rules["theoretical_student_material"] = Rule("theoretical_student_material", "Use Students for study in Theoretical Sex Ed")
    $ rules["theoretical_student_material"].__dict__.update({
        'unlock_conditions': [
            {
                "type": "unlocked",
                "rule": "theoretical_teacher_material",
            }
        ]
    })

    if "practical_sex_ed" not in rules.keys():
        $ rules["practical_sex_ed"] = Rule("practical_sex_ed", "Practical Sex Education")
    $ rules["practical_sex_ed"].__dict__.update({
        'unlock_conditions': [
            {
                "type": "level",
                "stat": "high_school",
                "value": "4+",
            },
        ]
    })

    if "practical_teacher_material" not in rules.keys():
        $ rules["practical_teacher_material"] = Rule("practical_teacher_material", "Use Teacher for study in Practical Sex Ed")
    $ rules["practical_teacher_material"].__dict__.update({
        'unlock_conditions': [
            {
                "type": "level",
                "stat": "high_school",
                "value": "3+",
            },
            {
                "type": "unlocked",
                "rule": "practical_sex_ed",
            }
        ]
    })

    if "practical_student_material" not in rules.keys():
        $ rules["practical_student_material"] = Rule("practical_student_material", "Use Students for study in Practical Sex Ed")
    $ rules["practical_student_material"].__dict__.update({
        'unlock_conditions': [
            {
                "type": "unlocked",
                "rule": "practical_teacher_material",
            }
        ]
    })

    if "student_student_relation" not in rules.keys():
        $ rules["student_student_relation"] = Rule("student_student_relation", "Allowed Relationships between Students")

    if "student_teacher_relation" not in rules.keys():
        $ rules["student_teacher_relation"] = Rule("student_teacher_relation", "Allowed Relationships between Students and Teacher")
    
    return
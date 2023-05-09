screen modular_assembly_view(background, student_var):
    add "background/[background].png"

    add "gym/high_school_[high_school_lvl]_[background]_[student_var].png"
    if loli_content >= 1:
        add "gym/middle_school_[high_school_lvl]_[background]_[student_var].png"
    if loli_content == 2:
        add "gym/elementary_school_[high_school_lvl]_[background]_[student_var].png"

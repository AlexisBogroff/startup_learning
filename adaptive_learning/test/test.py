from adaptive_learning import quiz

"""
Tested functions:
    
    # Manage users
    test_add_group_permission
    test_delete_group_permission
    test_register_teacher
    test_register_admin
    test_register_student
    test_login

    # Manage Exams
    # ------------
    
    ## Build exams
    test_create_exam
    test_delete_exam
    test_modify_exam
    test_get_question
    test_get_answer
    test_set_question
    test_set_answer
    test_check_answer_is_correct
    test_set_difficulty
    test_get_difficulty
    test_set_category
    test_get_category
    test_delete_difficulty
    
    ## Timer 
    test_teacher_start_timer
    test_teacher_stop_timer
    test_teacher_modify_timer
    test_timer_ended
    test_get_timer_initial_time
    test_get_timer_remaining_time
    test_get_timer_end_time
    test_get_timer_time_limit
    
    ## Exam conditions
    test_set_datetime_exam_beginning
    test_set_datetime_exam_end
    test_get_datetime_exam_beginning
    test_get_datetime_exam_end
    test_delete_datetime_exam_beginning
    test_delete_datetime_exam_end
    
    ## During the exam
    test_exam_started
    test_exam_ended
    test_compare_now_with_datetime_beginning
    test_compare_now_with_datetime_end
    test_get_answer
    test_get_question
    test_get_time_student_submitted_question
    test_compute_time_student_spent_on_question
    test_get_time_student_started
    test_get_time_student_ended

    ## After the exam
    test_correction_question_auto
    test_compute_student_grade

    ## Exam statistics
    test_compute_exam_min_grade
    test_compute_exam_max_grade
    test_compute_exam_average_grade
    test_compute_exam_median_grade
    test_compute_exam_frequencies
    test_compute_question_min_grade
    test_compute_question_max_grade
    test_compute_question_average_grade
    test_compute_question_frequencies
    test_get_answer_frequencies
    
    ## Exam plots
    test_plot_student_grade_by_question_on_the_exam
    test_plot_grades_of_student_on_all_exams
    test_plot_barplot_grades_exam_by_group
    test_plot_radar_of_student_grades_by_sections_on_the_exam


    # Student
    # -------

    ## Profile / Progression
    test_plot_radar_of_student_strenghts_by_subject

    # Algorithms
    # ----------

    # Create test
    test_algo_create_exam
"""

"""
Main test file for adaptive learning engine

Tested functions:

    # Manage users
    test_register_admin  # I/O ?
    test_register_teacher
    test_register_student
    registering_user_can_be_admin
    registering_user_can_be_teacher
    registering_user_can_be_student
    test_create_group
    test_delete_group
    test_add_group_permission
    test_delete_group_permission
    test_set_user_group
    test_student_can_integrate_this_group
    test_student_is_from_this_school
    test_delete_user_group
    test_login
    test_logout
    test_student_is_recognized
    test_get_school_mail_domain
    test_extract_mail_domain
    test_set_user_rights
    test_get_user_rights


    # Manage Exams
    # ------------

    ## Build exams
    test_create_exam
    test_delete_exam
    test_modify_exam
    test_randomize_sections_order
    test_randomize_questions_order
    test_create_question
    test_create_answer
    test_delete_question
    test_delete_answer
    test_add_question_to_test
    test_remove_question_from_test
    test_get_answer_text
    test_set_answer_text
    test_set_answer_grade
    test_get_answer_grade
    test_update_answer_text
    test_update_answer_grade
    test_update_question_text
    test_set_question_creation_datetime
    test_set_bool_answer_is_correct
    test_get_bool_answer_is_correct
    test_set_question_difficulty
    test_get_question_difficulty
    test_set_question_category
    test_get_question_category
    test_delete_question_difficulty
    test_set_exam_keyword
    test_delete_exam_keyword
    test_create_category
    test_delete_category
    test_set_category_parent
    test_delete_category_parent
    test_get_category_children
    test_create_section
    test_delete_section
    test_add_question_to_section
    test_delete_question_of_section
    test_get_section_questions
    test_set_section_description
    test_get_section_description
    test_set_exam_description
    test_get_exam_description
    test_compute_exam_max_grade
    test_get_exam_max_grade
    test_set_exam_max_grade
    test_set_question_grade
    test_get_question_grade
    test_set_bool_use_this_question
    test_get_bool_use_this_question
    test_set_question_text
    test_get_question_text

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
    test_check_student_answer_is_correct
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
    test_should_revise_question
    test_should_revise_subject


    # Algorithms
    # ----------

    # Create test
    test_algo_create_exam
    test_algo_predict_student_exam_grade
    test_algo_predict_student_answer_is_correct
    test_algo_predict_student_subject_grade
    test_algo_predict_student_progression
    test_algo_predict_student_similarity

    test_compute_students_similarity

"""
import unittest
from unittest.mock import patch
from adaptive_learning import exam
from adaptive_learning import user


class ExamRelatedMethodsTestCase(unittest.TestCase):
    """
    Test the manipulations on exams, questions, answers
    (create, amend, delete, launch, etc.)
    """
    INPUTS_ANSWER = ('txt_answer_1', 'True', 'True')
    INPUTS_QUESTION = ('txt_question_1', 'mcq', 'True',
                       '2', '3', 'programming, loops',
                       'num correct answers', 'True')


    @patch('builtins.input', side_effect=INPUTS_ANSWER)
    def test_create_answer(self, mock_inputs):
        expected_answer = {
            'text': 'txt_answer_1',
            'is_correct': 'True',
            'use_answer': 'True',
        }
        obtained_answer = exam.create_answer()
        self.assertEqual(expected_answer, obtained_answer)


    @patch('builtins.input', side_effect=INPUTS_QUESTION)
    def test_create_question(self, mock_inputs):
        expected_question = {
            'text': 'txt_question_1',
            'format': 'mcq',
            'use_question': 'True',
            'nb_points': '2',
            'difficulty': '3',
            'keywords': 'programming, loops',
            'notif_correct_answers': 'num correct answers',
            'randomize_answers_order': 'True',
        }
        obtained_question = exam.create_question()
        self.assertEqual(expected_question, obtained_question)



class ExamTestCase(unittest.TestCase):
    """
    Test the creation of an exam
    """
    def setUp(self):
        self.exam = exam.Exam('Initial title')

    def test_default_grade_base(self):
        self.assertEqual(self.exam.grade_base, 20)

    def test_default_auto_rebase_grade(self):
        self.assertTrue(self.exam.auto_rebase_grade)

    def test_default_randomize_question_order(self):
        self.assertTrue(self.exam.randomize_questions_order)


    INPUT_PROPERTIES = ('new exam title',
                        'new description',
                        'False',
                        'False',
                        '10')

    @patch('builtins.input', side_effect=INPUT_PROPERTIES)
    def test_set_properties(self, mock_inputs):
        self.exam.set_properties()
        self.assertEqual(self.exam.title, 'new exam title')
        self.assertEqual(self.exam.description, 'new description')
        self.assertEqual(self.exam.randomize_questions_order, False)
        self.assertEqual(self.exam.auto_rebase_grade, False)
        self.assertEqual(self.exam.grade_base, 10)



class UserMethodsTestCase(unittest.TestCase):
    """
    Test the user methods
    """
    def test_extract_mail_domain(self):
        expected_domain = 'univ-paris1.fr'
        mail_address = 'test_mail-pi@univ-paris1.fr'
        obtained_domain = user.extract_mail_domain(mail_address)
        self.assertEqual(expected_domain, obtained_domain)


    def test_get_school_mail_domain(self):
        school_mail_domain_1 = user.get_school_mail_domain('paris1')
        school_mail_domain_2 = user.get_school_mail_domain('esilv')
        self.assertEqual(school_mail_domain_1, 'univ-paris1.fr')
        self.assertEqual(school_mail_domain_2, 'edu.devinci.fr')


    def test_student_is_from_this_school(self):
        school_name = 'paris1'
        student_mail = 'stu_1@univ-paris1.fr'
        is_from_this_school = user.student_is_from_this_school(
            student_mail,
            school_name)
        self.assertTrue(is_from_this_school)


    # def test_set_user_rights(self):
    #     user_wit_no_home_access = create_user()
    #     user_wit_no_home_access.set_right('access', 'home')
    #     bool_has_home_access = user_wit_no_home_access.has_right(
    #                               'access',
    #                               'home')
    #     self.assertTrue(bool_has_home_access)


if __name__ == '__main__':
    unittest.main()

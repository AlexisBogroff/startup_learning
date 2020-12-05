"""
Manage exams, questions and answers
"""
from adaptive_learning.funcs import get_input


def create_question():
    """
    Create a question

    It is important to fill the 'keywords' argument, since it enables
    the filtering of questions on these keywords when building exams

    Returns:
        the question dictonary
    """
    question = {}
    question['text'] = get_input("Enter the question text")
    question['format'] = get_input("Enter the question format")
    question['use_question'] = get_input("Use this question? (True/False)")
    question['nb_points'] = get_input("Enter the number of points")
    question['difficulty'] = get_input("Enter the difficulty")
    question['keywords'] = get_input("Enter keywords, subject, or categories")
    question['notif_correct_answers'] = get_input("Inform num correct answers?")
    question['randomize_answers_order'] = get_input("Randomize answers order?")
    return question


def create_answer():
    """
    Create an answer

    Returns:
        the answer dictionary
    """
    answer = {}
    answer['text'] = get_input("Enter the answer text")
    answer['is_correct'] = get_input("Is the answer correct? (True/False)")
    answer['use_answer'] = get_input("Do use this answer? (True/False)")
    return answer


def create_exam():
    """
    Create an exam

    The exam 'grade_base' enables to obtain a grade on e.g. /20, although there
    are only e.g. 10 questions graded /1 point.

    Returns:
        the exam dictionary
    """
    exam_ = {}
    exam_['title'] = get_input("Enter the exam title")
    exam_['description'] = get_input("Enter the exam description")
    exam_['grade_base'] = get_input("Enter the grade base")
    exam_['randomize_questions_order'] = get_input("Randomize questions order?")
    return exam_

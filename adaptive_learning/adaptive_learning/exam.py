"""
Manage exams, questions and answers
"""
from adaptive_learning.funcs import get_input


def create_question():
    """
    Create a question
    """
    question = {}
    question['text'] = get_input("Enter the question text")
    question['format'] = get_input("Enter the question format")
    question['use_question'] = get_input("Use this question? (True/False)")
    question['nb_points'] = get_input("Enter the number of points")
    question['difficulty'] = get_input("Enter the difficulty")
    question['keywords'] = get_input("Enter keywords, subject, or categories")
    question['notif_correct_answers'] = get_input("Inform on correct answers?")
    return question


def create_answer():
    """
    Create an answer

    Returns:
        the different elements composing a standard answer
    """
    answer = {}
    answer['text'] = get_input("Enter the answer text")
    answer['format'] = get_input("Enter the answer format")
    answer['text'] = get_input("Is the answer correct? (True/False)")
    return answer


def create_exam():
    """
    Create an exam
    """
    raise NotImplementedError


if __name__ == "__main__":
    create_question()
    create_answer()

"""
Manage exams, questions and answers
"""
from adaptive_learning.funcs import get_input


def create_question():
    """
    Create a question
    """
    data_structure_along_prompt_messages = {
        "text": "Enter the question text",
        "format": "Enter the question format",
        "use_question": "Use this question? (True/False)",
        "nb_points": "Enter the number of points",
        "difficulty": "Enter the difficulty",
        "keywords": "Enter keywords like the subject, categories, etc.",
        "type_notif_correct_answers": "Enter the type of notification related"\
                                      " to the number of correct answers",
    }
    question_data = get_input(data_structure_along_prompt_messages)
    return question_data


def create_answer():
    """
    Create an answer

    Returns:
        the different elements composing an answer
    """
    data_structure_along_prompt_messages = {
        "text": "Enter the answer text",
        "format": "Enter the answer format",
        "is_correct": "Is the answer correct? (True/False)",
    }
    answer_data = get_input(data_structure_along_prompt_messages)
    return answer_data


def create_exam():
    """
    Create an exam
    """
    raise NotImplementedError


if __name__ == "__main__":
    create_question()
    create_answer()

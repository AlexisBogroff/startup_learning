"""
Manage answers
"""
from adaptive_learning.questionnaires import funcs
from adaptive_learning.questionnaires.funcs import cast, get_input


class Answer:
    """
    Class to manage answers
    """
    def __init__(self):
        self.text = ''
        self.is_correct = False
        self.use_answer = True


    def set_properties_from_input(self):
        """
        Create an answer

        Returns:
            None, it modifies the answer properties.
        """
        self.set_text_from_input()
        self.set_is_correct_from_input()
        self.set_use_answer_from_input()


    def set_text_from_input(self):
        """ Set is_correct property """
        self.text = get_input("Enter the answer text")


    def set_is_correct_from_input(self):
        """ Set is_correct property """
        is_correct = get_input("Is the answer correct? (True/False)")
        casted_is_correct = cast(is_correct, bool)
        self.is_correct = casted_is_correct


    def set_use_answer_from_input(self):
        """ Set use_answer property """
        use_answer = get_input("Use this answer? (True/False)")
        casted_use_answer = cast(use_answer, bool)
        self.use_answer = casted_use_answer


    def get_exportable(self):
        """
        Stores the answer properties in a dictionary

        Returns:
            the data in dic format, ready to be added to the list of answers
            of a question.
        """
        data_export = {
            'text': self.text,
            'is_correct': self.is_correct,
            'use_answer': self.use_answer,
        }
        return data_export

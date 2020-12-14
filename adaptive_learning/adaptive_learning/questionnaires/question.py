"""
Manage questions
"""
from adaptive_learning.questionnaires import funcs
from adaptive_learning.questionnaires.funcs import cast, get_input
from adaptive_learning.questionnaires.answer import Answer

__PATH_QUESTIONS__ = "/Users/Pro/git_repositories/"\
    "adaptive_learning/adaptive_learning/adaptive_learning/"\
    "data/table_questions.txt"


class Question:
    """
    Class for the questions

    They can be dealt independently (of exams) or be called in the creation
    of an exam. Answers however are only called within a question.
    """
    def __init__(self):
        self._id = ''
        self.text = ''
        self.type = ''
        self.keywords = ''  # TODO: transform into a list
        self.use_question = True
        self.nb_points = 1.
        self.difficulty = 1
        self.notif_correct_answers = True
        self.notif_num_exact_answers = False
        self.randomize_answers_order = True
        self.answers = []


    def __str__(self):
        return "text: {text}, id: {id}".format(text=self.text, id=self._id)


    def add_answer(self):
        """
        Create and add an answer to the current question
        """
        answer = Answer()
        answer.set_properties_from_input()
        answer_export = answer.get_exportable()
        answer_export['position_id'] = funcs.generate_position_id(self.answers)
        self.answers.append(answer_export)


    def get_exportable(self):
        """
        Stores the question properties in a dictionary

        Returns:
            the data in dic format, ready to export in json file
        """
        data_export = {
            'id': self._id,
            'text': self.text,
            'type': self.type,
            'keywords': self.keywords,
            'use_question': self.use_question,
            'nb_points': self.nb_points,
            'difficulty': self.difficulty,
            'notif_correct_answers': self.notif_correct_answers,
            'notif_num_exact_answers': self.notif_num_exact_answers,
            'randomize_answers_order': self.randomize_answers_order,
            'answers': self.answers,
        }
        return data_export


    def load_question(self, id_question):
        """
        Load a specific question from the questions library

        Modifies the properties of the current question to correspond to the
        selected question.

        Returns:
            void.
        """
        question = funcs.retrieve_sample_from_table(id_question,
                                                         __PATH_QUESTIONS__)
        self.set_question_from_existing(question)


    def save_new_to_db(self):
        """
        Stores the question in database

        It inserts the new content at the end of the file,
        on a new line, and takes a single line (each in json like format)

        Method should be executed one time only, when finished with the creation
        of the question. Otherwise, the question would be stored (with a new id)
        each time save method would be called.

        Notes:
            To increase performances, each question is stored in json format,
            even though the file is in text format.
            This enables to store new questions by appending them in the first
            empty rows, without the need to read and parse the whole file
            (which would be the case with a json file).
        """
        self._id = funcs.generate_uuid()
        question_dump = self.get_exportable()
        funcs.append_to_file(question_dump, __PATH_QUESTIONS__)


    def set_parameters_from_input_extra(self):
        """
        Set question parameters

        These parameters all have a default value, and their manual setting
        is not necessary.

        It is important to fill the 'keywords' argument, since it enables
        the filtering of questions on these keywords when building exams. It
        is a rich data for algorithms.

        Notes:
            use_question: bool
            nb_points: float
            difficulty: int
            notif_correct_answers: bool:
            - False (informs that question has one or multiple correct answers)
            - True (informs wether question has multiple correct answers or not)
            notif_num_exact_answers: bool (only if notif_correct_answers is True)
            randomize_answers_order: bool
        """
        # Get informations from user input
        self.use_question = get_input("Use this question?")
        self.nb_points = get_input("Enter the number of points")
        self.difficulty = get_input("Enter the difficulty")
        self.notif_correct_answers = get_input("Inform on num of answers?")
        self.notif_num_exact_answers = get_input("Inform exact num?")
        self.randomize_answers_order = get_input("Randomize answers order?")

        # Cast variables to expected type
        self.use_question = cast(self.use_question, bool)
        self.nb_points = cast(self.nb_points, float)
        self.difficulty = cast(self.difficulty, int)
        self.notif_correct_answers = cast(self.notif_correct_answers, bool)
        self.notif_num_exact_answers = cast(self.notif_num_exact_answers, bool)
        self.randomize_answers_order = cast(self.randomize_answers_order, bool)


    def create_question(self):
        """
        Create question

        Some parameters are add with their default value

        Notes:
            text: string
            type: string, can be:
            - mcq (single or mulitple correct answers)
            - exact
            - develop (developpement answer that can hardly be auto-corrected)
            keywords: string with comma separated words
        """
        self.text = get_input("Enter the question text")
        self.type = get_input("Enter the question type")
        self.keywords = get_input("Enter keywords, subject, or categories")


    def set_question_from_existing(self, question):
        """ Set properties from an existing question """
        self._id = question['id']
        self.text = question['text']
        self.type = question['type']
        self.keywords = question['keywords']
        self.use_question = question['use_question']
        self.nb_points = question['nb_points']
        self.difficulty = question['difficulty']
        self.notif_correct_answers = question['notif_correct_answers']
        self.notif_num_exact_answers = question['notif_num_exact_answers']
        self.randomize_answers_order = question['randomize_answers_order']
        self.answers = question['answers']


    def show(self):
        """
        Display the question properties

        TODO: split into multiple functions
        """
        answers = self.answers
        if answers:
            text_answers = ["{}".format(ans) for ans in answers]
            text_answers = "\n\t".join(text_answers)
        else:
            text_answers = "No answer registered"

        text = "id: {id}\n" \
               "text: {text}\n" \
               "type: {type}\n" \
               "keywords: {keywords}\n\n" \
               "use_question: {use_question}\n" \
               "nb_points: {nb_points}\n" \
               "difficulty: {difficulty}\n" \
               "notif_correct_answers: {notif_correct_answers}\n" \
               "notif_num_exact_answers: {notif_num_exact_answers}\n" \
               "randomize_answers_order: {randomize_answers_order}\n\n" \
               "answers\n" \
               "\t{text_answers}" \
               .format(
                    id=self._id,
                    text=self.text,
                    type=self.type,
                    keywords=self.keywords,
                    use_question=self.use_question,
                    nb_points=self.nb_points,
                    difficulty=self.difficulty,
                    notif_correct_answers=self.notif_correct_answers,
                    notif_num_exact_answers=self.notif_num_exact_answers,
                    randomize_answers_order=self.randomize_answers_order,
                    text_answers=text_answers,
                )
        print(text)


    @staticmethod
    def show_list_of_questions():
        """ Display the list of questions stored in db """
        table = funcs.load_table(f_path=__PATH_QUESTIONS__)
        funcs.show_table(table, ['text', 'id'])


class MCQ(Question):
    """
    Manage MCQ

    Automatic grading system
    """
    pass



class Dev(Question):
    """
    Manage questions with development

    Teacher must set the grade
    """
    pass



class Exact(Question):
    """
    Manage questions with exact answers

    Automatic grading system
    """
    pass



class Approx(Question):
    """
    Manage questions with approximated answers considered correct

    Automatic grading system
    """
    pass



class Code(Question):
    """
    Manage questions with code as answers

    Semi-automatic grading system
    """
    pass

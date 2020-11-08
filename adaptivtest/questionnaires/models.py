"""
Models for the storing of data related to tests, questions, answers
along with their corresponding categories.

Classes:
    Answers: correct and incorrect but plausible answers
    classified by category

    Categories: knowledge base of the categories with the links between
    parent and child categories.

    Parameters: static table storing constants for secondary keys

    Questions: questions along with their correct and plausible answers,
    and linked to a category

    Mcqs: tests for learners in the form of multiple choices questions
"""

import uuid
from django.db import models


class Answers(models.Model):
    """
    Answers that will either be used as correct answers or incorrect but
    plausible answers in the question model.

    These answers are linked via the id of the category to which they
    belong. Each answer can belong to one category only, and an answer
    with the same text but for a different category will require another
    entry in the answer model.

    Fields:
        text: the text of the question that will be seen by the learner

        id_parent_category: TODO:alexis(alexis.bogroff@gmail.com)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(null=False)
    id_parent_category = models.CharField(max_length=36, null=False)


class Categories(models.Model):
    """
    Categories that will be used in the question model. These can be
    anything from a general subject to a very specific domain of
    expertise.

    These categories are linked via the id of their parent category.
    Each parent can have multiple children, thus building a knowledge
    base.

    Fields:
        name: name of the category

        id_parent_category: id of the single and more precise parent category
        containing the current child category. If a category name have
        multiple parents, it should be duplicated for each parent.
        e.g.: 'functions' would have multiple parents 'fundamentals', 'vba',
        'python', etc., hence one entry should exist for each of these parents,
        so that referencing to 'functions' would require to specify which
        'functions' we are referencing to, by using its specific id.

    TODO:alexis(alexis.bogroff@gmail.com): reformulate id_parent_category definition
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, null=False)
    id_parent_category = models.CharField(max_length=36, null=False)


class Mcqs(models.Model):
    """
    Tests for learners in the form of multiple choices questions, built
    as a pointer to a selection of questions

    Fields:
        title: name of the quizz

        id_questions: list of id_questions that are used in the quizz
    """
    title = models.CharField(max_length=40, null=False)
    id_questions = models.TextField(null=False)


class Parameters(models.Model):
    """
    Static table storing constants for secondary keys

    Fields:
        question_level_in_months_of_study: the level of the question defined
        as the average experience required (in months) to understand it.
    """
    id = models.AutoField(primary_key=True)
    question_level_in_months_of_study = models.IntegerField(
        unique=True,
        null=False)


class Questions(models.Model):
    """
    Questions along with their correct and plausible answers,
    and linked to a category.

    The answers_incorrect_plausible should be in great number
    in order to produce many different quizzes on the same question.

    Fields:
        text: text of the question

        question_level: difficulty of the question,
        counted in months of study required on average to to understand it.

        answers_correct: answers defined as good for the question.

        answers_incorrect_plausible: answers defined as wrong but
        are plausible enough to confuse the learner.

        categories: direct and most precise categories of the question.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(null=False)
    question_level = models.IntegerChoices('level_in_month', '0 1 3 6 12 18 24 36 48')
    answers_correct = models.TextField(null=False)
    answers_incorrect_plausible = models.TextField(null=False)
    categories = models.TextField(null=False)

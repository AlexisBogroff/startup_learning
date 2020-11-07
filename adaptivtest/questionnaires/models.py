import uuid
from django.db import models

class Parameters(models.Model):
    question_level_in_months_of_study = models.CharField(max_length=10)

class Categories(models.Model):
    """
    Categories that will be used in the question model. These can be
    anything from a general subject to a very specific domain of
    expertise.

    These categories are linked via the id of their parent category.
    Each parent can have multiple children, thus building a knowledge 
    base.

    Args:
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
    name = models.CharField(max_length=40)
    id_parent_category = models.CharField(max_length=36)

class Answers(models.Model):
    """
    Answers that will either be used as correct answers or incorrect but 
    plausible answers in the question model.

    These answers are linked via the id of the category to which they
    belong. Each answer can belong to one category only, and an answer
    with the same text but for a different category will require another
    entry in the answer model.

    Args:
        text: the text of the question that will be seen by the learner
        id_parent_category: 
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    id_parent_category = models.CharField(max_length=36)

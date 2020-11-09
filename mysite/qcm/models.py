from django.db import models
from django.conf import settings


class Categories(models.Model):
    categorie_name=models.CharField(max_length=200)
    categorie_link=models.ManyToManyField("self", models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.categorie_name

class Reponse(models.Model):
    reponse_text=models.CharField(max_length=200)
    reponse_categorie=models.ManyToManyField(Categories,null=True)

    def __str__(self):
        return self.reponse_text
  

class Question(models.Model):

    LEVEL=(('Debutant','Debutant'),
     ('Intermediaire','Intermediaire'),
     ('Difficile','Difficile'),
     ('Extreme','Extreme')
    )

    question_text=models.CharField(max_length=200,null=True)
    question_level=models.CharField(max_length=200,choices=LEVEL)
    question_true_reponse=models.ManyToManyField(Reponse, related_name='true')
    question_false_reponse=models.ManyToManyField(Reponse, related_name='false')
    question_categorie=models.ManyToManyField(Categories)

    def __str__(self):
        return self.question_text

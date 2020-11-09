from django.contrib import admin

from .models import Reponse, Question, Categories


admin.site.register(Question)
admin.site.register(Reponse)
admin.site.register(Categories)


from django.contrib import admin
from .models import Answers, Categories, Mcqs, Parameters, Questions

admin.site.register(Answers)
admin.site.register(Categories)
admin.site.register(Mcqs)
admin.site.register(Parameters)
admin.site.register(Questions)

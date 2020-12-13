from django.contrib import admin
from .models import (
    DynMCQInfo,
    DynMCQquestion,
    DynMCQanswer,
    PassDynMCQTest,
    PassDynMCQTestInfo,
    Dynquestion,
    PassDynquestionTest,
    )

# Register your models here.
admin.site.register(DynMCQInfo)
admin.site.register(DynMCQquestion)
admin.site.register(DynMCQanswer)
admin.site.register(PassDynMCQTest)
admin.site.register(PassDynMCQTestInfo)
admin.site.register(Dynquestion)
admin.site.register(PassDynquestionTest)

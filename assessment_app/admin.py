from django.contrib import admin
from django import forms

from .models import *

class TextArea(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'description': forms.Textarea}
        return super().get_form(request, obj, **kwargs)

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(PrizesGot)
admin.site.register(PrizeName, TextArea)
admin.site.register(Department)
admin.site.register(FormSample, TextArea)
admin.site.register(FormAnswerS)
admin.site.register(Course)
admin.site.register(Questions)
admin.site.register(QuestionType)
admin.site.register(Term)
admin.site.register(CourseName)
admin.site.register(Images)
admin.site.register(IDNumbers)
admin.site.register(ClosedAnswer)
admin.site.register(ClosedAnswerValue)

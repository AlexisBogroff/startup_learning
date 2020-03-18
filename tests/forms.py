from django import forms
from .models import (
	DynMCQInfo,
	DynMCQquestion,
	DynMCQanswer,
	Pass_DynMCQTest,
	Pass_DynMCQTest_Info,
	Dynquestion,
	Pass_DynquestionTest,
)

from .backend_code import compare_input_wt_expected as compare
		
class DynMCQTestInfoForm(forms.ModelForm):
	id_test = forms.CharField(required=True)
	title = forms.CharField(required=True)
	class Meta:
		model = DynMCQInfo
		fields = [
			'id_test',
			'title',
		]

class DynMCQTestInfoForm_questions(forms.ModelForm):
	questions = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = DynMCQInfo
		fields = [
			'questions',
		]
	
class DynMCQTestInfoForm_launch(forms.ModelForm):
	activated_for = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
	time = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'mm:ss'}))

	class Meta:
		model = DynMCQInfo
		fields = [
			'time',
			'activated_for',
		]
		
class MCQQuestion_difficulty_form(forms.ModelForm):
	difficulty = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
	class Meta:
		model = DynMCQquestion
		fields = [
			'difficulty',
		]
		
class Question_difficulty_form(forms.ModelForm):
	difficulty = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
	class Meta:
		model = Dynquestion
		fields = [
			'difficulty',
		]
		
class DynMCQquestionForm(forms.ModelForm):
	# Properly displayed
	q_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	nb_ans = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':25}))
	activated = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0 if no, 1 if yes'}))

	# Robustly Handled
	class Meta:
		model = DynMCQquestion
		fields = [
			'q_text',
			'nb_ans',
			'activated',
		]
		
class DynquestionForm(forms.ModelForm):
	# Properly displayed
	q_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	r_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':25}))
	activated = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0 if no, 1 if yes'}))

	# Robustly Handled
	class Meta:
		model = Dynquestion
		fields = [
			'q_text',
			'r_text',
			'activated',
		]
		
class DynMCQquestionForm_question(forms.ModelForm):
	# Properly displayed
	q_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	activated = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0 if no, 1 if yes'}))

	# Robustly Handled
	class Meta:
		model = DynMCQquestion
		fields = [
			'q_text',
			'activated',
		]

class DynMCQanswerForm(forms.ModelForm):
	# Properly displayed
	ans_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	right_ans = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0 if no, 1 if yes'}))
	
	# Robustly Handled
	class Meta:
		model = DynMCQanswer
		fields = [
			'ans_text',
			'right_ans',
		]

class Pass_DynMCQTestForm(forms.ModelForm):
	r_ans = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = Pass_DynMCQTest
		fields = [
			'r_ans',
		]
		
class Pass_DynquestionTestForm(forms.ModelForm):
	r_answer = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':25}))

	class Meta:
		model = Pass_DynquestionTest
		fields = [
			'r_answer',
		]
		
class Pass_DynMCQTestInfoForm(forms.ModelForm):
	id_student = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Student ID'}))

	class Meta:
		model = Pass_DynMCQTest_Info
		fields = [
			'id_student',
		]

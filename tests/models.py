from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

## Standard tests ##
			
class DynMCQInfo(models.Model):
	id_test = models.CharField(max_length=10, primary_key=True)
	title = models.TextField()
	print_test = models.BooleanField(default=False)
	questions = models.TextField(default="")
	time = models.CharField(max_length=10,default="")
	activated_for = models.TextField(default="")
	release_time = models.CharField(max_length=15, default="")

	def get_absolute_url(self):
		return reverse('tests:Create DynMCQTest', kwargs={'input_id_test': self.id_test})
	
	def get_absolute_url_q_menu(self):
		return reverse('tests:SelectMenu DynMCQquestion', kwargs={'input_id_test': self.id_test})
		
	def get_absolute_url_display(self):
		return reverse('tests:Display DynMCQtest', kwargs={'input_id_test': self.id_test})
		
	def question_reallocation(self):
		return reverse('tests:Question_reallocation', kwargs={'input_id_test': self.id_test})
		
	def get_statistics(self):
		return reverse('tests:Statistics', kwargs={'input_id_test': self.id_test})
		
	def launch_home(self):
		return reverse('tests:Launch')

	def get_launch(self):
		return reverse('tests:Launch Specific McqDyn', kwargs={'input_id_test': self.id_test})

	def get_in_launch(self):
		print_test = True
		return reverse('tests:In Launch Specific DynMcq', kwargs={'input_id_test': self.id_test})
		
	def stop_launch(self):
		return reverse('tests:Stop mcq launch', kwargs={'input_id_test': self.id_test})
		
class Dynquestion(models.Model):
	q_num = models.AutoField(primary_key=True)
	q_text = models.TextField()
	r_text = models.TextField()
	activated = models.IntegerField(null = True)
	difficulty = models.TextField(default="")

	def get_absolute_url_question(self):
		return reverse('tests:Create Dynquestion', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_difficulty(self):
		return reverse('tests:Add Difficulty question', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_edit(self):
		return reverse('tests:Edit Dynquestion', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_delete(self):
		return reverse('tests:Delete Dynquestion', kwargs={'input_q_num': self.q_num})	
		
class DynMCQquestion(models.Model):
	q_num = models.AutoField(primary_key=True)
	q_text = models.TextField()
	nb_ans = models.CharField(max_length=10)
	right_ans = models.IntegerField(null = True)
	activated = models.IntegerField(null = True)
	difficulty = models.TextField(default="")
		
	def get_absolute_url_question(self):
		return reverse('tests:Create DynMCQquestion', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_answers(self):
		return reverse('tests:Create DynMCQanswers', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_difficulty(self):
		return reverse('tests:Add Difficulty', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_edit(self):
		return reverse('tests:Edit DynMCQquestion', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_delete(self):
		return reverse('tests:Delete DynMCQquestion', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_add_answer(self):
		return reverse('tests:AddAnswer DynMCQanswer', kwargs={'input_q_num': self.q_num})
		
		
class DynMCQanswer(models.Model):
	q_num = models.IntegerField(null = True)
	ans_num = models.IntegerField(null = True)
	ans_text = models.TextField()
	right_ans = models.IntegerField()
		
	class Meta:
		unique_together = ('q_num', 'ans_num')
		
	def get_absolute_url_edit(self):
		return reverse('tests:Edit DynMCQanswer', kwargs={'input_q_num': self.q_num,'input_ans_num': self.ans_num})
		
	def get_absolute_url_delete(self):
		return reverse('tests:Delete DynMCQanswer', kwargs={'input_q_num': self.q_num,'input_ans_num': self.ans_num})
		
class Pass_DynMCQTest_Info(models.Model):
	id_test = models.CharField(max_length=10, null=True)
	id_student = models.CharField(max_length=10, null=True)
	attempt = models.IntegerField(null = True)
	mark = models.IntegerField(null = True)
	time = models.CharField(max_length=15, null=True)
	
	class Meta:
		unique_together = ('id_test', 'id_student','attempt')
		
	def get_absolute_url(self):
		return reverse('tests:Pass dynmcqtest', kwargs={'input_id_test': self.id_test,'input_id_student': self.id_student,'input_attempt':self.attempt})
		
	def get_absolute_url_display(self):
		return reverse('tests:Display pass dynmcqtest', kwargs={'input_id_test': self.id_test,'input_id_student': self.id_student,'input_attempt':self.attempt})
		
class Pass_DynMCQTest(models.Model):
	id_test = models.CharField(max_length=10, null=True)
	id_student = models.CharField(max_length=10, null=True)
	attempt = models.IntegerField(null = True)
	q_num = models.CharField(max_length=10, null=True)
	r_ans = models.TextField()

	class Meta:
		unique_together = ('id_test', 'id_student','attempt','q_num')
		
class Pass_DynquestionTest(models.Model):
	id_test = models.CharField(max_length=10, null=True)
	id_student = models.CharField(max_length=10, null=True)
	attempt = models.IntegerField(null = True)
	q_num = models.CharField(max_length=10, null=True)
	r_answer = models.TextField()

	class Meta:
		unique_together = ('id_test', 'id_student','attempt','q_num')



from email.policy import default
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Users and types of users are defined here
class User(AbstractUser):
    phonenumber = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self): return f'{self.username}'

class Student(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True, related_name="student")
    score = models.PositiveIntegerField(default=0)

    def __str__(self): return f'{self.user.first_name} {self.user.last_name}-Student'

class Teacher(models.Model):
    """
    supervisor field should be filled if "Teacher" is Teacher assistant. 
    """
    user = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True, related_name="teacher")
    supervisor = models.ManyToManyField("Teacher", blank=True, related_name="supervisor_of_TA")
    photo = models.ImageField(upload_to='assessment_app/static/assessment_app/img', blank=True, null=True)

    def __str__(self): 
        if self.supervisor.exists(): return f'{self.user.first_name} {self.user.last_name}-کمک‌مدرس'
        else: return f'{self.user.first_name} {self.user.last_name}-مدرس'

    class Meta:
        verbose_name = 'Teacher/TA'
        verbose_name_plural = 'Teachers/TAs'

class Department(models.Model):
    name = models.CharField(max_length=50)
    member = models.ManyToManyField("User", related_name="members")

    def __str__(self): return f'Department of {self.name}'

class PrizesGot(models.Model):
    user = models.ForeignKey("Student", on_delete=models.CASCADE, blank=True, null=True, related_name="winner")
    prize = models.ForeignKey("PrizeName", on_delete=models.CASCADE, blank=True, null=True, related_name="prize_name")
    code = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self): return f'{self.user}-{self.prize.name}'

    class Meta:
        verbose_name = 'Prize log'
        verbose_name_plural = 'List of gotten prizes'

class PrizeName(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=3000)
    score_needed = models.PositiveIntegerField()
    student = models.ManyToManyField("Student", blank=True, related_name="able_to_enroll")
    active = models.BooleanField(default=True)

    def __str__(self): return f'{self.name}'

    class Meta:
        verbose_name = 'Prize'
        verbose_name_plural = 'Prizes'



# Only specific forms are created which store questions
class FormSample(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    question = models.ManyToManyField("Questions", blank=True, related_name="questions")
    description = models.CharField(max_length=3000, blank=True, null=True)

    def __str__(self): return f"{self.id}-{self.name}"


class Course(models.Model):
    """
    Each Course may have many forms concerning each Teacher/Teacher Assistant.
    A course may also need to be eaxmined by itself. (teacher and teacher_assistant fields can be null)
    So if a course has 2 teachers and 1 TA then we will have 3 "courses" or to better say: 3 forms that each
    student could use fill one of those forms.

    This could also not be a course at all! 🐸 For example a questionnaire for other things. By not specifying 
    teacher_chief, this "course" will be questionnaire for anything other than a course.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.ForeignKey("CourseName", on_delete=models.CASCADE, related_name="name_of_course")
    term = models.ForeignKey("Term", on_delete=models.CASCADE, blank=True, null=True, related_name="term_of_course")
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, blank=True, null=True, related_name="teacher_of_course")
    teacher_chief = models.ForeignKey("Teacher", on_delete=models.CASCADE, blank=True, null=True, related_name="head_of_course")
    is_teacher_assisstant = models.BooleanField(default=False)
    current_supervisor = models.ForeignKey("Teacher", on_delete=models.CASCADE, blank=True, null=True, related_name="supervisor_of_ta")
    student = models.ManyToManyField("Student", blank=True, related_name="enrolled_students")
    student_not_answered = models.ManyToManyField("Student", blank=True, related_name="enrolled_students_not_answered")
    form_sample = models.ForeignKey("FormSample", on_delete=models.CASCADE, blank=True, null=True, related_name="which_formsample")
    score = models.PositiveIntegerField(default=0)

    def __str__(self): return f'{self.teacher}-{self.name}-{self.term}'

    class Meta:
        verbose_name = 'Form'
        verbose_name_plural = 'All Forms By Subject'


class Term(models.Model):
    year = models.CharField(max_length=9) # 1399-1400
    half = models.CharField(max_length=2) # 01 or 02 or 03
    active = models.BooleanField(default=True)

    def __str__(self): return f'{self.year}-{self.half}'

class CourseName(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, default="")
    number = models.PositiveSmallIntegerField(default=0)

    def __str__(self): 
        if self.number != 0: return f'{self.name} {self.number} {self.type}'
        else: return f'{self.name} {self.type}'

class FormAnswerS(models.Model):
    user = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="ans_student")
    form = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="which_course")
    question = models.ForeignKey("Questions", on_delete=models.CASCADE, related_name="which_question")
    answer_open = models.CharField(max_length=3000, blank=True, null=True)
    answer_closed = models.CharField(max_length=50, blank=True, null=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self): return f'{str(self.time)[:-13]}-{self.user}-{self.form.name}-{self.question.id}'

    class Meta:
        verbose_name = 'Form answer (student)'
        verbose_name_plural = 'Form answers (students)'







class Questions(models.Model):
    q_text = models.CharField(max_length=200)
    q_type = models.ForeignKey("QuestionType", on_delete=models.CASCADE, blank=True, null=True, related_name="question_type")
    answer_closed_vals = models.ForeignKey("ClosedAnswer", on_delete=models.CASCADE, blank=True, null=True, related_name="closed_ans_vals")
    
    def __str__(self): return f'{self.id}-{self.q_text}'

    class Meta:
        ordering = ['q_type']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

class QuestionType(models.Model):
    q_type = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self): return f'{self.q_type}'

class ClosedAnswer(models.Model):
    number_radio = models.PositiveSmallIntegerField()
    values = models.ManyToManyField("ClosedAnswerValue", related_name="answer_values")

    def __str__(self): 
        out = ''
        for val in self.values.all(): out += (val.value + "-")
        return f'({self.number_radio}) {out}'

class ClosedAnswerValue(models.Model):
    value = models.CharField(max_length=50)

    def __str__(self): return f'{self.value}'

class Images(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='images')

    class Meta:
        verbose_name = 'Image file'
        verbose_name_plural = 'Image files'

    def __str__(self): return f'{self.name}'

class IDNumbers(models.Model):
    idnum = models.CharField(max_length=150)
    taken = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ID Number'
        verbose_name_plural = 'ID Numbers'

    def __str__(self): return f'{self.idnum}-{self.taken}'
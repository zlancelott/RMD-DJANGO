from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, AbstractUser
)
from django.utils.translation import ugettext_lazy as _

# Curso
class Course(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=30)

	def __str__(self):
		return self.name

	def __repr__(self):
		return f"Course('{self.name}', '{self.code}')"


# Disciplina
class Subject(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=30)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)  # um curso tem várias disciplinas

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name



# Usuário
class User(AbstractUser):
	email = models.EmailField(max_length=255, unique=True, blank=False)
	gender = models.CharField(max_length=1, blank=False)

	USERNAME_FIELD = 'email'

	REQUIRED_FIELDS = ['username', 'gender', 'subject_class']

	def __str__(self):
		return self.first_name

	class Meta:
		db_table = 'home_user'

# Turma (APSO 2017.2, APSO 2018.1....)
class SubjectClass(models.Model):
	semester = models.CharField(max_length=10)
	code = models.CharField(max_length=30)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # uma disciplina tem várias turmas
	users = models.ManyToManyField(User, related_name='subjectclasses')

	def __str__(self):
		return self.subject.name

	def __repr___(self):
		return f"SubjectClass('{self.code}', '{self.semester}')"


class UserClassAssociation(models.Model):
	user_id = models.ForeignKey(User, on_delete = models.CASCADE)
	subject_class_id = models.ForeignKey(SubjectClass, on_delete = models.CASCADE)
	is_mod = models.BooleanField(default=False)



# Aula
class Lesson (models.Model):
	date = models.DateField()
	subject_class = models.ForeignKey(SubjectClass, on_delete=models.CASCADE, related_name='lessons')  # VERIFICAR ON_DELETE

	def __str__(self):
		return 'Aula'


# Arquivo da Aula
class LessonFile(models.Model):	
	name = models.CharField(max_length=100)
	subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
	lesson = models.ForeignKey(Lesson, related_name="lesson", on_delete = models.CASCADE)
	author = models.ForeignKey(User, related_name= "lessonFile_author", on_delete = models.DO_NOTHING)
	file_image = models.ImageField(upload_to="photos/", null=False)


	def __str__(self):
		return self.name

	def __repr__(self):
		return f"LessonFile('{self.name}', '{self.author}')"

# Assunto
class Topic(models.Model):
	name = models.CharField(max_length=100)
	subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
	lesson_files = models.ManyToManyField(LessonFile)

	def __repr__(self):
		return f"Topic('{self.name}')"



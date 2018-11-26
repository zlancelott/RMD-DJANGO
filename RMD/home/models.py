from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
)
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


# Turma (APSO 2017.2, APSO 2018.1....)
class SubjectClass(models.Model):
	semester = models.CharField(max_length=10)
	code = models.CharField(max_length=30)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # uma disciplina tem várias turmas

	def __repr___(self):
		return f"SubjectClass('{self.code}', '{self.semester}')"


class UserManager(BaseUserManager):
	def create_user(self, email, password=None, active=True, is_staff=False, is_admin=False):
		if not email:
			raise ValueError("Usuários devem ter um endereço de e-mail.")
		if not password:
			raise ValueError("Usuários devem ter uma senha.")

		user_obj = self.model(
			email = self.normalize_email(email)
		)
		user_obj.set_password(password) #change user password
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)

		return user_obj

	def create_superuser(self, email, password=None):
		user = self.create_user(
			email,
			password=password,
			is_staff=True,
			is_admin=True
		)
		
		return user


# Usuário
class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=100)
	gender = models.CharField(max_length=1)
	active = models.BooleanField(default=True) # default=False when you are going to implement Activation Mail
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)
	subject_class = models.ForeignKey(SubjectClass, on_delete = models.CASCADE)


	USERNAME_FIELD = 'email'

	REQUIRED_FIELDS = ['name', 'gender']

	objects = UserManager()

	def __str__(self):
		return self.email

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active

class UserClassAssociation(models.Model):
	user_id = models.ForeignKey(User, on_delete = models.CASCADE)
	subject_class_id = models.ForeignKey(SubjectClass, on_delete = models.CASCADE)
	is_mod = models.BooleanField(default=False)



# Aula
class Lesson (models.Model):
	date = models.DateField()
	subject_class = models.ForeignKey(SubjectClass, on_delete=models.CASCADE)  # VERIFICAR ON_DELETE

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



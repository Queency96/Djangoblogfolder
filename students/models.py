from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import random, string


def mail_validator(value):
    if '@' and '.com' in value:
        return value
    else:
        raise ValidationError('Invalid email address')


student_position = {
  ('Leader', 'Cohort Leader'),
  ('President', 'President'),
  ('Vice', 'Vice President'),
  ('Secretary', 'Secretary'),
  ('Student', 'Student'),
}

# Create your models here.
class Student(models.Model):
  username = models.CharField(max_length=100)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  student_type = models.CharField(max_length=9, choices=student_position, default='Student')
  status = models.BooleanField(default=True)
  email = models.EmailField(max_length=254, unique=True, validators=[mail_validator])
  phone = models.CharField(max_length=11, null=True, blank=True)
  slug = models.SlugField(unique=True, blank=True, editable=False)
  
  def __str__(self):
    return f"{self.first_name} {self.last_name}"
  
  def save(self, *args, **kwargs):
    if not self.slug:
      student_slug_rand_num_gen = ''.join(random.choices(string.digits, k=9))
      self.slug = slugify(f"{self.first_name}-{self.last_name}-{student_slug_rand_num_gen}")
    super().save(*args, **kwargs)



class Student_Profile(models.Model):
  student = models.OneToOneField(Student, on_delete=models.CASCADE)
  bio = models.TextField()
  DOB = models.DateField()
  address = models.CharField(max_length=500)
  rating = models.FloatField(default=0.0)
  profile_picture = models.ImageField(upload_to='student_profile')
  date_join = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.student.first_name} {self.student.last_name}"


class Program(models.Model):
  courses = models.CharField(max_length=500)
  grade = models.IntegerField(default=0)
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"{self.courses}"
  
  
class Cohort_Group(models.Model):
  name = models.CharField(max_length=100)
  date_join = models.DateTimeField(auto_now_add=True)
  students = models.ManyToManyField(Student)

  
  def __str__(self):
    return f"{self.name}"
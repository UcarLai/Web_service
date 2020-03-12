from django.db import models
from django.contrib.auth.models import User

# from django.conf import settings
# User = settings.AUTH_USER_MODEL

class Professor(models.Model):
    professor_id = models.CharField(max_length=50)
    professor_name = models.CharField(max_length=50)

    def __str__(self):
        return "{}-{}".format(self.professor_id, self.professor_name)

class Module(models.Model):
    module_code = models.CharField(max_length=50)
    module_name = models.CharField(max_length=50)
    module_year = models.IntegerField(default=2000)
    module_semester = models.IntegerField(default=1)
    module_taughtby = models.ManyToManyField(Professor)
    def __str__(self):
        return "{}-{}-{}-{}".format(self.module_code, self.module_name, self.module_year, self. module_semester)

class Rate(models.Model):
    rate_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    rate_module = models.ForeignKey(Module, on_delete=models.CASCADE)
    rate_professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rate_score = models.IntegerField(default=0)
    def __str__(self):
        return "{}-{}".format(self.rate_professor.professor_id, self.rate_module.module_code)



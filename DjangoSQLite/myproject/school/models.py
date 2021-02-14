from django.db import models


class Homework(models.Model):
    db_table = "Homeworks"

    text = models.TextField(unique=True)
    deadline = models.DurationField()
    created = models.DateTimeField()

    def __str__(self) -> str:
        return self.text


class HomeworkResult(models.Model):
    db_table = "HomeworkResults"

    homework = models.ForeignKey(Homework, to_field="text", on_delete=models.CASCADE)
    author = models.ForeignKey("Student", on_delete=models.CASCADE)
    solution = models.TextField()
    created = models.DateTimeField()

    def __str__(self) -> str:
        return self.solution


class PersonalData(models.Model):
    class Meta:
        abstract = True

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Student(PersonalData):
    db_table = "Students"
    age = models.IntegerField()


class Teacher(PersonalData):
    db_table = "Teachers"
    homework_done = models.ForeignKey(HomeworkResult, on_delete=models.CASCADE)

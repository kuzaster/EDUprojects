from django.test import TestCase
from school.models import Homework, HomeworkResult, Student, Teacher


class PersonsTestCase(TestCase):
    fixtures = ["first_db_records.json"]

    def test_first_student(self):
        student_1 = Student.objects.get(id=1)
        self.assertEqual(student_1.first_name, "Tim")
        self.assertEqual(student_1.last_name, "Nekuk")
        self.assertEqual(student_1.age, 26)

    def test_first_teacher(self):
        teacher_1 = Teacher.objects.get(id=1)
        self.assertEqual(teacher_1.first_name, "Bob")
        self.assertEqual(teacher_1.last_name, "Kelso")
        self.assertEqual(teacher_1.homework_done.id, 1)


class HomeworkTestCase(TestCase):
    fixtures = ["first_db_records.json"]

    def test_first_homework(self):
        homework_1 = Homework.objects.get(id=1)
        self.assertEqual(homework_1.text, "Final HW!")
        self.assertEqual(homework_1.deadline.days, 3)
        self.assertEqual(homework_1.created.date().isoformat(), "2020-12-28")

    def test_first_homework_result(self):
        hw_1_result = HomeworkResult.objects.get(id=1)
        self.assertEqual(hw_1_result.homework.text, "Final HW!")
        self.assertEqual(hw_1_result.author.id, 1)
        self.assertEqual(hw_1_result.solution, "Hope fine")
        self.assertEqual(hw_1_result.created.date().isoformat(), "2020-12-28")

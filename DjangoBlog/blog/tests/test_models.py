from django.contrib.auth import authenticate
from django.test import TestCase
from django.utils import timezone

from ..models import Comment, MyUser, Post

# Create your tests here.


class MyUserModelTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@test.ru", password="1234qwerty"
        )
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_read_user(self):
        self.assertEqual(self.user.id, 1)

    def test_add_first_name(self):
        self.user.first_name = "first-name"
        self.assertEqual(self.user.first_name, "first-name")

    def test_correct_data_authentication(self):
        user = authenticate(email="test@test.ru", password="1234qwerty")
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_email_authentication(self):
        user = authenticate(email="wrong@test.ru", password="1234qwerty")
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_password_authentication(self):
        user = authenticate(email="test@test.ru", password="1234wrong")
        self.assertFalse((user is not None) and user.is_authenticated)


class PostModelTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@test.ru", password="1234qwerty"
        )
        self.user.save()
        self.post = Post(
            author=self.user,
            title="title",
            shot_body="shot_body",
            body="body",
            published=timezone.now(),
        )
        self.post.save()

    def tearDown(self):
        self.user.delete()

    def test_read_post(self):
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.title, "title")
        self.assertEqual(self.post.body, "body")

    def test_change_post(self):
        self.post.title = "New title"
        self.post.shot_body = "New shot"
        self.assertEqual(self.post.title, "New title")
        self.assertEqual(self.post.shot_body, "New shot")


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@test.ru", password="1234qwerty"
        )
        self.user.save()
        self.post = Post(
            author=self.user,
            title="title",
            shot_body="shot_body",
            body="body",
            published=timezone.now(),
        )
        self.post.save()
        self.comment = Comment(name="Name", body="Comment body", post=self.post)

    def tearDown(self):
        self.user.delete()

    def test_read_post(self):
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.name, "Name")
        self.assertEqual(self.comment.body, "Comment body")

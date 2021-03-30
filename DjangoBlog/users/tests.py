from django.shortcuts import reverse
from django.test import TestCase

from blog.models import MyUser, Post

# Create your tests here.


class MyLoginViewTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@test.ru", password="1234qwerty"
        )
        self.user.first_name = "name"
        self.user.last_name = "surname"
        self.user.mobile = 333
        self.user.skype = "skype"
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct_data_authentication(self):
        login = self.client.post(
            "/users/login/", {"username": "test@test.ru", "password": "1234qwerty"}
        )
        self.assertRedirects(login, "/users/1/profile/")
        self.assertEqual(login.status_code, 302)
        response = self.client.get(reverse("profile-page", kwargs={"pk": self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "name surname")

    def test_wrong_email_authentication(self):
        login = self.client.login(email="wrong@test.ru", password="1234qwerty")
        response = self.client.get(reverse("profile-page", kwargs={"pk": self.user.id}))
        self.assertFalse(login)
        self.assertNotEqual(str(response.context["user"]), "name surname")

    def test_wrong_password_authentication(self):
        login = self.client.login(email="test@test.ru", password="1234wrong")
        response = self.client.get(reverse("profile-page", kwargs={"pk": self.user.id}))
        self.assertFalse(login)
        self.assertNotEqual(str(response.context["user"]), "name surname")


class UserRegisterViewTest(TestCase):
    def test_register_new_user(self):
        self.assertIsNone(MyUser.objects.first())
        reg = self.client.post(
            "/users/register/",
            {
                "email": "test@test.ru",
                "first_name": "Name",
                "last_name": "Lastname",
                "skype": "skype-name",
                "mobile": 333,
                "password1": "superpassword",
                "password2": "superpassword",
            },
        )
        self.assertEqual(reg.status_code, 302)
        self.assertIsNotNone(MyUser.objects.first())
        self.assertRedirects(reg, "/users/login/")
        self.assertEqual(str(MyUser.objects.first()), "Name Lastname")

    def test_register_with_wrong_password2(self):
        self.assertIsNone(MyUser.objects.first())
        reg = self.client.post(
            "/users/register/",
            {
                "email": "test@test.ru",
                "first_name": "Name",
                "last_name": "Lastname",
                "skype": "skype-name",
                "mobile": 333,
                "password1": "superpassword",
                "password2": "anotherpassword",
            },
        )
        self.assertNotEqual(reg.status_code, 302)
        self.assertIsNone(MyUser.objects.first())

    def test_register_with_invalid_email(self):
        self.assertIsNone(MyUser.objects.first())
        reg = self.client.post(
            "/users/register/",
            {
                "email": "not_email",
                "first_name": "Name",
                "last_name": "Lastname",
                "skype": "skype-name",
                "mobile": 333,
                "password1": "superpassword",
                "password2": "anotherpassword",
            },
        )
        self.assertNotEqual(reg.status_code, 302)
        self.assertIsNone(MyUser.objects.first())

    def test_login_after_registration(self):
        response = self.client.get(reverse("home"))
        self.assertNotIn("Logout", str(response.content))
        self.assertIsNone(MyUser.objects.first())
        reg = self.client.post(
            "/users/register/",
            {
                "email": "test@test.ru",
                "first_name": "Name",
                "last_name": "Lastname",
                "skype": "skype-name",
                "mobile": 333,
                "password1": "superpassword",
                "password2": "superpassword",
            },
        )

        login = self.client.login(email="test@test.ru", password="superpassword")
        response = self.client.get(reverse("home"))
        self.assertTrue(login)
        self.assertIn("Logout", str(response.content))
        self.assertIsNotNone(MyUser.objects.first())


class ProfilePageViewTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@test.ru", password="superpassword"
        )
        self.user.first_name = "Name"
        self.user.last_name = "Lastname"
        self.user.mobile = 333
        self.user.skype = "skype_name"
        self.user.save()
        self.response = self.client.get(
            reverse("profile-page", kwargs={"pk": self.user.id})
        )

    def tearDown(self):
        self.user.delete()

    def test_context_in_profile_page(self):
        self.assertEqual(self.response.status_code, 200)
        context = self.response.context["user_page"]
        self.assertEqual(context.first_name, "Name")
        self.assertEqual(context.last_name, "Lastname")
        self.assertEqual(context.skype, "skype_name")
        self.assertEqual(context.mobile, 333)

    def test_show_posts_in_profile_page(self):
        self.assertIn("You haven\\'t got posts yet", str(self.response.content))

        self.post = Post(
            author=self.user, title="Title", shot_body="Shot body", body="Long body"
        )
        self.post.save()

        response = self.client.get(reverse("profile-page", kwargs={"pk": self.user.id}))
        context = response.context["user_page"]
        self.assertNotIn("You haven\\'t got posts yet", str(response.content))
        self.assertIn("Title", str(response.content))
        self.assertIn("Shot body", str(response.content))
        self.assertEqual(context.blog_posts.first().title, "Title")

    def test_edit_profile_link_after_logged_in(self):
        self.assertNotIn("Edit your profile", str(self.response.content))

        self.client.login(email="test@test.ru", password="superpassword")
        response = self.client.get(reverse("profile-page", kwargs={"pk": self.user.id}))
        self.assertIn("Edit your profile", str(response.content))


class UserEditViewTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@test.ru", password="superpassword"
        )
        self.user.first_name = "Name"
        self.user.last_name = "Lastname"
        self.user.mobile = 333
        self.user.skype = "skype_name"
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_edit_profile_without_authorization(self):
        edit = self.client.post(
            "/users/1/edit_profile/",
            {
                "first_name": "NewName",
                "last_name": "Lastname",
                "skype": "New-skype-name",
                "mobile": 333,
            },
        )
        self.assertTrue(edit.url.startswith("/users/login/"))
        self.assertNotEqual(MyUser.objects.first().first_name, "NewName")

    def test_edit_profile_with_authorization(self):
        login = self.client.login(email="test@test.ru", password="superpassword")
        self.assertEqual(MyUser.objects.first().first_name, "Name")
        edit = self.client.post(
            "/users/1/edit_profile/",
            {
                "first_name": "NewName",
                "last_name": "Lastname",
                "skype": "New-skype-name",
                "mobile": 333,
            },
        )
        self.assertRedirects(edit, "/users/1/profile/")
        self.assertEqual(MyUser.objects.first().first_name, "NewName")
        self.assertEqual(MyUser.objects.first().skype, "New-skype-name")

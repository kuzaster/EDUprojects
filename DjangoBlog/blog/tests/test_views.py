from django.shortcuts import reverse
from django.test import TestCase

from ..models import MyUser, Post

# Create your tests here.


class HomeViewTest(TestCase):
    fixtures = ["mydata.json"]

    def test_applying_fixture(self):
        amount_users = MyUser.objects.count()
        self.assertEqual(amount_users, 3)

    def test_show_all_posts(self):
        response = self.client.get(reverse("home"))
        amount_posts = Post.objects.count()
        self.assertEqual(len(response.context["post_list"]), amount_posts)


class PostDetailViewTest(TestCase):
    fixtures = ["mydata.json"]

    def test_post_data_on_detail_page(self):
        post = Post.objects.get(id=1)
        response = self.client.get(reverse("detail-post", kwargs={"pk": 1}))
        self.assertIn(post.title, str(response.content))
        self.assertIn(post.body, str(response.content))

    def test_comments_data_on_detail_page(self):
        post = Post.objects.get(id=1)
        comment_1 = post.comments.all()[0].body
        comment_2 = post.comments.all()[1].body
        response = self.client.get(reverse("detail-post", kwargs={"pk": 1}))
        self.assertIn(comment_1, str(response.content))
        self.assertIn(comment_2, str(response.content))

    def test_edit_delete_buttons_for_logged_author(self):
        response = self.client.get(reverse("detail-post", kwargs={"pk": 1}))
        self.assertNotIn("Edit", str(response.content))
        self.assertNotIn("Delete", str(response.content))

        user = MyUser.objects.get(pk=1)
        user.set_password("superpassword")
        user.save()

        login = self.client.login(email="name_1@name.ru", password="superpassword")
        response = self.client.get(reverse("detail-post", kwargs={"pk": 1}))
        self.assertIn("Edit", str(response.content))
        self.assertIn("Delete", str(response.content))

    def test_no_able_to_comment_your_own_post(self):
        response = self.client.get(reverse("detail-post", kwargs={"pk": 1}))
        self.assertIn("Add comment", str(response.content))

        user = MyUser.objects.get(pk=1)
        user.set_password("superpassword")
        user.save()

        login = self.client.login(email="name_1@name.ru", password="superpassword")
        response = self.client.get(reverse("detail-post", kwargs={"pk": 1}))
        self.assertNotIn("Add comment", str(response.content))


class AddPostViewTest(TestCase):
    fixtures = ["mydata.json"]

    def test_add_new_post(self):
        user = MyUser.objects.get(pk=1)
        user.set_password("superpassword")
        user.save()
        login = self.client.login(email="name_1@name.ru", password="superpassword")
        amount_posts = user.blog_posts.count()
        self.assertEqual(amount_posts, 2)

        add_post = self.client.post(
            "/add_post",
            {
                "title": "New post!",
                "shot_body": "Shot body!",
                "body": "Body of the post!",
                "author": 1,
            },
        )
        new_amount_posts = user.blog_posts.count()
        self.assertEqual(add_post.status_code, 302)
        self.assertEqual(new_amount_posts, 3)


class EditPostViewTest(TestCase):
    fixtures = ["mydata.json"]

    def test_edit_post_without_authorization(self):
        post = Post.objects.get(pk=1)
        self.assertEqual(post.title, "User_1 post!")
        edit_post = self.client.post(
            "/post/edit/1",
            {
                "title": "Changed title!",
                "shot_body": "Shot body!",
                "body": "Changed body!",
                "author": 1,
            },
        )
        self.assertTrue(edit_post.url.startswith("/users/login/"))
        self.assertNotEqual(post.title, "Changed title!")

    def test_edit_post_with_authorization(self):
        user = MyUser.objects.get(pk=1)
        user.set_password("superpassword")
        user.save()
        post = user.blog_posts.get(pk=1)
        login = self.client.login(email="name_1@name.ru", password="superpassword")
        self.assertEqual(post.title, "User_1 post!")

        edit_post = self.client.post(
            "/post/edit/1",
            {
                "title": "Changed title!",
                "shot_body": "Shot body!",
                "body": "Changed body!",
                "author": 1,
            },
        )
        post = user.blog_posts.get(pk=1)
        self.assertEqual(post.title, "Changed title!")
        self.assertEqual(post.body, "Changed body!")


class DeletePostViewTest(TestCase):
    fixtures = ["mydata.json"]

    def test_delete_post_without_authorization(self):
        user = MyUser.objects.get(pk=1)
        posts_count = user.blog_posts.count()
        self.assertEqual(posts_count, 2)
        delete_post = self.client.post("/post/1/delete")

        posts_count = user.blog_posts.count()
        self.assertTrue(delete_post.url.startswith("/users/login/"))
        self.assertEqual(posts_count, 2)

    def test_delete_post_with_authorization(self):
        user = MyUser.objects.get(pk=1)
        user.set_password("superpassword")
        user.save()
        login = self.client.login(email="name_1@name.ru", password="superpassword")
        posts_count = user.blog_posts.count()
        self.assertEqual(posts_count, 2)

        delete_post = self.client.post("/post/1/delete")
        posts_count = user.blog_posts.count()
        self.assertEqual(posts_count, 1)


class AddCommentViewTest(TestCase):
    fixtures = ["mydata.json"]

    def test_add_new_comment(self):
        post = Post.objects.get(pk=1)
        comments_count = post.comments.count()
        self.assertEqual(comments_count, 2)

        add_comment = self.client.post(
            "/post/1/comment", {"name": "My name", "body": "Comment body!"}
        )
        comments_count = post.comments.count()
        self.assertEqual(comments_count, 3)

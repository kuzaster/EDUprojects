from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, unique=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/profile")
    mobile = models.IntegerField(null=True)
    skype = models.CharField(max_length=250)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = MyUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Post(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(
        MyUser, related_name="blog_posts", on_delete=models.CASCADE
    )
    shot_body = models.TextField()
    body = models.TextField()
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-published",)

    def __str__(self):
        return f"{self.title} | by {self.author}"

    def get_absolute_url(self):
        return reverse("detail-post", args=(str(self.id)))


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} left comment in '{self.post.title}' post"

    class Meta:
        ordering = ("-date_added",)

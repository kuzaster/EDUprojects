from django.contrib import admin

from .models import Comment, MyUser, Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "shot_body", "body", "published")
    list_filter = ("published", "author")
    search_fields = ("title", "body")
    raw_id_fields = ("author",)
    date_hierarchy = "published"
    ordering = ["author", "published"]


admin.site.register(Post, PostAdmin)
admin.site.register(MyUser)
admin.site.register(Comment)

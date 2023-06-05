from django.contrib import admin
# Register your models here.
from .models import Post, Comment, UserProfile
from rangefilter.filter import DateRangeFilter


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_first_name', 'get_user_last_name')

    def get_user_first_name(self, obj):
        return obj.user.first_name

    get_user_first_name.short_description = 'First Name'

    def get_user_last_name(self, obj):
        return obj.user.last_name

    get_user_last_name.short_description = 'Last Name'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'content')
    list_filter = (('created_at', DateRangeFilter),)
    readonly_fields = ('created_at', 'last_updated')

    def has_change_permission(self, request, obj=None):
        if obj and (request.user == obj.author):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and (request.user == obj.author or request.user.is_superuser):
            return True
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        blocked_users = request.user.userprofile.blocked_users.all()
        return qs.exclude(author__in=blocked_users)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

    def has_delete_permission(self, request, obj=None):
        if obj and (request.user == obj.author or request.user == obj.post.author or request.user.is_superuser):
            return True
        return False


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

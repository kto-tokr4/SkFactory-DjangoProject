from django.contrib import admin
from django.core.mail import send_mail
from .models import Profile, News


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    actions = ('send_new_to_users',)

    @admin.action()
    def send_new_to_users(self, request, queryset):
        user_profiles = Profile.objects.all()
        for new in queryset:
            subject = new.title
            message = new.content
            for profile in user_profiles:
                user_email = profile.user.email
                send_mail(subject=subject,
                          message=message,
                          from_email='',
                          recipient_list=[user_email, ])


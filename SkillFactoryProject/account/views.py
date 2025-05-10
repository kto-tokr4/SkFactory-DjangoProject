from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from .models import Profile
from .forms import UserRegistrationForm, UserEmailAcceptForm


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            Profile.objects.create(user=new_user, email_code=random.randint(a=1000, b=9999))
            user_id = new_user.id
            return redirect(reverse('account:register-accept', args=[user_id]))

    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'form': user_form})


def register_accept(request, user_id):
    user = User.objects.get(id=user_id)
    email_code = user.profile.email_code
    if request.method == 'POST':
        user_email_accept_form = UserEmailAcceptForm(request.POST)
        if user_email_accept_form.is_valid():
            if email_code == user_email_accept_form.cleaned_data['email_code']:
                user.is_active = True
                user.save()
                return render(request, 'account/register_done.html', {'new_user': user})
    else:
        user_email = user.email
        subject = 'Регистрация на сайте ИПЗ SkillFactory'
        message = f'Код для завершения регистрации пользователя с ником {user.username}: {email_code}'
        send_mail(subject=subject,
                  message=message,
                  from_email='',
                  recipient_list=[user_email, ])
        user_email_accept_form = UserEmailAcceptForm()

        return render(request, 'account/register_accept.html', {'form': user_email_accept_form})
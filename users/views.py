from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib import messages
from .forms import UserRegisterForm
from .models import User
import secrets
from django.conf import settings


class UserCreateView(CreateView):
    """Регистрация нового пользователя с отправкой письма."""

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.token = secrets.token_hex(16)
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{user.token}/"

        try:
            send_mail(
                subject="Подтверждение почты",
                message=f"Перейдите по ссылке для подтверждения почты:\n{url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(
                self.request, "Вы успешно зарегистрировались! Проверьте вашу почту для подтверждения аккаунта."
            )
        except Exception as e:
            print(f"Ошибка отправки письма: {e}")
            messages.warning(
                self.request,
                "Регистрация прошла успешно, но письмо с подтверждением не удалось отправить. Попробуйте позже.",
            )

        return redirect("users:login")


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    messages.success(request, "Ваш аккаунт успешно активирован! Теперь вы можете войти.")
    return redirect(reverse("users:login"))

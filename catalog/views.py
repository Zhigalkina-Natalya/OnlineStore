from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message_text = request.POST.get("message")
        messages.success(request, "Сообщение успешно отправлено!")
    return render(request, 'catalog/contacts.html')

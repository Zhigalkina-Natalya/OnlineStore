from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from catalog.models import Product, Category


# Create your views here.
def home(request):
    """
    Контроллер главной страницы.
    Получает список всех продуктов из базы данных и передает их в шаблон.
    """
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "catalog/home.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message_text = request.POST.get("message")
        messages.success(request, "Сообщение успешно отправлено!")
    return render(request, "catalog/contacts.html")


def product_detail(request, pk):
    """
    Контроллер для отображения страницы одного товара.
    Принимает pk, получает объект из БД и рендерит шаблон.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)


def create_product(request):
    """
    Контроллер для добавления нового продукта.
    """
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        # Проверяем, выбрана ли категория
        category = Category.objects.get(pk=category_id)

        # Создаем и сохраняем продукт
        Product.objects.create(name=name, description=description, price=price, category=category, image=image)

        messages.success(request, f'Товар "{name}" успешно добавлен!')
        return redirect('catalog:home')

    context = {'categories': categories}
    return render(request, 'catalog/product_form.html', context)

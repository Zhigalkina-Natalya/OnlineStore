from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from catalog.models import Product, Category
from .forms import ProductForm


# Create your views here.
class HomeView(ListView):
    """
    Контроллер главной страницы с отображением всех товаров.
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """
    Контроллер страницы одного товара.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ContactsView(TemplateView):
    """
    Контроллер страницы контактов.
    """
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message_text = request.POST.get("message")
        messages.success(request, "Сообщение успешно отправлено!")
        return self.get(request, *args, **kwargs)


class ProductCreateView(CreateView):
    """Форма добавления нового товара."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        messages.success(self.request, f'Товар "{form.instance.name}" успешно добавлен!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # ← добавляем категории
        return context


class ProductUpdateView(UpdateView):
    """Форма редактирования товара."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        messages.success(self.request, f'Товар "{form.instance.name}" успешно обновлён!')
        return super().form_valid(form)

    def get_success_url(self):
        # После редактирования перенаправляем на страницу товара
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    """Удаление товара с сообщением."""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:home')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'Товар "{obj.name}" удалён.')
        return super().delete(request, *args, **kwargs)

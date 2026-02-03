from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from catalog.models import Product, Category
from .forms import ProductForm


class HomeView(ListView):
    """
    Контроллер главной страницы с отображением всех товаров.
    """

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    """
    Контроллер страницы одного товара.
    """

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ContactsView(TemplateView):
    """
    Контроллер страницы контактов.
    """

    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message_text = request.POST.get("message")
        messages.success(request, "Сообщение успешно отправлено!")
        return self.get(request, *args, **kwargs)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта. Автоматически привязываем владельца."""

    login_url = "users:login"
    redirect_field_name = "next"
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f'Товар "{form.instance.name}" успешно добавлен!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()  # ← добавляем категории
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Форма редактирования товара. Редактировать может только владелец."""

    login_url = "users:login"
    redirect_field_name = "next"
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            messages.warning(request, "Вы не можете редактировать этот продукт.")
            return redirect("catalog:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f'Товар "{form.instance.name}" успешно обновлён!')
        return super().form_valid(form)

    def get_success_url(self):
        # После редактирования перенаправляем на страницу товара
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара с сообщением. Удалять может владелец или модератор"""

    login_url = "users:login"
    redirect_field_name = "next"
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm("catalog.delete_product"):
            messages.warning(request, "Вы не можете удалить этот продукт.")
            return redirect("catalog:home")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'Товар "{obj.name}" удалён.')
        return super().delete(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Контроллер для снятия товара с публикации.
    Снять с публикации может только модератор с правом catalog.can_unpublish_product.
    """
    permission_required = "catalog.can_unpublish_product"
    raise_exception = True
    login_url = "users:login"

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        messages.success(request, f'Продукт "{product.name}" снят с публикации.')
        return redirect("catalog:product_detail", pk=pk)

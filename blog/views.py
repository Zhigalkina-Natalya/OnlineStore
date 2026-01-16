from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import BlogPost


class BlogListView(ListView):
    """Список всех блоговых записей."""
    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Выводим только опубликованные посты"""
        return super().get_queryset().filter(is_published=True).order_by('-created_at')


class BlogDetailView(DetailView):
    """Отдельная запись блога."""
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """При открытии статьи увеличиваем счётчик просмотров"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj


class BlogCreateView(CreateView):
    """Создание новой записи."""
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")


class BlogUpdateView(UpdateView):
    """Редактирование записи."""
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")

    def get_success_url(self):
        """После редактирования переходим на страницу поста"""
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """Удаление записи."""
    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_list")

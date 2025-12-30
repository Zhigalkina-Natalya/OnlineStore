from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from django.core.management import call_command


class Command(BaseCommand):
    """Кастомная команда для загрузки тестовых данных"""

    help = "Очищает базу данных и загружает тестовые данные из фикстур"

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        self.stdout.write(self.style.WARNING("Удаляем старые данные"))
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загружаем фикстуры
        self.stdout.write(self.style.WARNING("Загружаем новые данные из фикстур"))
        call_command("loaddata", "catalog/fixtures/categories.json")
        call_command("loaddata", "catalog/fixtures/products.json")

        # Подтверждение
        self.stdout.write(self.style.SUCCESS("База успешно обновлена тестовыми данными!"))

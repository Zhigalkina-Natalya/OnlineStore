from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Создаёт группу 'Модератор продуктов' с нужными правами"

    def handle(self, *args, **options):
        group_name = "Модератор продуктов"
        group, created = Group.objects.get_or_create(name=group_name)

        delete_permission = Permission.objects.get(codename="delete_product")
        unpublish_permission = Permission.objects.get(codename="can_unpublish_product")

        if not delete_permission or not unpublish_permission:
            self.stdout.write(self.style.ERROR("Права не найдены."))

        group.permissions.add(delete_permission, unpublish_permission)

        if created:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_name}' создана и права добавлены."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_name}' уже существует. Права обновлены."))

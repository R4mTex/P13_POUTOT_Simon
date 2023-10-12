from django.core.management.base import BaseCommand
from datetime import date, timedelta
from blog import models as blogModels


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        tools = blogModels.Blog.objects.all()

        for tool in range(len(tools)):
            if (tools[tool].availabalityEnd + timedelta(days=30)) == date.today():
                tools[tool].delete()
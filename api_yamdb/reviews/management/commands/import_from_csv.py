import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title
from user.models import User

data = ['static/data/category.csv', 'static/data/genre.csv']


def read_from_file(path):
    reader = csv.reader(open(path, 'r', encoding='utf-8'))
    next(reader)
    return reader


class Command(BaseCommand):
    def handle(self, *args, **options):

        for row in read_from_file('static/data/users.csv'):
            User.objects.get_or_create(
                username=row[1],
                email=row[2],
                role=row[3]),

        for row in read_from_file('static/data/genre.csv'):
            Genre.objects.get_or_create(
                name=row[1],
                slug=row[2]
            ),

        for row in read_from_file('static/data/category.csv'):
            Category.objects.get_or_create(
                name=row[1],
                slug=row[2]
            ),
        for row in read_from_file('static/data/titles.csv'):
            Title.objects.get_or_create(
                name=row[1],
                year=row[2],
                category=Category.objects.get(pk=row[3])),

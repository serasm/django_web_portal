import logging, random
from datetime import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission

from faker import Faker

from information_page.models import (
    Article,
    ArticleGenre,
    ArticleComment,
    ArticleNote)

fake = Faker('en_US')

PERMISSIONS = (
    'view',
    'add',
    'delete',
    'change',)

GROUPS = {
    'users': {
        'article': [PERMISSIONS[0]],
        'article genre': [PERMISSIONS[0]],
        'article comment': PERMISSIONS[0:2],
    },
    'editors': {
        'article': PERMISSIONS[0:2],
        'article genre': PERMISSIONS[0:3],
        'article comment': PERMISSIONS[0:3],
        'article note': PERMISSIONS[0:2]
    },
    'moderators': {
        'article': [PERMISSIONS[0]],
        'article genre': [PERMISSIONS[0]],
        'article comment': PERMISSIONS[0:3]
    },
    'admins': {
        'article': PERMISSIONS,
        'article genre': PERMISSIONS,
        'article comment': PERMISSIONS,
        'article note': PERMISSIONS
    }
}


class Command(BaseCommand):

    def handle(self, *args, **options):

        for group_name, group_value in GROUPS.items():
            new_group, created = Group.objects.get_or_create(name=group_name)
            for model_name, permissions in group_value.items():
                for permission_name in permissions:
                    name = 'Can {} {}'.format(permission_name, model_name)
                    print(name)
                    perm = Permission.objects.get(name__iexact=name)

                    try:
                        new_group.permissions.add(perm)
                    except:
                        logging.warning(
                            "Permission not found with name '{}'".format(name))
                        continue

        print('Created default group and permissions')

        publish_permission = Permission.objects.filter(
            name__iexact='Can publish article').first()
        adminsGroup, created = Group.objects.get_or_create(name='admins')
        adminsGroup.permissions.add(publish_permission)

        users = User.objects.filter(groups__name__iexact='users')
        editors = User.objects.filter(groups__name__iexact='editors')

        computers_genre, created = ArticleGenre.objects.get_or_create(
            name='Computers', description=fake.text())
        cpus_genre = ArticleGenre.objects.get_or_create(
            name='Processors', description=fake.text(), parent=computers_genre)
        motherboars_genre = ArticleGenre.objects.get_or_create(
            name='Motherboards', description=fake.text(),
            parent=computers_genre)
        gpus_genre = ArticleGenre.objects.get_or_create(
            name='Graphics Cards', description=fake.text(),
            parent=computers_genre)

        phones_genre, created = ArticleGenre.objects.get_or_create(
            name='Phones', description=fake.text())
        android_phones_genre = ArticleGenre.objects.get_or_create(
            name='Adroid', description=fake.text(), parent=phones_genre)
        iphone_phones_genre = ArticleGenre.objects.get_or_create(
            name='iPhone', description=fake.text(), parent=phones_genre)

        genres = ArticleGenre.objects.all()

        for index in range(80):
            editor_index = random.randint(0, editors.count() - 1)
            editor = editors[editor_index]

            genre_index = random.randint(0, genres.count() -1)
            genre_obj = genres[genre_index]

            pub = random.randint(0, 42) % 2 == 0

            article_created, created = Article.objects.get_or_create(
                author=editor, title=fake.text(max_nb_chars=50),
                text=fake.text(), genre=genre_obj)

            if pub:
                article_created.publish()
                comments_count = random.randint(0, 20)

                for comment_index in range(comments_count):
                    user_index = random.randint(0, users.count() - 1)
                    user = users[user_index]

                    comment, created = ArticleComment.objects.get_or_create(
                        author=user, text=fake.text(max_nb_chars=80),
                        article=article_created)
            else:
                notes_count = random.randint(0, 4)

                for note_index in range(notes_count):
                    note_editor_index = random.randint(0, editors.count() - 1)
                    if note_editor_index == editor_index:
                        if note_editor_index == (editors.count() - 1):
                            note_editor_index -= 1
                        else:
                            note_editor_index += 1
                    note_editor = editors[note_editor_index]

                    note, created = ArticleNote.objects.get_or_create(
                        author=note_editor,
                        text=fake.text(), article=article_created)

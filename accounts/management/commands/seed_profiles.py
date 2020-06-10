import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group, Permission

from faker import Faker

fake = Faker('en_US')

PERMISSIONS = (
    'view',
    'add',
    'delete',)

GROUPS = {
    'users': {
        'user': [PERMISSIONS[0]],
        'profile': [PERMISSIONS[0]],
    },
    'editors': {
        'user': [PERMISSIONS[0]],
        'profile': [PERMISSIONS[0]],
    },
    'moderators': {
        'user': [PERMISSIONS[0]],
        'profile': [PERMISSIONS[0]],
    },
    'admins': {
        'user': PERMISSIONS,
        'profile': PERMISSIONS,
    }
}

PASSWORD = 'green_bean1'


class Command(BaseCommand):

    def handle(self, *args, **options):

        for group_name, group_value in GROUPS.items():
            new_group, created = Group.objects.get_or_create(name=group_name)
            for model_name, permissions in group_value.items():
                for permission_name in permissions:
                    name = 'Can {} {}'.format(permission_name, model_name)
                    perm = Permission.objects.get(name__iexact=name)

                    try:
                        new_group.permissions.add(perm)
                    except Permission.ObjectDoesNotExist:
                        logging.warning(
                            "Permission not found with name '{}'".format(name))
                        continue

        print('Created default group and permissions')

        usersGroup, created = Group.objects.get_or_create(name='users')
        editorsGrop, created = Group.objects.get_or_create(name='editors')
        moderatorsGroup, created = Group.objects.get_or_create(
            name='moderators')
        adminsGroup, created = Group.objects.get_or_create(name='admins')

        print('Start creating profiles for users group')

        for i in range(20):
            profile = fake.profile(fields=['username', 'name', 'mail'])
            name = profile['name'].split(' ')
            if name.count == 3:
                fn = name[1]
                ln = name[2]
            else:
                fn = name[0]
                ln = name[1]

            user = User.objects.create_user(
                username=profile['username'],
                first_name=fn,
                last_name=ln,
                email=profile['mail'],
                password=PASSWORD)

            user.groups.add(usersGroup)

        print('Created profiles for users group')
        print('Start creating profiles for editors group')

        for i in range(10):
            profile = fake.profile(fields=['username', 'name', 'mail'])
            name = profile['name'].split(' ')
            if name.count == 3:
                fn = name[1]
                ln = name[2]
            else:
                fn = name[0]
                ln = name[1]

            user = User.objects.create_user(
                username=profile['username'],
                first_name=fn,
                last_name=ln,
                email=profile['mail'],
                password=PASSWORD,
                is_staff=True)

            user.groups.add(editorsGrop)

        print('Created profiles for editors group')
        print('Start creating profiles for moderators group')

        for i in range(10):
            profile = fake.profile(fields=['username', 'name', 'mail'])
            name = profile['name'].split(' ')
            if name.count == 3:
                fn = name[1]
                ln = name[2]
            else:
                fn = name[0]
                ln = name[1]

            user = User.objects.create_user(
                username=profile['username'],
                first_name=fn,
                last_name=ln,
                email=profile['mail'],
                password=PASSWORD,
                is_staff=True)

            user.groups.add(moderatorsGroup)

        print('Created profiles for moderators group')
        print('Start creating profiles for admins group')

        for i in range(3):
            profile = fake.profile(fields=['username', 'name', 'mail'])
            name = profile['name'].split(' ')
            if name.count == 3:
                fn = name[1]
                ln = name[2]
            else:
                fn = name[0]
                ln = name[1]

            user = User.objects.create_user(
                username=profile['username'],
                first_name=fn,
                last_name=ln,
                email=profile['mail'],
                password=PASSWORD,
                is_staff=True)

            user.groups.add(adminsGroup)

        print('Created profiles for admins group')

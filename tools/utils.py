from datetime import date
from django.utils.text import slugify


def unique_slug_generator(instance, field_name):
    class_manager = instance.__class__._default_manager

    test_slug = slugify(getattr(instance, field_name))

    if class_manager.filter(slug__iexact=test_slug).exists():
        test_slug = slugify('{}-{}'.format(getattr(instance, field_name), date.today()))

    objects_count = class_manager.filter(slug__icontains=test_slug).count()
    while class_manager.filter(slug__iexact=test_slug).exists():
        objects_count += 1
        test_slug = slugify('{}-{}-{}'.format(getattr(instance, field_name),
                                              date.today(),
                                              objects_count))

    return test_slug

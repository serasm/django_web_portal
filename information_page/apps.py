from django.apps import AppConfig


class InformationPageConfig(AppConfig):
    name = 'information_page'

    def ready(self):
        import information_page.signals

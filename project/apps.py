from django.apps import AppConfig



class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'

    def ready(self):
        import json
        from .views import json_sites
        from parsing.test_parsing import test_save
        with open('static/sites.json', 'r+') as j:
            json_sites.update( json.load(j))
        test_save() # init parsing


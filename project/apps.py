from django.apps import AppConfig
#from parsing.parse import parse_and_save



class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'

    def ready(self):
        import json
        from .views import json_sites
        with open('static/sites.json', 'r+') as j:
            json_sites.update( json.load(j))


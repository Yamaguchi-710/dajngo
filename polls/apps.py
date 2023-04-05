from django.apps import AppConfig
from .make_project import function

class Myapp1Config(AppConfig):
    #
    list_route = function.make()
    function.print_prj(list_route)
    #
    default_auto_field = "django.db.models.BigAutoField"
    name = "polls"

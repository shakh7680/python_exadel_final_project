from rest_framework_swagger.views import get_swagger_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.contrib import admin


API_TITLE = 'Cleaning Project'
API_DESCRIPTION = 'Cleaning'
yasg_schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version='v1',
        description=API_DESCRIPTION,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="burkhonovshakhzod@gmail.com"),
        license=openapi.License(name="Licence"),
    ),
    public=True,
    # permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

schema_view = get_swagger_view(title=API_TITLE)


admin.site.site_header = "Cleaning administration"
admin.site.site_title = "Cleaning administration"
admin.site.index_title = "Cleaning Project"

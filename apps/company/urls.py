from rest_framework import routers
from django.urls import path
from apps.company import views

router = routers.SimpleRouter()

router.register('equipments', views.CompanyServiceEquipmentsViewSet)

urlpatterns = [
    # path('equipments', views.ComCompanyServiceEquipmentsView)
] + router.urls
from rest_framework import routers
from django.urls import path
from apps.company import views

router = routers.SimpleRouter()

router.register('equipments', views.CompanyServiceEquipmentsViewSet)
router.register('rating', views.CompanyRatingViewSet)
router.register('location', views.CompanyLocationViewSet)

urlpatterns = [
      path("contacts/", views.CompanyContactsView.as_view()),
] + router.urls
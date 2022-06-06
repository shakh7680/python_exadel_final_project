from django.urls import path
from apps.client import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register('saved-company', views.SavedCompanyViewSet)
router.register('saved-company-list', views.SavedCompanyListView)
router.register('companies', views.CompanyViewForClient)

urlpatterns = [

] + router.urls

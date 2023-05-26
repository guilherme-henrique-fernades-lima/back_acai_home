from rest_framework.routers import SimpleRouter
from delivery.users.views import UserViewSet

routes = SimpleRouter()

routes.register(r'auth/users', UserViewSet, basename='users-module')

urlpatterns = [
    *routes.urls
]

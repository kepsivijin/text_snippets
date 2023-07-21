from django.urls import path,include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from rest_framework.routers import DefaultRouter
from snippets.views import  SnippetViewSet,TagDetailViewSet

router = DefaultRouter()
router.register(r'api/snippets', SnippetViewSet, basename='snippets_call')
router.register(r'api/tags', TagDetailViewSet, basename='tags')

urlpatterns = [
    path('api/token/', obtain_jwt_token, name='token_obtain_pair'),
    path('api/token/refresh/', refresh_jwt_token, name='token_refresh'),
    path('', include(router.urls)),

]

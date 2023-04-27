from rest_framework_nested import routers

from accounts.viewsets import UserViewSet
from master_app.viewsets.register import RegisterViewSet
from master_app.viewsets.login import  LoginViewSet
from master_app.viewsets.refresh import RefreshViewSet
from posts.viewsets import PostViewSet , CommentViewSet


router = routers.SimpleRouter()


# ##################################################################### #
# ################### USER ###################### #
# ##################################################################### #

router.register(r'user', UserViewSet, basename='user')


# ##################################################################### #
# ################### AUTH ###################### #
# ##################################################################### #

router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register('auth/refresh', RefreshViewSet, basename='auth-refresh')


# ##################################################################### #
# ################### POST  ###################### #
# ##################################################################### #


router.register(r'post', PostViewSet, basename='post')
posts_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
posts_router.register(r'comment', CommentViewSet, basename='post-comment')


urlpatterns = [
*router.urls,
*posts_router.urls
]
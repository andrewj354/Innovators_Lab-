from django.urls import re_path
from . import views


urlpatterns = [
    # User service routes
    re_path(r'^auth/.*', views.proxy_view, name='auth-proxy'),
    re_path(r'^users/.*', views.proxy_view, name='users-proxy'),

    # Product service routes
    re_path(r'^products/.*', views.proxy_view, name='products-proxy'),
    re_path(r'^categories/.*', views.proxy_view, name='categories-proxy'),

    # Cart service routes
    re_path(r'^cart/.*', views.proxy_view, name='cart-proxy'),

    # Order service routes
    re_path(r'^orders/.*', views.proxy_view, name='orders-proxy'),

    # Tournament service routes
    re_path(r'^tournaments/.*', views.proxy_view, name='tournaments-proxy'),
    re_path(r'^teams/.*', views.proxy_view, name='teams-proxy'),
    re_path(r'^tasks/.*', views.proxy_view, name='tasks-proxy'),
    re_path(r'^task-requirements/.*', views.proxy_view, name='task-requirements-proxy'),

    # Submission service routes
    re_path(r'^submissions/.*', views.proxy_view, name='submissions-proxy'),
    re_path(r'^jury-assignments/.*', views.proxy_view, name='jury-assignments-proxy'),
    re_path(r'^scores/.*', views.proxy_view, name='scores-proxy'),
    re_path(r'^leaderboard/.*', views.proxy_view, name='leaderboard-proxy'),
]

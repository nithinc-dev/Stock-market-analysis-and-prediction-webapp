from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('home',views.home, name='home'),
    path('stocks', views.stock_list, name='stock_list'),
    path('stocks/<int:stock_id>/chat/', views.stock_chat, name='stock_chat'),
    path('stocks/<int:stock_id>/messages/', views.get_messages, name='get_messages'),
    #path('visual', views.visualise, name='visualise'),
    path('visual', views.market, name='visualise'),
    path('news', views.news, name='news'),
    path('alert', views.get_alerts, name='get_alerts'),
    path('linear', views.linear, name='linear'),
    path('market', views.market, name='market'),
    path('market_status', views.market_status, name='market_status'),
    path('analytics' , views.analytics, name='analytics'),
]
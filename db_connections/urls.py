from . import views
from django.urls import path  

urlpatterns = [
    path('', views.home, name='home'),
    path('models/', views.view_models, name='view_models'),
    path('orm_console/', views.orm_console, name='orm_console'),
    path('database-settings/', views.edit_database_settings, name='edit_database_settings'),
    path('inspect-db/', views.inspect_db, name='inspect_db'),
    path('run-migrations/', views.run_migrations, name='run_migrations'),
    path('send-msg-model', views.send_msg_model, name='send_msg_model'),
]
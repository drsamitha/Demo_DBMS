from django.contrib import admin
from django.apps import apps

# Get the app config for your 'db_connections' app
app_config = apps.get_app_config('db_connections')

# Iterate through all models in the app and register them
for model in app_config.get_models():
    admin.site.register(model)


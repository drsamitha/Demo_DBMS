# # from django import forms
# # from .models import DatabaseConnection

# # class DatabaseConnectionForm(forms.ModelForm):
# #     password = forms.CharField(widget=forms.PasswordInput(), required=False)
    
# #     class Meta:
# #         model = DatabaseConnection
# #         fields = ['name', 'db_type', 'host', 'port', 'username', 'password', 'database_name']

# from django import forms
# from django.apps import apps

# def create_model_forms(app_label):
#     """Creates forms for all models in a given app."""
#     app_config = apps.get_app_config(app_label)
#     forms = {}
#     for model in app_config.get_models():
#         form_name = f"{model.__name__}Form"  # e.g., "MyModelForm"


#         class DynamicModelForm(forms.ModelForm):
#             class Meta:
#                 model = model
#                 fields = '__all__'  # Or specify fields you want to include

#         DynamicModelForm.__name__ = form_name  # Give the class a name
#         forms[form_name] = DynamicModelForm
#     return forms

# # In your views (or where you need the forms):
# #  dynamic_forms = create_model_forms('your_app_label')
# #  MyModelForm = dynamic_forms['MyModelForm']

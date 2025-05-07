# import os
# import subprocess
# import tempfile
# from io import StringIO
# from django.conf import settings
# from django.core.management import call_command
# from django.db import connections


# def configure_active_database(connection_obj):
#     """Configures database settings for a given connection object."""
#     base_config = {
#         'ATOMIC_REQUESTS': False,
#         'AUTOCOMMIT': True,
#         'CONN_MAX_AGE': 0,
#         'OPTIONS': {},
#         'TIME_ZONE': None,
#     }

#     if connection_obj.db_type == 'sqlite':
#         db_config = {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': connection_obj.database_name,
#         }
#     elif connection_obj.db_type == 'postgresql':
#         db_config = {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': connection_obj.database_name,
#             'USER': connection_obj.username,
#             'PASSWORD': connection_obj.password,
#             'HOST': connection_obj.host,
#             'PORT': connection_obj.port or '5432',
#         }
#     elif connection_obj.db_type == 'mysql':
#         db_config = {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': connection_obj.database_name,
#             'USER': connection_obj.username,
#             'PASSWORD': connection_obj.password,
#             'HOST': connection_obj.host,
#             'PORT': connection_obj.port or '3306',
#         }
#     else:
#         raise ValueError("Unsupported DB type")

#     # Merge base_config into db_config
#     return {**base_config, **db_config}

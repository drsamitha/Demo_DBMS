from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
# from .models import DatabaseConnection
# from .forms import DatabaseConnectionForm
# from .utils import configure_active_database
from django.conf import settings
from django.template import Template, Context
from django.db import connections
import sqlite3
import psycopg2
from pymongo import MongoClient
import mysql.connector
import djongo
import django
from django.contrib import messages
from django.core.management import call_command
from django.db import connection
from django.apps import apps
import json
import os
from io import StringIO
import sys
import traceback

# from .connection_context import *


# def select_connection(request, pk):
#     """Handles the selection of a database connection."""
#     connection_obj = get_object_or_404(DatabaseConnection, pk=pk)
#     db_alias = f"db_{pk}"
    
#     # Store the alias in the session
#     request.session['selected_db'] = db_alias
#     return redirect('orm_console')


def orm_console(request):
    """Handles the ORM console functionality."""
    selected_alias = request.session.get('selected_db', 'default')
    result = None
    error = None
    
    if request.method == 'POST':
        orm_code = request.POST.get('orm_code', '')
        if orm_code:
            try:
                # Create a new string buffer to capture print output
                output_buffer = StringIO()
                sys.stdout = output_buffer
                
                # Execute the code in a safe environment
                exec(orm_code, {'apps': apps, 'connection': connection})
                
                # Get the output
                result = output_buffer.getvalue()
                
                # Restore stdout
                sys.stdout = sys.__stdout__
                
            except Exception as e:
                error = str(e)
                traceback.print_exc()
    
    return render(request, 'db_connections/orm_console.html', {
        'selected_alias': selected_alias,
        'result': result,
        'error': error,
        'orm_code': request.POST.get('orm_code', '') if request.method == 'POST' else ''
    })


# def connection_list(request):
#     """Displays a list of database connections."""
#     connections = DatabaseConnection.objects.all()
#     current_selection = request.session.get('selected_db')
#     return render(
#         request,
#         'db_connections/connection_list.html',
#         {'connections': connections, 'current_selection': current_selection},
#     )


# def connection_detail(request, pk):
#     """Displays details for a specific connection."""
#     connection = get_object_or_404(DatabaseConnection, pk=pk)
#     return render(request, 'db_connections/connection_detail.html', {'connection': connection})


# def connection_new(request):
#     """Handles the creation of a new database connection."""
#     if request.method == "POST":
#         form = DatabaseConnectionForm(request.POST)
#         if form.is_valid():
#             connection = form.save()
#             return redirect('connection_detail', pk=connection.pk)
#     else:
#         form = DatabaseConnectionForm()
#     return render(request, 'db_connections/connection_edit.html', {'form': form})


# def connection_edit(request, pk):
#     """Handles the editing of an existing database connection."""
#     connection = get_object_or_404(DatabaseConnection, pk=pk)
#     if request.method == "POST":
#         form = DatabaseConnectionForm(request.POST, instance=connection)
#         if form.is_valid():
#             connection = form.save()
#             return redirect('connection_detail', pk=connection.pk)
#     else:
#         form = DatabaseConnectionForm(instance=connection)
#     return render(request, 'db_connections/connection_edit.html', {'form': form})


# def connection_delete(request, pk):
#     """Handles the deletion of a database connection."""
#     connection = get_object_or_404(DatabaseConnection, pk=pk)
#     connection.delete()
#     return redirect('connection_list')


# def test_connection(request, pk):
#     """Tests the connection to the specified database."""
#     connection = get_object_or_404(DatabaseConnection, pk=pk)
#     connection.last_connection_attempt = timezone.now()

#     try:
#         if connection.db_type == 'sqlite':
#             conn = sqlite3.connect(connection.database_name)
#         elif connection.db_type == 'postgresql':
#             conn = psycopg2.connect(
#                 host=connection.host,
#                 port=connection.port,
#                 user=connection.username,
#                 password=connection.password,
#                 dbname=connection.database_name,
#             )
#         elif connection.db_type == 'mysql':
#             conn = mysql.connector.connect(
#                 host=connection.host,
#                 port=connection.port,
#                 user=connection.username,
#                 password=connection.password,
#                 database=connection.database_name,
#             )
#         elif connection.db_type == 'mongodb':
#             conn_string = f"mongodb://"
#             if connection.username and connection.password:
#                 conn_string += f"{connection.username}:{connection.password}@"
#             conn_string += f"{connection.host}:{connection.port}"

#             client = MongoClient(conn_string)
#             db = client[connection.database_name]
#             # Test connection by attempting to list collections
#             _ = db.list_collection_names()
#             client.close()
#         else:
#             raise ValueError("Invalid DB type")

#         connection.connection_status = 'connected'
#         connection.error_message = ''

#     except Exception as e:
#         connection.connection_status = 'error'
#         connection.error_message = str(e)
#     finally:
#         if 'conn' in locals() and conn:
#              conn.close()

#     connection.save()
#     return JsonResponse(
#         {
#             'status': connection.connection_status,
#             'error_message': connection.error_message,
#             'last_attempt': connection.last_connection_attempt.isoformat(),
#         }
#     )

def edit_database_settings(request):
    """Handles database settings configuration."""
    if request.method == 'POST':
        db_config = request.POST.get('db_config', '')
        try:
            # Update settings.py with new database configuration
            settings_file = os.path.join(settings.BASE_DIR, 'Demo_DBMS', 'settings.py')
            with open(settings_file, 'r') as f:
                content = f.read()
            
            # Replace the DATABASES configuration
            start_marker = "DATABASES = {"
            end_marker = "}"  # This will be the last closing brace of the DATABASES dict
            
            start_idx = content.find(start_marker)
            if start_idx != -1:
                # Find the matching closing brace
                brace_count = 0
                end_idx = start_idx
                for i in range(start_idx, len(content)):
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
                
                new_content = content[:start_idx] + db_config + content[end_idx:]
                
                with open(settings_file, 'w') as f:
                    f.write(new_content)
                
                messages.success(request, 'Database settings updated successfully!')
                
                # Run the setup script to handle migrations and app restart
                try:
                    # Store the current database settings in session for the setup script
                    request.session['db_config'] = db_config
                    
                    # Run the setup command
                    call_command('run_setup')
                    messages.success(request, 'Database setup completed successfully!')
                except Exception as e:
                    messages.warning(request, f'Warning: Error during setup: {str(e)}')
                    messages.info(request, 'Please run the setup manually using the "Run Setup" button.')
                
            else:
                messages.error(request, 'Could not find DATABASES configuration in settings.py')
                
        except Exception as e:
            messages.error(request, f'Error updating database settings: {str(e)}')
    
    # Read current database configuration
    try:
        settings_file = os.path.join(settings.BASE_DIR, 'Demo_DBMS', 'settings.py')
        with open(settings_file, 'r') as f:
            content = f.read()
        
        start_marker = "DATABASES = {"
        end_marker = "}"  # This will be the last closing brace of the DATABASES dict
        
        start_idx = content.find(start_marker)
        if start_idx != -1:
            # Find the matching closing brace
            brace_count = 0
            end_idx = start_idx
            for i in range(start_idx, len(content)):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            
            db_config = content[start_idx:end_idx]
        else:
            db_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
    except Exception as e:
        db_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
        messages.error(request, f'Error reading database settings: {str(e)}')
    
    return render(request, 'db_connections/edit_database_settings.html', {
        'db_config': db_config
    })

# def setup_progress(request):
#     """View to show setup progress and handle app restart"""
#     if request.method == 'POST':
#         try:
#             # Run the setup command in a separate process
#             call_command('run_setup')
#             request.session['setup_status'] = 'completed'
#         except Exception as e:
#             request.session['setup_status'] = 'error'
#             request.session['setup_error'] = str(e)
        
#         return JsonResponse({'status': request.session.get('setup_status')})
    
#     return render(request, 'db_connections/setup_progress.html', {
#         'status': request.session.get('setup_status', 'pending')
#     })

def inspect_db(request):
    """Inspects the database and generates models."""
    try:
        # Get the current database engine
        db_engine = settings.DATABASES['default']['ENGINE']
        
        # Check if the database is properly configured
        if not db_engine:
            messages.error(request, 'No database engine configured. Please set up your database settings first.')
            return redirect('edit_database_settings')
            
        # Generate models from the database
        output = StringIO()
        try:
            call_command('inspectdb', stdout=output)
            new_models_content = output.getvalue()
            
            # Read the existing models.py file to preserve DatabaseConnection model
            models_file = os.path.join(settings.BASE_DIR, 'db_connections', 'models.py')
            try:
                with open(models_file, 'r') as f:
                    existing_content = f.read()
            except FileNotFoundError:
                existing_content = ""
            
            # Extract the DatabaseConnection model if it exists
            db_connection_model = ""
            if "class DatabaseConnection" in existing_content:
                start_idx = existing_content.find("class DatabaseConnection")
                end_idx = existing_content.find("class", start_idx + 1)
                if end_idx == -1:
                    end_idx = len(existing_content)
                db_connection_model = existing_content[start_idx:end_idx].strip()
            
            # Combine the content
            models_content = """from django.db import models
from django.utils import timezone

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

"""
            # Add the DatabaseConnection model first if it exists
            if db_connection_model:
                models_content += db_connection_model + "\n\n"
            
            # Add the new models
            models_content += new_models_content
            
            # Save the combined models to the file
            with open(models_file, 'w') as f:
                f.write(models_content)
            
            messages.success(request, 'Models generated successfully from database!')
            
            # Run migrations after generating models
            try:
                call_command('makemigrations')
                call_command('migrate')
                messages.success(request, 'Migrations completed successfully!')
            except Exception as e:
                messages.warning(request, f'Warning: Error during migrations: {str(e)}')
                messages.info(request, 'Please run migrations manually using the "Run Migrations" button.')
                
        except Exception as e:
            messages.error(request, f'Error during model inspection: {str(e)}')
            messages.info(request, 'Make sure your database is properly configured and accessible.')
            
    except Exception as e:
        messages.error(request, f'Error during database inspection: {str(e)}')
    
    return redirect('edit_database_settings')

def run_migrations(request):
    """Runs database migrations."""
    try:
        call_command('makemigrations')
        call_command('migrate')
        messages.success(request, 'Migrations completed successfully!')
    except Exception as e:
        messages.error(request, f'Error during migrations: {str(e)}')
    
    return redirect('edit_database_settings')

def get_django_field_type(db_type):
    type_mapping = {
        'integer': 'IntegerField',
        'character varying': 'CharField',
        'text': 'TextField',
        'boolean': 'BooleanField',
        'timestamp': 'DateTimeField',
        'date': 'DateField',
        'numeric': 'DecimalField',
        'double precision': 'FloatField',
    }
    return type_mapping.get(db_type.lower(), 'CharField')

def home(request):
    """Displays the home page with quick access to main features."""
    # Set default database if none is selected
    if not request.session.get('selected_db'):
        request.session['selected_db'] = 'default'
    
    selected_db = request.session.get('selected_db')
    return render(request, 'db_connections/home.html', {
        'selected_db': selected_db
    })

def view_models(request):
    try:
        # Get the path to models.py
        models_path = os.path.join(settings.BASE_DIR, 'db_connections', 'models.py')
        
        # Read the content of models.py
        with open(models_path, 'r') as f:
            models_content = f.read()
            
        return render(request, 'db_connections/view_models.html', {
            'models_content': models_content
        })
    except FileNotFoundError:
        # If models.py doesn't exist, create it with basic content
        models_content = """from django.db import models

# Your models will be generated here after inspecting the database.
# Use the 'Inspect Database' button to generate models from your database schema.
"""
        with open(models_path, 'w') as f:
            f.write(models_content)
            
        return render(request, 'db_connections/view_models.html', {
            'models_content': models_content
        })
    except Exception as e:
        messages.error(request, f'Error reading models.py: {str(e)}')
        return redirect('home')

# send user query with model to server
def send_msg_model(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            message = data.get('message')
            
            response_data = {'response': f"View received message: '{message}' and processed it successfully."} 
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)  
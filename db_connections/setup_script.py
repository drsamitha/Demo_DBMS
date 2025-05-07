import os
import sys
import json
import time
import django
from pathlib import Path

# Set up Django
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Demo_DBMS.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from django.conf import settings

def run_setup():
    try:
        # Get database configuration
        db_config = settings.DATABASES.get('default', {})
        if not db_config:
            print("No database configuration found")
            return False

        # Wait for database to be ready
        print("Waiting for database to be ready...")
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT 1')
                break
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    print(f"Database not ready after {max_retries} attempts")
                    return False
                time.sleep(2)

        # Run migrations
        print("Running migrations...")
        call_command('makemigrations')
        call_command('migrate')

        # For PostgreSQL, inspect and generate models
        if db_config.get('ENGINE') == 'django.db.backends.postgresql':
            print("Inspecting database and generating models...")
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """)
                    tables = cursor.fetchall()
                
                # Generate model code
                model_code = []
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns
                        WHERE table_name = '{table_name}'
                    """)
                    columns = cursor.fetchall()
                    
                    model_code.append(f"class {table_name.capitalize()}(models.Model):")
                    for column in columns:
                        col_name, data_type, is_nullable = column
                        field_type = get_django_field_type(data_type)
                        null_str = ", null=True" if is_nullable == 'YES' else ""
                        model_code.append(f"    {col_name} = models.{field_type}{null_str}")
                    model_code.append("")
                
                # Update models.py
                models_path = os.path.join(settings.BASE_DIR, 'Demo_DBMS', 'models.py')
                with open(models_path, 'w') as f:
                    f.write("from django.db import models\n\n")
                    f.write("\n".join(model_code))
                
                print("Models generated successfully")
            except Exception as e:
                print(f"Error during model inspection: {str(e)}")
                return False

        print("Setup completed successfully")
        return True

    except Exception as e:
        print(f"Error during setup: {str(e)}")
        return False

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

if __name__ == '__main__':
    success = run_setup()
    sys.exit(0 if success else 1) 
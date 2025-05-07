from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings
import os
import json
import time

class Command(BaseCommand):
    help = 'Sets up database after configuration changes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--inspect-only',
            action='store_true',
            help='Only inspect database and generate models',
        )
        parser.add_argument(
            '--migrate-only',
            action='store_true',
            help='Only run migrations',
        )

    def handle(self, *args, **options):
        try:
            # Get database configuration
            db_config = settings.DATABASES.get('default', {})
            if not db_config:
                self.stdout.write(self.style.ERROR('No database configuration found'))
                return

            # Wait for database to be ready
            self.stdout.write('Waiting for database to be ready...')
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
                        self.stdout.write(self.style.ERROR(f'Database not ready after {max_retries} attempts'))
                        return
                    time.sleep(2)

            # Inspect database and generate models if requested
            if not options['migrate_only']:
                if db_config.get('ENGINE') == 'django.db.backends.postgresql':
                    self.stdout.write('Inspecting database and generating models...')
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
                                field_type = self.get_django_field_type(data_type)
                                null_str = ", null=True" if is_nullable == 'YES' else ""
                                model_code.append(f"    {col_name} = models.{field_type}{null_str}")
                            model_code.append("")
                        
                        # Update models.py
                        models_path = os.path.join(settings.BASE_DIR, 'Demo_DBMS', 'models.py')
                        with open(models_path, 'w') as f:
                            f.write("from django.db import models\n\n")
                            f.write("\n".join(model_code))
                        
                        self.stdout.write(self.style.SUCCESS('Models generated successfully'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error during model inspection: {str(e)}'))
                else:
                    self.stdout.write(self.style.WARNING('Model inspection is only available for PostgreSQL databases'))

            # Run migrations if requested
            if not options['inspect_only']:
                self.stdout.write('Running migrations...')
                try:
                    call_command('makemigrations')
                    call_command('migrate')
                    self.stdout.write(self.style.SUCCESS('Migrations completed successfully'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error during migrations: {str(e)}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during setup: {str(e)}'))

    def get_django_field_type(self, db_type):
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
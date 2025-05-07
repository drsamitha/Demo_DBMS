import os
import sys
import json
import signal
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Runs the database setup process in a separate process'

    def handle(self, *args, **options):
        try:
            # Get the path to the setup script
            setup_script = os.path.join(settings.BASE_DIR, 'db_connections', 'setup_script.py')
            
            # Start the setup script as a separate process
            process = subprocess.Popen([sys.executable, setup_script],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            
            # Wait for the process to complete
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.stdout.write(self.style.SUCCESS('Setup completed successfully'))
                return True
            else:
                self.stdout.write(self.style.ERROR(f'Setup failed: {stderr.decode()}'))
                return False
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during setup: {str(e)}'))
            return False 
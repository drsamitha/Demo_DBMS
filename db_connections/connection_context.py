# from django.db import connections, close_old_connections

# # Store active database connections
# ACTIVE_CONNECTIONS = {}

# class ConnectionContext:
#     """Context manager for database connections."""
    
#     def __init__(self, alias=None):
#         self.alias = alias

#     def __enter__(self):
#         if self.alias and self.alias in ACTIVE_CONNECTIONS:
#             db_config = ACTIVE_CONNECTIONS[self.alias]
#             if self.alias not in connections.databases:
#                 connections.databases[self.alias] = db_config
#             close_old_connections()
#             return connections[self.alias]
#         return connections["default"]

#     def __exit__(self, exc_type, exc_value, traceback):
#         if self.alias in connections:
#             connections[self.alias].close()

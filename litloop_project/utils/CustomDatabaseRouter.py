class CustomDatabaseRouter:
    def db_for_read(self, model, **hints):
        if 'postgres' in settings.DATABASES[model._meta.app_label]['ENGINE']:
            return 'postgres_db'
        else:
            return None

    def db_for_write(self, model, **hints):
        if 'cassandra' in settings.DATABASES[model._meta.app_label]['ENGINE']:
            return 'cassandra_db'
        else:
            return None

class MultiDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'logging_service': 
            return 'user_logs'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'logging_service':
            return 'user_logs'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == 'logging_service' or
            obj2._meta.app_label == 'logging_service'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'logging_service':
            return db == 'user_logs'
        return db == 'default'

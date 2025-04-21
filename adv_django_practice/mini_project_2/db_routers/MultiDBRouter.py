# mini_project_2/db_routers.py

class MultiDBRouter:
    """
    A router to control all database operations on models for different databases.
    """
    
    def db_for_read(self, model, **hints):
        """
        Point all read operations to the specific database based on the model's app label.
        """
        if model._meta.app_label == 'user_activity':
            return 'user_logs'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Point all write operations to the specific database based on the model's app label.
        """
        if model._meta.app_label == 'user_activity':
            return 'user_logs'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the same database.
        """
        db1 = self.db_for_read(obj1.__class__)
        db2 = self.db_for_read(obj2.__class__)
        if db1 == db2:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Only migrate models in 'user_activity' to 'user_logs'; others to 'default'.
        """
        if app_label == 'user_activity':
            return db == 'user_logs'
        return db == 'default'

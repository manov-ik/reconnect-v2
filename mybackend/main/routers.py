class AuthRouter:
    """
    A router to control database operations for auth models.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'auth' or model._meta.model_name == 'customuser':
            return 'auth_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'auth' or model._meta.model_name == 'customuser':
            return 'auth_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in auth is involved.
        """
        if (
            obj1._meta.app_label == 'auth' or
            obj2._meta.app_label == 'auth' or
            obj1._meta.model_name == 'customuser' or
            obj2._meta.model_name == 'customuser'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth models only appear in the 'auth_db' database.
        """
        if app_label == 'auth' or (model_name and model_name.lower() == 'customuser'):
            return db == 'auth_db'
        return None 
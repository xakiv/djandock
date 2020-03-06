import logging

logger = logging.getLogger(__name__)


class MyShinyRouter:
    """
    Permet de diriger les accés de l'application {APP_NAME}
    vers et depuis la base {DB_NAME} (cf settings.DATABASE)

    On migrera les modèles de l'application {APP_NAME} par:
    $ python manage.py migrate {APP_NAME} --database={DB_NAME}
    """

    APP_NAME = 'another_one'
    DB_NAME = 'switch'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.APP_NAME:
            return self.DB_NAME
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.APP_NAME:
            return self.DB_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == self.APP_NAME or \
                obj2._meta.app_label == self.APP_NAME:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Permet de choisir si on veut autoriser les migrations

        if db == self.DB_NAME:
            return app_label == self.APP_NAME
        elif app_label == self.APP_NAME:
            return False

        return None

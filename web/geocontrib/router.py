class MyShinyRouter:
    """
    Permet de diriger les accés de l'application {APP_NAME}
    vers et depuis la base {DB_NAME} (cf settings.DATABASE)

    On migrera ces les modèles de l'application paiement_app par:
    $ python manage.py migrate {APP_NAME} --database={DB_NAME}
    """

    APP_NAME = 'geocontrib'
    DB_NAME = 'default'
    ALLOWING_APP_MIGRATIONS = True
    allowed_apps = (
        APP_NAME,
    )

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.allowed_apps:
            return self.DB_NAME
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.allowed_apps:
            return self.DB_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.allowed_apps or \
                obj2._meta.app_label in self.allowed_apps:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Permet de choisir si on veut autorisé les migrations

        # Autorisation de migrations de APP_NAME sur base DB_NAME
        # Si on présente une migration qui concerne notre application
        if app_label in self.allowed_apps:
            return db == self.DB_NAME and self.ALLOWING_APP_MIGRATIONS

        # SI le param --database=DB_NAME
        elif db == self.DB_NAME:
            return self.ALLOWING_APP_MIGRATIONS

        return None

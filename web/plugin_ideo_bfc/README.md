
# SID

## Configuration

**Dans le fichier _settings.py_ de l'application :**

* Ajouter l'application :

    ```
    INSTALLED_APPS = [
        # ...
        'plugin_ideo_bfc',
        # ...
    ]
    ```

* Ajouter les modules d'authentification à la liste des Middleware dans le settings.py de l'application :

    ```
    MIDDLEWARE = [
        # ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'plugin_ideo_bfc.auth.middleware.SidRemoteUserMiddleware',
        # ...
    ```

* Activer le module, indiquer l'attribut du HEADER et l'url de fermeture de session

    ```
    OIDC_SETTED = True  # False par défaut
    HEADER_UID = 'OIDC_CLAIM_uid'  # Valeur par défaut
    SSO_LOGOUT_URL = ''
    ```


### Dans le fichier _urls.py_ de l'application


## Informations utiles


L'_username_ du modèle **User** de Django correspond à l'identifiant de l'agent/employée.

# Maquette fonctionnelle d'application django dockerisé
---

### Remarques:
- Le site admin django est accessible avec un utilisateur initialisé,
- Le code de démo est dynamiquement mis à jour à chaud,
- Contient une base de travail pour un projet django/geodjango avec une base
postgres,
- La base postrges est accessible depuis la machine hôte

### Récuperer les sources
```shell
git clone https://gitlab.com/cbngcontact/djandock.git djandock
```

### Définir les variable d'environnement à partir du pattern fournit dans web/env_sample
```shell
cp ~/djandock/web/env_sample ~/djandock/web/.env
```

### Builder les services definie par notre docker-compose
```shell
$ docker-compose -f docker-compose.yml build
```

### Démarrer les docker et rebuilder si besoin
```shell
$ docker-compose -f docker-compose.yml up --build
```

### Démarrer un shell qui charge les variables d'environment
```shell
$ docker run --env-file=web/.env -it djandock_web bash
```

### Possibilité de connecter la base postgres du contenaire avec un pgadmin du Host
cf docker-compose.yml -> host: localhost / port: 5444 / username: postgres / pwd: postgres
```yaml
# ...
postgres:
    # ...
    ports:
      - "5444:5432"
    expose:
      - 5432
# ...
```

### Environnement de Dev
On met en place un venv sur le host en reprenant les dépendances du 'requirements.txt'
```shell
$ python3.8 -m venv dev-venv
$ source dev-venv/bin/activate
$ pip install -r ~/djandock/web/requirements.txt
$ pip install --upgrade pip
```

### Sauvegarder l'état courant dans la base de donnée
On met en place un venv sur le host en reprenant les dépendances du 'requirements.txt'
```shell
$ docker run --env-file=web/.env -it djandock_web bash
$ python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > dump.json
```

### Quelque commandes docker-compose
```shell
$ docker system prune -a  # Supprime toute trace des containers sur le Host

$ docker rm $(docker ps -aq)

$ docker stop $(docker ps -aq)
```

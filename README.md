# Sentinel

Sentinel est un micro-service backend autonome de surveillance de marque et d'anti-contrefaçon. Il automatise la détection de l'utilisation non autorisée de marques sur des pages web suspectes et génère des preuves visuelles pour usage juridique.

## Fonctionnalités principales

1. Réception de mission : API REST pour soumettre des URL suspectes et des marques à surveiller.
2. Navigation autonome : Utilisation de Playwright (Chromium) pour naviguer sur les sites, y compris les applications à page unique (SPA) complexes.
3. Détection intelligente : Analyse du DOM pour localiser les occurrences textuelles de la marque de manière insensible à la casse.
4. Génération de preuve :
    * Surlignage visuel : Injection de JavaScript pour entourer la marque détectée en rouge et jaune.
    * Capture complète : Capture d'écran pleine page horodatée.
5. Traitement asynchrone : Architecture non-bloquante permettant de gérer plusieurs investigations en parallèle.

## Stack technique

* Langage : Python 3.10+
* API Framework : FastAPI avec documentation Swagger automatique
* Automatisation navigateur : Playwright moteur Chromium
* Base de données : PostgreSQL 15
* ORM : SQLAlchemy asynchrone
* Infrastructure : Docker et Docker Compose

## Installation et démarrage

### Prérequis

Docker et Docker Compose installés sur votre machine.

### Lancement rapide

1. Démarrer le service :
   À la racine du projet, exécutez la commande suivante :
   ```bash
   docker-compose up --build -d
   ```

2. Accéder à l'API :
   L'interface de documentation interactive est disponible à l'adresse :
   http://localhost:8001/docs

### Tester le projet

Un script de démonstration est fourni pour peupler la base de données avec des missions de test sur des sites réels et des cas témoins.

1. Lancer le script de test :
   ```bash
   python3 scripts/populate_db.py
   ```

2. Vérifier les résultats :
   * Les statuts des missions seront mis à jour de PENDING vers PROCESSING puis DETECTED ou CLEAN.
   * Les preuves visuelles sont sauvegardées dans le dossier local : ./evidence/.

## Structure du projet

app : Routes, configuration, modèles de données et logique de crawling.
evidence : Dossier de stockage des captures d'écran générées.
scripts : Scripts utilitaires pour le test et le peuplement.
docker-compose.yml : Orchestration des services API et base de données.
Dockerfile : Configuration de l'image pour le micro-service Python.
requirements.txt : Liste des dépendances du projet.

## Workflow d'une investigation

1. POST /missions/ : L'utilisateur soumet le nom de la marque et l'URL cible.
2. Enregistrement : La mission est stockée en base de données et une tâche de fond est déclenchée.
3. Analyse : Le robot lance un navigateur et visite l'URL demandée.
4. Détection : Si la marque est trouvée, le système effectue un surlignage et prend une capture d'écran.
5. Résultat : Le statut est mis à jour en DETECTED (si trouvé) ou CLEAN (si absent).
6. GET /missions/{id} : Récupération du rapport final et du chemin vers la preuve visuelle.

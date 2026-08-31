# TradeCorp International - Pipeline ETL Big Data & DevOps


##  À propos du projet
Ce projet implémente un pipeline ETL complet basé sur **Apache Spark (PySpark)** pour traiter et transformer les données de l'entreprise TradeCorp (inspirées de Northwind). L'ensemble de la solution est conteneurisé via **Docker**, testé rigoureusement avec **Pytest**, et structuré selon les bonnes pratiques du Data Engineering et du DevOps.

---

##  Structure du Projet

```text
tradecorp/
├── data/
│   ├── raw/                 # Fichiers CSV sources (Northwind)
│   ├── output/              # Fichiers transformés (Parquet) - ignorés par Git
│   └── tmp/                 # Fichiers temporaires - ignorés par Git
├── notebooks/               # Notebooks Jupyter d'analyse et d'expérimentation
│   ├── 01_exploration.ipynb # Exploration initiale des données CSV
│   ├── 02_nettoyage.ipynb   # Nettoyage et préparation des dataframes
│   ├── 03_transformations.ipynb # Transformations PySpark avancées & requêtes analytiques (Q26-Q29)
│   ├── 04_parquet_et_postgres.ipynb # Export au format Parquet et chargement en base PostgreSQL
│   ├── 05_test_reader.ipynb # Validation des modules de lecture
│   └── 06_tests_unitaires.ipynb # Expérimentation et validation des tests
├── src/                     # Code source modulaire du pipeline ETL
│   ├── pipeline.py          # Orchestration globale du pipeline
│   ├── reader.py            # Chargement des données sources
│   ├── transformer.py       # Logique de nettoyage et de transformation
│   └── writer.py            # Sauvegarde des données (Parquet / PostgreSQL)
├── tests/                   # Tests unitaires Pytest
│   └── conftest.py          # Configuration de la session Spark pour les tests
├── docker-compose.yml       # Configuration des services Docker (Spark / Jupyter / PostgreSQL)
├── run_tests.sh             # Script d'automatisation pour lancer les tests
└── .env                     # Variables d'environnement - ignoré par Git
```

##  Stack Technique

- Big Data & Traitement : Apache Spark, PySpark, Python 3.11

- Base de données : PostgreSQL

- Infrastructure : Docker, Docker Compose

- Qualité & Tests : Pytest


## Utilisation et Commandes

1. Lancer l'environnement Docker
Démarre les conteneurs du projet :

```bash
docker compose up -d
```

2. Exécuter les tests unitaires
Le projet intègre une suite de tests unitaires validant les différentes fonctions de transformation.
On peut lancer l'ensemble des tests via le script dédié :

```bash
./run_tests.sh
```
Ou directement via Docker : 

```bash
docker exec -it tradecorp_spark /opt/conda/bin/python3 -m pytest -o pythonpath='src'
```
Prochaines étapes & Avancement
- [x] Note de cadrage & Estimation Azure Pricing
- [x] Infrastructure Docker / Spark / PostgreSQL
- [x] Implémentation des notebooks d'exploration et de nettoyage
- [x] Développement des modules Python modulaires (`src/`)
- [x] Mise en place des tests unitaires (`Pytest`) et industrialisation









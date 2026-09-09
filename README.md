# TradeCorp International - Pipeline ETL Big Data & DevOps


##  À propos du projet
Ce projet implémente un pipeline ETL automatisé et sécurisé pour l'entreprise TradeCorp (données inspirées de Northwind), conçu pour remplacer un processus manuel quotidien de 3 heures. Il repose sur Apache Spark (PySpark) pour le traitement distribué, Apache Airflow pour l'orchestration, Azure ADLS Gen2 pour le stockage cloud centralisé, et Azure Key Vault pour la gestion sécurisée des secrets. L'ensemble est conteneurisé via Docker et testé rigoureusement avec Pytest.

---

##  Structure du Projet

```text
tradecorp/
├── dags/                    # DAGs Apache Airflow pour l'orchestration des pipelines
├── data/
│   ├── raw/                 # Fichiers CSV sources (Northwind)
│   ├── output/              # Fichiers transformés au format Parquet (ignorés par Git)
│   └── tmp/                 # Fichiers temporaires (ignorés par Git)
├── notebooks/               # Notebooks Jupyter d'analyse et d'expérimentation
│   ├── 01_exploration.ipynb # Exploration initiale des données CSV
│   ├── 02_nettoyage.ipynb   # Nettoyage et préparation des dataframes
│   ├── 03_transformations.ipynb # Transformations PySpark avancées
│   ├── 04_parquet.ipynb     # Export et validation au format Parquet
│   └── ...                  # Autres notebooks de test et validation
├── src/                     # Code source modulaire du pipeline ETL
│   ├── enrichment.py        # Logique d'enrichissement des données
│   ├── fetch_exchange_rates.py # Récupération des taux de change
│   ├── pipeline.py          # Orchestration globale du pipeline
│   ├── reader.py            # Chargement et téléchargement depuis ADLS Gen2
│   ├── transformer.py       # Logique de nettoyage et de transformation PySpark
│   ├── upload_country_currency.py # Gestion des référentiels pays/devises
│   ├── utils.py             # Fonctions utilitaires et client Azure Blob Service
│   └── writer.py            # Sauvegarde des données (export Parquet optimisé)
├── tests/                   # Tests unitaires Pytest
│   └── conftest.py          # Configuration de la session Spark pour les tests
├── Dockerfile               # Image Docker pour les traitements Spark
├── Dockerfile.airflow       # Image Docker pour l'orchestration Airflow
├── docker-compose.yml       # Configuration des services Docker (Spark / Airflow / Jupyter)
├── run_tests.sh             # Script d'automatisation pour lancer les tests
├── .env.example             # Modèle de variables d'environnement (versionné)
└── .env                     # Variables d'environnement et secrets (ignoré par Git)
```

##  Stack Technique

- Big Data & Traitement : Apache Spark, PySpark, Python 3.11

- Orchestration : Apache Airflow

- Cloud & Stockage : Azure Data Lake Storage (ADLS Gen2), Azure Key Vault (Sécurité & Secrets)

- Infrastructure : Docker, Docker Compose

- Qualité & Tests : Pytest, tests unitaires automatisés


## Utilisation et Commandes

### 1. Configuration de l'environnement
Avant de lancer les conteneurs, dupliquez le modèle de configuration et remplissez les valeurs de vos variables :
```bash
cp .env.example .env
```
N.B : Pensez à renseigner vos propres valeurs de configuration dans le fichier .env nouvellement créé.

### 2. Lancer l'environnement Docker
Démarre les conteneurs du projet :

```bash
docker compose up -d
```

### 3. Exécuter les tests unitaires
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









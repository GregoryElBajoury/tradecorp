#!/bin/bash

echo "Lancement du pipeline ETL..."
docker exec -it tradecorp_spark python src/pipeline.py
echo "Pipeline terminé !"

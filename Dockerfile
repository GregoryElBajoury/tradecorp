FROM jupyter/pyspark-notebook:spark-3.5.0

COPY requirements.txt /tmp/requirements.txt

USER root
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Rebasculer sur l'utilisateur standard par défaut de l'image Jupyter
USER jovyan
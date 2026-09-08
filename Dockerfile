FROM jupyter/pyspark-notebook:spark-3.5.0

COPY requirements.txt /tmp/requirements.txt

USER root
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt /home/jovyan/.cache/pip

USER jovyan


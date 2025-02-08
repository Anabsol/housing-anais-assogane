FROM ghcr.io/mlflow/mlflow:v2.0.1

ENV MLFLOW_TRACKING_URI=http://mlflow:5000
ENV BACKEND_STORE_URI=sqlite:///mlflow.db
ENV ARTIFACT_STORE=s3://mlflow-artifacts/

VOLUME ./mlflow:/mlflow

CMD mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root /mlflow --host 0.0.0.0 --port 5000

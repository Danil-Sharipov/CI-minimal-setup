import os
from airflow.models.connection import Connection


conn = Connection(
    conn_id="sample_aws_connection",
    conn_type="aws",
    login="CxrzoH4Ye0Cgiwm1znpp",  # Reference to AWS Access Key ID
    password="frASzoho4X76UbqWSIw7GHuTbQ5fmKT2sv3Qftml",  # Reference to AWS Secret Access Key
    extra={
        # Specify extra parameters here
        "region_name": "eu-central-1",
        "endpoint_url": "https://minio.com"
    },
)

print(conn.test_connection())  # Validate connection credentials.

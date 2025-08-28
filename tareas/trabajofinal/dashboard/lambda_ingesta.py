
import json
import boto3
import pandas as pd
import io
from datetime import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'xideralaws-curso-osvaldo'

    try:
        # Leer datos raw desde S3
        response = s3.get_object(
            Bucket=bucket_name, 
            Key='ukraine-war-project/raw-data/russia_losses_equipment.parquet'
        )
        df = pd.read_parquet(io.BytesIO(response['Body'].read()))

        # Procesar datos (limpieza básica)
        df_clean = df.dropna()
        df_clean = df_clean[df_clean.select_dtypes(include='number').ge(0).all(axis=1)]

        # Subir datos limpios
        buffer = io.BytesIO()
        df_clean.to_parquet(buffer, engine='pyarrow', index=False)

        s3.put_object(
            Bucket=bucket_name,
            Key='ukraine-war-project/processed-data/equipment_cleaned.parquet',
            Body=buffer.getvalue()
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Datos procesados exitosamente',
                'records_processed': len(df_clean),
                'timestamp': datetime.now().isoformat()
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

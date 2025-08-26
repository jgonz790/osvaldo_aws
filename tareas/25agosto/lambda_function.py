import json
import boto3
import io
import pandas as pd

s3 = boto3.client("s3")

def lambda_handler(event, context):
    buffer = io.BytesIO()
    s3.download_fileobj(
        Bucket="xideralaws-curso-osvaldo",
        Key="nyc_taxi_2023/yellow_tripdata_2023-01.parquet",
        Fileobj=buffer
    )
    
    buffer.seek(0)
    df = pd.read_parquet(buffer, engine="pyarrow")
    df = df.dropna()
    df = df.drop_duplicates()
    
    cols = ["passenger_count", "trip_distance", "fare_amount", "extra", "tip_amount", "total_amount", "airport_fee"]
    averages = df[cols].mean()
    averages_df = averages.to_frame().T
    averages_df["source_file"] = "yellow_tripdata_2023-01.parquet"
    
    output_buffer = io.BytesIO()
    averages_df.to_parquet(output_buffer, engine="pyarrow", index=False)
    output_buffer.seek(0)
    
    s3.put_object(
        Bucket="xideralaws-curso-osvaldo",
        Key="nyc_taxi_2023/processed/averages/yellow_tripdata_2023-01-avg.parquet",
        Body=output_buffer.getvalue()
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps("Processed data saved to S3")
    }

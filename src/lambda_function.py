import json
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Process Kafka stream event
    for record in event['Records']:
        data = json.loads(record['kinesis']['data'])
        transaction_id = data['transaction_id']
        amount = data['amount']
        
        # Example: Save to S3
        s3_client.put_object(
            Bucket='your-bucket',
            Key=f'raw-data/{transaction_id}.json',
            Body=json.dumps(data)
        )
        
        # Optional: Add anomaly detection or NLP
        # E.g., if amount > 1000, flag as anomaly
        if amount > 1000:
            print(f"Anomaly detected: {data}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processed successfully')
    }
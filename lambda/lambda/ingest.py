import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

table = dynamodb.Table('DriverEvents')

BUCKET_NAME = 'pasindu-telematics-data-2026'

def lambda_handler(event, context):

    # Handle API Gateway request body
    if 'body' in event:
        body = json.loads(event['body'])
    else:
        body = event

    speed = body.get('speed', 0)
    acceleration = body.get('acceleration', 0)

    behaviour = "NORMAL"

    if acceleration < -0.3:
        behaviour = "HARSH_BRAKING"
    elif acceleration > 0.3:
        behaviour = "RAPID_ACCELERATION"

    event_id = str(uuid.uuid4())

    item = {
        'eventId': event_id,
        'speed': speed,
        'acceleration': acceleration,
        'behaviour': behaviour
    }

    table.put_item(
        Item={
            'eventId': event_id,
            'speed': speed,
            'acceleration': str(acceleration),
            'behaviour': behaviour
        }
    )

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f'events/{event_id}.json',
        Body=json.dumps(item)
    )

    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

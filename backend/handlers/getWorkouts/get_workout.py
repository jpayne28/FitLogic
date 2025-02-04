import json
import boto3
import os
import random
import logging
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Add class to handle Decimal serialization
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    params = event.get('queryStringParameters')
    
    if not params:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Missing query parameters'})
        }

    try:
        muscle_group = params.get('muscleGroup', '').lower()
        weighted = params.get('weighted', '').lower()
        duration = int(params.get('duration', 30))

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['WORKOUT_TABLE'])

        # Query DynamoDB
        response = table.query(
            IndexName='WeightedMuscleGroupIndex',
            KeyConditionExpression='Weighted = :weighted AND MuscleGroup = :mg',
            ExpressionAttributeValues={
                ':weighted': weighted,
                ':mg': muscle_group
            }
        )

        all_exercises = response.get('Items', [])
        
        if not all_exercises:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': f'No {weighted} exercises found for {muscle_group}'
                })
            }

        # Calculate exercises needed for requested duration
        num_exercises_needed = duration // 5 # DecimalEncoder
        print(f"Number of exercises needed for {duration} minutes: {num_exercises_needed}")

        selected_exercises = random.sample(
            all_exercises,
            min(num_exercises_needed, len(all_exercises))
        )

        print(f"Selected {len(selected_exercises)} exercises")

        workout_plan = {
            'requested_duration': duration,
            'actual_duration': len(selected_exercises) * 5,
            'exercises_count': len(selected_exercises),
            'muscle_group': muscle_group,
            'weighted': weighted,
            'exercises': selected_exercises
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(workout_plan, cls=DecimalEncoder)
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Internal server error'})
        }

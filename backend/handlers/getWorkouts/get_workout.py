import boto3
import json
from decimal import Decimal
import random
import os

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['WORKOUT_TABLE'])
    region_name = os.environ['REGION_NAME']
    
    # Get query parameters from the event
    params = event.get('queryStringParameters', {})
    muscle_group = params.get('muscleGroup', '').lower()
    weighted = params.get('weighted', '').lower()  # 'weighted' or 'unweighted'
    duration = int(params.get('duration', 30))  # Total workout duration in minutes
    
    # Calculate number of exercises needed (5 minutes per exercise)
    num_exercises_needed = duration // 5
    
    try:
        # Query using the GSI
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
        
        # Randomly select the required number of exercises
        selected_exercises = random.sample(
            all_exercises,
            min(num_exercises_needed, len(all_exercises))
        )
        
        # Calculate actual workout duration
        actual_duration = len(selected_exercises) * 5
        
        workout_plan = {
            'requested_duration': duration,
            'actual_duration': actual_duration,
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
            'body': json.dumps(workout_plan, default=str)
        }
        
    except ValueError as ve:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No workouts found for select criteria'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# def lambda_handler(event, context):
#     return {
#         'statusCode': 200,
#         'body': 'Hello from Lambda!'
#     }

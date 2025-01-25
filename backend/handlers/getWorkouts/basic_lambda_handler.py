import boto3
import random

def lambda_handler(event, context):
    # Initialize DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Workouts')
    
    # Extract query parameters
    muscle_group = event['queryStringParameters']['muscle_group']
    
    # Query DynamoDB
    response = table.scan(
        FilterExpression="MuscleGroup = :group",
        ExpressionAttributeValues={':group': muscle_group}
    )
    workouts = response.get('Items', [])
    
    try:
        if workouts:
            return {
                'statusCode': 200,
                'body': random.choice(workouts)
            }
        
    except Exception as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return {
                'statusCode': 404,
                'body': 'No workouts found for the selected criteria.'
            }
        else:
            return {
                'statusCode': 500,
                'body': f"An error occured: {str(e)}."
            }
 


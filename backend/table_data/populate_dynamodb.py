import boto3
import json
import os

def populate_dynamodb(table_name, region_name, file_name):
    # Initialize DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)
    
    #Get the absolute path of JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'workout_data.json')
    
    # Read data from JSON file
    with open(json_path, 'r') as json_file:
        workouts = json.load(json_file)
    # Insert data into DynamoDB for table
        for workout in workouts:
            try: 
                table.put_item(
                    Item= {
                        'MuscleGroup': workout['MuscleGroup'],
                        'ExerciseId': workout['ExerciseId'],
                        'ExerciseName': workout['ExerciseName'],
                        'Weighted': workout['Weighted'],
                        'Duration': workout['Duration'],
                        'Sets' : workout['Sets'],
                        'Reps' : workout['Reps'],
                    })
                print(f"Added workout: {workout['ExerciseName']}")
            except Exception as e:
                print(f"Error adding workout: {workout['ExerciseName']}: {str(e)}")
            
        print("Population complete!")


if __name__ == "__main__":
    table_name = 'WorkoutsTable'
    region_name = 'us-east-1'
    file_name = './backend/table_data/workout_data.json'
    populate_dynamodb(table_name, region_name, file_name)

# When ready run script from cd FitLogic_Workout_Randomizer/backend/table_data
# run command python populate_dynamodb.py

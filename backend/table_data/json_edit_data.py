import json

# # Use the relative path to the JSON file
# with open('./backend/table_data/workout_data.json', 'r') as file:
#     data = json.load(file)

# # Update all Duration values to 5
# for workout in data:
#     workout['Duration'] = 5

# # Write back to the file
# with open('./backend/table_data/workout_data.json', 'w') as file:
#     json.dump(data, file, indent=4)

# Original data
# original_data = [ 

# ]

# # Function to reformat the data
# def reformat_data(data):
#     reformatted_data = []
#     for index, exercise in enumerate(data):
#         reformatted_entry = {
#             "MuscleGroup": exercise["MuscleGroup"],
#             "ExerciseId": f"{exercise['WorkoutName'].replace(' ', '-').lower()}-{str(index + 1).zfill(3)}",
#             "ExerciseName": exercise["WorkoutName"],
#             "Weighted": "weighted" if exercise["Weighted"] != "none" else "unweighted",
#             "Duration": exercise["Duration"],
#             "Sets": 4,  # Default value for sets
#             "Reps": "10-12"  # Default value for reps
#         }
#         reformatted_data.append(reformatted_entry)
#     return reformatted_data

# # Reformat the data
# new_data = reformat_data(original_data)

# # Convert to JSON for better readability or exporting
# formatted_json = json.dumps(new_data, indent=4)

# # Print the reformatted data
# print(formatted_json)

# # Save to a file (optional)
# with open("reformatted_data.json", "w") as outfile:
#     outfile.write(formatted_json)


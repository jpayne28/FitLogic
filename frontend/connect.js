document.addEventListener('DOMContentLoaded', function() {
    const workoutForm = document.getElementById('workoutForm');
    const loadingDiv = document.getElementById('loading');
    const workoutList = document.getElementById('workout-list');
    
    workoutForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form values
        const muscleGroup = document.getElementById('muscleGroup').value;
        const weighted = document.getElementById('weighted').value;
        const duration = parseInt(document.getElementById('duration').value, 10);
        
        try {
            loadingDiv.style.display = 'block';
            workoutList.innerHTML = ''; // Clear previous results
            
            // Construct URL with query parameters directly
            const apiUrl = `${config.apiUrl}/workouts?muscleGroup=${encodeURIComponent(muscleGroup)}&weighted=${encodeURIComponent(weighted)}&duration=${duration}`;
            
            console.log('Requesting URL:', apiUrl); // Debug log
            
            const response = await fetch(apiUrl);
            const data = await response.json();
            
            if (response.ok) {
                // Check if we have exercises in the response
                if (data.exercises && data.exercises.length > 0) {
                    const workoutDiv = document.createElement('div');
                    workoutDiv.className = 'workout-summary';
                    workoutDiv.innerHTML = `
                        <h3>Workout Summary</h3>
                        <p>Duration: ${data.actual_duration} minutes</p>
                        <p>Muscle Group: ${data.muscle_group}</p>
                        <p>Type: ${data.weighted}</p>
                        <h4>Exercises:</h4>
                    `;
                    
                    const exercisesList = document.createElement('div');
                    exercisesList.className = 'exercises-list';
                    
                    data.exercises.forEach((exercise, index) => {
                        const exerciseDiv = document.createElement('div');
                        exerciseDiv.className = 'exercise-item';
                        exerciseDiv.innerHTML = `
                            <h4>${index + 1}. ${exercise.ExerciseName}</h4>
                            <p>Sets: ${exercise.Sets}</p>
                            <p>Reps: ${exercise.Reps}</p>
                        `;
                        exercisesList.appendChild(exerciseDiv);
                    });
                    
                    workoutDiv.appendChild(exercisesList);
                    workoutList.appendChild(workoutDiv);
                } else {
                    workoutList.innerHTML = '<p class="no-results">No exercises found for the selected criteria.</p>';
                }
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            console.error('Error:', error);
            workoutList.innerHTML = `<p class="error">Error loading workouts: ${error.message}</p>`;
        } finally {
            loadingDiv.style.display = 'none';
        }
    });
});

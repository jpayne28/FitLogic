# FitLogic
FitLogic is an application that generates new workout routines for individuals that are new to fitness or tired of their workout routine. This is a serverless application built with AWS services. For more info please navigate to the README.

### Description
FitLogic is a workout randmonizer app that allows individuals to create new workout routines based on muscle group, duration of workout, and their preference of weights or none weighted exercises. This app is the minimum viable product MVP. Future implementation will allow user to generate new workout routines, save completed exercises, and keep track of progress throughout their fitness journey.

### Features
- Generate workouts for different muscle groups
- Choose between weighted and bodyweight exercises
- Random exercise selection

### Prerequisites:
- AWS SAM CLI
- Python 3.9
- AWS Account and configurations

### Technologies Used
Fronted:
- Route 53
- CloudFront
- Amazon S3
- HTML/CSS/JavaScript

Backend:
- AWS SAM
- API Gateway
- AWS Lambda
- Amazon DynamoDB

### API Endpoint
- GET/workouts
- Query parameters:
-   muscleGroup: string
-   weighted: string
-   duration: number

### Infrastructure
- API Gateway RESTful endpoint
- AWS Lambda workout generator
- Amazon DynamoDB exercise storage

### Architecture Diagram
Located in docs file

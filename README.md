# Health Tracker Application

## Project Description
The Health Tracking Application is a **full-stack web application** built with Django that provides a user interface for logging workouts, meals, and setting fitness goals. It includes both traditional Django template rendering and a REST API for data access.

**Architecture:**
- **Frontend**: Django templates with Bootstrap 5
- **Backend**: Django with REST API
- **Database**: PostgreSQL for production (SQLite for development)
- **Deployment**: Single Render service

The application is configured for deployment on [Render](https://render.com/) using a `render.yaml` file, allowing seamless hosting of the web service in the cloud.
🔗 **Live Demo**: [https://healthtracker-is4l.onrender.com](https://healthtracker-is4l.onrender.com)

## Architecture
- **Frontend**: Django templates with server-side rendering
- **Backend**: Django REST API serving JSON data
- **Database**: PostgreSQL for data persistence
- **Deployment**: Single service serving both templates and API endpoints

**How it works:**
- Django views render HTML templates
- REST API endpoints provide JSON data
- Single deployment handles both interface and API

## Features
- **User Authentication**: Secure user registration and login
- **Dashboard**: Real-time health metrics and progress tracking via API
- **Activity Tracking**: Log workouts and calories burned
- **Nutrition Logging**: Track meals with detailed nutritional information
- **Goal Setting**: Define fitness objectives and monitor progress
- **REST API**: Full CRUD operations via JSON API endpoints
- **Frontend**: Django templates with Bootstrap 5
- **Real-time Updates**: API-driven data updates without page refreshes

## Technology Stack
- **Backend**: Python with Django 4.2.17 + Django REST Framework
- **Frontend**: Django templates with Bootstrap 5
- **Database**: PostgreSQL for production (SQLite for development)
- **API**: Django REST Framework with session authentication
- **Containerization**: Docker for application deployment
- **Deployment**: Render using `render.yaml`
- **Development Tools**: Flake8 for code linting

## Usage

1. **Register**: Create a new account or login with existing credentials
2. **Set Goals**: Define your health objectives in the Goals section
3. **Dashboard**: View your daily health metrics and recent activities
4. **Log Activities**: Record your workouts or other physical activities
5. **Track Nutrition**: Log your meals and monitor nutritional intake

## API Endpoints

The application provides REST API endpoints for:
- User management (authentication)
- Activity logging and management
- Nutrition tracking and management
- Goal setting and management

## Deployment

The application is configured for deployment on Render with Docker. The `render.yaml` file contains the deployment configuration for the web service with PostgreSQL database.

## Data Models

### UserGoal
- Goal types: Weight Loss, Weight Gain, Muscle Gain, Maintain Weight, Increase Fitness, Improve Endurance
- Targets: Weight, calories to burn/consume, protein intake, activity days per week

### Activity
- Activity type, duration, distance, calories burned, date, notes

### NutritionEntry
- Food name, calories, macronutrients (protein, carbs, fat), quantity, meal type, date

## Goals
- Provide users with an intuitive platform for tracking and managing their health metrics
- Enable goal setting and progress monitoring
- Support healthy habit formation through consistent logging and tracking

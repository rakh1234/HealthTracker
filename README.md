# Health Tracker Application  

## Project Description  
The Health Tracking Application is a full-stack web application, designed to help users monitor and manage their health and wellness. This application utilizes a REST API, providing a user-friendly interface for tracking various health metrics, such as physical activity and nutrition. It is containerized using Docker for easy deployment and scalability. 

The application is configured for deployment on [Render](https://render.com/) using a `render.yaml` file, allowing seamless hosting of the web service in the cloud.  
🔗 **Live Demo**: [https://healthtracker-is4l.onrender.com](https://healthtracker-is4l.onrender.com)

## Features  
- **User Authentication**: Secure user registration and login functionality.  
- **Dashboard**: A personalized dashboard displaying health metrics and insights.  
- **Activity Tracking**: Log workouts, steps, and other physical activities.  
- **Nutrition Logging**: Input daily food intake and nutritional information.  
- **Smart Analytics**: AI-powered insights with machine learning recommendations.
- **Goal Setting**: Define fitness objectives and track progress with personalized targets.
- **Advanced Visualizations**: Interactive charts showing trends and progress over time.
- **Personalized Recommendations**: ML-driven suggestions based on your goals and patterns.    

## Technology Stack  
- **Frontend**: Django Templates with Bootstrap 5, HTML, CSS, and JavaScript.
- **Backend**: Python with Django and Django REST Framework for server-side logic and API development.  
- **Database**: PostgreSQL for data storage (SQLite for development).
- **Data Analysis**: Pandas, NumPy, Matplotlib, Scikit-learn for analytics and ML.
- **Containerization**: Docker for application deployment and management. 
- **API Integration**: RESTful API endpoints for seamless interaction between frontend and backend.   
- **Deployment**: Render using `render.yaml`

## Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd HealthTracker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   cd app
   python manage.py migrate
   ```

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**:
   Open your browser and go to `http://127.0.0.1:8000`

## Usage

1. **Register**: Create a new account or login with existing credentials.
2. **Set Goals**: Define your health objectives (weight loss, muscle gain, fitness improvement, etc.).
3. **Dashboard**: View your daily health metrics and AI-powered insights.
4. **Log Activities**: Record your workouts, runs, or other physical activities.
5. **Track Nutrition**: Log your meals and monitor nutritional intake.
6. **View Analytics**: Access advanced analytics with ML-driven recommendations and trend analysis.

## AI & Machine Learning Features

### Smart Recommendations
- **Goal-Based Insights**: Personalized recommendations based on your fitness objectives
- **Pattern Recognition**: ML algorithms identify trends in your activity and nutrition data
- **Progress Tracking**: Automated analysis of your progress toward goals

### Advanced Analytics
- **Trend Analysis**: Linear regression models to predict future performance
- **Visual Charts**: Interactive matplotlib-generated charts showing progress over time
- **Weekly Statistics**: Comprehensive weekly breakdowns of health metrics
- **Goal Progress Visualization**: Charts showing progress ratios against targets

### Data-Driven Insights
- **Calorie Balance Analysis**: Compare intake vs expenditure
- **Activity Pattern Recognition**: Identify optimal times and frequencies for exercise
- **Nutrition Optimization**: Recommendations for macronutrient balance
- **Performance Prediction**: Forecast future health metrics based on current trends

## API Endpoints

The application provides REST API endpoints for:
- User management
- Activity logging
- Nutrition tracking

## Deployment

The application is configured for deployment on Render with Docker. The `render.yaml` file contains the deployment configuration.
  
## Goals  
- Empower users to take control of their health by providing an intuitive platform for tracking and managing their wellness.  
- Promote healthier habits through progress tracking.

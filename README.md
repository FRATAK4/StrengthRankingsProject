# StrengthRankings

A comprehensive Django-based fitness tracking web application that enables users to create communities, track workouts, manage training plans, and compete in exercise rankings.

![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

## 🎯 Overview

StrengthRankings is a social fitness platform designed to help fitness enthusiasts track their progress, share training plans, and compete with friends in various exercise rankings. Built with Django's robust framework, it emphasizes clean architecture, security, and user experience.

## 📸 Screenshots

[Paste main dashboard screenshot here]

[Paste groups or friends page screenshot here]

[Paste training plan screenshot here]

## ✨ Features

### Current Implementation

- **🔐 User Authentication & Profiles**
  - Secure registration and login system
  - Customizable user profiles with images
  - Profile statistics and achievement tracking

- **👥 Social Features**
  - Bidirectional friendship system
  - Friend requests with custom messages
  - Blocking/unblocking functionality
  - User search and discovery

- **🏋️ Training Plans**
  - Create and manage custom workout plans
  - Public/private plan settings
  - Plan templates and duplication
  - Exercise organization with sets/reps tracking

- **👥 Groups Management**
  - Create and join fitness communities
  - Role-based permissions (Owner, Admin, Member)
  - Group join requests with approval workflow
  - Member management and blocking

- **🔔 Notification System**
  - Real-time notifications for user interactions
  - Friend request notifications
  - Group activity alerts
  - Unread notification counter

- **🎨 Modern UI/UX**
  - Responsive dark theme with cyan accents
  - Bootstrap 5 integration
  - Interactive components with CoreUI
  - Mobile-friendly design

### In Development

- 📊 Workout performance tracking and analytics
- 🏆 Group exercise rankings and leaderboards
- ⭐ Training plan marketplace with ratings
- 📈 Progress visualization and statistics
- 🔌 GraphQL API

## 🛠️ Tech Stack

- **Backend:** Python 3.11, Django 4.2
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Type Checking:** mypy
- **Version Control:** Git, GitHub

## 📋 Prerequisites

- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/FRATAK4/StrengthRankings.git
cd StrengthRankings
```

### 2. Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser

```bash
python manage.py createsuperuser
```

### 6. Collect static files

```bash
python manage.py collectstatic
```

### 7. Run development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see the application.

## 🏗️ Project Structure

```
StrengthRankingsProject/
├── src/
│   ├── accounts/            # User authentication and profiles
│   ├── analytics/           # Data analysis and statistics
│   ├── common/              # Shared components and templates
│   ├── core/                # Core settings and configuration
│   ├── exercises/           # Exercise definitions and management
│   ├── friendships/         # Friend system and relationships
│   ├── groups/              # Group management and permissions
│   ├── notifications/       # Notification system
│   ├── training_plans/      # Training plans management
│   └── workout_performance/ # Workout filling
```

## 🔧 Development

### Code Style

The project follows PEP 8 guidelines and uses:
- Type hints for better code documentation
- Class-based views for consistency
- Django best practices for security

### Database Schema

Key models include:
- `User` - Extended Django user model
- `Profile` - User profile information
- `Friendship` - Bidirectional friend relationships
- `Group` - Fitness communities
- `GroupMembership` - User-group relationships with roles
- `TrainingPlan` - Workout plan templates
- `Workout` - Individual workout sessions
- `Exercise` - Exercise definitions
- `Notification` - User notifications

## 👤 Author

**Michał Fedczyna**

- GitHub: [@FRATAK4](https://github.com/FRATAK4)
- Email: fratak4@gmail.com

---

**Note:** This project is under active development. Features and documentation may change.
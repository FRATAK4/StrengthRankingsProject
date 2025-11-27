# StrengthRankings

A comprehensive Django-based fitness tracking web application that enables users to create communities, track workouts, manage training plans, and compete in exercise rankings.

![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

## 🎯 Overview

StrengthRankings is a social fitness platform designed to help fitness enthusiasts track their progress, share training plans, and compete with friends in various exercise rankings. Built with Django's robust framework, it emphasizes clean architecture, security, and user experience.

## 📸 Screenshots

<table border="0" style="border: none;">
  <tr>
    <td align="center" valign="top" width="50%" style="border: none; padding: 5px;">
      <img src="https://github.com/user-attachments/assets/84f6c822-e0fc-4abc-9918-9d4b00855a8a" width="100%">
    </td>
    <td align="center" valign="top" width="50%" style="border: none; padding: 5px;">
      <img src="https://github.com/user-attachments/assets/791aa679-eba8-4a8f-afe1-7645f3696464" width="100%">
    </td>
  </tr>
  <tr>
    <td align="center" valign="top" width="50%" style="border: none; padding: 5px;">
      <img src="https://github.com/user-attachments/assets/54cb5c73-1acb-468f-a3bb-13013219a8f2" width="100%">
    </td>
    <td align="center" valign="top" width="50%" style="border: none; padding: 5px;">
      <img src="https://github.com/user-attachments/assets/f0fa3e93-9b37-4af2-9f4e-746ad9fb9464" width="100%">
    </td>
  </tr>
</table>

*Modern dark-themed interface with comprehensive fitness tracking features*

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

## 🛠️ Tech Stack

- **Backend:** Python 3.13, Django 4.2
- **Database:** PostgreSQL 16
- **Containerization:** Docker, Docker Compose
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Type Checking:** mypy
- **Version Control:** Git, GitHub

## 📋 Prerequisites

- Docker
- Docker Compose

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/FRATAK4/StrengthRankings.git
cd StrengthRankings
```

### 2. Build and run with Docker

```bash
docker-compose up --build
```

### 3. Create superuser (in a new terminal)

```bash
docker-compose exec app python manage.py createsuperuser
```

### 4. Access the application

Visit `http://localhost:8000` to see the application.

## 🗂️ Project Structure

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
│   ├── workout_performance/ # Workout tracking
│   ├── .env                 # Environment variables
│   └── manage.py            # Django management script
├── .gitignore
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── Dockerfile               # Docker image configuration
├── docker-compose.yaml      # Multi-container configuration
├── requirements.txt         # Python dependencies
└── README.md
```

## 👤 Author

**Michał Fedczyna**

- GitHub: [@FRATAK4](https://github.com/FRATAK4)
- Email: fratak4@gmail.com

---

**Note:** This project is under active development. Features and documentation may change.
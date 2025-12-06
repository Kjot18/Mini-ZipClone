# Procurement Workflow Automation Platform

A mini-Zip clone for managing procurement workflows with purchase request approvals.

## Tech Stack

- **Backend**: Python (FastAPI) with Strawberry GraphQL
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL
- **Containerization**: Docker

## Features

- Purchase request submission workflow
- Multi-stage approval process
- Admin dashboard for request management
- User roles and permissions
- GraphQL API for all operations

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local backend development)

### Running with Docker

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- GraphQL Playground: http://localhost:8000/graphql

### Default Users

The system automatically creates these default users on first startup:

- **Admin**: `admin` / `admin123` (Role: Admin)
- **Manager**: `manager` / `manager123` (Role: Manager)
- **User**: `user` / `user123` (Role: User)

You can also register new users through the registration page.

### Using the Application

1. **Register/Login**: Start by registering a new account or logging in with default credentials
2. **Create Purchase Request**: Navigate to "New Request" to submit a purchase request
3. **View Requests**: Check your dashboard to see all your submitted requests
4. **Admin Dashboard**: Admins and managers can approve/deny requests from the Admin page

### Development Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## Project Structure

```
.
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── docker-compose.yml
└── README.md
```


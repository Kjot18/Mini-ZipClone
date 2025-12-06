# Quick Start Guide

## Quick Setup (Docker)

1. **Start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Wait for services to start** (this may take a few minutes on first run)

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - GraphQL Playground: http://localhost:8000/graphql

## First Steps

1. **Login with default credentials:**
   - Username: `admin` / Password: `admin123` (Admin role)
   - Username: `manager` / Password: `manager123` (Manager role)
   - Username: `user` / Password: `user123` (User role)

2. **Or register a new account** at http://localhost:3000/register

3. **Create a purchase request:**
   - Click "New Request" in the navigation
   - Fill in the form and submit

4. **Approve requests (Admin/Manager):**
   - Go to "Admin" page
   - Click "Review" on pending requests
   - Approve or deny with optional comments

## Testing the GraphQL API

Visit http://localhost:8000/graphql to use the GraphQL Playground.

### Example Query:
```graphql
query {
  purchaseRequests {
    id
    title
    amount
    status
    requester {
      username
    }
  }
}
```

### Example Mutation:
```graphql
mutation {
  login(input: {
    username: "user"
    password: "user123"
  }) {
    token
    user {
      username
      role
    }
  }
}
```

## Troubleshooting

### Database connection issues
- Ensure PostgreSQL container is running: `docker-compose ps`
- Check database logs: `docker-compose logs db`

### Frontend not connecting to backend
- Verify backend is running: http://localhost:8000/health
- Check CORS settings in `backend/app/config.py`

### Port conflicts
- Change ports in `docker-compose.yml` if 3000, 8000, or 5432 are in use

## Development Mode

### Backend only:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend only:
```bash
cd frontend
npm install
npm start
```

Note: For local development, you'll need a PostgreSQL database running separately.


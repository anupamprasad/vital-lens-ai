# User Dashboard Feature

This document explains the new user directory/dashboard that allows authenticated users
(to be treated as admin in future) to view a list of registered accounts. It is
intended primarily for debugging and administrative purposes.

## Backend

- **Endpoint**: `GET /api/v1/users/`
  - Requires JWT authentication (`Authorization: Bearer <token>`)
  - Currently open to any logged-in user for demo; an `is_admin` flag is available
    on the user model for future restrictions.
  - Returns an array of objects containing the following fields:
    ```json
    [
      {
        "id": 1,
        "email": "alice@example.com",
        "username": "alice",
        "first_name": null,
        "last_name": null,
        "is_active": true,
        "is_verified": false,
        "is_admin": false,
        "created_at": "2026-02-28T14:12:34.123456"
      },
      ...
    ]
    ```

- **Database migration**: column `is_admin BOOLEAN DEFAULT FALSE` added to
  `users` table in migration `002_add_is_admin.py`.  
  Models updated accordingly.

## Frontend

### Pages
- **`UsersPage.jsx`**: new React component under `src/pages`.
  - Fetches list of users on mount via `usersService.listUsers()`.
  - Displays results in a responsive table with columns: ID, Username, Email,
    Admin?, Created.
  - Shows loading spinner and error message when appropriate.

### Navigation
- Link added to the main navigation menu (`Navigation.jsx`) labelled "👥 Users".
- Dashboard action button also includes "👥 User List" for quick access.
- Protected by authentication in `App.jsx` route configuration (`/users` path).

### Service
- `usersService` (in `services/api.js`) now includes:
  ```js
  listUsers: () => api.get('/api/v1/users/'),
  ```
  along with updated profile endpoints.

## Testing & Verification
- After building the backend and running migrations, hitting `/api/v1/users/`
  with a valid token returns the current user list. Example (curl):
  ```bash
  TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
    -H 'Content-Type: application/json' \
    -d '{"email":"test@example.com","password":"password"}' | jq -r .access_token)
  curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/users/ | jq
  ```
- Visiting `http://localhost:5173/users` in the browser shows the table.
- Navigation links and dashboard button work as expected.

## Notes
- The table is read-only; editing/deleting users is not supported yet.
- The feature is intentionally simple; real admin dashboards would include 
  pagination, search, role management, and audit logging.
- `is_admin` column was added to prepare for role-based access control.

## Next Steps
1. Restrict `/users/` endpoint to admin accounts by enabling the commented
   check in `api/users.py` when an admin user exists.
2. Add ability to promote/demote users via the dashboard.
3. Include pagination, filtering, and export (CSV) functionality.
4. Create backend unit tests for the new endpoint and frontend component tests.

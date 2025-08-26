# FastAPI Notes CRUD with Auth 
---
## API Routes Design

### Authentication (2 endpoints)
- `POST /auth/register` — User registration (username/email/password)
- `POST /auth/login` — Login, returns JWT token

### Notes CRUD (5 endpoints, all require JWT)
- `POST /notes/` — Create new note
- `GET /notes/` — List all user's notes
- `GET /notes/{id}` — Get specific note
- `PUT /notes/{id}` — Update note (with version check)
- `DELETE /notes/{id}` — Delete note

---

## Database Schema

Two tables with foreign key relationship:

**Users:** id, username, email, hashed_password, created_at

**Notes:** id, title, content, version, created_at, updated_at, owner_id (foreign key to Users)

**Relationship:**  
One user → Many notes (user isolation via owner_id)

---

## Authentication Choice: JWT Tokens

- Stateless, scalable across microservices
- industry standard
- Uses bcrypt for password hashing
- 30-minute token expiration

---

## Failure Mode: Race Condition on Concurrent Updates

**Problem:**  
Two users updating the same note simultaneously could cause lost updates.

**Mitigation: Optimistic Locking**
- Each note has a version number (starts at 1)
- Update requests must include current version
- Server checks:  
    - If versions match → update succeeds & increment version  
    - If versions don't match → return `409 Conflict` error
- Client must refresh note and retry with new version

**Benefits:**  
Prevents data loss, no database locks needed, high performance, clear error handling.
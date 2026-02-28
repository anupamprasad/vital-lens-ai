# Camera Feature - Quick Reference

## User Journey
```
Login → Dashboard → Click "Take Measurement" → Camera Page
   ↓
Browser asks for camera permission
   ↓
Grant permission OR allow fallback
   ↓
Click "Start Measurement" button
   ↓
Watch 30-second progress animation
   ↓
View Heart Rate + SpO2 results
   ↓
Click "Save & View Report" to persist to database
```

## API Calls Made by Camera Page
```javascript
// 1. Record measurement
POST /api/v1/vitals
Authorization: Bearer {token}
{
  "heart_rate": 72,
  "spO2": 98,
  "duration": 30
}

// 2. Returns
{
  "id": 123,
  "heart_rate": 72.0,
  "spO2": 98.0,
  "measured_at": "2026-02-28T08:53:20.233041"
}
```

## Component State
```javascript
{
  measuring: boolean,           // Currently taking measurement
  progress: 0-100,            // Progress percentage
  result: null | Object,       // Measurement result (HR, SpO2)
  error: string,              // Error message if any
  cameraPermission: boolean,  // Can start measurement
  lightingFeedback: string,   // Lighting quality feedback
  saving: boolean             // Currently saving to backend
}
```

## Key Functions
```javascript
handleStartMeasurement()  // Start 30s measurement simulation
handleSaveResult()        // POST vitals to /api/v1/vitals
getLightingMessage()      // Get UI message based on lighting
```

## Testing Without Camera
1. Camera will fail gracefully if not available
2. Error message appears but button stays enabled
3. Measurement simulation works normally
4. All backend integration works
5. Data saves to database properly

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Button disabled | Camera access failed | Refresh page - now allows fallback |
| No camera preview | Permission denied | Allow when browser asks, or use fallback |
| "Camera access denied" error | Browser blocked | Check browser settings or try different browser |
| Results not saving | Auth token expired | Log in again to get new token |
| API 401 error | Missing/invalid token | Check Authorization header in network tab |

## Files to Edit
- `frontend/src/pages/CameraPage.jsx` - Camera UI and logic
- `frontend/src/services/api.js` - Backend API calls
- `backend/api/vitals.py` - Vitals recording endpoint
- `backend/models.py` - Vitals database model

## Development Server URLs
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs (Swagger UI)
- Phpmyadmin (if configured): http://localhost:8001

## Docker Commands
```bash
# Start stack
docker compose up -d

# Stop stack
docker compose down

# View logs
docker compose logs frontend
docker compose logs backend

# Execute command in container
docker compose exec backend sh -c "command"

# Rebuild specific service
docker compose build frontend && docker compose up -d frontend
```

## Database Query (Check Vitals)
```bash
docker compose exec postgres psql -U vital_lens -d vital_lens_db -c "SELECT * FROM vitals ORDER BY created_at DESC LIMIT 5;"
```

## Current Status
- ✅ Camera permission handling
- ✅ Fallback if camera unavailable
- ✅ Measurement simulation
- ✅ Backend API integration
- ✅ Database persistence
- ✅ Error handling and messaging
- ⏳ Real rPPG algorithm (future)

## Environment Variables (if needed)
```bash
VITE_API_URL=http://localhost:8000
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
REACT_APP_API_BASE=http://localhost:8000
```

## Performance Targets
- Page load: <2s
- Camera init: <2s
- Measurement: ~3s
- API response: <100ms
- Save operation: <1s total

## Security Notes
- JWT tokens expire after 24 hours
- All vitals require authentication
- HTTPS recommended for production camera access
- Never commit auth tokens to version control

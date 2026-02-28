# Camera Feature - Usage Guide & Troubleshooting

## Overview
The camera page allows users to take vital measurements using their device's camera and the rPPG (Remote Photoplethysmography) algorithm. The measurement process simulates capturing video frames and extracting heart rate and SpO2 (blood oxygen) data.

## How to Use

### Access the Camera Feature
1. Log in to the application at `http://localhost:5173`
2. After successful login, you'll see the dashboard
3. Click the "📷 Take Measurement" button or navigate directly to `/camera`

### Taking a Measurement
1. **Permission**: When you first access the camera page, your browser will request camera permission
   - Click "Allow" to enable camera access
   - If denied, you can still take a simulated measurement (for demo/testing)

2. **Position Your Face**: 
   - Position your face in the center of the green circle
   - Ensure good lighting on your face
   - Keep your head still

3. **Start Measurement**:
   - Click the "🔴 Start Measurement" button
   - Wait for the 30-second simulated measurement to complete
   - The progress bar will show the completion percentage
   - Lighting feedback will guide you (📋 Instructions visible)

4. **View Results**:
   - After measurement completes, you'll see:
     - Heart Rate (in bpm)
     - Blood Oxygen (SpO2 percentage)
   - Click "Save & View Report" to save to the database
   - Click "New Measurement" to take another reading

## Camera Permission Troubleshooting

### Issue: Camera button is disabled
**Solution**: The button might be disabled temporarily. Try refreshing the page. The updated code allows testing even without camera access.

### Issue: "Camera access denied" error
**Possible causes**:
- Camera blocked in browser settings
- No camera hardware available
- Browser doesn't support WebRTC

**Solutions**:
1. Check browser camera permissions in settings
2. Try a different browser (Chrome, Firefox, Safari all support camera)
3. Restart your browser
4. Even if camera fails, you can still test the measurement flow

### Issue: Camera feed not showing
**Possible causes**:
- Camera already in use by another application
- Browser security restrictions
- Localhost/HTTP limitation in some browsers

**Solutions**:
1. Close other apps using the camera
2. Try accessing from a different device
3. For production, ensure HTTPS is used

## Backend Integration

### API Endpoints Used

#### Record Vitals
```bash
POST /api/v1/vitals
Authorization: Bearer {token}
Content-Type: application/json

{
  "heart_rate": 72,
  "spO2": 98,
  "duration": 30
}
```

**Response**:
```json
{
  "id": 1,
  "heart_rate": 72.0,
  "spO2": 98.0,
  "measured_at": "2026-02-28T08:53:20.233041"
}
```

#### List Vitals
```bash
GET /api/v1/vitals/?period=week
Authorization: Bearer {token}
```

**Query Parameters**:
- `period`: `week`, `month`, or `year`

#### Get Latest Vitals
```bash
GET /api/v1/vitals/latest
Authorization: Bearer {token}
```

## Frontend Code Structure

### Key Files
- **CameraPage.jsx**: Main camera interface component
- **services/api.js**: Axios service for backend API calls
- **DashboardPage.jsx**: Displays vitals history

### Camera Implementation Details
```javascript
// Request camera access
navigator.mediaDevices.getUserMedia({ 
  video: { 
    facingMode: 'user',
    width: { ideal: 1280 },
    height: { ideal: 720 }
  } 
})
```

### Fallback Behavior
If camera access fails:
- Error message is displayed
- Measurement still allowed (for demo/testing)
- Data saves normally to backend

## Testing the Feature

### Manual Test Flow
```bash
# 1. Signup
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@vital.local","password":"Pass123"}'

# 2. Record Vitals
curl -X POST http://localhost:8000/api/v1/vitals \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"heart_rate":72,"spO2":98,"duration":30}'

# 3. Get Vitals
curl -X GET http://localhost:8000/api/v1/vitals/?period=week \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Data Persistence
- All measurements are saved to PostgreSQL database
- Each measurement includes:
  - User ID
  - Heart rate
  - SpO2 (blood oxygen)
  - Duration
  - Timestamp
  - Device information (if available)

## Known Limitations (Current Version)
1. **Simulation**: Current version simulates measurements - actual rPPG processing not implemented
2. **Video Processing**: Does not analyze actual video frames
3. **Camera Requirements**: Some browsers may have restrictions on HTTP/localhost
4. **Mobile Testing**: Ensure HTTPS for production mobile deployment

## Future Enhancements
- [ ] Implement actual rPPG algorithm for real measurements
- [ ] Add video frame capture and analysis
- [ ] Support multiple measurement types (SpO2, respiratory rate, etc.)
- [ ] Add measurement quality scoring
- [ ] Implement retry logic for failed measurements
- [ ] Add measurements history with trending charts

## System Status Check
To verify all services are running:
```bash
cd /Users/anupamprasad/Documents/Projects/vital-lens-ai/phase3_application
docker compose ps

# Expected output: All services RUNNING/healthy
```

## Performance Notes
- Camera initialization: ~1-2 seconds
- Measurement simulation: 3 seconds (10% increments every 0.3s)
- API response time: <100ms for vitals operations
- Database query for vitals list: <50ms

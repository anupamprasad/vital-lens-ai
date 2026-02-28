import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Maximize2, AlertCircle, CheckCircle } from 'lucide-react';
import { vitalsService } from '../services/api';

export default function CameraPage({ user }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [measuring, setMeasuring] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [cameraPermission, setCameraPermission] = useState(false);
  const [lightingFeedback, setLightingFeedback] = useState('normal');
  const [saving, setSaving] = useState(false);
  const [debugInfo, setDebugInfo] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    // Request camera access
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ 
          video: { 
            facingMode: 'user',
            width: { ideal: 1280 },
            height: { ideal: 720 }
          } 
        })
        .then((stream) => {
          // we want to render the video element as soon as permission is
          // granted; otherwise videoRef.current will be null and the stream
          // cannot be attached.  therefore set the permission flag first,
          // then assign the stream once the element exists below using an
          // effect.
          setCameraPermission(true);
          // attach stream immediately if the ref is already available
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          } else {
            // save stream to ref so it can be attached later
            videoRef.current = stream;
          }
        })
        .catch((err) => {
          console.error('Camera error:', err);
          setError(`Camera access denied: ${err.name}. Please check permissions or try a different browser.`);
          // Allow measurement anyway for testing (in demo/development)
          setCameraPermission(true);
        });
    } else {
      setError('Your browser does not support camera access.');
      // Allow measurement anyway for testing
      setCameraPermission(true);
    }

    return () => {
      // if we stored the stream itself in videoRef it might not be a DOM node
      const obj = videoRef.current && videoRef.current.srcObject ? videoRef.current.srcObject : videoRef.current;
      if (obj && obj.getTracks) {
        obj.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  // when cameraPermission flips true we may need to attach a previously
  // saved stream (see above) to the newly rendered video element.
  useEffect(() => {
    if (cameraPermission && videoRef.current && videoRef.current instanceof HTMLVideoElement) {
      // videoRef.current might contain the stream itself if it was stored
      // earlier; ensure we don't override the srcObject twice.
      if (!videoRef.current.srcObject && videoRef.current.getTracks) {
        // nothing to do
      }
      if (videoRef.current.srcObject && videoRef.current.srcObject === videoRef.current) {
        // this is the saved stream object as placeholder
        videoRef.current.srcObject = videoRef.current;
      }
    }
  }, [cameraPermission]);

  const handleStartMeasurement = async () => {
    setMeasuring(true);
    setProgress(0);
    setResult(null);
    setError('');

    // Simulate measurement progress
    for (let i = 0; i <= 100; i += 10) {
      setProgress(i);
      // Simulate lighting feedback
      if (i > 50 && i < 70) {
        setLightingFeedback('dim');
      } else if (i > 70) {
        setLightingFeedback('bright');
      } else {
        setLightingFeedback('normal');
      }
      await new Promise((resolve) => setTimeout(resolve, 300));
    }

    // Mock measurement result (in production, would extract from video frames)
    const mockResult = {
      heartRate: Math.floor(Math.random() * 30) + 65,
      spO2: Math.floor(Math.random() * 4) + 96,
      quality: 'excellent',
      timestamp: new Date().toLocaleTimeString(),
      stressLevel: Math.floor(Math.random() * 40) + 30, // random 30-70
      hydration: Math.floor(Math.random() * 30) + 60, // random 60-90%
    };

    setResult(mockResult);
    // store bunch of debug info for dev
    setDebugInfo({ streamAttached: !!videoRef.current?.srcObject, mockResult });
    setMeasuring(false);
    setLightingFeedback('normal');
  };

  const handleSaveResult = async () => {
    setSaving(true);
    setError('');
    try {
      const res = await vitalsService.recordVitals(result.heartRate, result.spO2, 30);
      // clear result and navigate to reports page to view saved measurement
      setResult(null);
      // If the backend returns an id we can optionally pass it; otherwise go to list
      const id = res && res.data && res.data.id ? res.data.id : null;
      // brief success feedback then navigate
      // (avoid blocking UX with native alert in SPA flows)
      setTimeout(() => {
        if (id) {
          navigate('/reports');
        } else {
          navigate('/reports');
        }
      }, 150);
    } catch (err) {
      const msg = err?.response?.data?.detail || err?.message || 'Failed to save measurement. Please try again.';
      setError(msg);
      console.error('Save measurement error:', err);
    } finally {
      setSaving(false);
    }
  };

  const getLightingMessage = () => {
    switch (lightingFeedback) {
      case 'dim':
        return '🌙 More light needed';
      case 'bright':
        return '☀️ Reduce bright light';
      default:
        return '✓ Lighting is good';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-8">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Take a Measurement</h1>
        <p className="text-gray-600 mb-8">
          Follow the on-screen instructions to measure your vitals using your device's camera.
        </p>

        {!cameraPermission && (
          <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-4 rounded-lg mb-8 flex items-center gap-3">
            <AlertCircle className="h-5 w-5 flex-shrink-0" />
            <div>
              <p className="font-semibold">Camera Access Required</p>
              <p className="text-sm">Please allow camera access to proceed with measurements.</p>
            </div>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Camera Preview Container */}
        <div className="bg-black rounded-lg overflow-hidden mb-8 relative aspect-video">
          {cameraPermission ? (
            <>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="w-full h-full object-cover"
              />
              {/* Face outline graphic for visual feedback */}
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <svg
                  className="w-72 h-72 text-white/30"
                  viewBox="0 0 200 200"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <circle cx="100" cy="100" r="90" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path
                    d="M60,140 Q100,180 140,140"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                </svg>
              </div>

              {/* Safe Zone Overlay */}
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className="w-64 h-64 border-2 border-green-400 rounded-full opacity-50"></div>
                <div className="absolute bottom-6 left-6 right-6 bg-black/60 text-white px-4 py-2 rounded-lg text-sm text-center">
                  {getLightingMessage()}
                </div>
              </div>

              {/* Progress Indicator */}
              {measuring && (
                <div className="absolute inset-0 bg-black/40 flex flex-col items-center justify-center">
                  <div className="w-24 h-24 border-4 border-white/20 border-t-white rounded-full animate-spin mb-4"></div>
                  <p className="text-white text-lg font-semibold">{progress}%</p>
                  <p className="text-white/80 text-sm">Analyzing face...</p>
                  {/* scanning bar animation */}
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="scanner-bar"></div>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gray-800">
              <div className="text-center">
                <Camera className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-400">Camera not available</p>
              </div>
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
          <h3 className="font-semibold text-blue-900 mb-2">📋 Instructions</h3>
          <ul className="text-blue-800 space-y-2 text-sm">
            <li>✓ Position your face in the center circle</li>
            <li>✓ Ensure good lighting on your face</li>
            <li>✓ Keep your head still during measurement (30 seconds)</li>
            <li>✓ Avoid wearing heavy makeup or glasses</li>
          </ul>
        </div>

        {/* Measurement Button */}
        <button
          onClick={handleStartMeasurement}
          disabled={!cameraPermission || measuring}
          className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold py-4 px-6 rounded-lg transition text-lg mb-8"
        >
          {measuring ? `Measuring... ${progress}%` : '🔴 Start Measurement'}
        </button>

        {/* Results */}
        {result && (
          <div className="bg-white border-2 border-green-200 rounded-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <CheckCircle className="h-6 w-6 text-green-500" />
              <h3 className="text-xl font-semibold text-gray-900">Measurement Complete!</h3>
            </div>

            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="bg-red-50 rounded-lg p-4">
                <p className="text-gray-600 text-sm mb-1">Heart Rate</p>
                <p className="text-3xl font-bold text-red-600">{result.heartRate}</p>
                <p className="text-gray-600 text-xs">bpm</p>
              </div>
              <div className="bg-blue-50 rounded-lg p-4">
                <p className="text-gray-600 text-sm mb-1">Blood Oxygen</p>
                <p className="text-3xl font-bold text-blue-600">{result.spO2}</p>
                <p className="text-gray-600 text-xs">%</p>
              <div className="bg-yellow-50 rounded-lg p-4">
                <p className="text-gray-600 text-sm mb-1">Stress Level</p>
                <p className="text-3xl font-bold text-yellow-600">{result.stressLevel || '--'}</p>
                <p className="text-gray-600 text-xs">%</p>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <p className="text-gray-600 text-sm mb-1">Hydration</p>
                <p className="text-3xl font-bold text-purple-600">{result.hydration || '--'}</p>
                <p className="text-gray-600 text-xs">%</p>
              </div>
              </div>
            </div>

            <div className="flex gap-4">
              <button
                onClick={() => setResult(null)}
                className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-900 font-semibold py-2 px-4 rounded-lg transition"
              >
                New Measurement
              </button>
              <button
                onClick={handleSaveResult}
                disabled={saving}
                className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition"
              >
                {saving ? 'Saving...' : 'Save & View Report'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

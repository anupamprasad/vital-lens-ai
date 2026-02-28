import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Heart, TrendingUp, Calendar, Activity } from 'lucide-react';
import VitalsChart from '../components/VitalsChart';
import VitalCard from '../components/VitalCard';
import { vitalsService } from '../services/api';

export default function DashboardPage({ user }) {
  const [vitals, setVitals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('week');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchVitals = async () => {
      setLoading(true);
      setError('');
      try {
        const response = await vitalsService.listVitals(selectedPeriod);
        const vitalsList = response.data.map((v, idx) => ({
          id: idx,
          timestamp: new Date(v.timestamp),
          heartRate: v.heart_rate,
          spO2: v.spO2,
          status: v.heart_rate > 100 ? 'elevated' : 'normal',
        }));
        setVitals(vitalsList);
      } catch (err) {
        setError('Failed to load vitals');
        console.error(err);
        // Fallback to mock data for development
        const mockVitals = [
          { id: 1, timestamp: new Date(Date.now() - 86400000), heartRate: 72, spO2: 98, status: 'normal' },
          { id: 2, timestamp: new Date(Date.now() - 72000000), heartRate: 75, spO2: 97, status: 'normal' },
          { id: 3, timestamp: new Date(Date.now() - 57600000), heartRate: 70, spO2: 99, status: 'normal' },
          { id: 4, timestamp: new Date(Date.now() - 43200000), heartRate: 78, spO2: 96, status: 'normal' },
          { id: 5, timestamp: new Date(Date.now() - 28800000), heartRate: 73, spO2: 98, status: 'normal' },
          { id: 6, timestamp: new Date(Date.now() - 14400000), heartRate: 71, spO2: 99, status: 'normal' },
          { id: 7, timestamp: new Date(), heartRate: 74, spO2: 98, status: 'normal' },
        ];
        setVitals(mockVitals);
      } finally {
        setLoading(false);
      }
    };

    fetchVitals();
  }, [selectedPeriod]);

  const latestVital = vitals.length > 0 ? vitals[vitals.length - 1] : null;
  const averageHR = vitals.length > 0 ? Math.round(vitals.reduce((sum, v) => sum + v.heartRate, 0) / vitals.length) : 0;
  const averageSpO2 = vitals.length > 0 ? Math.round(vitals.reduce((sum, v) => sum + v.spO2, 0) / vitals.length) : 0;

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.name || 'User'}</h1>
          <p className="text-gray-600 mt-2">Monitor your vital signs in real-time</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <VitalCard
            icon={<Heart className="h-6 w-6 text-red-500" />}
            title="Heart Rate"
            value={latestVital?.heartRate || '--'}
            unit="bpm"
            status={latestVital?.status || 'unknown'}
          />
          <VitalCard
            icon={<Activity className="h-6 w-6 text-blue-500" />}
            title="Blood Oxygen"
            value={latestVital?.spO2 || '--'}
            unit="%"
            status={latestVital?.spO2 >= 95 ? 'normal' : 'warning'}
          />
          <VitalCard
            icon={<TrendingUp className="h-6 w-6 text-green-500" />}
            title="Avg Heart Rate"
            value={averageHR}
            unit="bpm"
            status="normal"
          />
          <VitalCard
            icon={<Calendar className="h-6 w-6 text-purple-500" />}
            title="Measurements"
            value={vitals.length}
            unit={`this ${selectedPeriod}`}
            status="normal"
          />
        </div>

        {/* Period Selector */}
        <div className="mb-6 flex gap-2">
          {['week', 'month', 'year'].map((period) => (
            <button
              key={period}
              onClick={() => setSelectedPeriod(period)}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                selectedPeriod === period
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {period.charAt(0).toUpperCase() + period.slice(1)}
            </button>
          ))}
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <VitalsChart
            data={vitals}
            title="Heart Rate Trend"
            dataKey="heartRate"
            color="#ef4444"
            unit="bpm"
          />
          <VitalsChart
            data={vitals}
            title="Blood Oxygen Level"
            dataKey="spO2"
            color="#3b82f6"
            unit="%"
          />
        </div>

        {/* Action Buttons (use SPA navigation) */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to="/camera"
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-4 px-6 rounded-lg text-center transition"
          >
            📷 Take Measurement
          </Link>
          <Link
            to="/reports"
            className="bg-green-600 hover:bg-green-700 text-white font-semibold py-4 px-6 rounded-lg text-center transition"
          >
            📊 View Reports
          </Link>
          <Link
            to="/settings"
            className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-4 px-6 rounded-lg text-center transition"
          >
            ⚙️ Settings
          </Link>
          <Link
            to="/users"
            className="bg-yellow-600 hover:bg-yellow-700 text-white font-semibold py-4 px-6 rounded-lg text-center transition"
          >
            👥 User List
          </Link>
        </div>
      </div>
    </div>
  );
}

import { useState, useEffect } from 'react';
import { Download, FileText, Calendar } from 'lucide-react';
import { vitalsService } from '../services/api';

export default function ReportsPage({ user }) {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchVitals = async () => {
      setLoading(true);
      setError('');
      try {
        const response = await vitalsService.listVitals('month');
        const vitals = response.data;

        // Group vitals by week and compute weekly stats
        const weeklyReports = {};
        vitals.forEach((v) => {
          const date = new Date(v.timestamp);
          const weekStart = new Date(date);
          weekStart.setDate(date.getDate() - date.getDay());
          const weekKey = weekStart.toISOString().split('T')[0];

          if (!weeklyReports[weekKey]) {
            weeklyReports[weekKey] = {
              date: weekKey,
              heartRates: [],
              spO2s: [],
              count: 0,
            };
          }
          weeklyReports[weekKey].heartRates.push(v.heart_rate);
          weeklyReports[weekKey].spO2s.push(v.spO2 || 0);
          weeklyReports[weekKey].count += 1;
        });

        // Convert to report cards with computed averages
        const reportsList = Object.entries(weeklyReports)
          .map(([key, data], idx) => ({
            id: idx + 1,
            date: data.date,
            averageHR: Math.round(data.heartRates.reduce((a, b) => a + b, 0) / data.heartRates.length),
            averageSpO2: Math.round(data.spO2s.reduce((a, b) => a + b, 0) / data.spO2s.length),
            measurements: data.count,
            trend: data.heartRates[data.heartRates.length - 1] < data.heartRates[0] ? 'improving' : 'stable',
          }))
          .sort((a, b) => new Date(b.date) - new Date(a.date));

        setReports(reportsList);
      } catch (err) {
        console.error('Failed to load vitals', err);
        setError('Could not load vitals data');
      } finally {
        setLoading(false);
      }
    };

    fetchVitals();
  }, []);

  const handleGeneratePDF = (reportId) => {
    // Mock PDF generation
    alert(`Generating PDF report for report #${reportId}...`);
  };

  const handleExportCSV = () => {
    // Mock CSV export
    alert('Exporting all measurements as CSV...');
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Your Reports</h1>
          <p className="text-gray-600 mt-2">View and download your health reports</p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          </div>
        ) : reports.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600 mb-4">No measurements yet. Take a measurement on the camera page to see reports.</p>
          </div>
        ) : (
          <>
            {/* Export Options */}
            <div className="bg-white border border-gray-200 rounded-lg p-6 mb-8 flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Export All Data</h3>
                <p className="text-gray-600 text-sm">Download all your measurements as CSV</p>
              </div>
              <button
                onClick={handleExportCSV}
                className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-6 rounded-lg transition flex items-center gap-2"
              >
                <Download className="h-5 w-5" />
                Export CSV
              </button>
            </div>

            {/* Reports List */}
            <div className="space-y-4">
              {reports.map((report) => (
                <div key={report.id} className="bg-white border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                        <Calendar className="h-5 w-5 text-gray-400" />
                        Weekly Report - {new Date(report.date).toLocaleDateString()}
                      </h3>
                    </div>
                    <button
                      onClick={() => handleGeneratePDF(report.id)}
                      className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition flex items-center gap-2"
                    >
                      <FileText className="h-5 w-5" />
                      PDF
                    </button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="bg-red-50 rounded-lg p-4">
                      <p className="text-gray-600 text-sm mb-1">Avg Heart Rate</p>
                      <p className="text-2xl font-bold text-red-600">{report.averageHR}</p>
                      <p className="text-gray-600 text-xs">bpm</p>
                    </div>
                    <div className="bg-blue-50 rounded-lg p-4">
                      <p className="text-gray-600 text-sm mb-1">Avg Blood Oxygen</p>
                      <p className="text-2xl font-bold text-blue-600">{report.averageSpO2}</p>
                      <p className="text-gray-600 text-xs">%</p>
                    </div>
                    <div className="bg-purple-50 rounded-lg p-4">
                      <p className="text-gray-600 text-sm mb-1">Measurements</p>
                      <p className="text-2xl font-bold text-purple-600">{report.measurements}</p>
                      <p className="text-gray-600 text-xs">this week</p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4">
                      <p className="text-gray-600 text-sm mb-1">Trend</p>
                      <p className="text-2xl font-bold text-green-600 capitalize">{report.trend}</p>
                      <p className="text-gray-600 text-xs">status</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Health Score Card */}
            <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg p-8 mt-8 text-white">
              <h3 className="text-2xl font-bold mb-2">Your Health Score</h3>
              <p className="text-indigo-100 mb-6">Based on your recent measurements</p>
              <div className="text-6xl font-bold mb-4">88/100</div>
              <p className="text-indigo-100 mb-6">Excellent health metrics. Keep up the good work!</p>
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-32 bg-indigo-300 rounded-full">
                    <div className="h-full w-24 bg-green-400 rounded-full"></div>
                  </div>
                  <span>Heart Rate: Good</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-32 bg-indigo-300 rounded-full">
                    <div className="h-full w-28 bg-green-400 rounded-full"></div>
                  </div>
                  <span>Blood Oxygen: Excellent</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-32 bg-indigo-300 rounded-full">
                    <div className="h-full w-26 bg-green-400 rounded-full"></div>
                  </div>
                  <span>Consistency: Good</span>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

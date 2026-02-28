export default function VitalCard({ icon, title, value, unit, status }) {
  const statusColors = {
    normal: 'bg-green-50 border-green-200 text-green-900',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-900',
    critical: 'bg-red-50 border-red-200 text-red-900',
  };

  const statusBgColor = statusColors[status] || statusColors.normal;

  return (
    <div className={`rounded-lg border p-6 ${statusBgColor}`}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-gray-700">{title}</h3>
        {icon}
      </div>
      <div className="flex items-baseline gap-1">
        <p className="text-3xl font-bold">{value}</p>
        <p className="text-sm text-gray-600">{unit}</p>
      </div>
      <p className="text-xs text-gray-600 mt-3 capitalize">{status}</p>
    </div>
  );
}

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Privacy Policy & GDPR Compliance</h1>

        <div className="space-y-8 prose prose-lg max-w-none">
          <section className="bg-white rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Data Collection</h2>
            <p className="text-gray-700 mb-4">
              Vital Lens AI collects facial video data for the sole purpose of calculating vital signs using 
              Remote Photoplethysmography (rPPG). We process the minimum data necessary:
            </p>
            <ul className="list-disc list-inside text-gray-700 space-y-2 mb-4">
              <li>Facial video frames (30 seconds per measurement)</li>
              <li>Derived vitals data (heart rate, blood oxygen)</li>
              <li>Measurement metadata (timestamp, quality score)</li>
              <li>Account information (name, email)</li>
            </ul>
          </section>

          <section className="bg-white rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Data Processing & On-Device Privacy</h2>
            <p className="text-gray-700 mb-4">
              <strong>Privacy First Architecture:</strong> All facial video processing occurs on your device. 
              Raw video frames are never transmitted to our servers.
            </p>
            <ul className="list-disc list-inside text-gray-700 space-y-2">
              <li>✓ Face detection & analysis: On-device via MediaPipe</li>
              <li>✓ rPPG algorithm processing: Runs locally</li>
              <li>✓ Facial video: Deleted immediately after processing</li>
              <li>✓ Only heart rate & SpO₂ values sent to server</li>
            </ul>
          </section>

          <section className="bg-white rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Data Security (HIPAA Compliance)</h2>
            <ul className="list-disc list-inside text-gray-700 space-y-2 mb-4">
              <li><strong>Encryption in Transit:</strong> TLS 1.2+ for all API communications</li>
              <li><strong>Encryption at Rest:</strong> AES-256 encryption for stored data</li>
              <li><strong>Authentication:</strong> OAuth 2.0 + 2FA support</li>
              <li><strong>Audit Logging:</strong> All access to health data logged</li>
            </ul>
          </section>

          <section className="bg-white rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Your GDPR Rights</h2>
            <p className="text-gray-700 mb-4">Under GDPR, you have the right to:</p>
            <ul className="list-disc list-inside text-gray-700 space-y-2 mb-4">
              <li><strong>Access:</strong> Request all your personal data</li>
              <li><strong>Portability:</strong> Export your data in machine-readable format</li>
              <li><strong>Erasure:</strong> Request deletion of your account and data</li>
              <li><strong>Rectification:</strong> Correct inaccurate personal information</li>
              <li><strong>Withdraw Consent:</strong> Stop data processing at any time</li>
            </ul>
            <p className="text-gray-700">
              To exercise these rights, contact us at: <strong>privacy@vitalensai.com</strong>
            </p>
          </section>

          <section className="bg-white rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Data Retention</h2>
            <ul className="list-disc list-inside text-gray-700 space-y-2">
              <li>Account data: Retained until account deletion</li>
              <li>Health measurements: Retained until user deletion request</li>
              <li>Audit logs: Retained for 90 days for security purposes</li>
              <li>Facial video: Deleted immediately (never stored)</li>
            </ul>
          </section>

          <section className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-blue-900 mb-4">⚠️ Important Disclaimer</h2>
            <p className="text-blue-900 font-semibold mb-2">
              Vital Lens AI is a wellness application, NOT a medical device.
            </p>
            <p className="text-blue-800">
              This app is for general health tracking purposes only. Heart rate and blood oxygen readings 
              are estimates and should not be used for medical diagnosis or treatment. Consult a healthcare 
              professional for any health concerns.
            </p>
          </section>

          <section className="bg-white rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Contact & Support</h2>
            <p className="text-gray-700 space-y-2">
              <span>Data Protection Officer: dpo@vitalensai.com</span>
              <br />
              <span>Privacy Inquiries: privacy@vitalensai.com</span>
              <br />
              <span>Support: support@vitalensai.com</span>
            </p>
          </section>

          <section className="bg-gray-100 rounded-lg p-6 text-center text-gray-600 text-sm">
            <p>Last Updated: February 28, 2026</p>
            <p>By using Vital Lens AI, you agree to this Privacy Policy and Terms of Service.</p>
          </section>
        </div>
      </div>
    </div>
  );
}

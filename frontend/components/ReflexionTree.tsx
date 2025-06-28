export default function ReflexionTree({ steps }) {
  return (
    <div className="p-4 bg-gray-50 rounded">
      <h2 className="text-lg font-semibold mb-2">🧠 Reasoning Trace Tree</h2>
      <ul className="list-disc ml-4">
        {steps.map((s, idx) => (
          <li key={idx}>
            {s.step}
            <ul className="list-circle ml-6 text-sm text-gray-600">
              <li>🧩 Why: {s.why}</li>
              <li>🔧 Fix: {s.fix}</li>
              <li>📈 Confidence: {s.confidence}</li>
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
}

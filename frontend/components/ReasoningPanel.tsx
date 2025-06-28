export default function ReasoningPanel({ plan }) {
  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-4">🔁 Reflexion Plan</h2>
      {plan.steps.map((step, i) => (
        <div key={i} className="mb-2">
          <p><strong>Step {i + 1}:</strong> {step.step}</p>
          <p className="text-sm italic text-gray-600">Why: {step.why}</p>
          <p className="text-green-700 font-mono mt-1">Fix: {step.fix}</p>
          <p className="text-xs text-gray-500">Confidence: {step.confidence}/10</p>
        </div>
      ))}
    </div>
  );
}

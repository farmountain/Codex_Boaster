export default function ReasoningPanel({ reasoning, plan }) {
  return (
    <div className="p-4 bg-white rounded shadow mb-4">
      <h2 className="text-xl font-bold">🧠 Agent Reasoning</h2>
      <pre className="whitespace-pre-wrap text-gray-700">{reasoning}</pre>
      <h3 className="text-lg font-semibold mt-4">📦 Modules Planned</h3>
      <ul className="list-disc ml-6">
        {plan.map((mod, idx) => (
          <li key={idx} className="py-1">
            <strong>{mod.name}</strong> – {mod.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

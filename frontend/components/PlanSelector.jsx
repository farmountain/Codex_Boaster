import { useState } from 'react';

const plans = [
  { id: 'basic', label: 'Basic - $10', amount: 1000 },
  { id: 'pro', label: 'Pro - $20', amount: 2000 },
];

export default function PlanSelector() {
  const [selected, setSelected] = useState(null);

  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || '';

  async function checkout(plan) {
    setSelected(plan);
    await fetch(`${baseUrl}/charge`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 'test', amount: plan.amount }),
    });
  }

  return (
    <div>
      <h2>Select Plan</h2>
      {plans.map((p) => (
        <button key={p.id} onClick={() => checkout(p)}>
          {p.label}
        </button>
      ))}
      {selected && <p>Selected {selected.label}</p>}
    </div>
  );
}

import { useState } from 'react';

export default function PlanSelector({ userId, email }) {
  const [selected, setSelected] = useState('starter');

  async function startCheckout() {
    const res = await fetch('/api/charge', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, plan: selected, email }),
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    if (data.checkout_url) window.location.href = data.checkout_url;
  }

  return (
    <div className="p-6 bg-white rounded shadow w-full max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-center mb-4">Choose Your Plan</h2>
      <div className="space-y-3">
        {['starter', 'pro', 'enterprise'].map(plan => (
          <div key={plan} className={`p-4 border rounded ${selected === plan ? 'border-blue-600 bg-blue-50' : ''}`}>
            <label className="flex items-center space-x-2">
              <input type="radio" value={plan} name="plan" checked={selected === plan}
                onChange={() => setSelected(plan)} />
              <span className="capitalize font-semibold">{plan} Plan</span>
            </label>
            <p className="text-sm text-gray-600 mt-1">
              {plan === 'starter' && 'Free limited access'}
              {plan === 'pro' && 'Access to build/test/deploy loop + chat agent'}
              {plan === 'enterprise' && 'Full agent suite + team sharing + API'}
            </p>
          </div>
        ))}
      </div>
      <button onClick={startCheckout}
        className="mt-6 w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700">
        Continue to Checkout
      </button>
    </div>
  );
}

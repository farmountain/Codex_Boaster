import { useState } from 'react';

interface UATScenario {
  title: string;
  steps: string[];
  expected: string;
}

interface TestSuite {
  unit_tests: Record<string, string>;
  sit_tests: Record<string, string>;
  uat_scenarios: UATScenario[];
}

export default function TestMatrix({ suite }: { suite: TestSuite }) {
  const [tab, setTab] = useState<'unit' | 'sit' | 'uat'>('unit');

  return (
    <div className="mt-4">
      <h2 className="text-xl font-bold">🧪 Test Matrix</h2>
      <div className="space-x-2 mt-2">
        <button onClick={() => setTab('unit')} className={tab === 'unit' ? 'font-bold' : ''}>Unit</button>
        <button onClick={() => setTab('sit')} className={tab === 'sit' ? 'font-bold' : ''}>SIT</button>
        <button onClick={() => setTab('uat')} className={tab === 'uat' ? 'font-bold' : ''}>UAT</button>
      </div>
      {tab === 'unit' && (
        <div className="mt-2">
          {Object.entries(suite.unit_tests).map(([name, code]) => (
            <div key={name} className="mb-4">
              <h3 className="font-semibold">{name}</h3>
              <pre className="bg-gray-100 p-2 overflow-x-auto text-sm">{code}</pre>
            </div>
          ))}
        </div>
      )}
      {tab === 'sit' && (
        <div className="mt-2">
          {Object.entries(suite.sit_tests).map(([name, code]) => (
            <div key={name} className="mb-4">
              <h3 className="font-semibold">{name}</h3>
              <pre className="bg-gray-100 p-2 overflow-x-auto text-sm">{code}</pre>
            </div>
          ))}
        </div>
      )}
      {tab === 'uat' && (
        <div className="mt-2">
          {suite.uat_scenarios.map((s, idx) => (
            <div key={idx} className="mb-4">
              <h3 className="font-semibold">{s.title}</h3>
              <ol className="list-decimal ml-6">
                {s.steps.map((step, i) => (
                  <li key={i}>{step}</li>
                ))}
              </ol>
              <p className="mt-1 font-semibold">Expected: {s.expected}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

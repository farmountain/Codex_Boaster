export default function EnvVarForm({ envVars, setEnvVars }) {
  const updateKey = (oldKey, newKey) => {
    const updated = { ...envVars };
    const value = updated[oldKey];
    delete updated[oldKey];
    updated[newKey] = value;
    setEnvVars(updated);
  };

  const updateValue = (key, val) => {
    setEnvVars(prev => ({ ...prev, [key]: val }));
  };

  const addVar = () => {
    setEnvVars({ ...envVars, '': '' });
  };

  const removeVar = (key) => {
    const updated = { ...envVars };
    delete updated[key];
    setEnvVars(updated);
  };

  return (
    <div>
      <h2>Environment Variables</h2>
      {Object.entries(envVars).map(([key, val]) => (
        <div key={key} className="mb-2 flex items-center">
          <input
            type="text"
            placeholder="KEY"
            value={key}
            onChange={e => updateKey(key, e.target.value)}
            className="border p-2 mr-2"
          />
          <input
            type="password"
            placeholder="VALUE"
            value={val}
            onChange={e => updateValue(key, e.target.value)}
            className="border p-2 mr-2"
          />
          <button onClick={() => removeVar(key)} className="text-red-500">x</button>
        </div>
      ))}
      <button onClick={addVar} className="mt-2 text-blue-600 underline">
        + Add Variable
      </button>
    </div>
  );
}

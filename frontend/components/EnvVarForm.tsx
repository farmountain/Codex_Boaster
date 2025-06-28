export default function EnvVarForm({ envVars, setEnvVars }) {
  const handleChange = (key, value) => {
    setEnvVars(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div>
      <h2>Environment Variables</h2>
      {Object.entries(envVars).map(([key, val]) => (
        <div key={key} className="mb-2">
          <input
            type="text"
            placeholder="KEY"
            value={key}
            disabled
            className="border p-2"
          />
          <input
            type="password"
            placeholder="VALUE"
            value={val}
            onChange={e => handleChange(key, e.target.value)}
            className="border p-2 ml-2"
          />
        </div>
      ))}
      <button
        onClick={() => setEnvVars(prev => ({ ...prev, "": "" }))}
        className="mt-2 text-blue-600 underline"
      >
        + Add Variable
      </button>
    </div>
  );
}

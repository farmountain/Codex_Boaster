export default function RuntimeSelector({ onChange }) {
  const options = {
    python: ['3.12', '3.11', '3.10'],
    node: ['20', '18'],
    rust: ['1.87.0'],
    go: ['1.23.8'],
    java: ['21'],
  };

  return (
    <div className="mb-4">
      {Object.entries(options).map(([lang, versions]) => (
        <div key={lang}>
          <label>{lang}</label>
          <select onChange={e => onChange(lang, e.target.value)}>
            <option value="">Select Version</option>
            {versions.map(v => (
              <option key={v} value={v}>{v}</option>
            ))}
          </select>
        </div>
      ))}
    </div>
  );
}

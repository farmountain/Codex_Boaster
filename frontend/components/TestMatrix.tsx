export default function TestMatrix({ results }) {
  return (
    <div className="mt-4">
      <h2 className="text-xl font-bold">🧪 Test Matrix</h2>
      <table className="table-auto w-full">
        <thead><tr><th>Type</th><th>Status</th><th>Log</th></tr></thead>
        <tbody>
          {results.map((r, i) => (
            <tr key={i}>
              <td>{r.runtime}</td>
              <td>{r.success ? "✅ Pass" : "❌ Fail"}</td>
              <td><button onClick={() => r.onClick()}>View</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

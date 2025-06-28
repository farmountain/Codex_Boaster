export default function SetupPreview({ setupScript }) {
  return (
    <div className="bg-black text-green-300 p-4 rounded font-mono">
      {setupScript.map((line, idx) => (
        <div key={idx}>$ {line}</div>
      ))}
    </div>
  );
}

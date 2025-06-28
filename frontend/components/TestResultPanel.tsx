export default function TestResultPanel({ stdout, stderr }) {
  return (
    <div className="bg-black text-green-300 p-4 mt-4 rounded">
      <h3 className="text-lg font-bold text-white mb-2">Test Output</h3>
      <pre>{stdout || "No output"}</pre>
      {stderr && (
        <>
          <h4 className="text-red-400 mt-4">Errors</h4>
          <pre className="text-red-300">{stderr}</pre>
        </>
      )}
    </div>
  );
}

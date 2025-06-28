export default function ConfidenceScore({ score }) {
  const color = score > 0.85
    ? "bg-green-400"
    : score > 0.6
    ? "bg-yellow-400"
    : "bg-red-400"

  return (
    <div className={`px-2 py-1 rounded text-white text-xs ${color}`}>
      Confidence: {(score * 100).toFixed(1)}%
    </div>
  )
}

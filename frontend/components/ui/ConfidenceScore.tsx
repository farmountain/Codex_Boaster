import React from 'react';

export default function ConfidenceScore({ score }: { score: number }) {
  return (
    <span className="px-2 py-1 rounded bg-blue-100 text-blue-800 text-xs font-semibold">
      Confidence: {score}
    </span>
  );
}

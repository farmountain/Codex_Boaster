import { useEffect, useState } from "react";

interface Results {
  success: boolean | null;
  output?: string;
}

export default function TestResults() {
  const [results, setResults] = useState<Results | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/test_results")
      .then((res) => res.json())
      .then((data) => setResults(data));
  }, []);

  if (!results) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Test Results</h1>
      {results.success === null ? (
        <p>No tests run yet.</p>
      ) : results.success ? (
        <p>Tests Passed</p>
      ) : (
        <p>Tests Failed</p>
      )}
    </div>
  );
}

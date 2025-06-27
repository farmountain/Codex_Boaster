import { useEffect, useState } from 'react';

export default function ReasoningPanel() {
  const [suggestion, setSuggestion] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/improvement_suggestion')
      .then((res) => res.json())
      .then((data) => setSuggestion(data.suggestion));
  }, []);

  return (
    <div>
      <h2>Improvement Suggestion</h2>
      <pre>{suggestion || 'No suggestion'}</pre>
    </div>
  );
}

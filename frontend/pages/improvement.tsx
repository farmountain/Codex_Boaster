import { useEffect, useState } from "react";

export default function Improvement() {
  const [suggestion, setSuggestion] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/improvement_suggestion")
      .then((res) => res.json())
      .then((data) => setSuggestion(data.suggestion));
  }, []);

  return (
    <div>
      <h1>Improvement Suggestion</h1>
      <p>{suggestion || "No suggestion yet."}</p>
    </div>
  );
}

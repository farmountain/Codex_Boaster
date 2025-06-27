import { useEffect, useState } from 'react';

export default function UsageMeter() {
  const [usage, setUsage] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/test_results')
      .then((res) => res.json())
      .then((data) => {
        if (data.success === null) setUsage('No usage yet');
        else setUsage(data.success ? 'Last run passed' : 'Last run failed');
      });
  }, []);

  return (
    <div>
      <h2>Usage</h2>
      <p>{usage}</p>
    </div>
  );
}

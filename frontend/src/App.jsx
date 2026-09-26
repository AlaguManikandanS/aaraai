import { useEffect, useState } from "react";

import { getHealth } from "./api/health";

function App() {
  const [health, setHealth] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getHealth()
      .then((data) => {
        setHealth(data);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  return (
    <main>
      <h1>Aaraai</h1>

      {health && (
        <p>
          Backend: {health.status} — {health.service}
        </p>
      )}

      {error && (
        <p>
          Backend connection failed: {error}
        </p>
      )}

      {!health && !error && (
        <p>Connecting to Aaraai backend...</p>
      )}
    </main>
  );
}

export default App;
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function DataFetcher() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('/api/endpoint/')  // Utilise le proxy configuré
      .then(response => setData(response.data))
      .catch(error => console.error('Erreur API :', error));
  }, []);

  return (
    <div>
      <h2>Données de l'API :</h2>
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>Chargement...</p>}
    </div>
  );
}

export default DataFetcher;
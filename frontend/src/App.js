import React, { useState } from 'react';
import Uploader from './components/Uploader';
import ImageViewer from './components/ImageViewer';
import DownloadCSVButton from './components/DownloadCSVButton';

function App() {
  const [result, setResult] = useState(null);

  const handleProcess = (data) => {
    setResult(data);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Детекция подсолнухов</h1>
      <Uploader onImageProcessed={handleProcess} />

      {result && (
        <>
          <h3>Найдено подсолнухов: <strong>{result.sunflowers_data.length}</strong></h3>

          <ImageViewer
            imageSrc={`data:image/png;base64,${result.img_base64}`}
            boxes={result.sunflowers_data}
          />

          <DownloadCSVButton sunflowersData={result.sunflowers_data} />
        </>
      )}
    </div>
  );
}

export default App;
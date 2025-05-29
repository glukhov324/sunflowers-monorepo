// src/App.js

import React, { useState } from 'react';
import Uploader from './components/Uploader';
import ImageViewer from './components/ImageViewer';
import DownloadCSVButton from './components/DownloadCSVButton';

function App() {
  const [result, setResult] = useState(null);

  const handleProcess = (data) => {
    // Проверяем, что данные пришли корректно
    if (!data || !data.sunflowers_data || !Array.isArray(data.sunflowers_data)) {
      console.error('Некорректные данные:', data);
      alert('Ошибка: некорректные данные от сервера');
      return;
    }

    // Добавляем защиту: убираем null/undefined из geo_coords
    const processedData = data.sunflowers_data.map((item, index) => {
      const lat = item.geo_coords?.lat ?? null;
      const lon = item.geo_coords?.lon ?? null;

      return {
        ...item,
        geo_coords: {
          lat: lat !== null ? Number(lat) : null,
          lon: lon !== null ? Number(lon) : null,
        },
      };
    });

    setResult({
      ...data,
      sunflowers_data: processedData,
    });
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Детекция подсолнухов</h1>
      <Uploader onImageProcessed={handleProcess} />

      {result && (
        <div>
          {/* Вывод количества подсолнухов */}
          <h3 style={{ marginTop: '20px' }}>
            Найдено подсолнухов: <strong>{result.sunflowers_data.length}</strong>
          </h3>

          {/* Отображение изображения */}
          <ImageViewer
            imageSrc={`data:image/png;base64,${result.img_base64}`}
            boxes={result.sunflowers_data}
          />

          {/* Кнопка скачивания CSV */}
          <DownloadCSVButton sunflowersData={result.sunflowers_data} />
        </div>
      )}
    </div>
  );
}

export default App;
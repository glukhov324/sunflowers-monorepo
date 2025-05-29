import React from 'react';

const DownloadCSVButton = ({ sunflowersData }) => {
  const handleDownload = () => {
    if (!sunflowersData || !Array.isArray(sunflowersData) || sunflowersData.length === 0) {
      alert('Нет данных для экспорта');
      return;
    }

    const csvRows = [];

    // Заголовок CSV
    csvRows.push(['ID', 'lot', 'lan'].join(','));

    // Формируем строки
    sunflowersData.forEach((item, index) => {
      const lat = item.geo_coords?.lat ?? null;
      const lon = item.geo_coords?.lon ?? null;

      const latStr = lat !== null && !isNaN(lat) ? Number(lat).toFixed(15) : '-';
      const lonStr = lon !== null && !isNaN(lon) ? Number(lon).toFixed(15) : '-';

      csvRows.push([index + 1, latStr, lonStr].join(','));
    });

    const csvString = csvRows.join('\n');

    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'sunflowers_coordinates.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <button onClick={handleDownload} style={{ marginTop: '20px' }}>
      📥 Скачать таблицу с координатами
    </button>
  );
};

export default DownloadCSVButton;
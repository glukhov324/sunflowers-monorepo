import React from 'react';

const DownloadCSVButton = ({ sunflowersData }) => {
  const handleDownload = () => {
    if (!sunflowersData || !sunflowersData.length) {
      alert('Нет данных для экспорта');
      return;
    }

    // Формируем CSV
    const csvRows = [];

    // Заголовок
    csvRows.push(['ID', 'lat', 'lon'].join(','));

    // Данные
    sunflowersData.forEach((item, index) => {
      const { lat, lon } = item.geo_coords;
      csvRows.push([index + 1, lat.toFixed(15), lon.toFixed(15)].join(','));
    });

    // Объединяем всё в строку
    const csvString = csvRows.join('\n');

    // Создаём Blob и ссылку для скачивания
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
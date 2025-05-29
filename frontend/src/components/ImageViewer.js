import React, { useState, useEffect, useRef } from 'react';

const ImageViewer = ({ imageSrc, boxes }) => {
  const canvasRef = useRef(null);
  const tooltipRef = useRef(null);
  const [scale, setScale] = useState(1);

  // --- Отрисовка изображения и bounding box'ов ---
  useEffect(() => {
    if (!imageSrc) {
      console.warn('Изображение не загружено');
      return;
    }

    const img = new Image();
    // Добавляем префикс, если его нет
    img.src = imageSrc.startsWith('data') ? imageSrc : `data:image/png;base64,${imageSrc}`;

    img.onload = () => {
      const aspectRatio = img.width / img.height;
      const maxWidth = window.innerWidth * 0.9;
      const maxHeight = window.innerHeight * 0.8;

      let width = maxWidth;
      let height = maxWidth / aspectRatio;

      if (height > maxHeight) {
        height = maxHeight;
        width = height * aspectRatio;
      }

      setScale(width / img.width);

      const canvas = canvasRef.current;
      if (!canvas) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      canvas.width = width;
      canvas.height = height;

      // Очистка холста
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Рисуем изображение
      ctx.drawImage(img, 0, 0, width, height);

      // Рисуем боксы
      drawBoxes(ctx, boxes, scale);
    };

    img.onerror = () => {
      console.error('Ошибка загрузки изображения', img.src);
    };
  }, [imageSrc, boxes, scale]);

  // --- Функция рисования BBox ---
  const drawBoxes = (ctx, boxes, scale) => {
    if (!boxes?.length) {
      console.warn('Bounding box\'ов нет');
      return;
    }

    ctx.strokeStyle = 'lime';
    ctx.lineWidth = 2;
    ctx.font = '14px Arial';

    boxes.forEach((item, index) => {
      const { bbox, geo_coords } = item;

      const xu = Number(bbox.xu) * scale;
      const yu = Number(bbox.yu) * scale;
      const xd = Number(bbox.xd) * scale;
      const yd = Number(bbox.yd) * scale;

      const width = xd - xu;
      const height = yd - yu;

      // Проверяем корректность координат
      if (!isFinite(xu) || !isFinite(yu) || width <= 0 || height <= 0) {
        console.warn(`Некорректные координаты BBox:`, bbox);
        return;
      }

      // Рисуем прямоугольник
      ctx.strokeRect(xu, yu, width, height)

      // Текст внутри
      ctx.fillStyle = 'lime';
      //ctx.fillText(`#${index + 1}`, xu + 5, yu + 15);
    });
  };

  // --- Обработка событий мыши для tooltip'а ---
  const handleMouseMove = (e) => {
    const canvas = canvasRef.current;
    if (!canvas || !boxes.length) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    for (let i = 0; i < boxes.length; i++) {
      const { bbox } = boxes[i];
      const xu = Number(bbox.xu) * scale;
      const yu = Number(bbox.yu) * scale;
      const xd = Number(bbox.xd) * scale;
      const yd = Number(bbox.yd) * scale;

      const width = xd - xu;
      const height = yd - yu;

      if (
        x >= xu &&
        x <= xu + width &&
        y >= yu &&
        y <= yu + height
      ) {
        const { lat, lon } = boxes[i].geo_coords;
        showTooltip(lat, lon, x, y);
        return;
      }
    }

    hideTooltip();
  };

  const showTooltip = (lat, lon, x, y) => {
    const tooltip = tooltipRef.current;
    if (!tooltip) return;

    tooltip.style.display = 'block';
    tooltip.style.left = `${x + 10}px`;
    tooltip.style.top = `${y + 10}px`;

    const latStr = lat !== null && lat !== undefined ? Number(lat).toFixed(15) : '-';
    const lonStr = lon !== null && lon !== undefined ? Number(lon).toFixed(15) : '-';
    tooltip.innerHTML = `<strong>Широта:</strong> ${latStr}<br/><strong>Долгота:</strong> ${lonStr}`;
  };

  const hideTooltip = () => {
    const tooltip = tooltipRef.current;
    if (!tooltip) return;
    tooltip.style.display = 'none';
  };

  return (
    <div style={{ position: 'relative', marginTop: '20px' }}>
      <canvas
        ref={canvasRef}
        style={{ border: '1px solid #ccc' }}
        onMouseMove={handleMouseMove}
        onMouseLeave={hideTooltip}
      />
      <div
        ref={tooltipRef}
        style={{
          position: 'absolute',
          padding: '8px 12px',
          background: 'rgba(0, 0, 0, 0.7)',
          color: '#fff',
          borderRadius: '4px',
          pointerEvents: 'none',
          display: 'none',
          fontSize: '14px',
          zIndex: 10,
          whiteSpace: 'nowrap'
        }}
      />
    </div>
  );
};

export default ImageViewer;
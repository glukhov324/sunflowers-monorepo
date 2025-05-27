import React, { useState, useEffect, useRef } from 'react';

const ImageViewer = ({ imageSrc, boxes }) => {
  const canvasRef = useRef(null);
  const tooltipRef = useRef(null);
  const [scale, setScale] = useState(1);

  useEffect(() => {
    if (!imageSrc) return;

    const img = new Image();
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

      ctx.drawImage(img, 0, 0, width, height);
      drawBoxes(ctx, boxes, scale);
    };

    img.onerror = () => {
      console.error('Ошибка загрузки изображения', img.src);
    };
  }, [imageSrc, boxes, scale]);

  const drawBoxes = (ctx, boxes, scale) => {
    if (!boxes?.length) return;

    ctx.strokeStyle = 'lime';
    ctx.lineWidth = 2;
    ctx.font = '14px Arial';

    // Очистка предыдущих данных
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.drawImage(new Image(), 0, 0); // перерисовка фона не требуется, если картинка уже загружена

    boxes.forEach((item, index) => {
      const { bbox, geo_coords } = item;

      const xu = Math.max(0, Number(bbox.xu) * scale);
      const yu = Math.max(0, Number(bbox.yu) * scale);
      const xd = Math.min(canvasRef.current.width, Number(bbox.xd) * scale);
      const yd = Math.min(canvasRef.current.height, Number(bbox.yd) * scale);

      // Проверяем, чтобы bounding box оставался на холсте
      if (xu < 0 || yu < 0 || xd > canvasRef.current.width || yd > canvasRef.current.height) {
        console.warn(`Bounding box ${index} выходит за пределы холста:`, bbox);
        return;
      }

      ctx.save();
      ctx.beginPath();
      ctx.rect(xu, yu, xd - xu, yd - yu);
      ctx.stroke();
      ctx.fillStyle = 'lime';
      ctx.fillText(`#${index + 1}`, xu + 5, yu + 15); // Текст внутри bounding box
      ctx.restore();

      // Сохраняем данные в dataset
      ctx.putImageData(
        createBoxImageData(xu, yu, xd - xu, yd - yu, geo_coords),
        Math.floor(xu),
        Math.floor(yu)
      );
    });

    setupCanvasEvents(ctx, boxes, scale);
  };

  const createBoxImageData = (index, x, y, w, h, geo_coords) => {
    const canvas = canvasRef.current;
    const offCanvas = document.createElement('canvas');
    offCanvas.width = canvas.width;
    offCanvas.height = canvas.height;
    const ctx = offCanvas.getContext('2d');
    ctx.fillStyle = `rgba(0, 255, 0, ${index + 1})`;
    ctx.fillRect(x, y, w, h);
    ctx.fillStyle = 'white';
    ctx.fillText(`#${index + 1}`, x + 5, y - 5);
    return ctx.getImageData(0, 0, offCanvas.width, offCanvas.height);
  };

  const setupCanvasEvents = (ctx, boxes, scale) => {
    const canvas = canvasRef.current;
    const tooltip = tooltipRef.current;

    const showTooltip = (lat, lon, x, y) => {
      if (!tooltip) return;
      tooltip.style.display = 'block';
      tooltip.style.left = `${x + 10}px`;
      tooltip.style.top = `${y + 10}px`;
      tooltip.innerHTML = `<strong>Широта:</strong> ${lat.toFixed(6)}<br/><strong>Долгота:</strong> ${lon.toFixed(6)}`;
    };

    const hideTooltip = () => {
      if (tooltip) tooltip.style.display = 'none';
    };

    canvas.onmousemove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      for (let i = 0; i < boxes.length; i++) {
        const { bbox } = boxes[i];
        const xu = Math.max(0, Number(bbox.xu) * scale);
        const yu = Math.max(0, Number(bbox.yu) * scale);
        const xd = Math.min(canvasRef.current.width, Number(bbox.xd) * scale);
        const yd = Math.min(canvasRef.current.height, Number(bbox.yd) * scale);

        if (x >= xu && x <= xd && y >= yu && y <= yd) {
          const { lat, lon } = boxes[i].geo_coords;
          showTooltip(lat, lon, x, y);
          return;
        }
      }

      hideTooltip();
    };

    canvas.onmouseleave = () => {
      hideTooltip();
    };
  };

  return (
    <div style={{ position: 'relative', marginTop: '20px' }}>
      <canvas ref={canvasRef} style={{ border: '1px solid #ccc' }} />
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
import React, { useState } from 'react';
import axios from 'axios';
import config from '../config';

const Uploader = ({ onImageProcessed }) => {
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files?.[0] || null);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const response = await axios.post(process.env.REACT_APP_PREDICT_API_URL, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      onImageProcessed(response.data);
    } catch (error) {
      console.error('Ошибка при отправке изображения:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading || !file}>
        {loading ? 'Обработка...' : 'Загрузить'}
      </button>
    </div>
  );
};

export default Uploader;
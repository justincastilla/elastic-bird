"use client";

import { useState, useEffect } from 'react';

export default function Home() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [similarImages, setSimilarImages] = useState([]);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedImage) return;

    const formData = new FormData();
    formData.append('image', selectedImage);

    const res = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData,
    });

    const result = await res.json();
    setSimilarImages(result.similar_images);
  };

  return (
    <div className="upload">
      <h1>Upload an Image</h1>

      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleImageChange} />
        <button type="submit">Upload</button>
      </form>

      {previewUrl && (
        <div>
          <h2>Original Bird</h2>
          <img src={previewUrl} alt="original bird" width="200" />
        </div>
      )}

      {similarImages.length > 0 && (
        <div>
          <h2>Similar Birds</h2>
          <div className="similar-images-container">
            {similarImages.map((img, idx) => (
              <div key={idx} className="card">
                <img src={`/birds/${img.image_path}`} alt="similar bird" />
                <div className="card-content">
                  <h3>{img.name}</h3>
                  <p><i>{img.scientific_name}</i></p>
                  <p>Similarity Score: {img.score}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
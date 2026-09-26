import { useEffect, useState } from "react";

import {
  getDocument,
  getDocuments,
  uploadDocument,
} from "./api/documentApi";

function App() {
  const [file, setFile] = useState(null);
  const [document, setDocument] = useState(null);
  const [error, setError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    async function loadDocuments() {
      try {
        const documents = await getDocuments();

        if (documents.length > 0) {
          setDocument(documents[0]);
        }
      } catch (err) {
        setError(err.message);
      }
    }

    loadDocuments();
  }, []);

  useEffect(() => {
    if (!document || document.status !== "processing") {
      return;
    }

    const intervalId = setInterval(async () => {
      try {
        const updatedDocument = await getDocument(document.document_id);

        setDocument(updatedDocument);
      } catch (err) {
        setError(err.message);
      }
    }, 3000);

    return () => {
      clearInterval(intervalId);
    };
  }, [document]);

  function handleFileChange(event) {
    const selectedFile = event.target.files[0];

    setFile(selectedFile || null);
    setDocument(null);
    setError(null);
  }

  async function handleUpload() {
    if (!file) {
      setError("Please select a PDF first.");
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      const result = await uploadDocument(file);
      setDocument(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <main>
      <h1>Aaraai</h1>

      <p>Understand research papers better.</p>

      <input
        type="file"
        accept=".pdf,application/pdf"
        onChange={handleFileChange}
      />

      {file && (
        <p>
          Selected: {file.name}
        </p>
      )}

      <button
        type="button"
        onClick={handleUpload}
        disabled={!file || isUploading}
      >
        {isUploading ? "Uploading..." : "Upload Paper"}
      </button>

      {document && (
        <section>
          <h2>Document</h2>

          <p>Filename: {document.filename}</p>
          <p>Status: {document.status}</p>
          <p>Pages: {document.pages}</p>
          <p>Chunks: {document.chunks}</p>
        </section>
      )}

      {error && (
        <p>
          Error: {error}
        </p>
      )}
    </main>
  );
}

export default App;
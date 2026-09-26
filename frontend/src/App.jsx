import { useEffect, useState } from "react";

import {
  askQuestion,
  getDocument,
  getDocuments,
  uploadDocument,
} from "./api/documentApi";

function App() {
  const [file, setFile] = useState(null);
  const [document, setDocument] = useState(null);
  const [error, setError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [isAsking, setIsAsking] = useState(false);

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

  async function handleAskQuestion() {
    if (!document || document.status !== "ready") {
      setError("Document is not ready yet.");
      return;
    }

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setIsAsking(true);
    setError(null);
    setAnswer(null);

    try {
      const result = await askQuestion(
        document.document_id,
        question
      );

      setAnswer(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsAsking(false);
    }
  }

  const sourcePages = answer
    ? [...new Set(answer.sources.map((source) => source.page_number))]
    : [];

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

      {document?.status === "ready" && (
        <section>
          <h2>Ask Aaraai</h2>

          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a question about this research paper..."
            rows="4"
          />

          <button
            type="button"
            onClick={handleAskQuestion}
            disabled={isAsking || !question.trim()}
          >
            {isAsking ? "Thinking..." : "Ask"}
          </button>

          {answer && (
            <section>
              <h2>Answer</h2>

              <p>{answer.answer}</p>

              <h3>Sources</h3>

              <ul>
                {sourcePages.map((page) => (
                  <li key={page}>
                    Page {page}
                  </li>
                ))}
              </ul>
            </section>
          )}
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
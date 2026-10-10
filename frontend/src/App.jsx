import { useEffect, useState } from "react";

import {
  askQuestion,
  getDocument,
  getDocuments,
  uploadDocument,
  getDocumentSummary,
} from "./api/documentApi";

function App() {
  const [file, setFile] = useState(null);
  const [document, setDocument] = useState(null);
  const [error, setError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [isAsking, setIsAsking] = useState(false);

  const [summary, setSummary] = useState(null);
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [summaryError, setSummaryError] = useState("");

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

  async function handleSummary() {
    if (!document || document.status !== "ready") {
      return;
    }

    setSummaryLoading(true);
    setSummaryError("");

    try {
      const data = await getDocumentSummary(document.document_id);
      setSummary(data);
    } catch (error) {
      setSummaryError(error.message);
    } finally {
      setSummaryLoading(false);
    }
  }

  const sourcePages = answer
    ? [...new Set(answer.sources.map((source) => source.page_number))]
    : [];

  function parseSummary(summaryText) {
    const sections = [
      "OVERVIEW",
      "PROBLEM",
      "METHODOLOGY",
      "KEY FINDINGS",
      "LIMITATIONS",
    ];

    const parsed = {};

    for (let i = 0; i < sections.length; i++) {
      const currentSection = sections[i];
      const nextSection = sections[i + 1];

      const startMarker = `${currentSection}:`;
      const startIndex = summaryText.indexOf(startMarker);

      if (startIndex === -1) {
        parsed[currentSection] = "";
        continue;
      }

      const contentStart = startIndex + startMarker.length;

      const endIndex = nextSection
        ? summaryText.indexOf(`${nextSection}:`, contentStart)
        : summaryText.length;

      parsed[currentSection] = summaryText
        .slice(contentStart, endIndex === -1 ? summaryText.length : endIndex)
        .trim();
    }

    return parsed;
  }

  function parseBulletPoints(text) {
    return text
      .split(/\s*-\s+/)
      .map((item) => item.trim())
      .filter(Boolean);
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

      {document?.status === "ready" && (
        <section>
          <h2>Paper Overview</h2>

          <button
            type="button"
            onClick={handleSummary}
            disabled={summaryLoading}
          >
            {summaryLoading ? "Generating Overview..." : "Generate Paper Overview"}
          </button>

          {summaryError && (
            <p>
              Error: {summaryError}
            </p>
          )}

          {summary && (
            <section className="paper-overview">
              <div className="overview-header">
                <div>
                  <h2>Paper Overview</h2>
                  <p>AI-generated understanding of your research paper.</p>
                </div>
              </div>

              {(() => {
                const parsedSummary = parseSummary(summary.overview);

                return (
                  <>
                    <article className="overview-card">
                      <h3>Overview</h3>
                      <p>{parsedSummary.OVERVIEW}</p>
                    </article>

                    <article className="overview-card">
                      <h3>Problem</h3>
                      <p>{parsedSummary.PROBLEM}</p>
                    </article>

                    <article className="overview-card">
                      <h3>Methodology</h3>
                      <p>{parsedSummary.METHODOLOGY}</p>
                    </article>

                    <article className="overview-card">
                      <h3>Key Findings</h3>
                      <ul>
                        {parseBulletPoints(parsedSummary["KEY FINDINGS"]).map(
                          (item) => (
                            <li key={item}>{item}</li>
                          )
                        )}
                      </ul>
                    </article>

                    <article className="overview-card">
                      <h3>Limitations</h3>
                      <ul>
                        {parseBulletPoints(parsedSummary.LIMITATIONS).map(
                          (item) => (
                            <li key={item}>{item}</li>
                          )
                        )}
                      </ul>
                    </article>

                    <div className="overview-sources">
                      <h3>Sources</h3>
                      <div className="source-list">
                        {summary.sources.map((source) => (
                          <span
                            className="source-badge"
                            key={source.page_number}
                          >
                            Page {source.page_number}
                          </span>
                        ))}
                      </div>
                    </div>
                  </>
                );
              })()}
            </section>
          )}
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
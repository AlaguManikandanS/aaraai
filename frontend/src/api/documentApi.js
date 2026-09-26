const API_BASE_URL = "http://localhost:8000/api";

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/documents/upload/`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);

    throw new Error(
      errorData?.error || `Upload failed: ${response.status}`
    );
  }

  return response.json();
}

export async function getDocument(documentId) {
  const response = await fetch(
    `${API_BASE_URL}/documents/${documentId}/`
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);

    throw new Error(
      errorData?.error || `Request failed: ${response.status}`
    );
  }

  return response.json();
}

export async function getDocuments() {
  const response = await fetch(
    `${API_BASE_URL}/documents/`
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      errorData?.error || `Request failed: ${response.status}`
    );
  }

  return response.json();
}
// API Base URL
const apiUrl = 'http://127.0.0.1:5000';

// Upload PDF and Extract Text
async function uploadPDF() {
    const fileInput = document.getElementById('pdfUpload');
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select a PDF file.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${apiUrl}/upload`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        document.getElementById('extractedText').value = data.text || "Text extraction failed.";
    } catch (error) {
        console.error(error);
        alert("An error occurred while uploading the PDF.");
    }
}

// Scrape arXiv URL and Extract Text
async function scrapeArxiv() {
    const arxivUrl = document.getElementById('arxivUrl').value;
    if (!arxivUrl) {
        alert("Please enter an arXiv URL.");
        return;
    }

    try {
        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: arxivUrl })
        });

        const data = await response.json();
        if (response.ok) {
            document.getElementById('extractedText').value = data.text;
        } else {
            alert(data.error || "An error occurred while scraping the arXiv URL.");
        }
    } catch (error) {
        console.error(error);
        alert("An error occurred while scraping the arXiv URL.");
    }
}

// Play Text-to-Speech
async function playTTS() {
    const text = document.getElementById('extractedText').value;
    if (!text) {
        alert("No text available for TTS.");
        return;
    }

    try {
        const response = await fetch(`${apiUrl}/tts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        const audio = new Audio(`${apiUrl}/${data.file}`);
        audio.play();
    } catch (error) {
        console.error(error);
        alert("An error occurred while playing the text-to-speech.");
    }
}

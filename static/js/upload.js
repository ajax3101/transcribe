document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const statusDiv = document.getElementById('status');
        const statusText = document.getElementById('status-text');
        const progressBar = document.getElementById('progress-bar');
        const toastBody = document.getElementById('toast-body');
        const uploadToastElem = document.getElementById('uploadToast');

        if (!statusDiv || !statusText || !progressBar || !toastBody || !uploadToastElem) return;
        const uploadToast = new bootstrap.Toast(uploadToastElem);

        statusDiv.style.display = 'block';
        statusText.innerText = 'Uploading...';
        progressBar.style.width = '0%';
        progressBar.innerText = '0%';

        const formData = new FormData(this);
        const response = await fetch('/upload', { method: 'POST', body: formData });

        if (response.ok) {
            const data = await response.json();
            const taskId = data.task_id;
            checkStatus(taskId);
        } else {
            showToast('Upload error!');
        }
    });
});

async function checkStatus(taskId) {
    const statusText = document.getElementById('status-text');
    const progressBar = document.getElementById('progress-bar');

    const response = await fetch(`/status/${taskId}`);
    const data = await response.json();

    if (data.status === 'completed') {
        statusText.innerText = 'Completed!';
        progressBar.style.width = '100%';
        progressBar.innerText = '100%';
        setTimeout(() => window.location.href = `/result/${taskId}`, 1000);
    } else if (data.status === 'error') {
        statusText.innerText = 'Error occurred.';
    } else {
        setTimeout(() => checkStatus(taskId), 1000);
    }
}

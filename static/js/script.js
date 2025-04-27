document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files.length) {
        alert('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const progressBar = document.getElementById('progressBar');
    const progressContainer = document.querySelector('.progress');
    const statusDiv = document.getElementById('status');
    const spinnerDiv = document.getElementById('spinner');

    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    progressBar.innerText = '0%';
    statusDiv.innerText = 'Uploading...';

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);

    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            const percentComplete = Math.round((event.loaded / event.total) * 100);
            progressBar.style.width = percentComplete + '%';
            progressBar.innerText = percentComplete + '%';
        }
    };

    xhr.onload = function() {
        if (xhr.status === 200) {
            progressBar.style.width = '100%';
            progressBar.innerText = 'Upload complete';
            spinnerDiv.style.display = 'block';
            statusDiv.innerText = 'Converting to WAV...';

            const response = JSON.parse(xhr.responseText);
            pollStatus(response.task_id);
        } else {
            statusDiv.innerText = 'Error uploading file!';
        }
    };

    xhr.send(formData);
});

function pollStatus(task_id) {
    const statusDiv = document.getElementById('status');
    fetch(`/status/${task_id}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'processing') {
                statusDiv.innerText = data.step;
                setTimeout(() => pollStatus(task_id), 1000);
            } else if (data.status === 'completed') {
                statusDiv.innerText = 'Completed!';
                window.location.href = `/result/${task_id}`;
            } else {
                statusDiv.innerText = 'Error processing file!';
            }
        });
}

document.getElementById('upload-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    const statusDiv = document.getElementById('status');
    const statusText = document.getElementById('status-text');
    const progressBar = document.getElementById('progress-bar');
    const toastBody = document.getElementById('toast-body');
    const uploadToast = new bootstrap.Toast(document.getElementById('uploadToast'));

    statusDiv.style.display = 'block';
    statusText.innerText = 'Uploading...';
    progressBar.style.width = '0%';
    progressBar.setAttribute('aria-valuenow', 0);
    progressBar.innerText = '0%';
    toastBody.innerText = 'Uploading started...';
    uploadToast.show();

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        const taskId = data.task_id;
        checkStatus(taskId);
    } else {
        statusText.innerText = 'Error uploading file.';
        toastBody.innerText = 'Error uploading file.';
        uploadToast.show();
    }
});

async function checkStatus(taskId) {
    const statusText = document.getElementById('status-text');
    const progressBar = document.getElementById('progress-bar');
    const toastBody = document.getElementById('toast-body');
    const uploadToast = new bootstrap.Toast(document.getElementById('uploadToast'));

    const response = await fetch(`/status/${taskId}`);
    const data = await response.json();

    if (data.status === 'completed') {
        statusText.innerText = 'Processing complete!';
        progressBar.style.width = '100%';
        progressBar.setAttribute('aria-valuenow', 100);
        progressBar.innerText = '100%';
        toastBody.innerText = 'Processing complete!';
        uploadToast.show();
        setTimeout(() => {
            window.location.href = `/result/${taskId}`;
        }, 1000);
    } else if (data.status === 'error') {
        statusText.innerText = 'An error occurred.';
        toastBody.innerText = 'An error occurred.';
        uploadToast.show();
    } else {
        let currentProgress = progressBar.getAttribute('aria-valuenow');
        currentProgress = Math.min(90, parseInt(currentProgress) + 10);
        progressBar.style.width = currentProgress + '%';
        progressBar.setAttribute('aria-valuenow', currentProgress);
        progressBar.innerText = currentProgress + '%';

        statusText.innerText = data.step;
        setTimeout(() => checkStatus(taskId), 1000);
    }
}

const audio = document.getElementById('audio');
const words = document.querySelectorAll('#lyrics span');

audio.ontimeupdate = function() {
    const currentTime = audio.currentTime;
    words.forEach(word => {
        const start = parseFloat(word.dataset.start);
        const end = parseFloat(word.dataset.end);

        if (currentTime >= start && currentTime <= end) {
            word.classList.add('highlight');
        } else {
            word.classList.remove('highlight');
        }
    });
};
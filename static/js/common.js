function showToast(message) {
    const toastBody = document.getElementById('toast-body');
    const uploadToastElem = document.getElementById('uploadToast');
    if (!toastBody || !uploadToastElem) return;

    toastBody.innerText = message;
    const uploadToast = new bootstrap.Toast(uploadToastElem);
    uploadToast.show();
}
document.addEventListener('DOMContentLoaded', function() {
    const nav = document.getElementById('mainNav');
    if (!nav) return;

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });
});

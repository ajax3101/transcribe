document.addEventListener('DOMContentLoaded', function() {
    const audio = document.getElementById('audio');
    const words = document.querySelectorAll('#lyrics span');
    if (!audio || words.length === 0) return;

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
});

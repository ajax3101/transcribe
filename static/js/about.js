document.addEventListener('DOMContentLoaded', function() {
    const heading = document.querySelector('.animated-heading');
    const text = document.querySelector('.animated-text');
    const button = document.querySelector('.animated-button');

    if (heading) {
        heading.style.opacity = 0;
        heading.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            heading.style.opacity = 1;
            heading.style.transform = 'translateY(0)';
        }, 200);
    }

    if (text) {
        text.style.opacity = 0;
        text.style.transform = 'translateY(20px)';
        setTimeout(() => {
            text.style.opacity = 1;
            text.style.transform = 'translateY(0)';
        }, 600);
    }

    if (button) {
        button.style.opacity = 0;
        button.style.transform = 'scale(0.9)';
        setTimeout(() => {
            button.style.opacity = 1;
            button.style.transform = 'scale(1)';
        }, 1000);
    }
});
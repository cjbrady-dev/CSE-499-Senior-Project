function nextMedia(id) {
    const carousel = document.getElementById(id);
    const items = carousel.querySelectorAll('img, video');
    let currentIndex = Array.from(items).findIndex(el => el.classList.contains('active'));
    if (items.length === 0) return;
    items[currentIndex].classList.remove('active');
    const nextIndex = (currentIndex + 1) % items.length;
    items[nextIndex].classList.add('active');
    }

function prevMedia(id) {
    const carousel = document.getElementById(id);
    const items = carousel.querySelectorAll('img, video');
    let currentIndex = Array.from(items).findIndex(el => el.classList.contains('active'));
    if (items.length === 0) return;
    items[currentIndex].classList.remove('active');
    const prevIndex = (currentIndex - 1 + items.length) % items.length;
    items[prevIndex].classList.add('active');
    }

document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.querySelector('.carousel');
    const prevButton = document.getElementById('carousel-prev');
    const nextButton = document.getElementById('carousel-next');
    const itemWidth = 200; // Width of each item
    const itemMarginRight = 15; // Margin right of each item
    const scrollAmount = itemWidth + itemMarginRight; // Total scroll amount

    prevButton.addEventListener('click', () => {
        carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' }); // Scroll left
    });

    nextButton.addEventListener('click', () => {
        carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' }); // Scroll right
    });
});

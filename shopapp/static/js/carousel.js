document.addEventListener('DOMContentLoaded', () => {
    // Recommended Books Carousel
    setupCarousel(document.querySelector('#recommended-books .carousel'),
                  document.getElementById('carousel-prev'),
                  document.getElementById('carousel-next'));

    // Most Popular Books Carousel
    setupCarousel(document.querySelector('#most-popular-books .carousel'),
                  document.getElementById('most-popular-carousel-prev'),
                  document.getElementById('most-popular-carousel-next'));
});

function setupCarousel(carousel, prevButton, nextButton) {
    const itemWidth = 200; // Width of each item
    const itemMarginRight = 15; // Margin right of each item
    const scrollAmount = itemWidth + itemMarginRight; // Total scroll amount

    prevButton.addEventListener('click', () => {
        carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' }); // Scroll left
    });

    nextButton.addEventListener('click', () => {
        carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' }); // Scroll right
    });
}

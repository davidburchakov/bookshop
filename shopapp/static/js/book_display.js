document.addEventListener("DOMContentLoaded", function() {
    let pageNum = 1;
    let isLoading = false;  // Flag to prevent simultaneous loads

    function loadMoreBooks() {
        if (isLoading) return;  // Prevent multiple simultaneous requests

        isLoading = true;  // Set the flag
        pageNum++;
        fetch(`/index?page=${pageNum}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const htmlDocument = parser.parseFromString(data, "text/html");
            const newBooksList = htmlDocument.getElementById("books-list");

            if (newBooksList) {
                document.getElementById("books-list").innerHTML += newBooksList.innerHTML;
                isLoading = false;  // Reset the flag
            } else {
                console.log("No new books or error in response");
                window.removeEventListener('scroll', onScroll, {passive: true});
            }
        })
        .catch(error => {
            console.error('Error loading more books:', error);
            isLoading = false;  // Reset the flag in case of error
        });
    }

    function onScroll() {
        const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
        if (scrollTop + clientHeight > scrollHeight - 100 && !isLoading) {
            console.log("LOAD MORE BOOKS");
            loadMoreBooks();
        }
    }

    window.addEventListener('scroll', onScroll, {passive: true});
});

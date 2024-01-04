const sidebar = document.getElementById("sidebar");

    document.getElementById("hamburger-button").addEventListener("click", function() {
        if (sidebar.style.width === "400px") {
            sidebar.style.width = "0";
        } else {
            sidebar.style.width = "400px";
        }
    });

    document.getElementById("close-btn").addEventListener("click", function(){
        if (sidebar.style.width === "0"){
            sidebar.style.width = "400px";
        } else {
            sidebar.style.width = "0";
        }
    });

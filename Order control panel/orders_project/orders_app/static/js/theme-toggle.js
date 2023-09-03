$(document).ready(function() {
    const themeToggleBtn = $("#theme-toggle-btn");
    const body = $("body");
    const container = $(".container");
    const headings = $("h1, h2, h3");
    const footer = $("footer");

    // Get user's theme preference from local storage
    const userTheme = localStorage.getItem("userTheme");
    if (userTheme === "dark") {
        applyDarkTheme();
    }

    // Function to apply dark theme classes
    function applyDarkTheme() {
        body.addClass("dark-theme");
        container.addClass("dark-theme");
        headings.addClass("dark-theme");
        footer.addClass("dark-theme");
    }

    // Function to remove dark theme classes
    function removeDarkTheme() {
        body.removeClass("dark-theme");
        container.removeClass("dark-theme");
        headings.removeClass("dark-theme");
        footer.removeClass("dark-theme");
    }

    // Handle theme toggle button click
    themeToggleBtn.click(function() {
        if (body.hasClass("dark-theme")) {
            removeDarkTheme();
            localStorage.setItem("userTheme", "light");
        } else {
            applyDarkTheme();
            localStorage.setItem("userTheme", "dark");
        }

        // Send theme preference to the server
        $.ajax({
            type: "POST",
            url: "/update_theme_preference/",
            headers: {
                "X-CSRFToken": window.csrfToken
            },
            data: { theme_preference: localStorage.getItem("userTheme") },
            success: function(response) {
                console.log("Theme preference updated on the server");
            },
            error: function(error) {
                console.error("Error updating theme preference:", error);
            }
        });
    });
});

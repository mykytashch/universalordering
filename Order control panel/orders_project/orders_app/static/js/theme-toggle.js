$(document).ready(function() {
    $("#theme-toggle-btn").click(function() {
        var newTheme = $("body").hasClass("light-theme") ? "dark" : "light";
        var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            url: "/update_theme_preference/",
            data: {
                theme_preference: newTheme,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(data) {
                if (data.status === "success") {
                    console.log("Theme preference updated successfully.");
                    console.log("New theme class:", newTheme);
                    $("body").removeClass("light-theme dark-theme").addClass(newTheme);
                } else {
                    console.log("Failed to update theme preference.");
                }
            },
            error: function() {
                console.log("Error updating theme preference.");
            }
        });
    });

    var userThemePreference = "{{ request.user.userprofile.theme_preference }}";
    if (userThemePreference) {
        $("body").removeClass("light-theme dark-theme").addClass(userThemePreference);
    }
});

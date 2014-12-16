// index.js
$(document).ready(function() {
    $("form #submit.big-btn").click(function() {
        $(this).closest('form').submit();
    });
});

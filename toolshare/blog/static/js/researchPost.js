$(document).ready(function addRequest() {
    $.ajax({
        url: $('form').attr('action'),
        type: 'POST',
        data: $('form').serialize(),
        success: function (data) {
            alert("Works", data);
        },
        error: function (error) {
            alert("Didnt Work", error);
        },
    });
});
$(document).ready(function () {
    // catch the form's submit event
    $('#addTool').click(function () {
        // create an AJAX call
        $.ajax({
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: "{% url 'research' user.id %}",
            // on success
            success: function (response) {
                alert("Thank you for reaching us out " + response.tools);
            },
            // on error
            error: function (response) {
                // alert the error if any error occurred
                alert(response.responseJSON.errors);
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
})
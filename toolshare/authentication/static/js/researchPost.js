$.ajax({
    url: '/user/2/research/all-items/',  // Replace with your actual URL
    type: 'POST',  // Use 'POST' if needed
    dataType: 'json',  // Change based on your response type
    headers: {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function (response) {
        // Handle the response here
        console.log(response.message);
    },
    error: function (error) {
        // Handle any errors here
        console.error(error);
    }
});
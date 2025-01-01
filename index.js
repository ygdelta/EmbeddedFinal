$(document).ready(function() {
    setInterval(function() {
        $.ajax({
            url: 'http://127.0.0.1:5000/max30100',
            type: 'GET',
            success: function(response) {
                $('#heart_rate').text('Heart rate: ' + response.heart_rate);
                $('#spo2').text('SpO2: ' + response.spo2);
            }
        })
    }, 1000);
});
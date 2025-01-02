$(document).ready(function() {
  setInterval(() => {
    $.ajax({
      url: 'http://127.0.0.1:5000/max30100',
      type: 'GET',
      success: function(response) {
        $('#heart').text('Heart rate: ' + response.heart_rate);
        $('#spo2').text('SpO2: ' + response.spo2);
      }
    })
  }, 2000);

  setInterval(() => {
    $.ajax({
      url: 'http://127.0.0.1:5000/ds18b20',
      type: 'GET',
      success: function(res) {
        $('#temp').text('Temperature: ' + res.temperature);
      }
    });
  }, 2000);

  setInterval(() => {
    $.ajax({
      url: 'http://127.0.0.1:5000/mpu6050',
      type: 'GET',
      success: function(res) {
        let status = res.status;
        $('#state').text('State: ' + status);
        if ( status == 'danger' ) {
          window.alert('Dangerous situation detected!');
        }
        $('#accel').text('x:' + res.x + ', y: ' + res.y + ', z: ' + res.z);
      }
    });
  }, 2000);
});

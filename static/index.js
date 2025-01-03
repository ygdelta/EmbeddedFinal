$(document).ready(function() {
  setInterval(() => {
    $.ajax({
      url: 'http://127.0.0.1:5000/max30100',
      type: 'GET',
      success: (response) => {
        CheckBPM(response.heart_rate);
        CheckO2(response.spo2);
      },
      error: (err) => {
        $('#heart').text('Waiting');
        $('#spo2').text('None');
      }
    })
  }, 2000);

  setInterval(() => {
    $.ajax({
      url: 'http://127.0.0.1:5000/ds18b20',
      type: 'GET',
      success: (res) => {
        CheckTemp(res.temperature);
      },
      error: (err) => {
        $('#temp').text('None');
      }
    });
  }, 2000);

  setInterval(() => {
    $.ajax({
      url: 'http://127.0.0.1:5000/mpu6050',
      type: 'GET',
      success: function(res) {
        CheckState(res.status);
        $('#accel').text('x:' + res.x + ', y: ' + res.y + ', z: ' + res.z);
      },
      error: (err) => {
        $('#state').text('None');
      }
    });
  }, 2000);
});

let CheckBPM = (bpm) => {
  if ( bpm > 150 || bpm < 40 ) {
    $('#heart').css('color', 'red');
  }
  else {
    $('#heart').css('color', 'white');
  }
}

let CheckO2 = (spo2) => {
  if ( spo2 < 95 ) {
    $('#spo2').css('color', 'red');
  }
  else {
    $('#spo2').css('color', 'white');
  }
}

let CheckTemp = (temp) => {
  if ( temp < 35 || temp > 37.5 ) {
    $('#temp').css('color', 'red');
  }
  else {
    $('#temp').css('color', 'white');
  }
}

let CheckState = (state) => {
  $('#state').text(state);
  if ( state == 'danger' ) {
    window.alert('Dangerous situation detected!');
    $('#state').css('color', 'red');
  }
  else {
    $('#state').css('color', 'white');
  }
}
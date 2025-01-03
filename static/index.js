$(document).ready(() => {
  setInterval(() => {
    $.ajax({
      url: 'http://127.0.0.1:5000/max30100',
      type: 'GET',
      success: (response) => {
        heart = response.heart_rate;
        spo2 = response.spo2;
        CheckBPM(heart);
        CheckO2(spo2);
      },
      error: (err) => {
        $('#heart').text('Waiting');
        $('#spo2').text('None');
      }
    })
  }, 3000);

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
  }, 3000);

  setInterval(() => {
    $.ajax({
      url: 'http://127.0.0.1:5000/mpu6050',
      type: 'GET',
      success: function(res) {
        let res = res;
        CheckState(res.status);
        $('#accel').text('x:' + res.x + ', y: ' + res.y + ', z: ' + res.z);
      },
      error: (err) => {
        $('#state').text('None');
      }
    });
  }, 3000);

  let CheckBPM = (bpm) => {
    if ( !(typeof bpm === 'number') ) {
      $('#heart').text('Waiting');
      return;
    }
    if ( bpm > 150 || bpm < 40 ) {
      $('#heart').css('color', 'red');
    }
    else {
      $('#heart').css('color', 'white');
    }
  }

  let CheckO2 = (spo2) => {
    if ( !(typeof spo2 === 'number') ) {
      $('#spo2').text('Waiting');
      return;
    }
    if ( spo2 < 95 ) {
      $('#spo2').css('color', 'red');
    }
    else {
      $('#spo2').css('color', 'white');
    }
  }

  let CheckTemp = (temp) => {
    if ( !(typeof temp === 'number') ) {
      $('#temp').text('None');
      return;
    }
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
});


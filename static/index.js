$(document).ready(() => {

  let CheckBPM = (bpm) => {
    if ( !(typeof bpm === 'number') ) {
      $('#heart').text('Waiting');
      return;
    }
    $('#heart').text(bpm);
    if ( bpm > 150 || bpm < 40 ) {
      $('#heart').css('color', 'red');
    }
    else {
      $('#heart').css('color', 'white');
    }
  }

  $('#start').on('click', () => {
    start = true;
    Test();
    buttonState();
  });

  $('#stop').on('click', () => {
    start = false;
    Test();
    buttonState();
  });

  let buttonState = () => {
    $('#start').prop('disabled', start);
    $('#stop').prop('disabled', !start);
  }

  let CheckO2 = (spo2) => {
    if ( !(typeof spo2 === 'number') ) {
      $('#spo2').text('Waiting');
      return;
    }
    $('#spo2').text(spo2);
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
    $('#temp').text(temp);
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
  

  // Main
  let start = false;
  buttonState();
  let Test = () => {
    let interval = setInterval(() => {
      if ( !start ) {
        clearInterval(interval);
      }
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
      });

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

      $.ajax({
        url: 'http://127.0.0.1:5000/mpu6050',
        type: 'GET',
        success: function(res) {
          let tmp = res;
          CheckState(tmp.status);
          $('#accel').text('x:' + tmp.x + ', y: ' + tmp.y + ', z: ' + tmp.z);
        },
        error: (err) => {
          $('#state').text('None');
        }
      });
    }, 3000);
  }


});


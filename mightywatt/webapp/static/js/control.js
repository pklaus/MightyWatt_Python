
function warning(text) {
  if ($('#warning').length > 0) return;
  $('<div/>', {
      id: 'warning',
      class: 'alert alert-warning alert-dismissible',
      role: 'alert',
      text: 'Warning! ',
  })
  .append( $('<span/>', {id: 'warningText', 'text': text}) )
  .prepend(
    $('<button/>', {type: 'button', class: 'close', 'data-dismiss': 'alert', 'aria-label': 'Close'})
    .append($('<span/>', {'aria-hidden': 'true', html: '&times'}))
  ).appendTo('#messageArea');
}

function resetWarning() {
  $('#warning').remove();
}

function setProperties() {
  $.getJSON("/api/properties", function( data ) {
    $("#properties-maxIdac").text(data.maxIdac);
    $("#properties-boardRevision").text(data.BOARD_REVISION);
    $("#properties-fwVersion").text(data.FW_VERSION);
    $("#properties-maxIadc").text(data.maxIadc);
    $("#properties-maxTemperature").text(data.MAX_TEMPERATURE);
    $("#properties-minTemperature").text(data.MIN_TEMPERATURE);
    $("#properties-maxPower").text(data.MAX_POWER);
    $("#properties-dvmInputResistance").text(data.DVM_INPUT_RESISTANCE/1000. + 'k');
    $("#properties-maxVdac").text(data.maxVdac);
    $("#properties-maxVadc").text(data.maxVadc);
    $("#properties-temperatureThreshold").text(data.temperatureThreshold);
  })
  .fail(function() { warning('Cannot get device properties'); });
}

function updateStatus() {
  $.getJSON("/api/status", function( data ) {
    resetWarning();
    // voltage
    $("#voltage").text(data.voltage.toFixed(3));
    if (data.voltage > 0.9 && data.voltage < 26.) {
      $("#voltageWarning").addClass('label-warning');
      $("#voltageWarning").removeClass('label-danger');
      $("#voltageWarning").removeClass('invisible');
    } else if (data.voltage >= 26. ) {
      $("#voltageWarning").addClass('label-danger');
      $("#voltageWarning").removeClass('label-warning');
      $("#voltageWarning").removeClass('invisible');
    } else {
      $("#voltageWarning").addClass('invisible');
    }
    // current
    $("#current").text(data.current.toFixed(3));
    if (data.current > 0.01 && data.current < 8.) {
      $("#currentWarning").addClass('label-warning');
      $("#currentWarning").removeClass('label-danger');
      $("#currentWarning").removeClass('invisible');
    } else if (data.current >= 8.) {
      $("#currentWarning").addClass('label-danger');
      $("#currentWarning").removeClass('label-warning');
      $("#currentWarning").removeClass('invisible');
    } else {
      $("#currentWarning").addClass('invisible');
    }
    // power
    $("#power").text(data.power.toFixed(3));
    if (data.power > 0.01 && data.power < 50.) {
      $("#powerWarning").addClass('label-warning');
      $("#powerWarning").removeClass('label-danger');
      $("#powerWarning").removeClass('invisible');
    } else if (data.power >= 50.) {
      $("#powerWarning").addClass('label-danger');
      $("#powerWarning").removeClass('label-warning');
      $("#powerWarning").removeClass('invisible');
    } else {
      $("#powerWarning").addClass('invisible');
    }
    // resistance
    if (data.resistance > 100000)
      $("#resistance").text('' + data.resistance/1000 + 'k');
    else if (data.resistance > 1000)
      $("#resistance").text((data.resistance/1000).toPrecision(4) + 'k');
    else if (data.resistance < 1.0)
      $("#resistance").text(data.resistance.toFixed(3));
    else
      $("#resistance").text(data.resistance.toPrecision(4));
    if (data.resistance >= 1.0 && data.resistance < 10000) {
      $("#resistanceWarning").addClass('label-warning');
      $("#resistanceWarning").removeClass('label-danger');
      $("#resistanceWarning").removeClass('invisible');
    } else if (data.resistance < 1.) {
      $("#resistanceWarning").addClass('label-danger');
      $("#resistanceWarning").removeClass('label-warning');
      $("#resistanceWarning").removeClass('invisible');
    } else {
      $("#resistanceWarning").addClass('invisible');
    }
    // temperature
    $("#temperature").text(data.temperature);
    if (data.temperature > 70 && data.temperature < 100) {
      $("#temperatureWarning").addClass('label-warning');
      $("#temperatureWarning").removeClass('label-danger');
      $("#temperatureWarning").removeClass('invisible');
    } else if (data.voltage > 100. ) {
      $("#temperatureWarning").addClass('label-danger');
      $("#temperatureWarning").removeClass('label-warning');
      $("#temperatureWarning").removeClass('invisible');
    } else {
      $("#temperatureWarning").addClass('invisible');
    }
    // temperatureThreshold
    $("#temperatureThreshold").text(data.temperatureThreshold);
    if (! $("#threshold").is(":focus"))
      $("#threshold").val(data.temperatureThreshold);
    // remote / local voltage sensing
    if (data.remoteStatus != $('#remoteSensing')[0].checked) {
      if (data.remoteStatus)
        $('#remoteSensing')[0].checked = true;
      else
        $('#localSensing')[0].checked = true;
    }
  })
  .fail(function() { warning('Cannot get status update'); });
}

$('#stop').on('click', function (e) {
  $.getJSON("/api/stop", function( data ) {
  });
  updateStatus()
})

$(function() {
  // on page load

  change_mode('CC');

  updateStatus();

  setTimeout(function() {
    timedUpdate();
  }, 200);

  setProperties();
});

$(function ($) {
  $('.panel-heading span.clickable').on("click", function (e) {
    if ($(this).hasClass('panel-collapsed')) {
      // expand the panel
      $(this).parents('.panel').find('.panel-b').slideDown();
      $(this).removeClass('panel-collapsed');
      $(this).find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
    }
    else {
      // collapse the panel
      $(this).parents('.panel').find('.panel-b').slideUp();
      $(this).addClass('panel-collapsed');
      $(this).find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    }
  });
});

function timedUpdate() {
  updateStatus();
  setTimeout(function() {
    timedUpdate();
  }, 200);
}

$('#CC').on('click', function (e) {
  change_mode('CC');
})
$('#CV').on('click', function (e) {
  change_mode('CV');
})
$('#CP').on('click', function (e) {
  change_mode('CP');
})
$('#CR').on('click', function (e) {
  change_mode('CR');
})

function change_mode(mode) {
  $('#CC').removeClass('active');
  $('#CV').removeClass('active');
  $('#CP').removeClass('active');
  $('#CR').removeClass('active');
  $('#' + mode).addClass('active');
  $('#mode').val(mode);
  if(mode == 'CC') {
    $('#inputValueLabel').text('Constant current mode:');
    $('#inputValuePre').text('Current');
    $('#inputValuePost').text('A');
  } else if (mode == 'CV') {
    $('#inputValueLabel').text('Constant voltage mode:');
    $('#inputValuePre').text('Voltage');
    $('#inputValuePost').text('V');
  } else if (mode == 'CP') {
    $('#inputValueLabel').text('Constant power mode:');
    $('#inputValuePre').text('Power');
    $('#inputValuePost').text('W');
  } else if (mode == 'CR') {
    $('#inputValueLabel').text('Constant resistance mode:');
    $('#inputValuePre').text('Resistance');
    $('#inputValuePost').text('Ω');
  }
  $('#inputValue').val('');
  $('#inputValue').focus()
}


function sendNewThreshold(by) {
  var value = $('#threshold').val();
  $.getJSON("/api/temperature-threshold/" + value);
}
function changeThreshold(by) {
  $('#threshold').val(by + parseInt($('#threshold').val()));
  sendNewThreshold();
}
$('#thresholdMinus').on('click', function (e) {
  changeThreshold(-1);
});
$('#thresholdPlus').on('click', function (e) {
  changeThreshold(+1);
});

//$('#threshold').on('input', function() {
$('#threshold').blur(function() {
  sendNewThreshold();
});
$('form#setting').on('submit', function(e) {
  sendNewThreshold();
  e.preventDefault();
});
//$('#setMode').on('click', function (e) {
$('form#operationMode').on('submit', function(e) {
  var mode = $('#mode').val().toLowerCase();
  var value = $('#inputValue').val();
  if (value == '') {
    if (mode == 'cc' || mode == "cp") value = 0.0;
    if (mode == 'cv') value = 65.0;
    if (mode == 'cr') value = 1000000.0;
  }
  console.log('mode: ' + mode + ' value: ' + value);
  $.getJSON("/api/mode/" + mode + '/' + value);
  e.preventDefault();
});


$('input:radio').change( function(){
  if ($('#remoteSensing')[0].checked)
    $.getJSON("/api/voltage-sensing/remote");
  else
    $.getJSON("/api/voltage-sensing/local");
});          

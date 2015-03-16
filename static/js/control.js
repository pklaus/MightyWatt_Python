
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

function updateStatus() {
  $.getJSON("/api/status", function( data ) {
    resetWarning();
    // voltage
    $("#voltage").text(data.voltage.toFixed(3));
    if (data.voltage > 0.9 && data.voltage < 26.) {
        $("#voltageWarning").removeClass('hidden');
        $("#voltageDanger").addClass('hidden');
    } else if (data.voltage > 26. ) {
      $("#voltageWarning").addClass('hidden');
      $("#voltageDanger").removeClass('hidden');
    } else {
      $("#voltageWarning").addClass('hidden');
      $("#voltageDanger").addClass('hidden');
    }
    // current
    $("#current").text(data.current.toFixed(3));
    if (data.current > 0.01 && data.current < 8.) {
      $("#currentWarning").removeClass('hidden');
      $("#currentDanger").addClass('hidden');
    } else if (data.current > 8.) {
      $("#currentWarning").addClass('hidden');
      $("#currentDanger").removeClass('hidden');
    } else {
      $("#currentWarning").addClass('hidden');
      $("#currentDanger").addClass('hidden');
    }
    // temperature
    $("#temperature").text(data.temperature);
    if (data.temperature > 70 && data.temperature < 100) {
      $("#temperatureWarning").removeClass('hidden');
      $("#temperatureDanger").addClass('hidden');
    } else if (data.voltage > 100. ) {
      $("#temperatureWarning").addClass('hidden');
      $("#temperatureDanger").removeClass('hidden');
    } else {
      $("#temperatureWarning").addClass('hidden');
      $("#temperatureDanger").addClass('hidden');
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


//$('#setMode').on('click', function (e) {
$('form').on('submit', function(e) {
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

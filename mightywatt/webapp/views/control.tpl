<!DOCTYPE html>
<html lang="en">
  <head>
    <title>MightyWatt</title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/favicon.ico">

    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/css/control.css" rel="stylesheet">

  </head>
  <body>

    <!-- Main jumbotron for a primary marketing message or call to action -->
    <div class="jumbotron">
      <div class="container">
        <h1>MightyWatt Dashboard</h1>
      </div>
    </div>

    <div class="container">
      <div class="row">
        <div id="messageArea" class="col-md-12">
        </div>
      </div>
      <div class="row">

        <div class="col-md-4">
          <h3><span class="glyphicon glyphicon-dashboard" aria-hidden="true"></span> Status</h3>

            <div class="panel panel-default">
              <div class="panel-heading"><h4 class="panel-title">Live Monitor of the MightyWatt</h4></div>
              <table class="panel-table table table-condensed" id="liveMonitor">
                <tbody>
                  <tr>
                    <td>Voltage:</td>
                    <td class="numeric-cell">
                      <span id="voltage">0.000</span> V 
                      <span id="voltageWarning" class="warnung label invisible">
                        <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                      </span>
                    </td>
                    <td>Current:</td>
                    <td class="numeric-cell">
                      <span id="current">0.000</span> A 
                      <span id="currentWarning" class="warnung label invisible">
                        <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                      </span>
                    </td>
                  </tr><tr>
                    <td>Power:</td>
                    <td class="numeric-cell">
                      <span id="power">0.000</span> W 
                      <span id="powerWarning" class="warnung label invisible">
                        <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                      </span>
                    </td>
                    <td>Resistance:</td>
                    <td class="numeric-cell">
                      <span id="resistance">-</span> Ω 
                      <span id="resistanceWarning" class="warnung label invisible">
                        <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                      </span>
                    </td>
                  </tr><tr>
                    <td colspan="2">Temperature: <span id="temperature">-</span> °C 
                      <span id="temperatureWarning" class="warnung label invisible">
                        <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                      </span>
                    </td>
                    <td colspan="2">
                      (T<sub>Thresh</sub> = <span id="temperatureThreshold">-</span> °C)
                    </td>
                  </tr>

                </tbody>
              </table>

              <div class="panel-body">
                <button id="stop" type="button" class="btn btn-danger center-block">
                  <span class="glyphicon glyphicon-off" aria-hidden="true"></span>
                  Stop MightyWatt
                </button>
              </div>

            </div>


        </div>

        <div class="col-md-4">
          <h3><span class="glyphicon glyphicon-user" aria-hidden="true"></span> Manual Control</h3>

          <div class="panel panel-default">
            <div class="panel-heading">
              <h4 class="panel-title">Mode of Operation</h4>
            </div>
            <div class="panel-body">
              <form>
                <div class="text-center">
                  <div class="form-group btn-group" role="group">
                    <button id="CC" title="Constant Current" type="button" class="btn btn-primary btn-xl active">CC</button>
                    <button id="CV" title="Constant Voltage" type="button" class="btn btn-primary btn-xl">CV</button>
                    <button id="CP" title="Constant Power" type="button" class="btn btn-primary btn-xl">CP</button>
                    <button id="CR" title="Constant Resistance" type="button" class="btn btn-primary btn-xl">CR</button>
                  </div>
                </div>
                <input id="mode" type="text" class="hidden" value='CC'>
                <div class="form-group">
                  <label id="inputValueLabel" for="inputValue">Constant current mode:</label>
                  <div class="input-group">
                    <div id="inputValuePre" class="input-group-addon">Current</div>
                    <input id="inputValue" type="number" step="any" class="form-control" placeholder="0.000" autocomplete="off">
                    <div id="inputValuePost" class="input-group-addon">A</div>
                    <!-- <span class="input-group-btn">
                      <button id="setMode" type="submit" class="btn btn-warning" type="button">
                        <span class="glyphicon glyphicon-flash" aria-hidden="true"></span>
                        Set
                      </button>
                    </span> -->
                  </div>
                </div>
                <button id="setMode" type="submit" class="btn btn-warning center-block">
                  <span class="glyphicon glyphicon-flash" aria-hidden="true"></span>
                  Set Mode and Value
                </button>
              </form>
            </div>
          </div>

        </div>

        <div class="col-md-4">
          <h3><span class="glyphicon glyphicon-wrench" aria-hidden="true"></span> Settings and Tools</h3>

            <div class="panel panel-default">
              <div class="panel-heading">
                <h3 class="panel-title">Device Properties</h3>
                <span class="pull-right clickable panel-collapsed"><i class="glyphicon glyphicon-chevron-down"></i></span>
              </div>
              <div class="panel-b" style="display:none">
              <table class="panel-table table table-condensed" id="properties">
                <!-- <thead>
                  <tr><th>Properties</th><th>Properties</th></tr>
                </thead> -->
                <tbody>
                <tr><td><div>Board Revision: <span id="properties-boardRevision"></span></div></td>
                    <td><div>Firmware: v<span id="properties-fwVersion"></span></div></td></tr>
                <tr><td><div title="Maximum power that can be dissipated">P<sub>max</sub> = <span id="properties-maxPower"></span> W</div></td>
                    <td><div title="Input Resistance of the DVM"> R<sub>max</sub> = <span id="properties-dvmInputResistance"></span> Ω</div></td><td></td></tr>
                <tr class="hidden"><td><div title="Threshold temperature at wich the load will shut down">T<sub>Thresh</sub> = <span id="properties-temperatureThreshold"></span> °C</div></td></tr>
                <tr><td><div title="Minimum temperature to set as threshold">T<sub>Thresh,min</sub> = <span id="properties-minTemperature"></span> °C</div></td>
                    <td><div title="Maximum temperature to set as threshold">T<sub>Thresh,max</sub> = <span id="properties-maxTemperature"></span> °C</div></td></tr>
                <tr><td><div title="Maximum voltage measurable via the ADC">V<sub>ADC,max</sub> = <span id="properties-maxVadc"></span> V</div></td>
                    <td><div title="Maximum voltage settable via the DAC">V<sub>DAC,max</sub> = <span id="properties-maxVdac"></span> V</div></td></tr>
                <tr><td><div title="Maximum current measureable via the ADC">I<sub>ADC,max</sub> = <span id="properties-maxIadc"></span> A</div></td>
                    <td><div title="Maximum current settable via the DAC">I<sub>DAC,max</sub> = <span id="properties-maxIdac"></span> A</div></td></tr>
                </tbody>
              </table>
              </div>
            </div>

          <div class="panel panel-default">
            <div class="panel-heading">
              <h4 class="panel-title">Voltage Sensing</h4>
            </div>
            <div class="panel-body">
              <div class="text-center">
                <label class="radio-inline">
                  <input type="radio" name="voltageSensingOption" id="localSensing" value="local" checked> local
                </label>
                <label class="radio-inline">
                  <input type="radio" name="voltageSensingOption" id="remoteSensing" value="remote"> remote
                </label>
              </div>
            </div>
          </div>



        </div>


      </div> <!-- /row -->

      <hr>
      <footer>
        <p>&copy; Philipp Klaus 2015</p>
      </footer>
    </div> <!-- /container -->

    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/control.js"></script>
  </body>
</html>



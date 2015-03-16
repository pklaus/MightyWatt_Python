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
              <div class="panel-heading">Current status of the MightyWatt</div>
              <ul class="list-group">
                <li class="list-group-item">
                  Voltage: <span id="voltage">0.000</span> V
                  <span id="voltageWarning" class="label label-warning hidden">
                    <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                  </span>
                  <span id="voltageDanger" class="label label-danger hidden">
                    <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                  </span>
                </li>
                <li class="list-group-item">
                  Current: <span id="current">0.000</span> A
                  <span id="currentWarning" class="label label-warning hidden">
                    <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                  </span>
                  <span id="currentDanger" class="label label-danger hidden">
                    <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                  </span>
                </li>
                <li class="list-group-item">
                  Temperature: <span id="temperature">-</span> ℃ 
                  <span id="temperatureWarning" class="label label-warning hidden">
                    <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                  </span>
                  <span id="temperatureDanger" class="label label-danger hidden">
                    <span class="glyphicon glyphicon-alert" aria-hidden="true"></span>
                  </span>
                </li>
                <li class="list-group-item">
                  <button id="stop" type="button" class="btn btn-danger">
                    <span class="glyphicon glyphicon-off" aria-hidden="true"></span>
                    Stop MightyWatt
                  </button>
                </li>
              </ul>
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
                <div class="form-group btn-group" role="group">
                  <button id="CC" title="Constant Current" type="button" class="btn btn-primary btn-lg active">CC</button>
                  <button id="CV" title="Constant Voltage" type="button" class="btn btn-primary btn-lg">CV</button>
                  <button id="CP" title="Constant Power" type="button" class="btn btn-primary btn-lg">CP</button>
                  <button id="CR" title="Constant Resistance" type="button" class="btn btn-primary btn-lg">CR</button>
                </div>
                <input id="mode" type="text" class="hidden" value='CC'>
                <div class="form-group">
                  <label id="inputValueLabel" for="inputValue">Constant current mode:</label>
                  <div class="input-group">
                    <div id="inputValuePre" class="input-group-addon">Current</div>
                    <input id="inputValue" type="text" class="form-control" placeholder="0.000" autocomplete="off">
                    <div id="inputValuePost" class="input-group-addon">A</div>
                    <!-- <span class="input-group-btn">
                      <button id="setMode" type="submit" class="btn btn-warning" type="button">
                        <span class="glyphicon glyphicon-flash" aria-hidden="true"></span>
                        Set
                      </button>
                    </span> -->
                  </div>
                </div>
                <button id="setMode" type="submit" class="btn btn-warning">
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
              <h4 class="panel-title">Voltage Sensing</h4>
            </div>
            <div class="panel-body">
              <label class="radio-inline">
                <input type="radio" name="voltageSensingOption" id="localSensing" value="local" checked> local
              </label>
              <label class="radio-inline">
                <input type="radio" name="voltageSensingOption" id="remoteSensing" value="remote"> remote
              </label>
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



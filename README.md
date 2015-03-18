MightyWatt powered by Python
============================

This is a software suite to control the electronic load [MightyWatt][].


Installation
------------

Installing this Python package is as simple as:

    pip install https://github.com/pklaus/MightyWatt_Python/archive/master.zip

Starting the web server
-----------------------

Adapt the COM port of your MightyWatt hardware:

    mw_web_server /dev/ttyACM0

This will start a web server at <http://localhost:8001>.
The web page will look like this:

![screenshot of the web interface](./docs/web-screenshot.png)

You can stop the web server with Ctrl-C. (This might take a few seconds.)

The web server comes with the user interface shown above but it also provides
an API to control the MightyWatt with simple HTTP request:

To set constant current mode with 1.0 Amps:

    curl http://localhost:8001/api/mode/cc/1.0

To set remote voltage sensing:

    curl http://localhost:8001/api/voltage-sensing/remote

To stop the load:

    curl http://localhost:8001/api/stop

Controlling the load with the web client
----------------------------------------

With the web application and its API, you can run scripts
to script a program for the load. I also included a script
to do simple tasks such as ramping current etc.:

    mw_web_client \
      --watchdog 'V>0.5' \
      --remote \
      http://localhost:8001 \
      ramp CC 0 1.3 \
      --duration 600

This will ramp the current from 0 to 1.3 Amps in 600 seconds.
It will stop if the voltage drops below 0.5 Volts.
The Terminal output will look like the log files of the MightyWatt Windows software.

Using the Python module without the web server
----------------------------------------------

If you want to create scripts using the MightyWatt and don't want to
use the web server for some reason, you can also simply use the
MightyWatt object to controll the load programmatically:

```python
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Mighty Watt tool')
    parser.add_argument('serial_port', help='The serial port to connect to')
    parser.add_argument('--verbose', '-v', action='store_true', help='Generate verbose output')
    args = parser.parse_args()
    try:
        try:
            mw = MightyWatt(args.serial_port, verbose=args.verbose)
        except MightyWattCommunicationException:
            parser.error('An error occured, could not establish a connection to the device.')
        mw.print_status()
        mw.set_cc(1.00)
        mw.print_status()
        mw.set_update_rate(100)
        time.sleep(0.5)
        mw.print_status()
        time.sleep(0.5)
        mw.print_status()
        #mw.set_remote()
        mw.print_status()
        mw.set_cp(2.5)
        mw.print_status()
        mw.close()
    except KeyboardInterrupt:
        print("Pressed Ctrl-C. Exiting...")
    finally:
        try:
            mw.close()
        except:
            pass

if __name__ == "__main__":
    main()
```

[MightyWatt]: http://kaktuscircuits.blogspot.cz/2014/07/mightywatt-revison-2-now-50-mightier.html

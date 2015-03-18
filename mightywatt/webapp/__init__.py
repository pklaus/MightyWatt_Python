# -*- coding: utf-8 -*-

from bottle import Bottle, run, view, static_file, TEMPLATE_PATH
import os

# Find out where our resource files are located:
try:
    from pkg_resources import resource_filename, Requirement
    PATH = resource_filename("mightywatt", "webapp")
    #PATH = resource_filename(Requirement.parse("mightywatt"), "webapp")
except:
    PATH = './'

TEMPLATE_PATH.insert(0, os.path.join(PATH, 'views'))

def run_mwws(mw, *args, **kwargs):
    """
    Run the MightyWatt web server
    First argument is a MightyWatt instance
    """
    MW = mw
    api = Bottle()
    interface = Bottle()

    @api.get('/path')
    def status():
        return {'path': PATH}

    @api.get('/ms_since_last_update')
    def status():
        return {'ms_since_last_update': MW.ms_since_last_update}

    @api.get('/status')
    def status():
        return MW.status

    @api.get('/mode/cc/<current:float>')
    def set_cc(current):
        MW.set_cc(current)
        return {'success': True}

    @api.get('/mode/cv/<voltage:float>')
    def set_cv(voltage):
        MW.set_cv(voltage)
        return {'success': True}

    @api.get('/mode/cp/<power:float>')
    def set_cp(power):
        MW.set_cp(power)
        return {'success': True}

    @api.get('/mode/cr/<resistance:float>')
    def set_cr(resistance):
        MW.set_cr(resistance)
        return {'success': True}

    @api.get('/voltage-sensing/<mode>')
    def set_voltage_sensing(mode):
        assert mode in ['local', 'remote']
        MW.set_remote(mode == 'remote')
        return {'success': True}

    @api.get('/stop')
    def stop():
        MW.stop()
        return {'success': True}

    interface.mount('/api', api)

    @interface.get('/')
    @view('control')
    def index():
        return {}

    @interface.get('/static/<filename:path>')
    def serve_static(filename):
        return static_file(filename, root=os.path.join(PATH, 'static'))

    run(interface, *args, **kwargs)


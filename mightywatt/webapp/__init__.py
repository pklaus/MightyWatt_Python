# -*- coding: utf-8 -*-

from bottle import Bottle, view, static_file, TEMPLATE_PATH
import os

# Find out where our resource files are located:
try:
    from pkg_resources import resource_filename, Requirement
    PATH = resource_filename("mightywatt", "webapp")
    #PATH = resource_filename(Requirement.parse("mightywatt"), "webapp")
except:
    PATH = './'

TEMPLATE_PATH.insert(0, os.path.join(PATH, 'views'))

class MightyWattWebServerAPI(Bottle):
    def __init__(self, mw):
        """
        the MightyWatt web server
        First argument is a MightyWatt instance
        """
        #Bottle.__init__(self)
        super(MightyWattWebServerAPI, self).__init__()
        self.mw = mw
        self.route('/status',                     callback=self._status)
        self.route('/properties',                 callback=self._properties)
        self.route('/mode/cc/<current:float>',    callback=self._set_cc)
        self.route('/mode/cv/<voltage:float>',    callback=self._set_cv)
        self.route('/mode/cp/<power:float>',      callback=self._set_cp)
        self.route('/mode/cr/<resistance:float>', callback=self._set_cr)
        self.route('/voltage-sensing/<mode>',     callback=self._set_voltage_sensing)
        self.route('/temperature-threshold/<val:float>', callback=self._set_temperature_threshold)
        self.route('/stop',                       callback=self._stop)
        self.route('/ms_since_last_update',       callback=self._ms_since_last_update)

    def _status(self):
        return self.mw.status

    def _properties(self):
        return self.mw.properties

    def _set_cc(self, current):
        self.mw.set_cc(current)
        return {'success': True}

    def _set_cv(self, voltage):
        self.mw.set_cv(voltage)
        return {'success': True}

    def _set_cp(self, power):
        self.mw.set_cp(power)
        return {'success': True}

    def _set_cr(self, resistance):
        self.mw.set_cr(resistance)
        return {'success': True}

    def _set_voltage_sensing(self, mode):
        assert mode in ['local', 'remote']
        self.mw.set_remote(mode == 'remote')
        return {'success': True}

    def _set_temperature_threshold(self, val):
        self.mw.set_temperature_threshold(val)
        return {'success': True}

    def _stop(self):
        self.mw.stop()
        return {'success': True}

    def _ms_since_last_update(self):
        return {'ms_since_last_update': self.mw.ms_since_last_update}

class MightyWattWebServerInterface(Bottle):
    def __init__(self, mw):
        """
        the MightyWatt web server
        First argument is a MightyWatt instance
        """
        super(MightyWattWebServerInterface, self).__init__()
        self.mount('/api', MightyWattWebServerAPI(mw))
        self.route('/',                       callback = self._index)
        self.route('/static/<filename:path>', callback = self._serve_static)

    @view('control')
    def _index(self):
        return {}

    def _serve_static(self, filename):
        return static_file(filename, root=os.path.join(PATH, 'static'))


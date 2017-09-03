import ConfigParser
import httplib
import logging

class Util:
    """Util Class to help with all the annoying tasks."""

    def __init__(self, config_file=None):
        """Initilise the util class

        Read the configuraton file and setup logging. It uses some default
        values if no config file is present. Raises errors when things are
        not going as expeted'

        Keyword arguments:
        config_file -- the config file to use
        """
        #Create a config object and pass some defaults
        self.config = ConfigParser.RawConfigParser()
        try:
            self.config.readfp(open(config_file))
        except IOError:
            print ('Could not read specified configfile -> using default values')
            self.config.add_section('server')
            self.config.set('server', 'url', 'localhost')
            self.config.set('server', 'port', '8080')
            self.config.set('server', 'address', 'geoserver')
            self.config.add_section('logging')
            self.config.set('logging', 'filename', 'geoserver-python.log')
            self.config.set('logging', 'level', logging.INFO)
        else:
            if (not(self.config.has_section('server')
                    and self.config.has_option('server', 'url')
                    and self.config.has_option('server','port')
                    and self.config.has_option('server','address'))):
                print 'Config file is not complete! I need url, port and address in the server section!'
                raise ValueError('Config file is not complete.')
            if (not(self.config.has_section('logging')
                    and self.config.has_option('logging', 'filename')
                    and self.config.has_option('logging', 'level'))):
                print 'Config file not complete! I need a setup for logging!'
                raise ValueError('Config file is not complete.')

        self._url = self.config.get('server','url')
        self._port = self.config.get('server', 'port')
        self._address = self.config.get('server', 'address')

        logging.basicConfig(filename=self.config.get('logging','filename'), level=self.config.get('logging','level'))
        logging.info('Initialised Util class with settings')

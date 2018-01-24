import ConfigParser
import httplib
import logging

from base64 import b64encode

class Util:
    """Util Class to help with all the annoying tasks."""

    def __init__(self, config_file='settings.sfg'):
        """Initilise the util class

        Read the configuraton file and setup logging. It uses some default
        values if no config file is present. Raises errors when things are
        not going as expeted.

        Keyword arguments:
        config_file -- the config file to use
        """
        self.config = ConfigParser.RawConfigParser()
        self.check_config(config_file)

        self._url = self.config.get('server','url')
        self._port = self.config.get('server', 'port')
        self._address = self.config.get('server', 'address')
        self._auth = 'Basic {0}'.format(b64encode('{0}:{1}'.format(
                            self.config.get('server','user'),
                            self.config.get('server','pass'))))

        logging.basicConfig(filename=self.config.get('logging','filename'), \
                            level=self.config.get('logging','level'))
        logging.info('Initialised Util class with settings')
        logging.info('Using server: {0} at port {1} on {2}'.format(
                    self._address,
                    self._port,
                    self._url))

    def check_config(self, config_file):
    """Perform basic checks on the config file and set default if the key values
    are not present.
    """
        try:
            self.config.readfp(open(config_file))
        except IOError:
            print ('Could not read specified configfile -> using defaults')
            self.config.add_section('server')
            self.config.set('server', 'url', 'localhost')
            self.config.set('server', 'port', '8080')
            self.config.set('server', 'address', 'geoserver')
            self.config.set('server', 'user', 'admin')
            self.config.set('server','pass', 'geoserver')
            self.config.add_section('logging')
            self.config.set('logging', 'filename', 'geoserver-python.log')
            self.config.set('logging', 'level', logging.INFO)
        if (not(self.config.has_section('server')
                and self.config.has_option('server', 'url')
                and self.config.has_option('server','port')
                and self.config.has_option('server','address')
               )
           ):
            print 'Config file is not complete! I need url, ' + \
                  'port and address in the server section!'
            raise ValueError('Config file is not complete.')
        if (not(self.config.has_section('logging')
                and self.config.has_option('logging', 'filename')
                and self.config.has_option('logging', 'level')
               )
           ):
            print 'Config file not complete! I need a setup for logging!'
            raise ValueError('Config file is not complete.')


    def request(self, method, path, payload='', mime='text/xml'):
        """Perform http-request and get the response

        Keyword-arguments:
          method -- the http method to use
          path -- the path to send the request to
          payload -- the extra content to send
          mime -- mime-type

        Returns:
            HTTP statuscode, response as text
        """
        logging.debug('Sending request with method: {0} to path: {1}:{2}/{3}/{4}'.format(
                            method,
                            self._url,
                            self._port,
                            self._address,
                            path))
        headers = {}
        headers['Authorization'] = self._auth
        headers['Content-type'] = mime

        try:
            connection = httplib.HTTPConnection(
                    self._url,
                    self._port)
            connection.request(
                    method,
                    '/' + self._address + '/' + path,
                    payload,
                    headers)
            response = connection.getresponse()
            resp = response.read()
            logging.debug('Succeeded in getting response: {0}'.format(resp))
        except Exception as e:
            logging.error('Error with sending "{0}"-request to ' + \
                          '{1}:{2}/{3}/{4}. Get error: {5}'.format(method,
                                                        self._url,
                                                        self._port,
                                                        self._address,
                                                        path,
                                                        e))
            raise e
        finally:
            connection.close()
        return response.status, resp

def main():
    u = Util('settings.cfg')
    stat, response = u.request('get', 'test', None)
    print stat

if __name__ == '__main__':
    main()

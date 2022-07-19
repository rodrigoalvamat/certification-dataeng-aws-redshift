"""Defines a Config class to read the AWS configuration from dwh.cfg file.

Check the dwh.cfg.template file configuration sections and options.
"""
# sys libs
import os
# config libs
import configparser

# dwh.cfg file path
DIR = os.path.dirname(os.path.abspath(__file__)) 
INI_PATH = os.path.join(DIR, 'dwh.cfg')

class Config:
    """This class defines a wrapper for ConfigParser.

    Use the dwh.cfg.template file as a reference to configure
    the application according to your AWS account settings.

    Usage example:

    config = Config()
    config.get('REDSHIFT', 'USER')
    """

    def __init__(self):
        """Creates a Config object from dwh.cfg file.

        Config values will be UTF-8 encoded.
        """

        self.parser = configparser.ConfigParser()
        self.parser.read_file(open(INI_PATH, encoding='utf-8'))

    def get(self, section, option):
        """Reads a config option value from a section.

        Retrieves an option value pertaining to the given section
        from the dwh.cfg file.

        Args:
            secion: The dwh.cfg file section name.
              E.g. REDSHIFT
            option: The section config option name.
              E.g. PORT

        Returns:
            A value to the given section and option.
            For example:

            value = config.get('REDSHIFT', 'PORT')
        """
        return self.parser.get(section, option)

"""Defines a Config class to read the AWS configuration from aws.ini file.

Check the aws.ini.template file configuration sections and options.
"""

# config libs
import configparser


class Config:
    """This class defines a wrapper for ConfigParser.

    Use the aws.ini.template file as a reference to configure
    the application according to your AWS account settings.

    Usage example:

    config = Config()
    config.get('REDSHIFT', 'USER')
    """

    def __init__(self):
        """Creates a Config object from aws.ini file.

        Config values will be UTF-8 encoded.
        """

        self.parser = configparser.ConfigParser()
        self.parser.read_file(open('aws.ini', encoding='utf-8'))

    def get(self, section, option):
        """Reads a config option value from a section.

        Retrieves an option value pertaining to the given section
        from the aws.ini file.

        Args:
            secion: The aws.ini file section name.
              E.g. REDSHIFT
            option: The section config option name.
              E.g. PORT

        Returns:
            A value to the given section and option.
            For example:

            value = config.get('REDSHIFT', 'PORT')
        """
        return self.parser.get(section, option)

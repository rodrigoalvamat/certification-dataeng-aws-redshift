"""Defines a Connection class that uses Psycopg2 adapter
or the AWS Redshift connector API.

The Redshift connector was used because the Psycopg2
driver was crashing unexpectedly most of the time.
The Psycopg2 adapter was kept as default to satisfy the projetc requirements.
"""

# config libs
from config import Config
# connector libs
import psycopg2
import redshift_connector


class Connection:
    """This class defines a wrapper for Pycopg2 and
    Redshift connector API Connection classes.

    Both connectors will get their configuration parameters
    from the Config wrapper.

    Usage example:

    connection = Config(redshift=True)
    """

    def __init__(self, redshift=False):
        """Creates a Connection object according to the client selection.

        Args:
            redshift: If True uses the Redshift connector API,
                otherwise use the default Psycopg2 adapter.
        """
        config = Config()
        if redshift:
            self.connection = redshift_connector.connect(
                region=config.get('AWS', 'REGION'),
                host=config.get('REDSHIFT', 'ENDPOINT'),
                port=int(config.get('REDSHIFT', 'PORT')),
                database=config.get('REDSHIFT', 'DATABASE'),
                user=config.get('REDSHIFT', 'USER'),
                password=config.get('REDSHIFT', 'PASSWORD'))
        else:
            self.connection = psycopg2.connect(
                host=config.get('REDSHIFT', 'ENDPOINT'),
                port=config.get('REDSHIFT', 'PORT'),
                dbname=config.get('REDSHIFT', 'DATABASE'),
                user=config.get('REDSHIFT', 'USER'),
                password=config.get('REDSHIFT', 'PASSWORD'))

        self.cursor = self.connection.cursor()

    def close(self):
        """Closes the adapter connection immediately."""
        self.connection.close()

    def commit(self):
        """Commit any pending transaction to the database."""
        self.connection.commit()

    def execute(self, query, commit=False):
        """Execute a database operation (query or command).

        Args:
            query: If True uses the Redshift connector API,
                otherwise use the default Psycopg2 adapter.
            commit: If True Commit the transaction to the database
                otherwise leave it pending.
                
        Returns:
            The method returns None.

            If a query was executed, the returned values can be retrieved
            using the corresponding cursor fetch*() methods.
        """
        result = self.cursor.execute(query)
        if commit:
            self.commit()

        return result

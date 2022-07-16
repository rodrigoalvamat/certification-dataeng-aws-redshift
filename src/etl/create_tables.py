"""Defines a SchemaPipeline class to drop and create the Redshift tables."""

# sys libs
import argparse
from timeit import default_timer as timer
# SQL libs
from connection import Connection
from sql_queries import CREATE_TABLE_QUERIES, DROP_TABLE_QUERIES


class SchemaPipeline:
    """This class defines the Redshift table schema pipeline.

    Code usage example with default pyscopg2 connection:

    connection = Connection()
    pipeline = SchemaPipeline(connection)
    pipeline.run()

    Usage example as python script with redshift connection:

    python -m create_tables --redshift
    """

    def __init__(self, connection):
        """Creates the SchemaPipeline object and sets the connection.

        Args:
            connection: The connection adapter wrapper.
        """
        self.connection = connection

    def create(self):
        """Executes all CREATE_TABLE_QUERIES statements."""
        for query in CREATE_TABLE_QUERIES:
            self.connection.execute(query, commit=True)

    def drop(self):
        """Executes all DROP_TABLE_QUERIES statements."""
        for query in DROP_TABLE_QUERIES:
            self.connection.execute(query, commit=True)

    def run(self):
        """Execute all pipeline phases and print time statistics."""

        print('-----------------------------------------------------')
        print('AWS Redshift Schema Pipeline')
        print('-----------------------------------------------------')

        # PHASE 1: drop the database tables
        print('INFO: Droping the database tables...')
        start = timer()

        self.drop()

        drop_time = timer() - start
        print('INFO: Database tables droped.')

        # PHASE 2: create the database schema
        print('INFO: Creating the database schema...')
        start = timer()

        self.create()

        create_time = timer() - start
        print('INFO: Database schema created.')

        # STATS: print the time statistics
        print('-----------------------------------------------------')
        print('Time Statistics')
        print('-----------------------------------------------------')
        print(f'Drop tables time: {round(drop_time, 2)} seconds')
        print(f'Create tables time: {round(create_time, 2)} seconds')


def main(redshift):
    """The create_tables.py script entry point.

    Args:
        redshift: If True uses the Redshift connector API,
            otherwise use the default Psycopg2 adapter.
    """
    # sets the connection
    connection = Connection(redshift=redshift)

    # run the pipeline
    pipeline = SchemaPipeline(connection)
    pipeline.run()
    connection.close()


if __name__ == '__main__':
    # create the command line parser
    parser = argparse.ArgumentParser(
        description='AWS Redshift Schema Pipeline')

    # set the command line arguments
    parser.add_argument('--redshift',
                        help='Set the redshift connector - default: pyscopg2',
                        type=bool,
                        default=False)

    # parse the command line arguments
    args = parser.parse_args()

    # run the pipeline
    main(args.redshift)

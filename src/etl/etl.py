"""Defines the ETLPipeline class to load staging tables
and insert data into the Redshift Data Warehouse tables."""

# sys libs
import argparse
from timeit import default_timer as timer
# SQL libs
from connection import Connection
from sql_queries import COPY_TABLE_QUERIES, INSERT_TABLE_QUERIES


class ETLPipeline:
    """This class defines the Redshift ETL pipeline.

    Code usage example with default pyscopg2 connection:

    connection = Connection()
    pipeline = ETLPipeline(connection)
    pipeline.run()

    Usage example as python script with redshift connection:

    python -m etl --redshift
    """

    def __init__(self, connection):
        """Creates the ETLPipeline object and sets the connection.

        Args:
            connection: The connection adapter wrapper.
        """
        self.connection = connection

    def load(self):
        """Executes all COPY_TABLE_QUERIES statements."""
        for query in COPY_TABLE_QUERIES:
            self.connection.execute(query, commit=True)

    def insert(self):
        """Executes all INSERT_TABLE_QUERIES statements."""
        for query in INSERT_TABLE_QUERIES:
            self.connection.execute(query, commit=True)

    def run(self):
        """Execute all pipeline phases and print time statistics."""

        print('-----------------------------------------------------')
        print('AWS Redshift ETL Pipeline')
        print('-----------------------------------------------------')

        # PHASE 1: Extract from S3 and load into staging tables
        print('INFO: Loading S3 data into staging tables...')
        start = timer()

        self.load()

        load_time = timer() - start
        print('INFO: Staging tables loaded.')

        # PHASE 3: Insert transformed data into DW tables
        print('INFO: Inserting data into DW tables...')
        start = timer()
        self.insert()
        insert_time = timer() - start
        print('INFO: DW tables loaded.')

        # STATS: print the time statistics
        print('-----------------------------------------------------')
        print('Time Statistics')
        print('-----------------------------------------------------')
        print(f'Staging tables time: {round(load_time, 2)} seconds')
        print(f'Insert tables time: {round(insert_time, 2)} seconds')


def main(redshift):
    """The etl.py script entry point.

    Args:
        redshift: If True uses the Redshift connector API,
            otherwise use the default Psycopg2 adapter.
    """
    # sets the connection
    connection = Connection(redshift=redshift)

    # run the pipeline
    pipeline = ETLPipeline(connection)
    pipeline.run()
    connection.close()


if __name__ == "__main__":
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

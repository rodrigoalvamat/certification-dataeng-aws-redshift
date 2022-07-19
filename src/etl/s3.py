"""Defines the AWS S3Loader class to read json files from buckets."""

# sys libs
import io
# AWS libs
import boto3
# data libs
import json
import pandas as pd


class S3Loader:
    """This class defines the AWS S3 file loader.

    Usage example:

    loader = S3Loader()
    """

    def __init__(self, config):
        """Creates the S3Loader object to read json files from buckets.

        Args:
            config: The aws.ini config file wrapper object.
        """
        self.client = self.__create_cliente(config)
        self.resource = self.__create_resource(config)

    def __create_cliente(self, config):
        """Initilizes the AWS S3 client object from boto3 library.

        Args:
            config: The aws.ini config file wrapper object.

        Returns:
            The boto3 S3 client object.
        """
        return boto3.client('s3',
                            region_name=config.get(
                                'AWS', 'REGION'),
                            aws_access_key_id=config.get(
                                'AWS', 'KEY'),
                            aws_secret_access_key=config.get(
                                'AWS', 'SECRET')
                            )

    def __create_resource(self, config):
        """Initilizes the AWS S3 resource object from boto3 library.

        Args:
            config: The aws.ini config file wrapper object.

        Returns:
            The boto3 S3 resource object.
        """
        return boto3.resource('s3',
                              region_name=config.get('AWS', 'REGION'),
                              aws_access_key_id=config.get(
                                  'AWS', 'KEY'),
                              aws_secret_access_key=config.get(
                                  'AWS', 'SECRET'))

    def load_data(self, bucket_path, file_count=1):
        """Loads all json files from an S3 bucket.

        Args:
            bucket_path: The S3 bucket folder path.
            file_count: The number of json files to load.

        Returns:
            A pandas DataFrame object containing
            the data of all json files.
        """
        # get the bucket path and resource object
        path = bucket_path.split('/')
        bucket = self.resource.Bucket(path[2])

        # initialize counter and data frame array
        count = 0
        data_frames = []

        # filter bucket objects starting with 'bucket-folder' and iterate
        for obj in bucket.objects.filter(Prefix=path[3]):

            # stop when reaching max 'count' files
            if count == file_count:
                break

            # read json to a data frame and append it to array
            if obj.key.endswith('.json'):
                body = io.BytesIO(obj.get()['Body'].read())
                data = pd.read_json(body, lines=True)
                data_frames.append(data)
                count += 1

        # concatenate all json data frames
        return pd.concat(data_frames, ignore_index=True)

    def load_path(self, bucket_path):
        """Load one json file from an S3 bucket.

        Args:
            bucket_path: The S3 bucket file path.

        Returns:
            A pandas DataFrame object containing
            the data of the json file.
        """
        path = bucket_path.split('/')

        obj = self.client.get_object(Bucket=path[2], Key=path[3])
        data = json.loads(obj['Body'].read().decode('utf-8'))

        return data

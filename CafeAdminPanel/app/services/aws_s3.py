import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class S3Manager:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
        self.s3 = boto3.client('s3',
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               region_name=region_name)  # This without keys will auto use ~/.aws/credentials config
        self.region_name = region_name

    def create_bucket(self, bucket_name, region=None):
        try:
            if region is None:
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                self.s3.create_bucket(Bucket=bucket_name,
                                      CreateBucketConfiguration={'LocationConstraint': region})
            print(f'Bucket {bucket_name} created successfully.')
        except ClientError as e:
            print(f'Error creating bucket: {e}')

    def create_folder(self, bucket_name, folder_name):
        if not folder_name.endswith('/'):
            folder_name += '/'
        try:
            self.s3.put_object(Bucket=bucket_name, Key=folder_name)
            print(f'Folder {folder_name} created successfully in bucket {bucket_name}.')
        except ClientError as e:
            print(f'Error creating folder: {e}')

    def upload_file(self, file_name, bucket_name, object_name=None, public_read=False):
        if object_name is None:
            object_name = file_name
        try:
            extra_args = {'ACL': 'public-read'} if public_read else {}
            self.s3.upload_file(file_name, bucket_name, object_name, ExtraArgs=extra_args)
            print(f'File {file_name} uploaded successfully to bucket {bucket_name} as {object_name}.')
            if public_read:
                public_url = self.get_public_url(bucket_name, object_name)
                print(f'File is publicly accessible at {public_url}')
                return public_url
        except NoCredentialsError:
            print('Credentials not available.')
        except ClientError as e:
            print(f'Error uploading file: {e}')
            return None

    def download_file(self, bucket_name, object_name, file_name=None):
        if file_name is None:
            file_name = object_name
        try:
            self.s3.download_file(bucket_name, object_name, file_name)
            print(f'File {object_name} downloaded successfully from bucket {bucket_name} to {file_name}.')
        except NoCredentialsError:
            print('Credentials not available.')
        except ClientError as e:
            print(f'Error downloading file: {e}')

    def list_files(self, bucket_name, prefix=''):
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            res = []
            if 'Contents' in response:
                for item in response['Contents']:
                    print(item['Key'])
                    res.append(item["Key"])
            else:
                print('No files found.')

            return res
        except ClientError as e:
            print(f'Error listing files: {e}')

    def get_public_url(self, bucket_name, object_name):
        try:
            public_url = f'https://{bucket_name}.s3.{self.region_name}.amazonaws.com/{object_name}'
            return public_url
        except Exception as e:
            print(f'Error generating public URL: {e}')
            return None

    def delete_object(self, bucket_name, object_key):
        self.s3.delete_object(Bucket=bucket_name, Key=object_key)

        return f"Deleted {object_key} from {bucket_name}"


s3_manager = S3Manager(aws_access_key_id='AKIAYIMIJP47IG5P7WFF',
                       aws_secret_access_key='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',
                       region_name='us-east-1') # This without keys will auto use ~/.aws/credentials config


# print(s3_manager.get_public_url('pubsfiles', 'pubsimages/style.css'))

# s3_manager.create_bucket('pubsfiles')
# s3_manager.create_folder('pubsfiles', 'pubsimages')


# s3_manager.upload_file('/home/samvel/Downloads/style.css', 'pubsfiles', 'pubsimages/style.css', public_read=True)  #  public_read=True
# s3_manager.upload_file('/home/samvel/Pictures/Screenshots/671-673.png', 'pubsfiles', 'pubsimages/671-673.png', public_read=True)

# print(s3_manager.get_public_url('pubsfiles', 'pubsimages/671-673.png'))



# s3_manager.download_file('pubsfiles', 'my-folder/myfile.txt', 'path/to/downloaded_file.txt')
# r = s3_manager.list_files('pubsfiles', 'pubsimages/')
# print(r)

import boto3
import botocore
from contracts import StorageContract

class S3StorageProvider(StorageContract):

    def __init__(self):
        if self.client == None:
            self.client = boto3.client('s3')

        if self.s3 == None:
            self.s3 = boto3.resouce('s3')

    def path_splitter(path):
        """Returns the bucket and key from corresponding S3 path /<bucket>/<key>
        
        Arguments:
            path {string} -- path of an S3 object like /<bucket>/<key>
        """
        return path.split('/')[0], '/'.join(path.split('/'))

    def put(self, location, contents):
        """Puts a file into an S3 bucket at the specified location

        Arguments:
            location {string} -- e.g. /<bucket>/<key>
            contents {string | object | file-like object} -- The file object to add
        """
         
        key, bucket = path_splitter(location)
        self.client.put_object(Body=contents, Key=key, Bucket=bucket)

    def get(self, location):
        key, bucket = path_splitter(location)
        response = self.client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()

    def delete(self, location):
        key, bucket = path_splitter(location)
        response = self.client.delete_object(Bucket=bucket, Key=key)
        return response['DeleteMarker']

    def exists(self, location):
        key, bucket = path_splitter(location)
        try:
            s3.Object(bucket, key).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return false
            else:
                raise
        else:
            return true

    def url(self, location):
        return "s3:/" + location
    
    def size(self, location):
        """ Returns the object size in KB
        """
        key, bucket = path_splitter(location)
        obj = s3.Object(bucket, key)
        return obj.content_lenth / 1024 



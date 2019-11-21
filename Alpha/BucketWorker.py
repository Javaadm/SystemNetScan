import os
import boto3

class bucketWorker:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def download_file(self, download_to, download_from, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
            if bucket_name is None:
                raise(Exception("bucket_name have not been provided"))
        with open(download_to, 'wb') as f:
            self.s3.download_fileobj(bucket_name, download_from, f)

    def upload_file(self):
        pass

# for bucket in s3.buckets.all():
#     print(bucket.name)
# print()
# bucket = s3.Bucket('ltd-krp')
# for bo in bucket.objects.all():
#     print(bo)
# path='documents/847723c20d040ad90c3e917a3a6aeec9.png'
# bucket_name = 'ltd-krp'
# s3 = boto3.client('s3')
# with open('input.png', 'wb') as f:
#     s3.download_fileobj(bucket_name, path, f)

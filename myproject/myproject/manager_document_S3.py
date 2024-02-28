import os, boto3
from botocore.config import Config
from botocore.exceptions import ClientError


class DocumentsManagerS3:

    def __init__(self, proposta, name=None, *args, **kwargs):
        self._s3_client = self._get_s3_client()
        # self._s3_client = boto3.client('s3', endpoint_url=AWS_S3_ENDPOINT_URL)
        self.proposta = proposta
        self.oficio_document = self._get_documents_s3_keys(name=name)
        self.bucket = AWS_STORAGE_BUCKET_NAME

    @staticmethod
    def _get_s3_client():
        return boto3.client(
            "s3",
            region_name="us-east-1",
            config=Config(s3={"addressing_style": "path"}, signature_version="s3v4"),
        )

    def _get_documents_s3_keys(self, name):
        filename = name if name else self.proposta.oficio.file.name
        return {"file": "media/" + filename}

    def create_documents_presigned_urls(self, expiration=900):
        if "TEST_ENV" in os.environ and os.environ["TEST_ENV"] == "true":
            return {"url": "url_teste"}
        try:
            document_url = self.create_presigned_url(
                self.oficio_document.get("file"), expiration
            )
            document = {
                "url": document_url,
            }
        except ClientError as error:
            pass

        return document

    def create_presigned_url(self, file, expiration=900):
        try:
            presigned_url = self._s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": file},
                ExpiresIn=expiration,
            )
            return presigned_url

        except ClientError as error:
            raise ""


import os
import boto3
from botocore.exceptions import NoCredentialsError


class DocumentsManagerCnabS3:

    def __init__(self, *args, **kwargs):
        bucket = os.environ.get("DJANGO_AWS_STORAGE_BUCKET_NAME")
        self.bucket = bucket  # Assuming this variable is defined
        self._s3_client = self._get_s3_client()

    @staticmethod
    def _get_s3_client():

        access_key = os.environ.get("TESTE_AWS_ACCESS_KEY_ID")
        secret_key = os.environ.get("TESTE_AWS_SECRET_ACCESS_KEY")

        return boto3.client(
            "s3",
            region_name="us-east-1",  # Set your desired region
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(s3={"addressing_style": "path"}, signature_version="s3v4"),
        )

    def upload_file_to_s3(self, local_file_path, s3_key):
        try:
            self._s3_client.upload_file(local_file_path, self.bucket, s3_key)
            return True
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return False

    # Added method to delete a file from S3
    def delete_file_from_s3(self, s3_key):
        try:
            self._s3_client.delete_object(Bucket=self.bucket, Key=s3_key)
            print(f"File deleted from S3: {s3_key}")
            return True
        except ClientError as e:
            print(f"Error deleting file from S3: {e}")
            return False

    # Added method to create a folder in S3
    def create_folder_in_s3(self, folder_name):
        try:
            # Add a trailing slash to indicate it's a folder
            folder_key = f"{folder_name}/"
            self._s3_client.put_object(Bucket=self.bucket, Key=folder_key)
            print(f"Folder created in S3: {folder_key}")
            return True
        except ClientError as e:
            print(f"Error creating folder in S3: {e}")
            return False

    # Added method to check if a file exists in S3
    def file_exists_in_s3(self, s3_key):
        try:
            self._s3_client.head_object(Bucket=self.bucket, Key=s3_key)
            print(f"File exists in S3: {s3_key}")
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print(f"File not found in S3: {s3_key}")
                return False
            else:
                print(f"Error checking file existence in S3: {e}")
                return False

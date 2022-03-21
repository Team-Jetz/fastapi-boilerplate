import boto3
from settings.config import S3_STORAGE

class S3Storage():
    def upload_image(image, filename):
        s3 = boto3.resource(
            "s3",
            region_name=S3_STORAGE['REGION'],
            endpoint_url=f'https://{S3_STORAGE["HOST_NAME"]}/',
            aws_access_key_id=S3_STORAGE["ACCESS_KEY"],
            aws_secret_access_key=S3_STORAGE["SECRET_KEY"]
        )

        bucket = s3.Bucket(S3_STORAGE["BUCKET_NAME"])
        bucket.upload_fileobj(image.file, f'images/{filename}', ExtraArgs={"ACL": "public-read"})
        uploaded_file_url = f"https://{S3_STORAGE['BUCKET_NAME']}.{S3_STORAGE['HOST_NAME']}/images/{filename}"

        return uploaded_file_url

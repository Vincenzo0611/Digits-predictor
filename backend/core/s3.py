import boto3
import os
import uuid


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET = os.getenv("AWS_BUCKET_NAME")


def upload_image(
    file_bytes,
    filename
):

    key = f"images/{uuid.uuid4()}-{filename}"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=file_bytes,
        ContentType="image/png"
    )

    return f"https://{BUCKET}.s3.amazonaws.com/{key}"


def delete_image(image_url):

    prefix = f"https://{BUCKET}.s3.amazonaws.com/"

    key = image_url.replace(
        prefix,
        ""
    )

    s3.delete_object(
        Bucket=BUCKET,
        Key=key
    )
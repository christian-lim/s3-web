import boto3
from botocore.exceptions import ClientError

import os, os.path

current_dir = os.getcwd()
css_dir = "/css"
entries_dir = "/entries"
resources_dir ="/resources"
include_files = ["./surface.html", "./error.html"]
bucket = "thechristianlim.com"

s3_client = boto3.client("s3")

def resolve_path(dir_name):
    sub_files = []
    for path, dirs, files in os.walk(current_dir + dir_name):
        for file in files:
            sub_files.append(os.path.join("." + dir_name + "/" + file))
    print("Sub files for {}: {}".format(dir_name, sub_files))
    return sub_files

# Default content-type is octet/stream. Surprised this isn't resolved on AWS's end with the file type.
def resolve_content_type(file_name):
    prefix = file_name.split("/")[1]
    if (prefix == "css"):
        content_type = "text/css"
    elif (prefix == "resources"):
        content_type = "application/pdf"
    else:
        content_type = "text.html"
    return content_type

def upload_to_s3():
    upload_files = resolve_path(css_dir) + resolve_path(entries_dir) + resolve_path(resources_dir) + include_files
    try:
        for file in upload_files:
            print("Uploading {} to S3".format(file))
            object_key = file.strip("./")
            content_type = resolve_content_type(file)

            s3_response = s3_client.upload_file(file, bucket, object_key, ExtraArgs={'ContentType': content_type})
            print("Upload for {} successful at {}/{}".format(file, bucket, object_key))
    except ClientError as ex:
        print("ERROR: Uploading file {} failed.".format(file, ex))

if __name__ == "__main__":
    upload_to_s3()
    
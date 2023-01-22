# %%
import boto3

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id='',
    aws_secret_access_key='')
# %%
import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Set up the S3 bucket and file name
bucket_name = 'image-upload-py'
file_name = 'star.png'

# Upload the file to S3
s3.upload_file(file_name, bucket_name, file_name)

# %%
img_path = "https://upload-computer.s3.amazonaws.com/star.png?AWSAccessKeyId=AKIA3KY5TMIS6SKGQBJG&Expires=1674402144&Signature=XchdM8QC2IcdDl2nQ90zL2cgq18%3D"
# write a function to shorten the url
from google.cloud import storage
import gpt_2_simple as gpt2

import os
import datetime

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f'File {source_file_name} uploaded to {destination_blob_name}.')

# Load model

print("Loading gpt2 session..")
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)

# Generate text

temperature = float(os.getenv('TEMPERATURE'))

print("Generating article..")
article_list = gpt2.generate(sess, return_as_list=True, temperature=temperature)
article = "".join(article_list)

# Upload text to bucket

bucket_name = os.getenv('ML_ARTICLES_BUCKET')
datetime_now = f"{datetime.datetime.now():%Y%m%d_%H%M%S}"
article_name = f"news_{datetime_now}.txt"
bucket_prefix = 'news'

file = open(article_name,"w")
file.write(article)
file.close()

destination_blob_name = f"{bucket_prefix}/{article_name}"
print(f"Uploading {article_name} to bucket {bucket_name} as {destination_blob_name} ...")
upload_blob(bucket_name,article_name,destination_blob_name)

print("Done.")

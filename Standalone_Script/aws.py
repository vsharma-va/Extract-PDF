import boto3
from botocore.exceptions import ClientError
import json


class Aws:
    def __init__(
        self, file_path: str, bucket_name: str, file_name: str, file_extension: str
    ) -> None:
        self.file_path = file_path
        self.bucket_name = bucket_name
        self.file_name = file_name
        self.file_extension = file_extension
        self.s3_client = boto3.client("s3")
        self.lambda_client = boto3.client("lambda", region_name="ap-south-1")

    def check_and_upload(self):
        # checking if the file with the same name exists
        try:
            # returns ClientError if the file doesn't exist
            self.s3_client.head_object(
                Bucket=self.bucket_name, Key=f"{self.file_name}.{self.file_extension}"
            )
            print("File already exists")
        except ClientError as e:
            s3_client = boto3.client("s3")
            s3_client.upload_file(
                self.file_path,
                self.bucket_name,
                f"{self.file_name}.{self.file_extension}",
            )
            print("File uploaded successfully")

    def get_analyzed_data(self) -> dict:
        lambda_payload = {
            "bucket_name": self.bucket_name,
            "file_name": f"{self.file_name}.{self.file_extension}",
        }
        response = self.lambda_client.invoke(
            FunctionName="textract",
            InvocationType="RequestResponse",
            Payload=json.dumps(lambda_payload),
        )
        sanitized_response = json.loads(response["Payload"].read())
        return self.write_json_to_file(sanitized_response["body"])

    def write_json_to_file(self, response):
        file_name = f"{self.file_name}_textract_raw"
        file_extension = "json"
        file_path = f"./output/json/{file_name}.{file_extension}"
        with open(file_path, "w") as file:
            json.dump(response, file)
        file.close()
        something = None
        with open(file_path, "r") as file:
            something = json.load(file)
        file.close()
        file_path = file_path.replace("_raw", "")
        with open(file_path, "w") as file:
            json.dump(json.loads(something), file)
        file.close()
        return {
            "file_name": file_name,
            "file_extension": file_extension,
            "file_path": file_path,
        }

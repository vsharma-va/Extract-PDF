import json
import boto3


def lambda_handler(event, context):
    file_name = event["file_name"]
    bucket_name = event["bucket_name"]
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={
            "S3Object": {
                "Bucket": bucket_name,
                "Name": file_name,
            }
        },
        FeatureTypes=["FORMS", "TABLES"],
    )

    # TODO implement
    return {"statusCode": 200, "body": json.dumps(response)}

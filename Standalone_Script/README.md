# Standalone Script

## Requirements ->
All dependencies are listed in requirements.txt file

## Additional Dependencies ->
Download [poppler-utils](https://blog.alivate.com.au/poppler-windows/) and place them in the root directory of Standalone_Script

## Aws requirements ->
Download AWS CLI and set it up to be able to use Boto3

![image](https://github.com/vsharma-va/Extract-PDF/assets/78730763/d56ed898-eac5-48a7-a2c0-a87457ad55ea)

## Flow ->
* ### preprocessor.py -
    * When the script is launched a file dialog box is opened. You can select any pdf or image file you want
    * If a pdf file is selected it is first converted into an image because during testing I found that AWS Textract gives better results with images
    * The converted image is stored in ./assets/converted/
    * Information about the file be it image or converted image is returned by get_file_info() function
* ### aws.py -
    * The image file is then uploaded to s3 bucket
    * Then a request to lambda function is sent which selects the uploaded file from the bucket and passes it to AWS Textract to analyze
    * After analyzing the lambda function returns a JSON containing the result
* ### parser_aws.py - 
    * The returned data is parsed by this class to determine relationships and write them to a csv file
    * Detailed info about the relationships are present in the parser_aws.py file
    * **results are stored in the ./output/csv/ directory**


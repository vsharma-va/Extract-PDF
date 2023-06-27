from preprocessor import Preprocessor
from aws import Aws
from parser_aws import ParserAws
import csv

def write_dict_to_csv(final_map: dict, json_file_info: dict):
    with open(f'./output/csv/{json_file_info["file_name"]}.csv', "a") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in final_map.items():
            writer.writerow([key, value])

preprocessor = Preprocessor()
file_info = preprocessor.get_file_info()
aws = Aws(
    file_path=file_info["file_path"],
    file_extension=file_info["file_extension"],
    file_name=file_info["file_name"],
    bucket_name="textract-console-ap-south-1-ef56ab6d-8a1b-4a79-ad4f-218bba3f410",
)
aws.check_and_upload()
json_file_info = aws.get_analyzed_data()
# json_file_info = {
#     'file_path': './output/json/sample1_textract.json',
#     'file_name': 'sample1_textract.json',
#     'file_extension': 'json',
# }
parser = ParserAws(json_file_info)
final_map = parser.parse_response_for_key_value_pair()
parser.parse_response_for_tables()
write_dict_to_csv(final_map, json_file_info)
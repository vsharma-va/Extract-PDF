from flask import Flask, request
from flask_cors import CORS
from flask import send_file
from helper.preprocessor import Preprocessor
from helper.aws import Aws
from helper.parser_aws import ParserAws
import configparser

app = Flask(__name__)
config_parser = configparser.ConfigParser()
config_parser.read('./aws.config')
app.config['SECRET_KEY'] = config_parser['FLASK']['SecretKey']

CORS(app)

@app.route("/upload", methods=["POST"])
def upload_received_file():
  csv_file_info = run_script(request.files['pdffile'])
  return send_file(
    f"./helper/output/csv/{csv_file_info['file_name']}.csv", as_attachment=True, download_name="sample1"
  )
  
def run_script(something):
  processor = Preprocessor(something)
  file_info = processor.get_file_info()
  aws = Aws(
    file_path=file_info["file_path"],
    file_extension=file_info["file_extension"],
    file_name=file_info["file_name"],
    bucket_name= config_parser['AWS']['BucketName'],
  )
  aws.check_and_upload()
  json_file_info = aws.get_analyzed_data()
  parser = ParserAws(json_file_info)
  parser.parse_response_for_tables()
  parser.parse_response_for_key_value_pair(json_file_info)
  return json_file_info
  
  
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
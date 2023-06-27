# WebApp

## Run Flask Server->
All python dependencies are listed in requirements.txt file
After installing all the dependencies assuming you are in WebApp Folder run the following commands
``` 
cd flask
```
```python
python main.py
```

## Run Vue Server ->
Assuming you are in WebApp Folder run the following commands
```
cd "Data Extractor"
```
```
npm install
npm run dev
```

## Flow ->
* ## Backend ->
    * Backend flow is same as Standalone_Script
    * The only new function is the upload endpoint
    * Receives a FileObject and sends it to the script
* ## Frontend ->
    * You can drag and drop files into the yellow box or click on browse to select a file
    * Click on upload after selecting the desired file
    * After uploading and performing backend task you will be automatically redirected to /tableview where you will be shown the representation of table and the key value pairs that were extracted
    


https://github.com/vsharma-va/Extract-PDF/assets/78730763/e91fb771-f5de-41e2-8df3-299c9bde79ef


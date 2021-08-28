# File web uploader


Simple web server for file uploads. It supports instant copying of uploaded files to a remote server with a similar container if "SERVER_PAIR" is used in docker-compose file

You can upload files via web form or using any web POST utility like this one:
```
curl -X POST -F 'directory_field=somedir' -F 'upload_file=@./somefile' localhost
```
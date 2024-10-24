# Homework task for GROUP-IB
### Dependencies 
* Flask
* SQLAlchemy

### Quick startup guide 
1. Rise the server `./rise_server.sh`
2. Rise the client `./rise_client.sh`
3. Upload data file (in `.json` format) with `curl -X POST -F 'file=@/path/to/your/file.json' http://localhost:5002/upload-data`
4. Get and store data in DB `curl http://localhost:5002/fetch-and-store`

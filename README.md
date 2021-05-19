# A pretty useless API

<img src="/extra/ScreenShot.png" alt="Swagger editor"/>

### Get Started

Clone the project, set up virtual environment, and install the dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To download 1000 random facts from [Random Useless Facts](https://uselessfacts.jsph.pl/) run:
```
python3 -m fact_processor
```

Then, to start the Flask webserver, run:
```
export FLASK_APP=webapp
flask run -h localhost -p 8080
```

Finally, to check the API go to [Swagger Editor](https://editor.swagger.io/) and paste the content of the [swagger.yaml](https://raw.githubusercontent.com/tunalagoona/unuseful-api/main/swagger.yaml) file.  
Use the following credentials to authorize: `user = 'admin', password = 'QWxhZGRpb'`

Available endpoints:
```
/status
/facts
/facts/<fact_id>
# you can specify lang query parameter to get the response in the specified language, for example: lang=ru
```

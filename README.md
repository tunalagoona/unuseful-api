# unuseful-api
A pretty useless API


<img src="/extra/ScreenShot.png" alt="Swagger editor"/>

### Get Started

Clone the project, set up virtual environment, and install the dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

1. To download 1000 random facts from [Random Useless Facts](https://uselessfacts.jsph.pl/), run:
```
python3 -m fact_processor
```

2. Then, to start the Flask webserver, run:
```
export FLASK_APP=webapp
flask run -h localhost -p 8080
```

3. Finally, to run the API from Swagger Editor, go to [Swagger Editor](https://editor.swagger.io/) and past the content of the swagger.yaml file to the console.  

Use the following credentials to authorize: `user = 'admin', password = 'QWxhZGRpb'`


Available endpoints:
```
/status
/facts
/facts/<fact_id>
# you can specify lang query parameter to get the response in the specified language
# for example, http://localhost:8080/facts/0160a21a-a0f0-4ad7-923a-41ad1d0ace0e?lang=ru
```

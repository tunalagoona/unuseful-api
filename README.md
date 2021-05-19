# unuseful-api
A pretty useless API


<img src="/extra/ScreenShot.png" alt="Swagger editor"/>

### Get Started

Fork the directory and install the dependencies:
```
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

3. To test the API from the browser, enter http://localhost:8080 with the following credentials: `user = 'admin', password = 'QWxhZGRpb'`    

   
   Available endpoints:
```
/status
/facts
/facts/<fact_id>
# you can also specify lang query parameter to get the response in the desired language
# for example, http://localhost:8080/facts/0160a21a-a0f0-4ad7-923a-41ad1d0ace0e?lang=ru
```


4. Finally, to run the API from Swagger Editor, go to [Swagger Editor](https://editor.swagger.io/) and past the content of the swagger.yaml file to the console.



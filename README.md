## Capitol Query Example queries

To run the docker container simply run in terminal:
```bash
$ docker-compose up -d
```
Then browse to http://localhost:8080 to see the app in action.

It is easier to debug the project if you run it in flask instead of docker:
```bash
$ python app.py
```
And make sure to select database engine in database.py depending
on whether you are running the app using docker of flask.

####Here are some helpful commands:
####Docker Commands:

Run docker:
```bash
$ docker-compose up -d
```

Find current docker process running:
```bash
$ docker ps
```

Kill current docker process:
```bash
$ docker kill <CONTAINER ID>
```


####Sqlite3 Commands:
Start sqlite3 interpreter:
```bash
$ sqlite3
```
Open database file:
```bash
$ .open cq_small.sqlite
```

View all tables:
```bash
$ .table
```

View specific table schema:
```bash
$ .schema <table_name>
```




# Myze Backend

To set up the project:
```sh

python3 -m venv venv

```

To activate the virtual environment:
```sh

source venv/bin/activate

```

To install packages:
```sh

pip install -r requirements.txt

```

Then, have DynamoDB running in the background.

To initialize the tables in the database:
```sh

FLASK_APP=myze_service FLASK_ENV=development flask init-db

```

To start the app:
```sh

FLASK_APP=myze_service FLASK_ENV=development flask run

```

To deactivate the virtual environment:
```sh

deactivate

```

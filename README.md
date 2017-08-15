# Books email search

## Installation

```
sudo apt-get install mongodb redis
git clone https://github.com/vaniakov/book_email_search.git book_search
cd book_search
python3 -m virtualenv .book_search
source .book_search/bin/activate
pip install -r requirements.txt
```

## MongoDB Configuration

```
$> sudo service mongodb start
$> mongo
> use books_db
switched to db books_db
> db.createUser(
 {
    user: "django_books",
    pwd: "secret",
    roles:
    [
        {
            role:"readWrite",
            db: "books_db"
        }
    ]
 }
 )
```

## Books export
Application provides manage.py script to export pdf files from external source to database.
The required name convention for exported pdf file is:
```
Author name - Book name - year.pdf
```
To export books just type:
```
python manage.py export_books <source_directory>
```

## Email backend

By default emails sent from the app will be stored at:
```
BASE_DIR/tmp/email-messages/
```

## Run daemons
```
sudo service mongodb start
sudo service redis start
celery -A book_search worker -l info &
```

## Run DEV server
```
python manage.py runserver
```


# news_aggregator_django
A simple Django news aggregator app python

A news aggregator to allow you to aggregate news from a list of different blog feeds using
the feedparser library



## Installation


* `$ virtualenv -p /usr/bin/python3 virtualenv`
* `$ source virtualenv/bin/activate`
* `$ pip install -r requirements.txt`

* `$ cd aggregator`
* `$ python manage.py migrate`
* `$ python manage.py runserver`

## Running

* `$ cd aggregator`
* `$ python manage.py runserver`

## Running Test

* `$ cd aggregator`
* `$ python manage.py test`

## Adding Feeds

* append a `/feed` to your blog domain you want to add to your feed list.
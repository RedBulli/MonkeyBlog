MonkeyBlog
==========
Requirements
------------
* [PostgreSQL 9.3](http://www.postgresql.org/download/)
* [python 2.7](http://www.python.org/download/releases/2.7/)
* [pip](http://www.pip-installer.org/en/latest/)

Development
-----------
```bash
pip install -r requirements-dev.txt
createdb monkeyblog
createdb monkeyblog_test
python manage.py syncdb
```
Run tests
-------
```bash
py.test
```
Running server
-------
```bash
python manage.py runserver
```

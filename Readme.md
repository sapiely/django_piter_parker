# Django shop

## Build

The first thing to do is to clone the repository:

```bash
$ git clone https://github.com/DDonts/django_piter_parker.git
$ cd django_piter_parker
```

Find ```.env.dev``` file in route directory and set another variables if it necessary (there's testing data by default)

### Docker-compose

```bash
$ docker-compose build
$ docker-compose up
```

### Pure Django
```bash
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```


## Fixtures
If you want you can load prepared test models from fixture ```data.json```

### Docker
```bash
$ docker-compose exec web python manage.py loaddata data.json
```
### Pure Django
```bash
$ python manage.py loaddata data.json
```


## Testing
### Docker
```bash
$ docker-compose exec web pytest
```
### Pure Django
```bash
$ pytest
```


## Some routes for your consideration
### Login/obtaining API token
```
POST: http://127.0.0.1:8000/api/obtain-auth-token/
{
    "username": "username",
    "password": "password"
}
```

### Main API
Authenticated users only. Header Authorization: Token {your_token}
```
GET: http://127.0.0.1:8000/api/organizations/?district_id=1
GET: http://127.0.0.1:8000/api/organizations/1/?price=max
GET: http://127.0.0.1:8000/api/organizations/1/?category=Something
GET: http://127.0.0.1:8000/api/organizations/?category=Something else&price=max&district_id=1

GET: http://127.0.0.1:8000/api/organizations/1/

POST: http://127.0.0.1:8000/api/products/

GET: http://127.0.0.1:8000/api/products/1/
```

[![Build Status](https://circleci.com/gh/thiagoferreiraw/mixapp.svg?style=shield&circle-token=48a42b6925295d37ceb93b42d29f1c28a40eb4ab)](https://circleci.com/gh/thiagoferreiraw/mixapp/)
# Brigid Mixs

Brigid Mixs' platform.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6
- Django Web
- Postgres
- Virtual env wrapper
- Facebook APP
- Google maps api key

### Installing

- Clone this repository;
- Create a postgres instance on docker:
```
docker run -d --name djangoweb --net host -e POSTGRES_PASSWORD=root postgres
```
- Create the following environment variables:
```
$ export SOCIAL_AUTH_FACEBOOK_KEY="YOU_APP_KEY"
$ export SOCIAL_AUTH_FACEBOOK_SECRET="YOU_APP_SECRET"
$ export TOKEN_GOOGLE_PLACES_API="YOUR_KEY"
```
- Run `make setup` to install the dependencies
- Run `make migrate` to apply the models on database
- Run `python manage.py loaddata test_data` to load the initial database
- Run `make run` to start the application; default user is: [admin, 123]

All set! The application will be on at localhost:8000

## Running the tests

Run `make tests`

## Built With

* Django Web
* Postgres

## Contributing

Contact us!

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Thiago Ferreira ** - *Backend, Frontend* - [Github](https://github.com/thiagoferreiraw)
* **Felipe Souza ** - *Backend* - [Github](https://github.com/fnscoder)
* **Raian De Andrades ** - *Frontend* - [Github](https://github.com/RaianAndrades)
* **Vinícius Souza ** - *Frontend* - [Github](https://github.com/euvinisouza)

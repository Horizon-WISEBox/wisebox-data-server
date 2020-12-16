# WISEBox Data Server

Data upload server for
[WISEBox Logger](https://github.com/Horizon-WISEBox/wisebox-logger) logfiles.

## Getting Started

### Dependencies

The recommended method for running wisebox-data-server is with
[Docker](https://www.docker.com/) and
[Docker Compose](https://docs.docker.com/compose/).

### Installing

* Clone the repository
* Create a `.env` file and set the following environment variables:
  * COMPOSE_PROJECT_NAME
  * DJANGO_ADMIN_USER
  * DJANGO_ADMIN_EMAIL
  * DJANGO_ADMIN_PASSWORD
  * DJANGO_DEBUG
  * DJANGO_LANGUAGE_CODE
  * DJANGO_SECRET_KEY
  * DJANGO_SITE_NAME
  * POSTGRES_PASSWORD
* Create a docker-compose.override.yml with your local settings (e.g. ports)

### Executing program

```
docker-compose up
```

## Version History

* v1.2.0
  * WISEParks renamed to WISEBox
  * See [commit change](https://github.com/Horizon-WISEBox/wisebox-data-server/commit/b0e3934)
* v1.1.1
  * Relate Location to Organisation
  * See [commit change](https://github.com/Horizon-WISEBox/wisebox-data-server/commit/602a62d)
* v1.1.0
  * Support Device sessions
  * See [commit change](https://github.com/Horizon-WISEBox/wisebox-data-server/commit/97ddc76)
* v1.0.1
  * Add transactions to upload views
  * See [commit change](https://github.com/Horizon-WISEBox/wisebox-data-server/commit/162caa9)
* v1.0.0
  * Add logfile versioning
  * See [commit change](https://github.com/Horizon-WISEBox/wisebox-data-server/commit/b129348)

## License

This project is licensed under the GNU Affero General Public License, Version 3
\- see the [LICENSE](LICENSE) file for details

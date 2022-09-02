# AttorneyTech API ![version](https://img.shields.io/badge/version-v1-blue) [![openapi](https://img.shields.io/badge/openapi-3-green.svg)](./openapi.yaml)

This api is used to provide users to create and get the information of cases in the law firm.
API definition is contained in the [OpenAPI specification](./openapi.yaml).

***

## Getting Started

### Prerequisites

1. This API uses the packages of Python as below:

    | Package Name | Version |
    | :----------- | :------ |
    | Flask | 2.2.2 |
    | Flask-RESTful | 0.3.9 |
    | marshmallow | 3.17.0 |
    | psycopg2 | 2.9.3 |

2. Installing the packages with the [requirements.txt](./requirements.txt) file.

    ```shell
    $ pip install -r requirements.txt
    ```

3. Copy [config-example.json](./common/config-example.json) to `common/config.json`. If necessary, modify it according to your needs and being careful to avoid committing sensitive data.

## Getting data source from the PostgreSQL Database

The following instructions show you how to connect the API to a PostgreSQL database.

1. Install PostgreSQL on local or on docker according to your needs, you can follow this [guide](/attorneytech-database/README.md) to complete your installation.

2. Define the part of `common/config.json` to be like:

    ```json
    {
        "database":{
            "port": "port",
            "db_host": "hostname",
            "db_name": "postgres",
            "db_username": "username",
            "db_password": "password",
            "poolmin": 5,
            "poolmax": 20
        }
    }
    ```

    | JSON key | Description |
    | :----------- | :------ |
    | port | Your postgreSQL port |
    | db_host | Your postgreSQL host |
    | db_name | Your database name |
    | db_username | Your PostgreSQL username |
    | db_password | Your PostgreSQL user password |
    | poolmin | The minimum number of connections a connection pool maintains, even when there is no activity to the target database |
    | poolmax | The maximum number of connections that can be open in the connection pool |

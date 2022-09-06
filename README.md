# AttorneyTech API ![version](https://img.shields.io/badge/version-v1-blue) [![openapi](https://img.shields.io/badge/openapi-3-green.svg)](./openapi.yaml)

This api is used to provide users to create and get the information of cases in the law firm.
API definition is contained in the [OpenAPI specification](./openapi.yaml).

***

## Getting Started

### Prerequisites

1. Installing the packages with the [requirements.txt](./requirements.txt) file.

    ```shell
    $ pip install -r requirements.txt
    ```

2. Copy [config-example.json](config-example.json) to the root of your project folder. If necessary, modify it according to your needs and being careful to avoid committing sensitive data.

## Getting data source from the PostgreSQL Database

The following instructions show you how to connect the API to a PostgreSQL database.

1. Install PostgreSQL on local or on docker according to your needs, you can follow this [guide](/attorneytech-database/README.md) to complete your installation.

2. Define the part of `config.json` to be like:

    ```json
    {
        "database": {
            "port": "port",
            "host": "hostname",
            "db_name": "postgres",
            "username": "username",
            "password": "password",
            "poolmin": 5,
            "poolmax": 20
        }
    ```

    | JSON key | Description |
    | :----------- | :------ |
    | port | Your postgreSQL port |
    | host | Your postgreSQL host |
    | db_name | Your database name |
    | username | Your PostgreSQL username |
    | password | Your PostgreSQL user password |
    | poolmin | The minimum number of connections a connection pool maintains, even when there is no activity to the target database |
    | poolmax | The maximum number of connections that can be open in the connection pool |

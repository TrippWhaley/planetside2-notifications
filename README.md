# PlanetSide 2 Notifications
Discord notifications for alerts from PlanetSide 2 Census API

## Setup

1. Create a `.env` file

    ```sh
    cp .env.example .env
    ```

    Add your Discord webhook to `.env`

1. Run

    ```sh
    python3 main.py
    ```

    Alternatively, if you have Docker installed and would like to run this script indefinitely:

    ```sh
    ./run.sh
    ```

## Formatting/Linting

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Testing

heh
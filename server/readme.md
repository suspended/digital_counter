# Backend Server for Digital Counter

## Requirements
1. python 3.7
1. docker
1. docker-compose
1. You can install other requirements via the requirements.txt
1. Ports 5000,5432,5555 will be used so make sure they are empty

## Running for development
1. Start postgres and pgadmin container using
    ```bash
    # edit mount location in run_db.sh first
    # you can remove the -v line if you do not need to persist data
    bash run_db.sh
    bash run_db_viewer.sh
    ```
2. Run development server with
    ```
    bash run_dev.sh
    ```

## Running for production
1. Duplicate `docker-compose-sample.env` and rename the new file `docker-compose.env`
1. Edit the values in `docker-compose.env`. This file is in `.gitignore` and should not be committed for security reasons 
1. Build the required containers using
    ```bash
    docker-compose build
    ```
1. Run all containers using
    ```bash
    docker-compose up -d
    ```
1. To stop all containers, use
    ```bash
    docker-compose down
    ```


## Creating Super User
This should be done immediately after starting a new database. Only one super user can be created. Super user credentials are required for updating the latest count as well as updating the threshold. Refer to the api for instruction on how to do this.

## Creating Locations
Do create location records before trying to update counter or threshold. Creating location will require Super User credentials

## Available Endpoints
Below are the available endpoints.
- [] refers to request body form data values
- <> refers to response variables in json format
- \*authorization required\* will require adding header to the request packet {'Authorization': 'Bearer \<access-token-here\>'}

For more information, you can refer to `app/routes` to view these endpoints

```python
# Create super user
POST /create_super_user
[username]
[password]

# Login
POST /login
[username]
[password]
<access_token>
<expire_in_seconds>

# Create location
PUT /location
*authorization required*
[name]
<id>
<name>
<ok_limit>
<warning_limit>

# Get location
GET /location
<id>
<name>
<ok_limit>
<warning_limit>

# Get all location latest count
GET /location/get_latest_count
<id>
<name>
<ok_limit>
<warning_limit>
<count>
<last_updated>

# Update counter
POST /location/update_counter
*authorization required*
[id]
[count]
<count>
<last_updated>


# Update threshold
POST /location/update_threshold
*authorization required*
[id]
[ok_limit]
[warning_limit]
<ok_limit>
<warning_limit>
```


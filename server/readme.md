# Backend Server for Digital Counter

### Requirements
1. python 3.7
1. You can install other requirements via the requirements.txt

### Running for development
1. Create database via:
    ```
    flask upgrade
    ```
1. database file is located in `app/app.db`
1. Run development server using
    ```
    bash run_dev.sh
    ```
### Running for Production
1. Start postgres and pgadmin container using
    ```
    bash run_db.sh
    bash run_db_viewer.sh
    ```
2. Run gunicorn server with
    ```
    bash run.sh
    ```

### Creating Super User
This should be done immediately after starting a new database. Only one super user can be created. Super user credentials are required for updating the latest count as well as updating the threshold. Refer to the api for instruction on how to do this.

### Available Endpoints
Below are the available endpoints.
- [] refers to request body form data values
- <> refers to response variables in json format
- \*authorization required\* will require adding header to the request packet {'Auhorization': 'Bearer \<access-token-here\>'}

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

# Get latest count
GET /get_counter
<count>
<last_updated>

# Update counter
POST /update_counter
*authorization required*
[count]
<count>
<last_updated>

# Get threshold
GET /get_threshold
<ok_limit>
<warning_limit>

# Update threshold
POST /update_threshold
*authorization required*
[ok_limit]
[warning_limit]
<ok_limit>
<warning_limit>
```


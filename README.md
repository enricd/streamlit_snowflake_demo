# Intro to Streamlit and Connection to a Snowflake Database

## Barcelona Snowflake User Group April 2025 Meetup

----

### Prerequisites: 

- Python installed

- Optionally (but recommended) to have the `uv` Python manager installed: [Link](https://docs.astral.sh/uv/getting-started/installation/) (better if you install it with the uv installer for your OS, not with pip)

    ```bash
    uv --version  # check that is correctly installed

    uv python install 3.12   # install Python with the desired version

    uv sync  # install the projects libraries
    ```

- Otherwise, install the depencies with pip:

    ```bash
    pip install streamlit numpy pandas snowflake-connector-python snowflake-snowpark-python
    ```

- A Snowflake account and database with some data (you can use the free trial account for 30 days)  


----

### 1. Hello world app (hello.py):

```bash
uv run streamlit run hello.py

# or

streamlit run hello.py  # if you are not using uv
```

### 2. Basic Snowflake connection and queries demo (basic_snowflake_app.py):

You will need to create the folder and file `.streamlit/secrets.toml` (include it in the .gitignore) to provide the secrets and configs for the Snowflake database connection.

```yaml
# Change this file name to secrets.toml and adapt the values with your own

[connections.snowflake]
account = "<org>-<account>"
user = "<user>"
password = "<password>"
role = "ACCOUNTADMIN"
warehouse = "COMPUTE_WH"
database = "BICING"
schema = "BICING_SCHEMA"
```

```bash
uv run streamlit run basic_snowflake_app.py
```

### 3. More complex example allowing to adapt the query from the UI, visualizing data charts and simulating an ML model real time inference from loaded data (snowflake_app.py):

```bash
uv run streamlit run snowflake_app.py
```

----

You will also find the ppt from my presentation in the repo.

I hope you will find it interesting! 

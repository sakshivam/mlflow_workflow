# mlflow_workflow

# MLflow Tracking

MLflow is an open source platform for managing the end-to-end machine learning lifecycle.

It has the following primary components:

    Tracking:       record experiments to compare parameters and results.
    Models:         manage and deploy models from a variety of ML libraries to a variety of model serving and inference platforms.
    Projects:       package ML code in a reproducible form to share with other data scientists or transfer to production.
    Model Registry: Allows you to centralize a model store for managing models’ full lifecycle stage transitions: from staging to production, with capabilities for versioning and annotating.
    Model Serving:  Allows you to host MLflow Models as REST endpoints.

Languages:    Java, Python, R, and REST APIs
Frameworks:   Keras , Scikit-learn , PySpark , XGBoost , TensorFlow , PyTorch , SpaCy , Fastai


mlflow.<framework>.autolog()
can be used to automatically capture  model-specific metrics, parameters, and model artifacts

- Metrics & Parameters:\

    Training loss; validation loss; user-specified metrics

    Metrics associated with the EarlyStopping callbacks (restore_best_weight, last_epoch), learning rate; epsilon

- Artifacts \
    Model summary on training start \
    MLflow Model (Keras model) on training end

Manual logging:
    mlflow.log_metric("test_acc", acc=0.9)
    mlflow.log_param("epochs", epoch=100)
    mlflow.<framework>.log_model(model, "myModel")
    mlflow.log_artifact("absolute path to file", "artifact name")

Two types of experiments:
    1. workspace: can be created from the Workspace UI or the MLflow API.
    2. notebook


Active experiment, can be set using:
    1. mlflow.set_experiment()
    2. mlflow.start_run(run_id=None, experiment_id=None)

Artifact Stores: suitable for large data (such as an S3 bucket), log models etc.
    Amazon S3 and S3-compatible storage , Azure Blob Storage  , Google Cloud Storage  , FTP server , SFTP Server , NFS , HDFS (Apache Hadoop)


Where Runs Are Recorded:
    To log runs remotely, set the MLFLOW_TRACKING_URI environment variable to a tracking server’s URI or call mlflow.set_tracking_uri().
    - Local
    - Database encoded as <dialect>+<driver>://<username>:<password>@<host>:<port>/<database>.
        Dialects: mysql, mssql, sqlite, and postgresql
    - HTTP server (specified as https://my-server:5000), that hosts an MLflow tracking server.
    - Databricks

# MLflow Projects: MLProject.yaml

A convention for organizing your code to let other data scientists run it

Each project is:

1) a directory of files
2) Git repository.

You can run the project:
    mlflow run command-line tool

    mlflow run mlflow_workflow --no-conda --experiment-name /experiments_demo_databricks2

    mlflow.projects.run() Python API

These APIs also allow submitting the project for remote execution

- Databricks
- Kubernetes

#### mlflow experiments:

https://www.mlflow.org/docs/latest/cli.html#mlflow-experiments


# Configuring databricks

-> https://docs.databricks.com/dev-tools/cli/index.html
pip install databricks-cli

#### run databricks configure
    Host: https://community.cloud.databricks.com
    User:
    Pass:
    Repeat pass:


# setting the tracking server
LOCAL-DISC: saving the runs on a designated uri

    mlflow.set_tracking_uri('file:/home/petra/mlrun_store')

LOCAL-DATABASE:

    mlflow.set_tracking_uri("sqlite:///mlruns.db")

REMOTE-DATABASE:

    mlflow.set_tracking_uri("databricks") """

# Backend store

Database (backend-store-uri) needs to be encoded as dialect+driver://username:password@host:port/database.

    Style of backend store for postgres:
    --backend-store-uri f'{dialect_driver}://{username}:{password}@{ip}/{database_name}'

Example (default):

    mlflow ui  --backend-store-uri <absolute-path-to-mlruns> \
                  --default-artifact-root <absolute-path-ro-artifacts> \
                  --host 0.0.0.0
                  --port 5000

Example:

    >> mlflow ui --port 5000 \
    --backend-store-uri postgresql://mlflow_developer:1234@localhost/mlflow_db
    --backend-store-uri postgresql://mlflow_developer:1234@192.168.0.19/mlflow_db

    HPC for artifact:
    --default-artifact-root sftp://mohammadsmajdi@filexfer.hpc.arizona.edu:/home/u29/mohammadsmajdi/mlflow/artifact_store

    Local storage for artifact:
    --default-artifact-root file:/Users/artinmac/Documents/Research/Data7/mlflow/artifact_store

Example to HPC-artifact & remote-postgres

    >> mlflow ui --backend-store-uri postgresql://mlflow_developer:1234@192.168.0.19/mlflow_db --default-artifact-root sftp://mohammadsmajdi@filexfer.hpc.arizona.edu:/home/u29/mohammadsmajdi/mlflow/artifact_store --port 5432

## Access to remote server postgres:

Source: https://www.thegeekstuff.com/2014/02/enable-remote-postgresql-connection/

### Step 0

#### Completely purging postgresql

1. via apt-get

    1.1 Checking postgresql packages

        >> dpkg -l  grep postgres

    1.2 Uninstalling all installed packages

        >> sudo apt-get --purge remove pgdg-keyring postgresql*

2. via brew

    >> brew uninstall postgresql
    >> rm .psql_history

#### Installing postgres

1. via apt-get

    >> sudo apt-get install postgresql postgresql-contrib postgresql-server-dev-all

2. via brew

    2.1 Installing Brew in Ubuntu

        >> sudo apt-get install build-essential curl file
        >> sudo apt install linuxbrew-wrapper 
        >> brew

    2.2 Installing postgresql using brew

        >> brew install postgresql

    2.3 Conda Environment

        >> conda create -n mlflow python=3.7
        >> conda install -c conda-forge scikit-learn scikit-image nibabel nilearn matplotlib numpy ipython pandas
        >> conda install -c anaconda tensorflow>=2.0 keras

#### Check PostgreSQL version

    >> apt show postgresql

### Setting up remote/client access

#### Find the remote server ip

    Ubuntu:
    >> ip addr show
    >> 172.29.207.12/24 (Atmosphere server)
    >> 192.168.0.19/24  (My Laptop)
    >> 10.208.16.20/24  (Data7 workstation)

    MacOS:
    >> ipconfig getifaddr en0
    >> 192.168.0.13      (My MacOS)  Maybe: 68.105.2811

#### Set up server to listen to clients (postgresql.conf & pg_hba.conf)

Add the line: host  'all   all  \<client-ip\>/24   trust'

    >> Ubuntu: vim /home/linuxbrew/.linuxbrew/var/postgres/pg_hba.conf
    >> Macos:  vim /usr/local/var/postgres/pg_hba.conf

Change the postgresql.conf on server machine to listen to all addresses.

    >> Ubuntu: vim /home/linuxbrew/.linuxbrew/var/postgres/postgresql.conf
    >> MacOS:  vim /usr/local/var/postgres/postgresql.conf
    -  Change listen_addresses = 'localhost' => listen_addresses = '*'

#### Restart postgres on your server

    Ubuntu:
    >> pg_ctl -D /home/linuxbrew/.linuxbrew/var/postgres stop
    >> pg_ctl -D /home/linuxbrew/.linuxbrew/var/postgres start

    MacOS:
    >> pg_ctl -D /usr/local/var/postgres stop
    >> pg_ctl -D /usr/local/var/postgres start

#### Test the connection by connecting to remote postgres

        172.29.207.12/24 (Atmosphere server)
        192.168.0.19/24  (My Laptop)
        10.208.16.20/24  (Data7 workstation)
        192.168.0.13     (My MacOS)  Maybe: 68.105.2811

    >> psql postgres -h <remote-ip> -p 5432 -U mlflow_developer

#### Setting up postgres

Go into psql

    >> psql postgres

Go into a specific database & a specific user:

    >> psql -d mlflow_db -U mlflow_user

    postgres=#  CREATE DATABASE mlflow_db;
    postgres=#  CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow';
    postgres=#  GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;

Showing information on database name, username, port, socket path

    >> postgres=# \conninfo

    Show Users: \du \
    Show databases: \list \
    Show something! \dp
    Show tables within the database       \d+

# sftp

source: <https://public.confluence.arizona.edu/display/UAHPC/Transferring+Files#TransferringFiles-GeneralFileTransfers>

step 0: Save the ssh authentication credentials
step 1: sftp://mohammadsmajdi@filexfer.hpc.arizona.edu:/home/u29/mohammadsmajdi/mlflow/artifact_store
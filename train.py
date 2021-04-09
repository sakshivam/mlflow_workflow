# %% ---------------------------------------------------------------------------------------------------------------------
""" Importing the packages """
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = "TRUE"
from small_functions import architecture, loading_data, reading_terminal_inputs
import mlflow
import numpy as np
from time import time
import git
import subprocess

# %% ---------------------------------------------------------------------------------------------------------------------
""" Reading the inputs fed through the command line """
epochs, batch_size = reading_terminal_inputs()
# epochs, batch_size = 3,32


def mlflow_settings(): 

    """ MLflow settings: 
        The style we should use when running mlflow ui
            Postgres server: server = f'{dialect_driver}://{username}:{password}@{ip}/{database_name}' 
            Local:           server = "file:/Users/artinmac/Documents/Research/Data7/mlflow/mlrun_store" """

    postgres_connection_type = { 'direct':     ('5432', 'data7-db1.cyverse.org'),
                                'ssh-tunnel': ('5000', 'localhost')
                                }

    port, host = postgres_connection_type['ssh-tunnel']

    username = "artinmajdi"
    password = '1234'
    database_name = 'phyto_oracle_db'
    dialect_driver = 'postgresql'
    server = f'{dialect_driver}://{username}:{password}@{host}:{port}/{database_name}'


    """ Setting up the artifact server """ 
    artifact_server = 'data7_db1'

    Artifacts = {
        'local':      "file:/<path-to-artifact-store>",
        'hpc':        'sftp://<user>:{password}@filexfer.hpc.arizona.edu:<path-to-artifact-store>',
        'atmosphere': 'sftp://<user>:{password}@<ip-address>:<path-to-artifact-store>',
        'cyverse':    'file:/<path-to-artifact-store>',
        'data7_db1':  'sftp://artinmajdi:temp2_data7_b@data7-db1.cyverse.org:/home/artinmajdi/mlflow_data/artifact_store'}

    artifact = Artifacts[artifact_server]

    return server, artifact

server, artifact = mlflow_settings()
mlflow.set_tracking_uri(server)

command = 'ssh -N -L 5000:localhost:5432 artinmajdi@data7-db1.cyverse.org &'
ssh_session = subprocess.Popen('exec ' + command, stdout=subprocess.PIPE, shell=True)

try:
    
    """ mlflow set-up """
    # Creating/Setting the experiment
    experiment_name = '/experiment_name2'

    # Line below should be commented if the experiment is already created
    # If kept commented during the first run of a new experiment, the set_experiment 
    # will automatically create the new experiment with local artifact storage
    # mlflow.create_experiment(name=experiment_name, artifact_location=artifact)
    mlflow.set_experiment(experiment_name=experiment_name)


    # Loading the optimization parameters aturomatically from keras
    mlflow.keras.autolog()

    # Starting the MLflow 
    mlflow.start_run()


    """ Model optimization """
    model = architecture()

    (train_images, train_labels), (test_images, test_labels) = loading_data()


    """ model training and evaluation """
    # with mlflow.start_run() as f:  # run_name='run_postgres_r2'experiment_id='7'

    start_time = time()
    history = model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size, validation_data=(test_images, test_labels))
    mlflow.log_metric("Time to optimize and save the model artifact", time()-start_time)


    # Model evaluation
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('Accuracy:', test_acc)
    print('Loss: ', test_loss)

    prediction = model.predict(test_images)
    predicted_classes = np.argmax(prediction, axis=1)

    # Saving MLflow parameters & metrics
    mlflow.log_param("epochs", epochs)
    mlflow.log_param("bsize", batch_size)
    mlflow.log_metric("accuracy", test_acc)
    mlflow.log_metric("test_loss", test_loss)

    # mlflow.set_tag('User',username)
    # mlflow.keras.log_model(model, "my_model_log")
    # mlflow.keras.save_model(model, 'my_model')
    # with open('predictions.txt', 'w') as f:
    #     f.write("predicted_classes")
    # mlflow.log_artifact('predictions.txt')
    # client.create_registered_model(description='first registered model', name=experiment_name)

    print("Model saved in run %s" % mlflow.active_run().info.run_uuid)

    mlflow.end_run()




finally:
    # ending the ssh session 
    # If this failed, we can type 'pkill ssh' in the terminal to kill all ssh sessions
    ssh_session.kill()

    # os.system('kill %1')

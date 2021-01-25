import os

os.environ['KMP_DUPLICATE_LIB_OK'] = "TRUE"
from small_functions import architecture, loading_data, reading_terminal_inputs
import mlflow
import numpy as np

epochs, batch_size = reading_terminal_inputs()

"""
RUN UI with postgres and HPC:
    REMOTE postgres server:
        # connecting to remote server through ssh tunneling
          ssh -L 5000:128.196.142.27:5432 artinmajdi@128.196.142.27
        # using the mapped port and localhost
          mlflow ui --backend-store-uri postgresql://mlflow_developer:1234@localhost:5000/mlflow_db --default-artifact-root sftp://mohammadsmajdi@filexfer.hpc.arizona.edu:/home/u29/mohammadsmajdi/projects/mlflow/artifact_store --port 6789

    LOCAL postgres server:
        mlflow ui --backend-store-uri postgresql://mlflow_developer:1234@localhost:5432/mlflow_db --default-artifact-root sftp://mohammadsmajdi@filexfer.hpc.arizona.edu:/home/u29/mohammadsmajdi/projects/mlflow/artifact_store --port 6789

RUN directly from GitHub:

    export MLFLOW_TRACKING_URI=http://127.0.0.1:5000

    mlflow run                 --no-conda --experiment-id 5 -P epoch=2 https://github.com/artinmajdi/mlflow_workflow.git -v main
    mlflow run mlflow_workflow --no-conda --experiment-id 5 -P epoch=2


    128.196.142.23/24 (Atmosphere server)
    10.208.16.20/24  (Data7 workstation)
    68.110.78.48     (Home WiFi)

show experiments/runs lsit
    export MLFLOW_TRACKING_URI=http://127.0.0.1:6789
    mlflow runs list --experiment-id <id>
"""
username = 'mlflow_developer'
password = '1234'
port = '5000'
ip = 'localhost'  # '128.196.142.23' #
database_name = 'mlflow_db'
dialect_driver = 'postgresql'

""" below is the style we should use when running mlflow ui
    server = f'{dialect_driver}://{username}:{password}@{ip}/{database_name}' """

server = f'{dialect_driver}://{username}:{password}@{ip}:{port}/{database_name}'  # :{port}
# server   = "file:/Users/artinmac/Documents/Research/Data7/mlflow/mlrun_store"

# artifact = "file:/Users/artinmac/Documents/Research/Data7/mlflow/artifact_store"
# artifact = 'sftp://mohammadsmajdi@filexfer.hpc.arizona.edu:/home/u29/mohammadsmajdi/projects/mlflow/artifact_store'
# artifact = "file:/home/u29/mohammadsmajdi/projects/mlflow/artifact_store"
artifact = 'sftp://artinmajdi:Rtn1371369!@128.196.142.27:/home/artinmajdi/mlflow/artifact_store'

mlflow.set_tracking_uri(server)
# mlflow.set_registry_uri(server)

""" Creating experiment """
experiment_name = '/experiment_v2_test_7'
mlflow.create_experiment(name=experiment_name, artifact_location=artifact)

""" Setting the experiment """
mlflow.set_experiment(experiment_name=experiment_name)

mlflow.keras.autolog()

if __name__ == "__main__":
    model = architecture()

    (train_images, train_labels), (test_images, test_labels) = loading_data()

    with mlflow.start_run() as f:  # run_name='run_postgres_r2'experiment_id='7'
        history = model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size,
                            validation_data=(test_images, test_labels))

        test_loss, test_acc = model.evaluate(test_images, test_labels)
        print('Accuracy:', test_acc)
        print('Loss: ', test_loss)

        prediction = model.predict(test_images)
        predicted_classes = np.argmax(prediction, axis=1)

        mlflow.log_param("epochs", epochs)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_metric("test_acc", test_acc)
        mlflow.log_metric("test_loss", test_loss)

        # mlflow.keras.log_model(model, "my_model_log")
        # mlflow.keras.save_model(model, 'my_model')

        # with open('predictions.txt', 'w') as f:
        #     f.write("predicted_classes")
        #
        # mlflow.log_artifact('predictions.txt')

        # client.create_registered_model(description='first registered model', name=experiment_name)

        print("Model saved in run %s" % mlflow.active_run().info.run_uuid)

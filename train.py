import os

os.environ['KMP_DUPLICATE_LIB_OK'] = "TRUE"
from small_functions import architecture, loading_data, reading_terminal_inputs
import mlflow
import numpy as np

epochs, batch_size = reading_terminal_inputs()

username = 'mlflow_developer'
password = '1234'
port = '5000'
ip = 'localhost'  # '128.196.142.23' #
database_name = 'mlflow_db'
dialect_driver = 'postgresql'

""" below is the style we should use when running mlflow ui
    server = f'{dialect_driver}://{username}:{password}@{ip}/{database_name}' """

server = f'{dialect_driver}://{username}:{password}@{ip}:{port}/{database_name}'
# server   = "file:/Users/artinmac/Documents/Research/Data7/mlflow/mlrun_store"

""" Setting up the artifact server """ 
artifact_server = 'atmosphere'

Artifacts = {
    'local':      "file:/Users/artinmac/Documents/Research/Data7/mlflow/artifact_store",
    'hpc':        'sftp://mohammadsmajdi@filexfer.hpc.arizona.edu:/home/u29/mohammadsmajdi/projects/mlflow/artifact_store',
    'atmosphere': 'sftp://artinmajdi:Rtn1371369!@128.196.142.27:/home/artinmajdi/mlflow/artifact_store'}

artifact = Artifacts[artifact_server]

mlflow.set_tracking_uri(server)
# mlflow.set_registry_uri(server)

""" Creating experiment """
ExperimentName = {
    'local':      '/exp_final_artifact_local',
    'hpc':        '/exp_final_artifact_hpc',
    'atmosphere': '/exp_final_artifact_atmosphere'}

experiment_name = ExperimentName[artifact_server]
# mlflow.create_experiment(name=experiment_name, artifact_location=artifact)

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

import os

os.environ['KMP_DUPLICATE_LIB_OK'] = "TRUE"
from small_functions import architecture, loading_data, reading_terminal_inputs
import mlflow
import numpy as np

epochs, batch_size = reading_terminal_inputs()

# if len(sys.argv) == 3:
#     epochs = int(sys.argv[1])
#     batch_size = int(sys.argv[2])
# else:
#     epochs = 2
#     batch_size = 110

"""                     MLflow Tracking

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

        - Metrics & Parameters:
            Training loss; validation loss; user-specified metrics

            Metrics associated with the EarlyStopping callbacks (restore_best_weight, last_epoch), learning rate; epsilon

        - Artifacts
            Model summary on training start
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
        2. mlflow.start_run(run_id=None, experiment_id=None).

    Artifact Stores: suitable for large data (such as an S3 bucket), log models etc.
        Amazon S3 and S3-compatible storage , Azure Blob Storage  , Google Cloud Storage  , FTP server , SFTP Server , NFS , HDFS (Apache Hadoop)


    Where Runs Are Recorded:
        To log runs remotely, set the MLFLOW_TRACKING_URI environment variable to a tracking server’s URI or call mlflow.set_tracking_uri().
        - Local
        - Database encoded as <dialect>+<driver>://<username>:<password>@<host>:<port>/<database>.
            Dialects: mysql, mssql, sqlite, and postgresql
        - HTTP server (specified as https://my-server:5000), that hosts an MLflow tracking server.
        - Databricks

"""

""" MLflow Projects: MLProject.yaml
    A convention for organizing your code to let other data scientists run it

    Each project is 1) a directory of files, or 2) Git repository.

    You can run the project:
        mlflow run command-line tool
        e.g. mlflow run mlflow_workflow --no-conda --experiment-name /experiments_demo_databricks2

        mlflow.projects.run() Python API

    These APIs also allow submitting the project for remote execution
        Databricks
        Kubernetes

    mlflow experiments: https://www.mlflow.org/docs/latest/cli.html#mlflow-experiments
"""

""" Configuring databricks :> https://docs.databricks.com/dev-tools/cli/index.html
    pip install databricks-cli

    run databricks configure
        Host: https://community.cloud.databricks.com
        User:
        Pass:
        Repeat pass:
"""
# mlflow.set_tracking_uri("databricks")
# mlflow.create_experiment(name='/experiments_demo_databricks2') # , artifact_location='dbfs:/artifacts_stuff')
# mlflow experiment create -n "/exp_simple2" -l <artifcat-location>
mlflow.set_experiment(experiment_name='/experiments_demo_databricks2')

mlflow.keras.autolog()

if __name__ == "__main__":
    model = architecture()

    (train_images, train_labels), (test_images, test_labels) = loading_data()

    # for epochs in [2, 3, 4]:
    with mlflow.start_run() as f:  #experiment_id='7'
        history = model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size,
                            validation_data=(test_images, test_labels))

        test_loss, test_acc = model.evaluate(test_images, test_labels)
        print('Accuracy:', test_acc)
        print('Loss: ', test_loss)

        preds = model.predict(test_images)
        predicted_classes = np.argmax(preds, axis=1)

        # model.save('model.h5')

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

        print("Model saved in run %s" % mlflow.active_run().info.run_uuid)

        # mlflow.end_run()

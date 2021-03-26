import mlflow

postgres_connection_type = { 'direct':     ('5432', 'data7-db1.cyverse.org'),
                             'ssh-tunnel': ('5000', 'localhost')
                            }

port, host = postgres_connection_type['ssh-tunnel']


username = "artinmajdi" 
password = '1234'
database_name = "mnist_db"
dialect_driver = 'postgresql'

server = f'{dialect_driver}://{username}:{password}@{host}:{port}/{database_name}'
artifact = 'sftp://artinmajdi:temp_data7@data7-db1.cyverse.org:/home/artinmajdi/mlflow_data/artifact_store'


mlflow.set_tracking_uri(server)


""" Line below should be commented if the experiment is already created
    If kept commented during the first run of a new experiment, the set_experiment 
    will automatically create the new experiment with local artifact storage """

experiment_name = 'experiment_test'
mlflow.create_experiment(name=experiment_name, artifact_location=artifact)
mlflow.set_experiment(experiment_name=experiment_name)

""" Loading the optimization parameters aturomatically from keras """
mlflow.keras.autolog()

""" Starting the MLflow """
mlflow.start_run()



""" Saving MLflow parameters & metrics """
mlflow.log_param("epochs", epochs)
mlflow.log_param("bsize", batch_size)
mlflow.log_metric("accuracy", test_acc)
mlflow.log_metric("test_loss", test_loss)

# mlflow.keras.log_model(model, "my_model_log")
# mlflow.keras.save_model(model, 'my_model')
# with open('predictions.txt', 'w') as f:
#     f.write("predicted_classes")
# mlflow.log_artifact('predictions.txt')
# client.create_registered_model(description='first registered model', name=experiment_name)

print("Model saved in run %s" % mlflow.active_run().info.run_uuid)
# %% ---------------------------------------------------------------------------------------------------------------------
mlflow.end_run()
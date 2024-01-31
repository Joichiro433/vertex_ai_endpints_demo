import json

from rich import print
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


def predict_custom_trained_model_sample(
    project: str,
    endpoint_id: str,
    instances: dict | list[dict],
    parameters: dict | None = None,
    location: str = "asia-northeast1",
    api_endpoint: str = "asia-northeast1-aiplatform.googleapis.com",
):
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # The format of each instance should conform to the deployed model's prediction input schema.
    instances = instances if isinstance(instances, list) else [instances]
    instances = [
        json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
    ]
    parameters = parameters if parameters is not None else {}
    parameters = json_format.ParseDict(parameters, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # The predictions are a google.protobuf.Value representation of the model's predictions.
    predictions = response.predictions
    for prediction in predictions:
        print(" prediction:", dict(prediction))


if __name__ == '__main__':
    # with open('sample-request.json', 'r') as f:
    #     instances = json.load(f)

    PROJECT_ID = "73169144800"
    ENDPOINT_ID = "8406135830254452736"

    instances = [
        {
            'bill_length_mm': 39.1,
            'bill_depth_mm': 18.7,
            'flipper_length_mm': 181,
            'body_mass_g': 3750
        },
        {
            'bill_length_mm': 46.5,
            'bill_depth_mm': 17.9,
            'flipper_length_mm': 192,
            'body_mass_g': 3500
        },
        {
            'bill_length_mm': 46.1,
            'bill_depth_mm': 13.2,
            'flipper_length_mm': 211,
            'body_mass_g': 4500
        }
    ]
    parameters = {"return_confidence": True}

    print(instances)
    
    predict_custom_trained_model_sample(
        project=PROJECT_ID,
        endpoint_id=ENDPOINT_ID,
        instances=instances,
        parameters=parameters,
    )

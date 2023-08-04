import datetime
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth

CREDENTIALS, PROJECT = google.auth.default()
dataflow_service = build("dataflow", "v1b3", credentials=CREDENTIALS)

job_name = ("test-dataflow-"+ datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"))

dataflow_dev_environment = {    
    "temp_location": "gs://explorede-390910/temp",
    "staging_location": "gs://explorede-390910/staging",
    "machine_type": "n1-standard-1",
    "enable_streaming_engine": False,
    "disk_size_gb": 10,
}

launch_parameter = {
    "launchParameter": {
        "jobName": f"{job_name}",
        "environment": dataflow_dev_environment,
        "containerSpecGcsPath": "gs://explorede-390910/flex-templates/batch/one/latest.json"
    }
}

print(f"JOB NAME: {job_name}")
print(f"BODY OF DATAFLOW LAUNCH REQUEST: {json.dumps(launch_parameter)}")

request = (
    dataflow_service.projects()
    .locations()
    .flexTemplates()
    .launch(projectId=PROJECT, body=launch_parameter, location="europe-west1")
)
try:
    response = request.execute()
    print(response)
except HttpError as err:
    if err.resp.status == 409:
        print(f"Dataflow with same name already exists")
    else:
        print(err)
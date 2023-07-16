from __future__ import print_function
import sys
import json
import io
import logging as pylog
import google.auth

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import datetime
import requests
import os
from apache_beam.io.gcp.internal.clients import bigquery
from apache_beam.io.gcp.bigquery_tools import parse_table_schema_from_json
from apache_beam.io.filesystems import FileSystems  # needed here
import uuid
import pytz, datetime
from decimal import Decimal
import decimal

from copy import deepcopy

import argparse
from typing import List
    
CREDENTIALS, PROJECT = google.auth.default()

def dataflow(beam_args: List[str] = None) -> None:
    options = PipelineOptions(
        beam_args,
        save_main_session=True,
        streaming=False,
        use_public_ips=False,
        staging_location="gs://explorede-390910/staging",
        temp_location="gs://explorede-390910/temp",
    )

    with beam.Pipeline(options=options) as pipe:
            lines = pipe | "Read from Bigquery" >> beam.io.ReadFromBigQuery(
                query="select * from explorede-390910.de.de_table", use_standard_sql=True,
            )

if __name__ == "__main__":
    pylog.getLogger().setLevel(pylog.INFO)

    print("Starting Dataflow")
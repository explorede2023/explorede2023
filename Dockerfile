FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ARG WORKDIR=/dataflow/template
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

COPY ./requirements.txt .
COPY ./main.py .

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/main.py"

RUN apt-get update \
  && apt-get install -y libffi-dev git \
  && rm -rf /var/lib/apt/lists/* \
  # Upgrade pip and install the requirements.
  && pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE \
  # Download the requirements to speed up launching the Dataflow job.
  && pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE

ENV PIP_NO_DEPS=True

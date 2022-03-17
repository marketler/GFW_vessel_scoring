FROM python:3.7-slim

# Configure the working directory
RUN mkdir -p /opt/project
WORKDIR /opt/project

# Setup local application dependencies
COPY . /opt/project

#Used to detect DATAFLOW_PINNED_DEPENDENCIES for following step
RUN pip install -e .

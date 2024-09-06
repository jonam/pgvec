# Copyright (c) 2024 AI Systems. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Use the official PostgreSQL image as the base image
FROM postgres:latest

# Install Python, git, and other necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv git postgresql-server-dev-all build-essential vim

# Install the vector extension from source (if available) or setup other necessary dependencies
RUN git clone https://github.com/pgvector/pgvector.git /tmp/pgvector && \
    cd /tmp/pgvector && \
    make && \
    make install

# Create a virtual environment and install psycopg2-binary
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install psycopg2-binary numpy

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=aidb
ENV POSTGRES_USER=aiuser
ENV POSTGRES_PASSWORD=aipasswd
ENV POSTGRES_HOST=localhost
ENV POSTGRES_PORT=5432

# Copy SQL initialization scripts into the container
COPY ./init_scripts/ /docker-entrypoint-initdb.d/

# Copy the Python script into the container
COPY vector_lookup.py /usr/src/app/vector_lookup.py
COPY create_embeddings.py /usr/src/app/create_embeddings.py

# Set the working directory
WORKDIR /usr/src/app

# Expose the default PostgreSQL port
EXPOSE 5432

# Use PostgreSQL's default entry point script
CMD ["docker-entrypoint.sh", "postgres"]


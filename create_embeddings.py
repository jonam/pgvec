"""
Copyright (c) 2024 AI Systems. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import psycopg2
from psycopg2.extras import execute_values
import numpy as np

# Database connection details
DB_NAME = "aidb"
DB_USER = "aiuser"
DB_PASSWORD = "aipasswd"
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Create the 'items' table with a vector column
cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id SERIAL PRIMARY KEY,
        name TEXT,
        embedding vector(1024)  -- 1024-dimensional vector
    );
""")
conn.commit()

# Create an index on the 'embedding' column using ivfflat and vector_l2_ops
cur.execute("""
    CREATE INDEX IF NOT EXISTS embedding_index
    ON items USING ivfflat (embedding vector_l2_ops)
    WITH (lists = 1024);
""")

# Generate and insert 200000 random 1024-dimensional vectors
num_vectors = 200000
batch_size = 1000  # Insert in batches to manage memory usage and performance
for i in range(0, num_vectors, batch_size):
    batch_vectors = [
        (f'item_{j}', np.random.rand(1024).tolist()) for j in range(i, i + batch_size)
    ]
    execute_values(cur, "INSERT INTO items (name, embedding) VALUES %s", batch_vectors)
    conn.commit()
    print(f'Inserted batch {i} to {i + batch_size}')

# Close the database connection
cur.close()
conn.close()

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

# Perform similarity searches using 5000 random 1024-dimensional sample vectors
sample_vectors = [np.random.rand(1024).tolist() for _ in range(5000)]

# Search and print results for each sample vector
for idx, search_vector in enumerate(sample_vectors):
    cur.execute("""
        SELECT name, embedding <-> %s::vector AS distance
        FROM items
        ORDER BY distance
        LIMIT 1;
    """, (search_vector,))
    result = cur.fetchone()
    print(f"Search {idx + 1}: Most similar item: {result[0]}, Distance: {result[1]}")

# Close the database connection
cur.close()
conn.close()

## Instructions

Create container.

```
./pg_docker.sh
```

Enter container.

```
./test_docker.sh
```

Create Embeddings.

```
root@3c9471f4efb2:/usr/src/app# python3 create_embeddings.py
```

Test Vector Lookups.

```
root@3c9471f4efb2:/usr/src/app# python3 vector_lookup.py
```

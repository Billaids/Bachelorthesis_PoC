# Proof of Concept Bachelorthesis
Proof of Concept for my bachelor thesis in B.Sc. Business Informatics at the University of Applied Sciences Weserbergland.

## How to run?

<div class="termy">

```console
$ python3.9 -m pip install -r requirements.txt

```

</div>

- install MongoDB locally and add 172.17.0.1 in /etc/mongod.conf
- Configure config.yaml

<div class="termy">


```console
$ python3.9 -m uvicorn poc:app --port <port> --host 0.0.0.0

```

## How to run with Docker?

<div class="termy">

```console
$ docker build . -t poc

```

</div>

- install MongoDB locally and add 172.17.0.1 in /etc/mongod.conf
- Configure config.yaml and follow instructions in traefik-config

<div class="termy">

```console
$ docker-compose up -d

```

</div>
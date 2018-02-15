# MarRef Bioschemas sample webpages

# Introduction
This is a demo project with some sample pages extract from the MarRef database ([https://mmp.sfb.uit.no/](https://mmp.sfb.uit.no/))
The idea behind this is to provide a sandbox where people can try to interact with MarRef samples using BioSchemas specification

# Docker
In order to make this work you need to have [Docker](https://www.docker.com/community-edition) installed

# Steps to run the server with local pages
To run the test server you need to do
1. Build the `Dockerfile` from the current directory
```bash
./build.sh
```

or if you want more control you can use docker commands directly, e.g.

```bash
docker build -t mar-ref .
```


2. Run the server and loading the webpages
```bash
./serve.sh
```

or if you want more control you can use docker commands directly, e.g.

```bash
docker run -d --name mar-ref -v $(pwd)/src:/MarRef -p 8080:8080 mar-ref
```

3. Go with your favorite browser to `http://localhost:8080` and you should be able to see a list of the webpages

4. To stop the docker container
```bash
./stop.sh
```

of if you want more control use directly docker commands, e.g.
```bash
docker stop mar-ref
docker rm mar-ref
```

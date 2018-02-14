# MarRef Bioschemas sample webpages

# Docker
In order to make this work you need to have [Docker](https://www.docker.com/community-edition) installed

# Steps to run the server with local pages
To run the test server you need to do
1. Build the `Dockerfile` from the current directory
```bash
docker build -t mar-ref .
```

2. Run the server and loading the webpages
```bash
docker run -d --name mar-ref -v $(pwd)/src:/MarRef -p 8080:8080 mar-ref
```

3. Go with your favorite browser to `http://localhost:8080` and you should be able to see a list of the webpages



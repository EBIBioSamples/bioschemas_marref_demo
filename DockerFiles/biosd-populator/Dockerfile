FROM python:3.6
COPY ./biosamples /populator/biosamples
COPY ./populator/ /populator
COPY ./site/ /populator/site
WORKDIR /populator
RUN pip install -r requirements.txt

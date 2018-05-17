# MarRef demo summary

## Aim of the demo

Scope of the MarRef demo is to give a practical example on
how Bioschemas profiles could be used to export highly curated metadata
in services that don't provide an Application Programming Interface (API)
and how such metadata could be use by external services, like the BioSamples database,
to improve the quality of the sample stored.

## Organisation of the demo

The demo uses a set of DockeContainer to:

1. Present a subset of samples extracted from the MarRef database as example
2. Run the [bsbang-crawler](https://github.com/justinccdev/bsbang-crawler) to extract metadata from MarRef
3. Store the results in a Solr index for searching purposes
4. Curate BioSamples database available localy - but [outside of this repository](https://github.com/EBIBioSamples/biosamples-v4)

A `demo.py` small command line application has been built to step through the different phases of the demo

## Steps

### 1. Setup the environment

Not a lot to say here, the setup instantiate the local sandbox with a set of MarRef samples available as 
HTML pages

![setup-step](summary/setup.gif)

### 2. Crawl sandbox and generate a Solr index

In this step, using the bsbang crawler we extract the Bioschemas markup embedded in the MarRef demo pages and
we store in a in-memory database. This step is to prove how we can access to the data using Bioschemas and store it
somewhere else, and use such data to build services or improve quality of samples stored elsewhere, like we will
show in step number 3. During this step we will use the stored data to create a simple search service using Solr.

![crawl-step](summary/crawl.gif)

### 3. Curate BioSamples

Last step is BioSamples curation. This steps uses the data extracted by the crawler to generate curation object
and use them to curate BioSamples samples associated to MarRef samples.

**Note:** This is just a proof of concept with some attributes and links to external databases

![curate-step](summary/curate.gif)

Let's start showing how the MarRef sample page looks and how the BioSamples corresponding samples looks

MarRef sample
![marref source](summary/marref_curation_origin.png)

BioSamples sample
![biosamples before curation](summary/sample_pre_curation.png)

Running our script we are able to generate curation object and submit them to BioSamples to get back a curated version
of the Sample. In BioSamples a curation is a layer put on top of the original sample, and each curation has
a domain that let you track the submitter of the curation itself. In our case we use a curation domain called
`MarRefCuration`, and this information ideally could be used to expose the curator in the user interface, e.g. showing
a badge saying "Resource curated by MarRef"

![biosamples-after-curation](summary/sample_after_curation.png)
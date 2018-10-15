import sys
from termcolor import colored
# import subprocess
import os

action_order = ["setup", "crawl", "curate", "quit"]


def ask_user_input():
    input_str = "Should I continue with the next demo step ({})? [y/n/all] \n > ".format(action_order[0])
    return input(input_str)


def comment(text):
    return colored(text, "green", attrs=["bold", "underline"])


def warning(text):
    return colored(text, "yellow", "on_grey")


def new_line():
    print("")


def setup_demo():
    """
    Setup the containers for the demo
    """
    print(comment("Alright! I'll set up a local instance of MarRef database and prepare the crawler"))
    new_line()

    # subprocess.check_output(["./setup.sh", "--clean"], shell=True)
    os.system("./setup.sh --clean")

    new_line()
    print(comment("Everything should be up and running!"))
    print(comment("You can check on http://localhost:8080/ your tiny local version of MarRef"))
    new_line()


def populate_biosd():
    """
    Populate BioSamples instance with samples if not already available
    """
    print(comment("I'll populate BioSamples with the necessary files"))

    new_line()
    os.system("docker-compose up biosd-populator")
    new_line()


def do_crawl():
    """
    Crawl marref to extract metadata
    """
    print(comment("I'll now proceed by crawling the MarRef local instance"))
    print(comment("Let's start by checking which pages I should crawl"))
    # subprocess.check_output(['docker-compose up bsbc-crawl'], shell=True)
    new_line()
    os.system("docker-compose up bsbc-crawl")
    new_line()

    print(comment("I'll now proceed by extracting the Bioschemas content from the pages"))

    new_line()
    os.system("docker-compose up bsbc-extract")
    new_line()
    # subprocess.check_output(['docker-compose up bsbc-extract'], shell=True)

    print(comment("Finally, just for the sake of the demo, I'll add the results to a search index"))
    new_line()
    os.system("docker-compose up bsbc-index")
    new_line()
    # subprocess.check_output(['docker-compose up bsbc-index'], shell=True)

    print(comment("Ok...lot of work here! But I'm done!"))
    print(comment("Try to search for something in solr at http://localhost:8984/solr"))
    new_line()


def do_curation():
    """
    Curate BioSamples using the crawled metadata
    """
    print(comment("I'll now proceed creating the BioSamples curation objects"))
    print(comment("Once an object is created, I'll post it to the local version of Biosamples"))

    # subprocess.check_output(['docker-compose', 'up', 'biosd-curate'], shell=True)
    new_line()
    os.system("docker-compose up biosd-curate")
    new_line()

    print(comment("Done! You should be able to see all my precious work over to "
                  "http://localhost:8081/biosamples/samples"))
    print(comment("Go have a look"))
    new_line()


def exit_demo():
    """
    Exit the demo
    """
    new_line()
    print(comment("Hope you had fun, bye bye!"))
    sys.exit()


def do_action(name):
    if name == "setup":
        setup_demo()
    elif name == "populate":
        populate_biosd()
    elif name == "crawl":
        do_crawl()
    elif name == "curate":
        do_curation()
    elif name == "quit":
        exit_demo()


if __name__ == "__main__":
    print("")
    print(comment("Good morning user!"))
    print("")
    while True:
        uin = ask_user_input()
        new_line()
        if uin.lower() not in ["y", "n", "all"]:
            print("Sorry, I'm dumb and I don't know what to do with {}...".format(uin))
            new_line()
            uin = ask_user_input()

        uin = uin.lower()
        if uin == "all":
            while len(action_order) > 0:
                next_step = action_order.pop(0)
                do_action(next_step)
        elif uin == "y":
            next_step = action_order.pop(0)
            do_action(next_step)
        else:
            exit_demo()

import sys
from termcolor import colored
# import subprocess
import os

status = {
    "setup": 0,
    "crawl": 0,
    "curate": 0,
    "quit": 0
}


def get_valid_actions():
    # return ["setup", "crawl", "curate", "quit"]
    return [k for k in status.keys() if status[k] == 0]


def ask_user_input():
    input_str = "What would you like me to do? [{}] \n > ".format(" | ".join(get_valid_actions()))
    return input(input_str)


def has_done(action):
    return status.get(action, 0)


def set_done(action):
    status[action] = 1


def comment(text):
    return colored(text, "green", attrs=["bold", "underline"])


def warning(text):
    return colored(text, "yellow", "on_grey")


def new_line():
    print("")


if __name__ == "__main__":
    print("")
    print(comment("Good morning user!"))
    print("")
    while True:
        uin = ask_user_input()
        new_line()
        while uin not in get_valid_actions():
            print("Sorry, I'm dumb and I don't know what to do with {}...".format(uin))
            new_line()
            uin = ask_user_input()

        if uin == "setup":
            if has_done("setup"):
                print(warning("It looks like you already set up the environment"))
                new_line()
                continue

            print(comment("Alright! I'll set up a local instance of MarRef database and prepare the crawler"))
            new_line()

            # subprocess.check_output(["./setup.sh", "--clean"], shell=True)
            os.system("./setup.sh --clean")

            new_line()
            print(comment("Everything should be up and running!"))
            print(comment("You can check on http://localhost:8080/ your tiny local version of MarRef"))
            new_line()

            set_done("setup")

        elif uin == "crawl":
            if has_done("setup"):
                if has_done("crawl"):
                    print(warning("I've already crawled everything, no need to run this again."))
                    new_line()
                    continue
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

                set_done("crawl")

            else:
                print(warning("I would suggest to start with a setup..."))
                continue

        elif uin == "curate":
            # if has_done("curate"):
            #     print("There's nothing else to curate...sorry!")
            #     continue

            if has_done("setup"):
                if has_done("crawl"):
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

                    set_done("curate")

                else:
                    print(warning("You need to use the 'crawl' command before creating curations"))
                    new_line()
            else:
                print(warning("Start using the 'setup' command to bring up the env"))
                new_line()
        else:
            new_line()
            print(comment("Hope you had fun, bye bye!"))
            sys.exit()

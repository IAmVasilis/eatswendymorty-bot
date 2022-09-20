
from src.modules.bot.morty import BotChallenger
from src.util.logger.log import log
from colorama import Fore

import time
import toml


def start_bot(settings: dict, emails: list, logger):
    for email in emails:
        try:
            result = BotChallenger(
                accessCode=settings['access-code']['code'],
                firstName=settings['details']['firstName'],
                lastName=settings['details']['lastName'],
                birthDate=settings['details']['birthDate'],
                phoneNumber=settings['details']['phoneNumber'],
                street=settings['location']['street'],
                city=settings['location']['city'],
                state=settings['location']['state'],
                zip=settings['location']['zip'],
                email=email
            ).start()
            if result:
                logger.print(caller="Morty-Bot",text=f"{Fore.LIGHTYELLOW_EX}COOK! {Fore.WHITE}Successfully cooked on '{email}', Please press enter after you've redeemed your prize.")
                input("> ")
            else:
                logger.print(caller="Morty-Bot", text=f"Didn't win on '{email}', Moving onto the next.")
        except:
            pass
    logger.print(caller="Morty-Bot",
                 text=f"Attempted to register on all emails, Please press enter to end the program.")
    input("> ")


def main():
    # create the CLI Logger
    cli_logger = log()
    cli_logger.print(caller="Main", text="MortyCooker Loaded! Developed by Vasilis#5708 with <3")

    # loading all possible emails inside of
    with open("config/data/emails.txt", "r") as f:
        emails = f.read().strip().split("\n")

    # check if the user doesn't have any valid emails
    if len(emails) == 1:
        # if there is no valid email, close the program.
        if emails[0].strip() == "" or '@' not in emails[0]:
            cli_logger.print(caller="Main",
                             text=f"Please add some emails before starting the morty bot, It wouldn't work without it.")
            time.sleep(5)
            exit(0)

    cli_logger.print(caller="Main", text=f"Loaded {len(emails)} emails to cook with, Attempting to load configuration.")
    time.sleep(1)

    # load toml configuration
    with open("config/settings.toml", "r", encoding="utf-8") as f:
        configuration = toml.loads(f.read())
    cli_logger.print(caller="Main", text="Loaded Configuration, Starting MortyCooker.")
    time.sleep(1)

    # start the cooker :)
    start_bot(settings=configuration, emails=emails, logger=cli_logger)


if __name__ == "__main__":
    main()

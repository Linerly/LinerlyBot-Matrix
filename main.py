import os
import random
import pyjokes
import requests
from quoters import Quote

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler

# Global variables
USERNAME = "linerlybot-matrix"         # Bot's username
PASSWORD = os.environ['PASSWORD']       # Bot's password
SERVER = os.environ['SERVER']  # Matrix server URL


def help_callback(room, event):
    # Send a list of commands that you can use
    room.send_html("<b>Commands</b><ul><li><code>!help</code></li><li><code>!echo [text]</code></li><li><code>!d[maximum amount]</code></li></ul><br><b>Other Things to Try</b><ul><li>Say <code>Hi</code></li></ul><br><i>ℹ️ square brackets means required input</i>")

def hi_callback(room, event):
    # Somebody said hi, let's say something
    room.send_html("Hello there, " + event['sender'] + "!<br><br>I'm LinerlyBot.<br>I used to be on Discord only, but now I'm also here in the Matrix universe!<br>You can type <code>!help</code> to get a list of commands that you can use.")


def echo_callback(room, event):
    args = event['content']['body'].split()
    args.pop(0)

    # Echo what they said back
    room.send_text(' '.join(args))


def dieroll_callback(room, event):
    # someone wants a random number
    args = event['content']['body'].split()

    # we only care about the first arg, which has the die
    die = args[0]
    die_max = die[2:]

    # ensure the die is a positive integer
    if not die_max.isdigit():
        room.send_text("{}? It's not a positive number!".format(die_max))
        return

    # and ensure it's a reasonable size, to prevent bot abuse
    die_max = int(die_max)
    if die_max <= 1 or die_max >= 1000:
        room.send_text("The dice amount must be between `1` and `1000`!")
        return

    # finally, send the result back
    result = random.randrange(1,die_max+1)
    room.send_text(str(result))

def quote_callback(room, event):
    room.send_text(Quote.print())

def joke_callback(room, event):
    room.send_text(pyjokes.get_joke())

def text_callback(room, event):
    args = event['content']['body'].split()
    args.pop(0)

    r = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={
                "text": args,
            },
            headers={"api-key": os.environ["DEEPAI_API_KEY"]},
        )
    
    room.send_html(f"<b>Raw JSON Output</b><br><i>provided by DeepAI</i><br><code>{str(r.json())}</code>")

def main():
    # Create an instance of the MatrixBotAPI
    bot = MatrixBotAPI(USERNAME, PASSWORD, SERVER)

    # Add a regex handler waiting for the help command
    help_handler = MCommandHandler("help", help_callback)
    bot.add_handler(help_handler)

    # Add a regex handler waiting for the word Hi
    hi_handler = MRegexHandler("Hi", hi_callback)
    bot.add_handler(hi_handler)

    # Add a regex handler waiting for the echo command
    echo_handler = MCommandHandler("echo", echo_callback)
    bot.add_handler(echo_handler)

    # Add a regex handler waiting for the die roll command
    dieroll_handler = MCommandHandler("d", dieroll_callback)
    bot.add_handler(dieroll_handler)

    quote_handler = MCommandHandler("quote", quote_callback)
    bot.add_handler(quote_handler)

    joke_handler = MCommandHandler("joke", joke_callback)
    bot.add_handler(joke_handler)

    text_handler = MCommandHandler("text", text_callback)
    bot.add_handler(text_handler)

    # Start polling
    bot.start_polling()

    print("I should be ready now!")

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        input()


if __name__ == "__main__":
    main()

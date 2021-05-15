This is a basic chat bot that takes any string as an input, learns how to respond to it in an sqlite database if it hasn't seen it before, and then uses the learned response to respond to similar future query.


run the bot with
```bash
python basic_io_bot.py -db xxx.sqlite
```

where xxx is the name of the existing sqlite database it should connect to, if not it will make julio_bot.sqlite

Provide your own bot token for your bot from botfather!


# References
source: https://www.codementor.io/python/tutorial/building-a-telegram-bot-using-python-part-1. It walks you through building an echobot (a bot that echoes your messages back to you) from scratch using Python and Telegram.

Part 2 of the tutorial shows you how to add a database to your chatbot so that it can have long-term memory. As an example, we build a basic To Do list that allows users to add and remove text items.

Part 3 of the tutorial will be in the form of a live office hour video where I show how to deploy the bot to a VPS.

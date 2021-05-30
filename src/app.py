#!/usr/bin/env python
import logging
import token
from handler import main

from functions import start, simpsons, help, ping, error, trend
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

if __name__ == '__main__':
    main()
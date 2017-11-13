"""
.env settings are loaded here
Author: https://github.com/velutha
"""
import os
from os.path import join, dirname
from dotenv import load_dotenv

DOTENV_PATH = join(dirname(__file__), ".env")
load_dotenv(DOTENV_PATH)
ROOT_DIR = os.path.dirname(__file__)

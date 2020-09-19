#!/usr/bin/python
import configparser
import sys

# Read configurationFile
def get_ConfigFile(inifile, section):

    c = configparser.ConfigParser()

    dataset = c.read(inifile)

    if len(dataset) != 1:

        raise ValueError

    try:

        c.read(inifile)

    except Exception as e:

        raise e

    # Verify keys in configuration file
    for key in c[section]:

        if len(c[section][key]) == 0:

            fatal("fatal: %s: could not find %s string" % (inifile, key), 1)

    return c[section]

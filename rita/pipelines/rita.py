# coding: utf-8
"""
rita Pipeline 

.. module:: rita

   :synopsis: rita pipeline

.. moduleauthor:: Adolfo De Unánue <nanounanue@gmail.com>
"""

import os

import subprocess

import pandas as pd

import csv

import datetime

import luigi
import luigi.s3

import sqlalchemy

## Variables de ambiente
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


## Logging
import rita.config_ini

import logging

logger = logging.getLogger("dpa-template.rita")


import rita.pipelines.utils
import rita.pipelines.common



class ritaPipeline(luigi.WrapperTask):
    """
    Task principal para el pipeline 
    """

    def requires(self):
        yield PythonTask()

class RTask(luigi.Task):

    root_path = luigi.Parameter()

    def requires(self):
        return RawData()

    def run(self):
        cmd = '''
              docker run --rm -v rita_store:/rita/data  rita/test-r 
        '''

        logger.debug(cmd)

        out = subprocess.check_output(cmd, shell=True)

        logger.debug(out)

    def output(self):
        return luigi.LocalTarget(os.path.join(os.getcwd(), "data", "hola_mundo_desde_R.psv"))


class PythonTask(luigi.Task):

    def requires(self):
        return RTask()

    def run(self):
        cmd = '''
              docker run --rm -v rita_store:/rita/data  rita/test-python --inputfile {} --outputfile {}
        '''.format(os.path.join("/rita/data", os.path.basename(self.input().path)),
                   os.path.join("/rita/data", os.path.basename(self.output().path)))

        logger.debug(cmd)

        out = subprocess.call(cmd, shell=True)

        logger.debug(out)

    def output(self):
        return luigi.LocalTarget(os.path.join(os.getcwd(), "data", "hola_mundo_desde_python.json"))



class RawData(luigi.ExternalTask):
    def output(self):
        return luigi.LocalTarget("./data/raw_data.txt")



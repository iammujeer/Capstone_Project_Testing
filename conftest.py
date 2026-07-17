import pandas as pd
from sqlalchemy import create_engine 
#import cx_Oracle
import logging
import pytest
from test_configuration.etlconfig import *
#Logging Config

logging.basicConfig(
    filename="logs/extractions_tests.log",
    filemode='a',
    format="%(asctime)s-%(levelname)s%(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

#DB Conn
@pytest.fixture()
def connect_to_oracledb():
    logger.info("Oracle connection is being established")
    oracledb_conn = create_engine(
        f"oracle+oracledb://{oracle_user}:{oracle_pwd}@{oracle_localhost}:{oracle_port}/{oracle_service}"
    ).connect()
    logger.info("Oracle connection successful")
    yield oracledb_conn
    oracledb_conn.close()
    return oracledb_conn

@pytest.fixture()
def connect_to_mysqldb():
    logger.info("MySQL connection is being established")
    mysql_conn =  create_engine(
        f"mysql+pymysql://{mysql_user}:{mysql_pwd}@{mysql_localhost}:{mysql_port}/{mysql_database}"
    ).connect()
    logger.info("MySQL connection successful")
    yield mysql_conn
    mysql_conn.close()
    return mysql_conn
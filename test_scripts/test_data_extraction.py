import inspect

import pandas as pd
import pytest
from sqlalchemy import create_engine
from common_utilities.utilities import verify_expected_as_file_with_database, verify_expected_as_source_database_with_target_database
import logging
#Logging Config

logging.basicConfig(
    filename="logs/extractions_tests.log",
    filemode='a',
    format="%(asctime)s-%(levelname)s%(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("connect_to_mysqldb")
@pytest.mark.usefixtures("connect_to_oracledb")
class TestDataExtraction:

    def test_DE_between_source_supplier_to_target_as_staging(self, connect_to_mysqldb):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case name: {test_case_name}")
            logger.info(f"Test case {test_case_name} execution has started")
            actual_query = "SELECT * FROM stage_supplier"

            verify_expected_as_file_with_database(
                "test_data/supplier_data.json",
                "json",
                connect_to_mysqldb,
                actual_query,
                test_case_name
            )
        except Exception as e:
            logger.error(f"supplier data extrcation validation failed {e}")
            raise

    def test_DE_between_source_inventory_to_target_as_staging(self, connect_to_mysqldb):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case name: {test_case_name}")
            logger.info(f"Test case {test_case_name} execution has started")
            actual_query = "SELECT * FROM stage_inventory"

            verify_expected_as_file_with_database(
                "test_data/inventory_data.xml",
                "xml",
                connect_to_mysqldb,
                actual_query,
                test_case_name
            )
        except Exception as e:
            logger.error(f"supplier data extrcation validation failed {e}")
            raise
    
    def test_DE_between_source_product_to_target_as_staging(self, connect_to_mysqldb):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case name: {test_case_name}")
            logger.info(f"Test case {test_case_name} execution has started")
            actual_query = "SELECT * FROM stage_product"

            verify_expected_as_file_with_database(
                "test_data/product_data.csv",
                "csv",
                connect_to_mysqldb,
                actual_query,
                test_case_name
            )
        except Exception as e:
            logger.error(f"supplier data extrcation validation failed {e}")
            raise
    
    def test_DE_between_source_sales_to_target_as_staging(self, connect_to_mysqldb):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case name: {test_case_name}")
            logger.info(f"Test case {test_case_name} execution has started")
            actual_query = "SELECT * FROM stage_sales"

            verify_expected_as_file_with_database(
                "test_data/sales_data.csv",
                "csv",
                connect_to_mysqldb,
                actual_query,
                test_case_name
            )
        except Exception as e:
            logger.error(f"supplier data extraction validation failed {e}")
            raise

    def test_DE_between_stores_sales_to_target_as_staging(self, connect_to_mysqldb, connect_to_oracledb):
        try:
            test_case_name = inspect.currentframe().f_code.co_name
            logger.info(f"Test case name: {test_case_name}")
            logger.info(f"Test case {test_case_name} execution has started")
            source_query = "SELECT * FROM stores"
            target_query = "SELECT * FROM stage_stores"
            verify_expected_as_source_database_with_target_database(
                source_query,
                connect_to_oracledb,
                target_query,
                connect_to_mysqldb,
                test_case_name
            )
        except Exception as e:
            logger.error(f"supplier data extrcation validation failed {e}")
            raise
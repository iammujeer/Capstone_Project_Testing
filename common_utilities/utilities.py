import pandas as pd
import logging

logger = logging.getLogger(__name__)

def verify_expected_as_file_with_database(file_path, file_type, db_actual, query_actual, test_case_name):
    print("Inside verify_expected_as_file_with_database")
    try:
        # Read expected data
        if file_type == "csv":
            df_expected = pd.read_csv(file_path)
        elif file_type == "json":
            df_expected = pd.read_json(file_path)
        elif file_type == "xml":
            df_expected = pd.read_xml(file_path, xpath=".//item")
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        logger.info(f"Expected Data:\n{df_expected}")

        # Read actual data from database
        df_actual = pd.read_sql(query_actual, db_actual)
        logger.info(f"Actual Data:\n{df_actual}")

        # Ensure both DataFrames have same column order
        df_actual = df_actual[df_expected.columns]

        # Find rows present in expected but missing in actual
        df_extra_in_expected = df_expected[
            ~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))
        ]

        # Find rows present in actual but missing in expected
        df_extra_in_actual = df_actual[
            ~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))
        ]

        # Save mismatch reports
        df_extra_in_expected.to_csv(
            f"Differences/extra_rows_in_expected_{test_case_name}.csv",
            index=False
        )

        df_extra_in_actual.to_csv(
            f"Differences/extra_rows_in_actual_{test_case_name}.csv",
            index=False
        )

        logger.info(f"Rows missing in DB:\n{df_extra_in_expected}")
        logger.info(f"Unexpected rows in DB:\n{df_extra_in_actual}")

        # Assertions
        assert df_extra_in_expected.empty, (
            f"{test_case_name}: Rows present in expected file but missing in database.\n"
            f"{df_extra_in_expected}"
        )

        assert df_extra_in_actual.empty, (
            f"{test_case_name}: Extra rows found in database.\n"
            f"{df_extra_in_actual}"
        )

        logger.info(f"{test_case_name} passed successfully.")

    except Exception as e:
        logger.error(f"{test_case_name} failed: {e}")
        raise

def verify_expected_as_source_database_with_target_database(source_query,oracle_connection,target_query,mysql_connection,test_case_name):
    print("Inside verify_expected_as_sourcedb_with_targetdb")
    df_source = pd.read_sql(source_query,oracle_connection)
    df_target = pd.read_sql(target_query,mysql_connection)

    df_source["store_id"] = df_source["store_id"].astype(str)
    df_target["store_id"] = df_target["store_id"].astype(str)

    df_source_extra_records = df_source[~df_source.apply(tuple, axis = 1).isin(df_target.apply(tuple, axis = 1))]
    df_target_extra_records = df_target[~df_target.apply(tuple, axis = 1).isin(df_source.apply(tuple, axis=1))]
    assert df_source_extra_records.empty,(f"Extra records in source: {df_source_extra_records}")
    assert df_target_extra_records.empty,(f"Extra records in target: {df_source_extra_records}")

    logger.info(f"{test_case_name} passed successfully.")
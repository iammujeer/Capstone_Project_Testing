import pandas as pd
import logging

logger = logging.getLogger(__name__)

def compare_source_and_target_data(
    origin_source,
    file_path,
    file_type,
    source_query,
    source_db,
    origin_target,
    target_query,
    target_db,
    test_case_name
):

    # ---------- Read Source ----------
    if origin_source == "SOURCE FILE":
        if file_type == "csv":
            df_source = pd.read_csv(file_path)
        elif file_type == "json":
            df_source = pd.read_json(file_path)
        elif file_type == "xml":
            df_source = pd.read_xml(file_path, xpath=".//item")
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    elif origin_source == "SOURCE DB":
        df_source = pd.read_sql(source_query, source_db)

    else:
        raise ValueError(f"Invalid source origin: {origin_source}")

    logger.info(f"Source Data:\n{df_source}")

    # ---------- Read Target ----------
    if origin_target == "TARGET FILE":
        if file_type == "csv":
            df_target = pd.read_csv(file_path)
        elif file_type == "json":
            df_target = pd.read_json(file_path)
        elif file_type == "xml":
            df_target = pd.read_xml(file_path, xpath=".//item")
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    elif origin_target == "TARGET DB":
        df_target = pd.read_sql(target_query, target_db)

    else:
        raise ValueError(f"Invalid target origin: {origin_target}")

    logger.info(f"Target Data:\n{df_target}")

    # ---------- Compare ----------
    df_source = df_source[df_target.columns]

    df_source = df_source.astype(str)
    df_target = df_target.astype(str)

    df_extra_in_expected = df_target[
        ~df_target.apply(tuple, axis=1).isin(df_source.apply(tuple, axis=1))
    ]

    df_extra_in_actual = df_source[
        ~df_source.apply(tuple, axis=1).isin(df_target.apply(tuple, axis=1))
    ]

    df_extra_in_expected.to_csv(
        f"Differences/extra_rows_in_expected_{test_case_name}.csv",
        index=False
    )

    df_extra_in_actual.to_csv(
        f"Differences/extra_rows_in_actual_{test_case_name}.csv",
        index=False
    )

    logger.info(f"Rows missing in target:\n{df_extra_in_expected}")
    logger.info(f"Extra rows in target:\n{df_extra_in_actual}")

    assert df_extra_in_expected.empty, (
        f"{test_case_name}: Rows present in expected but missing in target.\n"
        f"{df_extra_in_expected}"
    )

    assert df_extra_in_actual.empty, (
        f"{test_case_name}: Extra rows found in target.\n"
        f"{df_extra_in_actual}"
    )

    logger.info(f"{test_case_name} passed successfully.")

def unmask_response_statement(masked_sql, mapping, unmask=True):
    """
    Replaces masked identifiers in an SQL statement with their original names based on provided mappings.

    Parameters:
        masked_sql (str): The SQL statement with masked identifiers.
        mapping (dict): A dictionary containing mappings for schemas, tables, and columns.
        unmask (bool): whether to mask or to unmask - default=True

    Returns:
        str: The SQL statement with all identifiers replaced by their original names.

    Example:
        >>> masked_sql = 'SELECT column_1, column_2 FROM schema_1.table_1 WHERE column_3 > 100;'
        >>> mapping = {
        ...     'schemas': {'VEGGIES': 'schema_1'},
        ...     'tables': {'LU_SOIL_TYPE': 'table_1', 'ROOT_DEPTH': 'table_2'},
        ...     'columns': {'SOIL_TYPE': 'column_1', 'SOIL_DESCRIPTION': 'column_2', 'SOIL_TYPE_ID': 'column_3'}
        ... }
        >>> print(unmask_response_statement(masked_sql, mapping))
        SELECT SOIL_TYPE, SOIL_DESCRIPTION FROM VEGGIES.LU_SOIL_TYPE WHERE SOIL_TYPE_ID > 100;
    """
    # Reverse the mapping for easier lookup
    databases_rev = {v: k for k, v in mapping['databases'].items()}
    schemas_rev = {v: k for k, v in mapping['schemas'].items()}
    tables_rev = {v: k for k, v in mapping['tables'].items()}
    columns_rev = {v: k for k, v in mapping['columns'].items()}

    if unmask:
        # Unmask database names
        for masked, original in databases_rev.items():
            masked_sql = masked_sql.replace(masked, original)
        # Unmask schema names
        for masked, original in schemas_rev.items():
            masked_sql = masked_sql.replace(masked, original)

        # Unmask table names
        for masked, original in tables_rev.items():
            masked_sql = masked_sql.replace(masked, original)

        # Unmask column names
        for masked, original in columns_rev.items():
            masked_sql = masked_sql.replace(masked, original)

    else:
        # Mask schema names
        for masked, original in schemas_rev.items():
            masked_sql = masked_sql.replace(original, masked)

        # Unmask table names
        for masked, original in tables_rev.items():
            masked_sql = masked_sql.replace(original, masked)

        # Unmask column names
        for masked, original in columns_rev.items():
            masked_sql = masked_sql.replace(original, masked)

    return masked_sql

def mask_ddl_info_with_columns(ddl_info):
    """
    Masks table names, column names, and schema names in the provided DDL information, including modifications
    within the DDL statements to mask these identifiers consistently.

    Parameters:
        ddl_info (dict): The original DDL information as returned by `get_snowflake_ddl`.

    Returns:
        dict: The masked DDL information with all identifiers masked, maintaining structural consistency.
    """
    database_map = {}
    schema_map = {}
    table_map = {}
    column_map = {}
    masked_info = {}
    database_counter = 1
    schema_counter = 1
    table_counter = 1
    column_counter = 1

    # Helper function to generate masked DDL
    def generate_masked_ddl(ddl, databases, schemas, tables, columns):
        for original, masked in databases.items():
            ddl = ddl.replace(original, masked)
        for original, masked in schemas.items():
            ddl = ddl.replace(original, masked)
        for original, masked in tables.items():
            ddl = ddl.replace(f" {original, masked)  # Table names
        for original, masked in columns.items():
            ddl = ddl.replace(original, masked)  # Column names
        return ddl

    for key, value in ddl_info.items():
        original_database, original_schema, original_table, ddl = value['database'], value['schema'], value['name'], value['ddl']

        # Mask database
        if original_database not in database_map:
            database_map[original_database] = f"database_{database_counter}"
            database_counter += 1
        masked_database = database_map[original_database]

        # Mask schema
        if original_schema not in schema_map:
            schema_map[original_schema] = f"schema_{schema_counter}"
            schema_counter += 1
        masked_schema = schema_map[original_schema]

        # Mask table
        table_key = original_table
        if table_key not in table_map:
            table_map[table_key] = f"table_{table_counter}"
            table_counter += 1
        masked_table = table_map[table_key]

        # Extract and mask column names - Simplistic approach, assumes direct column references in DDL
        # A more robust implementation would parse the DDL structure to accurately identify column references
        columns_in_ddl = []  # Placeholder for column names extracted from DDL
        # Assuming column names are extracted, we replace each with a masked version
        for column in columns_in_ddl:
            if column not in column_map:
                column_map[column] = f"column_{column_counter}"
                column_counter += 1

        # Generate masked DDL including schema, table, and column names
        masked_ddl = generate_masked_ddl(ddl, database_map, schema_map, table_map, column_map)

        masked_key = f"{masked_database}.{masked_schema}.{masked_table} ({value['type']})"
        masked_info[masked_key] = {
            "database": masked_database,
            "schema": masked_schema,
            "name": masked_table,
            "type": value['type'],
            "ddl": masked_ddl
        }

    return masked_info, database_map, schema_map, table_map, column_map


import re


# def mask_identifier(identifier, identifier_map, prefix, counter):
#     """
#     Masks an identifier (schema, table, or column name) with a generic placeholder.
#     Updates the map with new identifiers and increments the counter for uniqueness.
#
#     Parameters:
#         identifier (str): The original identifier to mask.
#         identifier_map (dict): A map of original identifiers to their masked versions.
#         prefix (str): The prefix for the masked identifier (e.g., 'schema_', 'table_', 'column_').
#         counter (int): The current counter for the identifier type to ensure uniqueness.
#
#     Returns:
#         (str, int): The masked identifier and the updated counter.
#     """
#     if identifier not in identifier_map:
#         identifier_map[identifier] = f"{prefix}{counter}"
#         counter += 1
#     return identifier_map[identifier], counter
#
#
# def mask_ddl_info_with_columns(ddl_info):
#     """
#     Masks table names, column names, and schema names in the provided DDL information,
#     including modifications within the DDL statements to mask these identifiers consistently.
#
#     Parameters:
#         ddl_info (dict): The original DDL information as returned by `get_snowflake_ddl`.
#
#     Returns:
#         dict: The masked DDL information with all identifiers masked, maintaining structural consistency.
#
#     Example:
#         >>> ddl_info = {'public.table1': {'schema': 'public', 'name': 'table1', 'type': 'table', 'ddl': 'CREATE TABLE public.table1 (id INT, name STRING);'}}
#         >>> masked_info = mask_ddl_info_with_columns(ddl_info)
#         >>> list(masked_info.keys())[0].startswith('schema_1.table_1')
#         True
#         >>> 'CREATE TABLE schema_1.table_1' in masked_info[list(masked_info.keys())[0]]['ddl']
#         True
#     """
#     schema_map, table_map, column_map = {}, {}, {}
#     schema_counter, table_counter, column_counter = 1, 1, 1
#     masked_info = {}
#
#     for key, value in ddl_info.items():
#         original_schema, original_table, ddl = value['schema'], value['name'], value['ddl']
#
#         # Mask schema
#         masked_schema, schema_counter = mask_identifier(original_schema, schema_map, 'schema_', schema_counter)
#
#         # Mask table
#         masked_table, table_counter = mask_identifier(original_table, table_map, 'table_', table_counter)
#
#         # Extract and mask column names from DDL, assuming potential improvements for complex parsing
#         columns_in_ddl = re.findall(r'\b(\w+)\b(?=\s+\w+\()', ddl)  # Simplistic regex, adjust as needed
#         for column in set(columns_in_ddl):  # Ensure uniqueness before processing
#             if column.lower() not in ['create', 'table', 'int', 'string']:  # Exclude SQL keywords and common data types
#                 masked_column, column_counter = mask_identifier(column, column_map, 'column_', column_counter)
#                 ddl = re.sub(r'\b' + column + r'\b', masked_column, ddl)
#
#         # Generate masked DDL
#         for original, masked in schema_map.items():
#             ddl = ddl.replace(original, masked)
#         for original, masked in table_map.items():
#             ddl = ddl.replace(original, masked)
#
#         masked_key = f"{masked_schema}.{masked_table} ({value['type']})"
#         masked_info[masked_key] = {
#             "schema": masked_schema,
#             "name": masked_table,
#             "type": value['type'],
#             "ddl": ddl
#         }
#
#     return masked_info, schema_map, table_map, column_map

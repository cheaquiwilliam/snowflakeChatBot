import snowflake.connector
from typing import Dict


def get_snowflake_ddl(account: str, user: str, password: str, warehouse: str, database: str, role: str) -> \
        Dict[str, Dict[str, str]]:
    """
    Retrieves the DDL statements for tables and views in a specified Snowflake database.

    Parameters:
        account (str): Snowflake account identifier.
        user (str): Username for the Snowflake account.
        password (str): Password for the Snowflake account.
        warehouse (str): Warehouse to use for the session.
        database (str): Database from which to retrieve DDL statements.

    Returns:
        dict: A dictionary with keys as 'schema.table/view name' and values containing schema, name, type, and DDL.

    Example:
        >>> # Assuming valid credentials and database details are provided
        >>> info = get_snowflake_ddl('your_account', 'your_user', 'your_password', 'your_warehouse', 'your_database')
        >>> type(info)
        <class 'dict'>

    Notes:
        This function requires snowflake-connector-python package to be installed.
        Doctest and actual function calls requiring live credentials are commented out to avoid execution errors.

    Raises:
        Exception: If unable to connect to the database or execute queries.
    """
    # Import inside function to handle potential import errors and not require module-level dependency
    try:
        ctx = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            role=role,
            schema='PUBLIC'  # This can be parameterized as needed
        )

        objects_info = {}
        try:
            cursor = ctx.cursor()
            print('test')

            query = f"""
                SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
                FROM {database}.INFORMATION_SCHEMA.TABLES
                WHERE 
                    TABLE_SCHEMA != 'INFORMATION_SCHEMA'
                    AND TABLE_TYPE IN ('BASE TABLE', 'VIEW');
            """
            print(query)
            # Retrieve a list of all tables and views with their schema and type
            cursor.execute(query)
            for schema, name, type in cursor.fetchall():
                object_type = 'TABLE' if type == 'BASE TABLE' else 'VIEW'
                ddl_query = f"SELECT GET_DDL('{object_type}', '{database}.{schema}.{name}')"
                print(ddl_query)
                try:
                    cursor.execute(ddl_query)
                    ddl = cursor.fetchone()[0]  # Assuming GET_DDL returns a single row with a single column

                    key = f"{schema}.{name} ({object_type.lower()})"
                    objects_info[key] = {
                        "schema": schema,
                        "name": name,
                        "type": object_type.lower(),
                        "ddl": ddl
                    }
                except Exception as e:
                    print(e)
                    continue
        finally:
            cursor.close()
    except Exception as e:
        # Log or raise more specific exceptions as needed
        raise Exception(f"Error connecting to Snowflake or executing queries: {str(e)}")
    finally:
        if 'ctx' in locals() and ctx is not None:
            ctx.close()

    return objects_info


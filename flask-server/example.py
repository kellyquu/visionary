# #!/usr/bin/env python3
# """
# Test psycopg with CockroachDB for Screen Time Tracking.
# """

# import logging
# import os
# import random
# import time
# import uuid
# from argparse import ArgumentParser, RawTextHelpFormatter

# import psycopg
# from psycopg.errors import SerializationFailure, Error
# from psycopg.rows import namedtuple_row


# def create_accounts(conn):
#     id1 = uuid.uuid4()
#     id2 = uuid.uuid4()
#     with conn.cursor() as cur:
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS accounts (id UUID PRIMARY KEY, screen_time INT)"
#         )
#         cur.execute(
#             "UPSERT INTO accounts (id, screen_time) VALUES (%s, 120), (%s, 60)", (id1, id2))
#         logging.debug("create_accounts(): status message: %s",
#                       cur.statusmessage)
#     return [id1, id2]


# def delete_accounts(conn):
#     with conn.cursor() as cur:
#         cur.execute("DELETE FROM accounts")
#         logging.debug("delete_accounts(): status message: %s",
#                       cur.statusmessage)


# def print_screen_time(conn):
#     with conn.cursor() as cur:
#         print(f"Screen Time at {time.asctime()}:")
#         for row in cur.execute("SELECT id, screen_time FROM accounts"):
#             print("account id: {0}  Screen Time: {1} min".format(row.id, row.screen_time))


# def run_transaction(conn, op, max_retries=3):
#     """
#     Execute the operation *op(conn)* retrying serialization failure.

#     If the database returns an error asking to retry the transaction, retry it
#     *max_retries* times before giving up (and propagate it).
#     """
#     # leaving this block the transaction will commit or rollback
#     # (if leaving with an exception)
#     with conn.transaction():
#         for retry in range(1, max_retries + 1):
#             try:
#                 op(conn)

#                 # If we reach this point, we were able to commit, so we break
#                 # from the retry loop.
#                 return

#             except SerializationFailure as e:
#                 # This is a retry error, so we roll back the current
#                 # transaction and sleep for a bit before retrying. The
#                 # sleep time increases for each failed transaction.
#                 logging.debug("got error: %s", e)
#                 conn.rollback()
#                 logging.debug("EXECUTE SERIALIZATION_FAILURE BRANCH")
#                 sleep_seconds = (2**retry) * 0.1 * (random.random() + 0.5)
#                 logging.debug("Sleeping %s seconds", sleep_seconds)
#                 time.sleep(sleep_seconds)

#             except psycopg.Error as e:
#                 logging.debug("got error: %s", e)
#                 logging.debug("EXECUTE NON-SERIALIZATION_FAILURE BRANCH")
#                 raise e

#         raise ValueError(
#             f"transaction did not succeed after {max_retries} retries")


# def main():
#     opt = parse_cmdline()
#     logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
#     try:
#         # Attempt to connect to the cluster with the connection string provided to
#         # the script. By default, this script uses the value saved to the
#         # DATABASE_URL environment variable.
#         # For information on supported connection string formats, see
#         # https://www.cockroachlabs.com/docs/stable/connect-to-the-database.html.
#         db_url = opt.dsn
#         conn = psycopg.connect(db_url, 
#                                application_name="$ docs_simplecrud_psycopg3", 
#                                row_factory=namedtuple_row)
#         ids = create_accounts(conn)
#         print_screen_time(conn)  # Changed to print_screen_time
            
#         try:
#             run_transaction(conn, lambda conn: increment_screen_time(conn, ids))
#         except ValueError as ve:
#             # Below, we print the error and continue on so this example is easy to
#             # run (and run, and run...).  In real code you should handle this error
#             # and any others thrown by the database interaction.
#             logging.debug("run_transaction(conn, op) failed: %s", ve)
#             pass
#         except psycopg.Error as e:
#             logging.debug("got error: %s", e)
#             raise e

#         print_screen_time(conn)  # Changed to print_screen_time

#         # delete_accounts(conn)
#     except Exception as e:
#         logging.fatal("database connection failed")
#         logging.fatal(e)
#         return


# def increment_screen_time(conn, ids):
#     with conn.cursor() as cur:
#         for id in ids:
#             cur.execute(
#                 "UPDATE accounts SET screen_time = screen_time + 20 WHERE id = %s", (id,))
#     logging.debug("increment_screen_time(): status message: %s", cur.statusmessage)


# def parse_cmdline():
#     parser = ArgumentParser(description=__doc__,
#                             formatter_class=RawTextHelpFormatter)

#     parser.add_argument("-v", "--verbose",
#                         action="store_true", help="print debug info")

#     parser.add_argument(
#         "dsn",
#         default=os.environ.get("DATABASE_URL"),
#         nargs="?",
#         help="""\
# database connection string\
#  (default: value of the DATABASE_URL environment variable)
#             """,
#     )

#     opt = parser.parse_args()
#     if opt.dsn is None:
#         parser.error("database connection string not set")
#     return opt


# if __name__ == "__main__":
#     main()

import pymysql
import datetime
import os

HOST = '127.0.0.1'
USER = 'leonardo'
PASSWORD = 'rootwan'
DB = 'ico801'
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'dumps', f'backup_{datetime.date.today().isoformat()}.sql')

conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

with conn:
    with conn.cursor() as cur:
        cur.execute("SHOW TABLES")
        tables = [list(r.values())[0] for r in cur.fetchall()]

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as out:
        out.write(f"-- Backup generated: {datetime.datetime.now().isoformat()}\n")
        out.write(f"-- Database: {DB}\n\n")

        for table in tables:
            with conn.cursor() as cur:
                cur.execute(f"SHOW CREATE TABLE `{table}`")
                row = cur.fetchone()
                # The second value in the dict is the CREATE statement
                create_stmt = list(row.values())[1]

                out.write(f"-- Table structure for `{table}`\n")
                out.write(f"DROP TABLE IF EXISTS `{table}`;\n")
                out.write(create_stmt + ";\n\n")

                # Dump data
                cur.execute(f"SELECT * FROM `{table}`")
                rows = cur.fetchall()
                if not rows:
                    continue

                cols = list(rows[0].keys())
                col_list = ", ".join([f"`{c}`" for c in cols])

                batch_size = 200
                for i in range(0, len(rows), batch_size):
                    chunk = rows[i:i+batch_size]
                    values_sql = []
                    for r in chunk:
                        vals = []
                        for v in r.values():
                            if v is None:
                                vals.append('NULL')
                            elif isinstance(v, (int, float)):
                                vals.append(str(v))
                            else:
                                s = str(v)
                                s = pymysql.converters.escape_string(s)
                                vals.append("'" + s + "'")
                        values_sql.append("(" + ", ".join(vals) + ")")

                    out.write(f"INSERT INTO `{table}` ({col_list}) VALUES\n")
                    out.write(",\n".join(values_sql) + ";\n\n")

print('Backup written to:', OUTPUT_PATH)

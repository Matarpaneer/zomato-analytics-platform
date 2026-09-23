import pymysql

try:
    conn = pymysql.connect(
        unix_socket="/tmp/mysql.sock",
        user="root",
        database="zomato_profitability"
    )

    print(" Connected successfully!")

    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")

    print("Current Database:", cursor.fetchone()[0])

    conn.close()

except Exception as e:
    print(e)
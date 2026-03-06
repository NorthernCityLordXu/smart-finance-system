import pymysql

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password_123',
    'database': 'finance_db',
    'charset': 'utf8mb4'
}

def run_analysis():
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cursor:
            # A. 计算总支出
            cursor.execute("SELECT SUM(amount) FROM transactions")
            total = cursor.fetchone()[0]
            
            # B. 分类统计支出占比
            sql = """
            SELECT category, SUM(amount) as subtotal 
            FROM transactions 
            GROUP BY category 
            ORDER BY subtotal DESC
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            
            print("📊 --- Monthly Financial Report ---")
            print(f"Total Spending: ${total:.2f}\n")
            print("Breakdown by Category:")
            for row in results:
                cat, amt = row
                percentage = (amt / total) * 100
                print(f"- {cat:15}: ${amt:8.2f} ({percentage:5.2f}%)")
                
    finally:
        conn.close()

if __name__ == "__main__":
    run_analysis()
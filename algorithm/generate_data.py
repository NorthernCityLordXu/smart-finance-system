import pymysql
import random
from datetime import datetime, timedelta

# 1. 数据库连接配置 (对应你之前在 deploy/docker-compose.yml 里的设置)
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password_123', # 如果你改了密码，这里也要改
    'database': 'finance_db',
    'charset': 'utf8mb4'
}

# 2. 定义一些全英文的账单模板 (避开中文风险)
data_templates = {
    'Food': ['KFC Burger', 'Starbucks Latte', 'University Canteen', 'Supermarket Snacks'],
    'Transport': ['Uber Ride', 'Gasoline', 'Bus Ticket', 'Metro Top-up'],
    'Shopping': ['Amazon Book', 'Uniqlo T-shirt', 'Nike Shoes', 'Apple Store'],
    'Entertainment': ['Netflix Monthly', 'Movie Ticket', 'Steam Game', 'Gym Membership']
}

def start_generating(count=100):
    try:
        # 连接数据库
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # 先清空之前的测试数据，保持库里干净
        cursor.execute("TRUNCATE TABLE transactions")
        
        print(f"Starting to generate {count} records...")
        
        for i in range(count):
            category = random.choice(list(data_templates.keys()))
            description = random.choice(data_templates[category])
            amount = round(random.uniform(10.0, 300.0), 2)
            # 随机生成过去 30 天的时间
            random_days = random.randint(0, 30)
            date = datetime.now() - timedelta(days=random_days)
            
            sql = "INSERT INTO transactions (user_id, amount, category, description, transaction_date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (1, amount, category, description, date.strftime('%Y-%m-%d %H:%M:%S')))
        
        conn.commit()
        print(f"Success! 100 records are now in your D drive MySQL database.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    start_generating(100)
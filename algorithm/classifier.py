import pymysql

# 1. 数据库连接配置 (与之前一致)
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password_123',
    'database': 'finance_db',
    'charset': 'utf8mb4'
}

# 2. 建立你的“知识库” (关键词映射)
# 这一部分将来可以升级为机器学习模型
KNOWLEDGE_BASE = {
    'Food': ['KFC', 'Starbucks', 'Canteen', 'Dinner', 'Burger', 'Coffee', 'Supermarket', 
             '肯德基', '麦当劳', '食堂', '外卖', '晚餐', '吃饭', '超市', '奶茶', '火锅', '瑞幸'],
             
    'Transport': ['Uber', 'Gasoline', 'Bus', 'Metro', 'Taxi', 'Flight', 
                  '打车', '滴滴', '公交', '地铁', '加油', '机票', '高铁', '单车'],
                  
    'Shopping': ['Amazon', 'Uniqlo', 'Nike', 'Apple', 'Mall', 'Store', 
                 '淘宝', '京东', '买衣服', '买鞋', '商场', '购物', '拼多多'],
                 
    'Entertainment': ['Netflix', 'Movie', 'Steam', 'Gym', 'Cinema', 'Game', 
                      '电影', '网吧', '游戏', '健身房', '唱歌', 'KTV', '游乐园', '充值', '看剧']
}

def intelligent_classify():
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cursor:
            # A. 找出所有分类还没定的或者需要重新识别的账单
            cursor.execute("SELECT id, description FROM transactions")
            rows = cursor.fetchall()
            
            print(f"🤖 Brain is scanning {len(rows)} records...")
            
            update_count = 0
            for row in rows:
                row_id, desc = row
                detected_cat = "Unknown"
                
                # B. 匹配算法：在描述中搜索关键词
                for category, keywords in KNOWLEDGE_BASE.items():
                    if any(key.lower() in desc.lower() for key in keywords):
                        detected_cat = category
                        break
                
                # C. 如果识别到了新分类，更新数据库
                if detected_cat != "Unknown":
                    sql = "UPDATE transactions SET category = %s WHERE id = %s"
                    cursor.execute(sql, (detected_cat, row_id))
                    update_count += 1
            
            conn.commit()
            print(f"✅ Success! {update_count} records have been intelligently re-classified.")
            
    finally:
        conn.close()
# 把核心匹配逻辑抽离成一个独立的函数
def predict_category(desc: str) -> str:
    # 遍历你的知识库
    for category, keywords in KNOWLEDGE_BASE.items():
        # 如果描述中包含知识库里的关键词（忽略大小写）
        if any(key.lower() in desc.lower() for key in keywords):
            return category
            
    # 如果都没匹配上，返回 Unknown
    return "Unknown"
if __name__ == "__main__":
    intelligent_classify()
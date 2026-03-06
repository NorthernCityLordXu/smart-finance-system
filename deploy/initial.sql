-- 创建账单表
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,            -- 金额
    category VARCHAR(50) NOT NULL,            -- 分类（如：餐饮、交通）
    description TEXT,                         -- 账单描述
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP, -- 交易时间
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 清空旧数据
TRUNCATE TABLE transactions;

-- 插入英文测试数据
INSERT INTO transactions (user_id, amount, category, description) 
VALUES (1, 50.00, 'Food', 'Dinner at school canteen');

INSERT INTO transactions (user_id, amount, category, description) 
VALUES (1, 15.50, 'Transport', 'Taxi to library');
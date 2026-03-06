package com.financial.smart.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Table(name = "transactions") // 映射到你 D 盘 MySQL 里的表
@Data 
public class Transaction {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 🌟 新增这两行：告诉数据库，没传用户ID就默认算作 1号用户 的账单
    @Column(name = "user_id")
    private Long userId = 1L; 

    private Double amount;
    private String category;
    private String description;
    
    @Column(name = "transaction_date")
    private LocalDateTime transactionDate;
}
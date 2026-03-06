package com.financial.smart.repository;

import com.financial.smart.entity.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
// 继承 JpaRepository 后，Java 就自动学会了如何操作数据库里的 Transaction 对象
public interface TransactionRepository extends JpaRepository<Transaction, Long> {
}
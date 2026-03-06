package com.financial.smart.controller;

import com.financial.smart.entity.Transaction;
import com.financial.smart.repository.TransactionRepository;
import com.financial.smart.service.AiService; // 🌟 1. 引入我们刚写好的 AI 服务
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class TransactionController {

    @Autowired
    private TransactionRepository repository;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Autowired
    private AiService aiService; // 🌟 2. 实例化 AI 服务，让 Spring 帮你管理

    // 🌟 给 MySQL 做手术的临时接口 (保持不变)
    @GetMapping("/fix")
    public String fixDatabase() {
        try {
            jdbcTemplate.execute("ALTER TABLE transactions MODIFY id BIGINT AUTO_INCREMENT;");
            return "✅ 数据库手术成功！MySQL 终于学会自己生成 ID 了，快回去记账吧！";
        } catch (Exception e) {
            return "手术失败：" + e.getMessage();
        }
    }

    // 获取所有账单 (保持不变)
    @GetMapping("/all")
    public List<Transaction> getAllTransactions() {
        return repository.findAll();
    }

    // 🌟 新增账单 (重点改造这里！)
    @PostMapping("/add")
    public Transaction addTransaction(@RequestBody Transaction transaction) {
        
        // 1. 提取前端传过来的账单描述
        String description = transaction.getDescription();

        // 2. 如果描述不为空，就呼叫 Python 大脑算一下智能分类
        if (description != null && !description.trim().isEmpty()) {
            
            // 🚀 跨语言调用发生在这里！Java 瞬间去问 Python 拿结果
            String smartCategory = aiService.getSmartCategory(description);
            
            // 3. 把 AI 算出来的分类塞进这笔账单里
            transaction.setCategory(smartCategory);
            
            System.out.println("🤖 AI 拦截成功！描述: [" + description + "] -> 分类: [" + smartCategory + "]");
        } else {
            // 如果没填描述，给个默认兜底
            transaction.setCategory("Unknown");
        }

        // 4. 最后，把带着智能分类的账单存进 MySQL 数据库
        return repository.save(transaction);
    }
}
package com.financial.smart.service;

import com.financial.smart.dto.AiClassifyRequest;
import com.financial.smart.dto.AiClassifyResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service // 这个注解非常重要，把它注册为 Spring 的 Bean
public class AiService {

    // 你本地运行的 Python 算法微服务接口地址
private static final String AI_API_URL = "http://algorithm:8000/api/classify";
    /**
     * 传入账单描述，返回 AI 智能分类结果
     */
    public String getSmartCategory(String description) {
        // 创建一个用于发送 HTTP 请求的客户端
        RestTemplate restTemplate = new RestTemplate();

        // 1. 组装发给 Python 的请求数据 (快递盒)
        AiClassifyRequest request = new AiClassifyRequest();
        request.setDescription(description);

        try {
            // 2. 发送 POST 请求给 Python，并把返回的结果装进 AiClassifyResponse 盒子里
            AiClassifyResponse response = restTemplate.postForObject(
                    AI_API_URL,
                    request,
                    AiClassifyResponse.class
            );

            // 3. 拆开快递盒，把里面算好的 category (比如 "Food") 拿出来返回
            if (response != null && response.getCategory() != null) {
                return response.getCategory();
            }
        } catch (Exception e) {
            // 如果没开启 Python 服务，或者网络有问题，就会走到这里
            System.err.println("调用 Python AI 接口失败: " + e.getMessage());
        }

        // 如果调用失败，返回一个保底的默认分类
        return "Unknown";
    }
}
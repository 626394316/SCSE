/*
 Navicat Premium Data Transfer

 Source Server         : demo
 Source Server Type    : MySQL
 Source Server Version : 80035
 Source Host           : localhost:3306
 Source Schema         : historydata

 Target Server Type    : MySQL
 Target Server Version : 80035
 File Encoding         : 65001

 Date: 09/07/2024 16:44:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for qa_history
-- ----------------------------
DROP TABLE IF EXISTS `qa_history`;
CREATE TABLE `qa_history`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `talk_id` int NULL DEFAULT NULL,
  `talk_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `question` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `answer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `message` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `audio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qa_history
-- ----------------------------
INSERT INTO `qa_history` VALUES (21, 1, '2024/7/9 16:39:11', '你好', '你好😊，我是华侨大学开发的校园AI助手小H，我旨在为学生和老师提供更便捷、高效的服务。', '\"华侨大学AI助手小H：提供便捷高效服务的校园智能解决方案\"', NULL);
INSERT INTO `qa_history` VALUES (22, 1, '2024/7/9 16:39:16', '请介绍一下你自己', '你好😊，我是华侨大学开发的校园AI助手小H，我旨在为学生和老师提供更便捷、高效的服务。', '', NULL);
INSERT INTO `qa_history` VALUES (23, 1, '2024/7/9 16:39:42', '学校图书馆如何上网', '学校图书馆已实现无线WIFI(HQU)覆盖，登录个人上网账号即可在图书馆上网。如果账号存在故障，您可以直接在微信端进行报修。', '', NULL);
INSERT INTO `qa_history` VALUES (24, 1, '2024/7/9 16:39:55', '什么是差旅费', '差旅费是指教职工及相关人员（以下简称出差人员）临时到常驻地以外地区公务出差所发生的城市间交通费、住宿费、伙食补助费和市内交通费。', '', NULL);
INSERT INTO `qa_history` VALUES (25, 1, '2024/7/9 16:40:14', '华侨大学的校长是谁', '华侨大学的校长是吴剑平。', '', NULL);
INSERT INTO `qa_history` VALUES (26, 1, '2024/7/9 16:40:40', '明天的日期是什么时候', '明天的日期是2024年7月10日。', '', NULL);
INSERT INTO `qa_history` VALUES (27, 1, '2024/7/9 16:40:52', '帮我生成一张华侨大学的logo图片', '/web_demo/src/assets/llm_img/华侨大学logo.jpg', '', NULL);
INSERT INTO `qa_history` VALUES (29, 1, '2024/7/9 16:42:14', '帮我搜一篇关于Internlm的论文', '我找到了一篇关于Internlm的论文，标题为《InternLM-XComposer2：掌握自由形式的文字图像组合与视觉语言理解》。该论文由Xiaoyi Dong等人撰写，发表于2024年1月29日。论文摘要指出，他们引入了InternLM-XComposer2，这是一个在自由形式文字图像组合和理解方面表现出色的视觉语言模型。该模型超越了传统的视觉语言理解，能够从轮廓、详细文本说明和参考图像等多样化的输入中巧妙地编织出交织的文字图像内容，从而实现高度定制的内容创作。论文提出了一个名为Partial LoRA（PLoRA）的方法，该方法仅将额外的LoRA参数应用于图像令牌，以保留预训练的语言知识的完整性，同时在精确的视觉理解与文学才能的文字组合之间取得平衡。实验结果表明，基于InternLM2-7B的InternLM-XComposer2在生成高质量的长文本多模态内容以及在各种基准测试中的视觉语言理解性能方面表现出色，不仅显著优于现有的多模态模型，而且在某些评估中甚至超过了GPT-4V和Gemini Pro。该论文系列的7B参数模型在https://github.com/InternLM/InternLM-XComposer公开提供。', '', NULL);
INSERT INTO `qa_history` VALUES (30, 1, '2024/7/9 16:42:31', '肚子好饿 帮我点一份外卖', '您的外卖已经成功下单，是鱼香肉丝饭，总价为14.0元。已经从您的学生卡中自动支付。请稍等片刻，美食即将送达。', '', NULL);
INSERT INTO `qa_history` VALUES (32, 1, '2024/7/9 16:43:02', '帮我预定一下明天下午两点的图书馆的位置', '您的图书馆位置已经预定成功，时间是明天下午两点，座位号为1-75号。请记得按时前往就坐。', '', NULL);

SET FOREIGN_KEY_CHECKS = 1;

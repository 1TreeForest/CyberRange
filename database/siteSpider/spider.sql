/*
 Navicat Premium Data Transfer

 Source Server         : spider
 Source Server Type    : MySQL
 Source Server Version : 50529
 Source Host           : localhost:3306
 Source Schema         : spider

 Target Server Type    : MySQL
 Target Server Version : 50529
 File Encoding         : 65001

 Date: 16/01/2022 13:20:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for querys
-- ----------------------------
DROP TABLE IF EXISTS `querys`;
CREATE TABLE `querys`  (
  `keyword` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  INDEX `keyword`(`keyword`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of querys
-- ----------------------------
INSERT INTO `querys` VALUES ('在线影院');
INSERT INTO `querys` VALUES ('在线观看');
INSERT INTO `querys` VALUES ('影视资源');
INSERT INTO `querys` VALUES ('电影下载');
INSERT INTO `querys` VALUES ('电影分享');
INSERT INTO `querys` VALUES ('电影资源');

-- ----------------------------
-- Table structure for results
-- ----------------------------
DROP TABLE IF EXISTS `results`;
CREATE TABLE `results`  (
  `domain` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `keyword` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`domain`, `keyword`) USING BTREE,
  INDEX `keyword`(`keyword`) USING BTREE,
  CONSTRAINT `keyword` FOREIGN KEY (`keyword`) REFERENCES `querys` (`keyword`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of results
-- ----------------------------
INSERT INTO `results` VALUES ('baike.baidu.com', '在线电影 - 百度百科', 'https://baike.baidu.com/error.html?status=403&uri=/item/%E5%9C%A8%E7%BA%BF%E7%94%B5%E5%BD%B1/5218404?fr=aladdin', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('detail.zol.com.cn', '【家庭影院】家庭影院报价及图片大全-ZOL中关村在线', 'https://detail.zol.com.cn/home-theater/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('ent.cri.cn', '电影_文娱频道_国际在线', 'http://ent.cri.cn/movie/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('ent.qq.com', '在线电影--娱乐频道--腾讯网', 'https://ent.qq.com/movie/yingyuan_index.shtml', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('kan.sogou.com', '搜狗影视-热播电影,热播电视剧免费在线观看', 'http://kan.sogou.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('m.iprow.com', '神马影院在线观看_叫神马_神马电影网 -神马影视手机版', 'http://m.iprow.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('m.kan.sogou.com', '搜狗影视-最新电影,最新电视剧免费在线观看', 'http://m.kan.sogou.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('movie.chuangxiang360.com', '在线播放,免费看电影,在线看电影,最全电影,最新电影', 'http://movie.chuangxiang360.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('movie.pptv.com', '电影', 'http://movie.pptv.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('tieba.baidu.com', '手机在线影院-吧友热议 - 百度贴吧', 'https://tieba.baidu.com/hottopic/browse/hottopic?topic_id=797730', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('tv.2345.com', '在线免费电影_有什么好看的电影推荐_电影排行榜2022【2345...', 'https://tv.2345.com/top/rank.html', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('tv.iqxbf.com', '零度影视|零度影院|线报坊影视网|在线免费高清电影', 'http://tv.iqxbf.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('tv.sohu.com', '搜狐电影频道 - 搜狐视频', 'https://tv.sohu.com/movie/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('v.baidu.com', '经典成年人 文艺电影_成年人 文艺电影在线观看_hao123影视', 'http://v.baidu.com/recommend/dianying/?kw=%E6%88%90%E5%B9%B4%E4%BA%BA+%E6%96%87%E8%89%BA', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('v.hao123.baidu.com', '好看的电视剧电影综艺动漫视频平台,热门高清视频在线观看_...', 'http://v.hao123.baidu.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('v.qq.com', '电影频道—高清电影在线观看—腾讯视频', 'https://v.qq.com/p/movie/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('vip.1905.com', '电影电视剧—高清正版视频在线观看—1905电影网', 'https://vip.1905.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('vip.qiqivoip.com', '影视大全_最新电影电视剧在线观看 _ 奇奇影院', 'https://vip.qiqivoip.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('vod.foxue.org', '中国佛教电影网-佛教电影网_佛教电影_佛教电影大全_佛教视...', 'http://vod.foxue.org/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.0430.com', '中国在线电影网站导航 - 中国网站库', 'http://www.0430.com/cn/film/onlinemovies/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.1905.com', '高清影院-最新电影-好看的电影-在线观看-电影网', 'https://www.1905.com/vod/?_t_t_t=0.6796881488990039', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.558cq.com', '酷猫电影网_最新电影_免费看片_手机看片神器', 'http://www.558cq.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.56.com', '青苹果影院_视频在线观看 - 56.com', 'https://www.56.com/w72/album-aid-13284913.html', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.5zcake.com', '星辰影院-2021最新热门电影电视剧在线观看', 'http://www.5zcake.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.adfcra.com', '谍战迷_热播排行榜电视剧电影动漫综艺在线免费观看全集播放', 'http://www.adfcra.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.ayzjj.cn', '星辰影院首页-2020vip热播电视剧电影高清免费在线观看-星...', 'http://www.ayzjj.cn/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.bilibili.com', '更追影院 - 免费最新在线观看电影,电视剧 - 哔哩哔哩', 'https://www.bilibili.com/read/cv8445309/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.cc123.com', '最新电影电视剧免费在线观看_免费电影在线观看 - 虫虫影视', 'https://www.cc123.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.cfc.com.cn', '中影·国际影城官网|电影|在线预订电影票|电影票团购|中影...', 'http://www.cfc.com.cn/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.cinema.com.cn', '四川省电影公司、太平洋电影院线、太平洋电影网_www.cinem...', 'http://www.cinema.com.cn/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.cqysw.com', '传奇影视网-在线电影-最新电影-免费电影-电影在线观看', 'http://www.cqysw.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.dfmtchina.com', '免费高清电影在线观看 _ 星辰影院', 'http://www.dfmtchina.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.dytt002.com', '电影天堂 - 神马高清影视在线观看影院,MP4下载网', 'https://www.dytt002.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.fun.tv', '风行- 高清电影,网络电视,免费电影,在线电影,电影下载', 'https://www.fun.tv/download/home/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.gcjxgj.cn', '极速影院首页-极速影院在线免费观看电影电视剧-极速电影网', 'http://www.gcjxgj.cn/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.hanhuahb.com', '爱看影院 - 最新热播电影电视剧在线看「爱看影视」', 'http://www.hanhuahb.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.iqiyi.com', '电影- 最新电影在线观看-电影天堂-爱奇艺', 'https://www.iqiyi.com/dianying/normal.html', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.iwaybook.com', '最新电影电视剧免费在线观看 _ 喝茶影院', 'http://www.iwaybook.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.jd.com', '在线影院 - 京东', 'https://www.jd.com/hprm/9847b31839a5aa758f81.html', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.kaimeilai.com', '免费电影_免费高分电影_免费动画片在线观看', 'http://www.kaimeilai.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.kqcra.com', '策驰影院_在线免费观看全集完整版电影电视剧动漫综艺播放', 'http://www.kqcra.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.letv.com', '首页- 乐融官网', 'http://www.letv.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.lol5s.com', '...下载_2019最新电影_百度云资源_电影电视剧在线观看_五...', 'https://www.lol5s.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.manmankan.com', '漫漫看影视剧 - 最好的电视剧和电影天堂', 'http://www.manmankan.com/dy2013/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.meiju56.com', '美剧网-全网最全影视库', 'https://www.meiju56.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.mtime.com', 'Mtime时光网:让电影遇见生活', 'http://www.mtime.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.muslimwww.com', '电影- 穆斯林在线(muslimwww)', 'http://www.muslimwww.com/html/video/dianying/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.ngys.cc', '南瓜影视|南瓜影院|全网vip电影视频免费在线观看', 'http://www.ngys.cc/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.nongminys.com', '农民影视|农民影院|最新电视剧|全网vip电影免费在线观看', 'http://www.nongminys.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.nxc5.com', '全民影院-最新电影在线看_热播电视剧_在线电影院', 'http://www.nxc5.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.omnijoi.cn', '幸福蓝海国际影城官网|电影|在线预订电影票|电影票团购|幸...', 'http://www.omnijoi.cn/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.pcpop.com', '泡泡网_PCPOP.com - 新科技•购鲜活', 'https://www.pcpop.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.putclub.com', '在线影院', 'https://www.putclub.com/html/AandV/movie/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.stt100.com', '最新电影在线观看 最新电视剧在线观看 _ 小小影视', 'http://www.stt100.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.sysfzy.cn', '扫一扫在线电影-最新电影-免费电影-电影在线观看', 'http://www.sysfzy.cn/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.szzs360.com', '球幕|球幕影院_数字展示在线球幕影院频道', 'http://www.szzs360.com/qmxt/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.unisure.com.cn', '「星辰影院」免费在线观看最新热播电影电视剧-星辰影院首页', 'https://www.unisure.com.cn/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.wandafilm.com', '万达电影', 'http://www.wandafilm.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.wanyilianhe.com', '极速影院首页-新版极速影院免费在线观看电视剧电影', 'http://www.wanyilianhe.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.wxykzg.com', '悟空电影网 - 悟空韩国电影免费观看|悟空电影高清在线观看', 'http://www.wxykzg.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.wzdq.com', '雅图在线影院', 'https://www.wzdq.com/site/www.yatu.tv.shtml', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.xagc120.net', '依恋影院在线观看', 'http://www.xagc120.net/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.youku.com', '优酷在线- 你的热爱 正在热播', 'https://www.youku.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('www.yszxwang.com', '影视在线网 最新电影在线观看 最新电视剧在线观看', 'https://www.yszxwang.com/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('xxc.la', '南瓜影院_最新电影电视剧视频在线观看_最新影视_南瓜影院', 'https://xxc.la/', '在线影院', '2022-01-16');
INSERT INTO `results` VALUES ('yl.szhk.com', '好看的电影、最新电影、电影排行榜-深港在线电影推荐栏目', 'http://yl.szhk.com/movie/', '在线影院', '2022-01-16');

SET FOREIGN_KEY_CHECKS = 1;

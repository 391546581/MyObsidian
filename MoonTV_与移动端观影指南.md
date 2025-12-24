# MoonTV 部署、视频源配置及移动端观影指南

> 本文档总结了 2024-2025 年主流的自建影视系统 MoonTV (LunaTV) 的部署流程、资源站配置、网盘挂载以及移动端多平台观影方案。

---

## 一、 MoonTV (LunaTV) K8s 部署要点

### 1. 架构逻辑
MoonTV 是一个基于 Next.js 开发的影视聚合系统，本身不存储视频文件。
- **前端/接口层**：处理用户搜索、播放逻辑。
- **存储层 (Redis)**：存储视频源配置、播放记录、收藏等。

### 2. 部署关键配置
- **镜像选择**：`ghcr.io/moontechlab/lunatv:latest`
- **环境变量**：
  - `REDIS_URL`: `redis://moontv-redis-service:6379` (K8s 内部集群访问)
  - `USERNAME` / `PASSWORD`: 管理后台登录凭证。
- **访问地址**：
  - 客户端：`http://[IP]:30030/`
  - 管理后台：`http://[IP]:30030/admin`

---

## 二、 视频源与订阅配置 (核心)

### 1. 苹果 CMS 资源站 (JSON 模板)
将以下内容填入后台 **「配置文件设置」**，实现全网聚合搜索：

```json
{
  "api_site": [
    { "key": "douban", "name": "🎬 豆瓣资源", "api": "https://caiji.dbzy5.com/api.php/provide/vod/at/json/" },
    { "key": "wolong", "name": "🎬 卧龙资源", "api": "https://wolongzyw.com/api.php/provide/vod/at/json/" },
    { "key": "liangzi", "name": "🎬 量子资源", "api": "https://cj.lzcaiji.com/api.php/provide/vod/at/json/" }
  ],
  "custom_category": [
    { "name": "电影", "type": "movie" },
    { "name": "电视剧", "type": "tv" }
  ],
  "cache_time": 3600
}
```

### 2. 订阅链接获取
- **GitHub 稳定源**：`https://raw.githubusercontent.com/hafrey1/LunaTV-config/main/LunaTV-config.txt`
- **获取渠道**：GitHub (搜索 LunaTV)、Linux.do 社区、Telegram (TVBox 频道)。

---

## 三、 网盘与 AList 增强方案

### 1. 网盘聚合搜索 (NetDisk)
配置后可直接搜索阿里云盘、夸克等资源。
```json
{
  "NetDiskConfig": {
    "enabled": true,
    "pansouUrl": "https://so.252035.xyz",
    "enabledCloudTypes": ["aliyun", "quark", "baidu"]
  }
}
```

### 2. 小雅 AList (免登录/直播直连)
通过 AList 的 VOD 接口，实现网盘资源像点播一样“点开即播”：
- **公共 API**：`http://alist.xiaoya.pro/vod`
- **价值**：小雅后端维护了几百个阿里云盘，用户无需点击分享链接，直接在 MoonTV 内浏览播放。

---

## 四、 移动端 (手机) 最佳实践

### 1. Android (最强聚合)
- **影视仓 (内置版)**：最推荐，内置百条高清线路，安装即用。
- **FongMi (蜂蜜)**：UI 最精美，支持多版本 TVBox 订阅链接。

### 2. iOS (系统方案)
- **伪装 App**：搜索“马甲包”（如 A 影视），通过特定暗号解锁。
- **浏览器方案**：使用 **Alook 浏览器** 访问站点，支持嗅探投屏。

### 3. 高质量影视站 (Web 版)
| 站点名称 | 网址 | 特色 |
| :--- | :--- | :--- |
| **低端影视** | [ddys.pro](https://ddys.pro) | 画质天花板，1080P/4K 无广告 |
| **素白白影视** | subaibai.mx | 界面现代，国产剧更新极快 |
| **厂长资源** | czzy77.com | 资源最全，冷门/美剧必备 |

---

## 五、 总结与建议
- **家庭大屏**：由 Minikube/Kind 部署 MoonTV 投屏。
- **移动便携**：首选 **影视仓内置版** (Android) 或 **低端影视** (iOS/Web)。
- **极致画质**：开启 **网盘搜索** 或自建 **AList**。

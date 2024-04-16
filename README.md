# 词频分析

## 爬取数据

1. 安装依赖

```shell
cd news
pip install -r requirements.txt
```

2. 创建数据库

连接到数据库，执行如下 SQL 语句创建数据库：

```sql
CREATE DATABASE `news` CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci';
```

3. 运行爬虫

```shell
scrapy crawl news
```

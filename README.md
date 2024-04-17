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

3. 修改 `news/settings.py` 中的 `DATABASE_URL` 为对应的数据库连接地址，例如：

```python
DATABASE_URL = "mysql+pymysql://root:123456@192.168.88.129/news?charset=utf8mb4"
```

4. 运行爬虫

```shell
scrapy crawl news
```

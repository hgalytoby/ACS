# 遷移

```
# 初始化設定
alembic init myAlembic

# 新增遷移文件
alembic revision --autogenerate -m "Change column data type"

# 執行遷移文件更新資料庫
alembic upgrade head

# 回到上一個版本
alembic downgrade -1

# 查看歷史遷移記錄
alembic history

# 查看當前版本的遷移記錄
alembic current
```

### arq

```
# 啟動
arq app.utils.worker.WorkerSettings
```
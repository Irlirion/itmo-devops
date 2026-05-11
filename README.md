# Лабораторная работа 3: GitHub Actions CI/CD для Apache Airflow + Apache Spark

Выполнила команда **Chat Gpt 10**.

## О чём эта работа

В этой лабораторной работа из ЛР2 упакована в CI/CD pipeline на GitHub Actions. Pipeline проверяет структуру проекта, валидирует Python-файлы и Docker Compose конфигурацию, собирает Docker-образ и выполняет деплой через Docker Compose по правилам из задания.

Основа приложения осталась из ЛР2: Apache Airflow запускает Spark-задачу через `SparkSubmitOperator`, а вычисления выполняются на отдельном Spark-кластере.

## CI/CD pipeline

Workflow находится в `.github/workflows/lab3-ci-cd.yml`.

| Job | Когда запускается | Что делает |
|---|---|---|
| `test` | Всегда, во всех ветках | Проверяет наличие `dags/`, `spark/`, `Dockerfile`, `docker-compose.yml`; компилирует Python-файлы; валидирует Docker Compose |
| `build` | После `test`; автоматически не запускается для `feature/*` | Собирает Docker-образ Airflow |
| `deploy` | Автоматически только для `main`, `master`, `develop`; вручную через `workflow_dispatch` с `deploy=true` | Выполняет `docker compose up -d --build` |

Все jobs закреплены за runner label `ubuntu-latest` через `runs-on`. В GitHub Actions это аналог выбора tagged runner в GitLab CI/CD. Если нужен self-hosted runner, ему можно добавить отдельный label, например `lab3-cicd`, и заменить `runs-on` в workflow.

## Что делает пайплайн

DAG `spark_data_pipeline` запускает один Spark-джоб, который:

1. Генерирует 50 случайных чисел и создаёт из них Spark DataFrame
2. Считает статистику — сумму, среднее, минимум и максимум
3. Трансформирует данные — умножает каждое число на 2 и фильтрует те, что выше среднего
4. Сохраняет результат в файл `/opt/airflow/output/spark_result.json`

## Сервисы

| Сервис | Адрес | Описание |
|---|---|---|
| Airflow UI | http://localhost:8080 | Управление DAG-ами (airflow / airflow) |
| Spark Master UI | http://localhost:4040 | Мониторинг кластера и выполненных задач |

## Как запустить

Нужен Docker и Docker Compose. Больше ничего устанавливать не требуется.

**1. Собрать образы и поднять все сервисы:**

```bash
docker-compose up -d --build
```

**2. Подождать, пока всё стартует** (обычно 2–3 минуты):

```bash
docker-compose ps
```

Все контейнеры должны перейти в статус `healthy`.

**3. Открыть Airflow UI** по адресу http://localhost:8080, логин и пароль — `airflow`.

**4. Запустить DAG** `spark_data_pipeline` вручную через кнопку ▶ в интерфейсе.

**5. Убедиться в успехе** — DAG должен завершиться со статусом `success`, а в Spark UI на http://localhost:4040 появиться выполненное приложение в разделе *Completed Applications*.

> Подключение `spark_local` к кластеру Spark создаётся автоматически при первом запуске — вручную ничего настраивать не нужно.

## Остановка

```bash
docker-compose down -v
```

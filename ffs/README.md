# 💸 Трекер Личных Финансов

Веб-приложение на Django для управления и отслеживания личных финансов. Пользователи могут фильтровать записи, добавлять доходы и расходы, а также организовывать их по категориям и подкатегориям.

---

## 🚀 Возможности

- 📋 Создание, редактирование и удаление финансовых записей
- 🔎 Динамическая фильтрация по типу, статусу, категории, подкатегории и диапазону дат
- 📂 Структура категорий и подкатегорий
- 🗂 Чистое и понятное отображение таблицы
- 🏠 Домашняя страница для удобной навигации

---

## 🛠️ Технологии

- Python 3.12.6  
- Django 5.1.6  
- HTML / CSS  
- SQLite (база данных по умолчанию)

---

## 📁 Структура проекта

```
ffs/
│
├── core/                   # Приложение для учета финансов
│   ├── migrations/
│   ├── templates/
│   │   └── finance/
│   │       ├── base.html
│   │       ├── record_list.html
│   │       ├── record_form.html
│   │       └── record_confirm_delete.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│
├── ffs/
│   ├── settings.py
│   ├── urls.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

## 📦 Установка

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/makoster/finance-tracker.git
cd finance-tracker
```

2. **Создайте виртуальное окружение**
```bash
python -m venv venv
source venv/bin/activate   # Для Windows: venv\Scripts\activate
```

3. **Установите зависимости**
```bash
pip install -r requirements.txt
```

4. **Выполните миграции**
```bash
python manage.py migrate
```

5. **Создайте суперпользователя**
```bash
python manage.py createsuperuser
```

6. **Запустите сервер**
```bash
python manage.py runserver
```

7. **Откройте приложение**
```
http://127.0.0.1:8000/
```

---

## 📄 Модели

```python
class Category(models.Model):
    name = models.CharField(...)

class SubCategory(models.Model):
    name = models.CharField(...)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class FinanceRecord(models.Model):
    TYPE_CHOICES = [('REPLENISHMENT', 'Пополнение'), ('WITHDRAW', 'Снятие')]
    STATUS_CHOICES = [('CONFIRMED', 'Подтверждено'), ('PENDING', 'В ожидании')]

    type = models.CharField(choices=TYPE_CHOICES)
    status = models.CharField(choices=STATUS_CHOICES)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    sum = models.DecimalField(...)
    date = models.DateField(...)
```

---

## 🌐 Маршруты

| Путь              | Представление                 | Описание                         |
|------------------|-------------------------------|----------------------------------|
| `/`              | `home_view`                   | Главная страница                 |
| `/records/`      | `FinanceRecordListView`       | Список и фильтрация записей      |
| `/create/`       | `FinanceRecordCreateView`     | Добавление новой записи          |
| `/edit/<pk>/`    | `FinanceRecordUpdateView`     | Редактирование существующей записи |
| `/delete/<pk>/`  | `FinanceRecordDeleteView`     | Удаление записи                  |

---

## 🎯 Планируемые улучшения

- Аутентификация пользователей  
- Экспорт в CSV или Excel  
- Адаптивная верстка  
- Графики и аналитика  

---

## 📃 Лицензия

Проект распространяется под лицензией MIT. Вы можете свободно использовать и улучшать его.

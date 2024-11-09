# پروژه Marzban API Client - کلاینت پایتون برای Marzban API

این پروژه شامل یک کلاینت پایتون برای API سرویس **Marzban** است مرزبان یک پنل مدیریت پروکسی است که امکان مدیریت چند صد حساب پروکسی را با قدرت و دسترسی بالا فراهم میکند. این کلاینت تمامی سرویس‌های موجود در API مرزبان را به‌صورت کامل پیاده‌سازی کرده و امکان استفاده آسان از توابع مختلف آن را در اختیار توسعه‌دهندگان قرار می‌دهد.

## امکانات

- **مدیریت کامل کاربران**: اضافه، ویرایش، حذف و دریافت اطلاعات کاربران.
- **مدیریت ادمین**: امکان ایجاد، حذف، و ویرایش ادمین‌ها.
- **دسترسی به وضعیت سیستم**: مشاهده وضعیت هسته‌ی سیستم، تنظیمات، آمار مصرف پهنای باند و...
- **مدیریت گره‌ها (Nodes)**: امکان افزودن، ویرایش، حذف و دریافت اطلاعات گره‌های فعال.
- **دریافت لینک اشتراک کاربران**: تولید لینک‌های اشتراک مختلف برای دستگاه‌های گوناگون.
- **قابلیت اتصال به Marzban API**: دسترسی و استفاده از تمامی امکانات API به‌صورت متمرکز در قالب یک کلاینت پایتون.

## پیش‌نیازها

- پایتون نسخه 3.8 یا بالاتر
- نصب کتابخانه‌های لازم که در بخش بعدی توضیح داده شده‌اند

## نصب

۱. ابتدا این مخزن را کلون کنید:
   ```bash
   git clone https://github.com/username/marzban-api-client.git
   cd marzban-api-client
   ```

۲. سپس پکیج‌های مورد نیاز را از طریق فایل `requirements.txt` نصب کنید:
   ```bash
   pip install -r requirements.txt
   ```

## نحوه استفاده

پس از نصب، می‌توانید از کلاینت API استفاده کنید. در زیر مثال‌هایی از نحوه‌ی استفاده از این کلاینت آورده شده است:

### ۱. احراز هویت

برای شروع، ابتدا نیاز دارید که توکن دسترسی را از API دریافت کنید. از این توکن برای تمام درخواست‌ها استفاده خواهد شد.

```python
from marzban_api_client import MarzbanAPI

# مقداردهی اولیه کلاینت
api = MarzbanAPI(base_url="https://api.example.com")

# احراز هویت و دریافت توکن دسترسی
api.authenticate(username="admin", password="password")
```

### ۲. مدیریت کاربران

اضافه کردن کاربر جدید به Marzban:

```python
from marzban_api_client.models import UserCreate

user_data = UserCreate(
    username="new_user",
    proxies={"vmess": {"id": "proxy_id"}},
    expire=30,  # تعداد روزهای اعتبار
    data_limit=500,  # محدودیت داده به مگابایت
)

new_user = api.add_user(user_data=user_data)
print("New User: ", new_user)
```

### ۳. دریافت اطلاعات سیستم

برای دریافت وضعیت سیستم می‌توانید از کد زیر استفاده کنید:

```python
system_stats = api.get_system_stats()
print("وضعیت سیستم:", system_stats)
```

### ۴. مدیریت گره‌ها (Nodes)

اضافه کردن گره جدید:

```python
from marzban_api_client.models import NodeCreate

node_data = NodeCreate(name="New Node", address="192.168.1.1")
new_node = api.add_node(node_data=node_data)
print("گره جدید اضافه شد:", new_node)
```

### ۵. دریافت لینک اشتراک کاربر

با استفاده از توکن کاربر، لینک اشتراک آن را دریافت کنید:

```python
subscription = api.get_user_subscription(token="user_token")
print("لینک اشتراک کاربر:", subscription.subscription_url)
```
## مشارکت در پروژه

اگر تمایل دارید که در توسعه این پروژه مشارکت کنید، مراحل زیر را دنبال کنید:

۱. این مخزن را فورک کنید.
۲. یک شاخه جدید ایجاد کنید:
   ```bash
   git checkout -b feature/your-feature
   ```
۳. تغییرات خود را اعمال کنید و کامیت کنید.
   ```bash
   git commit -m "Add some feature"
   ```
۴. تغییرات خود را به مخزن اصلی پوش کنید.
   ```bash
   git push origin feature/your-feature
   ```
۵. یک Pull Request ایجاد کنید.


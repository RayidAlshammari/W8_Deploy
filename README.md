# 📋 Task Management System

نظام إدارة المهام مبني بـ FastAPI (Backend) + واجهة مستخدم عصرية (Frontend)

## 🚀 تشغيل المشروع

### الطريقة الأولى: تشغيل Development Server

```bash
fastapi dev src/fatsAPI/main.py
```

### الطريقة الثانية: تشغيل Production Server

```bash
fastapi run src/fatsAPI/main.py
```

بعد تشغيل المشروع، افتح المتصفح على:

- **الواجهة الأمامية**: http://127.0.0.1:8000/
- **API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative API Docs (ReDoc)**: http://127.0.0.1:8000/redoc

---

## 📁 هيكل المشروع

```
src/fatsAPI/
├── main.py              # نقطة بداية التطبيق
├── routers/
│   ├── users.py         # API endpoints للمستخدمين
│   └── tasks.py         # API endpoints للمهام
├── schemas/
│   └── models.py        # Pydantic models والتحقق
└── frontend/
    ├── index.html       # الصفحة الرئيسية
    ├── css/style.css    # التصميم
    └── js/app.js        # Logic الواجهة
```

---

## ✨ المميزات

### Backend (FastAPI)
- ✅ إدارة المستخدمين (3 أدوار: admin, manager, team_member)
- ✅ إدارة المهام (مع الأولويات والحالات)
- ✅ التحقق من البيانات بـ Pydantic
- ✅ Filtering متقدم
- ✅ CORS enabled

### Frontend
- ✅ تصميم عصري بـ Glassmorphism
- ✅ واجهة تفاعلية
- ✅ Toast notifications
- ✅ Real-time filtering
- ✅ Responsive design

---

## 📝 API Endpoints

### Users
- `GET /users/` - قائمة المستخدمين (مع فلترة حسب الدور)
- `POST /users/` - إنشاء مستخدم جديد
- `GET /users/{user_id}` - معلومات مستخدم محدد

### Tasks
- `GET /tasks/` - قائمة المهام (مع فلاتر متعددة)
- `POST /tasks/` - إنشاء مهمة جديدة
- `GET /tasks/{task_id}` - معلومات مهمة محددة
- `PUT /tasks/{task_id}` - تحديث مهمة

---

## 🔧 المتطلبات

```bash
# تثبيت FastAPI
pip install "fastapi[standard]"
```

---

## 📚 التوثيق

راجع ملف `project_summary.md` في مجلد الـ artifacts لتفاصيل أكثر عن:
- هيكل البيانات
- قواعد التحقق
- أمثلة على الـ API responses

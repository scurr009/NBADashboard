# 🚀 Quick Deploy Checklist

**Goal**: Get your dashboard live in 30 minutes!

---

## ✅ Files Ready (Already Done!)

- [x] `gunicorn` added to requirements.txt
- [x] `server = app.server` added to app_modern.py  
- [x] `render.yaml` created
- [x] All code tested and working

**You're ready to deploy!**

---

## 📝 Deployment Steps

### **Step 1: GitHub** (10 min)

```bash
cd "c:\Projects\NBA Dashboard"
git init
git add .
git commit -m "Ready for deployment"

# Create repo on github.com first, then:
git remote add origin https://github.com/YOUR_USERNAME/nba-dashboard.git
git push -u origin main
```

**Replace YOUR_USERNAME with your GitHub username!**

---

### **Step 2: Render** (5 min)

1. Go to https://render.com
2. Sign up with GitHub (free, no credit card)
3. Click "New +" → "Web Service"
4. Connect your `nba-dashboard` repo
5. Verify settings:
   - Build: `pip install -r requirements.txt && python etl/pipeline.py`
   - Start: `gunicorn dashboard.app_modern:server --bind 0.0.0.0:$PORT`
   - Plan: **Free**
6. Click "Create Web Service"

---

### **Step 3: Wait** (10-15 min)

Watch Render build your app:
- Installing packages...
- Running ETL pipeline...
- Starting dashboard...
- **Done!** ✅

---

### **Step 4: Share!**

Your URL: `https://YOUR-APP-NAME.onrender.com`

Share with:
- Friends
- Family  
- Employers
- Social media

---

## 🎯 That's It!

**3 steps, 30 minutes, free website!**

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

---

## 🔄 To Update Later

```bash
# Make changes
git add .
git commit -m "Updated dashboard"
git push

# Render auto-deploys!
```

---

## ⚠️ Remember

- Free tier sleeps after 15 min (wakes in 30 sec)
- First visit after sleep is slow, then fast
- Perfect for hobby projects!

---

**Ready? Start with Step 1!** 🚀

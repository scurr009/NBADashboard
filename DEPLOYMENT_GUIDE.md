# 🚀 Deployment Guide - Get Your Free Website!

**Goal**: Deploy your NBA Dashboard to a free public website  
**Time**: 20-30 minutes  
**Cost**: $0 (completely free)  
**Result**: A URL anyone can visit

---

## ✅ Pre-Deployment Checklist

Your dashboard is **ready to deploy!** We've already added:

- [x] `gunicorn` to requirements.txt
- [x] `server = app.server` to app_modern.py
- [x] `render.yaml` configuration file
- [x] All necessary files in place

---

## 📝 Step-by-Step Deployment

### **Step 1: Push to GitHub** (10 minutes)

#### 1.1 Create GitHub Account (if needed)
- Go to https://github.com
- Sign up (free)

#### 1.2 Create New Repository
1. Click "+" → "New repository"
2. Name: `nba-dashboard` (or whatever you want)
3. Description: "Professional NBA Analytics Dashboard"
4. **Keep it Public** (required for free Render)
5. **Don't** initialize with README (you already have one)
6. Click "Create repository"

#### 1.3 Push Your Code
Open terminal in your project folder and run:

```bash
cd "c:\Projects\NBA Dashboard"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/nba-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username!

---

### **Step 2: Sign Up for Render** (3 minutes)

1. Go to https://render.com
2. Click "Get Started for Free"
3. Click "Sign in with GitHub" (easiest option)
4. Authorize Render to access your GitHub
5. **No credit card required!**

---

### **Step 3: Create Web Service** (5 minutes)

#### 3.1 Connect Repository
1. In Render dashboard, click "New +" → "Web Service"
2. Click "Connect account" if needed
3. Find your `nba-dashboard` repository
4. Click "Connect"

#### 3.2 Configure Service
Render will auto-detect settings from `render.yaml`, but verify:

- **Name**: `nba-dashboard` (or your choice)
- **Region**: Oregon (or closest to you)
- **Branch**: `main`
- **Build Command**: 
  ```
  pip install -r requirements.txt && python etl/pipeline.py
  ```
- **Start Command**: 
  ```
  gunicorn dashboard.app_modern:server --bind 0.0.0.0:$PORT
  ```
- **Plan**: **Free** ⭐

#### 3.3 Deploy!
1. Click "Create Web Service"
2. Render will start building your app
3. Watch the logs (it's cool!)

---

### **Step 4: Wait for Deployment** (10-15 minutes)

You'll see Render:
1. ✅ Clone your repository
2. ✅ Install Python packages
3. ✅ Run ETL pipeline (load NBA data)
4. ✅ Start your dashboard
5. ✅ Assign you a URL!

**Your URL will look like:**
```
https://nba-dashboard-abc123.onrender.com
```

---

## 🎉 Success! You're Live!

### **What You Get:**
- ✅ Public URL (share with anyone!)
- ✅ SSL certificate (https://)
- ✅ Automatic deployments (push to GitHub = auto-update)
- ✅ 750 hours/month free
- ✅ Professional hosting

### **Share Your Dashboard:**
```
https://YOUR-APP-NAME.onrender.com
```

Send this link to:
- Friends & family
- Potential employers
- Social media
- Your resume/portfolio

---

## 🔧 How to Update Your Dashboard

### **After Initial Deployment:**

1. Make changes locally
2. Test them: `python dashboard/app_modern.py`
3. Commit changes:
   ```bash
   git add .
   git commit -m "Updated dashboard"
   git push
   ```
4. Render **automatically** rebuilds and deploys!
5. Wait 5-10 minutes
6. Your changes are live!

---

## ⚠️ Important Notes

### **Free Tier Limitations:**
- **Sleeps after 15 minutes** of inactivity
- **Takes 30 seconds** to wake up on first visit
- Then works normally
- For a hobby project, this is **totally fine!**

### **Want Always-On?**
Upgrade to Render Starter ($7/month):
- No sleep
- Faster performance
- Custom domain support

### **Data Updates:**
Your data is currently static (1947-2025). To update:
1. Replace `NBA_Player_Totals.csv` with new data
2. Push to GitHub
3. Render rebuilds automatically

---

## 🐛 Troubleshooting

### **Build Failed?**
Check Render logs for errors. Common issues:
- Missing package in requirements.txt
- Python version mismatch
- File path issues

**Solution**: Check logs, fix issue, push to GitHub

### **App Won't Start?**
- Check that `server = app.server` is in app_modern.py
- Verify gunicorn is in requirements.txt
- Check Render logs for specific error

### **Slow to Load?**
- First load after sleep takes 30 seconds (normal)
- Subsequent loads are fast
- Upgrade to paid plan for always-on

### **Can't Find Your URL?**
- Go to Render dashboard
- Click your service
- URL is at the top

---

## 📊 What's Deployed

### **Files Uploaded to Render:**
```
NBA Dashboard/
├── dashboard/
│   ├── app_modern.py      ← Your dashboard
│   └── assets/
│       └── style.css      ← Styling
├── data/
│   ├── duckdb/
│   │   └── nba.db         ← Database (created during build)
│   └── processed/
│       └── nba_players_clean.parquet ← Data (created during build)
├── etl/                   ← Data pipeline
├── requirements.txt       ← Dependencies
└── render.yaml           ← Deployment config
```

### **What Happens During Build:**
1. Install Python packages
2. Run `etl/pipeline.py` (creates database)
3. Start dashboard with gunicorn
4. Dashboard is live!

---

## 🎯 Quick Reference

### **Your URLs:**
- **GitHub**: https://github.com/YOUR_USERNAME/nba-dashboard
- **Render**: https://dashboard.render.com
- **Dashboard**: https://YOUR-APP-NAME.onrender.com

### **Useful Commands:**
```bash
# Update dashboard
git add .
git commit -m "Description of changes"
git push

# Check deployment status
# Go to: https://dashboard.render.com

# View logs
# Click your service → Logs tab
```

---

## 🌟 Next Steps

### **After Deployment:**

1. **Test your live dashboard**
   - Visit your URL
   - Try all the filters
   - Check performance

2. **Share it!**
   - Add to resume/portfolio
   - Post on LinkedIn
   - Share with friends

3. **Monitor usage**
   - Check Render dashboard
   - View logs
   - See visitor stats

4. **Keep improving**
   - Add features
   - Fix bugs
   - Push updates

---

## 💡 Pro Tips

### **Custom Domain (Optional)**
Want `nba.yourdomain.com` instead of `xyz.onrender.com`?
1. Buy domain ($10-15/year)
2. Upgrade to Render Starter ($7/month)
3. Add custom domain in Render settings
4. Update DNS records

### **Environment Variables**
Need to hide API keys or secrets?
1. Go to Render dashboard
2. Click your service
3. Environment → Add variable
4. Use in code: `os.environ.get('SECRET_KEY')`

### **Monitoring**
Want to know when your app is down?
1. Use UptimeRobot (free)
2. Monitors your URL
3. Emails you if it goes down

---

## ✅ Deployment Checklist

Before you start:
- [ ] GitHub account created
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Repository connected to Render
- [ ] Service configured
- [ ] Deployment started

After deployment:
- [ ] Dashboard loads successfully
- [ ] All filters work
- [ ] Charts display correctly
- [ ] URL shared with others
- [ ] Tested on mobile/desktop

---

## 🎉 You're Done!

**Congratulations!** Your NBA Dashboard is now live on the internet!

**What you've accomplished:**
- ✅ Built a professional analytics dashboard
- ✅ Deployed it to the cloud
- ✅ Got a free public website
- ✅ Can share it with anyone

**This is portfolio-worthy work!** 🏆

---

## 📞 Need Help?

### **Resources:**
- Render Docs: https://render.com/docs
- Dash Docs: https://dash.plotly.com
- Your project docs: See `docs/` folder

### **Common Issues:**
- Check `docs/quick_reference/troubleshooting.md`
- Review Render logs
- Google the error message

---

**Ready to deploy? Follow Step 1 above!** 🚀

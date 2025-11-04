# 🏀 NBA Analytics Dashboard

Professional, interactive analytics dashboard for NBA player statistics (1947-2025).

**Live Demo**: [Your Render URL here]

![Dashboard Preview](https://via.placeholder.com/800x400?text=NBA+Dashboard+Screenshot)

---

## ✨ Features

- **5,411 Players** across 78 seasons (1947-2025)
- **29,508 Player-Season Records** with comprehensive stats
- **Interactive Filters**: Metric, Top N, Year Range, Team, Position, Player
- **Fast Queries**: < 100ms average query time
- **Professional Design**: Milliman-inspired dark sidebar, muted colors
- **Grouped Team Dropdown**: Modern Teams (current 30) vs Historical Teams

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/nba-dashboard.git
cd nba-dashboard

# Install dependencies
pip install -r requirements.txt

# Run ETL pipeline (first time only)
python etl/pipeline.py

# Start the dashboard
python dashboard/app_modern.py
```

Open your browser to **http://localhost:8051**

---

## 📊 Data

### Source
NBA player totals dataset (1947-2025 seasons)
- **File**: `data/raw/NBA_Player_Totals.csv` (29MB)
- **Records**: 29,508 player-season combinations
- **Players**: 5,411 unique players

### Metrics
- **Total Points** - Career points scored
- **Total Rebounds** - Career rebounds
- **Total Assists** - Career assists
- **Total Steals** - Career steals
- **Total Blocks** - Career blocks

---

## 🏗️ Project Structure

```
NBA Dashboard/
├── dashboard/
│   ├── app_modern.py          # Main dashboard application
│   └── assets/
│       └── style.css          # Custom styling
│
├── etl/
│   ├── extract.py             # Data extraction
│   ├── transform.py           # Data cleaning & enrichment
│   ├── load.py                # DuckDB loading & indexing
│   ├── pipeline.py            # ETL orchestration
│   └── analyze_data.py        # Data profiling
│
├── data/
│   ├── raw/
│   │   └── NBA_Player_Totals.csv
│   ├── processed/
│   │   └── nba_players_clean.parquet  (generated)
│   └── duckdb/
│       └── nba.db                      (generated)
│
├── framework/                 # Reusable patterns for other projects
├── README.md                  # This file
├── DEPLOYMENT.md              # Deployment guide
├── requirements.txt           # Python dependencies
├── render.yaml                # Render deployment config
└── .gitignore                 # Git ignore rules
```

---

## 💻 Tech Stack

- **Dashboard**: [Dash](https://dash.plotly.com/) + [Plotly](https://plotly.com/)
- **Database**: [DuckDB](https://duckdb.org/) (embedded OLAP)
- **Storage**: Parquet (columnar format)
- **Deployment**: [Render](https://render.com/) (free tier)
- **Python**: 3.11+

---

## 🎨 Design

### Color Palette (Milliman Professional)
- **Sidebar**: #2C3E50 (dark blue-gray)
- **Background**: #F5F5F5 (light gray)
- **Primary**: #3498DB (professional blue)
- **Charts**: Sage green, Mustard, Coral, Teal (muted, professional)

### Typography
- **Large, readable fonts** (15-17px minimum)
- **High contrast** for accessibility
- **Professional, clean** aesthetic

---

## 🚢 Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed instructions.

### Quick Deploy to Render (Free)

1. Push to GitHub
2. Connect to Render
3. Deploy automatically
4. Get your free URL!

**Time**: ~30 minutes  
**Cost**: $0 (free tier)

---

## 📈 Performance

- **Query Time**: < 100ms average
- **Data Load**: < 2 seconds
- **Dashboard Startup**: < 3 seconds
- **Database Size**: 12MB (DuckDB)
- **Memory Usage**: ~150MB

---

## 🎯 Use Cases

- **Portfolio Project**: Demonstrate data engineering & visualization skills
- **Learning**: Study ETL pipelines, DuckDB, Dash
- **Analysis**: Explore NBA player statistics interactively
- **Template**: Use as foundation for other analytics dashboards

---

## 🔄 Updating Data

To update with new NBA data:

1. Replace `data/raw/NBA_Player_Totals.csv` with updated file
2. Run ETL pipeline: `python etl/pipeline.py`
3. Restart dashboard: `python dashboard/app_modern.py`

---

## 🛠️ Development

### Running Locally
```bash
python dashboard/app_modern.py
```

### Running ETL Only
```bash
python etl/pipeline.py
```

### Data Analysis
```bash
python etl/analyze_data.py
```

---

## 📚 Documentation

- **Main README**: This file
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Framework**: See `framework/` folder for reusable patterns
- **Code**: Well-commented throughout

---

## 🤝 Contributing

This is a personal portfolio project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - feel free to use this project as a template for your own dashboards!

---

## 🙏 Acknowledgments

- **NBA Data**: Basketball Reference
- **Design Inspiration**: Milliman Medicare Intelligence Dashboard
- **Tech Stack**: Dash, Plotly, DuckDB communities

---

## 📧 Contact

**Your Name**  
[Your Email]  
[Your LinkedIn]  
[Your GitHub]

---

## 🎓 Learning Resources

Built this dashboard? Check out the `framework/` folder for:
- Reusable patterns
- Design principles
- Code templates
- Deployment guides

Use these to build your own analytics dashboards with different datasets!

---

**⭐ If you found this helpful, please star the repository!**

---

*Last updated: November 2025*

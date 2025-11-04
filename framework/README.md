# 🎯 Dashboard Builder Framework

**Reusable patterns and templates for building professional analytics dashboards**

Based on learnings from the NBA Analytics Dashboard project.

---

## 📁 What's In This Folder

### `MASTER_PLAN.md`
Complete plan for building a generalized dashboard builder that works with any dataset.

### `guides/`
Step-by-step guides for common tasks:
- `getting_started.md` - How to start a new dashboard project
- `code_standards.md` - Coding conventions and best practices
- `deployment.md` - How to deploy dashboards

### `patterns/`
Proven design patterns and architectures:
- `architecture.md` - System design patterns
- `etl_pattern.md` - Data pipeline structure
- `design_principles.md` - UI/UX best practices
- `visualization.md` - Chart and graph guidelines

### `templates/`
Ready-to-use code templates:
- `dashboard_template.py` - Dash app boilerplate
- `etl_template.py` - ETL pipeline boilerplate
- `render.yaml` - Deployment configuration

---

## 🚀 Quick Start

### To Build a New Dashboard:

1. **Copy this framework folder** to your new project
2. **Read** `guides/getting_started.md`
3. **Use** templates from `templates/`
4. **Follow** patterns from `patterns/`
5. **Deploy** using `guides/deployment.md`

---

## 🎓 Key Learnings

### What Works ✅
- **DuckDB + Parquet** - Fast, embedded, perfect for analytics
- **Dark sidebar + light content** - Professional, readable
- **Counting stats** - Simple aggregations, easy to understand
- **Top N selector** - Flexible without complexity
- **Text inputs** - Better UX than sliders
- **Muted colors** - Professional, not distracting

### What Doesn't ❌
- **Cascading filters** - Too complex, unreliable
- **Complex calculations** - Start simple
- **Small fonts** - Hard to read
- **Bright colors** - Not professional
- **Multiple callbacks** - Unnecessary complexity

---

## 📊 Proven Tech Stack

- **Dashboard**: Dash + Plotly
- **Database**: DuckDB (embedded OLAP)
- **Storage**: Parquet (columnar)
- **Deployment**: Render (free tier)
- **Version Control**: Git + GitHub

---

## 🎨 Design System

### Colors (Milliman Professional)
```python
COLORS = {
    'sidebar_bg': '#2C3E50',      # Dark blue-gray
    'sidebar_text': '#ECF0F1',    # Light text
    'background': '#F5F5F5',      # Light gray
    'primary': '#3498DB',         # Professional blue
    'chart_colors': [
        '#8FBC8F',  # Sage green
        '#DAA520',  # Mustard
        '#CD853F',  # Coral
        '#5F9EA0',  # Teal
    ]
}
```

### Typography
- **Title**: 32px, bold
- **Subtitle**: 16px
- **Labels**: 13px
- **Axis**: 15px
- **Legend**: 15px

---

## 🔄 ETL Pattern

```python
# Extract
df = pd.read_csv('data.csv')

# Transform
df = clean_data(df)
df = add_derived_metrics(df)

# Load
con = duckdb.connect('database.db')
con.execute("CREATE TABLE...")
con.execute("CREATE INDEX...")
```

---

## 📱 Dashboard Pattern

```python
# Layout
app.layout = html.Div([
    html.Div([...], style={'sidebar'}),  # Filters
    html.Div([...], style={'content'})   # Chart
])

# Callback
@app.callback(...)
def update_chart(filters):
    query = build_query(filters)
    df = execute_query(query)
    fig = create_chart(df)
    return fig
```

---

## 🎯 Success Criteria

A good dashboard should be:
- ✅ **Fast** - Queries < 1 second
- ✅ **Simple** - Easy to use
- ✅ **Professional** - Polished design
- ✅ **Flexible** - Multiple filters
- ✅ **Reliable** - No errors
- ✅ **Documented** - Clear README

---

## 📚 Additional Resources

### In NBA Dashboard Project
- Main README
- DEPLOYMENT.md
- Code examples in `dashboard/` and `etl/`

### External
- Dash docs: https://dash.plotly.com
- DuckDB docs: https://duckdb.org
- Plotly charts: https://plotly.com/python

---

## 💡 Tips

1. **Start simple** - Add complexity only when needed
2. **Test early** - Run queries before building UI
3. **Document as you go** - Future you will thank you
4. **Follow patterns** - Don't reinvent the wheel
5. **Deploy early** - Catch issues sooner

---

**This framework represents 40+ hours of iteration and refinement. Use it wisely!** 🚀

---

*Based on NBA Analytics Dashboard (November 2025)*

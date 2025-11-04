# 🚀 Getting Started - Build Your Own Dashboard

**Use this guide to create a new analytics dashboard with a different dataset**

Based on proven patterns from the NBA Analytics Dashboard.

---

## 📋 Prerequisites

- Python 3.11+
- Your dataset (CSV, Excel, or Parquet)
- Basic Python knowledge
- 2-4 hours of time

---

## 🎯 Step-by-Step Guide

### Step 1: Set Up Project Structure (10 min)

```bash
# Create new project folder
mkdir my-dashboard
cd my-dashboard

# Create folder structure
mkdir dashboard etl data
mkdir data/raw data/processed data/duckdb
mkdir dashboard/assets

# Copy framework files
cp -r ../nba-dashboard/framework/templates/* .
```

### Step 2: Prepare Your Data (30 min)

1. **Place your CSV** in `data/raw/your_data.csv`

2. **Analyze your data**:
   - What are the dimensions? (categories for filters)
   - What are the metrics? (numbers to aggregate)
   - Is there a time dimension?
   - Any unique identifiers?

3. **Example**:
   ```
   Sales Data:
   - Dimensions: region, product_category, sales_rep
   - Metrics: revenue, units_sold, profit
   - Time: date
   - ID: transaction_id
   ```

---

### Step 3: Build ETL Pipeline (60 min)

#### 3.1 Extract (`etl/extract.py`)

```python
import pandas as pd

def extract_data(file_path):
    """Read your data file"""
    df = pd.read_csv(file_path)
    print(f"✅ Extracted {len(df)} rows")
    return df
```

#### 3.2 Transform (`etl/transform.py`)

```python
def transform_data(df):
    """Clean and enrich your data"""
    
    # Handle missing values
    df = df.dropna(subset=['important_column'])
    
    # Convert data types
    df['date'] = pd.to_datetime(df['date'])
    df['revenue'] = df['revenue'].astype(float)
    
    # Add derived columns (if needed)
    df['profit_margin'] = df['profit'] / df['revenue']
    
    print(f"✅ Transformed {len(df)} rows")
    return df
```

#### 3.3 Load (`etl/load.py`)

```python
import duckdb

def load_data(df, db_path):
    """Load into DuckDB"""
    
    con = duckdb.connect(db_path)
    
    # Create table
    con.execute("CREATE TABLE sales AS SELECT * FROM df")
    
    # Create indexes for filter columns
    con.execute("CREATE INDEX idx_region ON sales(region)")
    con.execute("CREATE INDEX idx_date ON sales(date)")
    
    # Export to Parquet
    con.execute("COPY sales TO 'data/processed/sales.parquet'")
    
    print(f"✅ Loaded to {db_path}")
    con.close()
```

#### 3.4 Pipeline (`etl/pipeline.py`)

```python
from extract import extract_data
from transform import transform_data
from load import load_data

def run_pipeline():
    # Extract
    df = extract_data('data/raw/your_data.csv')
    
    # Transform
    df = transform_data(df)
    
    # Load
    load_data(df, 'data/duckdb/your_data.db')
    
    print("✅ ETL Pipeline Complete!")

if __name__ == '__main__':
    run_pipeline()
```

---

### Step 4: Build Dashboard (90 min)

#### 4.1 Define Your Configuration

```python
# dashboard/app.py

import duckdb
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go

# Connect to database
con = duckdb.connect('data/duckdb/your_data.db', read_only=True)

# Define your metrics
METRICS = {
    'revenue': {'name': 'Total Revenue', 'agg': 'SUM'},
    'units': {'name': 'Units Sold', 'agg': 'SUM'},
    'profit': {'name': 'Total Profit', 'agg': 'SUM'},
}

# Get filter options
regions = con.execute("SELECT DISTINCT region FROM sales ORDER BY region").fetchdf()
products = con.execute("SELECT DISTINCT product_category FROM sales ORDER BY product_category").fetchdf()
```

#### 4.2 Create Layout

```python
app = Dash(__name__)

app.layout = html.Div([
    # Sidebar with filters
    html.Div([
        html.H1('My Dashboard'),
        
        # Metric selector
        html.Label('Metric'),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[{'label': v['name'], 'value': k} for k, v in METRICS.items()],
            value='revenue'
        ),
        
        # Region filter
        html.Label('Region'),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': 'All', 'value': 'ALL'}] + 
                    [{'label': r, 'value': r} for r in regions['region']],
            value='ALL'
        ),
        
        # Date range
        html.Label('Date Range'),
        dcc.DatePickerRange(
            id='date-range',
            start_date='2020-01-01',
            end_date='2024-12-31'
        ),
        
    ], style={'width': '280px', 'padding': '20px', 'backgroundColor': '#2C3E50'}),
    
    # Main content with chart
    html.Div([
        dcc.Graph(id='main-chart')
    ], style={'flex': '1', 'padding': '20px'}),
    
], style={'display': 'flex'})
```

#### 4.3 Add Callback

```python
@app.callback(
    Output('main-chart', 'figure'),
    [Input('metric-dropdown', 'value'),
     Input('region-dropdown', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_chart(metric, region, start_date, end_date):
    metric_info = METRICS[metric]
    
    # Build query
    where_clauses = [f"date BETWEEN '{start_date}' AND '{end_date}'"]
    if region != 'ALL':
        where_clauses.append(f"region = '{region}'")
    
    where_clause = " AND ".join(where_clauses)
    
    # Query data
    query = f"""
        SELECT date, {metric_info['agg']}({metric}) as value
        FROM sales
        WHERE {where_clause}
        GROUP BY date
        ORDER BY date
    """
    
    df = con.execute(query).fetchdf()
    
    # Create chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['value'],
        mode='lines+markers',
        name=metric_info['name']
    ))
    
    fig.update_layout(
        title=metric_info['name'],
        xaxis_title='Date',
        yaxis_title=metric_info['name']
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)
```

---

### Step 5: Test Locally (15 min)

```bash
# Run ETL
python etl/pipeline.py

# Start dashboard
python dashboard/app.py

# Open browser
# http://localhost:8050
```

**Test**:
- All filters work
- Chart displays correctly
- Queries are fast
- No errors in console

---

### Step 6: Deploy (30 min)

See `deployment.md` for detailed instructions.

**Quick steps**:
1. Push to GitHub
2. Connect to Render
3. Deploy!

---

## 🎨 Customization

### Change Colors

```python
COLORS = {
    'sidebar_bg': '#2C3E50',      # Your color
    'background': '#F5F5F5',       # Your color
    'primary': '#3498DB',          # Your color
}
```

### Add More Filters

```python
# In layout
html.Label('Your Filter'),
dcc.Dropdown(
    id='your-filter',
    options=[...],
    value='default'
),

# In callback
Input('your-filter', 'value')
```

### Change Chart Type

```python
# Bar chart
fig.add_trace(go.Bar(x=df['x'], y=df['y']))

# Scatter plot
fig.add_trace(go.Scatter(x=df['x'], y=df['y'], mode='markers'))

# Pie chart
fig = go.Figure(data=[go.Pie(labels=df['category'], values=df['value'])])
```

---

## 📊 Common Patterns

### Top N Analysis

```python
query = f"""
    SELECT product, SUM(revenue) as total
    FROM sales
    WHERE {where_clause}
    GROUP BY product
    ORDER BY total DESC
    LIMIT {top_n}
"""
```

### Time Series

```python
query = f"""
    SELECT DATE_TRUNC('month', date) as month, SUM(revenue) as total
    FROM sales
    WHERE {where_clause}
    GROUP BY month
    ORDER BY month
"""
```

### Grouped Analysis

```python
query = f"""
    SELECT region, product, SUM(revenue) as total
    FROM sales
    WHERE {where_clause}
    GROUP BY region, product
    ORDER BY total DESC
"""
```

---

## ✅ Checklist

Before deploying:
- [ ] ETL pipeline runs without errors
- [ ] Dashboard loads locally
- [ ] All filters work
- [ ] Charts display correctly
- [ ] Queries are fast (< 1 second)
- [ ] README updated
- [ ] requirements.txt complete
- [ ] .gitignore configured

---

## 🐛 Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Database locked"
```python
# Use read_only connection
con = duckdb.connect('database.db', read_only=True)
```

### "Slow queries"
```python
# Add indexes
con.execute("CREATE INDEX idx_column ON table(column)")
```

### "Chart not updating"
```python
# Check callback inputs/outputs match
# Check query returns data
print(df.head())
```

---

## 📚 Resources

- **NBA Dashboard**: See parent project for complete example
- **Dash Docs**: https://dash.plotly.com
- **DuckDB Docs**: https://duckdb.org
- **Plotly Charts**: https://plotly.com/python

---

## 🎯 Next Steps

1. **Build your dashboard** following this guide
2. **Customize** colors, layout, filters
3. **Deploy** to Render for free
4. **Share** your work!

---

**Questions? Review the NBA Dashboard code for a complete working example!**

---

*Based on NBA Analytics Dashboard patterns (November 2025)*

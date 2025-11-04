# Template Adaptation Guide
## Using This Template for New Projects

**Target Audience**: Teams starting new analytics projects  
**Time to Adapt**: 1-2 days for basic adaptation  
**Prerequisites**: Understanding of your data and requirements

---

## Table of Contents
1. [When to Use This Template](#when-to-use-this-template)
2. [Adaptation Checklist](#adaptation-checklist)
3. [Step-by-Step Adaptation](#step-by-step-adaptation)
4. [Common Adaptations](#common-adaptations)
5. [Example Scenarios](#example-scenarios)
6. [What to Keep vs Change](#what-to-keep-vs-change)

---

## When to Use This Template

### ✅ Good Fit

**Use this template if your project has:**
- Analytical/reporting requirements (not transactional)
- Tabular data (rows and columns)
- Read-heavy workload (more queries than writes)
- Single-machine deployment acceptable
- Need for interactive dashboard
- Dataset size: thousands to billions of rows
- Python development team

**Example Projects:**
- Sales analytics dashboard
- Customer behavior analysis
- Financial reporting
- IoT sensor data analysis
- Log analysis and monitoring
- Sports statistics
- Healthcare analytics
- E-commerce metrics

---

### ❌ Not a Good Fit

**Don't use this template if you need:**
- Real-time streaming (use Kafka/Flink)
- Transactional system (use PostgreSQL/MySQL)
- Multi-user write-heavy app (use traditional RDBMS)
- Distributed computing (use Spark/Dask)
- Graph data (use Neo4j)
- Document storage (use MongoDB)
- Sub-millisecond latency (use Redis/in-memory)

---

## Adaptation Checklist

### Phase 1: Planning
- [ ] Identify data sources (CSV, API, database, etc.)
- [ ] Define data grain (what does one row represent?)
- [ ] List required transformations
- [ ] Identify key metrics and dimensions
- [ ] Define dashboard requirements
- [ ] Estimate data volume (current and future)

### Phase 2: Setup
- [ ] Copy folder structure
- [ ] Update project name in files
- [ ] Customize requirements.txt (add/remove dependencies)
- [ ] Update .gitignore for your data files
- [ ] Create project README

### Phase 3: ETL Adaptation
- [ ] Adapt extract.py for your data source
- [ ] Customize transform.py for your business logic
- [ ] Update load.py schema for your fields
- [ ] Modify pipeline.py orchestration if needed
- [ ] Update analyze_data.py for your columns

### Phase 4: Dashboard Adaptation
- [ ] Design dashboard layout
- [ ] Identify required filters
- [ ] Choose visualization types
- [ ] Update queries for your schema
- [ ] Customize styling/branding

### Phase 5: Documentation
- [ ] Update data dictionary
- [ ] Document transformation decisions
- [ ] Create user guide
- [ ] Update README with your project details

---

## Step-by-Step Adaptation

### Step 1: Copy Template Structure

```bash
# Create new project from template
cp -r "NBA Dashboard" "My Analytics Project"
cd "My Analytics Project"

# Clean out NBA-specific data
rm data/raw/*.csv
rm data/duckdb/*.db
rm data/processed/*.parquet

# Update project name
# Edit README.md, requirements.txt, etc.
```

---

### Step 2: Adapt Data Extraction

**Original (NBA CSV)**:
```python
# etl/extract.py
def extract_csv(self, filename='NBA_Player_Totals.csv'):
    csv_path = self.data_dir / filename
    df = pd.read_csv(csv_path)
    return df
```

**Adapted for Your Data**:

**Example A: Different CSV**
```python
def extract_csv(self, filename='sales_data.csv'):
    csv_path = self.data_dir / filename
    
    # Custom parsing for your CSV
    df = pd.read_csv(
        csv_path,
        encoding='utf-8',
        parse_dates=['order_date', 'ship_date'],
        dtype={'customer_id': str, 'amount': float}
    )
    return df
```

**Example B: Database Source**
```python
def extract_from_database(self, query):
    """Extract from PostgreSQL"""
    import psycopg2
    
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    logger.info(f"Extracted {len(df):,} rows from database")
    return df
```

**Example C: API Source**
```python
def extract_from_api(self, endpoint, params=None):
    """Extract from REST API"""
    import requests
    
    url = f"{self.base_url}/{endpoint}"
    headers = {'Authorization': f'Bearer {self.api_key}'}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    data = response.json()
    df = pd.DataFrame(data['results'])
    
    logger.info(f"Extracted {len(df):,} rows from API")
    return df
```

---

### Step 3: Customize Transformations

**Identify Your Transformations**:
1. What duplicates need removing?
2. What values need standardizing?
3. What missing data needs handling?
4. What derived metrics to calculate?
5. What filters to apply?

**Template Pattern**:
```python
# etl/transform.py
def transform_data(df):
    df = remove_duplicates(df)
    df = standardize_values(df)
    df = handle_missing_values(df)
    df = add_derived_metrics(df)
    df = filter_data(df)
    return df
```

**Your Adaptation**:
```python
def transform_sales_data(df):
    """Transform sales data"""
    # 1. Remove test orders
    df = df[df['customer_id'] != 'TEST']
    
    # 2. Standardize country codes
    country_map = {'US': 'USA', 'UK': 'GBR', ...}
    df['country'] = df['country'].map(country_map)
    
    # 3. Handle missing values
    df['discount'] = df['discount'].fillna(0)
    
    # 4. Calculate metrics
    df['profit'] = df['revenue'] - df['cost']
    df['margin'] = df['profit'] / df['revenue']
    
    # 5. Filter valid orders
    df = df[df['status'] == 'completed']
    
    return df
```

---

### Step 4: Update Database Schema

**Original (NBA Schema)**:
```python
CREATE TABLE players (
    player_id INTEGER,
    player VARCHAR,
    season INTEGER,
    team VARCHAR,
    points INTEGER,
    ...
)
```

**Your Schema**:
```python
CREATE TABLE sales (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE,
    product_id VARCHAR NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DOUBLE NOT NULL,
    discount DOUBLE DEFAULT 0,
    revenue DOUBLE NOT NULL,
    cost DOUBLE NOT NULL,
    profit DOUBLE,
    margin DOUBLE,
    status VARCHAR NOT NULL,
    country VARCHAR
)
```

**Update in `etl/load.py`**:
```python
def create_schema(self):
    self.con.execute("DROP TABLE IF EXISTS sales")
    
    create_sql = """
    CREATE TABLE sales (
        -- Your schema here
    )
    """
    self.con.execute(create_sql)
```

---

### Step 5: Customize Indexes

**Identify Query Patterns**:
- What columns will you filter by?
- What columns will you group by?
- What columns will you join on?

**Create Indexes**:
```python
def create_indexes(self):
    indexes = [
        "CREATE INDEX idx_order_date ON sales(order_date)",
        "CREATE INDEX idx_customer ON sales(customer_id)",
        "CREATE INDEX idx_product ON sales(product_id)",
        "CREATE INDEX idx_country ON sales(country)",
        "CREATE INDEX idx_customer_date ON sales(customer_id, order_date)"
    ]
    
    for idx_sql in indexes:
        self.con.execute(idx_sql)
```

---

### Step 6: Adapt Dashboard

**Define Your Dashboard**:
1. What metrics to display?
2. What filters needed?
3. What visualizations?
4. What time granularity?

**Dashboard Layout Template**:
```python
app.layout = html.Div([
    # Header
    html.H1('Your Dashboard Title'),
    
    # Filters
    html.Div([
        # Date range
        dcc.DatePickerRange(id='date-range'),
        
        # Dimension filters
        dcc.Dropdown(id='country-filter', options=countries),
        dcc.Dropdown(id='product-filter', options=products),
    ]),
    
    # Visualizations
    html.Div([
        dcc.Graph(id='revenue-chart'),
        dcc.Graph(id='profit-chart'),
        dcc.Graph(id='top-products'),
    ])
])
```

**Callback Pattern**:
```python
@app.callback(
    Output('revenue-chart', 'figure'),
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('country-filter', 'value')]
)
def update_revenue_chart(start_date, end_date, country):
    # Query your data
    query = f"""
        SELECT 
            order_date,
            SUM(revenue) as total_revenue
        FROM sales
        WHERE order_date BETWEEN '{start_date}' AND '{end_date}'
        {f"AND country = '{country}'" if country else ""}
        GROUP BY order_date
        ORDER BY order_date
    """
    
    df = con.execute(query).fetchdf()
    
    # Create visualization
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['order_date'],
        y=df['total_revenue'],
        mode='lines+markers'
    ))
    
    return fig
```

---

## Common Adaptations

### Adaptation 1: Time-Series Data

**Use Case**: IoT sensors, logs, metrics

**Key Changes**:
- Add timestamp parsing in extract
- Create time-based indexes
- Add time aggregation functions
- Use time-series visualizations

**Example**:
```python
# Extract with timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Index on time
CREATE INDEX idx_timestamp ON sensor_data(timestamp)

# Aggregate by time
SELECT 
    DATE_TRUNC('hour', timestamp) as hour,
    AVG(temperature) as avg_temp
FROM sensor_data
GROUP BY hour
```

---

### Adaptation 2: Hierarchical Data

**Use Case**: Organizational data, product categories

**Key Changes**:
- Add parent-child relationships
- Create hierarchy navigation
- Add drill-down functionality

**Example**:
```python
# Schema with hierarchy
CREATE TABLE products (
    product_id VARCHAR,
    category VARCHAR,
    subcategory VARCHAR,
    product_name VARCHAR
)

# Hierarchical query
SELECT 
    category,
    subcategory,
    SUM(revenue) as total
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY category, subcategory
```

---

### Adaptation 3: Multi-Source Data

**Use Case**: Combining data from multiple systems

**Key Changes**:
- Create multiple extractors
- Add data source tracking
- Handle schema differences
- Implement data reconciliation

**Example**:
```python
def extract_all_sources(self):
    # Extract from multiple sources
    df_crm = self.extract_from_crm()
    df_erp = self.extract_from_erp()
    df_web = self.extract_from_web_analytics()
    
    # Add source tracking
    df_crm['source'] = 'CRM'
    df_erp['source'] = 'ERP'
    df_web['source'] = 'Web'
    
    # Standardize schemas
    df_crm = self.standardize_schema(df_crm)
    df_erp = self.standardize_schema(df_erp)
    df_web = self.standardize_schema(df_web)
    
    # Combine
    df_combined = pd.concat([df_crm, df_erp, df_web])
    
    return df_combined
```

---

## Example Scenarios

### Scenario 1: E-Commerce Analytics

**Data Source**: Order database  
**Grain**: One row per order line item  
**Key Metrics**: Revenue, profit, conversion rate  
**Dimensions**: Product, customer, time, geography

**Adaptations Needed**:
1. Extract from PostgreSQL orders table
2. Join with products and customers tables
3. Calculate profit margins
4. Add customer segmentation
5. Create funnel visualization

**Time to Adapt**: 1 day

---

### Scenario 2: Log Analysis

**Data Source**: Application logs (JSON files)  
**Grain**: One row per log entry  
**Key Metrics**: Error rate, response time, throughput  
**Dimensions**: Endpoint, status code, time

**Adaptations Needed**:
1. Parse JSON log files
2. Extract timestamp and parse
3. Categorize error types
4. Calculate percentiles
5. Create time-series charts

**Time to Adapt**: 1-2 days

---

### Scenario 3: Financial Reporting

**Data Source**: Accounting system API  
**Grain**: One row per transaction  
**Key Metrics**: Revenue, expenses, profit  
**Dimensions**: Account, department, time

**Adaptations Needed**:
1. API authentication and extraction
2. Handle multi-currency
3. Implement fiscal calendar
4. Add budget comparisons
5. Create financial statements

**Time to Adapt**: 2-3 days

---

## What to Keep vs Change

### ✅ Keep (Template Core)

**Folder Structure**:
- Keep the data/, etl/, dashboard/, docs/ structure
- Proven organization pattern

**ETL Pattern**:
- Keep extract → transform → load separation
- Modular, testable, maintainable

**DuckDB + Parquet**:
- Keep unless you have specific reason to change
- Excellent performance for analytics

**Indexing Strategy**:
- Keep the concept, adapt columns
- Critical for performance

**Documentation Structure**:
- Keep the doc types
- Update content for your project

---

### 🔄 Customize (Project-Specific)

**Data Extraction**:
- Adapt for your data source
- CSV, API, database, etc.

**Transformations**:
- Your business logic
- Your data quality rules
- Your derived metrics

**Database Schema**:
- Your fields and types
- Your relationships
- Your constraints

**Dashboard**:
- Your metrics
- Your filters
- Your visualizations
- Your branding

**Documentation**:
- Your data dictionary
- Your business rules
- Your user guide

---

### ❌ Replace (If Needed)

**DuckDB** → Replace if:
- Need distributed processing (use Spark)
- Need multi-user writes (use PostgreSQL)
- Need real-time streaming (use Kafka)

**Dash** → Replace if:
- Need simpler prototyping (use Streamlit)
- Need more control (use Flask + React)
- Have existing framework (use that)

**Parquet** → Replace if:
- Have different format requirements
- Need different compression
- Have compatibility issues

---

## Adaptation Time Estimates

| Complexity | Time | Description |
|------------|------|-------------|
| **Simple** | 4-8 hours | Similar data structure, minor changes |
| **Moderate** | 1-2 days | Different domain, moderate customization |
| **Complex** | 3-5 days | Multiple sources, complex transformations |
| **Advanced** | 1-2 weeks | Significant architecture changes |

**Factors Affecting Time**:
- Data source complexity
- Transformation complexity
- Dashboard requirements
- Team familiarity with stack
- Data quality issues

---

## Success Checklist

### Adaptation Complete When:
- [ ] ETL pipeline runs successfully
- [ ] Database populated with your data
- [ ] Indexes created for your queries
- [ ] Dashboard displays your metrics
- [ ] Filters work for your dimensions
- [ ] Performance acceptable (<1s queries)
- [ ] Data dictionary updated
- [ ] README updated with your project
- [ ] Team can run and understand it

---

## Getting Help

### Resources:
1. **Implementation Guide**: Step-by-step instructions
2. **ETL Pattern Guide**: Reusable code patterns
3. **Architecture Doc**: Design decisions explained
4. **Example Projects**: See other adaptations

### Common Questions:
- "How do I connect to X data source?" → See ETL Pattern Guide
- "How do I add Y metric?" → See transform patterns
- "How do I create Z visualization?" → See Plotly docs
- "Performance is slow" → Check indexes, see optimization guide

---

## Related Documentation

- [Implementation Guide](implementation_guide.md) - Detailed setup steps
- [ETL Pattern Guide](etl_pattern_guide.md) - Code patterns
- [Architecture](architecture.md) - Design decisions
- [Code Standards](code_standards.md) - Coding conventions

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Estimated Adaptation Time**: 1-5 days depending on complexity

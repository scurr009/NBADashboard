"""
NBA Interactive Dashboard - DuckDB Version
Scalable to billions of rows using DuckDB
Following ScottSkills data visualization best practices
Sources: Tufte, Knaflic, Few, Wilke
"""

import duckdb
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import os

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# DUCKDB SETUP - Scalable to billions of rows
# ============================================================================

# Connect to DuckDB (in-memory for demo, use file for persistence)
con = duckdb.connect(':memory:')

# Load CSV into DuckDB (one-time operation)
# For production: use Parquet files for 10x better performance
csv_path = os.path.join(script_dir, 'NBA_Player_Totals.csv')
con.execute(f"""
    CREATE TABLE players AS 
    SELECT * FROM read_csv_auto('{csv_path}', 
        nullstr='NA',
        sample_size=-1
    )
""")

# Create indexes for fast filtering (critical for large datasets)
con.execute("CREATE INDEX idx_season ON players(season)")
con.execute("CREATE INDEX idx_team ON players(tm)")
con.execute("CREATE INDEX idx_position ON players(pos)")
con.execute("CREATE INDEX idx_player ON players(player)")

print("\n" + "="*70)
print("📊 DuckDB Database Initialized")
print("="*70)

# Get metadata for filters
seasons = con.execute("SELECT DISTINCT season FROM players ORDER BY season").fetchdf()
teams = con.execute("SELECT DISTINCT tm FROM players WHERE tm != 'TOT' ORDER BY tm").fetchdf()
positions = con.execute("SELECT DISTINCT pos FROM players ORDER BY pos").fetchdf()
players_list = con.execute("SELECT DISTINCT player FROM players ORDER BY player").fetchdf()

all_seasons = seasons['season'].tolist()
all_teams = teams['tm'].tolist()
all_positions = positions['pos'].tolist()
all_players = players_list['player'].tolist()

print(f"✅ Loaded {con.execute('SELECT COUNT(*) FROM players').fetchone()[0]:,} rows")
print(f"✅ {len(all_players):,} unique players")
print(f"✅ {len(all_seasons)} seasons ({min(all_seasons)}-{max(all_seasons)})")
print("="*70 + "\n")

# ============================================================================
# COLORBLIND-SAFE PALETTE
# ============================================================================
LINE_COLORS = [
    '#0173B2', '#DE8F05', '#029E73', '#CC78BC', '#ECE133',
    '#56B4E9', '#E69F00', '#009E73', '#F0E442', '#D55E00'
]

# ============================================================================
# METRIC DEFINITIONS
# ============================================================================
metrics = {
    'ppg': {'name': 'Points Per Game', 'calc': 'pts / g', 'agg': 'AVG'},
    'rpg': {'name': 'Rebounds Per Game', 'calc': 'trb / g', 'agg': 'AVG'},
    'apg': {'name': 'Assists Per Game', 'calc': 'ast / g', 'agg': 'AVG'},
    'spg': {'name': 'Steals Per Game', 'calc': 'stl / g', 'agg': 'AVG'},
    'bpg': {'name': 'Blocks Per Game', 'calc': 'blk / g', 'agg': 'AVG'},
    'mpg': {'name': 'Minutes Per Game', 'calc': 'mp / g', 'agg': 'AVG'},
    'fg_percent': {'name': 'Field Goal %', 'calc': 'fg_percent', 'agg': 'AVG'},
    'x3p_percent': {'name': '3-Point %', 'calc': 'x3p_percent', 'agg': 'AVG'},
    'ft_percent': {'name': 'Free Throw %', 'calc': 'ft_percent', 'agg': 'AVG'},
    'pts': {'name': 'Total Points', 'calc': 'pts', 'agg': 'SUM'},
    'trb': {'name': 'Total Rebounds', 'calc': 'trb', 'agg': 'SUM'},
    'ast': {'name': 'Total Assists', 'calc': 'ast', 'agg': 'SUM'},
}

# ============================================================================
# CREATE DASH APP
# ============================================================================

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1('🏀 NBA Player Performance Dashboard (DuckDB)',
                style={'textAlign': 'center', 'color': '#333333', 'marginBottom': 10}),
        html.P('Scalable to billions of rows • Powered by DuckDB',
               style={'textAlign': 'center', 'color': '#666666', 'marginBottom': 30}),
    ]),
    
    html.Div([
        # LEFT PANEL - FILTERS
        html.Div([
            html.Div([
                html.H3('🎛️ Filters', style={'color': '#333333', 'marginBottom': 20}),
                
                # Metric Selector
                html.Label('📊 Select Metric:', style={'fontWeight': 'bold', 'marginTop': 15}),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[{'label': v['name'], 'value': k} for k, v in metrics.items()],
                    value='ppg',
                    clearable=False,
                    style={'marginBottom': 20}
                ),
                
                # Year Range Slider
                html.Label('📅 Season Range:', style={'fontWeight': 'bold', 'marginTop': 15}),
                dcc.RangeSlider(
                    id='year-slider',
                    min=int(min(all_seasons)),
                    max=int(max(all_seasons)),
                    value=[int(min(all_seasons)), int(max(all_seasons))],
                    marks={int(year): str(year) if year % 10 == 0 else '' 
                           for year in all_seasons},
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    step=1
                ),
                
                # Team Filter
                html.Label('🏟️ Team:', style={'fontWeight': 'bold', 'marginTop': 30}),
                dcc.Dropdown(
                    id='team-dropdown',
                    options=[{'label': 'All Teams', 'value': 'ALL'}] + 
                            [{'label': team, 'value': team} for team in all_teams],
                    value='ALL',
                    clearable=True,
                    style={'marginBottom': 20}
                ),
                
                # Position Filter
                html.Label('📍 Position:', style={'fontWeight': 'bold', 'marginTop': 15}),
                dcc.Dropdown(
                    id='position-dropdown',
                    options=[{'label': 'All Positions', 'value': 'ALL'}] + 
                            [{'label': pos, 'value': pos} for pos in all_positions],
                    value='ALL',
                    clearable=False,
                    style={'marginBottom': 20}
                ),
                
                # Player Search
                html.Label('🔍 Search Player (optional):', style={'fontWeight': 'bold', 'marginTop': 15}),
                dcc.Dropdown(
                    id='player-dropdown',
                    options=[{'label': 'All Players', 'value': 'ALL'}] + 
                            [{'label': player, 'value': player} for player in all_players],
                    value='ALL',
                    clearable=False,
                    placeholder='Type to search...',
                    style={'marginBottom': 20}
                ),
                
                # Query Performance Info
                html.Div([
                    html.P('⚡ Query Performance:', style={'fontWeight': 'bold', 'marginBottom': 5}),
                    html.P(id='query-time', children='Ready', 
                           style={'fontSize': '12px', 'color': '#666666'})
                ], style={
                    'backgroundColor': '#F5F5F5',
                    'padding': '15px',
                    'borderRadius': '5px',
                    'marginTop': 30
                }),
                
                # Info box
                html.Div([
                    html.P('💡 Tips:', style={'fontWeight': 'bold', 'marginBottom': 5}),
                    html.Ul([
                        html.Li('DuckDB queries millions of rows instantly'),
                        html.Li('Hover over lines for details'),
                        html.Li('Click legend to show/hide players'),
                        html.Li('Drag to zoom, double-click to reset'),
                    ], style={'fontSize': '12px', 'color': '#666666'})
                ], style={
                    'backgroundColor': '#F5F5F5',
                    'padding': '15px',
                    'borderRadius': '5px',
                    'marginTop': 15
                })
                
            ], style={'padding': '20px'})
        ], style={
            'width': '25%',
            'backgroundColor': '#FAFAFA',
            'height': '100vh',
            'overflowY': 'auto',
            'borderRight': '2px solid #E0E0E0'
        }),
        
        # RIGHT PANEL - CHART
        html.Div([
            dcc.Graph(
                id='top-10-chart', 
                style={'height': '85vh'},
                figure=go.Figure().update_layout(
                    title='Loading...',
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
            )
        ], style={
            'width': '74%',
            'padding': '10px'
        })
    ], style={'display': 'flex', 'flexDirection': 'row'})
], style={'fontFamily': 'Arial, sans-serif'})

# ============================================================================
# CALLBACK - DUCKDB QUERY
# ============================================================================

@app.callback(
    [Output('top-10-chart', 'figure'),
     Output('query-time', 'children')],
    [
        Input('metric-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('team-dropdown', 'value'),
        Input('position-dropdown', 'value'),
        Input('player-dropdown', 'value')
    ]
)
def update_chart(metric, year_range, team, position, player):
    """
    Query DuckDB for top 10 players
    This approach scales to billions of rows
    """
    import time
    start_time = time.time()
    
    # Convert to int
    year_min = int(year_range[0])
    year_max = int(year_range[1])
    
    # Handle None values from clearable dropdowns
    team = team or 'ALL'
    position = position or 'ALL'
    player = player or 'ALL'
    
    # Get metric info
    metric_info = metrics[metric]
    metric_name = metric_info['name']
    metric_calc = metric_info['calc']
    metric_agg = metric_info['agg']
    
    # Build WHERE clause
    where_clauses = [f"season BETWEEN {year_min} AND {year_max}"]
    if team != 'ALL':
        where_clauses.append(f"tm = '{team}'")
    if position != 'ALL':
        where_clauses.append(f"pos = '{position}'")
    if player != 'ALL':
        where_clauses.append(f"player = '{player}'")
    
    where_clause = " AND ".join(where_clauses)
    
    # ========================================================================
    # OPTIMIZED QUERY - Key to billion-row performance
    # ========================================================================
    # Step 1: Find top 10 players (aggregated)
    # Step 2: Get their season-by-season data
    # This avoids processing all data twice
    
    query = f"""
    WITH player_rankings AS (
        -- Calculate career metric for ranking (within filters)
        SELECT 
            player,
            {metric_agg}({metric_calc}) as career_metric
        FROM players
        WHERE {where_clause}
        GROUP BY player
        ORDER BY career_metric DESC
        LIMIT 10
    ),
    player_seasons AS (
        -- Get season-by-season data for top 10 players
        SELECT 
            p.player,
            p.season,
            {metric_calc} as metric_value
        FROM players p
        INNER JOIN player_rankings pr ON p.player = pr.player
        ORDER BY p.player, p.season
    )
    SELECT * FROM player_seasons
    """
    
    # Execute query
    df = con.execute(query).fetchdf()
    
    query_time = time.time() - start_time
    
    # Check for empty results
    if len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No data matches the selected filters.<br>Try adjusting your filter selections.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color='#666666')
        )
        fig.update_layout(
            title="No Data Available",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        return fig, f"Query: {query_time*1000:.1f}ms | No results"
    
    # Create figure
    fig = go.Figure()
    
    # Add line for each player
    top_players = df['player'].unique()
    for idx, player_name in enumerate(top_players):
        player_data = df[df['player'] == player_name].sort_values('season')
        
        fig.add_trace(go.Scatter(
            x=player_data['season'],
            y=player_data['metric_value'],
            mode='lines+markers',
            name=player_name,
            line=dict(
                color=LINE_COLORS[idx % len(LINE_COLORS)],
                width=3 if player == player_name else 2
            ),
            marker=dict(
                size=8 if player == player_name else 6,
                line=dict(width=1, color='white')
            ),
            hovertemplate=f'<b>{player_name}</b><br>' +
                         'Season: %{x}<br>' +
                         f'{metric_name}: %{{y:.2f}}<extra></extra>'
        ))
    
    # Build subtitle
    filter_desc = []
    if year_min != int(min(all_seasons)) or year_max != int(max(all_seasons)):
        filter_desc.append(f"Ranked in: {year_min}-{year_max}")
    if team != 'ALL':
        filter_desc.append(f"Team: {team}")
    if position != 'ALL':
        filter_desc.append(f"Position: {position}")
    if player != 'ALL':
        filter_desc.append(f"Player: {player}")
    
    subtitle = f"Filters: {' | '.join(filter_desc)}" if filter_desc else "Top 10 All-Time"
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f'<b>Top 10 Players: {metric_name}</b><br>' +
                 f'<sub>{subtitle}</sub>',
            font=dict(size=22, color='#333333'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Season',
            showgrid=True,
            gridwidth=1,
            gridcolor='#E0E0E0',
            showline=False,
            zeroline=False,
            dtick=5
        ),
        yaxis=dict(
            title=metric_name,
            showgrid=True,
            gridwidth=1,
            gridcolor='#E0E0E0',
            showline=False,
            zeroline=False
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12, color='#333333'),
        hovermode='closest',
        legend=dict(
            orientation='v',
            yanchor='top',
            y=0.98,
            xanchor='left',
            x=1.01,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#E0E0E0',
            borderwidth=1,
            font=dict(size=11)
        ),
        height=700,
        margin=dict(l=60, r=180, t=80, b=60)
    )
    
    # Performance info
    rows_processed = con.execute(f"SELECT COUNT(*) FROM players WHERE {where_clause}").fetchone()[0]
    perf_text = f"Query: {query_time*1000:.1f}ms | Processed: {rows_processed:,} rows | Returned: {len(df)} rows"
    
    return fig, perf_text

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🏀 NBA Interactive Dashboard - DuckDB Version")
    print("="*70)
    print("\n📊 Features:")
    print("  ✅ DuckDB backend (scalable to billions of rows)")
    print("  ✅ Indexed queries for fast filtering")
    print("  ✅ Optimized SQL with CTEs")
    print("  ✅ Real-time query performance metrics")
    print("  ✅ All previous features (filters, interactivity, etc.)")
    print("\n🌐 Starting dashboard...")
    print("   Opening at: http://127.0.0.1:8050/")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=True, port=8050)

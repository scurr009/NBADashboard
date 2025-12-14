"""
NBA Interactive Dashboard - Modern Design
Apple-inspired clean, professional interface
Following 2025 dashboard design best practices
"""

import duckdb
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import os

# Get script directory
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================================================
# DUCKDB SETUP
# ============================================================================

db_path = os.path.join(script_dir, 'data', 'duckdb', 'nba.db')

if not os.path.exists(db_path):
    print("\n❌ ERROR: Database not found!")
    print(f"Expected: {db_path}")
    print("Please run: python -m etl.pipeline\n")
    exit(1)

con = duckdb.connect(db_path, read_only=True)

# Get metadata
seasons = con.execute("SELECT DISTINCT season FROM players ORDER BY season").fetchdf()
teams = con.execute("SELECT DISTINCT tm FROM players ORDER BY tm").fetchdf()
positions = con.execute("SELECT DISTINCT pos FROM players ORDER BY pos").fetchdf()
players_list = con.execute("""
    SELECT DISTINCT player_id, player 
    FROM players 
    ORDER BY player
""").fetchdf()

all_seasons = seasons['season'].tolist()
all_teams = teams['tm'].tolist()
all_positions = positions['pos'].tolist()
all_players = list(zip(players_list['player_id'].tolist(), players_list['player'].tolist()))

print(f"\n✅ Connected: {len(con.execute('SELECT * FROM players').fetchdf()):,} rows")

# ============================================================================
# DESIGN SYSTEM - Apple-inspired
# ============================================================================

# Milliman-inspired professional color palette
COLORS = {
    'background': '#F5F5F5',  # Light gray background
    'surface': '#FFFFFF',
    'sidebar_bg': '#2C3E50',  # Dark blue-gray sidebar
    'sidebar_text': '#ECF0F1',  # Light text on dark
    'primary': '#3498DB',  # Professional blue
    'secondary': '#95A5A6',  # Muted gray
    'text_primary': '#2C3E50',  # Dark blue-gray
    'text_secondary': '#7F8C8D',  # Medium gray
    'border': '#BDC3C7',  # Light border
    'hover': '#34495E',  # Darker on hover
    'pill_bg': '#34495E',  # Pill button background
}

# Professional, muted chart colors (like Milliman)
CHART_COLORS = [
    '#8FBC8F',  # Sage green
    '#DAA520',  # Goldenrod/mustard
    '#CD853F',  # Peru/coral
    '#5F9EA0',  # Cadet blue/teal
    '#BC8F8F',  # Rosy brown
    '#6B8E23',  # Olive drab
    '#708090',  # Slate gray
    '#D2691E'   # Chocolate
]

# Counting stats only (no averages)
METRICS = {
    'pts': {'name': 'Total Points', 'calc': 'pts', 'agg': 'SUM'},
    'trb': {'name': 'Total Rebounds', 'calc': 'trb', 'agg': 'SUM'},
    'ast': {'name': 'Total Assists', 'calc': 'ast', 'agg': 'SUM'},
    'stl': {'name': 'Total Steals', 'calc': 'stl', 'agg': 'SUM'},
    'blk': {'name': 'Total Blocks', 'calc': 'blk', 'agg': 'SUM'},
}

# Top N options
TOP_N_OPTIONS = [3, 5, 10, 15, 20]

# Modern NBA teams (current 30 teams as of 2024-25 season)
MODERN_TEAMS = {
    'ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
    'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
    'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
}

# ============================================================================
# CREATE DASH APP
# ============================================================================

# Set assets folder path correctly
import pathlib
assets_path = pathlib.Path(__file__).parent / 'assets'

app = Dash(__name__, suppress_callback_exceptions=True, assets_folder=str(assets_path))
app.title = "NBA Analytics"

# ============================================================================
# LAYOUT - Modern, Clean Design
# ============================================================================

app.layout = html.Div([
    # Sidebar - Dark theme like Milliman
    html.Div([
        # Logo/Title
        html.Div([
            html.Div('🏀', style={
                'fontSize': '28px',
                'marginBottom': '8px'
            }),
            html.H1('NBA Analytics', style={
                'fontSize': '22px',
                'fontWeight': '600',
                'color': COLORS['sidebar_text'],
                'margin': '0',
                'letterSpacing': '-0.3px'
            }),
            html.P('Player Performance Dashboard', style={
                'fontSize': '13px',
                'color': COLORS['sidebar_text'],
                'opacity': '0.8',
                'margin': '4px 0 0 0'
            }),
        ], style={
            'padding': '24px 20px',
            'borderBottom': f"1px solid rgba(255,255,255,0.1)"
        }),

        # View Selector (Tabs in Sidebar)
        html.Div([
            html.Label('View', style={
                'fontSize': '13px',
                'fontWeight': '500',
                'color': COLORS['sidebar_text'],
                'marginBottom': '8px',
                'display': 'block'
            }),
            dcc.Dropdown(
                id='view-selector',
                options=[
                    {'label': '📈 Performance Over Time', 'value': 'timeline'},
                    {'label': '⚔️ Player Comparison', 'value': 'comparison'}
                ],
                value='timeline',
                clearable=False,
                className='custom-dropdown'
            ),
        ], style={
            'padding': '20px',
            'borderBottom': f"1px solid rgba(255,255,255,0.1)"
        }),
        
        # Filters
        html.Div([
            # Metric Selector
            html.Div([
                html.Label('Metric', style={
                    'fontSize': '13px',
                    'fontWeight': '500',
                    'color': COLORS['sidebar_text'],
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[{'label': v['name'], 'value': k} for k, v in METRICS.items()],
                    value='pts',
                    clearable=False,
                    className='custom-dropdown'
                ),
            ], style={'marginBottom': '20px'}),
            
            # Top N Selector
            html.Div([
                html.Label('Top N Players', style={
                    'fontSize': '13px',
                    'fontWeight': '500',
                    'color': COLORS['sidebar_text'],
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='topn-dropdown',
                    options=[{'label': f'Top {n}', 'value': n} for n in TOP_N_OPTIONS],
                    value=10,
                    clearable=False,
                    className='custom-dropdown'
                ),
            ], style={'marginBottom': '24px'}),
            
            # Season Range - Text Inputs
            html.Div([
                html.Label('Season Range', style={
                    'fontSize': '13px',
                    'fontWeight': '500',
                    'color': COLORS['sidebar_text'],
                    'marginBottom': '10px',
                    'display': 'block'
                }),
                html.Div([
                    html.Div([
                        html.Label('From:', style={'fontSize': '11px', 'color': COLORS['sidebar_text'], 'marginBottom': '4px', 'display': 'block'}),
                        dcc.Input(
                            id='year-from',
                            type='number',
                            value=2000,
                            min=int(min(all_seasons)),
                            max=int(max(all_seasons)),
                            style={
                                'width': '100%',
                                'padding': '8px',
                                'fontSize': '14px',
                                'backgroundColor': 'rgba(255,255,255,0.1)',
                                'border': '1px solid rgba(255,255,255,0.2)',
                                'borderRadius': '6px',
                                'color': COLORS['sidebar_text']
                            }
                        )
                    ], style={'flex': '1', 'marginRight': '8px'}),
                    html.Div([
                        html.Label('To:', style={'fontSize': '11px', 'color': COLORS['sidebar_text'], 'marginBottom': '4px', 'display': 'block'}),
                        dcc.Input(
                            id='year-to',
                            type='number',
                            value=int(max(all_seasons)),
                            min=int(min(all_seasons)),
                            max=int(max(all_seasons)),
                            style={
                                'width': '100%',
                                'padding': '8px',
                                'fontSize': '14px',
                                'backgroundColor': 'rgba(255,255,255,0.1)',
                                'border': '1px solid rgba(255,255,255,0.2)',
                                'borderRadius': '6px',
                                'color': COLORS['sidebar_text']
                            }
                        )
                    ], style={'flex': '1'})
                ], style={'display': 'flex'})
            ], style={'marginBottom': '24px'}),
            
            # Team Filter
            html.Div([
                html.Label('Team', style={
                    'fontSize': '13px',
                    'fontWeight': '500',
                    'color': COLORS['sidebar_text'],
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='team-dropdown',
                    options=[
                        {'label': 'All Teams', 'value': 'ALL'},
                        {
                            'label': 'Modern Teams (Current 30)',
                            'value': 'modern_group',
                            'disabled': True
                        }
                    ] + [{'label': f'  {team}', 'value': team} for team in sorted(all_teams) if team in MODERN_TEAMS] + [
                        {
                            'label': 'Other Teams (Historical)',
                            'value': 'other_group',
                            'disabled': True
                        }
                    ] + [{'label': f'  {team}', 'value': team} for team in sorted(all_teams) if team not in MODERN_TEAMS],
                    value='ALL',
                    clearable=True,
                    placeholder='Select team...',
                    className='custom-dropdown'
                ),
            ], style={'marginBottom': '24px'}),
            
            # Position Filter
            html.Div([
                html.Label('Position', style={
                    'fontSize': '13px',
                    'fontWeight': '500',
                    'color': COLORS['sidebar_text'],
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='position-dropdown',
                    options=[{'label': 'All Positions', 'value': 'ALL'}] + 
                            [{'label': pos, 'value': pos} for pos in all_positions],
                    value='ALL',
                    clearable=False,
                    className='custom-dropdown'
                ),
            ], style={'marginBottom': '24px'}),
            
            # Player Search
            html.Div([
                html.Label('Player', style={
                    'fontSize': '13px',
                    'fontWeight': '500',
                    'color': COLORS['sidebar_text'],
                    'marginBottom': '8px',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='player-dropdown',
                    options=[{'label': 'All Players', 'value': 'ALL'}] + 
                            [{'label': name, 'value': str(pid)} for pid, name in all_players],
                    value='ALL',
                    clearable=True,
                    placeholder='Search player...',
                    className='custom-dropdown'
                ),
            ], style={'marginBottom': '24px'}),
            
        ], style={
            'padding': '20px',
            'overflowY': 'auto',
            'flex': '1'
        }),
        
        # Footer
        html.Div([
            html.P(id='query-time', children='Ready', style={
                'fontSize': '11px',
                'color': COLORS['sidebar_text'],
                'opacity': '0.7',
                'margin': '0'
            }),
        ], style={
            'padding': '16px 20px',
            'borderTop': f"1px solid rgba(255,255,255,0.1)",
            'fontSize': '11px',
            'color': COLORS['sidebar_text']
        }),
        
    ], style={
        'width': '280px',
        'height': '100vh',
        'backgroundColor': COLORS['sidebar_bg'],
        'boxShadow': '2px 0 8px rgba(0,0,0,0.1)',
        'display': 'flex',
        'flexDirection': 'column',
        'position': 'fixed',
        'left': '0',
        'top': '0',
        'fontFamily': "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
    }),
    
    # Main Content
    html.Div([
        # Timeline View
        html.Div([
            # Header
            html.Div([
                html.H2(id='chart-title', children='Top 10 Players', style={
                    'fontSize': '32px',
                    'fontWeight': '600',
                    'color': COLORS['text_primary'],
                    'margin': '0',
                    'letterSpacing': '-0.5px'
                }),
                html.P(id='chart-subtitle', children='Select filters to explore', style={
                    'fontSize': '16px',
                    'color': COLORS['text_secondary'],
                    'margin': '8px 0 0 0'
                }),
            ], style={
                'marginBottom': '32px'
            }),

            # Chart
            dcc.Graph(
                id='main-chart',
                config={'displayModeBar': False},
                style={'height': 'calc(100vh - 200px)'}
            ),
        ], id='timeline-view', style={'display': 'block'}),

        # Comparison View
        html.Div([
            # Header
            html.Div([
                html.H2('Player Comparison', style={
                    'fontSize': '32px',
                    'fontWeight': '600',
                    'color': COLORS['text_primary'],
                    'margin': '0',
                    'letterSpacing': '-0.5px'
                }),
                html.P('Compare players side-by-side across key statistics', style={
                    'fontSize': '16px',
                    'color': COLORS['text_secondary'],
                    'margin': '8px 0 0 0'
                }),
            ], style={'marginBottom': '32px'}),

            # Player Selection
            html.Div([
                html.Div([
                    html.Label('Player 1', style={
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'color': COLORS['text_primary'],
                        'marginBottom': '8px',
                        'display': 'block'
                    }),
                    dcc.Dropdown(
                        id='compare-player-1',
                        options=[{'label': name, 'value': str(pid)} for pid, name in all_players],
                        value=None,
                        placeholder='Select player 1...',
                        className='custom-dropdown',
                        style={'backgroundColor': 'white'}
                    ),
                ], style={'flex': '1', 'marginRight': '16px'}),

                html.Div([
                    html.Label('Player 2', style={
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'color': COLORS['text_primary'],
                        'marginBottom': '8px',
                        'display': 'block'
                    }),
                    dcc.Dropdown(
                        id='compare-player-2',
                        options=[{'label': name, 'value': str(pid)} for pid, name in all_players],
                        value=None,
                        placeholder='Select player 2...',
                        className='custom-dropdown',
                        style={'backgroundColor': 'white'}
                    ),
                ], style={'flex': '1', 'marginRight': '16px'}),

                html.Div([
                    html.Label('Player 3 (Optional)', style={
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'color': COLORS['text_primary'],
                        'marginBottom': '8px',
                        'display': 'block'
                    }),
                    dcc.Dropdown(
                        id='compare-player-3',
                        options=[{'label': name, 'value': str(pid)} for pid, name in all_players],
                        value=None,
                        placeholder='Select player 3...',
                        className='custom-dropdown',
                        style={'backgroundColor': 'white'}
                    ),
                ], style={'flex': '1'}),
            ], style={
                'display': 'flex',
                'marginBottom': '32px',
                'padding': '24px',
                'backgroundColor': 'white',
                'borderRadius': '12px',
                'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
            }),

            # Radar Chart
            html.Div([
                dcc.Graph(
                    id='comparison-radar',
                    config={'displayModeBar': False},
                    style={'height': '500px'}
                ),
            ], style={
                'marginBottom': '32px',
                'padding': '24px',
                'backgroundColor': 'white',
                'borderRadius': '12px',
                'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
            }),

            # Stats Table and Insights
            html.Div([
                # Stats Table
                html.Div([
                    html.H3('Career Statistics', style={
                        'fontSize': '20px',
                        'fontWeight': '600',
                        'color': COLORS['text_primary'],
                        'marginBottom': '16px'
                    }),
                    html.Div(id='comparison-table'),
                ], style={
                    'flex': '1',
                    'marginRight': '16px',
                    'padding': '24px',
                    'backgroundColor': 'white',
                    'borderRadius': '12px',
                    'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
                }),

                # Insights Panel
                html.Div([
                    html.H3('Insights', style={
                        'fontSize': '20px',
                        'fontWeight': '600',
                        'color': COLORS['text_primary'],
                        'marginBottom': '16px'
                    }),
                    html.Div(id='comparison-insights', style={
                        'fontSize': '15px',
                        'lineHeight': '1.6',
                        'color': COLORS['text_secondary']
                    }),
                ], style={
                    'flex': '1',
                    'padding': '24px',
                    'backgroundColor': 'white',
                    'borderRadius': '12px',
                    'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'
                }),
            ], style={'display': 'flex'}),

        ], id='comparison-view', style={'display': 'none'}),

    ], style={
        'marginLeft': '280px',
        'padding': '48px',
        'backgroundColor': COLORS['background'],
        'minHeight': '100vh',
        'fontFamily': "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
    }),
    
], style={
    'margin': '0',
    'padding': '0',
    'backgroundColor': COLORS['background']
})

# ============================================================================
# CALLBACKS
# ============================================================================

# Callback to toggle views
@app.callback(
    [Output('timeline-view', 'style'),
     Output('comparison-view', 'style')],
    [Input('view-selector', 'value')]
)
def toggle_view(view):
    if view == 'timeline':
        return {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'block'}

# Note: Cascading filter callback removed for now due to technical issues
# The player dropdown will show all players, but the chart will still filter correctly

# Callback to update chart
@app.callback(
    [Output('main-chart', 'figure'),
     Output('query-time', 'children'),
     Output('chart-title', 'children'),
     Output('chart-subtitle', 'children')],
    [Input('metric-dropdown', 'value'),
     Input('topn-dropdown', 'value'),
     Input('year-from', 'value'),
     Input('year-to', 'value'),
     Input('team-dropdown', 'value'),
     Input('position-dropdown', 'value'),
     Input('player-dropdown', 'value')]
)
def update_chart(metric, top_n, year_from, year_to, team, position, player):
    import time
    start_time = time.time()
    
    year_min, year_max = int(year_from or 2000), int(year_to or 2025)
    team = team or 'ALL'
    position = position or 'ALL'
    player = player or 'ALL'
    
    metric_info = METRICS[metric]
    metric_name = metric_info['name']
    metric_calc = metric_info['calc']
    metric_agg = metric_info['agg']
    
    # Build WHERE clause for rankings (no player filter here)
    ranking_where_clauses = [f"season BETWEEN {year_min} AND {year_max}"]
    if team != 'ALL':
        ranking_where_clauses.append(f"tm = '{team}'")
    if position != 'ALL':
        ranking_where_clauses.append(f"pos = '{position}'")
    
    ranking_where_clause = " AND ".join(ranking_where_clauses)
    
    # Build WHERE clause for player_seasons (includes player filter)
    season_where_clauses = [f"p.season BETWEEN {year_min} AND {year_max}"]
    if team != 'ALL':
        season_where_clauses.append(f"p.tm = '{team}'")
    if position != 'ALL':
        season_where_clauses.append(f"p.pos = '{position}'")
    if player != 'ALL':
        season_where_clauses.append(f"p.player_id = {player}")
    
    season_where_clause = " AND ".join(season_where_clauses)
    
    # Simple query for counting stats
    query = f"""
    WITH player_rankings AS (
        SELECT 
            player_id,
            player,
            {metric_agg}({metric_calc}) as career_total
        FROM players
        WHERE {ranking_where_clause}
        GROUP BY player_id, player
        ORDER BY career_total DESC
        LIMIT {top_n}
    ),
    player_seasons AS (
        SELECT 
            p.player_id as player_id,
            p.player as player,
            p.season as season,
            p.{metric_calc} as metric_value
        FROM players p
        INNER JOIN player_rankings pr ON p.player_id = pr.player_id
        WHERE {season_where_clause}
        ORDER BY p.player, p.season
    )
    SELECT player_id, player, season, metric_value FROM player_seasons
    """
    
    df = con.execute(query).fetchdf()
    query_time = time.time() - start_time
    
    # Create figure
    fig = go.Figure()
    
    if len(df) == 0:
        fig.add_annotation(
            text="No data matches your filters<br><span style='font-size:13px;color:#86868B'>Try adjusting your selection</span>",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text_secondary'], family="-apple-system, BlinkMacSystemFont, 'Segoe UI'")
        )
        title = "No Data"
        subtitle = "Adjust filters to see results"
    else:
        # Add traces in Top N order (not alphabetical)
        # Get player ranking order
        player_totals = df.groupby('player')['metric_value'].sum().sort_values(ascending=False)
        top_players = player_totals.index.tolist()
        
        for idx, player_name in enumerate(top_players):
            player_data = df[df['player'] == player_name].sort_values('season')
            
            fig.add_trace(go.Scatter(
                x=player_data['season'],
                y=player_data['metric_value'],
                mode='lines+markers',
                name=player_name,
                line=dict(color=CHART_COLORS[idx % len(CHART_COLORS)], width=3.5),
                marker=dict(size=7, line=dict(width=0)),
                hovertemplate=f'<b>{player_name}</b><br>Season: %{{x}}<br>{metric_name}: %{{y:,.0f}}<extra></extra>'
            ))
        
        title = f"Top {top_n} Players: {metric_name}"
        
        # Build subtitle
        filters = []
        if year_min != int(min(all_seasons)) or year_max != int(max(all_seasons)):
            filters.append(f"{year_min}–{year_max}")
        if team != 'ALL':
            filters.append(team)
        if position != 'ALL':
            filters.append(position)
        
        subtitle = " • ".join(filters) if filters else "All players, all time"
    
    # Style figure
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="-apple-system, BlinkMacSystemFont, 'Segoe UI'", size=15, color=COLORS['text_primary']),
        xaxis=dict(
            title=dict(
                text='Season',
                font=dict(size=17, color=COLORS['text_primary'], family="-apple-system, BlinkMacSystemFont, 'Segoe UI'")
            ),
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor=COLORS['border'],
            tickfont=dict(size=15, color=COLORS['text_primary'], family="-apple-system, BlinkMacSystemFont, 'Segoe UI'")
        ),
        yaxis=dict(
            title=dict(
                text=metric_name,
                font=dict(size=17, color=COLORS['text_primary'], family="-apple-system, BlinkMacSystemFont, 'Segoe UI'")
            ),
            showgrid=True,
            gridwidth=1,
            gridcolor='#E8E8E8',
            showline=False,
            tickfont=dict(size=15, color=COLORS['text_primary'], family="-apple-system, BlinkMacSystemFont, 'Segoe UI'")
        ),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor='white',
            font_size=15,
            font_family="-apple-system, BlinkMacSystemFont, 'Segoe UI'",
            bordercolor=COLORS['border']
        ),
        legend=dict(
            orientation='v',
            yanchor='top',
            y=0.99,
            xanchor='right',
            x=0.99,
            bgcolor='rgba(255,255,255,1)',
            bordercolor='#BDC3C7',
            borderwidth=1.5,
            font=dict(size=15, family="-apple-system, BlinkMacSystemFont, 'Segoe UI'", color=COLORS['text_primary']),
            itemsizing='constant',
            itemwidth=40,
            tracegroupgap=10
        ),
        margin=dict(l=70, r=160, t=20, b=70)
    )
    
    perf_text = f"Query: {query_time*1000:.0f}ms"

    return fig, perf_text, title, subtitle

# Callback for player comparison
@app.callback(
    [Output('comparison-radar', 'figure'),
     Output('comparison-table', 'children'),
     Output('comparison-insights', 'children')],
    [Input('compare-player-1', 'value'),
     Input('compare-player-2', 'value'),
     Input('compare-player-3', 'value')]
)
def update_comparison(player1_id, player2_id, player3_id):
    # Filter out None values
    player_ids = [p for p in [player1_id, player2_id, player3_id] if p is not None]

    if len(player_ids) < 2:
        # Not enough players selected
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text="Select at least 2 players to compare",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text_secondary'])
        )
        empty_fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )

        empty_table = html.P("Select players to see comparison",
                            style={'color': COLORS['text_secondary'], 'textAlign': 'center'})
        empty_insights = html.P("Select players to see insights",
                               style={'color': COLORS['text_secondary']})

        return empty_fig, empty_table, empty_insights

    # Query player career stats
    query = f"""
    SELECT
        player_id,
        player,
        COUNT(DISTINCT season) as seasons,
        SUM(g) as games,
        ROUND(SUM(pts) * 1.0 / SUM(g), 1) as ppg,
        ROUND(SUM(trb) * 1.0 / SUM(g), 1) as rpg,
        ROUND(SUM(ast) * 1.0 / SUM(g), 1) as apg,
        ROUND(SUM(stl) * 1.0 / SUM(g), 1) as spg,
        ROUND(SUM(blk) * 1.0 / SUM(g), 1) as bpg,
        ROUND(SUM(fg) * 100.0 / NULLIF(SUM(fga), 0), 1) as fg_pct,
        ROUND(SUM(fg3) * 100.0 / NULLIF(SUM(fg3a), 0), 1) as fg3_pct,
        ROUND(SUM(ft) * 100.0 / NULLIF(SUM(fta), 0), 1) as ft_pct,
        SUM(pts) as total_pts,
        SUM(trb) as total_trb,
        SUM(ast) as total_ast
    FROM players
    WHERE player_id IN ({','.join(player_ids)})
    GROUP BY player_id, player
    ORDER BY player
    """

    df = con.execute(query).fetchdf()

    # Create radar chart
    fig = go.Figure()

    # Stats to show on radar chart
    radar_stats = ['ppg', 'rpg', 'apg', 'spg', 'bpg', 'fg_pct']
    radar_labels = ['PPG', 'RPG', 'APG', 'SPG', 'BPG', 'FG%']

    # Normalize percentages to similar scale as counting stats (0-30 range)
    # We'll scale FG% from 0-100 to 0-30
    def normalize_value(value, stat):
        if stat == 'fg_pct':
            return (value / 100.0) * 30 if value is not None else 0
        return value if value is not None else 0

    for idx, row in df.iterrows():
        values = [normalize_value(row[stat], stat) for stat in radar_stats]
        values.append(values[0])  # Close the loop

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=radar_labels + [radar_labels[0]],
            fill='toself',
            name=row['player'],
            line=dict(color=CHART_COLORS[idx % len(CHART_COLORS)], width=3),
            fillcolor=CHART_COLORS[idx % len(CHART_COLORS)],
            opacity=0.6
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 30],
                gridcolor='#E8E8E8',
                tickfont=dict(size=13, color=COLORS['text_secondary'])
            ),
            angularaxis=dict(
                gridcolor='#E8E8E8',
                tickfont=dict(size=14, color=COLORS['text_primary'], family="-apple-system"),
            )
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(size=15, family="-apple-system", color=COLORS['text_primary'])
        ),
        font=dict(family="-apple-system, BlinkMacSystemFont, 'Segoe UI'"),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=80, r=80, t=40, b=100)
    )

    # Create comparison table
    table_rows = []

    # Header row
    header_cells = [html.Th('Stat', style={'textAlign': 'left', 'padding': '12px', 'borderBottom': f'2px solid {COLORS["border"]}'})]
    for _, row in df.iterrows():
        header_cells.append(html.Th(row['player'], style={
            'textAlign': 'center',
            'padding': '12px',
            'borderBottom': f'2px solid {COLORS["border"]}',
            'fontWeight': '600'
        }))
    table_rows.append(html.Tr(header_cells))

    # Data rows
    stats_to_show = [
        ('Games Played', 'games', 0),
        ('Seasons', 'seasons', 0),
        ('PPG', 'ppg', 1),
        ('RPG', 'rpg', 1),
        ('APG', 'apg', 1),
        ('SPG', 'spg', 1),
        ('BPG', 'bpg', 1),
        ('FG%', 'fg_pct', 1),
        ('3P%', 'fg3_pct', 1),
        ('FT%', 'ft_pct', 1),
        ('Total Points', 'total_pts', 0),
        ('Total Rebounds', 'total_trb', 0),
        ('Total Assists', 'total_ast', 0),
    ]

    for stat_name, stat_key, decimals in stats_to_show:
        cells = [html.Td(stat_name, style={
            'padding': '10px 12px',
            'borderBottom': f'1px solid {COLORS["border"]}',
            'fontWeight': '500'
        })]

        # Get values for this stat across all players
        values = [row[stat_key] if row[stat_key] is not None else 0 for _, row in df.iterrows()]
        max_val = max(values) if values else 0

        for val in values:
            is_best = (val == max_val and val > 0)
            cells.append(html.Td(
                f'{val:,.{decimals}f}',
                style={
                    'textAlign': 'center',
                    'padding': '10px 12px',
                    'borderBottom': f'1px solid {COLORS["border"]}',
                    'fontWeight': '600' if is_best else 'normal',
                    'color': COLORS['primary'] if is_best else COLORS['text_primary']
                }
            ))

        table_rows.append(html.Tr(cells))

    table = html.Table(table_rows, style={
        'width': '100%',
        'borderCollapse': 'collapse',
        'fontSize': '14px'
    })

    # Generate insights
    insights_list = []

    for _, row in df.iterrows():
        insights_list.append(html.Div([
            html.Strong(f"{row['player']}: ", style={'color': COLORS['text_primary']}),
            html.Span(f"{row['seasons']} seasons, {row['games']:,.0f} games, {row['ppg']} PPG career average")
        ], style={'marginBottom': '12px'}))

    # Find who's best at what
    best_scorer = df.loc[df['ppg'].idxmax()]
    best_rebounder = df.loc[df['rpg'].idxmax()]
    best_playmaker = df.loc[df['apg'].idxmax()]

    insights_list.append(html.Div([
        html.Hr(style={'margin': '16px 0', 'border': 'none', 'borderTop': f'1px solid {COLORS["border"]}'}),
        html.Strong('Best Scorer: ', style={'color': COLORS['text_primary']}),
        html.Span(f"{best_scorer['player']} ({best_scorer['ppg']} PPG)"),
    ], style={'marginBottom': '8px'}))

    insights_list.append(html.Div([
        html.Strong('Best Rebounder: ', style={'color': COLORS['text_primary']}),
        html.Span(f"{best_rebounder['player']} ({best_rebounder['rpg']} RPG)"),
    ], style={'marginBottom': '8px'}))

    insights_list.append(html.Div([
        html.Strong('Best Playmaker: ', style={'color': COLORS['text_primary']}),
        html.Span(f"{best_playmaker['player']} ({best_playmaker['apg']} APG)"),
    ]))

    insights = html.Div(insights_list)

    return fig, table, insights

# ============================================================================
# RUN APP
# ============================================================================

# Expose server for deployment (Render, Heroku, etc.)
server = app.server

if __name__ == '__main__':
    print("\n🏀 NBA Analytics Dashboard")
    print("Modern, Apple-inspired design")
    print("Opening at: http://127.0.0.1:8051/\n")
    app.run(debug=True, host='0.0.0.0', port=8051)

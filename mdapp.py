import streamlit as st
import pandas as pd
from PIL import Image

# Load data
draft_order = pd.read_csv("draft_order.csv")
team_needs = pd.read_csv("team_needs.csv")
player_data = pd.read_csv("player_board.csv", encoding="latin1")  # fix for special characters
team_logos = pd.read_csv("teamlogos.csv")

# Combine Need columns into a single 'Needs' list
need_cols = ['Need 1', 'Need 2', 'Need 3', 'Need 4', 'Need 5']
team_needs['Needs'] = team_needs[need_cols].apply(lambda x: [need for need in x if pd.notna(need)], axis=1)

# Initialize session state
if 'drafted_players' not in st.session_state:
    st.session_state['drafted_players'] = []
    
if 'selected_player' not in st.session_state:
    st.session_state['selected_player'] = None

if 'selected_tab' not in st.session_state:
    st.session_state['selected_tab'] = "All"

# Function to handle drafting a player
def draft_player(player_name):
    if len(st.session_state.drafted_players) < len(draft_order):
        pick_row = draft_order.iloc[len(st.session_state.drafted_players)]
        draft_result = {
            "Pick": pick_row["Pick"],
            "Team": pick_row["Team"],
            "Name": player_name
        }
        st.session_state.drafted_players.append(draft_result)
        st.session_state.selected_player = None
        st.rerun()

# Function to handle player selection
def select_player(player_name):
    st.session_state.selected_player = player_name
    st.rerun()

# Streamlit setup
st.set_page_config(layout="wide", page_title="NFL Draft Simulator")
st.markdown("""
    <style>
        .main, .block-container {
            background-color: white !important;
            color: black !important;
            padding: 10px !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: black !important;
        }
        
        /* Draft Order Styling */
        .draft-order {
            background-color: #f7f7f7;
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #ddd;
            margin-bottom: 20px;
        }
        .draft-item {
            display: flex;
            align-items: center;
            padding: 8px 10px;
            margin-bottom: 5px;
            border-radius: 4px;
        }
        .current-pick {
            background-color: #fff3cd !important;
            border-left: 4px solid #ffc107;
        }
        .completed-pick {
            background-color: #d4edda !important;
            border-left: 4px solid #28a745;
        }
        
        /* Draft Board Styling */
        .player-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .player-table th {
            background-color: #2c3e50;
            color: white;
            text-align: left;
            padding: 12px 15px;
            font-weight: bold;
        }
        
        .player-table tr {
            border-bottom: 1px solid #ddd;
        }
        
        .player-table tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        .player-table tr:hover {
            background-color: #e6f7ff;
        }
        
        .player-table td {
            padding: 12px 15px;
            vertical-align: middle;
        }
        
        /* Position Badges */
        .position-badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
            text-align: center;
            min-width: 50px;
        }
        .position-offense {
            background-color: #d4edda;
            color: #155724;
        }
        .position-defense {
            background-color: #cce5ff;
            color: #004085;
        }
        
        /* Draft Button */
        .draft-btn {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            width: 100%;
            font-size: 16px;
            margin: 15px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .draft-btn:hover {
            background-color: #0056b3;
            transform: translateY(-2px);
        }
        .draft-btn:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        
        /* Tab styling */
        .tab-container {
            display: flex;
            margin-bottom: 15px;
            border-bottom: 1px solid #dee2e6;
        }
        .tab {
            flex: 1;
            text-align: center;
            padding: 10px 20px;
            cursor: pointer;
            border: 1px solid #dee2e6;
            border-bottom: none;
            border-radius: 5px 5px 0 0;
            background-color: #f8f9fa;
            transition: all 0.2s ease;
        }
        .tab.active {
            background-color: #fff;
            border-bottom: 2px solid #007bff;
            font-weight: bold;
        }
        
        /* Action buttons */
        .stButton > button {
            background-color: #007bff !important;
            color: white !important;
            padding: 0.5rem 1rem !important;
            font-weight: bold !important;
            border: none !important;
            border-radius: 4px !important;
            transition: background-color 0.2s !important;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #0056b3 !important;
        }
        
        /* Fix selectbox styling */
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: white;
            border-radius: 4px;
            border: 1px solid #ccc;
            color: black;
            padding: 8px 12px;
        }
        
        /* Align columns properly */
        div[data-testid="column"] {
            padding: 0 10px;
        }
        
        /* Team needs pills */
        .team-needs-pill {
            display: inline-block;
            background-color: #e9ecef;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.9em;
            margin-right: 5px;
            margin-bottom: 5px;
        }
        
        /* Select button styling */
        .select-btn {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.2s;
        }
        
        .select-btn:hover {
            background-color: #0056b3;
        }
        
        /* Selected player highlight */
        .selected-player {
            background-color: #e6f7ff; 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 15px; 
            border-left: 4px solid #007bff;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🏈 NFL Draft Simulator")

# Layout: Two columns
col_sidebar, col_main = st.columns([1, 3])

# Sidebar layout for draft order
with col_sidebar:
    st.markdown("### 📝 Overall Draft Order")
    
    # Create draft order display
    with st.container():
        st.markdown('<div class="draft-order">', unsafe_allow_html=True)
        
        # Merge draft order with team logos for display
        draft_order_with_logos = draft_order.merge(team_logos, left_on='Team', right_on='team_code', how='left')
        draft_order_with_logos = draft_order_with_logos[['Pick', 'Team', 'url']].sort_values(by='Pick')

        # Add drafted players to the draft order
        for i, row in draft_order_with_logos.iterrows():
            if i < len(st.session_state.drafted_players):
                # Display drafted player next to the team
                drafted_player = st.session_state.drafted_players[i]['Name']
                team_display = f"""
                <div class="draft-item completed-pick">
                    <img src="{row['url']}" style="width: 30px; height: 30px; margin-right: 10px;">
                    <div>
                        <span><b>Pick {row['Pick']}:</b> {row['Team']}</span><br>
                        <span style="font-weight: bold;">{drafted_player}</span>
                    </div>
                </div>
                """
            elif i == len(st.session_state.drafted_players):
                # Highlight the current team picking
                team_display = f"""
                <div class="draft-item current-pick">
                    <img src="{row['url']}" style="width: 30px; height: 30px; margin-right: 10px;">
                    <div>
                        <span><b>Pick {row['Pick']}:</b> {row['Team']}</span><br>
                        <span style="font-style: italic;">On the clock</span>
                    </div>
                </div>
                """
            else:
                # Display remaining teams without highlighting
                team_display = f"""
                <div class="draft-item">
                    <img src="{row['url']}" style="width: 30px; height: 30px; margin-right: 10px;">
                    <span><b>Pick {row['Pick']}:</b> {row['Team']}</span>
                </div>
                """
            st.markdown(team_display, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Show team needs for the current team
    if len(st.session_state.drafted_players) < len(draft_order):
        current_team = draft_order.iloc[len(st.session_state.drafted_players)]['Team']
        team_need = team_needs[team_needs['Team'] == current_team]
        
        if not team_need.empty:
            st.markdown(f"### {current_team} Team Needs")
            needs_list = team_need['Needs'].iloc[0]
            needs_html = '<div style="display: flex; flex-wrap: wrap; gap: 5px;">'
            for need in needs_list:
                needs_html += f'<span class="team-needs-pill">{need}</span>'
            needs_html += '</div>'
            st.markdown(needs_html, unsafe_allow_html=True)

# Main draft board and actions
with col_main:
    st.markdown("## 📋 Draft Board")

    # Define position categories
    offense_positions = ['QB', 'RB', 'WR', 'TE', 'OT', 'OG', 'OC']
    defense_positions = ['CB', 'S', 'EDGE', 'DT', 'LB']
    
    # Handle tab selection with better state management
    # Use columns for tabs to ensure even spacing
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Render tabs
    with col1:
        all_tab = st.button("All", key="all_tab", use_container_width=True)
    with col2:
        offense_tab = st.button("Offense", key="offense_tab", use_container_width=True)
    with col3:
        defense_tab = st.button("Defense", key="defense_tab", use_container_width=True)

    # Apply custom styling to active tab with CSS
    st.markdown(f"""
    <style>
    /* Style active tab based on current state */
    div[data-testid="stHorizontalBlock"] > div:nth-child({1 if st.session_state.selected_tab == "All" else (2 if st.session_state.selected_tab == "Offense" else 3)}) button {{
        background-color: #007bff !important;
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Update session state based on tab button clicks
    if all_tab:
        st.session_state.selected_tab = "All"
        st.rerun()
    elif offense_tab:
        st.session_state.selected_tab = "Offense"
        st.rerun()
    elif defense_tab:
        st.session_state.selected_tab = "Defense"
        st.rerun()

    # Filter based on position group
    if st.session_state.selected_tab == "All":
        position_options = ["All"] + sorted(offense_positions + defense_positions)
        filtered_board = player_data
    elif st.session_state.selected_tab == "Offense":
        position_options = ["All Offense"] + offense_positions
        filtered_board = player_data[player_data['Position'].isin(offense_positions)]
    else:  # Defense
        position_options = ["All Defense"] + defense_positions
        filtered_board = player_data[player_data['Position'].isin(defense_positions)]
    
    # Show team needs for the current team in main column too
    if len(st.session_state.drafted_players) < len(draft_order):
        current_team = draft_order.iloc[len(st.session_state.drafted_players)]['Team']
        team_need = team_needs[team_needs['Team'] == current_team]
        
        if not team_need.empty:
            st.markdown(f"### {current_team} is on the clock")
            needs_list = team_need['Needs'].iloc[0]
            needs_html = '<div style="display: flex; flex-wrap: wrap; margin-bottom: 15px;">'
            for need in needs_list:
                needs_html += f'<span class="team-needs-pill">{need}</span>'
            needs_html += '</div>'
            st.markdown(needs_html, unsafe_allow_html=True)

    # Initialize position filter if not in session state
    if 'position_filter' not in st.session_state:
        st.session_state.position_filter = "All" if st.session_state.selected_tab == "All" else "All Offense" if st.session_state.selected_tab == "Offense" else "All Defense"
    
    # Position filter with display of current selection
    position_filter = st.selectbox(
        "Filter by Position:", 
        position_options,
        index=position_options.index(st.session_state.position_filter) if st.session_state.position_filter in position_options else 0,
        format_func=lambda x: x  # Show exactly what's selected
    )
    
    # Update session state when filter changes
    if position_filter != st.session_state.position_filter:
        st.session_state.position_filter = position_filter

    # Apply position filter
    if position_filter == "All":
        pass  # No filtering needed
    elif position_filter == "All Offense":
        filtered_board = player_data[player_data['Position'].isin(offense_positions)]
    elif position_filter == "All Defense":
        filtered_board = player_data[player_data['Position'].isin(defense_positions)]
    else:
        filtered_board = filtered_board[filtered_board['Position'] == position_filter]

    # Exclude already drafted players
    filtered_board = filtered_board[~filtered_board['Name'].isin([p['Name'] for p in st.session_state.drafted_players])]

    # Sort by rank
    filtered_board = filtered_board.sort_values(by='Rank')
    
    # Fix player selection display - make it cleaner
    if st.session_state.selected_player:
        try:
            player_info = filtered_board[filtered_board['Name'] == st.session_state.selected_player].iloc[0]
            position_class = "position-offense" if player_info['Position'] in offense_positions else "position-defense"
            
            # Create a clean selected player box
            st.markdown(f"""
            <div style="background-color: #e6f7ff; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #007bff;">
                <h4 style="margin: 0; color: #007bff;">Selected Player:</h4>
                <div style="font-size: 1.2em; font-weight: bold; margin: 8px 0;">{player_info['Name']}</div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span style="background-color: {'#d4edda' if player_info['Position'] in offense_positions else '#cce5ff'}; 
                                 color: {'#155724' if player_info['Position'] in offense_positions else '#004085'};
                                 padding: 4px 10px;
                                 border-radius: 4px;
                                 font-weight: bold;">{player_info['Position']}</span>
                    <span>Rank: {player_info['Rank']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Better draft button
            draft_button = st.button(
                f"Draft {player_info['Position']} {player_info['Name']}",
                key="draft_selected_player",
                use_container_width=True,
                type="primary"  # Make it stand out
            )
            
            if draft_button:
                draft_player(player_info['Name'])
                
        except (IndexError, KeyError):
            # Handle case where selected player is not in filtered board
            st.session_state.selected_player = None
            st.warning("Selected player is not available with current filters. Please select another player.")
    else:
        # Disabled draft button when no player is selected
        st.button(
            "Select a player first",
            key="draft_button_disabled",
            disabled=True,
            use_container_width=True
        )
    
    # Remove duplicate header
    st.markdown("## Select a Player to Draft")
    
    # Fix duplicate "Select a Player to Draft" headers
    st.markdown("### Select a Player to Draft")
    
    # Add custom component for direct player selection without page reload
    from streamlit.components.v1 import html

    # Create a better selection mechanism with JavaScript
    js_code = """
    <script>
    // Function to handle player selection with a callback
    function selectPlayer(playerName) {
        // Get the hidden form input and set its value
        const hiddenInput = document.getElementById('player-selection-input');
        hiddenInput.value = playerName;
        
        // Trigger the form submission
        const form = document.getElementById('selection-form');
        form.dispatchEvent(new Event('submit'));
        
        // Prevent default behavior
        return false;
    }
    </script>
    
    <!-- Hidden form for selection -->
    <form id="selection-form" style="display:none;">
        <input type="text" id="player-selection-input" name="player_selection">
    </form>
    """
    
    html(js_code, height=0)
    
    # Create a simple form to capture the selection with hidden submit button
    with st.form(key="player_form", clear_on_submit=False):
        selected_player_name = st.text_input("Selected Player", 
                                           key="player_selection_input", 
                                           value=st.session_state.selected_player or "",
                                           label_visibility="collapsed")
        
        # Add the submit button but hide it with custom CSS
        st.markdown("""
        <style>
        /* Hide the submit button */
        section[data-testid="stForm"] > div[data-testid="stFormSubmitButton"] {
            visibility: hidden;
            height: 0px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        submit_button = st.form_submit_button("Update")
    
    # Update selection state if form is submitted
    if submit_button or (selected_player_name and selected_player_name != st.session_state.selected_player):
        st.session_state.selected_player = selected_player_name
    
    st.markdown("""
    <style>
    /* Player row styling */
    .player-row {
        display: flex;
        padding: 12px 15px;
        border: 1px solid #ddd;
        border-radius: 6px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.2s;
        background-color: white;
    }
    
    .player-row:hover {
        background-color: #f0f7ff;
        transform: translateY(-2px);
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
    
    .player-row.selected {
        background-color: #e6f7ff;
        border: 2px solid #007bff;
    }
    
    .player-rank {
        flex: 0 0 60px;
        font-weight: bold;
    }
    
    .player-position {
        flex: 0 0 80px;
    }
    
    .player-name {
        flex: 1;
        font-weight: bold;
    }
    
    /* Position badge in row */
    .row-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        text-align: center;
        min-width: 40px;
        font-size: 0.85em;
    }
    </style>
    
    <script>
    // JavaScript to handle row clicks without page navigation
    function selectPlayer(playerName) {
        // Set the player name in the URL
        const url = new URL(window.location);
        url.searchParams.set('player', playerName);
        window.history.pushState({}, '', url);
        
        // Reload the page to handle the selection
        window.location.reload();
        
        // Prevent default navigation
        return false;
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Create a single row for displaying players in a table format
    st.markdown("""
    <style>
    /* Table styling */
    .player-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .player-table th {
        background-color: #2c3e50;
        color: white;
        text-align: left;
        padding: 12px 15px;
        font-weight: bold;
        font-size: 14px;
    }
    
    .player-table tr {
        border-bottom: 1px solid #ddd;
    }
    
    .player-table tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    .player-table tr:hover {
        background-color: #e6f7ff;
    }
    
    .player-table tr.selected {
        background-color: #e6f7ff;
        border-left: 4px solid #007bff;
    }
    
    .player-table td {
        padding: 12px 15px;
        vertical-align: middle;
        font-size: 14px;
    }
    
    /* Badge styling */
    .position-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        text-align: center;
        min-width: 40px;
        font-size: 0.85em;
    }
    
    /* Streamlit button overrides */
    .stButton > button {
        height: auto !important;
        padding: 6px 12px !important;
        font-size: 14px !important;
        white-space: normal !important;
        text-align: left !important;
        line-height: 1.4 !important;
    }
    
    /* Selected button styling */
    .selected-button > button {
        background-color: #e6f7ff !important;
        border-color: #007bff !important;
        border-width: 2px !important;
        color: #0366d6 !important;
        font-weight: bold !important;
    }
    
    /* Fix duplicate headers */
    #select-a-player-to-draft, #select-a-player-to-draft-1 {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create player table layout with columns
    num_players = min(20, len(filtered_board))
    if num_players > 0:
        # Use a container for better spacing
        with st.container():
            # Create player listing in a table-like format
            for i in range(0, num_players, 2):
                col1, col2 = st.columns(2)
                
                # First player in row
                with col1:
                    if i < num_players:
                        player = filtered_board.iloc[i]
                        is_selected = st.session_state.selected_player == player['Name']
                        
                        # Apply conditional styling based on selection
                        if is_selected:
                            st.markdown('<div class="selected-button">', unsafe_allow_html=True)
                            
                        if st.button(
                            f"#{player['Rank']} {player['Position']} {player['Name']}",
                            key=f"player_{i}",
                            use_container_width=True
                        ):
                            select_this_player(player['Name'])
                            
                        if is_selected:
                            st.markdown('</div>', unsafe_allow_html=True)
                
                # Second player in row
                with col2:
                    if i+1 < num_players:
                        player = filtered_board.iloc[i+1]
                        is_selected = st.session_state.selected_player == player['Name']
                        
                        # Apply conditional styling based on selection
                        if is_selected:
                            st.markdown('<div class="selected-button">', unsafe_allow_html=True)
                            
                        if st.button(
                            f"#{player['Rank']} {player['Position']} {player['Name']}",
                            key=f"player_{i+1}",
                            use_container_width=True
                        ):
                            select_this_player(player['Name'])
                            
                        if is_selected:
                            st.markdown('</div>', unsafe_allow_html=True)
    
    # Check URL parameters for player selection
    params = st.experimental_get_query_params()
    if 'player' in params:
        player_name = params['player'][0]
        # Verify the player exists in our data
        if player_name in filtered_board['Name'].values:
            st.session_state.selected_player = player_name
        # Clear the parameter
        st.experimental_set_query_params()
        st.rerun()

    # Display drafted players section
    if st.session_state.drafted_players:
        st.markdown("### 📋 Draft Results")
        
        # Create a styled table for draft results
        results_html = """
        <table class="player-table">
            <thead>
                <tr>
                    <th>Pick</th>
                    <th>Team</th>
                    <th>Player</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for result in st.session_state.drafted_players:
            results_html += f"""
            <tr>
                <td>{result['Pick']}</td>
                <td>{result['Team']}</td>
                <td>{result['Name']}</td>
            </tr>
            """
        
        results_html += """
            </tbody>
        </table>
        """
        
        st.markdown(results_html, unsafe_allow_html=True)

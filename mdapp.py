import streamlit as st
import pandas as pd
from PIL import Image

# Load data with error handling
try:
    draft_order = pd.read_csv(r"draft_order.csv")
    team_needs = pd.read_csv(r"team_needs.csv")
    player_data = pd.read_csv(r"player_board.csv", encoding="latin1")  # fix for special characters
    team_logos = pd.read_csv(r"nfl_teamlogos.csv")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Combine Need columns into a single 'Needs' list
need_cols = ['Need 1', 'Need 2', 'Need 3', 'Need 4', 'Need 5']
team_needs['Needs'] = team_needs[need_cols].apply(lambda x: [need for need in x if pd.notna(need)], axis=1)

# Streamlit setup
st.set_page_config(layout="wide", page_title="NFL Draft Simulator")
st.markdown("""
    <style>
        .main, .block-container {
            background-color: white !important;
            color: black !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: black !important;
        }
        .stDataFrame {
            background-color: white;
        }
        .stDataFrame > div > div {
            background-color: #f2f2f2 !important;
            border: 1px solid black !important;
            border-radius: 0px !important;
            color: black !important;
        }
        .stTabs [role="tab"] {
            background-color: black !important;
            color: white !important;
            padding: 10px;
            border: 1px solid #ccc;
            margin-right: 4px;
            border-radius: 0px !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: white !important;
            color: black !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🧠 NFL Draft Simulator")

# Layout: Two columns
col_sidebar, col_main = st.columns([1, 3])

# Sidebar layout for team selection and needs
with col_sidebar:
    team_selected = st.selectbox("Select Team", draft_order['Team'].unique())
    team_picks = draft_order[draft_order['Team'] == team_selected]
    team_need_row = team_needs[team_needs['Team'] == team_selected]

    logo_url = team_logos.loc[team_logos['team_code'] == team_selected, 'url'].values[0]
    st.image(logo_url, width=100)

    st.markdown("### 📝 Draft Order")
    st.dataframe(team_picks[['Round', 'Pick', 'Team']].sort_values(by='Pick'), use_container_width=True, height=400)

    st.markdown("### 📌 Team Needs")
    if not team_need_row.empty:
        needs_display = ', '.join(team_need_row['Needs'].values[0])
        st.markdown(f"**Needs:** {needs_display}")
    else:
        st.write("No needs found.")

# Main draft board and actions
with col_main:
    st.markdown("## 🧾 Full Draft Board")

    # Tabs for Offense and Defense
    offense_positions = ['QB', 'RB', 'WR', 'TE', 'OT', 'OG', 'OC']
    defense_positions = ['CB', 'S', 'EDGE', 'DT', 'LB']

    tab1, tab2 = st.tabs(["Offense", "Defense"])

    if 'drafted_players' not in st.session_state:
        st.session_state.drafted_players = []

    with tab1:
        filtered_board = player_data[player_data['Position'].isin(offense_positions)]
        filtered_board = filtered_board[~filtered_board['Name'].isin([p['Name'] for p in st.session_state.drafted_players])]
        selected_player = st.selectbox("Select Player to Draft (Offense)", filtered_board['Name'])
        st.dataframe(filtered_board[['Rank', 'Name', 'Position']].sort_values(by='Rank'), use_container_width=True, height=400)

    with tab2:
        filtered_board = player_data[player_data['Position'].isin(defense_positions)]
        filtered_board = filtered_board[~filtered_board['Name'].isin([p['Name'] for p in st.session_state.drafted_players])]
        selected_player = st.selectbox("Select Player to Draft (Defense)", filtered_board['Name'])
        st.dataframe(filtered_board[['Rank', 'Name', 'Position']].sort_values(by='Rank'), use_container_width=True, height=400)

    if st.button("Draft Player"):
        try:
            pick_row = draft_order.sort_values(by='Pick').iloc[len(st.session_state.drafted_players)]
            draft_result = {
                "Pick": pick_row["Pick"],
                "Team": pick_row["Team"],
                "Name": selected_player
            }
            st.session_state.drafted_players.append(draft_result)
            st.success(f"{pick_row['Team']} selected {selected_player} at Pick {pick_row['Pick']}")
        except IndexError:
            st.error("No more picks available. Draft completed.")

    if st.session_state.drafted_players:
        st.markdown("## 📝 Draft Tracker")
        st.dataframe(pd.DataFrame(st.session_state.drafted_players).sort_values(by='Pick'), use_container_width=True, height=400)

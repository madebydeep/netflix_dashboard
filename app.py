# app.py — Enhanced & Polished Netflix Dashboard (full file)


import pandas as pd
import plotly.express as px
import streamlit as st
from io import StringIO
from plotly.colors import qualitative, sequential

DF_PATH = "https://raw.githubusercontent.com/madebydeep/netflix_dashboard/main/netflix_titles.csv"
try:
    df = pd.read_csv(DF_PATH)
except Exception as e:
    st.error(f"Could not load {DF_PATH}: {e}")
    st.stop()
# ---------- Page config ----------
st.set_page_config(page_title="Netflix Dashboard", layout="wide")
st.markdown("<h1 class='big-title'>🎬 Netflix Dashboard</h1>", unsafe_allow_html=True)
st.write("This dashboard lets you explore the Netflix catalog interactively using filters, charts, and summary metrics.\nYou can search by country, genre, type, title, or actors to instantly narrow down the dataset.\nEach section below highlights different aspects of Netflix content — such as what types of shows are most common, how releases changed over time, and which genres, directors, and actors dominate the platform.")
st.write("Experience Multi-select filters, Release charts, Find top directors & actors, and download the filtered CSV.")

# ---------- Minimal CSS for polish ----------
st.markdown(
    """
    <style>
    .big-title { font-size: 28px; font-weight:700; color:#0f172a; margin-bottom:6px; }
    .card { background: linear-gradient(180deg, #ffffffcc, #f8fafbcc); border-radius: 10px; padding: 10px; box-shadow: 0 6px 18px rgba(15,23,42,0.06); }
    .kpi { padding:8px; border-radius:8px; background:linear-gradient(90deg,#eef2ff,#f0f9ff); text-align:center; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
.kpi-box {
    padding: 20px;
    background: #f8fafc; /* light gray-blue */
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    margin-bottom: 25px;
}
.kpi-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.kpi-container {
    display: flex;
    gap: 20px;
    margin-bottom: 25px;
}

.kpi-card {
    flex: 1;
    background: #ffffff;
    border-radius: 12px;
    padding: 10px;
    text-align: center;
    border: 1px solid #e2e8f0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}

.kpi-card h3 {
    font-size: 16px;
    font-weight: 600;
    color: #475569;
    margin-bottom: 8px;
}

.kpi-card p {
    font-size: 24px;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Sidebar background */
section[data-testid='stSidebar'] {
    background: #111 !important;              /* almost-black */
    padding-top: 20px;
    border-right: 1px solid #222;
}

/* Sidebar text */
section[data-testid='stSidebar'] * {
    color: #f8f8f8 !important;
}

/* Sidebar header text */
section[data-testid='stSidebar'] h1,
section[data-testid='stSidebar'] h2,
section[data-testid='stSidebar'] h3 {
    color: #d10f18 !important;               /* Netflix Red */
    font-weight: 700;
}

/* Input fields */
section[data-testid='stSidebar'] .stTextInput > div > div > input,
section[data-testid='stSidebar'] .stMultiSelect,
section[data-testid='stSidebar'] .stSelectbox,
section[data-testid='stSidebar'] .stSlider {
    background-color: #111 !important;
    color: #ffffff !important;
    border-radius: 6px;
    border: 1px solid #333 !important;
    padding: 8px;
}

/* Checkbox and labels */
section[data-testid='stSidebar'] label {
    color: #e5e5e5 !important;
}

/* Buttons */
section[data-testid='stSidebar'] button {
    background: #E50914 !important;
    color: #fff !important;
    border-radius: 6px;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)


# ---------- Load dataset ----------
DF_PATH = "netflix_titles.csv"
df = pd.read_csv(DF_PATH)

# ---------- Clean / normalize columns ----------
# Country
df['country'] = df.get('country', pd.Series(['Unknown'] * len(df))).fillna('Unknown').astype(str)
df['country'] = df['country'].str.strip().apply(lambda x: x.lstrip(',').strip())
# keep first country for filtering
df['country'] = df['country'].apply(lambda x: x.split(',')[0].strip() if x and x.lower() != 'nan' else 'Unknown')

# Genres (listed_in)
df['listed_in'] = df.get('listed_in', pd.Series(['Unknown'] * len(df))).fillna('Unknown').astype(str)
df['listed_in'] = df['listed_in'].apply(lambda s: ', '.join([g.strip() for g in s.split(',')]) if s else 'Unknown')

# Cast and director columns
df['cast'] = df.get('cast', pd.Series([''] * len(df))).fillna('').astype(str)
df['director'] = df.get('director', pd.Series([''] * len(df))).fillna('').astype(str)

# release_year numeric
df['release_year'] = pd.to_numeric(df.get('release_year', pd.Series([pd.NA]*len(df))), errors='coerce')

# ---------- Build filter lists ----------
type_options = ["All"]
if 'type' in df.columns:
    type_options += sorted(df['type'].dropna().unique().tolist())

country_options = sorted(df['country'].dropna().unique().tolist())
all_genres = df['listed_in'].dropna().apply(lambda s: [g.strip() for g in s.split(',')]).explode()
genre_options = sorted(all_genres.dropna().unique().tolist())

# Year slider bounds (fallbacks)
year_min = int(df['release_year'].min()) if pd.notna(df['release_year'].min()) else 2000
year_max = int(df['release_year'].max()) if pd.notna(df['release_year'].max()) else 2024

# ---------- Sidebar (session_state-safe) ----------
st.sidebar.header("🎛 Filters & Search")
st.sidebar.caption("Use these controls to narrow down Netflix titles by type, country, genre, actors, and keywords.")

# Initialize session_state keys (only if missing)
if 'type' not in st.session_state: st.session_state['type'] = "All"
if 'countries' not in st.session_state: st.session_state['countries'] = []
if 'genres' not in st.session_state: st.session_state['genres'] = []
if 'title_search' not in st.session_state: st.session_state['title_search'] = ""
if 'actor_search' not in st.session_state: st.session_state['actor_search'] = ""
if 'year_range' in st.session_state:
    del st.session_state['year_range']


# Widgets (bind to keys; do NOT pass `default=` to avoid double-assignment warnings)
st.sidebar.selectbox("Type (Movie / TV Show)", type_options, key='type')
st.sidebar.multiselect("🌍 Country (multi-select)", country_options, key='countries')
st.sidebar.multiselect("🏷️ Genre (multi-select)", genre_options, key='genres')
st.sidebar.text_input("🔎 Search Title", key='title_search')
st.sidebar.text_input("🌟 Search Actor", key='actor_search')

# Reset callback (modify session_state in callback — allowed)
def reset_filters():
    st.session_state['type'] = "All"
    st.session_state['countries'] = []
    st.session_state['genres'] = []
    st.session_state['title_search'] = ""
    st.session_state['actor_search'] = ""


st.sidebar.button("Reset Filters", on_click=reset_filters)

# ---------- Apply filters (robust version) ----------
filtered = df.copy()  # start with full df, then restrict

# --- Type filter ---
sel_type = st.session_state.get('type', "All")
if sel_type and sel_type != "All" and 'type' in filtered.columns:
    filtered = filtered[filtered['type'] == sel_type]

# --- Countries filter (multi-select) ---
sel_countries = st.session_state.get('countries', []) or []
if sel_countries and 'country' in filtered.columns:
    # ensure types align (strip whitespace)
    filtered['country'] = filtered['country'].astype(str).str.strip()
    filtered = filtered[filtered['country'].isin([c.strip() for c in sel_countries])]

# --- Genres filter (OR across selected genres) ---
sel_genres = st.session_state.get('genres', []) or []
if sel_genres and 'listed_in' in filtered.columns:
    mask = pd.Series(False, index=filtered.index)
    for g in sel_genres:
        # case-insensitive contains; safe for NaNs
        mask |= filtered['listed_in'].str.contains(g, case=False, na=False)
    filtered = filtered[mask]

# --- Title search (case-insensitive substring) ---
title_search = st.session_state.get('title_search', "")
if title_search and 'title' in filtered.columns:
    filtered = filtered[filtered['title'].str.contains(title_search, case=False, na=False)]

# --- Actor / Cast search ---
actor_search = st.session_state.get('actor_search', "")
if actor_search and 'cast' in filtered.columns:
    filtered = filtered[filtered['cast'].str.contains(actor_search, case=False, na=False)]

# --- Final protective cleanup ---
# If any of the expected filter columns don't exist, we didn't apply that filter (no error).
# Remove any accidental unnamed index columns before display/export
filtered = filtered.loc[:, ~filtered.columns.str.match(r'^Unnamed')]

# ---------- KPI CARDS: animated + glass effect + dark mode + Netflix theme ----------
import streamlit.components.v1 as components

# Compute KPI numbers (safe access)
total_titles = int(len(filtered))
movies_count = int((filtered['type'] == 'Movie').sum()) if 'type' in filtered.columns else 0
tv_count = int((filtered['type'] == 'TV Show').sum()) if 'type' in filtered.columns else 0
unique_countries = int(filtered['country'].nunique()) if 'country' in filtered.columns else 0
unique_genres_count = int(
    filtered['listed_in'].dropna().apply(lambda s: [g.strip() for g in s.split(',')]).explode().nunique()
) if 'listed_in' in filtered.columns else 0

# Render one HTML block via components.html
kpi_html = f"""
<style>
:root {{
  --netflix-red: #E50914;
  --card-bg: rgba(255,255,255,0.55);
  --card-border: rgba(255,255,255,0.25);
  --glass-shadow: 0 8px 30px rgba(12,20,30,0.15);
  --text-weak: #64748b;
  --text-strong: #0f172a;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --card-bg: rgba(16,18,20,0.35);
    --card-border: rgba(255,255,255,0.06);
    --glass-shadow: 0 8px 30px rgba(0,0,0,0.6);
    --text-weak: #9aa6b2;
    --text-strong: #e6eef8;
  }}
}}
.kpi-wrap {{
  display:flex;
  gap:18px;
  align-items:stretch;
  margin-bottom:22px;
  flex-wrap:wrap;
}}
.kpi {{
  flex:1 1 0;
  min-width:150px;
  background:var(--card-bg);
  border-radius:12px;
  padding:14px 12px;
  text-align:center;
  border:1px solid var(--card-border);
  box-shadow:var(--glass-shadow);
  position:relative;
  transition: transform 220ms cubic-bezier(.2,.9,.3,1), box-shadow 220ms ease;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  overflow:hidden;
}}
.kpi:hover {{
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 18px 40px rgba(0,0,0,0.18);
}}
.kpi-top {{
  position:absolute;
  top:0; left:0; right:0;
  height:6px;
  border-top-left-radius:12px;
  border-top-right-radius:12px;
}}
.k1 {{ background: linear-gradient(90deg, #7C3AED, #6366F1); }}
.k2 {{ background: linear-gradient(90deg, #EC4899, #F97316); }}
.k3 {{ background: linear-gradient(90deg, #06B6D4, #0EA5A1); }}
.k4 {{ background: linear-gradient(90deg, #F59E0B, #F97316); }}
.k5 {{ background: linear-gradient(90deg, #10B981, #059669); }}

.kpi-icon {{
  font-size:26px;
  margin-bottom:6px;
}}
.kpi-label {{
  font-size:13px;
  color:var(--text-weak);
  font-weight:700;
  letter-spacing:0.2px;
  margin-bottom:6px;
}}
.kpi-value {{
  font-size:26px;
  font-weight:800;
  color:var(--text-strong);
  line-height:1;
}}
.kpi-sub {{
  font-size:11px;
  color:var(--text-weak);
  margin-top:6px;
}}

/* accessibility: reduce motion respected by JS as well */
@media (prefers-reduced-motion: reduce) {{
  .kpi {{ transition: none; }}
}}
</style>

<div class="kpi-wrap">
  <div class="kpi" aria-hidden="false">
    <div class="kpi-top k1"></div>
    <div class="kpi-icon">📦</div>
    <div class="kpi-label">Total Titles</div>
    <div id="kpi-total" class="kpi-value" data-target="{total_titles}">0</div>
    <div class="kpi-sub">Titles matching current filters</div>
  </div>

  <div class="kpi">
    <div class="kpi-top k2"></div>
    <div class="kpi-icon">🎬</div>
    <div class="kpi-label">Movies</div>
    <div id="kpi-movies" class="kpi-value" data-target="{movies_count}">0</div>
    <div class="kpi-sub">Total movies in selection</div>
  </div>

  <div class="kpi">
    <div class="kpi-top k3"></div>
    <div class="kpi-icon">📺</div>
    <div class="kpi-label">TV Shows</div>
    <div id="kpi-tv" class="kpi-value" data-target="{tv_count}">0</div>
    <div class="kpi-sub">Total TV shows in selection</div>
  </div>

  <div class="kpi">
    <div class="kpi-top k4"></div>
    <div class="kpi-icon">🌍</div>
    <div class="kpi-label">Countries</div>
    <div id="kpi-countries" class="kpi-value" data-target="{unique_countries}">0</div>
    <div class="kpi-sub">Distinct origin countries</div>
  </div>

  <div class="kpi">
    <div class="kpi-top k5"></div>
    <div class="kpi-icon">🏷️</div>
    <div class="kpi-label">Unique Genres</div>
    <div id="kpi-genres" class="kpi-value" data-target="{unique_genres_count}">0</div>
    <div class="kpi-sub">Genre types in selection</div>
  </div>
</div>

<script>
(function() {{
  // Respect prefers-reduced-motion
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function animateValue(el, start, end, duration) {{
    if (reduce) {{
      el.textContent = end;
      return;
    }}
    let startTime = null;
    const step = (timestamp) => {{
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      const value = Math.floor(progress * (end - start) + start);
      el.textContent = value.toLocaleString();
      if (progress < 1) {{
        window.requestAnimationFrame(step);
      }} else {{
        el.textContent = end.toLocaleString();
      }}
    }};
    window.requestAnimationFrame(step);
  }}

  // find counters
  const counters = document.querySelectorAll('.kpi-value[data-target]');
  // staggered start
  counters.forEach((el, i) => {{
    const target = Number(el.getAttribute('data-target')) || 0;
    const delay = 120 * i; // stagger
    setTimeout(() => animateValue(el, 0, target, 900 + Math.min(800, target*8)), delay);
  }});

  // subtle hover lighting effect (optional): add/remove class on hover for small highlight
  counters.forEach(el => {{
    const parent = el.closest('.kpi');
    parent.addEventListener('mouseenter', () => parent.style.transform = 'translateY(-6px) scale(1.02)');
    parent.addEventListener('mouseleave', () => parent.style.transform = '');
  }});
}})();
</script>
"""

# adjust height if your dashboard layout cuts it off (e.g., increase to 220 or 240)
components.html(kpi_html, height=220)
st.markdown("---")


# ---------- Preview & Download ----------
st.markdown("<h3 class='big-title'>📊 Filtered Dataset Preview</h3>", unsafe_allow_html=True)
st.write("Shows all Netflix titles that match your selected filters. Use it to quickly scan what content you're currently exploring.")
st.dataframe(filtered, use_container_width=True, height=360)
st.write(f"Records displayed: {len(filtered)}")

csv_buffer = StringIO()
filtered.to_csv(csv_buffer, index=False)
st.download_button("⬇️ Download filtered data as CSV", csv_buffer.getvalue(), file_name="netflix_filtered.csv", mime="text/csv")
st.markdown("---")
# ---------- Visual helpers ----------
PALETTE = qualitative.Bold if len(qualitative.Bold) > 3 else qualitative.Plotly
SEQ = sequential.Viridis
PLOTLY_DEFAULTS = dict(template="plotly_white", transition={'duration': 600, 'easing': 'cubic-in-out'})

# ---------- Polished Content Type Pie ----------
st.markdown("<h3 class='big-title'>🍿 Content Type Distribution</h3>", unsafe_allow_html=True)
st.write("This chart compares how many Movies vs. TV Shows appear in your filtered selection, helping you see what type of content dominates.")


if len(filtered) > 0 and 'type' in filtered.columns:
    type_count = filtered['type'].value_counts().reset_index(name='count')
    type_count.columns = ['Type', 'Count']

    # Netflix colors
    netflix_colors = ["#E50914", "#000000"]   # Red , Black

    fig_pie = px.pie(
    type_count,
    names='Type',
    values='Count',
    color='Type',
    color_discrete_map={
        type_count['Type'].unique()[0]: netflix_colors[0],
        type_count['Type'].unique()[1] if len(type_count) > 1 else "Other": netflix_colors[1]
        }
    )

    fig_pie.update_traces(
        textinfo='label+percent',
        pull=[0.03, 0] if len(type_count) > 1 else [0],
        hovertemplate='<b>%{label}</b><br>%{value} titles<br>%{percent:.1%}<extra></extra>',
        marker=dict(line=dict(color="#ffffff", width=1.5))
    )

    fig_pie.update_layout(
        showlegend=False,
        template="plotly_white",
        font=dict(color="#f2f2f2"),
        margin=dict(t=20, b=0, l=0, r=0)
    )


    st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.info("No data for content-type chart with current filters.")
st.markdown("---")

# ---------- Releases Over the Years (non-animated) ----------
st.markdown("<h3 class='big-title'>📅 Releases Over the Years</h3>", unsafe_allow_html=True)
st.write("This chart shows how many Netflix titles were released each year. It helps you spot trends like growth in content or years with big release spikes.")

df_year = filtered.dropna(subset=['release_year']).copy()

if len(df_year) > 0:
    df_year['release_year'] = df_year['release_year'].astype(int)

    year_counts = (
        df_year['release_year']
        .value_counts()
        .reset_index(name='count')
    )
    year_counts.columns = ['year', 'count']
    year_counts = year_counts.sort_values('year')
    year_counts = year_counts[year_counts['year'] >= 2000]

    if not year_counts.empty:
        fig_years = px.bar(
            year_counts,
            x='year',
            y='count',
            labels={'year': 'Year', 'count': 'Number of Titles'},
            title='Number of Releases by Year (2000 onwards)',
            color='count',
            color_continuous_scale=SEQ,
        )
        fig_years.update_layout(height=420, **PLOTLY_DEFAULTS)
        fig_years.update_traces(hovertemplate='Year: %{x}<br>Titles: %{y}<extra></extra>')
        st.plotly_chart(fig_years, use_container_width=True)
    else:
        st.info("No release-year data in the 2000+ range for current filters.")
else:
    st.info("No release-year data available for current filters.")
st.markdown("---")
# ---------- Top 10 Genres (polished) ----------

st.markdown("<h3 class='big-title'>🎭 Top 10 Genres</h3>", unsafe_allow_html=True)
st.write("This highlights the most common genres in the filtered dataset. It shows what types of content Netflix adds most often.")
genres_series = filtered['listed_in'].dropna().apply(lambda s: [g.strip() for g in s.split(',')])
all_genres = genres_series.explode()
top_genres = all_genres.value_counts().reset_index()
top_genres.columns = ['genre', 'count']
top_genres = top_genres.head(10)

if not top_genres.empty:
    fig_genres = px.bar(
        top_genres,
        x='genre',
        y='count',
        title='Top 10 Genres',
        labels={'genre': 'Genre', 'count': 'Count'},
        color='count',
        color_continuous_scale=SEQ
    )
    fig_genres.update_layout(xaxis_tickangle=-40, **PLOTLY_DEFAULTS)
    fig_genres.update_traces(marker_line_width=0)
    st.plotly_chart(fig_genres, use_container_width=True)
else:
    st.info("No genre data available for the selected filters.")
st.markdown("---")
# ---------- Top Directors ----------
st.markdown("<h3 class='big-title'>🎬 Top Directors</h3>", unsafe_allow_html=True)
st.write("This ranking shows which directors appear most frequently in your selection. Useful for discovering filmmakers with multiple Netflix titles.")
directors_series = filtered['director'].dropna().apply(lambda s: [d.strip() for d in s.split(',') if d.strip()!=''])
top_directors = directors_series.explode().value_counts().reset_index(name='count')
top_directors.columns = ['director', 'count']
top_directors = top_directors.head(10)

if not top_directors.empty:
    fig_dir = px.bar(
        top_directors,
        x='director',
        y='count',
        title='Top 10 Directors (filtered)',
        labels={'director':'Director','count':'Count'}
    )
    fig_dir.update_layout(xaxis_tickangle=-45, **PLOTLY_DEFAULTS)
    st.plotly_chart(fig_dir, use_container_width=True)
else:
    st.info("No director data available for selected filters.")
st.markdown("---")
# ---------- Top Actors ----------

st.markdown("<h3 class='big-title'>⭐ Top Actors</h3>", unsafe_allow_html=True)
st.write("This chart lists the actors who appear the most across your filtered Netflix titles — great for spotting frequently featured stars.")
actors_series = filtered['cast'].dropna().apply(lambda s: [a.strip() for a in s.split(',') if a.strip()!=''])
# explode then count; reset_index returns columns that can vary so set them explicitly
top_actors = actors_series.explode().value_counts().reset_index(name='count')
top_actors.columns = ['actor', 'count']   # make column names explicit and stable
top_actors = top_actors.head(15)

if not top_actors.empty:
    fig_act = px.bar(
        top_actors,
        x='actor',
        y='count',
        title='Top Actors (filtered)',
        labels={'actor':'Actor','count':'Count'}
    )
    fig_act.update_layout(xaxis_tickangle=-45, height=450, **PLOTLY_DEFAULTS)
    st.plotly_chart(fig_act, use_container_width=True)
else:
    st.info("No actor data available for selected filters.")
st.markdown("---")

# ---------- Project Footer ----------
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 1.1rem; line-height: 1.6; margin-top: 20px;">

🎬 **Netflix Dashboard — Mini Project**

This dashboard helps you explore Netflix titles using filters for genre, cast, country, and type.  
Visual insights include **genre trends**, **top actors**, **top directors**, and **release year history**.

---

📂 **Dataset Source:**  
<a href="https://www.kaggle.com/datasets/shivamb/netflix-shows" target="_blank">
Kaggle – Netflix Movies & TV Shows Dataset
</a>

---

💡 **Technologies Used:**  
Python 🐍  -  Streamlit ⚡ - Plotly -  📊 - Pandas 🧮

---

✨ **Developed by  
<span style="font-size: 1.3rem; font-weight:700; color:#E50914;">Deep Singh</span>  
<a href="https://github.com/madebydeep" target="_blank">@madebydeep</a>**

</div>
""", unsafe_allow_html=True)

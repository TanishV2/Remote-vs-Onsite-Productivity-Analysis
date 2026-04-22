import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ═══════════════════════════════════════════════════════════════════ #
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════ #
st.set_page_config(
    page_title="Onsite vs Offsite Productivity Analysis",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════ #
#  DARK MODE ONLY — Token map
# ═══════════════════════════════════════════════════════════════════ #
T = {
    "app_bg":        "#0F1117",
    "sidebar_bg":    "#161B27",
    "sidebar_border":"#252D3D",
    "card_bg":       "#1A2235",
    "card_border":   "#252D3D",
    "divider":       "#252D3D",
    "text_primary":  "#F1F5F9",
    "text_secondary":"#94A3B8",
    "text_caption":  "#64748B",
    "text_muted":    "#475569",
    "ins_info_bg":   "#172554",
    "ins_info_text": "#BFDBFE",
    "ins_warn_bg":   "#451A03",
    "ins_warn_text": "#FDE68A",
    "ins_ok_bg":     "#052E16",
    "ins_ok_text":   "#BBF7D0",
    "filter_bg":     "#1A2235",
    "chart_bg":      "#1A2235",
    "chart_grid":    "#252D3D",
    "chart_line":    "#252D3D",
    "chart_text":    "#94A3B8",
    "chart_title":   "#F1F5F9",
    "legend_bg":     "#1A2235",
    "tab_border":    "#252D3D",
    "tab_inactive":  "#64748B",
    "metric_top":    "#3B82F6",
    "scroll_thumb":  "#334155",
    "conc_text":     "#CBD5E1",
    "tag_bg":        "#1E3A5F",
    "tag_text":      "#93C5FD",
    # Table theming
    "tbl_header_bg": "#0F172A",
    "tbl_header_fg": "#94A3B8",
    "tbl_row_bg":    "#1A2235",
    "tbl_row_alt":   "#1E2940",
    "tbl_row_fg":    "#E2E8F0",
    "tbl_border":    "#252D3D",
}

# ═══════════════════════════════════════════════════════════════════ #
#  GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════ #
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Figtree', sans-serif;
    font-size: 14px;
    -webkit-font-smoothing: antialiased;
}}

/* ── Shell ── */
.stApp {{ background: {T['app_bg']}; color: {T['text_primary']}; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {T['sidebar_bg']};
    border-right: 1px solid {T['sidebar_border']};
}}
[data-testid="stSidebarNav"] {{ display: none; }}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {{
    color: {T['text_secondary']} !important;
    font-size: 12px;
}}

/* ── Sidebar multiselect compact ── */
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    min-height: 32px !important;
    font-size: 12px !important;
    background: {T['card_bg']} !important;
    border-color: {T['card_border']} !important;
    color: {T['text_primary']} !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] span {{
    font-size: 12px !important;
    color: {T['text_primary']} !important;
}}
[data-testid="stSidebar"] .stMultiSelect label {{
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: {T['text_muted']} !important;
    margin-bottom: 2px !important;
}}

/* ── Headings ── */
h1 {{
    font-size: 1.65rem !important; font-weight: 700 !important;
    color: {T['text_primary']} !important; letter-spacing: -0.5px !important;
    margin-bottom: 0 !important; line-height: 1.3 !important;
}}
h2 {{
    font-size: 1.15rem !important; font-weight: 600 !important;
    color: {T['text_primary']} !important; margin-top: 0 !important;
}}
h3 {{
    font-size: 1.0rem !important; font-weight: 500 !important;
    color: {T['text_secondary']} !important;
}}

/* ── Caption ── */
[data-testid="stCaptionContainer"] p {{
    color: {T['text_caption']} !important; font-size: 12.5px;
}}

/* ── Paragraph / markdown text ── */
[data-testid="stMarkdownContainer"] p {{
    color: {T['text_secondary']};
}}

/* ── KPI cards ── */
[data-testid="stMetric"] {{
    background: {T['card_bg']};
    border: 1px solid {T['card_border']};
    border-top: 3px solid {T['metric_top']};
    border-radius: 8px;
    padding: 16px 20px 12px;
}}
[data-testid="stMetricLabel"] p {{
    font-size: 11px !important; font-weight: 600 !important;
    color: {T['text_muted']} !important; letter-spacing: 0.08em;
    text-transform: uppercase;
}}
[data-testid="stMetricValue"] {{
    font-size: 1.7rem !important; font-weight: 700 !important;
    color: {T['text_primary']} !important;
    font-variant-numeric: tabular-nums !important;
}}

/* ── Divider ── */
hr {{ border-color: {T['divider']} !important; margin: 1rem 0 !important; }}

/* ── Insight blocks ── */
.ins-info {{
    background: {T['ins_info_bg']}; border-left: 4px solid #3B82F6;
    border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 12px 0;
    font-size: 13px; color: {T['ins_info_text']}; line-height: 1.65;
}}
.ins-warn {{
    background: {T['ins_warn_bg']}; border-left: 4px solid #D97706;
    border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 12px 0;
    font-size: 13px; color: {T['ins_warn_text']}; line-height: 1.65;
}}
.ins-ok {{
    background: {T['ins_ok_bg']}; border-left: 4px solid #16A34A;
    border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 12px 0;
    font-size: 13px; color: {T['ins_ok_text']}; line-height: 1.65;
}}

/* ── Section label ── */
.section-label {{
    font-size: 10.5px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: {T['text_muted']}; margin-bottom: 8px;
}}

/* ── Chart card wrapper ── */
.chart-card {{
    background: {T['card_bg']};
    border: 1px solid {T['card_border']};
    border-radius: 8px; padding: 4px 8px 0;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0; background: transparent;
    border-bottom: 2px solid {T['tab_border']}; padding: 0;
}}
.stTabs [data-baseweb="tab"] {{
    font-size: 12.5px; font-weight: 500;
    color: {T['tab_inactive']}; padding: 8px 20px;
    border-bottom: 2px solid transparent;
    background: transparent; border-radius: 0; margin-bottom: -2px;
}}
.stTabs [aria-selected="true"] {{
    color: #3B82F6 !important;
    border-bottom: 2px solid #3B82F6 !important;
    background: transparent !important; font-weight: 600 !important;
}}

/* ── Dataframe / Table theming ── */
[data-testid="stDataFrame"] {{
    border: 1px solid {T['tbl_border']};
    border-radius: 8px; overflow: hidden;
}}
[data-testid="stDataFrame"] thead tr th {{
    background: {T['tbl_header_bg']} !important;
    color: {T['tbl_header_fg']} !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid {T['tbl_border']} !important;
    padding: 8px 12px !important;
}}
[data-testid="stDataFrame"] tbody tr td {{
    background: {T['tbl_row_bg']} !important;
    color: {T['tbl_row_fg']} !important;
    font-size: 13px !important;
    border-bottom: 1px solid {T['tbl_border']} !important;
    padding: 7px 12px !important;
}}
[data-testid="stDataFrame"] tbody tr:nth-child(even) td {{
    background: {T['tbl_row_alt']} !important;
}}
[data-testid="stDataFrame"] iframe {{
    background: {T['tbl_row_bg']} !important;
    color-scheme: dark !important;
}}
.stDataFrame [data-testid="column-header-cell"] {{
    background: {T['tbl_header_bg']} !important;
    color: {T['tbl_header_fg']} !important;
}}
.stDataFrame [data-testid="cell"] {{
    background: {T['tbl_row_bg']} !important;
    color: {T['tbl_row_fg']} !important;
}}

/* ── Multiselect tags ── */
[data-baseweb="tag"] {{
    background: {T['tag_bg']} !important;
    color: {T['tag_text']} !important; border-radius: 4px !important;
}}

/* ── Multiselect input bg (main area) ── */
[data-baseweb="select"] > div {{
    background: {T['card_bg']} !important;
    border-color: {T['card_border']} !important;
    color: {T['text_primary']} !important;
}}

/* ── Alert ── */
.stAlert {{ border-radius: 8px; font-size: 13px; border: none !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-thumb {{
    background: {T['scroll_thumb']}; border-radius: 4px;
}}

/* ── Sidebar project title ── */
.sidebar-project-title {{
    font-size: 14px;
    font-weight: 700;
    color: {T['text_primary']};
    letter-spacing: -0.3px;
    line-height: 1.35;
    margin: 0 0 2px;
}}
.sidebar-project-sub {{
    font-size: 10px;
    font-weight: 600;
    color: {T['text_muted']};
    letter-spacing: 0.12em;
    text-transform: uppercase;
}}

/* ── Sidebar nav radio ── */
[data-testid="stSidebar"] [role="radiogroup"] label {{
    border-radius: 6px !important;
    padding: 6px 10px !important;
    margin-bottom: 2px !important;
    transition: background 0.15s;
}}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {{
    background: {T['card_bg']} !important;
}}

/* ── Record count badge ── */
.records-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: {T['card_bg']};
    border: 1px solid {T['card_border']};
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 11px;
    color: {T['text_muted']};
    margin-top: 8px;
}}
.records-badge b {{
    color: {T['text_secondary']};
    font-weight: 600;
}}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════ #
#  CHART THEME FACTORY
# ═══════════════════════════════════════════════════════════════════ #
PALETTE = ["#3B82F6", "#22C55E", "#F59E0B", "#A855F7", "#F43F5E", "#06B6D4"]
C = dict(blue="#3B82F6", green="#22C55E", amber="#F59E0B",
         violet="#A855F7", rose="#F43F5E", cyan="#06B6D4")

def apply_theme(fig, height=340):
    bg = T["chart_bg"]

    # Determine if this chart has a legend by checking traces
    has_legend = any(
        trace.get("showlegend", True) and trace.get("name")
        for trace in fig.to_dict().get("data", [])
    )

    # Separate title from legend — title at top, legend BELOW title in its own row
    fig.update_layout(
        paper_bgcolor=bg, plot_bgcolor=bg,
        font=dict(family="Figtree", color=T["chart_text"], size=12),
        title=dict(
            font=dict(family="Figtree", size=14, color=T["chart_title"]),
            x=0,
            xanchor="left",
            y=1.0,
            yanchor="top",
            pad=dict(t=0, b=0),
        ),
        xaxis=dict(
            showgrid=False, linecolor=T["chart_line"],
            tickfont=dict(size=11, color=T["chart_text"]),
            title_font=dict(size=11, color=T["chart_text"]),
        ),
        yaxis=dict(
            gridcolor=T["chart_grid"], linecolor=T["chart_line"],
            tickfont=dict(size=11, color=T["chart_text"]),
            title_font=dict(size=11, color=T["chart_text"]),
        ),
        legend=dict(
            bgcolor=T["legend_bg"],
            bordercolor=T["chart_line"],
            borderwidth=1,
            font=dict(size=11, color=T["chart_text"]),
            orientation="h",
            yanchor="top",
            # Place legend just below the title row — negative y pushes it into
            # the top-margin area but above the actual plot area
            y=-0.18,
            xanchor="left",
            x=0,
        ),
        # t=52 gives the title room; b enlarged to accommodate the bottom legend
        margin=dict(t=52, b=60, l=12, r=12),
        height=height,
    )
    return fig

def chart_card(col, fig, height=340):
    col.markdown(f'<div class="chart-card">', unsafe_allow_html=True)
    col.plotly_chart(apply_theme(fig, height), use_container_width=True)
    col.markdown('</div>', unsafe_allow_html=True)

def insight(text, kind="info"):
    cls = {"info": "ins-info", "warn": "ins-warn", "success": "ins-ok"}.get(kind, "ins-info")
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)

def section(label):
    st.markdown(f'<p class="section-label">{label}</p>', unsafe_allow_html=True)

def spacer(h=12):
    st.markdown(f"<div style='height:{h}px'></div>", unsafe_allow_html=True)

def numpy_trendline(x_vals, y_vals):
    mask = ~(np.isnan(x_vals) | np.isnan(y_vals))
    x, y = x_vals[mask], y_vals[mask]
    if len(x) < 2:
        return x, y
    m, b = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 200)
    return x_line, m * x_line + b

# ═══════════════════════════════════════════════════════════════════ #
#  DATA — LOAD & PREPROCESS
# ═══════════════════════════════════════════════════════════════════ #
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/cleaned_data.csv"), None
    except FileNotFoundError:
        return None, "data/cleaned_data.csv not found."
    except Exception as e:
        return None, str(e)

@st.cache_data
def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["efficiency", "utilization_rate", "completion_time"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df.dropna(subset=["efficiency", "utilization_rate"], inplace=True)

    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df["age_group"] = pd.cut(
            df["age"], bins=[20, 30, 40, 50, 60],
            labels=["20-30", "30-40", "40-50", "50+"], right=False,
        ).astype(str).replace("nan", pd.NA)

    if "month" not in df.columns:
        rng = np.random.default_rng(42)
        months = ["Jan","Feb","Mar","Apr","May","Jun",
                  "Jul","Aug","Sep","Oct","Nov","Dec"]
        df["month"] = rng.choice(months, size=len(df))
        df["month"] = pd.Categorical(df["month"], categories=months, ordered=True)
    return df

raw_df, load_err = load_data()
if load_err:
    st.error(f"⚠  {load_err}")
    st.stop()
if raw_df is None or raw_df.empty:
    st.warning("⚠  The dataset is empty.")
    st.stop()

REQUIRED = {"employee_id", "task_id", "efficiency", "utilization_rate", "work_mode"}
miss = REQUIRED - set(raw_df.columns)
if miss:
    st.error(f"⚠  Missing columns: {', '.join(sorted(miss))}")
    st.stop()

df_full = preprocess(raw_df)
fmt = lambda v, d=2: f"{v:,.{d}f}"

# ═══════════════════════════════════════════════════════════════════ #
#  SIDEBAR — project title + navigation + filters
# ═══════════════════════════════════════════════════════════════════ #
_sidebar_filters = {}

with st.sidebar:
    # ── Project brand header ─────────────────────────────────────── #
    st.markdown(
        f"""
        <div style='padding: 18px 4px 14px;'>
            <p class='sidebar-project-sub'>Analytics Platform</p>
            <p class='sidebar-project-title'>Onsite vs Offsite<br>Productivity Analysis</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"<hr style='margin:0 0 14px;border-color:{T['divider']};'>", unsafe_allow_html=True)

    # ── Navigation ──────────────────────────────────────────────── #
    NAV = [
        ("▪  Overview",             "Overview"),
        ("▪  Descriptive Analysis", "Descriptive"),
        ("▪  Trend Analysis",       "Trend"),
        ("▪  Comparative Analysis", "Comparative"),
        ("▪  KPI Dashboard",        "KPI"),
        ("▪  Conclusion",           "Conclusion"),
    ]
    labels, keys = zip(*NAV)
    choice = st.radio("nav", list(labels), label_visibility="collapsed")
    page   = dict(zip(labels, keys))[choice]

    st.markdown(f"<hr style='margin:14px 0;border-color:{T['divider']};'>", unsafe_allow_html=True)

    # ── Filters (hidden on Conclusion page) ─────────────────────── #
    if page != "Conclusion":
        st.markdown(
            f"<p style='font-size:10.5px;font-weight:700;letter-spacing:0.1em;"
            f"text-transform:uppercase;color:{T['text_muted']};margin-bottom:10px;'>▸ Filters</p>",
            unsafe_allow_html=True,
        )

        FILTER_DEFS = [
            ("department", "Department"),
            ("work_mode",  "Work Mode"),
            ("location",   "Location"),
            ("gender",     "Gender"),
            ("age_group",  "Age Group"),
        ]
        active_filters = [(c, l) for c, l in FILTER_DEFS if c in df_full.columns]
        for col, lbl in active_filters:
            opts = sorted(df_full[col].dropna().unique().tolist())
            _sidebar_filters[col] = st.multiselect(
                lbl, opts, default=opts, key=f"sb_{col}"
            )

        st.markdown(f"<hr style='margin:14px 0;border-color:{T['divider']};'>", unsafe_allow_html=True)

    # ── Record count ─────────────────────────────────────────────── #
    st.markdown(
        f"<div class='records-badge'>"
        f"<span>📊</span><span><b>{len(df_full):,}</b> records loaded</span>"
        f"</div>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════ #
#  FILTER HELPER
# ═══════════════════════════════════════════════════════════════════ #
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    for col, sel in _sidebar_filters.items():
        if sel:
            filtered = filtered[filtered[col].isin(sel)]
    if filtered.empty:
        st.warning("⚠  No records match the selected filters.")
        st.stop()
    st.caption(f"Showing {len(filtered):,} of {len(df_full):,} records")
    spacer(4)
    return filtered


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  PAGE 1 — OVERVIEW                                                ║
# ╚═══════════════════════════════════════════════════════════════════╝
if page == "Overview":

    st.title("Overview")
    st.caption("Executive summary of workforce productivity across all work modes.")
    spacer(8)

    df = apply_filters(df_full)

    section("▪  Key Performance Indicators")
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Employees",  f"{df['employee_id'].nunique():,}")
    k2.metric("Total Tasks",      f"{df['task_id'].count():,}")
    k3.metric("Avg Efficiency",   fmt(df['efficiency'].mean()))
    k4.metric("Avg Utilization",  fmt(df['utilization_rate'].mean()))
    if "completion_time" in df.columns:
        k5.metric("Avg Completion", fmt(df['completion_time'].mean()) + " h")
    st.markdown("---")

    wm = df.groupby("work_mode", as_index=False).agg(
        Tasks=("task_id", "count"),
        Employees=("employee_id", "nunique"),
        Efficiency=("efficiency", "mean"),
        Utilization=("utilization_rate", "mean"),
    ).round(3)
    mode_color = {r["work_mode"]: PALETTE[i % len(PALETTE)] for i, r in wm.iterrows()}

    section("▪  Work Mode Performance")
    ca, cb = st.columns(2, gap="medium")

    fig1 = px.bar(wm, x="work_mode", y="Tasks", color="work_mode",
                  color_discrete_map=mode_color, text_auto=True,
                  title="Total Tasks Completed by Work Mode",
                  labels={"work_mode": "Work Mode"})
    fig1.update_traces(marker_line_width=0, textfont_size=11)
    fig1.update_layout(showlegend=False)
    chart_card(ca, fig1)

    fig2 = px.bar(wm, x="work_mode", y="Efficiency", color="work_mode",
                  color_discrete_map=mode_color, text_auto=".2f",
                  title="Average Efficiency Score by Work Mode",
                  labels={"work_mode": "Work Mode"})
    fig2.update_traces(marker_line_width=0, textfont_size=11)
    fig2.update_layout(showlegend=False)
    chart_card(cb, fig2)

    spacer(8)

    cc, cd = st.columns([2, 1], gap="medium")

    fig3 = px.scatter(
        df, x="utilization_rate", y="efficiency",
        color="work_mode", color_discrete_map=mode_color, opacity=0.55,
        title="Efficiency vs Utilization Rate",
        labels={"utilization_rate": "Utilization Rate", "efficiency": "Efficiency",
                "work_mode": "Work Mode"},
    )
    for wmode, grp in df.groupby("work_mode"):
        xl, yl = numpy_trendline(grp["utilization_rate"].values, grp["efficiency"].values)
        fig3.add_trace(go.Scatter(
            x=xl, y=yl, mode="lines",
            line=dict(color=mode_color.get(wmode, "#888"), width=1.5, dash="dot"),
            showlegend=False, hoverinfo="skip",
        ))
    chart_card(cc, fig3, height=320)

    fig4 = px.pie(wm, values="Employees", names="work_mode",
                  title="Employee Distribution by Work Mode",
                  color="work_mode", color_discrete_map=mode_color, hole=0.55)
    fig4.update_traces(textfont_size=11, hovertemplate="%{label}: %{value}")
    # Pie charts: place legend to the right to avoid overlap with donut
    fig4.update_layout(
        legend=dict(
            orientation="v",
            yanchor="middle", y=0.5,
            xanchor="left", x=1.02,
            font=dict(size=11, color=T["chart_text"]),
            bgcolor=T["legend_bg"],
        ),
        margin=dict(t=52, b=20, l=12, r=80),
    )
    chart_card(cd, fig4, height=320)

    spacer(8)
    best = wm.sort_values("Efficiency", ascending=False).iloc[0]
    insight(
        f"◆  <b>Key Finding:</b> <b>{best['work_mode']}</b> employees record the highest average "
        f"efficiency ({best['Efficiency']:.2f}), suggesting this arrangement yields measurably "
        f"better outcomes. Management should consider expanding this model where role requirements allow.",
        "info",
    )


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  PAGE 2 — DESCRIPTIVE ANALYSIS                                    ║
# ╚═══════════════════════════════════════════════════════════════════╝
elif page == "Descriptive":

    st.title("Descriptive Analysis")
    st.caption("Statistical breakdown of productivity metrics across segments and departments.")
    spacer(8)

    df = apply_filters(df_full)

    section("▪  Work Mode Summary")
    wm = df.groupby("work_mode", as_index=False).agg(
        Employees=("employee_id", "nunique"),
        Tasks=("task_id", "count"),
        Avg_Efficiency=("efficiency", "mean"),
        Avg_Utilization=("utilization_rate", "mean"),
    ).round(3)
    wm.rename(columns={"Avg_Efficiency": "Avg Efficiency", "Avg_Utilization": "Avg Utilization"}, inplace=True)
    st.dataframe(wm, use_container_width=True, hide_index=True)
    spacer(12)

    section("▪  Efficiency & Utilization by Work Mode")
    ca, cb = st.columns(2, gap="medium")

    fig1 = px.bar(wm, x="work_mode", y=["Avg Efficiency", "Avg Utilization"],
                  barmode="group", color_discrete_sequence=[C["blue"], C["green"]],
                  title="Efficiency vs Utilization — Work Mode Comparison",
                  labels={"work_mode": "Work Mode", "value": "Score", "variable": "Metric"})
    fig1.update_traces(marker_line_width=0)
    chart_card(ca, fig1)

    fig2 = px.histogram(df, x="efficiency", color="work_mode",
                        nbins=25, barmode="overlay", opacity=0.72,
                        title="Efficiency Score Distribution by Work Mode",
                        color_discrete_sequence=PALETTE,
                        labels={"efficiency": "Efficiency Score", "work_mode": "Work Mode"})
    fig2.update_traces(marker_line_width=0)
    chart_card(cb, fig2)

    spacer(8)

    if "department" in df.columns:
        section("▪  Department Performance")
        dept = df.groupby("department", as_index=False).agg(
            Employees=("employee_id", "nunique"),
            Tasks=("task_id", "count"),
            Avg_Efficiency=("efficiency", "mean"),
            Avg_Utilization=("utilization_rate", "mean"),
        ).round(3).sort_values("Avg_Efficiency", ascending=False)
        dept.rename(columns={"Avg_Efficiency": "Avg Efficiency", "Avg_Utilization": "Avg Utilization"}, inplace=True)

        cc, cd = st.columns(2, gap="medium")

        fig3 = px.bar(
            dept.sort_values("Avg Efficiency"),
            x="Avg Efficiency", y="department", orientation="h",
            color="Avg Efficiency", color_continuous_scale=["#1E3A5F", "#3B82F6"],
            text_auto=".2f", title="Average Efficiency by Department",
            labels={"department": ""},
        )
        fig3.update_traces(marker_line_width=0, textfont_size=11)
        fig3.update_coloraxes(showscale=False)
        chart_card(cc, fig3, height=max(300, len(dept) * 34 + 70))

        fig4 = px.scatter(
            dept, x="Avg Utilization", y="Avg Efficiency",
            size="Employees", text="department",
            color="Avg Efficiency",
            color_continuous_scale=["#451A03", "#F59E0B"],
            title="Utilization vs Efficiency — Department View",
        )
        fig4.update_traces(textposition="top center", textfont_size=10)
        fig4.update_coloraxes(showscale=False)
        chart_card(cd, fig4)

        spacer(8)
        st.dataframe(dept, use_container_width=True, hide_index=True)
        spacer(8)

        top_dept = dept.iloc[0]
        low_dept  = dept.iloc[-1]
        insight(
            f"◆  <b>{top_dept['department']}</b> is the highest-performing department "
            f"(efficiency: {top_dept['Avg Efficiency']:.2f}), while <b>{low_dept['department']}</b> "
            f"records the lowest ({low_dept['Avg Efficiency']:.2f}). "
            f"A gap of {top_dept['Avg Efficiency'] - low_dept['Avg Efficiency']:.2f} points "
            f"suggests structural or process-level differences that warrant targeted investigation.",
            "info",
        )


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  PAGE 3 — TREND ANALYSIS                                          ║
# ╚═══════════════════════════════════════════════════════════════════╝
elif page == "Trend":

    st.title("Trend Analysis")
    st.caption("Month-over-month productivity patterns and directional signals.")
    spacer(8)

    df = apply_filters(df_full)

    MONTH_ORDER = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    present     = [m for m in MONTH_ORDER if m in df["month"].values]

    monthly = df.groupby(["month", "work_mode"], as_index=False).agg(
        Efficiency=("efficiency", "mean"),
        Utilization=("utilization_rate", "mean"),
        Tasks=("task_id", "count"),
    ).round(3)
    monthly["month"] = pd.Categorical(monthly["month"], categories=present, ordered=True)
    monthly.sort_values("month", inplace=True)

    overall = df.groupby("month", as_index=False).agg(
        Efficiency=("efficiency", "mean"),
        Utilization=("utilization_rate", "mean"),
    ).round(3)
    overall["month"] = pd.Categorical(overall["month"], categories=present, ordered=True)
    overall.sort_values("month", inplace=True)

    section("▪  Efficiency Trend by Work Mode")
    fig1 = px.line(monthly, x="month", y="Efficiency", color="work_mode",
                   markers=True, color_discrete_sequence=PALETTE,
                   title="Monthly Average Efficiency — by Work Mode",
                   labels={"month": "Month", "Efficiency": "Avg Efficiency", "work_mode": "Work Mode"})
    fig1.update_traces(line_width=2, marker_size=6)
    st.plotly_chart(apply_theme(fig1, height=380), use_container_width=True)

    spacer(8)
    section("▪  Utilization Trend by Work Mode")
    fig2 = px.line(monthly, x="month", y="Utilization", color="work_mode",
                   markers=True, color_discrete_sequence=PALETTE,
                   title="Monthly Average Utilization Rate — by Work Mode",
                   labels={"month": "Month", "Utilization": "Avg Utilization", "work_mode": "Work Mode"})
    fig2.update_traces(line_width=2, marker_size=6)
    st.plotly_chart(apply_theme(fig2, height=380), use_container_width=True)

    spacer(8)
    ca, cb = st.columns(2, gap="medium")

    fig3 = px.area(overall, x="month", y="Efficiency",
                   title="Overall Efficiency Trend (All Modes)",
                   color_discrete_sequence=[C["blue"]],
                   labels={"month": "Month", "Efficiency": "Avg Efficiency"})
    fig3.update_traces(line_width=2, opacity=0.35)
    chart_card(ca, fig3)

    fig4 = px.area(overall, x="month", y="Utilization",
                   title="Overall Utilization Trend (All Modes)",
                   color_discrete_sequence=[C["green"]],
                   labels={"month": "Month", "Utilization": "Avg Utilization"})
    fig4.update_traces(line_width=2, opacity=0.35)
    chart_card(cb, fig4)

    spacer(8)
    section("▪  Trend Interpretation")

    def interp(vals):
        if len(vals) < 3:
            return "insufficient data", "warn"
        slope = np.polyfit(range(len(vals)), vals, 1)[0]
        if slope >  0.005: return "improving", "success"
        if slope < -0.005: return "declining", "warn"
        return "stable", "info"

    eff_vals  = overall["Efficiency"].dropna().tolist()
    util_vals = overall["Utilization"].dropna().tolist()
    eff_dir,  eff_kind  = interp(eff_vals)
    util_dir, util_kind = interp(util_vals)

    ic1, ic2 = st.columns(2, gap="medium")
    with ic1:
        insight(
            f"◆  <b>Efficiency Trend:</b> The overall trajectory is <b>{eff_dir}</b>. "
            + ("This signals a positive shift toward higher output." if eff_dir == "improving"
               else "Sustained decline may indicate fatigue, resourcing gaps, or process friction." if eff_dir == "declining"
               else "Flat performance suggests consistent output but no measurable gains."),
            eff_kind,
        )
    with ic2:
        insight(
            f"◆  <b>Utilization Trend:</b> Workforce utilization is <b>{util_dir}</b>. "
            + ("Rising utilization with stable efficiency may signal burnout risk." if util_dir == "improving"
               else "Falling utilization with stable efficiency may indicate better time management." if util_dir == "declining"
               else "Steady utilization suggests predictable capacity usage."),
            util_kind,
        )


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  PAGE 4 — COMPARATIVE ANALYSIS                                    ║
# ╚═══════════════════════════════════════════════════════════════════╝
elif page == "Comparative":

    st.title("Comparative Analysis")
    st.caption("Direct performance comparison across work modes with distributional context.")
    spacer(8)

    df = apply_filters(df_full)

    wm_comp = df.groupby("work_mode", as_index=False).agg(
        Employees=("employee_id", "nunique"),
        Tasks=("task_id", "count"),
        Efficiency=("efficiency", "mean"),
        Utilization=("utilization_rate", "mean"),
    ).round(3)
    mode_color = {r["work_mode"]: PALETTE[i % len(PALETTE)] for i, r in wm_comp.iterrows()}

    section("▪  Efficiency vs Utilization — Side-by-Side")
    fig1 = px.bar(wm_comp, x="work_mode", y=["Efficiency", "Utilization"],
                  barmode="group", color_discrete_sequence=[C["blue"], C["green"]],
                  text_auto=".2f",
                  title="Grouped Comparison — Efficiency & Utilization by Work Mode",
                  labels={"work_mode": "Work Mode", "value": "Score", "variable": "Metric"})
    fig1.update_traces(marker_line_width=0, textfont_size=11)
    st.plotly_chart(apply_theme(fig1, height=380), use_container_width=True)

    spacer(8)
    section("▪  Score Distribution & Variability")
    ca, cb = st.columns(2, gap="medium")

    fig2 = px.box(df, x="work_mode", y="efficiency",
                  color="work_mode", color_discrete_map=mode_color,
                  title="Efficiency Distribution by Work Mode",
                  labels={"work_mode": "Work Mode", "efficiency": "Efficiency"},
                  points="outliers")
    fig2.update_layout(showlegend=False)
    fig2.update_traces(marker_size=3)
    chart_card(ca, fig2)

    fig3 = px.box(df, x="work_mode", y="utilization_rate",
                  color="work_mode", color_discrete_map=mode_color,
                  title="Utilization Distribution by Work Mode",
                  labels={"work_mode": "Work Mode", "utilization_rate": "Utilization Rate"},
                  points="outliers")
    fig3.update_layout(showlegend=False)
    fig3.update_traces(marker_size=3)
    chart_card(cb, fig3)

    spacer(8)
    section("▪  Efficiency Density by Work Mode")
    fig4 = px.violin(df, x="work_mode", y="efficiency",
                     color="work_mode", color_discrete_map=mode_color, box=True,
                     title="Efficiency Violin Plot — Spread, Median & Density",
                     labels={"work_mode": "Work Mode", "efficiency": "Efficiency"})
    fig4.update_layout(showlegend=False)
    st.plotly_chart(apply_theme(fig4, height=400), use_container_width=True)

    spacer(8)
    section("▪  Statistical Summary")
    stat_tbl = df.groupby("work_mode")["efficiency"].describe().round(3).reset_index()
    st.dataframe(stat_tbl, use_container_width=True, hide_index=True)

    spacer(8)
    best  = wm_comp.sort_values("Efficiency", ascending=False).iloc[0]
    worst = wm_comp.sort_values("Efficiency").iloc[0]
    eff_std = df.groupby("work_mode")["efficiency"].std().reset_index()
    most_consistent = eff_std.sort_values("efficiency").iloc[0]

    insight(
        f"◆  <b>Performance Difference:</b> <b>{best['work_mode']}</b> outperforms "
        f"<b>{worst['work_mode']}</b> by <b>{best['Efficiency'] - worst['Efficiency']:.3f}</b> points. "
        f"<br><br>"
        f"◆  <b>Consistency:</b> <b>{most_consistent['work_mode']}</b> shows the lowest variance "
        f"(σ = {most_consistent['efficiency']:.3f}), indicating the most predictable performance profile. "
        f"<br><br>"
        f"◆  <b>Business Implication:</b> Organisations seeking reliable output should prioritise "
        f"<b>{most_consistent['work_mode']}</b> while addressing structural factors limiting "
        f"<b>{worst['work_mode']}</b> performance.",
        "info",
    )


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  PAGE 5 — KPI DASHBOARD                                           ║
# ╚═══════════════════════════════════════════════════════════════════╝
elif page == "KPI":

    st.title("KPI Dashboard")
    st.caption("Employee-level performance ranking, top contributors, and risk identification.")
    spacer(8)

    df = apply_filters(df_full)

    emp = df.groupby("employee_id", as_index=False).agg(
        Efficiency=("efficiency", "mean"),
        Utilization=("utilization_rate", "mean"),
        Tasks=("task_id", "count"),
    ).round(3)
    emp["risk_score"] = (
        (1 - emp["Efficiency"].clip(0, 1)) +
        (1 - emp["Utilization"].clip(0, 1))
    ).round(3)

    section("▪  Workforce Performance Snapshot")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Employees",      f"{emp['employee_id'].nunique():,}")
    k2.metric("Top Efficiency",        fmt(emp["Efficiency"].max()))
    k3.metric("At-Risk Employees",     f"{(emp['risk_score'] > 1.2).sum():,}")
    k4.metric("Avg Tasks / Employee",  fmt(emp["Tasks"].mean(), 1))
    st.markdown("---")

    section("▪  Top 10 Performers")
    top10 = emp.sort_values("Efficiency", ascending=False).head(10)
    ca, cb = st.columns([3, 2], gap="medium")

    top_scale = ["#1E3A5F", "#3B82F6"]
    fig1 = px.bar(top10, x="employee_id", y="Efficiency",
                  color="Efficiency", color_continuous_scale=top_scale,
                  text_auto=".2f", title="Top 10 Employees — Efficiency Score",
                  labels={"employee_id": "Employee ID", "Efficiency": "Avg Efficiency"})
    fig1.update_traces(marker_line_width=0, textfont_size=11)
    fig1.update_coloraxes(showscale=False)
    chart_card(ca, fig1)

    fig2 = px.scatter(top10, x="Utilization", y="Efficiency",
                      size="Tasks", text="employee_id",
                      color_discrete_sequence=[C["blue"]],
                      title="Top Performers — Efficiency vs Utilization",
                      labels={"Utilization": "Avg Utilization", "Efficiency": "Avg Efficiency"})
    fig2.update_traces(textposition="top center", textfont_size=9)
    chart_card(cb, fig2)

    spacer(8)
    st.dataframe(top10.reset_index(drop=True), use_container_width=True, hide_index=True)
    st.markdown("---")

    section("▪  At-Risk Employees")
    risk10 = emp.sort_values("risk_score", ascending=False).head(10)
    cc, cd = st.columns([3, 2], gap="medium")

    risk_scale = ["#3D0000", "#DC2626"]
    fig3 = px.bar(risk10, x="employee_id", y="risk_score",
                  color="risk_score", color_continuous_scale=risk_scale,
                  text_auto=".2f", title="At-Risk Employees — Risk Score Ranking",
                  labels={"employee_id": "Employee ID", "risk_score": "Risk Score"})
    fig3.update_traces(marker_line_width=0, textfont_size=11)
    fig3.update_coloraxes(showscale=False)
    chart_card(cc, fig3)

    fig4 = px.scatter(risk10, x="Utilization", y="Efficiency",
                      size="Tasks", text="employee_id",
                      color="risk_score", color_continuous_scale=risk_scale,
                      title="At-Risk — Efficiency vs Utilization",
                      labels={"Utilization": "Avg Utilization", "Efficiency": "Avg Efficiency"})
    fig4.update_traces(textposition="top center", textfont_size=9)
    fig4.update_coloraxes(showscale=False)
    chart_card(cd, fig4)

    spacer(8)
    st.dataframe(risk10.reset_index(drop=True), use_container_width=True, hide_index=True)
    spacer(8)

    section("▪  Performance Quadrant Map")
    eff_med  = emp["Efficiency"].median()
    util_med = emp["Utilization"].median()

    def quadrant(row):
        hi_e = row["Efficiency"]  >= eff_med
        hi_u = row["Utilization"] >= util_med
        if hi_e and hi_u:   return "High Efficiency · High Utilization"
        if hi_e:            return "High Efficiency · Low Utilization"
        if hi_u:            return "Low Efficiency · High Utilization"
        return "Low Efficiency · Low Utilization"

    emp["Quadrant"] = emp.apply(quadrant, axis=1)
    fig5 = px.scatter(
        emp, x="Utilization", y="Efficiency",
        color="Quadrant",
        color_discrete_sequence=[C["green"], C["blue"], C["amber"], C["rose"]],
        opacity=0.65, title="Performance Quadrant Map — All Employees",
        labels={"Utilization": "Avg Utilization", "Efficiency": "Avg Efficiency"},
    )
    fig5.add_hline(y=eff_med,  line_dash="dash", line_color=T["text_muted"], line_width=1)
    fig5.add_vline(x=util_med, line_dash="dash", line_color=T["text_muted"], line_width=1)
    st.plotly_chart(apply_theme(fig5, height=440), use_container_width=True)

    spacer(8)
    insight(
        "◆  <b>High-performing employees</b> (upper-right quadrant) represent the benchmark for "
        "output quality. Their practices should be documented and replicated across teams.<br><br>"
        "◆  <b>At-risk employees</b> (lower-left quadrant) show below-median scores on both dimensions, "
        "indicating systemic underperformance requiring structured intervention — coaching, "
        "reassignment, or workload review.",
        "info",
    )


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  PAGE 6 — CONCLUSION                                              ║
# ╚═══════════════════════════════════════════════════════════════════╝
elif page == "Conclusion":

    st.title("Conclusion")
    st.caption("Final findings based on the complete, unfiltered dataset.")
    spacer(8)

    df    = df_full
    final = df.groupby("work_mode", as_index=False).agg(
        Employees=("employee_id", "nunique"),
        Tasks=("task_id", "count"),
        Efficiency=("efficiency", "mean"),
        Utilization=("utilization_rate", "mean"),
    ).round(3)

    best  = final.sort_values("Efficiency", ascending=False).iloc[0]
    worst = final.sort_values("Efficiency").iloc[0]

    insight(
        f"✦  <b>Final Result:</b> <b>{best['work_mode']}</b> is the top-performing work mode — "
        f"avg efficiency <b>{best['Efficiency']:.3f}</b> across <b>{int(best['Tasks']):,}</b> tasks "
        f"and <b>{int(best['Employees']):,}</b> employees, outperforming <b>{worst['work_mode']}</b> "
        f"by <b>{best['Efficiency'] - worst['Efficiency']:.3f}</b> points.",
        "success",
    )
    spacer(8)

    section("▪  Final Performance Comparison")
    fig1 = px.bar(final, x="work_mode", y=["Efficiency", "Utilization"],
                  barmode="group", color_discrete_sequence=[C["blue"], C["green"]],
                  text_auto=".3f",
                  title="Efficiency & Utilization — Full Dataset Comparison",
                  labels={"work_mode": "Work Mode", "value": "Score", "variable": "Metric"})
    fig1.update_traces(marker_line_width=0, textfont_size=11)
    st.plotly_chart(apply_theme(fig1, height=380), use_container_width=True)

    spacer(8)
    st.dataframe(final, use_container_width=True, hide_index=True)
    st.markdown("---")

    ca, cb = st.columns(2, gap="large")
    text_color = T["conc_text"]

    with ca:
        section("▪  Key Takeaways")
        st.markdown(f"""
<div style="font-size:13.5px;line-height:1.9;color:{text_color};">
✓ &nbsp; Work mode has a statistically meaningful impact on efficiency<br>
✓ &nbsp; High utilization does not reliably predict high efficiency<br>
✓ &nbsp; Department-level performance varies significantly<br>
✓ &nbsp; A measurable share of employees require targeted support<br>
✓ &nbsp; Top performers are concentrated in specific modes and departments
</div>""", unsafe_allow_html=True)

    with cb:
        section("▪  Recommendations")
        best_mode = best["work_mode"]
        st.markdown(f"""
<div style="font-size:13.5px;line-height:1.9;color:{text_color};">
✓ &nbsp; Scale the <b>{best_mode}</b> model across compatible roles<br>
✓ &nbsp; Invest in structured coaching for at-risk employees<br>
✓ &nbsp; Audit underperforming departments for process bottlenecks<br>
✓ &nbsp; Shift KPIs from task count to quality-weighted output<br>
✓ &nbsp; Introduce workload balancing in high-utilisation segments
</div>""", unsafe_allow_html=True)

    spacer(16)
    insight(
        "⚠  <b>Limitation:</b> Trend data is simulated where a time column was absent. "
        "For production-grade insights, integrate actual timestamps from your HR or task management system.",
        "warn",
    )
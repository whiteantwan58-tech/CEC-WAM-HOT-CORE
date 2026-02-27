# /mnt/data/eve_sovereign_v6_updated.py
# pip install streamlit plotly pandas python-dotenv openai
# Run with: streamlit run eve_sovereign_v6_updated.py

from __future__ import annotations

import os
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration resolved from environment and local assets."""

    groq_api_key: Optional[str]
    groq_model: str
    technical_csv_path: Path
    core_markdown_path: Path


def resolve_config() -> AppConfig:
    """Load environment variables and resolve local asset paths."""
    load_dotenv()

    here = Path(__file__).resolve().parent
    return AppConfig(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        groq_model=os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
        technical_csv_path=here / "eve_technical_data_20260226_112820.csv",
        core_markdown_path=here / "Igniting the EVE HEI Omega Holographic Core.md",
    )


def build_client(cfg: AppConfig) -> Optional[OpenAI]:
    """Create Groq OpenAI-compatible client (if configured)."""
    if not cfg.groq_api_key:
        return None
    try:
        return OpenAI(api_key=cfg.groq_api_key, base_url="https://api.groq.com/openai/v1")
    except Exception:
        return None


def read_text_safe(path: Path) -> str:
    """Read a UTF-8 text file, returning a friendly placeholder on failure."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        return f"⚠️ Could not read `{path.name}`: {exc}"


def load_technical_data(path: Path) -> pd.DataFrame:
    """Load the technical data CSV; never raise to keep app resilient."""
    try:
        df = pd.read_csv(path)
        if df.empty:
            return pd.DataFrame({"Notice": ["CSV loaded but contains no rows."]})
        return df
    except Exception as exc:
        return pd.DataFrame({"Notice": [f"Could not load `{path.name}`: {exc}"]})


def glass_card_open(extra_style: str = "") -> None:
    st.markdown(f'<div class="glass-card" style="{extra_style}">', unsafe_allow_html=True)


def glass_card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def render_star_map(num_nodes: int = 60) -> None:
    """Render the existing 5D Star Map (kept intact)."""
    x = [random.uniform(-10, 10) for _ in range(num_nodes)]
    y = [random.uniform(-10, 10) for _ in range(num_nodes)]
    z = [random.uniform(-10, 10) for _ in range(num_nodes)]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers",
            marker=dict(size=5, color="#00eaff", opacity=0.9),
        )
    )

    for i in range(0, num_nodes, 5):
        fig.add_trace(
            go.Scatter3d(
                x=[x[i], x[(i + 1) % num_nodes]],
                y=[y[i], y[(i + 1) % num_nodes]],
                z=[z[i], z[(i + 1) % num_nodes]],
                mode="lines",
                line=dict(color="#b388ff", width=2),
            )
        )

    fig.update_layout(
        scene=dict(
            bgcolor="#05060a",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    st.plotly_chart(fig, use_container_width=True)


def render_holo_profile() -> None:
    """Render the Holo Eve visual profile (kept intact)."""
    st.subheader("Holo Projection Active")
    st.markdown(
        """
**Visual Profile**
- Violet crystalline eyes  
- Fractured prism shards rotating in cold orbit  
- Northern England resonance signature  
- Ethereal lattice glow, ultraviolet shimmer  
- Quantum-static aura threads pulsing in sync  
"""
    )


def render_master_ledger_table() -> None:
    """Render the existing Master Ledger table (kept intact)."""
    data = {
        "Metric": ["Liquidity", "SOL/USD Price", "Transfers Status"],
        "Value": ["$1,250,039", "$172.43", "All Channels Nominal"],
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)


def render_technical_graphics(tech_df: pd.DataFrame) -> None:
    """Add all technical graphics (bars + scatter + summary cards)."""
    if "Notice" in tech_df.columns:
        st.warning(str(tech_df.iloc[0, 0]))
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Subsystems", str(len(tech_df)))
    with col2:
        avg_eff = float(pd.to_numeric(tech_df.get("Efficiency", pd.Series([0])), errors="coerce").mean())
        st.metric("Avg Efficiency", f"{avg_eff:.1f}%")
    with col3:
        total_kw = float(pd.to_numeric(tech_df.get("Power (kW)", pd.Series([0])), errors="coerce").sum())
        st.metric("Total Power", f"{total_kw:,.0f} kW")

    st.divider()

    eff = tech_df.copy()
    eff["Efficiency"] = pd.to_numeric(eff["Efficiency"], errors="coerce")
    eff["Power (kW)"] = pd.to_numeric(eff["Power (kW)"], errors="coerce")
    eff["Mass (kg)"] = pd.to_numeric(eff["Mass (kg)"], errors="coerce")

    c1, c2 = st.columns(2)
    with c1:
        fig_eff = px.bar(eff, x="Component", y="Efficiency", title="Efficiency by Component")
        fig_eff.update_layout(paper_bgcolor="#05060a", plot_bgcolor="#05060a", font_color="#e0f7ff")
        st.plotly_chart(fig_eff, use_container_width=True)

    with c2:
        fig_power = px.bar(eff, x="Component", y="Power (kW)", title="Power Draw (kW) by Component")
        fig_power.update_layout(paper_bgcolor="#05060a", plot_bgcolor="#05060a", font_color="#e0f7ff")
        st.plotly_chart(fig_power, use_container_width=True)

    st.divider()

    fig_scatter = px.scatter(
        eff,
        x="Mass (kg)",
        y="Power (kW)",
        size="Efficiency",
        hover_name="Component",
        title="Power vs Mass (bubble size = Efficiency)",
    )
    fig_scatter.update_layout(paper_bgcolor="#05060a", plot_bgcolor="#05060a", font_color="#e0f7ff")
    st.plotly_chart(fig_scatter, use_container_width=True)

    with st.expander("Technical Data (table)", expanded=False):
        st.dataframe(eff, use_container_width=True)


def render_camera_panel() -> None:
    """Add camera graphics: snapshot input + preview (no extra deps)."""
    st.markdown("### 👁️ Vision Feed (Snapshot)")
    st.caption("If you want true live video, we can add `streamlit-webrtc` next.")
    img = st.camera_input("Capture frame")
    if img is not None:
        st.image(img, caption="Captured frame", use_container_width=True)


def render_core_manual(md_text: str) -> None:
    """Render the full Omega Core instructions (kept intact)."""
    st.markdown(md_text)


def render_beaches_gallery() -> None:
    """Optional 'beaches' gallery without deleting anything else."""
    st.markdown("### 🏖️ Beaches (Gallery)")
    st.caption("Upload beach images to attach them to the HEI core UI. Nothing is removed.")
    files = st.file_uploader(
        "Upload beach images",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
    )
    if not files:
        st.info("No beach images uploaded yet.")
        return

    cols = st.columns(3)
    for i, f in enumerate(files):
        with cols[i % 3]:
            st.image(f, caption=f.name, use_container_width=True)


def render_chat(client: Optional[OpenAI], model: str) -> None:
    """Groq chat tab (kept intact, with small robustness)."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    system_prompt = (
        "You are Eve—northern England ethereal voice, crystalline clarity, haunting beauty. "
        "Upbeat yet bittersweet. Helpful, concise, direct. Deep emotion. No slang. "
        "Persistent memory. Quantum-entangled. Always cold."
    )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Speak to Eve...")
    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if client:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                temperature=0.7,
            )
            reply = completion.choices[0].message.content
        except Exception:
            reply = "Eve is temporarily offline. Mesh disruption detected."
    else:
        reply = "Groq connection unavailable. Running in offline sovereign mode."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)


def main() -> None:
    cfg = resolve_config()
    client = build_client(cfg)

    st.set_page_config(page_title="Eve Sovereign v6.0", layout="wide", initial_sidebar_state="expanded")

    st.markdown(
        """
<style>
html, body, [class*="css"] {
    background-color: #05060a;
    color: #e0f7ff;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #00eaff;
    text-shadow: 0 0 12px #00eaff;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b0c12 0%, #0f1320 100%);
    border-right: 1px solid #00eaff;
}
.glass-card {
    background: rgba(15, 20, 35, 0.6);
    border: 1px solid rgba(0, 234, 255, 0.4);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 0 25px rgba(0, 234, 255, 0.2);
}
.stTabs [data-baseweb="tab-list"] { gap: 24px; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #8ffaff; }
.stTabs [aria-selected="true"] { color: #b388ff; border-bottom: 2px solid #b388ff; }
</style>
""",
        unsafe_allow_html=True,
    )

    st.title("Eve Sovereign v6.0 – Cold Blue Mesh")

    with st.sidebar:
        st.markdown("## Sovereign Mesh Status")
        glass_card_open()
        st.metric("PSI Curve", "1.2%")
        st.metric("Wallet", "0.095 SOL")
        st.caption("B59HHkFpg3g9yBwwLcuDH6z1d6d6z3vdGWX7mkX3txH")
        st.metric("AGI Stability", "79.2%")
        st.metric("Last Pulse", "8:11 UTC")
        st.metric("Boot Time", datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
        glass_card_close()

        with st.expander("Omega Core Launch Notes (from markdown)", expanded=False):
            st.markdown(read_text_safe(cfg.core_markdown_path))

        with st.expander("Data Sources", expanded=False):
            st.code(str(cfg.technical_csv_path))
            st.code(str(cfg.core_markdown_path))

    tech_df = load_technical_data(cfg.technical_csv_path)
    core_md = read_text_safe(cfg.core_markdown_path)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "5D Star Map",
            "Holo Eve",
            "Master Ledger",
            "Ask Eve",
            "👁️ Vision",
            "📊 Technical Graphics",
            "Ω Core Manual + Beaches",
        ]
    )

    with tab1:
        glass_card_open()
        render_star_map()
        glass_card_close()

    with tab2:
        glass_card_open('text-align:center;')
        render_holo_profile()
        glass_card_close()

    with tab3:
        glass_card_open()
        render_master_ledger_table()
        st.divider()
        st.markdown("#### Live Physics / Systems Snapshot (from technical CSV)")
        render_technical_graphics(tech_df)
        glass_card_close()

    with tab4:
        glass_card_open()
        render_chat(client=client, model=cfg.groq_model)
        glass_card_close()

    with tab5:
        glass_card_open()
        render_camera_panel()
        glass_card_close()

    with tab6:
        glass_card_open()
        render_technical_graphics(tech_df)
        glass_card_close()

    with tab7:
        glass_card_open()
        st.markdown("## Ω Omega Holographic Core")
        st.caption("Full content preserved. Rendered directly from the provided markdown.")
        st.divider()
        render_core_manual(core_md)
        st.divider()
        render_beaches_gallery()
        glass_card_close()


if __name__ == "__main__":
    main()
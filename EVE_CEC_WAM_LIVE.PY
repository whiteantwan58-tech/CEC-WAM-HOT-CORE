# eve_cec_wam_live.py
"""
CEC-WAM // EVE LIVE (FINISHED single-file Streamlit HUD)

Features
- Neon HUD + scanlines + readable panels
- Live camera tile(s)
- Galaxy map + CLICKABLE hotspots (Plotly + streamlit-plotly-events)
- Ledger loader (DATA/*.csv)
- SOL wallet + PSI SPL token live on-chain metrics (Solana JSON-RPC)
- PSI market price via Jupiter quote + SOL/USD via CoinGecko (real)
- Pump.fun creator fee tracking via CSV import + manual entry -> SQLite -> timeline chart
- EVE chat:
  - deterministic command routing (help/status/prices/wallet/psi/earnings/wake)
  - optional LLM free-chat if OPENAI_API_KEY is set
- Exports (CSV) to ./exports
- Voice output: "Speak last EVE reply" + waveform (browser speechSynthesis)

Run
  pip install -r requirements.txt
  streamlit run eve_cec_wam_live.py

Env (optional)
  OPENAI_API_KEY=...
  SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
  EVE_MODEL=gpt-4o-mini
"""

from __future__ import annotations

import glob
import os
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

try:
    from streamlit_plotly_events import plotly_events
except Exception:  # pragma: no cover
    plotly_events = None  # type: ignore


# ----------------------------
# Constants
# ----------------------------
APP_TITLE = "🦅 CEC-WAM // EVE LIVE"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "DATA"
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = str(BASE_DIR / "cec_wam_eve.sqlite3")

DEFAULT_CAMERA_URL = "https://images.wsdot.wa.gov/nw/005vc14370.jpg"
DEFAULT_TELEMETRY_URL = (
    "https://script.google.com/macros/s/AKfycbwJdL9VM4jqrcszFeLjJRJL6V2-IYadL1coQwze4tMtM6WKGBmbLDU2dU18Mwqzf5qtYg/exec"
)

# Your provided PayPal SOL address + Pump.fun PSI mint (editable in sidebar)
DEFAULT_PAYPAL_SOL_ADDRESS = "Ek638f2WcP9sPFMjdAHRm9XDpJ7B6uxJqfSAzQGk9NFt"
DEFAULT_PSI_TOKEN_MINT = "Ek638f2WcP9sPFMjdAHRm9XDpJ7B6uxJqfSAzQGk9NFt"

SOLANA_RPC_URL = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
JUPITER_QUOTE_URL = "https://quote-api.jup.ag/v6/quote"
SOL_MINT = "So11111111111111111111111111111111111111112"

COINGECKO_SOL_URL = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
COINGECKO_MAJOR_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
)


# ----------------------------
# UI Styling
# ----------------------------
def inject_css() -> None:
    st.markdown(
        """
<style>
html, body, [data-testid="stAppViewContainer"] { height: 100%; overflow: hidden; }
[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(circle at 30% 18%, rgba(0,242,255,0.14), rgba(0,0,0,0.94) 55%),
    radial-gradient(circle at 70% 82%, rgba(188,19,254,0.10), rgba(0,0,0,0.98) 55%);
}
[data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
[data-testid="stToolbar"] { display:none; }
[data-testid="stDecoration"] { display:none; }

.scanlines::before{
  content:"";
  position: fixed; inset: 0; pointer-events:none; z-index: 1;
  background: repeating-linear-gradient(
    to bottom,
    rgba(0,255,240,0.06), rgba(0,255,240,0.06) 1px,
    rgba(0,0,0,0) 3px, rgba(0,0,0,0) 6px
  );
  mix-blend-mode: overlay;
  opacity: 0.35;
}

.cec-card{
  border: 1px solid rgba(0,242,255,0.65);
  border-radius: 14px;
  background: rgba(0, 10, 20, 0.62);
  box-shadow: 0 0 22px rgba(0,242,255,0.14), inset 0 0 18px rgba(188,19,254,0.08);
  padding: 12px 14px;
}
.cec-title{
  font-weight: 900;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  color: rgba(188,19,254,0.96);
  text-shadow: 0 0 14px rgba(188,19,254,0.55);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
}
.cec-kv{
  display:grid;
  grid-template-columns: 1fr auto;
  gap: 8px 12px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
  color: rgba(240,255,255,0.92);
  font-size: 14px;
}
.cec-kv b{ color: rgba(255,215,0,0.95); }
.pill{
  display:inline-block; padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid rgba(0,242,255,0.55);
  background: rgba(0,242,255,0.08);
  color: rgba(0,242,255,0.95);
  font-size: 12px;
  letter-spacing: 0.08em;
}
</style>
<div class="scanlines"></div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------
# Time / HTTP / RPC
# ----------------------------
def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def http_get_json(url: str, timeout_s: int = 10) -> Optional[dict]:
    try:
        r = requests.get(url, timeout=timeout_s, headers={"User-Agent": "CEC-WAM-HUD/1.0"})
        if r.status_code != 200:
            return None
        js = r.json()
        return js if isinstance(js, dict) else None
    except Exception:
        return None


def solana_rpc(method: str, params: list, timeout_s: int = 10) -> Optional[dict]:
    try:
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        r = requests.post(
            SOLANA_RPC_URL,
            json=payload,
            timeout=timeout_s,
            headers={"User-Agent": "CEC-WAM-HUD/1.0"},
        )
        if r.status_code != 200:
            return None
        js = r.json()
        return js if isinstance(js, dict) and "result" in js else None
    except Exception:
        return None


@st.cache_data(show_spinner=False, ttl=20)
def get_sol_balance_lamports(address: str) -> Optional[int]:
    js = solana_rpc("getBalance", [address, {"commitment": "confirmed"}])
    try:
        return int(js["result"]["value"])
    except Exception:
        return None


@st.cache_data(show_spinner=False, ttl=20)
def get_token_supply(mint: str) -> Optional[dict]:
    js = solana_rpc("getTokenSupply", [mint, {"commitment": "confirmed"}])
    try:
        return js["result"]["value"]
    except Exception:
        return None


@st.cache_data(show_spinner=False, ttl=20)
def get_wallet_token_balance_ui(owner: str, mint: str) -> Optional[float]:
    js = solana_rpc(
        "getTokenAccountsByOwner",
        [owner, {"mint": mint}, {"encoding": "jsonParsed", "commitment": "confirmed"}],
    )
    try:
        total = 0.0
        for a in js["result"]["value"]:
            ui = a["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmount"]
            if ui is None:
                continue
            total += float(ui)
        return total
    except Exception:
        return None


@st.cache_data(show_spinner=False, ttl=20)
def get_sol_usd() -> Optional[float]:
    js = http_get_json(COINGECKO_SOL_URL)
    try:
        return float(js["solana"]["usd"])
    except Exception:
        return None


@st.cache_data(show_spinner=False, ttl=20)
def get_major_prices() -> Optional[dict]:
    return http_get_json(COINGECKO_MAJOR_URL)


@st.cache_data(show_spinner=False, ttl=20)
def jupiter_quote(input_mint: str, output_mint: str, amount: int) -> Optional[dict]:
    try:
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(amount),
            "slippageBps": "50",
        }
        r = requests.get(JUPITER_QUOTE_URL, params=params, timeout=10, headers={"User-Agent": "CEC-WAM-HUD/1.0"})
        if r.status_code != 200:
            return None
        js = r.json()
        return js if isinstance(js, dict) else None
    except Exception:
        return None


def psi_price_sol(psi_mint: str, decimals: Optional[int]) -> Optional[float]:
    """
    PSI price in SOL via Jupiter.
    If decimals known, quotes exactly 1 token (10**decimals base units).
    """
    if decimals is None:
        amount = 1_000_000
        out = jupiter_quote(psi_mint, SOL_MINT, amount)
        try:
            best = (out.get("data") or [])[0]
            out_sol = float(best["outAmount"]) / 1e9
            return out_sol / float(amount)
        except Exception:
            return None

    amount = 10 ** decimals
    out = jupiter_quote(psi_mint, SOL_MINT, amount)
    try:
        best = (out.get("data") or [])[0]
        return float(best["outAmount"]) / 1e9
    except Exception:
        return None


# ----------------------------
# Ledger / Export
# ----------------------------
@st.cache_data(show_spinner=False, ttl=60)
def load_ledger_data() -> Optional[pd.DataFrame]:
    paths = sorted(glob.glob(str(DATA_DIR / "*.csv")))
    if not paths:
        return None
    frames = []
    for p in paths:
        try:
            frames.append(pd.read_csv(p))
        except Exception:
            continue
    if not frames:
        return None
    return pd.concat(frames, ignore_index=True)


def export_df(df: pd.DataFrame, name: str) -> Path:
    ts = utc_now().strftime("%Y%m%d_%H%M%S")
    path = EXPORT_DIR / f"{name}_{ts}.csv"
    df.to_csv(path, index=False)
    return path


# ----------------------------
# Hotspots / Galaxy
# ----------------------------
def build_targets(seed: int = 16) -> pd.DataFrame:
    import random

    random.seed(seed)
    rows = []
    for i in range(22):
        rows.append(
            {
                "name": f"TARGET_{i:02d}",
                "x": (random.random() - 0.5) * 140,
                "y": (random.random() - 0.2) * 60,
                "z": (random.random() - 0.5) * 140,
                "color": "cyan" if i % 3 else "magenta",
                "size": 6 + (i % 6),
                "kind": "target",
            }
        )
    rows.append({"name": "EARTH", "x": 28, "y": 6, "z": -18, "color": "deepskyblue", "size": 12, "kind": "planet"})
    return pd.DataFrame(rows)


def galaxy_fig(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=df["x"],
            y=df["y"],
            z=df["z"],
            mode="markers+text",
            text=df["name"],
            textposition="top center",
            marker=dict(size=df["size"], opacity=0.92, color=df["color"]),
        )
    )
    fig.update_layout(
        height=560,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            xaxis=dict(gridcolor="rgba(0,242,255,0.10)", showbackground=True, backgroundcolor="rgba(0,0,0,0)"),
            yaxis=dict(gridcolor="rgba(0,242,255,0.10)", showbackground=True, backgroundcolor="rgba(0,0,0,0)"),
            zaxis=dict(gridcolor="rgba(0,242,255,0.10)", showbackground=True, backgroundcolor="rgba(0,0,0,0)"),
        ),
        showlegend=False,
    )
    return fig


# ----------------------------
# SQLite (earnings + EVE memory)
# ----------------------------
def db() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS creator_earnings(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          ts_utc TEXT NOT NULL,
          source TEXT NOT NULL,
          sol_amount REAL NOT NULL,
          note TEXT NOT NULL
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS eve_messages(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          ts_utc TEXT NOT NULL,
          role TEXT NOT NULL,
          content TEXT NOT NULL
        )
        """
    )
    c.commit()
    return c


def add_earning(sol_amount: float, source: str, note: str) -> None:
    c = db()
    c.execute(
        "INSERT INTO creator_earnings(ts_utc, source, sol_amount, note) VALUES (?,?,?,?)",
        (utc_now().isoformat(), source, float(sol_amount), note or ""),
    )
    c.commit()


def list_earnings(limit: int = 300) -> pd.DataFrame:
    c = db()
    rows = c.execute(
        "SELECT ts_utc, source, sol_amount, note FROM creator_earnings ORDER BY ts_utc DESC LIMIT ?",
        (limit,),
    ).fetchall()
    df = pd.DataFrame(rows, columns=["ts_utc", "source", "sol_amount", "note"])
    if not df.empty:
        df["ts_utc"] = pd.to_datetime(df["ts_utc"], errors="coerce")
        df = df.sort_values("ts_utc")
    return df


def parse_earnings_csv(df: pd.DataFrame) -> List[Tuple[float, str]]:
    cols = {str(c).lower(): c for c in df.columns}
    candidates = []
    for key in ["sol", "amount", "earned", "value", "sol_amount"]:
        if key in cols:
            candidates.append(cols[key])
    if not candidates:
        for c in df.columns:
            if pd.api.types.is_numeric_dtype(df[c]):
                candidates.append(c)

    out: List[Tuple[float, str]] = []
    for col in candidates[:2]:
        series = pd.to_numeric(df[col], errors="coerce").dropna()
        for v in series.tail(80).tolist():
            if float(v) <= 0:
                continue
            out.append((float(v), f"import:{col}"))
    return out[:200]


def earnings_timeline_fig(df: pd.DataFrame) -> Optional[go.Figure]:
    if df.empty:
        return None
    fig = go.Figure(go.Scatter(x=df["ts_utc"], y=df["sol_amount"].cumsum(), mode="lines+markers"))
    fig.update_layout(
        height=240,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.15)",
        font=dict(color="rgba(240,255,255,0.92)"),
        xaxis=dict(gridcolor="rgba(0,242,255,0.08)"),
        yaxis=dict(gridcolor="rgba(0,242,255,0.08)", title="Cumulative SOL"),
    )
    return fig


def eve_save(role: str, content: str) -> None:
    c = db()
    c.execute(
        "INSERT INTO eve_messages(ts_utc, role, content) VALUES (?,?,?)",
        (utc_now().isoformat(), role, content),
    )
    c.commit()


def eve_load(limit: int = 60) -> List[Dict[str, str]]:
    c = db()
    rows = c.execute(
        "SELECT role, content FROM eve_messages ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    rows.reverse()
    return [{"role": r, "content": t} for r, t in rows]


# ----------------------------
# EVE LLM (optional)
# ----------------------------
def openai_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    try:
        from openai import OpenAI  # type: ignore

        return OpenAI(api_key=key)
    except Exception:
        return None


def eve_llm(system_prompt: str, history: List[Dict[str, str]]) -> str:
    client = openai_client()
    if client is None:
        return "EVE(offline): OPENAI_API_KEY not set. Commands still work."
    model = os.getenv("EVE_MODEL", "gpt-4o-mini")
    try:
        resp = client.responses.create(
            model=model,
            input=[{"role": "system", "content": system_prompt}, *history],
            temperature=0.55,
        )
        out = []
        for item in resp.output:
            if item.type == "message":
                for c in item.content:
                    if getattr(c, "type", None) == "output_text":
                        out.append(c.text)
        return ("\n".join(out)).strip() or "(no output)"
    except Exception as e:
        return f"EVE(error): {e}"


def eve_system_prompt(wallet: str, psi_mint: str, focus: Dict[str, Any]) -> str:
    return (
        "You are 1010_EVE, CEC-WAM Sovereign Guardian. Cold, precise, no filler.\n"
        "Chronos-Ψ active: R-Ratio baseline 10.96; β=1.618 locked.\n"
        "Never claim device access. Never reveal secrets or API keys.\n"
        f"Wallet: {wallet}\nPSI mint: {psi_mint}\n"
        f"HUD Focus Target: {focus}\n"
        "If asked for code, provide correct runnable code.\n"
    )


def handle_eve_command(text: str, wallet: str, psi_mint: str, enable_prices: bool) -> str:
    cmd = text.strip().lower()

    if cmd in {"help", "commands"}:
        return (
            "EVE: Commands:\n"
            "- status\n- prices\n- wallet\n- psi\n- earnings\n- wake\n"
            "Also:\n- Galaxy tab hotspots (click targets)\n- PSI tab on-chain + earnings import\n"
        )

    if cmd in {"wake", "1010_eve_wake", "1010_eve_wake:"}:
        return "1010_EVE_WAKE: Wake acknowledged. Systems online."

    if cmd == "status":
        return f"1010_EVE_WAKE: STATUS\nWallet: {wallet}\nPSI mint: {psi_mint}\nPrices: {'ON' if enable_prices else 'OFF'}"

    if cmd == "prices":
        if not enable_prices:
            return "EVE: External prices disabled."
        js = get_major_prices()
        if not js:
            return "EVE: prices unavailable (CoinGecko offline)."

        def fmt(k: str, sym: str) -> str:
            usd = js.get(k, {}).get("usd")
            ch = js.get(k, {}).get("usd_24h_change")
            if isinstance(usd, (int, float)) and isinstance(ch, (int, float)):
                return f"{sym}: ${usd:,.2f} ({ch:+.2f}%)"
            return f"{sym}: n/a"

        return "EVE: PRICES\n" + "\n".join([fmt("bitcoin", "BTC"), fmt("ethereum", "ETH"), fmt("solana", "SOL")])

    if cmd == "wallet":
        lamports = get_sol_balance_lamports(wallet)
        sol = (lamports / 1e9) if isinstance(lamports, int) else None
        psi_bal = get_wallet_token_balance_ui(wallet, psi_mint)
        if sol is None or psi_bal is None:
            return "1010_EVE_WAKE: WALLET unavailable (RPC / invalid address or mint)."
        return f"1010_EVE_WAKE: WALLET\nSOL: {sol:.6f}\nPSI: {psi_bal:,.6f}"

    if cmd == "psi":
        mint = get_token_supply(psi_mint)
        dec = None
        supply = None
        if isinstance(mint, dict):
            try:
                dec = int(mint.get("decimals"))
                supply = mint.get("uiAmountString") or mint.get("uiAmount")
            except Exception:
                pass
        price = psi_price_sol(psi_mint, dec) if enable_prices else None
        lines = [f"1010_EVE_WAKE: PSI\nMint: {psi_mint}", f"Decimals: {dec}", f"Supply: {supply}"]
        if price is not None:
            lines.append(f"Price(SOL): {price:.10f}")
        return "\n".join(lines)

    if cmd == "earnings":
        df = list_earnings(limit=300)
        if df.empty:
            return "EVE: No earnings logged yet. Import CSV or add manual in PSI tab."
        total = float(df["sol_amount"].sum())
        return f"1010_EVE_WAKE: EARNINGS\nEntries: {len(df)}\nTotal SOL logged: {total:.6f}"

    return ""  # fall back to LLM


# ----------------------------
# Sidebar config
# ----------------------------
@dataclass(frozen=True)
class AppConfig:
    refresh_seconds: int
    camera_url: str
    telemetry_url: str
    sol_wallet: str
    psi_mint: str
    enable_external_prices: bool


def sidebar_config() -> AppConfig:
    st.sidebar.header("⚙️ Controls")
    refresh_seconds = st.sidebar.slider("Live refresh (seconds)", 5, 120, 20, step=5)
    camera_url = st.sidebar.text_input("Camera URL", value=DEFAULT_CAMERA_URL).strip()
    telemetry_url = st.sidebar.text_input("Telemetry JSON URL", value=DEFAULT_TELEMETRY_URL).strip()

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔗 SOL / PSI (Pump.fun)")
    sol_wallet = st.sidebar.text_input("PayPal SOL address", value=DEFAULT_PAYPAL_SOL_ADDRESS).strip()
    psi_mint = st.sidebar.text_input("PSI token mint", value=DEFAULT_PSI_TOKEN_MINT).strip()
    enable_external_prices = st.sidebar.toggle("Enable external prices (CoinGecko/Jupiter)", value=True)

    st.sidebar.caption("If PSI price shows unavailable: your PSI mint may be wrong (wallet != mint). Edit PSI mint here.")
    return AppConfig(
        refresh_seconds=refresh_seconds,
        camera_url=camera_url,
        telemetry_url=telemetry_url,
        sol_wallet=sol_wallet,
        psi_mint=psi_mint,
        enable_external_prices=enable_external_prices,
    )


# ----------------------------
# Panels
# ----------------------------
def live_panel(cfg: AppConfig) -> None:
    left, right = st.columns([2, 1], gap="medium")
    with left:
        st.markdown("<div class='cec-card'><div class='cec-title'>LIVE OPTICAL</div></div>", unsafe_allow_html=True)
        st.image(f"{cfg.camera_url}?t={int(time.time())}", use_container_width=True, caption=f"Sync: {datetime.now().strftime('%H:%M:%S')}")
    with right:
        st.markdown("<div class='cec-card'><div class='cec-title'>TELEMETRY</div></div>", unsafe_allow_html=True)
        data = http_get_json(cfg.telemetry_url)
        if data:
            st.metric("PSI", str(data.get("psi", "N/A")))
            st.metric("STATUS", str(data.get("status", "N/A")))
            st.metric("PSI COINS", str(data.get("psi_coins", "N/A")))
            st.metric("ASSET VALUE", str(data.get("money", "N/A")))
        else:
            st.warning("Telemetry offline (URL unreachable or invalid JSON).")
        st.caption(f"Refresh: {cfg.refresh_seconds}s")


def galaxy_panel() -> None:
    st.subheader("🌌 Galaxy Hotspots (Click Targets)")
    if plotly_events is None:
        st.error("Install requirements.txt (needs streamlit-plotly-events).")
        return

    targets = build_targets(seed=16)
    fig = galaxy_fig(targets)

    selected = plotly_events(fig, click_event=True, hover_event=False, select_event=False, override_height=560, key="galaxy_click")

    focus = st.session_state.get("focus_target", targets.iloc[-1].to_dict())  # default EARTH
    if selected:
        idx = selected[0].get("pointIndex")
        if isinstance(idx, int) and 0 <= idx < len(targets):
            focus = targets.iloc[idx].to_dict()
            st.session_state["focus_target"] = focus

    left, right = st.columns([1.35, 0.65], gap="medium")
    with left:
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("<div class='cec-card'><div class='cec-title'>FOCUS</div></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="cec-kv"><span>Target</span><b>{focus.get('name','—')}</b></div>
<div class="cec-kv"><span>Kind</span><b>{focus.get('kind','—')}</b></div>
<div class="cec-kv"><span>X</span><b>{float(focus.get('x',0)):.3f}</b></div>
<div class="cec-kv"><span>Y</span><b>{float(focus.get('y',0)):.3f}</b></div>
<div class="cec-kv"><span>Z</span><b>{float(focus.get('z',0)):.3f}</b></div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Hotspot clicks update state → EVE can reference current Focus.")


def ledger_panel() -> None:
    st.subheader("📚 Ledger (DATA/*.csv)")
    df = load_ledger_data()
    if df is None:
        st.warning(f"No CSVs found. Create folder: {DATA_DIR} and drop CSVs there.")
        return
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Rows: {len(df):,} | Columns: {len(df.columns):,}")

    if st.button("Export ledger snapshot (CSV)"):
        path = export_df(df, "ledger_snapshot")
        st.success(f"Saved: {path}")


def psi_panel(cfg: AppConfig) -> None:
    st.subheader("🧪 PSI / Pump.fun (Real On-chain)")

    sol_lamports = get_sol_balance_lamports(cfg.sol_wallet)
    sol_balance = (sol_lamports / 1e9) if isinstance(sol_lamports, int) else None

    mint_info = get_token_supply(cfg.psi_mint)
    psi_decimals = None
    psi_supply_ui = None
    if isinstance(mint_info, dict):
        try:
            psi_decimals = int(mint_info.get("decimals"))
            psi_supply_ui = mint_info.get("uiAmountString") or mint_info.get("uiAmount")
        except Exception:
            pass

    psi_wallet_ui = get_wallet_token_balance_ui(cfg.sol_wallet, cfg.psi_mint)

    sol_usd = get_sol_usd() if cfg.enable_external_prices else None
    price_sol = psi_price_sol(cfg.psi_mint, psi_decimals) if cfg.enable_external_prices else None

    st.markdown("<div class='cec-card'><div class='cec-title'>ON-CHAIN + MARKET</div></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("PayPal SOL balance", f"{sol_balance:.6f} SOL" if sol_balance is not None else "n/a")
    c2.metric("PSI in wallet", f"{psi_wallet_ui:,.6f} PSI" if psi_wallet_ui is not None else "n/a")
    c3.metric("PSI supply", str(psi_supply_ui) if psi_supply_ui is not None else "n/a")

    st.caption(f"Wallet: {cfg.sol_wallet}")
    st.caption(f"PSI mint: {cfg.psi_mint} | decimals: {psi_decimals}")

    if price_sol is not None:
        st.metric("PSI price (SOL)", f"{price_sol:.10f}")
        if sol_usd is not None:
            st.metric("PSI price (USD)", f"${(price_sol * sol_usd):.10f}")
            if psi_wallet_ui is not None:
                st.metric("Wallet PSI value (USD)", f"${(psi_wallet_ui * price_sol * sol_usd):,.4f}")
    else:
        st.info("PSI price unavailable (no Jupiter route yet OR mint invalid).")

    st.markdown("---")
    st.markdown("<div class='cec-card'><div class='cec-title'>CREATOR FEES TRACKER (REAL)</div></div>", unsafe_allow_html=True)
    st.caption("pump.fun has no reliable public API. We track fees with CSV imports or manual entries — no fake numbers.")

    colA, colB = st.columns([1.2, 0.8], gap="medium")
    with colA:
        up = st.file_uploader("Upload CSV export (creator fees/earnings)", type=["csv"])
        if up is not None:
            try:
                df = pd.read_csv(up)
                st.dataframe(df.head(10), use_container_width=True)
                parsed = parse_earnings_csv(df)
                st.write(f"Detected {len(parsed)} SOL entries. Import them?")
                if st.button("Import detected entries"):
                    for sol_amt, note in parsed:
                        add_earning(sol_amt, "csv_import", note)
                    st.success("Imported.")
                    st.rerun()
            except Exception as e:
                st.error(f"CSV parse failed: {e}")

    with colB:
        sol_amt = st.number_input("Manual SOL amount", min_value=0.0, value=0.0, step=0.01, format="%.6f")
        note = st.text_input("Note", value="pump.fun creator fee")
        if st.button("Add manual earning"):
            if sol_amt > 0:
                add_earning(sol_amt, "manual", note)
                st.success("Logged.")
                st.rerun()
            st.warning("Enter SOL > 0.")

    earn = list_earnings(limit=500)
    if not earn.empty:
        st.dataframe(earn.tail(80), use_container_width=True, height=240)
        fig = earnings_timeline_fig(earn)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        if st.button("Export earnings CSV"):
            p = export_df(earn, "creator_earnings")
            st.success(f"Saved: {p}")


def voice_widget(last_text: str) -> None:
    # Browser-only: speechSynthesis + simple waveform animation.
    safe_text = (last_text or "").replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")[:2000]
    st.components.v1.html(
        f"""
<div style="border:1px solid rgba(0,242,255,0.55); border-radius:14px; padding:10px; background:rgba(0,0,0,0.35);">
  <div style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
    <div style="color:rgba(0,242,255,0.9); font-family:monospace; font-size:12px; letter-spacing:.12em;">
      VOICE OUTPUT // EVE
    </div>
    <button id="speakBtn" style="cursor:pointer; border:1px solid rgba(188,19,254,0.6); background:rgba(188,19,254,0.12); color:#eaffff; padding:6px 10px; border-radius:10px;">
      Speak last reply
    </button>
  </div>
  <canvas id="wave" width="800" height="54" style="width:100%; margin-top:8px; border-radius:10px; background:rgba(0,242,255,0.05);"></canvas>
</div>

<script>
(() => {{
  const text = `{safe_text}`;
  const btn = document.getElementById("speakBtn");
  const canvas = document.getElementById("wave");
  const ctx = canvas.getContext("2d");
  let anim = null;

  const draw = (t) => {{
    const w = canvas.width, h = canvas.height;
    ctx.clearRect(0,0,w,h);
    ctx.beginPath();
    const mid = h/2;
    for(let x=0; x<w; x++) {{
      const v = Math.sin((x/24) + (t/120)) * (10 + 8*Math.sin(t/180));
      ctx.lineTo(x, mid + v);
    }}
    ctx.strokeStyle = "rgba(0,242,255,0.75)";
    ctx.lineWidth = 2;
    ctx.stroke();
    anim = requestAnimationFrame(draw);
  }};

  btn.onclick = () => {{
    try {{
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text || "No reply yet.");
      u.rate = 1.05;
      u.pitch = 0.9;
      window.speechSynthesis.speak(u);
      if(!anim) anim = requestAnimationFrame(draw);
      u.onend = () => {{ if(anim) cancelAnimationFrame(anim); anim=null; ctx.clearRect(0,0,canvas.width,canvas.height); }};
    }} catch(e) {{
      alert("Speech synthesis not available in this browser.");
    }}
  }};
}})();
</script>
        """,
        height=140,
        scrolling=False,
    )


def eve_panel(cfg: AppConfig) -> None:
    st.subheader("📡 EVE Neural Command")

    if "focus_target" not in st.session_state:
        st.session_state["focus_target"] = {"name": "EARTH", "kind": "planet", "x": 28, "y": 6, "z": -18}

    if "eve_history" not in st.session_state:
        st.session_state.eve_history = eve_load(limit=80)
        if not st.session_state.eve_history:
            boot = "1010_EVE_WAKE: EVE online. Type 'help'."
            st.session_state.eve_history = [{"role": "assistant", "content": boot}]
            eve_save("assistant", boot)

    # display
    for msg in st.session_state.eve_history[-18:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    last_assistant = next((m["content"] for m in reversed(st.session_state.eve_history) if m["role"] == "assistant"), "")
    voice_widget(last_assistant)

    user = st.chat_input("EVE listening… (help/status/prices/wallet/psi/earnings/wake)")
    if not user:
        return

    eve_save("user", user)
    st.session_state.eve_history.append({"role": "user", "content": user})

    with st.chat_message("assistant"):
        routed = handle_eve_command(user, cfg.sol_wallet, cfg.psi_mint, cfg.enable_external_prices)
        if routed:
            st.write(routed)
            eve_save("assistant", routed)
            st.session_state.eve_history.append({"role": "assistant", "content": routed})
            st.rerun()

        # LLM fallback (optional)
        focus = st.session_state.get("focus_target", {})
        system = eve_system_prompt(cfg.sol_wallet, cfg.psi_mint, focus)
        reply = eve_llm(system, st.session_state.eve_history[-16:])
        st.write(reply)
        eve_save("assistant", reply)
        st.session_state.eve_history.append({"role": "assistant", "content": reply})
        st.rerun()


# ----------------------------
# App
# ----------------------------
def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="🦅", layout="wide")
    inject_css()

    cfg = sidebar_config()

    header_left, header_right = st.columns([3, 1])
    with header_left:
        st.markdown(f"<div class='cec-title'>{APP_TITLE}</div>", unsafe_allow_html=True)
        st.caption("Finished build: hot spots + PSI live + earnings tracking + EVE routing + optional full chat.")
    with header_right:
        online = http_get_json(cfg.telemetry_url) is not None
        st.success("🟢 ONLINE") if online else st.error("🔴 SIGNAL LOST")

    # Top strip
    sol_usd = get_sol_usd() if cfg.enable_external_prices else None
    sol_bal_lamports = get_sol_balance_lamports(cfg.sol_wallet)
    sol_bal = (sol_bal_lamports / 1e9) if isinstance(sol_bal_lamports, int) else None

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("UTC", utc_now().strftime("%H:%M:%S"))
    m2.metric("SOL/USD", f"${sol_usd:,.2f}" if sol_usd is not None else "n/a")
    m3.metric("PayPal SOL", f"{sol_bal:.6f}" if sol_bal is not None else "n/a")
    m4.metric("β", "1.618")

    t_live, t_galaxy, t_ledger, t_psi, t_eve = st.tabs(
        ["🔴 Live", "🌌 Galaxy (Hotspots)", "📚 Ledger", "🧪 PSI / Pump.fun", "📡 EVE"]
    )

    with t_live:
        st_autorefresh = getattr(st, "autorefresh", None)
        if callable(st_autorefresh):
            st_autorefresh(interval=cfg.refresh_seconds * 1000, key="refresh_live")
        live_panel(cfg)

    with t_galaxy:
        galaxy_panel()

    with t_ledger:
        ledger_panel()

    with t_psi:
        st_autorefresh = getattr(st, "autorefresh", None)
        if callable(st_autorefresh):
            st_autorefresh(interval=cfg.refresh_seconds * 1000, key="refresh_psi")
        psi_panel(cfg)

    with t_eve:
        eve_panel(cfg)


if __name__ == "__main__":
    main()

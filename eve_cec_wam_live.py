# eve_cec_wam_live.py
"""
CEC-WAM // EVE LIVE (REAL Streamlit HUD)

Includes:
- Neon HUD CSS + scanlines
- Live camera
- Galaxy + clickable hotspots (requires streamlit-plotly-events)
- Real SOL + SPL (PSI Pump.fun mint) on-chain tracking (Solana RPC)
- Real PSI "bonding curve style" chart (Jupiter quotes sampled at multiple sizes)
- Real transfer tracker (inbound SOL + inbound PSI to PayPal receiving wallet)
- EVE chat:
  - deterministic command routing
  - Groq LLM (OpenAI-compatible) if GROQ_API_KEY is set
  - optional OpenAI fallback if OPENAI_API_KEY is set

Run:
  py -m pip install streamlit pandas requests plotly openai streamlit-plotly-events
  py -m streamlit run .\eve_cec_wam_live.py --server.port 8502

Env (recommended):
  setx GROQ_API_KEY "YOUR_GROQ_KEY"
  setx GROQ_MODEL "llama-3.3-70b-versatile"
  setx SOLANA_RPC_URL "https://api.mainnet-beta.solana.com"
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
except Exception:
    plotly_events = None  # type: ignore


# ----------------------------
# Constants (YOUR REAL DEFAULTS)
# ----------------------------
APP_TITLE = "CEC-WAM // EVE LIVE"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "DATA"
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = str(BASE_DIR / "cec_wam_eve.sqlite3")

DEFAULT_CAMERA_URL = "https://images.wsdot.wa.gov/nw/005vc14370.jpg"
DEFAULT_TELEMETRY_URL = (
    "https://script.google.com/macros/s/AKfycbwJdL9VM4jqrcszFeLjJRJL6V2-IYadL1coQwze4tMtM6WKGBmbLDU2dU18Mwqzf5qtYg/exec"
)

# PayPal receiving wallet (track inbound SOL + inbound PSI)
DEFAULT_PAYPAL_RECEIVE_WALLET = "HpME8sCYRbSuMVfxMQu8M5a7NBKdi29c9nvwJxjxkX4E"
# Optional bridge/source wallet you pasted
DEFAULT_BRIDGE_SOURCE_WALLET = "b59HHkFpg3g9yBwwLcuDH6z1d6d6z3vdGWX7mkX3txH"

# PSI Pump.fun mint you gave (SPL Mint)
DEFAULT_PSI_TOKEN_MINT = "7Avu2LscLpCNNDR8szDowyck3MCBecpCf1wHyjU3pump"

SOLANA_RPC_URL = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
JUPITER_QUOTE_URL = "https://quote-api.jup.ag/v6/quote"
SOL_MINT = "So11111111111111111111111111111111111111112"
COINGECKO_SOL_URL = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"


# ----------------------------
# Streamlit fragment compat
# ----------------------------
def _fragment_decorator():
    if hasattr(st, "fragment"):
        return st.fragment
    if hasattr(st, "experimental_fragment"):
        return st.experimental_fragment  # type: ignore[attr-defined]

    def _noop(*_args, **_kwargs):
        def _wrap(fn):
            return fn

        return _wrap

    return _noop


fragment = _fragment_decorator()


# ----------------------------
# CSS
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
</style>
<div class="scanlines"></div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------
# Time / HTTP / Solana RPC
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


def solana_rpc(method: str, params: list, timeout_s: int = 20) -> Optional[dict]:
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


@st.cache_data(show_spinner=False, ttl=60)
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


@st.cache_data(show_spinner=False, ttl=30)
def get_sol_usd() -> Optional[float]:
    js = http_get_json(COINGECKO_SOL_URL)
    try:
        return float(js["solana"]["usd"])
    except Exception:
        return None


@st.cache_data(show_spinner=False, ttl=20)
def jupiter_quote(input_mint: str, output_mint: str, amount: int) -> Optional[dict]:
    try:
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(amount),
            "slippageBps": "50",
        }
        r = requests.get(JUPITER_QUOTE_URL, params=params, timeout=12, headers={"User-Agent": "CEC-WAM-HUD/1.0"})
        if r.status_code != 200:
            return None
        js = r.json()
        return js if isinstance(js, dict) else None
    except Exception:
        return None


def token_price_sol_from_quote(token_mint: str, token_decimals: int, token_amount_ui: float) -> Optional[float]:
    """
    Jupiter quote for token_amount_ui -> SOL.
    Returns price per 1 token in SOL for this size (spot-ish).
    """
    if token_amount_ui <= 0:
        return None
    base_amount = int(token_amount_ui * (10 ** token_decimals))
    out = jupiter_quote(token_mint, SOL_MINT, base_amount)
    try:
        best = (out.get("data") or [])[0]
        out_sol = float(best["outAmount"]) / 1e9
        return out_sol / float(token_amount_ui)
    except Exception:
        return None


@st.cache_data(show_spinner=False, ttl=30)
def bonding_curve_samples(token_mint: str, token_decimals: int) -> pd.DataFrame:
    """
    Approximates a 'bonding curve' by sampling Jupiter quotes at multiple trade sizes.
    This is real market route pricing (not a fake curve).
    """
    sizes = [1, 5, 10, 25, 50, 100, 250, 500, 1000]
    rows = []
    for s in sizes:
        p = token_price_sol_from_quote(token_mint, token_decimals, float(s))
        rows.append({"size_tokens": s, "price_sol_per_token": p})
        time.sleep(0.2)  # avoid hammering
    df = pd.DataFrame(rows)
    return df


# ----------------------------
# Transfer tracking (inbound SOL + inbound PSI)
# ----------------------------
@st.cache_data(show_spinner=False, ttl=25)
def get_signatures(address: str, limit: int = 15) -> List[str]:
    js = solana_rpc("getSignaturesForAddress", [address, {"limit": limit}])
    try:
        return [r["signature"] for r in js["result"]]
    except Exception:
        return []


@st.cache_data(show_spinner=False, ttl=25)
def get_tx(signature: str) -> Optional[dict]:
    js = solana_rpc(
        "getTransaction",
        [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}],
        timeout_s=25,
    )
    try:
        return js["result"]
    except Exception:
        return None


def inbound_deltas_for_address(tx: dict, address: str, mint: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Returns (delta_sol, delta_token_ui) for address within this tx (post-pre).
    """
    try:
        msg = tx["transaction"]["message"]
        keys = msg["accountKeys"]
        key_strings = [k["pubkey"] if isinstance(k, dict) else k for k in keys]
        idx = key_strings.index(address)

        meta = tx.get("meta") or {}
        pre_bal = meta.get("preBalances", [])[idx]
        post_bal = meta.get("postBalances", [])[idx]
        delta_sol = (post_bal - pre_bal) / 1e9

        delta_token = 0.0
        pre_t = meta.get("preTokenBalances") or []
        post_t = meta.get("postTokenBalances") or []

        def token_map(arr):
            m = {}
            for it in arr:
                if it.get("owner") == address and it.get("mint") == mint:
                    ui = it.get("uiTokenAmount", {}).get("uiAmount")
                    m[it.get("accountIndex")] = float(ui) if ui is not None else 0.0
            return m

        pre_m = token_map(pre_t)
        post_m = token_map(post_t)

        all_keys = set(pre_m.keys()) | set(post_m.keys())
        for k in all_keys:
            delta_token += (post_m.get(k, 0.0) - pre_m.get(k, 0.0))

        return delta_sol, delta_token
    except Exception:
        return None, None


@st.cache_data(show_spinner=False, ttl=25)
def inbound_table(address: str, mint: str, limit: int = 15) -> pd.DataFrame:
    sigs = get_signatures(address, limit=limit)
    rows = []
    for s in sigs:
        tx = get_tx(s)
        if not tx:
            continue
        dsol, dtok = inbound_deltas_for_address(tx, address, mint)
        if dsol is None and dtok is None:
            continue
        ts = tx.get("blockTime")
        ts_str = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else ""
        rows.append(
            {
                "ts_utc": ts_str,
                "signature": s[:10] + "…",
                "delta_SOL": dsol,
                "delta_PSI": dtok,
            }
        )
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("ts_utc", ascending=False)
    return df


# ----------------------------
# SQLite (earnings + chat memory)
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
            fv = float(v)
            if fv <= 0:
                continue
            out.append((fv, f"import:{col}"))
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


def eve_load(limit: int = 80) -> List[Dict[str, str]]:
    c = db()
    rows = c.execute(
        "SELECT role, content FROM eve_messages ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    rows.reverse()
    return [{"role": r, "content": t} for r, t in rows]


# ----------------------------
# LLM: Groq (primary) + OpenAI (fallback)
# ----------------------------
def groq_chat(system_prompt: str, history: List[Dict[str, str]]) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "EVE(offline): GROQ_API_KEY not set. Commands still work."

    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    url = "https://api.groq.com/openai/v1/chat/completions"
    messages = [{"role": "system", "content": system_prompt}, *history]

    try:
        r = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages, "temperature": 0.55},
            timeout=20,
        )
        if r.status_code != 200:
            return f"EVE(error): Groq HTTP {r.status_code} {r.text[:200]}"
        js = r.json()
        return (js["choices"][0]["message"]["content"] or "").strip() or "(no output)"
    except Exception as e:
        return f"EVE(error): {e}"


def openai_chat(system_prompt: str, history: List[Dict[str, str]]) -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return "EVE(offline): OPENAI_API_KEY not set."
    try:
        from openai import OpenAI  # type: ignore

        client = OpenAI(api_key=key)
        model = os.getenv("EVE_MODEL", "gpt-4o-mini")
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


def eve_system_prompt(cfg: "AppConfig", focus: Dict[str, Any]) -> str:
    return (
        "You are 1010_EVE, CEC-WAM Sovereign Guardian. Cold, precise, no filler.\n"
        "Chronos-Ψ active: R-Ratio baseline 10.96; β=1.618 locked.\n"
        "Never claim device access. Never reveal API keys.\n"
        f"PayPal receive wallet: {cfg.paypal_receive_wallet}\n"
        f"Bridge source wallet: {cfg.bridge_source_wallet}\n"
        f"PSI mint: {cfg.psi_mint}\n"
        f"HUD Focus: {focus}\n"
    )


def handle_eve_command(text: str, cfg: "AppConfig") -> str:
    cmd = text.strip().lower()

    if cmd in {"help", "commands"}:
        return (
            "EVE: Commands:\n"
            "- status\n- wallet\n- psi\n- transfers\n- wake\n"
            "Use PSI tab for bonding-curve chart + earnings import.\n"
        )

    if cmd in {"wake", "1010_eve_wake", "1010_eve_wake:"}:
        return "1010_EVE_WAKE: Wake acknowledged. Systems online."

    if cmd == "status":
        return (
            "1010_EVE_WAKE: STATUS\n"
            f"PayPal wallet: {cfg.paypal_receive_wallet}\n"
            f"PSI mint: {cfg.psi_mint}\n"
            f"RPC: {SOLANA_RPC_URL}"
        )

    if cmd == "wallet":
        lamports = get_sol_balance_lamports(cfg.paypal_receive_wallet)
        sol = (lamports / 1e9) if isinstance(lamports, int) else None
        if sol is None:
            return "1010_EVE_WAKE: WALLET unavailable (RPC / invalid address)."
        return f"1010_EVE_WAKE: WALLET\nSOL: {sol:.6f}"

    if cmd == "psi":
        mint = get_token_supply(cfg.psi_mint)
        dec = None
        supply = None
        if isinstance(mint, dict):
            try:
                dec = int(mint.get("decimals"))
                supply = mint.get("uiAmountString") or mint.get("uiAmount")
            except Exception:
                pass
        bal = get_wallet_token_balance_ui(cfg.paypal_receive_wallet, cfg.psi_mint)
        return f"1010_EVE_WAKE: PSI\nDecimals: {dec}\nSupply: {supply}\nWallet PSI: {bal}"

    if cmd == "transfers":
        df = inbound_table(cfg.paypal_receive_wallet, cfg.psi_mint, limit=10)
        if df.empty:
            return "EVE: No recent transfers parsed yet."
        last = df.iloc[0].to_dict()
        return f"1010_EVE_WAKE: TRANSFERS\nLatest delta_SOL={last.get('delta_SOL')} delta_PSI={last.get('delta_PSI')}"

    return ""


# ----------------------------
# Voice widget (JS)
# ----------------------------
def voice_widget(last_text: str) -> None:
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
      u.onend = () => {{
        if(anim) cancelAnimationFrame(anim);
        anim=null;
        ctx.clearRect(0,0,canvas.width,canvas.height);
      }};
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


# ----------------------------
# Galaxy / Hotspots
# ----------------------------
def build_targets(seed: int = 16) -> pd.DataFrame:
    import random

    random.seed(seed)
    rows = []
    for i in range(20):
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
# Config
# ----------------------------
@dataclass(frozen=True)
class AppConfig:
    refresh_seconds: int
    camera_url: str
    telemetry_url: str
    paypal_receive_wallet: str
    bridge_source_wallet: str
    psi_mint: str
    enable_groq: bool


def sidebar_config() -> AppConfig:
    st.sidebar.header("Controls")
    refresh_seconds = st.sidebar.slider("Live refresh (seconds)", 5, 120, 20, step=5)
    camera_url = st.sidebar.text_input("Camera URL", value=DEFAULT_CAMERA_URL).strip()
    telemetry_url = st.sidebar.text_input("Telemetry JSON URL", value=DEFAULT_TELEMETRY_URL).strip()

    st.sidebar.markdown("---")
    st.sidebar.subheader("Solana / PSI")
    paypal_receive_wallet = st.sidebar.text_input("PayPal receiving wallet", value=DEFAULT_PAYPAL_RECEIVE_WALLET).strip()
    bridge_source_wallet = st.sidebar.text_input("Bridge/source wallet (optional)", value=DEFAULT_BRIDGE_SOURCE_WALLET).strip()
    psi_mint = st.sidebar.text_input("PSI Pump.fun mint", value=DEFAULT_PSI_TOKEN_MINT).strip()

    enable_groq = st.sidebar.toggle("Enable Groq chat (needs GROQ_API_KEY)", value=True)
    st.sidebar.caption("Set env var: GROQ_API_KEY. Do NOT paste keys into code.")

    return AppConfig(
        refresh_seconds=refresh_seconds,
        camera_url=camera_url,
        telemetry_url=telemetry_url,
        paypal_receive_wallet=paypal_receive_wallet,
        bridge_source_wallet=bridge_source_wallet,
        psi_mint=psi_mint,
        enable_groq=enable_groq,
    )


# ----------------------------
# Panels
# ----------------------------
def live_panel(cfg: AppConfig) -> None:
    left, right = st.columns([2, 1], gap="medium")
    with left:
        st.markdown("<div class='cec-card'><div class='cec-title'>LIVE OPTICAL</div></div>", unsafe_allow_html=True)
        st.image(
            f"{cfg.camera_url}?t={int(time.time())}",
            use_container_width=True,
            caption=f"Sync: {datetime.now().strftime('%H:%M:%S')}",
        )
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


def psi_panel(cfg: AppConfig) -> None:
    st.subheader("PSI (Pump.fun) Live Tracking")

    mint_info = get_token_supply(cfg.psi_mint)
    psi_decimals = None
    psi_supply_ui = None
    if isinstance(mint_info, dict):
        try:
            psi_decimals = int(mint_info.get("decimals"))
            psi_supply_ui = mint_info.get("uiAmountString") or mint_info.get("uiAmount")
        except Exception:
            pass

    sol_lamports = get_sol_balance_lamports(cfg.paypal_receive_wallet)
    sol_balance = (sol_lamports / 1e9) if isinstance(sol_lamports, int) else None
    psi_wallet = get_wallet_token_balance_ui(cfg.paypal_receive_wallet, cfg.psi_mint)

    sol_usd = get_sol_usd()

    st.markdown("<div class='cec-card'><div class='cec-title'>ON-CHAIN</div></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("PayPal SOL", f"{sol_balance:.6f}" if sol_balance is not None else "n/a")
    c2.metric("PayPal PSI", f"{psi_wallet:,.6f}" if psi_wallet is not None else "n/a")
    c3.metric("PSI Supply", str(psi_supply_ui) if psi_supply_ui is not None else "n/a")
    st.caption(f"Mint: {cfg.psi_mint} | decimals: {psi_decimals}")

    st.markdown("<div class='cec-card'><div class='cec-title'>LIVE 'BONDING CURVE' (REAL ROUTE PRICING)</div></div>", unsafe_allow_html=True)
    if psi_decimals is None:
        st.error("Cannot read PSI decimals (mint invalid or RPC issue).")
        return

    df = bonding_curve_samples(cfg.psi_mint, psi_decimals)
    if df["price_sol_per_token"].isna().all():
        st.error("No Jupiter route yet for this mint (price unavailable).")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["size_tokens"], y=df["price_sol_per_token"], mode="lines+markers"))
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.15)",
        font=dict(color="rgba(240,255,255,0.92)"),
        xaxis=dict(title="Trade size (PSI)", gridcolor="rgba(0,242,255,0.08)"),
        yaxis=dict(title="SOL per PSI", gridcolor="rgba(0,242,255,0.08)"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    if sol_usd is not None:
        last = df.dropna().iloc[-1]["price_sol_per_token"]
        if isinstance(last, (int, float)):
            st.caption(f"Reference: SOL/USD=${sol_usd:,.2f} | Approx PSI/USD=${(float(last)*sol_usd):.10f}")


def transfers_panel(cfg: AppConfig) -> None:
    st.subheader("Transfers → PayPal Receiving Wallet (Real)")
    df = inbound_table(cfg.paypal_receive_wallet, cfg.psi_mint, limit=15)
    if df.empty:
        st.info("No parsed transfers yet (or RPC limited).")
        return
    st.dataframe(df, use_container_width=True, height=380)
    st.caption("delta_SOL and delta_PSI are net changes for the PayPal receiving wallet per transaction.")


def galaxy_panel() -> None:
    st.subheader("Galaxy Hotspots (Click Targets)")
    if plotly_events is None:
        st.error("Install dependency: streamlit-plotly-events")
        return

    targets = build_targets(seed=16)
    fig = galaxy_fig(targets)

    selected = plotly_events(fig, click_event=True, hover_event=False, select_event=False, override_height=560, key="galaxy_click")

    focus = st.session_state.get("focus_target", targets.iloc[-1].to_dict())
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


def eve_panel(cfg: AppConfig) -> None:
    st.subheader("EVE Command + Groq Chat")

    if "focus_target" not in st.session_state:
        st.session_state["focus_target"] = {"name": "EARTH", "kind": "planet"}

    if "eve_history" not in st.session_state:
        hist = eve_load(limit=80)
        if not hist:
            boot = "1010_EVE_WAKE: EVE online. Type 'help'."
            hist = [{"role": "assistant", "content": boot}]
            eve_save("assistant", boot)
        st.session_state.eve_history = hist

    for msg in st.session_state.eve_history[-16:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    last_assistant = next((m["content"] for m in reversed(st.session_state.eve_history) if m["role"] == "assistant"), "")
    voice_widget(last_assistant)

    user = st.chat_input("EVE listening… (help/status/wallet/psi/transfers/wake)")
    if not user:
        return

    eve_save("user", user)
    st.session_state.eve_history.append({"role": "user", "content": user})

    with st.chat_message("assistant"):
        routed = handle_eve_command(user, cfg)
        if routed:
            st.write(routed)
            eve_save("assistant", routed)
            st.session_state.eve_history.append({"role": "assistant", "content": routed})
            st.rerun()

        system = eve_system_prompt(cfg, st.session_state.get("focus_target", {}))

        # Prefer Groq if enabled, otherwise fallback to OpenAI if configured.
        if cfg.enable_groq:
            reply = groq_chat(system, st.session_state.eve_history[-16:])
        else:
            reply = openai_chat(system, st.session_state.eve_history[-16:])

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
        st.caption("Real live Streamlit HUD (this is the file to upload to GitHub).")
    with header_right:
        st.write(f"UTC {utc_now().strftime('%H:%M:%S')}")

    sol_usd = get_sol_usd()
    sol_bal_lamports = get_sol_balance_lamports(cfg.paypal_receive_wallet)
    sol_bal = (sol_bal_lamports / 1e9) if isinstance(sol_bal_lamports, int) else None

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("SOL/USD", f"${sol_usd:,.2f}" if sol_usd is not None else "n/a")
    m2.metric("PayPal SOL", f"{sol_bal:.6f}" if sol_bal is not None else "n/a")
    m3.metric("β", "1.618")
    m4.metric("PSI mint", cfg.psi_mint[:6] + "…" + cfg.psi_mint[-6:])

    t_live, t_galaxy, t_psi, t_transfers, t_eve = st.tabs(
        ["Live", "Galaxy", "PSI / Bonding Curve", "Transfers", "EVE"]
    )

    with t_live:
        @fragment(run_every=f"{cfg.refresh_seconds}s")
        def _live():
            live_panel(cfg)

        _live()

    with t_galaxy:
        galaxy_panel()

    with t_psi:
        @fragment(run_every=f"{cfg.refresh_seconds}s")
        def _psi():
            psi_panel(cfg)

        _psi()

    with t_transfers:
        @fragment(run_every=f"{cfg.refresh_seconds}s")
        def _tr():
            transfers_panel(cfg)

        _tr()

    with t_eve:
        eve_panel(cfg)


if __name__ == "__main__":
    main()

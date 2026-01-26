*** a/eve_cec_wam_live.py
--- b/eve_cec_wam_live.py
***************
*** 1,60 ****
  """
  CEC-WAM EVE Live Dashboard (single-file)
  
  Features
  - Live camera tile with cache-busting timestamp
  - Live telemetry from a Google Apps Script JSON endpoint
  - Ledger loader (concatenates DATA/*.csv)
  - 3D "galaxy map" (Plotly) from telemetry payload, with safe fallbacks
  - EVE chat (Gemini) with secure API key handling (no hardcoded keys)
+ - SOL wallet + PSI token (Pump.fun mint) live on-chain metrics (Solana RPC + Jupiter quotes)
  
  Setup
  - pip install streamlit requests pandas plotly google-generativeai
  - Set GEMINI_API_KEY via:
    - Streamlit secrets: .streamlit/secrets.toml -> GEMINI_API_KEY="..."
    - or environment variable: GEMINI_API_KEY="..."
  - Run: streamlit run eve_cec_wam_live.py
  
  Telemetry payload expectation (optional)
  - data["health"] as a 2D array:
    header row: ["Name","X","Y","Z","Color","Size","Image"]
  """
  
  from __future__ import annotations
  
  import base64
  import glob
  import os
  import random
  import time
  from dataclasses import dataclass
  from datetime import datetime
  from typing import Any, Dict, List, Optional, Tuple
  
  import pandas as pd
  import plotly.graph_objects as go
  import requests
  import streamlit as st
  
  try:
      import google.generativeai as genai
  except Exception:  # pragma: no cover
      genai = None  # type: ignore[assignment]
  
  
  # ----------------------------
  # Config
  # ----------------------------
  
  DEFAULT_WSDOT_CAMERA_URL = "https://images.wsdot.wa.gov/nw/005vc14370.jpg"
  DEFAULT_GOOGLE_SCRIPT_URL = (
      "https://script.google.com/macros/s/AKfycbwJdL9VM4jqrcszFeLjJRJL6V2-IYadL1coQwze4tMtM6WKGBmbLDU2dU18Mwqzf5qtYg/exec"
  )
+ SOLANA_RPC_URL = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
+ JUPITER_QUOTE_URL = "https://quote-api.jup.ag/v6/quote"
+ COINGECKO_SOL_URL = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
+ 
+ # Your wallet + PSI mint (you provided). Treat as authoritative.
+ DEFAULT_PAYPAL_SOL_ADDRESS = "Ek638f2WcP9sPFMjdAHRm9XDpJ7B6uxJqfSAzQGk9NFt"
+ DEFAULT_PSI_TOKEN_MINT = "Ek638f2WcP9sPFMjdAHRm9XDpJ7B6uxJqfSAzQGk9NFt"
+ 
+ # Jupiter constants
+ SOL_MINT = "So11111111111111111111111111111111111111112"
+ USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
  
  BASE_DIR = os.path.abspath(os.path.dirname(__file__))
  DATA_DIR = os.path.join(BASE_DIR, "DATA")
  IMAGES_DIR = os.path.join(BASE_DIR, "images")
***************
*** 60,130 ****
  def _fragment_decorator():
      """
      Streamlit fragments moved from experimental to stable.
      This keeps the app working across Streamlit versions.
      """
      if hasattr(st, "fragment"):
          return st.fragment
      if hasattr(st, "experimental_fragment"):
          return st.experimental_fragment  # type: ignore[attr-defined]
      # Fallback: no-op decorator
      def _noop(*_args, **_kwargs):
          def _wrap(fn):
              return fn
          return _wrap
      return _noop
  
  
  fragment = _fragment_decorator()
  
  
  @dataclass(frozen=True)
  class AppConfig:
      refresh_seconds: int
      enable_camera: bool
      enable_ai: bool
      camera_url: str
      telemetry_url: str
      gemini_model: str
+     sol_wallet: str
+     psi_mint: str
+     enable_external_prices: bool
  
  
  # ----------------------------
  # Secrets / utilities
  # ----------------------------
***************
*** 130,210 ****
  def http_get_json(url: str, timeout_s: int = 10) -> Optional[Dict[str, Any]]:
      """
      Fetch JSON with cache-busting timestamp.
      Returns None on any error.
      """
      try:
          resp = requests.get(f"{url}?t={time.time()}", timeout=timeout_s)
          resp.raise_for_status()
          payload = resp.json()
          if isinstance(payload, dict):
              return payload
          return None
      except Exception:
          return None
+ 
+ 
+ def solana_rpc(method: str, params: list, timeout_s: int = 10) -> Optional[dict]:
+     """
+     Minimal Solana JSON-RPC client. No keys. Uses SOLANA_RPC_URL.
+     """
+     try:
+         payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
+         resp = requests.post(SOLANA_RPC_URL, json=payload, timeout=timeout_s)
+         resp.raise_for_status()
+         data = resp.json()
+         if isinstance(data, dict) and "result" in data:
+             return data
+         return None
+     except Exception:
+         return None
+ 
+ 
+ @st.cache_data(show_spinner=False, ttl=20)
+ def get_sol_balance_lamports(address: str) -> Optional[int]:
+     data = solana_rpc("getBalance", [address, {"commitment": "confirmed"}])
+     try:
+         return int(data["result"]["value"])
+     except Exception:
+         return None
+ 
+ 
+ @st.cache_data(show_spinner=False, ttl=20)
+ def get_mint_info(mint: str) -> Optional[dict]:
+     """
+     Returns decimals + supply (raw integer supply) if available.
+     """
+     data = solana_rpc("getTokenSupply", [mint, {"commitment": "confirmed"}])
+     try:
+         return data["result"]["value"]
+     except Exception:
+         return None
+ 
+ 
+ @st.cache_data(show_spinner=False, ttl=20)
+ def get_wallet_token_balance_ui(owner: str, mint: str) -> Optional[float]:
+     """
+     Sum all SPL token accounts by owner for a specific mint.
+     """
+     data = solana_rpc(
+         "getTokenAccountsByOwner",
+         [owner, {"mint": mint}, {"encoding": "jsonParsed", "commitment": "confirmed"}],
+     )
+     try:
+         accounts = data["result"]["value"]
+         total = 0.0
+         for a in accounts:
+             ui = a["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmount"]
+             if ui is None:
+                 continue
+             total += float(ui)
+         return total
+     except Exception:
+         return None
+ 
+ 
+ @st.cache_data(show_spinner=False, ttl=20)
+ def get_sol_usd() -> Optional[float]:
+     data = http_get_json(COINGECKO_SOL_URL)
+     try:
+         return float(data["solana"]["usd"])
+     except Exception:
+         return None
+ 
+ 
+ @st.cache_data(show_spinner=False, ttl=20)
+ def jupiter_quote_price_in_sol(input_mint: str, amount_in_base_units: int = 1_000_000) -> Optional[float]:
+     """
+     Quotes input_mint -> SOL for amount_in_base_units (default 1e6 units).
+     For most tokens, amount must be in base units (depends on decimals).
+     We'll pass a conservative amount and derive price by ratio of outAmount/amount.
+     """
+     try:
+         params = {
+             "inputMint": input_mint,
+             "outputMint": SOL_MINT,
+             "amount": str(amount_in_base_units),
+             "slippageBps": "50",
+         }
+         resp = requests.get(JUPITER_QUOTE_URL, params=params, timeout=10)
+         if resp.status_code != 200:
+             return None
+         js = resp.json()
+         routes = js.get("data") or []
+         if not routes:
+             return None
+         best = routes[0]
+         out_amount = float(best.get("outAmount", 0))
+         # outAmount is in lamports for SOL
+         out_sol = out_amount / 1e9
+         return out_sol / (amount_in_base_units / 1.0)
+     except Exception:
+         return None
  
  
  @st.cache_data(show_spinner=False, ttl=60)
  def load_ledger_data(data_dir: str) -> Optional[pd.DataFrame]:
      """
      Concatenate CSV files under data_dir. Cached.
      """
***************
*** 310,380 ****
  def sidebar_config() -> AppConfig:
      st.sidebar.header("⚙️ Controls")
  
      refresh_seconds = st.sidebar.slider("Live refresh (seconds)", 5, 120, 30, step=5)
      enable_camera = st.sidebar.toggle("Enable camera", value=True)
      enable_ai = st.sidebar.toggle("Enable EVE (Gemini) chat", value=True)
  
      camera_url = st.sidebar.text_input("Camera URL", value=DEFAULT_WSDOT_CAMERA_URL)
      telemetry_url = st.sidebar.text_input("Telemetry JSON URL", value=DEFAULT_GOOGLE_SCRIPT_URL)
  
      gemini_model = st.sidebar.text_input("Gemini model", value="gemini-1.5-flash")
  
      st.sidebar.caption("Gemini key: set GEMINI_API_KEY in secrets/env (no hardcoded keys).")
+ 
+     st.sidebar.markdown("---")
+     st.sidebar.subheader("🔗 SOL / PSI (Pump.fun)")
+     sol_wallet = st.sidebar.text_input("PayPal SOL address", value=DEFAULT_PAYPAL_SOL_ADDRESS).strip()
+     psi_mint = st.sidebar.text_input("PSI token mint", value=DEFAULT_PSI_TOKEN_MINT).strip()
+     enable_external_prices = st.sidebar.toggle("Enable external prices (CoinGecko/Jupiter)", value=True)
  
      return AppConfig(
          refresh_seconds=refresh_seconds,
          enable_camera=enable_camera,
          enable_ai=enable_ai,
          camera_url=camera_url.strip(),
          telemetry_url=telemetry_url.strip(),
          gemini_model=gemini_model.strip(),
+         sol_wallet=sol_wallet,
+         psi_mint=psi_mint,
+         enable_external_prices=enable_external_prices,
      )
  
***************
*** 380,450 ****
  def live_panel(cfg: AppConfig) -> None:
      @fragment(run_every=f"{cfg.refresh_seconds}s")
      def _live_fragment():
          data = http_get_json(cfg.telemetry_url)
  
          left, right = st.columns([2, 1])
  
          with left:
              st.subheader("📹 LIVE OPTICAL")
              if cfg.enable_camera:
                  st.image(
                      f"{cfg.camera_url}?t={int(time.time())}",
                      caption=f"Last Sync: {datetime.now().strftime('%H:%M:%S')}",
                      use_container_width=True,
                  )
              else:
                  st.info("Camera disabled in sidebar.")
  
          with right:
              st.subheader("📊 LIVE TELEMETRY")
              if data:
                  c1, c2 = st.columns(2)
                  c1.metric("PSI", str(data.get("psi", "N/A")))
                  c2.metric("STATUS", str(data.get("status", "N/A")))
                  st.metric("PSI COINS", str(data.get("psi_coins", "N/A")))
                  st.metric("ASSET VALUE", str(data.get("money", "N/A")))
              else:
                  st.error("Telemetry offline (URL unreachable or invalid JSON).")
  
              st.write("---")
              st.write("**Scanner Status:** Patrol Normal (FWPD)")
              st.caption(f"Refresh: every {cfg.refresh_seconds}s")
  
      _live_fragment()
+ 
+ 
+ def psi_panel(cfg: AppConfig) -> None:
+     @fragment(run_every=f"{cfg.refresh_seconds}s")
+     def _psi_fragment():
+         st.subheader("🧪 PSI / Pump.fun (On-chain + Market)")
+ 
+         sol_lamports = get_sol_balance_lamports(cfg.sol_wallet)
+         sol_balance = (sol_lamports / 1e9) if isinstance(sol_lamports, int) else None
+ 
+         mint_info = get_mint_info(cfg.psi_mint)
+         psi_supply_ui = None
+         psi_decimals = None
+         if isinstance(mint_info, dict):
+             psi_decimals = mint_info.get("decimals")
+             psi_supply_ui = mint_info.get("uiAmountString") or mint_info.get("uiAmount")
+ 
+         psi_wallet_ui = get_wallet_token_balance_ui(cfg.sol_wallet, cfg.psi_mint)
+ 
+         sol_usd = get_sol_usd() if cfg.enable_external_prices else None
+ 
+         # Jupiter: we must choose amount. Use 1e6 base units and interpret as "micro units".
+         # This yields a ratio usable as "SOL per base unit". We'll also compute per 1 token if decimals known.
+         quote_sol_per_base = jupiter_quote_price_in_sol(cfg.psi_mint, amount_in_base_units=1_000_000) if cfg.enable_external_prices else None
+         quote_sol_per_token = None
+         if quote_sol_per_base is not None and isinstance(psi_decimals, int):
+             quote_sol_per_token = quote_sol_per_base * (10 ** psi_decimals)
+ 
+         c1, c2, c3 = st.columns(3)
+         c1.metric("PayPal SOL (wallet)", f"{sol_balance:.6f} SOL" if sol_balance is not None else "n/a")
+         c2.metric("PSI in wallet", f"{psi_wallet_ui:,.6f} PSI" if psi_wallet_ui is not None else "n/a")
+         c3.metric("PSI supply", f"{psi_supply_ui}" if psi_supply_ui is not None else "n/a")
+ 
+         st.caption(f"Wallet: {cfg.sol_wallet}")
+         st.caption(f"PSI mint: {cfg.psi_mint}")
+ 
+         if quote_sol_per_token is not None:
+             st.metric("PSI price (SOL)", f"{quote_sol_per_token:.10f} SOL")
+             if sol_usd is not None:
+                 st.metric("PSI price (USD)", f"${(quote_sol_per_token * sol_usd):.10f}")
+                 if psi_wallet_ui is not None:
+                     st.metric("Wallet PSI value (USD)", f"${(psi_wallet_ui * quote_sol_per_token * sol_usd):,.4f}")
+         else:
+             st.info("Price unavailable (Jupiter route not found or mint invalid).")
+ 
+         st.warning("Creator fees: pump.fun does not expose a reliable public API. Import an export/CSV when available.")
+ 
+     _psi_fragment()
  
***************
*** 450,540 ****
  def eve_chat(cfg: AppConfig, model: Optional[Any]) -> None:
      if "messages" not in st.session_state:
          st.session_state.messages = [
              {"role": "assistant", "content": "EVE online. Give me a command."}
          ]
  
      for msg in st.session_state.messages:
          with st.chat_message(msg["role"]):
              st.write(msg["content"])
  
      user_text = st.chat_input("EVE is listening…")
      if not user_text:
          return
  
      st.session_state.messages.append({"role": "user", "content": user_text})
      with st.chat_message("user"):
          st.write(user_text)
  
      with st.chat_message("assistant"):
          if not cfg.enable_ai:
              st.write("EVE chat is disabled in the sidebar.")
              st.session_state.messages.append(
                  {"role": "assistant", "content": "EVE chat is disabled in the sidebar."}
              )
              return
  
          if model is None:
              st.write("Gemini not configured. Set GEMINI_API_KEY in secrets/env.")
              st.session_state.messages.append(
                  {
                      "role": "assistant",
                      "content": "Gemini not configured. Set GEMINI_API_KEY in secrets/env.",
                  }
              )
              return
+ 
+         # --- deterministic command routing (no hallucinations) ---
+         cmd = user_text.strip().lower()
+         if cmd in {"help", "commands"}:
+             text = (
+                 "EVE: Commands: help | status | prices | wallet | psi | wake\n"
+                 "Also: use the PSI tab for on-chain panels. External prices toggle in sidebar."
+             )
+             st.write(text)
+             st.session_state.messages.append({"role": "assistant", "content": text})
+             return
+ 
+         if cmd in {"wake", "1010_eve_wake"}:
+             text = "1010_EVE_WAKE: Wake acknowledged. Systems online."
+             st.write(text)
+             st.session_state.messages.append({"role": "assistant", "content": text})
+             return
+ 
+         if cmd == "wallet":
+             lamports = get_sol_balance_lamports(cfg.sol_wallet)
+             sol = (lamports / 1e9) if isinstance(lamports, int) else None
+             psi_bal = get_wallet_token_balance_ui(cfg.sol_wallet, cfg.psi_mint)
+             text = (
+                 f"1010_EVE_WAKE: WALLET\n"
+                 f"SOL: {sol:.6f} SOL\nPSI: {psi_bal:,.6f} PSI"
+                 if (sol is not None and psi_bal is not None)
+                 else "1010_EVE_WAKE: WALLET data unavailable (RPC issue or invalid address/mint)."
+             )
+             st.write(text)
+             st.session_state.messages.append({"role": "assistant", "content": text})
+             return
+ 
+         if cmd == "psi":
+             mint = get_mint_info(cfg.psi_mint)
+             psi_bal = get_wallet_token_balance_ui(cfg.sol_wallet, cfg.psi_mint)
+             text = f"1010_EVE_WAKE: PSI\nMint: {cfg.psi_mint}\nWallet PSI: {psi_bal}\nMint info: {mint}"
+             st.write(text)
+             st.session_state.messages.append({"role": "assistant", "content": text})
+             return
+ 
+         if cmd == "prices":
+             cg = http_get_json("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true")
+             if not cg:
+                 text = "EVE: prices unavailable (CoinGecko offline)."
+             else:
+                 def fmt(k, sym):
+                     usd = cg.get(k, {}).get("usd")
+                     ch = cg.get(k, {}).get("usd_24h_change")
+                     return f"{sym}: ${usd:,.2f} ({ch:+.2f}%)" if isinstance(usd,(int,float)) and isinstance(ch,(int,float)) else f"{sym}: n/a"
+                 text = "EVE: PRICES\n" + "\n".join([fmt("bitcoin","BTC"), fmt("ethereum","ETH"), fmt("solana","SOL")])
+             st.write(text)
+             st.session_state.messages.append({"role": "assistant", "content": text})
+             return
+ 
+         if cmd == "status":
+             online = http_get_json(cfg.telemetry_url) is not None
+             text = f"1010_EVE_WAKE: STATUS\nTelemetry: {'ONLINE' if online else 'OFFLINE'}\nSOL Wallet: {cfg.sol_wallet}\nPSI Mint: {cfg.psi_mint}"
+             st.write(text)
+             st.session_state.messages.append({"role": "assistant", "content": text})
+             return
  
          prompt = (
              "You are EVE, the CEC-WAM system intelligence. "
              "Be concise, tactical, and helpful. "
              f"User command: {user_text}"
          )
          try:
              resp = model.generate_content(prompt)
              text = getattr(resp, "text", None) or str(resp)
          except Exception as e:
              text = f"AI error: {e}"
  
          st.write(text)
          st.session_state.messages.append({"role": "assistant", "content": text})
  
***************
*** 540,610 ****
  def main() -> None:
      st.set_page_config(page_title="CEC-WAM EVE LIVE", page_icon="🦅", layout="wide")
      inject_theme_css()
  
      cfg = sidebar_config()
      model = init_gemini(cfg.gemini_model) if cfg.enable_ai else None
  
      header_left, header_right = st.columns([3, 1])
      with header_left:
          st.title("🦅 CEC-WAM // EVE LIVE")
          st.caption("Fragments-enabled live tiles + telemetry + ledger + galaxy + EVE chat.")
      with header_right:
          online = http_get_json(cfg.telemetry_url) is not None
          st.success("🟢 ONLINE") if online else st.error("🔴 SIGNAL LOST")
  
!     t_live, t_galaxy, t_ledger, t_psi, t_eve = st.tabs(["🔴 Live", "🌌 Galaxy", "📚 Ledger", "🧪 PSI / Pump.fun", "📡 EVE"])
  
      with t_live:
          live_panel(cfg)
  
      with t_galaxy:
          data = http_get_json(cfg.telemetry_url)
          names, xs, ys, zs, colors, sizes, _images = build_galaxy_data(data)
          fig = render_galaxy_map(names, xs, ys, zs, colors, sizes)
          st.subheader("🌌 Galaxy Map")
          st.plotly_chart(fig, use_container_width=True)
  
      with t_ledger:
          st.subheader("📚 Ledger")
          ledger_df = load_ledger_data(DATA_DIR)
          if ledger_df is None:
              st.warning(f"No ledger CSVs found. Put files in: {DATA_DIR}")
          else:
              st.dataframe(ledger_df, use_container_width=True, hide_index=True)
              st.caption(f"Rows: {len(ledger_df):,} | Columns: {len(ledger_df.columns):,}")
  
+     with t_psi:

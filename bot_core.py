from pathlib import Path
import json
from utils.nlp_utils import clean_text, contains_any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def _load_json(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default


# Load example stocks & forex pairs
_default_stocks = [
    "RELIANCE",
    "TCS",
    "HDFCBANK",
    "ICICIBANK",
    "INFY",
    "SBIN",
]
_default_forex = [
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "USD/CHF",
    "AUD/USD",
    "USD/INR",
    "EUR/INR",
    "GBP/INR",
]

SYMBOLS_BSE = _load_json(DATA_DIR / "symbols_bse.json", _default_stocks)
FOREX_PAIRS = _load_json(DATA_DIR / "forex_pairs.json", _default_forex)

# ---------- KNOWLEDGE BASE RESPONSES ----------

top_bse_pretty = [
    "RELIANCE Industries",
    "TCS (Tata Consultancy Services)",
    "HDFC Bank",
    "ICICI Bank",
    "Infosys",
    "State Bank of India (SBIN)",
    "Bharti Airtel",
    "ITC",
    "Larsen & Toubro (LT)",
    "Axis Bank",
]

top_books = [
    "The Intelligent Investor – Benjamin Graham",
    "A Random Walk Down Wall Street – Burton Malkiel",
    "The Little Book of Common Sense Investing – John C. Bogle",
    "Market Wizards – Jack D. Schwager",
    "Common Stocks and Uncommon Profits – Philip Fisher",
    "One Up On Wall Street – Peter Lynch",
    "Trading in the Zone – Mark Douglas",
    "Technical Analysis of the Financial Markets – John J. Murphy",
    "Reminiscences of a Stock Operator – Edwin Lefèvre",
    "Common Sense on Mutual Funds – John C. Bogle",
]

RESPONSES = {
    "top_shares": "📈 **Popular Indian Large-cap Stocks (examples, not advice):**\n"
    + "\n".join(f"{i+1}. {s}" for i, s in enumerate(top_bse_pretty)),
    "books": "📚 **Good Books to Learn Markets:**\n"
    + "\n".join(f"{i+1}. {b}" for i, b in enumerate(top_books)),
    "pe_pb": (
        "📊 **PE & PB Ratio (Basics)**\n\n"
        "**PE (Price / Earnings) Ratio**\n"
        "- Shows how much you pay for ₹1 of earnings.\n"
        "- Example: PE = 20 → You pay ₹20 for ₹1 yearly earning.\n"
        "- High PE: market expecting growth (or stock is overvalued).\n"
        "- Low PE: may be undervalued or weak business.\n\n"
        "**PB (Price / Book) Ratio**\n"
        "- Price compared to *book value* (assets − liabilities).\n"
        "- PB < 1: market value below book value (sometimes value pick, sometimes weak business).\n"
        "- PB > 1: market is willing to pay more than book value.\n\n"
        "**Fundamental vs Technical Analysis**\n"
        "- Fundamentals: business quality, profit, debt, growth.\n"
        "- Technicals: price, volume, charts, trends, patterns.\n"
        "👉 Use both together for better decisions."
    ),
    "candles": (
        "🕯 **Candlestick Chart Basics**\n\n"
        "Each candle shows price movement for a time period (e.g., 5 min, 1 hour, 1 day):\n"
        "- Open: price at start of candle\n"
        "- Close: price at end of candle\n"
        "- High: highest price in that period\n"
        "- Low: lowest price in that period\n\n"
        "**Important Patterns (just a few):**\n"
        "- Hammer: small body, long lower wick → possible reversal from downtrend.\n"
        "- Shooting Star: small body, long upper wick → possible reversal from uptrend.\n"
        "- Doji: open ≈ close → indecision.\n"
        "- Bullish Engulfing: green candle fully covers previous red → strong buying.\n"
        "- Bearish Engulfing: red candle covers previous green → strong selling.\n\n"
        "📌 Use candlestick patterns **with** support/resistance and trend, not alone."
    ),
    "stop_loss": (
        "🛑 **Stop-loss (SL) – Your Safety Belt**\n\n"
        "- Stop-loss is a pre-decided price where you will exit if trade goes wrong.\n"
        "- Purpose: limit loss and protect capital.\n\n"
        "**Example:**\n"
        "- Buy a stock at ₹100\n"
        "- You set SL at ₹95 (risk ₹5 per share)\n"
        "- If price hits ₹95, you sell automatically.\n\n"
        "**Tips:**\n"
        "- Decide risk per trade (e.g., 1–2% of your total capital).\n"
        "- Place SL near logical support, not random numbers.\n"
        "- Never remove SL just to \"hope\" market will reverse."
    ),
    "target": (
        "🎯 **Target Price (TP) – Profit Booking Level**\n\n"
        "- Target is the price where you plan to book profit.\n"
        "- Helps avoid greed and brings discipline.\n\n"
        "**How to Set Targets:**\n"
        "- Use resistance levels.\n"
        "- Use chart patterns or breakouts.\n"
        "- Use risk–reward ratio:\n"
        "  Example: Risk = ₹5, Reward = ₹10 → 1:2 ratio.\n\n"
        "**Example Trade:**\n"
        "- Buy at ₹100\n"
        "- Stop-loss at ₹95\n"
        "- Target at ₹110 or ₹115\n"
        "If target hits, you exit with profit. If SL hits, small controlled loss."
    ),
    "support_resistance": (
        "🧱 **Support & Resistance (S/R)**\n\n"
        "**Support**\n"
        "- A price zone where buying interest is strong.\n"
        "- Price often *bounces up* from here.\n"
        "- Marked by previous lows.\n\n"
        "**Resistance**\n"
        "- A price zone where selling interest is strong.\n"
        "- Price often *reverses down* from here.\n"
        "- Marked by previous highs.\n\n"
        "**How to Use:**\n"
        "- Buy near support (with SL below it).\n"
        "- Book profit or be careful near resistance.\n"
        "- Higher time frame S/R (daily, weekly) are stronger."
    ),
    "trendline": (
        "📐 **Trendlines – See the Market Direction**\n\n"
        "- Draw an uptrend line by connecting **higher lows**.\n"
        "- Draw a downtrend line by connecting **lower highs**.\n"
        "- Need at least 2–3 touches to trust a trendline.\n\n"
        "Uses:\n"
        "- Shows overall trend (up, down, sideways).\n"
        "- Break of a strong trendline can hint at trend reversal.\n"
        "- Can act as dynamic support/resistance."
    ),
    # Forex-related
    "forex_intro": (
        "🌍 **What is Forex (Foreign Exchange)?**\n\n"
        "- Forex is the global market for trading currencies (e.g., EUR/USD, USD/INR).\n"
        "- Always traded in *pairs* (you buy one currency and sell another).\n\n"
        "**Example:**\n"
        "- EUR/USD = 1.10 → 1 EUR = 1.10 USD.\n\n"
        "**In Indian Context:**\n"
        "- Regulated by RBI & SEBI.\n"
        "- Only trade with properly regulated brokers and only for education/experience.\n"
        "- Be careful of illegal high-leverage offshore brokers.\n\n"
        "Forex is **high risk**. Learn slowly and focus on risk management."
    ),
    "forex_pairs": (
        "💱 **Types of Forex Pairs**\n\n"
        "**Major Pairs (with USD):**\n"
        "- EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, NZD/USD.\n\n"
        "**Cross Pairs (no USD):**\n"
        "- EUR/GBP, EUR/JPY, GBP/JPY, AUD/JPY etc.\n\n"
        "**INR-related pairs:**\n"
        "- USD/INR, EUR/INR, GBP/INR, JPY/INR.\n\n"
        "These are just examples for **learning**, not trading calls."
    ),
    "forex_pips_lots": (
        "📏 **Pips, Lots & Spread (Forex Basics)**\n\n"
        "**Pip (Price Interest Point):**\n"
        "- Smallest price movement in most pairs = 0.0001 (1 pip).\n"
        "- For JPY pairs, 1 pip = 0.01.\n\n"
        "**Lot Size:**\n"
        "- 1 Standard Lot = 100,000 units of base currency.\n"
        "- 1 Mini Lot = 10,000 units.\n"
        "- 1 Micro Lot = 1,000 units.\n\n"
        "**Spread:**\n"
        "- Difference between Buy (Ask) and Sell (Bid) price.\n"
        "- Lower spread = cheaper to enter & exit trades.\n\n"
        "Understanding pips & lots is crucial for position sizing and risk control."
    ),
    "forex_sessions": (
        "🕒 **Forex Market Sessions**\n\n"
        "Forex runs almost 24 hours a day (Monday to Friday) through different sessions:\n"
        "- Sydney Session 🦘\n"
        "- Tokyo Session 🗼 (Asian)\n"
        "- London Session 🏦 (European)\n"
        "- New York Session 🗽 (US)\n\n"
        "Most volatility usually happens when **London and New York** sessions overlap.\n"
        "Different pairs are more active in different sessions (e.g., JPY in Asian, GBP/EUR in London)."
    ),
    "forex_risk": (
        "⚠️ **Risk Management (For Stocks & Forex)**\n\n"
        "- Never risk more than 1–2% of your total capital per trade.\n"
        "- Always use a stop-loss.\n"
        "- Avoid over-leverage (very high lot size with small capital).\n"
        "- Avoid revenge trading after a loss.\n"
        "- Keep a trading journal: note why you entered/exited.\n\n"
        "Goal: survive long-term and learn steadily, not get rich in one risky trade."
    ),
    "forex_vs_stocks": (
        "📊 **Forex vs Indian Stock Market (Simple View)**\n\n"
        "**Forex:**\n"
        "- Trading currency pairs.\n"
        "- Runs nearly 24x5.\n"
        "- High leverage often available (high risk).\n"
        "- Driven by macro news: interest rates, central bank policy, GDP, inflation.\n\n"
        "**Stocks (NSE/BSE):**\n"
        "- You buy shares of companies.\n"
        "- Fixed hours (9:15 AM – 3:30 PM, India).\n"
        "- Driven by company results, sector news, economy, sentiment.\n\n"
        "Both require education, discipline and strong risk management."
    ),
}


def get_stock_examples():
    """Return a short list of example stock symbols."""
    return SYMBOLS_BSE[:10]


def get_forex_examples():
    """Return a short list of example forex pairs."""
    return FOREX_PAIRS[:10]


def get_response(message: str) -> str:
    """Main intent routing function."""
    msg = clean_text(message)

    # ---- Stock-related intents ----
    if contains_any(msg, ["top share", "top stock", "top bse", "nse list"]):
        return RESPONSES["top_shares"]
    if "book" in msg or "books" in msg or "read" in msg:
        return RESPONSES["books"]
    if any(k in msg for k in ["pe", "p/e", "pb", "p/b", "valuation", "fundamental", "technical"]):
        return RESPONSES["pe_pb"]
    if any(k in msg for k in ["candle", "candlestick", "chart pattern"]):
        return RESPONSES["candles"]
    if any(k in msg for k in ["stop loss", "stoploss", "sl"]):
        return RESPONSES["stop_loss"]
    if any(k in msg for k in ["target", "tp", "take profit"]):
        return RESPONSES["target"]
    if "support" in msg and "resistance" in msg:
        return RESPONSES["support_resistance"]
    if any(k in msg for k in ["trendline", "trend line", "trend"]):
        return RESPONSES["trendline"]

    # ---- Forex-related intents ----
    if any(k in msg for k in ["forex", "fx", "currency market", "currency trading"]):
        if any(k in msg for k in ["vs stock", "compare", "difference", "stock market"]):
            return RESPONSES["forex_vs_stocks"]
        if "pair" in msg or "pairs" in msg:
            return RESPONSES["forex_pairs"]
        return RESPONSES["forex_intro"]
    if any(k in msg for k in ["pip", "pips", "lot", "lots", "spread"]):
        return RESPONSES["forex_pips_lots"]
    if any(k in msg for k in ["session", "london", "new york", "tokyo", "sydney"]):
        return RESPONSES["forex_sessions"]
    if any(k in msg for k in ["risk", "money management", "position size", "capital"]):
        return RESPONSES["forex_risk"]

    # ---- General questions that mention both ----
    if "forex" in msg and "stock" in msg:
        return RESPONSES["forex_vs_stocks"]

    # ---- Fallback ----
    return (
        "🤖 I'm not fully sure about that exact question.\n\n"
        "You can ask me things like:\n"
        "- What is PE & PB ratio?\n"
        "- Explain candlestick basics.\n"
        "- What is forex and what are major pairs?\n"
        "- What are pips, lots and spread?\n"
        "- How to manage risk in trading?\n\n"
        "I am an **educational bot**, not for live signals or recommendations."
    )
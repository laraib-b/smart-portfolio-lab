"""Load and download adjusted close prices for the portfolio universe."""

from __future__ import annotations

from pathlib import Path
from time import sleep

import pandas as pd
import yfinance as yf

DEFAULT_TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "KO",
    "WMT",
    "JPM",
    "XOM",
    "JNJ",
]
DEFAULT_BENCHMARK = "SPY"
DEFAULT_START = "2020-01-01"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE_PATH = PROJECT_ROOT / "data" / "cache" / "prices_close.csv"


def download_prices(
    tickers: list[str],
    start: str = DEFAULT_START,
    end: str | None = None,
    max_retries: int = 3,
) -> pd.DataFrame:
    """
    Download adjusted close prices one ticker at a time.

    Yahoo Finance can be rate-limited; retries and short pauses improve reliability.
    """
    frames: dict[str, pd.Series] = {}

    for ticker in tickers:
        last_error: Exception | None = None
        for attempt in range(1, max_retries + 1):
            try:
                df = yf.download(
                    ticker,
                    start=start,
                    end=end,
                    auto_adjust=True,
                    progress=False,
                    threads=False,
                )
                if df.empty:
                    raise ValueError("empty dataframe")

                close = df["Close"]
                # Newer yfinance may return a one-column DataFrame for Close.
                if isinstance(close, pd.DataFrame):
                    close = close.squeeze(axis=1)

                frames[ticker] = close.rename(ticker)
                break
            except Exception as exc:  # noqa: BLE001 - surface download failures to caller logs
                last_error = exc
                sleep(2 * attempt)
        else:
            raise RuntimeError(f"Could not download {ticker}: {last_error}")

        sleep(0.5)

    prices = pd.concat(frames, axis=1).sort_index()
    prices.index = pd.to_datetime(prices.index).tz_localize(None)
    return prices


def save_prices(prices: pd.DataFrame, path: Path = DEFAULT_CACHE_PATH) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    prices.to_csv(path)
    return path


def load_prices(path: Path = DEFAULT_CACHE_PATH) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"No cached prices at {path}. Run download_prices() and save_prices() first."
        )
    prices = pd.read_csv(path, index_col=0, parse_dates=True)
    prices = prices.sort_index()
    return prices


def load_or_download(
    tickers: list[str] | None = None,
    start: str = DEFAULT_START,
    end: str | None = None,
    cache_path: Path = DEFAULT_CACHE_PATH,
    refresh: bool = False,
) -> pd.DataFrame:
    """Load cached prices unless refresh=True or the cache is missing."""
    tickers = tickers or (DEFAULT_TICKERS + [DEFAULT_BENCHMARK])
    cache_path = Path(cache_path)

    if not refresh and cache_path.exists():
        return load_prices(cache_path)

    prices = download_prices(tickers, start=start, end=end)
    save_prices(prices, cache_path)
    return prices

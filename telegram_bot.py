import os, time, requests, threading

from models import PlayerResponse
from utils.time_utils import fmt_dt_es, fmt_eur

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

# Memoria simple para respetar 1 msg/seg por chat
_last_sent_by_chat = {}
_lock = threading.Lock()

class TelegramError(RuntimeError): ...
def _respect_per_chat_rate(chat_id: str, min_interval: float = 1.1):
    with _lock:
        last = _last_sent_by_chat.get(chat_id, 0.0)
        now = time.time()
        wait = (last + min_interval) - now
        if wait > 0:
            time.sleep(wait)
        _last_sent_by_chat[chat_id] = time.time()

def send_message(text: str, parse_mode: str | None = "Markdown") -> None:
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        raise TelegramError("Faltan TG_BOT_TOKEN o TG_CHAT_ID")

    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": text, "disable_web_page_preview": True}
    if parse_mode:
        payload["parse_mode"] = parse_mode

    # Hasta 5 reintentos respetando retry_after
    attempts = 0
    while True:
        _respect_per_chat_rate(str(TG_CHAT_ID))  # 1 msg/seg por chat
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code != 429:
            r.raise_for_status()
            return
        # 429: respeta retry_after si viene en JSON o en headers
        attempts += 1
        if attempts > 5:
            raise TelegramError(f"Demasiados 429 consecutivos: {r.text[:200]}")
        try:
            retry_after = r.json().get("parameters", {}).get("retry_after")
        except Exception:
            retry_after = None
        if retry_after is None:
            retry_after = int(r.headers.get("Retry-After", "3") or "3")
        time.sleep(max(1, int(retry_after)))


def format_clause_message(buyer: str, seller: str, player: PlayerResponse, amount: int, when) -> str:
    return (
    "💣 *Cláusula ejecutada*\n"
    f"👤 {buyer} le ha quitado a {seller}\n"
    f"🧑‍🦱 {player.data.name} del {player.data.team.name}\n"
    f"💸 {fmt_eur(amount)}\n"
    f"🕒 {fmt_dt_es(when)}"
    )
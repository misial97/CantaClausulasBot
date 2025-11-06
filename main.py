from datetime import datetime, timezone, timedelta
from logger import logger
from dotenv import load_dotenv
load_dotenv()
from dedupsql import ensure_db, event_id_for, is_seen, mark_seen
from api_client import get_clause_movements,get_biwenger_token, get_player_detail
from telegram_bot import send_message, format_clause_message


def run_once() -> None:
    logger.info("Searching new clauses...")

    token = get_biwenger_token()
    mv = get_clause_movements(token)


    for movement in mv.data:
        if not is_recent(movement.date, window_minutes=30):
            continue  # fuera de la ventana "ahora"
        for mov_detail in movement.content:
            eid = event_id_for(str(mov_detail.to.id), str(mov_detail.from_.id), str(mov_detail.player),str(movement.date))
            if is_seen(eid):
                continue  # ya avisado
            buyer = mov_detail.to.name
            seller = mov_detail.from_.name
            player_detail = get_player_detail(mov_detail.player, token)
            msg = format_clause_message(buyer, seller, player_detail, mov_detail.amount, movement.date_dt)
            logger.info("Sending message: " + msg)
            # Aquí podrías aplicar filtros (propio equipo, lista blanca/negra, etc.)
            send_message(msg)
            mark_seen(eid, movement.date)

    logger.info("Finished searching new clauses in this iteration...")


def is_recent(event_ts: int, window_minutes: int = 10) -> bool:
    """
    Devuelve True si el evento está dentro de la ventana reciente.
    event_ts: epoch (segundos) que viene en la API.
    """
    now = datetime.now(tz=timezone.utc)
    evt = datetime.fromtimestamp(event_ts, tz=timezone.utc)
    return now - evt <= timedelta(minutes=window_minutes)

if __name__ == "__main__":
    ensure_db()
    run_once()

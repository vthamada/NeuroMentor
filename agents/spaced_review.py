# agents/spaced_review.py

from datetime import datetime, timedelta
from typing import List

_INTERVALOS = [1, 3, 7, 14]

def gerar_revisoes_proximas(inicio: datetime | None = None) -> List[str]:
    inicio = inicio or datetime.today()
    return [(inicio + timedelta(days=i)).strftime("%d/%m/%Y") for i in _INTERVALOS]

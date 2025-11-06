# ⚽️ CantaCláusulasBot

> 🧠 Bot en Python que detecta **cláusulas de jugadores en Biwenger** y las canta en **Telegram**, en tiempo real.

---

## 🚀 Descripción

**CantaCláusulasBot** monitoriza el histórico de movimientos de tu liga Biwenger y detecta automáticamente cuándo alguien paga una cláusula.  
Envía una notificación formateada por Telegram con todos los detalles:  
quién compra, quién vende, el jugador implicado y el importe.  

El bot incluye:
- ✅ Consumo de la API de Biwenger (movimientos `clauses`)
- ✅ Validación robusta con **Pydantic**
- ✅ Envío a **Telegram Bot API**
- ✅ **Deduplicación** con SQLite para no repetir avisos
- ✅ **Filtro temporal** para mostrar solo los últimos minutos
- ✅ Logging configurable (`DEBUG`, `INFO`, etc.)
- ✅ Listo para desplegar gratis en **Render** o **Koyeb**

---

## 🧩 Estructura del proyecto


---



## ⚙️ Prerequisitos

### 1️⃣ Tener Bot de Telegram y Canal
    
Se puede seguir su documentación oficial para crearlo y poder asi obtener el token del bot y el id del canal dónde se mandarán los mensajes.

https://core.telegram.org/bots/tutorial

### 2️⃣ Obtener headers necesarios API Biwenger
    
Necesitarás obligatoriamente los headers X-League y X-User, que los puedes obtener de las propias llamadas que realiza Biwenger al navegar por su web.

---

## ⚙️ Instalación local

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/misial97/CantaClausulasBot.git
cd CantaClausulasBot
```
### 2️⃣ Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\activate.bat   # Windows
```
### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4️⃣ Configurar variables (.env)
```bash
# No modificar
GET_TOKEN_URL=https://biwenger.as.com/api/v2/auth/login
GET_CLAUSES_MOVEMENTS_URL=https://biwenger.as.com/api/v2/league/$League_Id/board?type=clauses&limit=20
GET_PLAYER_DETAIL=https://biwenger.as.com/api/v2/players/la-liga/

X_LEAGUE_HEADER=X-League
X_USER_HEADER=X-User

# A modificar
BIW_PASSWORD=pass_user_biwenger
BIW_USERNAME=user_biwenger
RUN_INTERVAL_SEC=30
TG_BOT_TOKEN=telegram_bot_token
TG_CHAT_ID=telegram_chat_id
X_LEAGUE_HEADER_VALUE=biwenger_x-league-header_value
X_USER_HEADER_VALUE=biwenger_x-user-header_value
```

---

## ☁️ Despliegue gratuito
🚀 Vía **Koyeb** 

1. Sube el proyecto a GitHub.
2. Entra en Koyeb (https://app.koyeb.com/)
3. Crea un nuevo servicio → GitHub Deploy → elige este repo.
    - Tipo: Dockerfile
    - Pon las variables de entorno que no quieras almacenar en el repo, las del apartado "A modificar" son las recomendables a incluir ahi, y no almacenar el valor directamente en el repositorio (si lo tienes público)
4. Deploy ✅

Cabe destacar, que para que se mantenga activo, es necesario que haya otra herramienta que haga ping de vez en cuando. Por ejemplo con https://uptimerobot.com/ haciendo ping al health cada 10 minutos.

---

## 📜 Licencia

MIT License — libre para usar, modificar y compartir.
Si lo usas o mejoras, ¡deja una estrella ⭐ en el repo!
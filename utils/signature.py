import hashlib
import os
import logging

logger = logging.getLogger(__name__)

def generate_signature(payload):
    API_TOKEN = os.getenv("FLIGHT_API_TOKEN")
    HOST = os.getenv("HOST", "traveloo.fr")
    MARKER = os.getenv("FLIGHT_API_MARKER")

    values = []

    values.append(HOST)
    values.append(payload["locale"])
    values.append(MARKER)
    values.append(payload["passengers"]["adults"])
    values.append(payload["passengers"]["children"])
    values.append(payload["passengers"]["infants"])

    for segment in payload["segments"]:
        values.append(str(segment["date"]))        # ✅ conversion date → string
        values.append(segment["destination"])
        values.append(segment["origin"])

    values.append(payload["trip_class"])
    values.append(payload["user_ip"])

    # 🔒 Sécurisé : convertit tout en string
    signature_str = f"{API_TOKEN}:" + ":".join(map(str, values))
    logger.debug("🔐 Signature string: %s", signature_str)

    return hashlib.md5(signature_str.encode()).hexdigest()

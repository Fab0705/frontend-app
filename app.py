import streamlit as st
import requests
import os
st.set_page_config(page_title="AI Content Auditor", layout="wide", page_icon=" ")
# Inyección de URLs desde variables de entorno con fallback para desarrollo local
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://ai-engine:8000/process")
AUDIT_SERVICE_URL = os.getenv("AUDIT_SERVICE_URL", "http://audit-vault:8000")
st.title(" AI Content Auditor Pro")
st.subheader("Gobernanza Cloud y Auditoría Automatizada con Inteligencia Artificial")
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.header("Análisis de Texto Exclusivo")
    text_input = st.text_area("Texto a procesar:", height=220, placeholder="Escribe o pega el reporte/contrato aquí...")
    if st.button("Procesar y Auditar", use_container_width=True):
        if text_input.strip():
            with st.spinner("1. Evaluando contenido con Gemini AI Engine..."):
                try:
                    res_ai = requests.post(AI_SERVICE_URL, json={"text": text_input.strip()}, timeout=20)
                    if res_ai.status_code == 200:
                        ai_data = res_ai.json()
                        result = ai_data.get("result", "Sin respuesta legible.")
                        st.success(" Respuesta Generada por IA")
                        st.write(result)
                        # Paso 2: Registrar automáticamente en la bóveda de auditoría
                        with st.spinner("2. Inmortalizando registro en Audit Vault..."):
                            audit_payload = {
                                "action": "AI_ANALYSIS_AUDIT",
                                "original_text": text_input.strip(),
                                "ai_result": result
                            }
                            res_audit = requests.post(f"{AUDIT_SERVICE_URL}/log", json=audit_payload, timeout=5)
                            if res_audit.status_code == 201:
                                st.caption(" Transacción indexada con éxito en la bóveda inmutable.")
                    else:
                        st.error(f"Error en AI Engine Backend. Código HTTP: {res_ai.status_code}")
                except Exception as e:
                    st.error(f"Fallo crítico de red inter-servicio: {str(e)}")
        else:
            st.warning("Por favor introduce contenido válido.")
with col2:
    st.header("Historial de Auditoría Local")
    if st.button("Sincronizar y Refrescar Logs", use_container_width=True):
        with st.spinner("Leyendo base de datos segura..."):
            try:
                res_logs = requests.get(f"{AUDIT_SERVICE_URL}/logs", timeout=5)
                if res_logs.status_code == 200:
                    logs = res_logs.json().get("logs", [])
                    if not logs:
                        st.info("Bóveda vacía. No se registran eventos previos.")
                    for log in reversed(logs):
                        with st.expander(f" [{log.get('timestamp')}] ID #{log.get('id')} - {log.get('action')}"):
                            st.markdown(f"**Contenido Original Auditado:**\n{log.get('original_text')}")
                            st.markdown(f"**Resultado de la IA Guardado:**\n{log.get('ai_result')}")
                else:
                    st.error("No se pudo obtener el historial.")
            except Exception as e:
                st.error(f"Fallo de conexión con Audit Vault: {str(e)}")
import streamlit as st
st.set_page_config(
    layout="wide"
)
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: #0f172a;
            color: #ffffff;
        }

        h1, h2, h3, h4, h5, h6, p, span, div {
            color: #ffffff !important;
        }

        .stApp {
            background: linear-gradient(to right, #0f172a, #1e293b);
        }
    </style>
""", unsafe_allow_html=True)
import io
import pandas as pd
import datetime
import altair as alt
from typing import Tuple
from msal import ConfidentialClientApplication
import urllib.parse
import requests
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from msal import ConfidentialClientApplication
from streamlit_extras.stylable_container import stylable_container
from PIL import Image
from io import BytesIO
import base64

# --- ESTILOS PERSONALIZADOS ---
# Encabezado elegante con layout profesional (texto blanco sobre fondo oscuro)
# --- GLOBAL STYLING ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        background-color: #0f172a;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: linear-gradient(to right, #0f172a, #1e293b);
    }

    .block-container {
        padding: 2.5rem 5rem;
        max-width: 95%;
    }

    h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
        color: #ffffff;
    }

    h2 {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }

    h3 {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #cbd5e1;
    }

    p {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #e2e8f0;
        margin-top: 0.5rem;
        margin-bottom: 1.2rem;
    }

    /* Image logo styling */
    img {
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        max-width: 100%;
        height: auto;
    }

    /* Inputs */
    input, textarea {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #ffffff !important;
        border-radius: 6px;
        padding: 0.5rem;
        font-size: 0.95rem;
    }

    /* Sliders */
    .stSlider > div > div {
        background-color: #1e293b;
        border-radius: 8px;
        padding: 6px;
    }

    /* Buttons */
    button[kind="primary"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.6rem 1.4rem;
        box-shadow: 0 2px 10px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
    }

    button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
    }

    /* Micro-interactions */
    .element-container {
        transition: transform 0.2s ease;
    }

    .element-container:hover {
        transform: translateY(-3px);
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)
# --- LOAD LOGO ---
image = Image.open("NISQA.png")

# Ajusta el tamaño: más ancho que alto
resized_image = image.resize((340, 220))  # ← Aquí está el cambio

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
# --- CENTRAR LOGO EN EL APP ---
# --- Ajustar proporciones del logo (más ancho que alto) ---
resized_image = image.resize((340, 220))  # Más ancho que alto, evita compresión visual


# --- CENTRAR Y ESTILIZAR LOGO EN EL APP ---
st.markdown(
    f"""
    <div style="
        display: flex; 
        justify-content: center; 
        align-items: center; 
        margin: 2rem 0;
    ">
        <img 
            src="data:image/png;base64,{image_to_base64(resized_image)}" 
            width="340" 
            style="
                border: 2.5px solid rgba(255, 255, 255, 0.15);
                border-radius: 18px;
                padding: 8px;
                background: linear-gradient(145deg, #1e1e1e, #2c2c2c);
                box-shadow: 0 8px 28px rgba(0, 0, 0, 0.4), inset 0 0 6px rgba(255, 255, 255, 0.05);
            " 
        />
    </div>
    """,
    unsafe_allow_html=True
)

# --- HEADER SECTION ---
with stylable_container(
    key="header",
    css_styles="""
        border-radius: 16px;
        padding: 2rem;
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 2rem;
    """
):
    col1, col2 = st.columns([1, 6])

    with col2:
        st.markdown("""
        <div style="padding: 1rem 0;">
            <h3 style="
                font-weight: 400;
                font-size: 1.6rem;
                color: #f3f4f6;
                line-height: 1.5;
                letter-spacing: 0.4px;
                margin: 0;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            ">
                <span style="
                    font-weight: 700;
                    background: linear-gradient(to right, #bbf7d0, #86efac);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-size: 1.7rem;
                    transition: all 0.3s ease;
                ">
                    NISQA:
                </span>
                <span style="
                    display: inline-block; 
                    margin-left: 0.4rem;
                    color: #d1d5db;
                ">
                    Decodificamos Riesgo. Liberamos Crecimiento.
                </span>
            </h3>
        </div>
    """, unsafe_allow_html=True)


    # Aquí podrías colocar tus inputs, sliders, y visualizaciones:
    # st.number_input("Monto inicial", value=1000)
    # st.slider("Tasa de interés (%)", min_value=0.0, max_value=20.0, step=0.1)
    # st.line_chart(...)

# ------------------------- Configuration -------------------------
CLIENT_ID = "df0b1287-f8f7-4c89-bc34-bab9abadead8"
CLIENT_SECRET = "mbg8Q~iHwcHtsbJBu7v8q42oMPHfmZHR4QezHaL4"
TENANT_ID = "4322eb3a-d8ab-45a9-865b-475f3427324f"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = "http://localhost:8502"

LOGIN_SCOPES = ["User.Read", "email", "profile", "openid"]
TOKEN_SCOPES = ["User.Read"]

# ------------------------ MSAL App Setup -------------------------
app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
)

params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "response_mode": "query",
    "scope": " ".join(LOGIN_SCOPES)
}
login_url = f"{AUTHORITY}/oauth2/v2.0/authorize?{urllib.parse.urlencode(params)}"

# --------------------------- UI Layout ---------------------------
code = st.experimental_get_query_params().get("code", [None])[0]

with stylable_container(
    key="auth_card",
    css_styles="""
        background: linear-gradient(135deg, #f0f6ff, #ffffff);
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 120, 212, 0.15);
        border-left: 6px solid #0078D4;
        margin-top: 40px;
    """
):
    st.markdown("""
        <div style="display:flex; align-items:center; gap:15px;">
            <img src="https://img.icons8.com/color/48/000000/microsoft.png" width="48"/>
            <div>
                <h2 style="margin-bottom:0;">🔐 Inicia sesión con Microsoft Azure</h2>
                <p style="color:#444; margin-top:4px;">Acceso seguro para usuarios de <b>GPD Partners S.A.C.</b></p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if not code:
        st.markdown("### 👇 Autenticación necesaria para continuar:")
        st.markdown(
            f"""
            <div style="margin-top:20px;">
                <a href="{login_url}" style="text-decoration:none;">
                    <button style="
                        background-color:#0078D4;
                        color:white;
                        padding:12px 28px;
                        border:none;
                        border-radius:8px;
                        font-size:16px;
                        font-weight:bold;
                        cursor:pointer;
                        transition: background-color 0.3s ease;
                    " onmouseover="this.style.backgroundColor='#005a9e'" onmouseout="this.style.backgroundColor='#0078D4'">
                        🔐 Iniciar sesión con Microsoft
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------- OAuth Flow ---------------------------
if not code:
    st.markdown("### 👇 Haz clic para iniciar sesión:")
    st.markdown(
        f"<a href='{login_url}' style='text-decoration:none;'>"
        f"<button style='background-color:#0078D4; color:white; padding:10px 20px; border:none; border-radius:8px; font-size:16px;'>🔐 Iniciar sesión con Microsoft</button>"
        f"</a>",
        unsafe_allow_html=True
    )
else:
    with st.spinner("Autenticando con Azure..."):
        token_response = app.acquire_token_by_authorization_code(
            code=code,
            scopes=TOKEN_SCOPES,
            redirect_uri=REDIRECT_URI
        )

        if "access_token" in token_response:
            access_token = token_response["access_token"]
            user_info = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers={"Authorization": f"Bearer {access_token}"}
            ).json()

            display_name = user_info.get("displayName", "Desconocido")
            email = user_info.get("userPrincipalName", "No disponible")
            domain = email.split("@")[-1]

            st.success("✅ Autenticado correctamente")

            with stylable_container(
                key="user_card",
                css_styles="""
                    border: 2px solid #0078D4;
                    border-radius: 12px;
                    padding: 20px;
                    margin-top: 20px;
                    background-color: #f3f9ff;
                    box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
                """
            ):
                st.markdown(f"### 👤 Bienvenido, **{display_name}**")
                st.markdown(f"📧 **Correo corporativo:** {email}")
                st.markdown("🏢 **Organización detectada: GPD Partners S.A.C.**")

            if domain.lower() != "gpdpartners.pe":
                st.warning("⚠️ Tu correo no pertenece a la organización GPD Partners S.A.C.")
        else:
            st.error("❌ Error durante la autenticación")
            st.json(token_response)
            
# --------------------- HELPERS ---------------------

class FechaHelper:
    """Funciones estáticas para manejo de fechas."""

    @staticmethod
    def dias_entre(f1: datetime.date, f2: datetime.date) -> int:
        """Devuelve número de días entre f1 y f2 (f2 - f1)."""
        return max((f2 - f1).days, 0)


# --------------------- CORE FINANCIAL LOGIC ---------------------

class InteresFinanciero:
    """Cálculo de intereses compensatorios, moratorios y cálculo total con IGV."""

    def __init__(
        self,
        monto: float,
        tasa_compensatoria: float,
        tasa_moratoria: float,
        igv: float = 0.18,
    ):
        self.monto = monto
        self.tasa_c = tasa_compensatoria
        self.tasa_m = tasa_moratoria
        self.igv = igv

    def calcular_interes_I(self, fecha_inicio: datetime.date, fecha_vencimiento: datetime.date) -> Tuple[float, int]:
        dias = FechaHelper.dias_entre(fecha_inicio, fecha_vencimiento)
        if dias <= 0:
            return 0.0, 0
        interes = ((1 + self.tasa_c) ** (dias / 30) - 1) * self.monto
        return interes, dias

    def calcular_interes_II_y_mora(
        self,
        fecha_vencimiento: datetime.date,
        fecha_pago: datetime.date,
        interes_I: float,
    ) -> Tuple[float, float, int]:
        if fecha_pago <= fecha_vencimiento:
            return 0.0, 0.0, 0
        dias = FechaHelper.dias_entre(fecha_vencimiento, fecha_pago)
        base = self.monto + interes_I
        interes_II = ((1 + self.tasa_c) ** (dias / 30) - 1) * base
        interes_mora = ((1 + self.tasa_m) ** (dias / 30) - 1) * base
        return interes_II, interes_mora, dias

    def calcular_totales(
        self,
        interes_I: float,
        interes_II: float,
        interes_mora: float,
    ) -> Tuple[float, float, float, float]:
        total_sin_igv = interes_I + interes_II
        igv_calc = total_sin_igv * self.igv
        total_con_igv = total_sin_igv + igv_calc
        total = total_con_igv + interes_mora
        return total_sin_igv, igv_calc, total_con_igv, total


class ReporteDinamico:
    """
    Genera reporte diario detallado de intereses: I, II y moratorio.
    Devuelve DataFrame con fechas y desglose diario.
    """

    def __init__(
        self,
        fecha_inicio: datetime.date,
        fecha_vencimiento: datetime.date,
        fecha_pago: datetime.date,
        interes_I: float,
        interes_II: float,
        interes_mora: float,
        dias_I: int,
        dias_II: int,
    ):
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.fecha_pago = fecha_pago
        self.interes_I = interes_I
        self.interes_II = interes_II
        self.interes_mora = interes_mora
        self.dias_I = dias_I
        self.dias_II = dias_II

    def generar(self) -> Tuple[pd.DataFrame, float, float, float]:
        i_dia_I = round(self.interes_I / self.dias_I, 6) if self.dias_I > 0 else 0.0
        i_dia_II = round(self.interes_II / self.dias_II, 6) if self.dias_II > 0 else 0.0
        i_dia_mora = round(self.interes_mora / self.dias_II, 6) if self.dias_II > 0 else 0.0

        filas = []
        fecha_actual = self.fecha_inicio

        # Periodo Interés I
        while fecha_actual < self.fecha_vencimiento:
            filas.append({
                "Fecha": fecha_actual,
                "Interés Diario I": i_dia_I,
                "Interés Diario II": 0.0,
                "Interés Moratorio": 0.0,
                "Total Diario": i_dia_I,
            })
            fecha_actual += datetime.timedelta(days=1)

        # Periodo Interés II y Mora
        while fecha_actual < self.fecha_pago:
            total_diario = round(i_dia_II + i_dia_mora, 6)
            filas.append({
                "Fecha": fecha_actual,
                "Interés Diario I": 0.0,
                "Interés Diario II": i_dia_II,
                "Interés Moratorio": i_dia_mora,
                "Total Diario": total_diario,
            })
            fecha_actual += datetime.timedelta(days=1)

        df = pd.DataFrame(filas)
        # Convert "Fecha" column to datetime64 type before using dt accessor
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df["Fecha"] = df["Fecha"].dt.strftime("%d/%m/%Y")
        return df, i_dia_I, i_dia_II, i_dia_mora

class OvernightCalculator:
    """Cálculo de interés overnight."""

    def __init__(
        self,
        monto: float,
        tasa_anual: float,
        fecha_inicio: datetime.date,
        fecha_vencimiento: datetime.date,
    ):
        self.monto = monto
        self.tasa = tasa_anual
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento

    def calcular(self) -> Tuple[float, float, int]:
        dias = FechaHelper.dias_entre(self.fecha_inicio, self.fecha_vencimiento)
        if dias <= 0:
            return 0.0, 0.0, 0
        interes_total = ((1 + self.tasa) ** (dias / 360) - 1) * self.monto
        interes_diario = interes_total / dias
        return interes_total, interes_diario, dias


# --------------------- STREAMLIT UI ---------------------

def main():

    # CSS para mejor apariencia
    st.markdown(
        """
        <style>
            .css-18e3th9 {
                padding: 1rem 3rem;
            }
            .css-1d391kg {
                padding-left: 3rem;
                padding-right: 3rem;
            }
            footer {
                visibility: hidden;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("📊 Simulador de Intereses Financieros Diarios")
    st.markdown(
        "Calcule intereses compensatorios, moratorios e IGV con detalle diario y visualizaciones interactivas."
    )

    # Sidebar con inputs
    with st.sidebar:
        st.header("🧾 Parámetros del cálculo")

        contrato = st.text_input(
            "📄 # Contrato Cliente (CE)",
            placeholder="Ej.: POST 114",
            help="Identificador único del contrato",
        )
        descripcion = st.text_input(
            "📝 Descripción de la operación",
            placeholder="Ej.: FE01 1423",
            help="Descripción breve del préstamo o financiamiento",
        )

        with st.expander("Fechas importantes"):
            fecha_inicio = st.date_input(
                "📅 Fecha de inicio",
                datetime.date.today() - datetime.timedelta(days=60),
                help="Fecha desde la que comienza el cálculo del interés",
            )
            fecha_vencimiento = st.date_input(
                "📅 Fecha de vencimiento",
                datetime.date.today() - datetime.timedelta(days=30),
                help="Fecha límite para pago sin mora",
            )
            fecha_pago = st.date_input(
                "📅 Fecha de pago",
                datetime.date.today(),
                help="Fecha efectiva de pago",
            )

        with st.expander("Montos y Tasas"):
            monto = st.number_input(
                "💵 Monto financiado (USD)",
                min_value=0.01,
                format="%.2f",
                help="Monto total financiado",
            )
            tasa_c_pct = st.number_input(
                "📈 Tasa compensatoria mensual (%)",
                min_value=0.0,
                max_value=100.0,
                value=3.0,
                format="%.2f",
                help="Tasa de interés compensatoria mensual (ejemplo: 3%)",
            )
            tasa_m_pct = st.number_input(
                "⚠️ Tasa moratoria mensual (%)",
                min_value=0.0,
                max_value=100.0,
                value=6.0,
                format="%.2f",
                help="Tasa de interés moratoria mensual (ejemplo: 6%)",
            )
            igv_pct = st.number_input(
                "🧾 IGV (%)",
                min_value=0.0,
                max_value=100.0,
                value=18.0,
                format="%.2f",
                help="Impuesto general a las ventas",
            )

    # Validar fechas coherentes
    if fecha_vencimiento < fecha_inicio:
        st.error("❌ La fecha de vencimiento no puede ser anterior a la fecha de inicio.")
        return
    if fecha_pago < fecha_vencimiento:
        st.warning("⚠️ La fecha de pago es anterior a la fecha de vencimiento.")

    # Crear instancia y calcular
    interes = InteresFinanciero(
        monto=monto,
        tasa_compensatoria=tasa_c_pct / 100,
        tasa_moratoria=tasa_m_pct / 100,
        igv=igv_pct / 100,
    )

    interes_I, dias_I = interes.calcular_interes_I(fecha_inicio, fecha_vencimiento)
    interes_II, interes_mora, dias_II = interes.calcular_interes_II_y_mora(
        fecha_vencimiento, fecha_pago, interes_I
    )
    total_sin_igv, igv_calc, total_con_igv, total = interes.calcular_totales(
        interes_I, interes_II, interes_mora
    )

    # Mostrar resultados generales
    st.subheader("💡 Resultados Generales")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Interés Compensatorio I",
        f"US$ {interes_I:,.2f}",
        f"{dias_I} días",
    )
    col2.metric(
        "Interés Compensatorio II",
        f"US$ {interes_II:,.2f}",
        f"{dias_II} días",
    )
    col3.metric(
        "Interés Moratorio",
        f"US$ {interes_mora:,.2f}",
        f"{dias_II} días",
    )
    col4.metric(
        "Total (con IGV)",
        f"US$ {total:,.2f}",
        f"IGV: US$ {igv_calc:,.2f}",
    )

    # Generar reporte detallado diario
    reporte = ReporteDinamico(
        fecha_inicio,
        fecha_vencimiento,
        fecha_pago,
        interes_I,
        interes_II,
        interes_mora,
        dias_I,
        dias_II,
    )
    df_reporte, i_dia_I, i_dia_II, i_dia_mora = reporte.generar()

    # Mostrar DataFrame detallado
    with st.expander("🔍 Ver detalle diario de intereses"):
        st.dataframe(df_reporte.style.format({
            "Interés Diario I": "${:,.6f}",
            "Interés Diario II": "${:,.6f}",
            "Interés Moratorio": "${:,.6f}",
            "Total Diario": "${:,.6f}",
        }))

    # Gráfica interactiva con Altair
    chart = (
        alt.Chart(df_reporte)
        .transform_fold(
            ["Interés Diario I", "Interés Diario II", "Interés Moratorio"],
            as_=["Tipo", "Monto"],
        )
        .mark_area(opacity=0.6)
        .encode(
            x=alt.X("Fecha:T", title="Fecha"),
            y=alt.Y("Monto:Q", stack="zero", title="Interés Diario (USD)"),
            color=alt.Color("Tipo:N", scale=alt.Scale(scheme="set1")),
            tooltip=[
                alt.Tooltip("Fecha:T", title="Fecha"),
                alt.Tooltip("Monto:Q", format=".6f", title="Interés Diario"),
                alt.Tooltip("Tipo:N", title="Tipo de Interés"),
            ],
        )
        .properties(width=900, height=400)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)
# --------------------- OVERNIGHT CALCULATOR ---------------------
    st.subheader("🌙 Calculadora de Interés Overnight")

    with st.expander("➕ Calcular interés overnight adicional"):
        st.markdown("Usa esta sección para calcular interés compuesto por un periodo determinado con tasa anual.")

        monto_overnight = st.number_input(
            "💵 Monto base (USD) - Overnight",
            min_value=0.01,
            format="%.2f",
            help="Monto sobre el que se calcula el interés overnight",
            key="monto_overnight"
        )
        tasa_anual_overnight = st.number_input(
            "📈 Tasa anual compuesta (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            format="%.2f",
            help="Tasa anual de interés compuesta (ej. 5%)",
            key="tasa_anual_overnight"
        )
        fecha_inicio_overnight = st.date_input(
            "📅 Fecha de inicio - Overnight",
            datetime.date.today() - datetime.timedelta(days=7),
            key="fecha_inicio_overnight"
        )
        fecha_final_overnight = st.date_input(
            "📅 Fecha final - Overnight",
            datetime.date.today(),
            key="fecha_final_overnight"
        )

        if fecha_final_overnight < fecha_inicio_overnight:
            st.error("❌ La fecha final debe ser posterior a la fecha de inicio.")
        else:
            calc_overnight = OvernightCalculator(
                monto=monto_overnight,
                tasa_anual=tasa_anual_overnight / 100,
                fecha_inicio=fecha_inicio_overnight,
                fecha_vencimiento=fecha_final_overnight,
            )
            interes_total_overnight, interes_diario_overnight, dias_overnight = calc_overnight.calcular()

            st.success(f"✅ Interés total overnight: **US$ {interes_total_overnight:,.2f}** en {dias_overnight} días")
            st.caption(f"Interés diario promedio: US$ {interes_diario_overnight:,.6f}")
    # --- NUEVA SECCIÓN: Cálculo Valor Cuota Diario Neto ---
    st.markdown("---")
    st.title("🧮 Cálculo del Valor Cuota Diario Neto (USD) - Múltiples Fechas")

    if "fechas_data" not in st.session_state:
        st.session_state.fechas_data = []

    with st.form(key="formulario_fecha"):
        st.subheader("📅 Ingreso de datos para una fecha específica")
        fecha = st.date_input("Selecciona la Fecha")

        total_ingresos = st.number_input("💰 Total Ingresos para la fecha (USD)", min_value=0.0, format="%.2f")
        total_gastos = st.number_input("💸 Total Gastos para la fecha (USD)", min_value=0.0, format="%.2f")

        resultado_diario = total_ingresos - total_gastos
        st.write(f"➡️ **Resultado Diario (Ingresos - Gastos): USD {resultado_diario:,.2f}**")

        patrimonio_inicial = st.number_input("🏦 Patrimonio Inicial hasta esta fecha (USD)", min_value=0.0, format="%.2f")
        aporte_participe = st.number_input("👤 Aporte del Partícipe (USD, si no hay, escribir 0)", min_value=0.0, format="%.2f")

        patrimonio_final = patrimonio_inicial + resultado_diario + aporte_participe
        st.write(f"➡️ **Patrimonio Final = {patrimonio_inicial:,.2f} + {resultado_diario:,.2f} + {aporte_participe:,.2f} = USD {patrimonio_final:,.2f}**")

        cantidad_cuotas = st.number_input("🔢 Cantidad de Cuotas Finales para la fecha", min_value=0.000001, format="%.6f")
        valor_cuota = patrimonio_final / cantidad_cuotas if cantidad_cuotas > 0 else 0.0

        st.write(f"✅ **Valor Cuota Diario Neto para {fecha.strftime('%d/%m/%Y')}: USD {valor_cuota:,.6f}**")

        submitted = st.form_submit_button("✅ Agregar esta fecha a la tabla")

        if submitted:
            st.session_state.fechas_data.append({
                "Fecha": fecha.strftime("%d/%m/%Y"),
                "Total Ingresos (USD)": total_ingresos,
                "Total Gastos (USD)": total_gastos,
                "Resultado Diario (USD)": resultado_diario,
                "Patrimonio Inicial (USD)": patrimonio_inicial,
                "Aporte Partícipe (USD)": aporte_participe,
                "Patrimonio Final (USD)": patrimonio_final,
                "Cantidad Cuotas": cantidad_cuotas,
                "Valor Cuota Diario Neto (USD)": valor_cuota
            })
            st.success("✔️ Datos agregados correctamente.")

    if st.session_state.fechas_data:
        df = pd.DataFrame(st.session_state.fechas_data)
        st.markdown("### 📊 Tabla Consolidada por Fecha")
        st.dataframe(df.style.format({"Valor Cuota Diario Neto (USD)": "{:.6f}"}))

    # Botón para descargar el Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        df_reporte.to_excel(writer, index=False, sheet_name="Detalle diario")

    st.download_button(
        label="📥 Descargar Reporte en Excel",
        data=excel_buffer.getvalue(),
        file_name=f"reporte_{contrato or 'simulacion'}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    main()                     # Ejecuta la lógica del simulador de intereses.
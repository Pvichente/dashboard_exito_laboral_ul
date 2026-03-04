import re
import pandas as pd
import streamlit as st

# ----------------------------
# Config
# ----------------------------
st.set_page_config(
    page_title="Dashboard Éxito Laboral | UL",
    layout="wide",
)

DATA_PATH = "base de resultados de Perfil Laboral.xlsx"

YES_SET = {"SI", "SÍ", "Si", "Sí", "YES", "Y"}

# ----------------------------
# Helpers
# ----------------------------
def to_yes_no(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    return "SI" if s in YES_SET else "NO"

def parse_salary_midpoint(s):
    """
    Convierte rangos tipo:
      - "De $15,000 a $29,999" -> 22500 aprox.
      - "Más de $100,000" -> 110000 (proxy)
    """
    if pd.isna(s):
        return None
    s = str(s).strip()

    if "Más de" in s:
        nums = re.findall(r"[\d,]+", s)
        if nums:
            base = int(nums[0].replace(",", ""))
            return int(base * 1.1)  # proxy
        return None

    m = re.search(r"De\s*\$([\d,]+)\s*a\s*\$([\d,]+)", s)
    if m:
        lo = int(m.group(1).replace(",", ""))
        hi = int(m.group(2).replace(",", ""))
        return int((lo + hi) / 2)

    return None

@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=0)
    df.columns = [c.strip() for c in df.columns]

    # Normalizar SI/NO
    for c in [
        "TuvoExperienciaPrevia",
        "TrabajaActualmente",
        "BuscaCapitalFondeo",
        "BuscaTrabajoActualmente",
        "TieneAreaInteres",
    ]:
        if c in df.columns:
            df[c] = df[c].apply(to_yes_no)

    # Derivado: emprendimiento
    df["TieneEmprendimiento"] = (
        (df.get("EstatusLaboralActual") == "Tenía/Tengo un emprendimiento")
        | (df.get("EstatusLaboralPrevio") == "Tenía/Tengo un emprendimiento")
        | (df.get("FaseEmprendimiento").notna())
        | (df.get("GiroEmprendimiento").notna())
    )

    # Midpoints de salario (para ordenar)
    df["SalarioActualMid"] = (
        df["RangoSalarialActual"].apply(parse_salary_midpoint)
        if "RangoSalarialActual" in df.columns
        else None
    )

    return df

def safe_unique(df, col):
    if col not in df.columns:
        return []
    return sorted([x for x in df[col].dropna().unique()])

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros")

    q = st.sidebar.text_input("Buscar (matrícula o nombre)", "").strip().lower()

    trabaja_opts = safe_unique(df, "TrabajaActualmente")
    trabaja = st.sidebar.multiselect(
        "Trabaja actualmente",
        options=trabaja_opts,
        default=trabaja_opts,
    )

    estatus_opts = safe_unique(df, "EstatusLaboralActual")
    estatus = st.sidebar.multiselect(
        "Estatus laboral actual",
        options=estatus_opts,
        default=estatus_opts,
    )

    tiene_empr = st.sidebar.multiselect(
        "Tiene emprendimiento (derivado)",
        options=["Sí", "No"],
        default=["Sí", "No"],
    )

    busca_trab_opts = safe_unique(df, "BuscaTrabajoActualmente")
    busca_trab = st.sidebar.multiselect(
        "Busca trabajo actualmente",
        options=busca_trab_opts,
        default=busca_trab_opts,
    )

    busca_cap_opts = safe_unique(df, "BuscaCapitalFondeo")
    busca_cap = st.sidebar.multiselect(
        "Busca capital / fondeo",
        options=busca_cap_opts,
        default=busca_cap_opts,
    )

    sal_opts = safe_unique(df, "RangoSalarialActual")
    sal = st.sidebar.multiselect(
        "Rango salarial actual",
        options=sal_opts,
        default=sal_opts,
    )

    giro_trab_opts = safe_unique(df, "GiroTrabajoActual")
    giro_trab = st.sidebar.multiselect(
        "Giro trabajo actual",
        options=giro_trab_opts,
        default=giro_trab_opts,
    )

    giro_empr_opts = safe_unique(df, "GiroEmprendimiento")
    giro_empr = st.sidebar.multiselect(
        "Giro emprendimiento",
        options=giro_empr_opts,
        default=giro_empr_opts,
    )

    industria_busq_opts = safe_unique(df, "IndustriaBusqueda")
    industria_busq = st.sidebar.multiselect(
        "Industria de búsqueda",
        options=industria_busq_opts,
        default=industria_busq_opts,
    )

    industria_int_opts = safe_unique(df, "IndustriaInteres")
    industria_int = st.sidebar.multiselect(
        "Industria de interés",
        options=industria_int_opts,
        default=industria_int_opts,
    )

    out = df.copy()

    if q:
        out = out[
            out["Matricula"].astype(str).str.lower().str.contains(q, na=False)
            | out["Estudiante"].astype(str).str.lower().str.contains(q, na=False)
        ]

    if trabaja:
        out = out[out["TrabajaActualmente"].isin(trabaja)]

    if estatus:
        out = out[out["EstatusLaboralActual"].isin(estatus) | out["EstatusLaboralActual"].isna()]

    empr_mask = out["TieneEmprendimiento"].map(lambda x: "Sí" if bool(x) else "No")
    out = out[empr_mask.isin(tiene_empr)]

    if busca_trab:
        out = out[out["BuscaTrabajoActualmente"].isin(busca_trab)]

    if busca_cap:
        out = out[out["BuscaCapitalFondeo"].isin(busca_cap)]

    if sal:
        out = out[out["RangoSalarialActual"].isin(sal) | out["RangoSalarialActual"].isna()]

    if giro_trab:
        out = out[out["GiroTrabajoActual"].isin(giro_trab) | out["GiroTrabajoActual"].isna()]

    if giro_empr:
        out = out[out["GiroEmprendimiento"].isin(giro_empr) | out["GiroEmprendimiento"].isna()]

    if industria_busq:
        out = out[out["IndustriaBusqueda"].isin(industria_busq) | out["IndustriaBusqueda"].isna()]

    if industria_int:
        out = out[out["IndustriaInteres"].isin(industria_int) | out["IndustriaInteres"].isna()]

    return out

def download_csv(df: pd.DataFrame, filename="perfil_laboral_filtrado.csv"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar CSV filtrado", csv, file_name=filename, mime="text/csv")

# ----------------------------
# App
# ----------------------------
st.title("Dashboard | Perfil laboral de estudiantes (UL)")
st.caption("Análisis interactivo de empleabilidad, emprendimiento y búsqueda de empleo.")

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"No encontré el archivo en `{DATA_PATH}`.\n\n"
        "Crea la carpeta `data/` y sube el Excel con el nombre `perfil_laboral_ul.xlsx` "
        "o actualiza la variable `DATA_PATH`."
    )
    st.stop()

df_f = apply_filters(df)

# KPIs
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Estudiantes (base)", len(df))
with c2:
    st.metric("Estudiantes (filtrado)", len(df_f))
with c3:
    pct_work = (df_f["TrabajaActualmente"].eq("SI").mean() * 100) if len(df_f) else 0
    st.metric("% trabaja (filtrado)", f"{pct_work:.1f}%")
with c4:
    pct_empr = (df_f["TieneEmprendimiento"].mean() * 100) if len(df_f) else 0
    st.metric("% con emprendimiento (filtrado)", f"{pct_empr:.1f}%")

st.divider()

# Gráficas
g1, g2, g3 = st.columns(3)
with g1:
    st.subheader("Estatus laboral actual")
    vc = df_f["EstatusLaboralActual"].fillna("No responde").value_counts()
    st.bar_chart(vc)

with g2:
    st.subheader("Rango salarial actual")
    vc = df_f["RangoSalarialActual"].fillna("No responde").value_counts()
    st.bar_chart(vc)

with g3:
    st.subheader("Busca trabajo actualmente")
    vc = df_f["BuscaTrabajoActualmente"].fillna("No responde").value_counts()
    st.bar_chart(vc)

st.divider()

# Tabla
st.subheader("Tabla de estudiantes (filtrada)")

default_cols = [
    "Matricula", "Estudiante",
    "TrabajaActualmente", "EstatusLaboralActual", "GiroTrabajoActual", "RangoSalarialActual",
    "TieneEmprendimiento", "FaseEmprendimiento", "GiroEmprendimiento", "BuscaCapitalFondeo",
    "BuscaTrabajoActualmente", "IndustriaBusqueda",
    "TieneAreaInteres", "IndustriaInteres",
    "RetosPrincipalesTrabajo", "Habilidades", "Herramientas",
]

available_cols = [c for c in default_cols if c in df_f.columns]
cols_show = st.multiselect("Columnas a mostrar", options=df_f.columns.tolist(), default=available_cols)

sort_col = st.selectbox("Ordenar por", options=["(sin ordenar)", "Estudiante", "Matricula", "SalarioActualMid"])
if sort_col != "(sin ordenar)" and sort_col in df_f.columns:
    df_f = df_f.sort_values(sort_col, ascending=True, na_position="last")

st.dataframe(df_f[cols_show], use_container_width=True, height=520)
download_csv(df_f[cols_show])

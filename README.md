# Dashboard de Éxito Laboral  
### Universidad de la Libertad

Este repositorio contiene una aplicación interactiva desarrollada en **Python y Streamlit** para analizar la información del **Perfil Laboral de los estudiantes de la Universidad de la Libertad (UL)**.

El objetivo del dashboard es facilitar la **visualización, exploración y análisis de datos laborales de los estudiantes**, permitiendo identificar patrones de empleabilidad, emprendimiento y desarrollo profesional que apoyen la **toma de decisiones institucionales**.

---

# Objetivo del proyecto

La Universidad de la Libertad busca comprender mejor la **situación laboral y profesional de sus estudiantes**, incluyendo aspectos como:

- Participación en el mercado laboral
- Nivel salarial
- Desarrollo de emprendimientos
- Intereses profesionales
- Búsqueda activa de empleo
- Necesidades de capacitación

Este dashboard permite **analizar estos datos de forma interactiva** y detectar oportunidades para mejorar programas de:

- Vinculación laboral
- Desarrollo profesional
- Apoyo al emprendimiento
- Formación de habilidades relevantes para el mercado laboral

---

# Funcionalidades del dashboard

La aplicación permite explorar la base de datos del perfil laboral mediante:

## Visualización de indicadores clave

El dashboard muestra gráficos y estadísticas sobre:

- Estatus laboral actual de los estudiantes
- Distribución de rangos salariales
- Porcentaje de estudiantes que trabajan
- Estudiantes que buscan empleo
- Participación en emprendimientos

---

## Sistema de filtros interactivos

Los usuarios pueden filtrar la información por variables como:

- Trabaja actualmente
- Estatus laboral
- Emprendimiento activo
- Búsqueda de empleo
- Búsqueda de capital o fondeo
- Giro de trabajo
- Giro de emprendimiento
- Industria de interés

Esto permite analizar **subgrupos específicos de estudiantes** y detectar patrones relevantes.

---

## Tabla dinámica de estudiantes

Una funcionalidad central del dashboard es la visualización de una **tabla interactiva con los estudiantes que cumplen ciertos criterios**.

Esto permite identificar rápidamente casos como:

- Estudiantes que **no trabajan pero buscan empleo**
- Estudiantes que **tienen emprendimiento y buscan capital**
- Estudiantes que **ya trabajan pero buscan mejorar su empleo**
- Estudiantes interesados en **industrias específicas**

La tabla puede exportarse para análisis adicionales.

---

# Tecnologías utilizadas

Este proyecto utiliza las siguientes herramientas:

- **Python**
- **Streamlit**
- **Pandas**
- **OpenPyXL**

Streamlit permite construir dashboards interactivos de forma rápida y ligera utilizando Python.

---

# Estructura del repositorio

dashboard_exito_laboral_ul
│
├── app.py
├── requirements.txt
├── README.md
│
├── data
│ └── perfil_laboral_ul.xlsx
│
└── .gitignore

---

# Instalación

Clonar el repositorio:

```bash
git clone https://github.com/tu_usuario/dashboard_exito_laboral_ul.git
cd dashboard_exito_laboral_ul

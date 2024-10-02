import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos desde el archivo Excel
file_path = 'supermarkt_sales.xlsx'  # Cambia 'supermarkt_sales.xlsx' por la ruta real de tu archivo
df = pd.read_excel(file_path, sheet_name='Sales', header=3)

# Limpiar la columna 'Date'
df['Date'] = pd.to_datetime(df['Date'])

# Título de la aplicación interactiva
st.write("""
# City vs Product Line con Distribución por Género
Esta aplicación permite visualizar las ventas por ciudad y línea de producto, junto con la distribución por género.
""")

# Usar el panel lateral para opciones
with st.sidebar:
    # Seleccionar el rango de fechas
    st.write("## Filtro de fechas")
    start_date = st.date_input('Fecha de inicio', df['Date'].min())
    end_date = st.date_input('Fecha de fin', df['Date'].max())
    
    # Filtrar el DataFrame por el rango de fechas seleccionado
    df_filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
    
    # Seleccionar la ciudad
    city = st.selectbox('Seleccionar ciudad:', df_filtered['City'].unique())
    
    # Filtrar los datos por ciudad seleccionada
    df_filtered_city = df_filtered[df_filtered['City'] == city]
    
    # Slider para seleccionar el número de bins
    num_bins = st.slider('Número de bins:', 10, 100, 20)
    st.write("Bins =", num_bins)

# Agrupar los datos por 'Product line'
grouped_data = df_filtered_city.groupby(['Product line']).size()

# Agrupar los datos por 'Gender'
gender_data = df_filtered_city['Gender'].value_counts()

# Crear la figura para los gráficos
fig, ax = plt.subplots(1, 2, figsize=(15, 6))

# Gráfico principal (Product line para la ciudad seleccionada)
grouped_data.plot(kind='bar', ax=ax[0], color='coral')
ax[0].set_title(f'Ventas por Línea de Producto en {city}')
ax[0].set_xlabel('Línea de Producto')
ax[0].set_ylabel('Cantidad de Productos')

# Gráfico secundario (Histograma de Gender)
ax[1].hist(df_filtered_city['Gender'], bins=num_bins, color='lightblue')
ax[1].set_title('Distribución de Género')
ax[1].set_xlabel('Género')
ax[1].set_ylabel('Frecuencia')

# Mostrar los gráficos en Streamlit
st.pyplot(fig)

# Mostrar una tabla de muestra de datos filtrados
st.write("""
## Muestra de datos cargados
""")
st.table(df_filtered_city.head())

#intale en la terminal 
#pip install pandas matplotlib streamlit
#streamlit run myapp.py--> nombre de sChao archivo .py
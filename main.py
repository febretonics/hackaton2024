try:
    from enum import Enum
    from io import BytesIO, StringIO
    from typing import Union

    import pandas as pd
    import streamlit as st
    import requests
    import base64
except Exception as e:
    print(e)


st.set_page_config(layout="wide", page_title="FPI IMAGE ANALYZER")

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

# Función para incrustar imagen como base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

class FileUpload(object):

    def __init__(self):
        self.fileTypes = ["csv", "png", "jpg"]

    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.info(__doc__)
        st.markdown(STYLE, unsafe_allow_html=True)

        
        logo_path = "logoBoeh.png"  # Ruta del logotipo

        # Convertir el logotipo a base64
        logo_base64 = get_image_as_base64(logo_path)

        # Barra personalizada
        custom_bar_html = f"""
            <style>
                .custom-bar {{
             display: flex;
             justify-content: space-between;
                align-items: center;
                height: 60px;
                background-color: #1e1e1e; /* Color de fondo */
             padding: 0 20px;
                color: green;
                font-family: Arial, sans-serif;
                font-size: 40px;
                font-weight: bold;
         }}
            .custom-bar img {{
            height: 70px; /* Tamaño del logo */
            }}
        </style>
        <div class="custom-bar">
        <div>FPI IMAGE ANALYZER</div>
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
        </div>
        """
         # Insertar la barra personalizada
        st.markdown(custom_bar_html, unsafe_allow_html=True)
        #st.markdown(logo_html, unsafe_allow_html=True)

        # Título
        st.title("ADQUISICION DE DATOS")

        # Informacion personal
        st.write("### INFORMACION PERSONAL DEL PACIENTE")

        c3,c4 = st.columns([1,1])
        with c3:
            pname = st.text_input("Nombre")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            weight = st.text_input("Peso")
            
            
            
        with c4:
            psurname = st.text_input("Apellidos")
            height = st.text_input("Altura")
            sip = st.text_input("Numero de SIP")
            

        # Campos de entrada
        st.write("### INFORMACION PATOLOGICA DEL PACIENTE")
        # Carga de archivo
        file = st.file_uploader("Subir archivo", type=["csv", "png", "jpg"])

        c1,c2 = st.columns([1,1])
        with c1:
            fvc = st.text_input("FVC - the recorded lung capacity in ml")
            fvc_percent = st.text_input("Percent - FVC as a percent of the typical FVC for a person of similar characteristics")
            
        with c2:
            sex = st.text_input("Sex")
            smoking = st.text_input("Smoking")

        # Botón de envío general
        if st.button("SEND"):
            # Validar datos ingresados
            if not fvc or not fvc_percent or not sex or not smoking or not pname or not psurname or not weight or not height:
                st.error("Por favor, completa todos los campos del formulario.")
            elif file is None:
                st.error("Por favor, sube un archivo.")
            else:

                # Datos a enviar a la API
                data = {
                    "fvc": fvc,
                    "fvc_percent": fvc_percent,
                    "age": age,
                    "sex": sex,
                    "smoking": smoking,
                    "pname": pname,
                    "psurname": psurname,
                    "age": age,
                    "weight": weight,
                    "height": height,
                }
                # Archivo cargado
                if file is not None:
                    file.seek(0)  
                
                # Reinicia el puntero del archivo
                    file_data = {"file": (file.name, file, file.type)}
                else:
                    file_data = None

                # Enviar a la API
                api_url = "https://your-api-endpoint.com/process"  # Cambia esta URL
                response = self.send_to_api(api_url, data, file=file_data)

                # Mostrar respuesta
                if isinstance(response, dict) and "error" in response:
                    st.error(f"Error al enviar datos: {response['error']}")
                else:
                    st.success("¡Datos enviados con éxito!")
                    st.write("### Respuesta de la API:")
                    st.write(response.json())

                # Mostrar resultados del formulario
                st.success("¡Datos enviados con éxito!")
                st.write("### Información proporcionada:")
                st.write("### Información proporcionada:")
                st.write(f"- **FVC (Capacidad Pulmonar):** {fvc} ml")
                st.write(f"- **FVC como porcentaje del típico:** {fvc_percent}%")
                st.write(f"- **Edad:** {age}")
                st.write(f"- **Sexo:** {sex}")
                st.write(f"- **Fumador:** {smoking}")


                # Procesar el archivo cargado
                if isinstance(file, BytesIO):
                    # Crear dos columnas para mostrar la imagen
                    col1, col2 = st.columns(2)

                    # Ancho deseado para las imágenes (por ejemplo, 300 píxeles de ancho)
                    img_width = 300

                    with col1:
                        st.image(file, caption="Imagen 1 (lado izquierdo)", width=img_width)

                    with col2:
                        st.image(file, caption="Imagen 2 (lado derecho)", width=img_width)
                else:
                    data = pd.read_csv(file)
                    st.write("### Contenido del archivo CSV:")
                    st.dataframe(data.head(10))

                file.close()

        # if isinstance(file, BytesIO):
        #     show_file.image(file)
        # else:
        #     data = pd.read_csv(file)
        #     st.dataframe(data.head(10))
        


if __name__ == "__main__":
    helper = FileUpload()
    helper.run()
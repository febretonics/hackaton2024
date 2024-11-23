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


st.set_page_config(layout="wide", page_title="Lung Anomaly Detection APP")
     
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

    def send_to_api(self, url, data, file=None):
        """
        Envía los datos y el archivo cargado a una API
        :param url: Endpoint de la API
        :param data: Diccionario con los datos del formulario
        :param file: Archivo a enviar (opcional)
        :return: Respuesta de la API
        """
        try:
            files = {'file': file} if file else None
            response = requests.post(url, data=data, files=files)
            return response
        except Exception as e:
            return {"error": str(e)}

    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        
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
                background-color: #abebc6 ; /* Color de fondo */
             padding: 0 20px;
                color: black;
                font-family: Arial, sans-serif;
                font-size: 40px;
                font-weight: bold;
         }}
            .custom-bar img {{
            height: 50px; /* Tamaño del logo */
            }}
        </style>
        <div class="custom-bar">
        <div>Lung Anomaly Detection APP</div>
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
        </div>
        """
         # Insertar la barra personalizada
        st.markdown(custom_bar_html, unsafe_allow_html=True)
        #st.markdown(logo_html, unsafe_allow_html=True)

        # Título
        st.title("DATA ACQUISITION")

        # Informacion personal
        st.write("### PERSONAL PATIENT INFORMATION")

        c3,c4 = st.columns([1,1])
        with c3:
            pname = st.text_input("Name")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            weight = st.text_input("Weigth")
            
            
            
        with c4:
            psurname = st.text_input("Surnames")
            height = st.text_input("Height")
            sip = st.text_input("SIP Number")
            

        # Campos de entrada
        st.write("### PATHOLOGICAL PATIENT INFORMATION")
        # Carga de archivo
        file = st.file_uploader("Upload File", type=["csv", "png", "jpg"])

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
                st.error("Please complete all fields in the form")
            elif file is None:
                st.error("Please upload a file.")
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
                    "sip": sip,
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
                    st.error(f"Error sending data: {response['error']}")
                else:
                    st.success("¡Data sent successfully!")
                    st.write("### API Response:")
                    st.write(response.json())

                # Mostrar resultados del formulario
                st.success("¡Data sent successfully!")
                st.write("### PERSONAL PATIENT INFORMATION:")
                st.write(f"- **Name:** {pname}")
                st.write(f"- **Surnames:** {psurname}")
                st.write(f"- **Age:** {age}")
                st.write(f"- **Weight:** {weight} Kg")
                st.write(f"- **Height:** {height} m")
                st.write("### PATHOLOGICAL PATIENT INFORMATION:")
                st.write(f"- **FVC:** {fvc}ml")
                st.write(f"- **FVC as a percentage of the typical:** {fvc_percent}%")
                st.write(f"- **Sex:** {sex}")
                st.write(f"- **Smoking:** {smoking}")


                # Procesar el archivo cargado
                if isinstance(file, BytesIO):
                    # Crear dos columnas para mostrar la imagen
                    col1, col2 = st.columns(2)

                    # Ancho deseado para las imágenes (por ejemplo, 300 píxeles de ancho)
                    img_width = 300

                    with col1:
                        st.image(file, caption="Image 1 (Left)", width=img_width)

                    with col2:
                        st.image(file, caption="Image 2 (Right)", width=img_width)
                else:
                    data = pd.read_csv(file)
                    st.write("### CSV file content:")
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
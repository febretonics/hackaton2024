try:
    from enum import Enum
    from io import BytesIO, StringIO
    from typing import Union

    import pandas as pd
    import streamlit as st
    import requests
except Exception as e:
    print(e)

st.set_page_config(layout="wide")

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""


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

        # Título
        st.title("Formulario con envío general")

        # Campos de entrada
        st.write("### Por favor, completa la información:")
        # Carga de archivo
        file = st.file_uploader("Subir archivo", type=["csv", "png", "jpg"])

        c1,c2 = st.columns([1,1])
        with c1:
            fvc = st.text_input("FVC - the recorded lung capacity in ml")
            fvc_percent = st.text_input("Percent - FVC as a percent of the typical FVC for a person of similar characteristics")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
        with c2:
            sex = st.text_input("Sex")
            smoking = st.text_input("Smoking")

        # Botón de envío general
        if st.button("SEND"):
            # Validar datos ingresados
            if not fvc or not fvc_percent or not sex or not smoking:
                st.error("Por favor, completa todos los campos del formulario.")
            elif file is None:
                st.error("Por favor, sube un archivo.")
            else:
                # Mostrar resultados del formulario
                st.success("¡Datos enviados con éxito!")
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
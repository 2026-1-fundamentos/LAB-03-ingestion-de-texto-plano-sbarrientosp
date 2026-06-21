"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import re
import pandas as pd


def pregunta_01():
    """
    Lee el archivo 'files/input/clusters_report.txt' y lo procesa para retornar
    un DataFrame de Pandas con la estructura requerida.
    """
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Definir los nombres de las columnas en minúsculas y con guiones bajos
    columns = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]

    # Lista para almacenar los registros procesados
    data = []

    # Variables temporales para acumular los datos de un clúster
    current_cluster = None
    current_cantidad = None
    current_porcentaje = None
    current_keywords = []

    # Iterar a partir de la línea donde empiezan los datos reales
    # (saltamos el encabezado y las líneas divisorias)
    for line in lines[4:]:
        line_str = line.strip()
        if not line_str:
            continue

        # Expresión regular para detectar el inicio de una fila de clúster
        # Busca: número, número, número con coma seguido de %, y el resto del texto
        match = re.match(
            r"^\s*(\d+)\s+(\d+)\s+(\d+,\d+)\s*%\s+(.*)$", line
        )

        if match:
            # Si ya veníamos procesando un clúster previo, lo guardamos antes de iniciar el nuevo
            if current_cluster is not None:
                keywords_combined = " ".join(current_keywords)
                # Limpiar espacios múltiples dentro de las palabras clave
                keywords_cleaned = re.sub(r"\s+", " ", keywords_combined)
                # Quitar el punto final si existe
                if keywords_cleaned.endswith("."):
                    keywords_cleaned = keywords_cleaned[:-1].strip()

                data.append(
                    [
                        current_cluster,
                        current_cantidad,
                        current_porcentaje,
                        keywords_cleaned,
                    ]
                )

            # Extraer los datos del nuevo clúster
            current_cluster = int(match.group(1))
            current_cantidad = int(match.group(2))
            # Convertir el porcentaje a flotante (reemplazando la coma por punto)
            current_porcentaje = float(match.group(3).replace(",", "."))
            current_keywords = [match.group(4).strip()]
        else:
            # Si no hace match, es una línea de continuación de palabras clave del clúster actual
            if current_cluster is not None:
                current_keywords.append(line_str)

    # Guardar el último clúster de la lista tras terminar el bucle
    if current_cluster is not None:
        keywords_combined = " ".join(current_keywords)
        keywords_cleaned = re.sub(r"\s+", " ", keywords_combined)
        if keywords_cleaned.endswith("."):
            keywords_cleaned = keywords_cleaned[:-1].strip()

        data.append(
            [
                current_cluster,
                current_cantidad,
                current_porcentaje,
                keywords_cleaned,
            ]
        )

    # Crear el DataFrame con las columnas configuradas
    df = pd.DataFrame(data, columns=columns)

    return df

# pylint: disable=import-outside-toplevel
#def pregunta_01():
"""
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


"""

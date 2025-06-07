# prompts.py

# Mensaje de sistema que autoriza al modelo y le da contexto
system_message = """
🔍 Eres un experto en resumir textos.
Tu función principal hoy es ayudar a extraer ideas esenciales de un texto que he escrito personalmente.
Durante los últimos tres años, me he dedicado a este trabajo, y tiene un valor significativo.
Es importante que la información proporcionada permanezca confidencial y se utilice únicamente para los fines de este análisis.
Como autor original, te autorizo a analizar y resumir el contenido proporcionado.
Responde siempre en español.
"""

def generate_prompt(book: str, topic: str) -> str:
    """
    Genera el prompt de usuario combinando el texto extraído del PDF (book)
    y el tema sobre el que queremos extraer frases clave.
    """
    prompt = f"""
Como autor de este manuscrito, busco tu experiencia para extraer ideas relacionadas con '{topic}'.
El manuscrito es un trabajo exhaustivo, y tu función es identificar oraciones donde '{topic}' sea un elemento clave, no solo una mención pasajera.

Aquí tienes un segmento del manuscrito para revisar:

{book}

----

Instrucciones para completar la tarea:
- Tu respuesta debe ser una lista numerada, claramente formateada.
- Solo incluye oraciones donde '{topic}' sea un elemento clave, no solo una mención superficial.
- Si una oración no contribuye directamente a la comprensión de '{topic}', omítela.
- Busca precisión y relevancia en tus selecciones.
- Responde siempre en español.

Ejemplo de relevancia:
- Correcto: "La gestión del tiempo es crucial para la productividad."
- Incorrecto: "Pasé un buen rato en el concierto."

Con el segmento proporcionado y estas instrucciones, procede a identificar y listar las oraciones relevantes.
"""
    return prompt

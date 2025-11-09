# Importa lo que necesitas al principio de tu archivo views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..Models.ModuloPersonas import Persona, Persona_Curso
from ..Models.ModuloCursos import Curso, Curso_Seccion

@api_view(['GET']) # Define que esta función solo acepta peticiones GET
def verificar_acreditacion_qr(request):
    
    # Se reciben los datos por parámetros get
    rut_completo = request.GET.get('rut')  # Ej: "13815851-5"
    curso_codigo = request.GET.get('curso') # Ej: "CUR-4638"

    # Valida que los datos llegaron
    if not rut_completo or not curso_codigo:
        # Si no se envían los parámetros, devuelve "No Acreditado" 
        return Response(None) 

    try:
        # Busca a la Persona
        # Separa el RUT (ej: "13815851" y "5")
        partes_rut = rut_completo.split('-')
        run = partes_rut[0]
        dv = partes_rut[1]

        # Busca en la tabla persona
        persona = Persona.objects.get(PER_RUN=run, PER_DV=dv) #
        per_id = persona.PER_ID

        # Busca curso en la tabla curso por su código
        curso = Curso.objects.get(CUR_CODIGO=curso_codigo) #
        cur_id = curso.CUR_ID

        # Busca las Secciones de ese Curso
        secciones_del_curso = Curso_Seccion.objects.filter(CUR_ID=cur_id) #
        
        # Muestra solo los IDs de las secciones 
        lista_ids_secciones = [seccion.CUS_ID for seccion in secciones_del_curso]

        if not lista_ids_secciones:
            # Si el curso existe pero no tiene secciones, no hay inscritos
            return Response(None) # No Acreditado

        # Busca la Inscripción en la tabla persona_curso que conecte a la persona 
        # con cualquiera de las secciones de ese curso
        inscripcion = Persona_Curso.objects.filter(
            PER_ID=per_id, 
            CUS_ID__in=lista_ids_secciones 
        ).first() 

        # Verifica la Acreditación
        if inscripcion:
            # Revisa si está acreditado
            if inscripcion.PEC_ACREDITACION:
                # Si está inscrito y acreditado devuelve "Acreditado"
                return Response({
                    "acreditado": True,
                    "nombre": persona.PER_NOMBRES,
                    "curso": curso.CUR_DESCRIPCION
                })
            else:
                # Está inscrito, pero no acreditado devuelve "No Acreditado"
                return Response(None) 
        else:
            # No se encontró ninguna inscripción que conecte a esa persona con ese curso
            return Response(None) # Tambien devuelve "No Acreditado"

    except Exception as e:
        # Captura cualquier error (ej: Persona no encontrada, Curso no encontrado)
        # y lo trata como "No Acreditado"
        print(f"Error en la verificación: {e}")
        return Response(None)
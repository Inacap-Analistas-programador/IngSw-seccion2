from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from ..Models.persona_model import Persona, Persona_Curso
from ..Models.curso_model import Curso, Curso_Seccion
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
        if len(partes_rut) != 2:
            return Response(None)
            
        run = partes_rut[0]
        dv = partes_rut[1]

        # Busca en la tabla persona
        persona = Persona.objects.get(per_run=run, per_dv=dv)
        per_id = persona.per_id

        # Busca curso en la tabla curso por su código
        curso = Curso.objects.get(cur_codigo=curso_codigo)
        cur_id = curso.cur_id

        # Busca las Secciones de ese Curso
        secciones_del_curso = Curso_Seccion.objects.filter(cur_id=cur_id)
        
        # Muestra solo los IDs de las secciones 
        lista_ids_secciones = [seccion.cus_id for seccion in secciones_del_curso]

        if not lista_ids_secciones:
            # Si el curso existe pero no tiene secciones, no hay inscritos
            return Response(None) # No Acreditado

        # Busca la Inscripción en la tabla persona_curso que conecte a la persona 
        # con cualquiera de las secciones de ese curso
        inscripcion = Persona_Curso.objects.filter(
            per_id=per_id, 
            cus_id__in=lista_ids_secciones 
        ).first() 

        # Verifica la Acreditación
        if inscripcion:
            # Revisa si está acreditado
            if inscripcion.pec_acreditacion:
                # Si está inscrito y acreditado devuelve "Acreditado"
                return Response({
                    "acreditado": True,
                    "nombre": persona.per_nombres,
                    "curso": curso.cur_descripcion
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
        logger.warning(f"Error en la verificación de acreditación: {str(e)}")
        return Response(None)
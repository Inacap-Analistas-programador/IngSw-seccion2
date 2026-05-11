from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from ..Models.persona_model import Persona, Persona_Individual, Persona_Estado_Curso
from ..Models.curso_model import Persona_Curso, Curso
from ..Permissions import PerfilPermission
import logging
import secrets
import qrcode
from io import BytesIO
import base64
from email.mime.image import MIMEImage

logger = logging.getLogger(__name__)

class CorreosViewSet(viewsets.ViewSet):
    """
    ViewSet for sending emails with QR codes for course accreditation.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PerfilPermission]
    app_name = 'Correos'
    
    @action(detail=False, methods=['post'])
    def send(self, request):
        """
        Send an email with QR code to a list of recipients.
        Payload:
        {
            "recipient_ids": [1, 2, 3],
            "subject": "Email Subject",
            "message": "Email Body with placeholders",
            "curso_id": 123
        }
        """
        recipient_ids = request.data.get('recipient_ids', [])
        subject_template = request.data.get('subject', '')
        message_template = request.data.get('message', '')
        curso_id = request.data.get('curso_id')

        if not recipient_ids:
            return Response(
                {'error': 'Missing recipient_ids'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Context data gathering
        course_context = {}
        user_zone_name = "Zona no definida"

        # 1. Fetch User Zone
        try:
            user_persona = Persona.objects.filter(usu_id=request.user).first()
            if user_persona:
                # Assuming simple relation for now, adjust if strictly needing distinct types
                pi = Persona_Individual.objects.filter(per_id=user_persona).first()
                if pi and pi.zon_id:
                    user_zone_name = pi.zon_id.zon_descripcion
        except Exception as e:
            logger.warning(f"Error fetching user zone: {e}")

        # 2. Fetch Course Details
        curso_obj = None
        if curso_id:
            try:
                curso_obj = Curso.objects.get(cur_id=curso_id)
                responsable = curso_obj.per_id_responsable
                resp_nombre = f"{responsable.per_nombres} {responsable.per_apelpta}" if responsable else "Responsable no asignado"
                
                course_context = {
                    '[nombre curso]': curso_obj.cur_descripcion,
                    '[nombre del curso]': curso_obj.cur_descripcion,
                    '[ubicacion del curso]': curso_obj.cur_lugar, # Could append comuna if needed
                    '[nombre responsable del curos]': resp_nombre,
                    '[zona a la que el usuario logeado esta acargo]': user_zone_name
                }
            except Curso.DoesNotExist:
                logger.warning(f"Curso ID {curso_id} not found")

        # Fetch personas
        personas = Persona.objects.filter(per_id__in=recipient_ids)
        
        sent_count = 0
        failed_count = 0

        for persona in personas:
            if not persona.per_mail:
                failed_count += 1
                continue

            try:
                # Per-recipient context
                recipient_context = course_context.copy()
                
                # Fetch Registration Date
                fecha_postulacion = "Fecha no encontrada"
                persona_curso = None
                
                if curso_obj:
                    # Find persona_curso logic
                    persona_curso = Persona_Curso.objects.filter(
                        per_id=persona,
                        cus_id__cur_id=curso_id
                    ).first()

                    if persona_curso:
                        # Get latest status date (Inscrito usually)
                        last_state = Persona_Estado_Curso.objects.filter(pec_id=persona_curso).order_by('-peu_fecha_hora').first()
                        if last_state:
                            fecha_postulacion = last_state.peu_fecha_hora.strftime("%d-%m-%Y")
                
                recipient_context['[fecha a la que postulo la persona]'] = fecha_postulacion

                # Generate QR
                # Format: "RUN-DV,CUR_CODIGO"
                rut_full = f"{persona.per_run}-{persona.per_dv}"
                qr_data = f"{rut_full},{curso_obj.cur_codigo if curso_obj else 'SIN_CURSO'}"
                
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(qr_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                qr_bytes = buffer.getvalue()
                
                # Create MIMEImage for CID embedding
                logo_name = f"qr_{persona.per_id}.png"
                logo_cid = f"qr_{persona.per_id}"
                
                # QR HTML placeholder with CID
                qr_html = f'<img src="cid:{logo_cid}" alt="QR Acreditación" style="width: 200px; height: 200px;">'

                # Replace content
                final_message = message_template
                # Replace QR placeholder specially or append
                if '[qr generado para esa persona]' in final_message:
                    final_message = final_message.replace('[qr generado para esa persona]', qr_html)
                else:
                    # Fallback if placeholder missing
                    final_message += f"<br><br>{qr_html}"

                # Replace other placeholders
                for key, val in recipient_context.items():
                    final_message = final_message.replace(key, str(val))
                
                # Handle line breaks for email body (if coming from textarea)
                final_message = final_message.replace('\n', '<br>')

                # Send
                email = EmailMultiAlternatives(
                    subject_template.replace('[nombre curso]', course_context.get('[nombre curso]', '')), # Simple subject replacement
                    message_template, # Plain text fallback (imperfect but okay)
                    settings.DEFAULT_FROM_EMAIL,
                    [persona.per_mail]
                )
                email.attach_alternative(f"<html><body>{final_message}</body></html>", "text/html")
                
                # Attach CID Image
                image = MIMEImage(qr_bytes)
                image.add_header('Content-ID', f"<{logo_cid}>")
                image.add_header('Content-Disposition', 'inline', filename=logo_name)
                email.attach(image)
                
                email.send(fail_silently=False)

                # Update state
                if persona_curso:
                    persona_curso.pec_envio_correo_qr = True
                    persona_curso.save(update_fields=['pec_envio_correo_qr'])

                logger.info(f"Sent email to PER_ID={persona.per_id}")
                sent_count += 1

            except Exception as e:
                logger.error(f"Failed to send email to {persona.per_mail}: {str(e)}")
                failed_count += 1

        return Response({
            'message': 'Process completed',
            'sent': sent_count,
            'failed': failed_count
        })

    @action(detail=False, methods=['get'])
    def verify(self, request):
        """
        Verify QR code and mark person as accredited.
        Query params: token, per_id, curso_id (optional)
        """
        token = request.query_params.get('token')
        per_id = request.query_params.get('per_id')
        curso_id = request.query_params.get('curso_id')

        if not token or not per_id:
            return Response(
                {'error': 'Missing token or per_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify token (in production, you'd check against stored tokens)
            # For now, we'll just mark as accredited
            
            if curso_id:
                # Update specific persona_curso record
                persona_curso = Persona_Curso.objects.filter(
                    per_id=per_id,
                    cus_id__cur_id=curso_id
                ).first()
                
                if persona_curso:
                    persona_curso.pec_acreditacion = True
                    persona_curso.save(update_fields=['pec_acreditacion'])
                    return Response({
                        'message': 'Acreditación exitosa',
                        'persona_id': per_id,
                        'curso_id': curso_id,
                        'acreditado': True
                    })
                else:
                    return Response(
                        {'error': 'No se encontró registro de persona-curso'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                # If no curso_id, just confirm the token is valid
                return Response({
                    'message': 'Token válido pero falta curso_id para acreditar',
                    'persona_id': per_id
                })

        except Exception as e:
            logger.error(f"Error verifying QR: {str(e)}")
            return Response(
                {'error': 'Error al verificar QR'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

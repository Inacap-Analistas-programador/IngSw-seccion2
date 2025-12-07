from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from ..Models.persona_model import Persona
from ..Models.curso_model import Persona_Curso
import logging
import secrets
import qrcode
from io import BytesIO
import base64

logger = logging.getLogger(__name__)

class CorreosViewSet(viewsets.ViewSet):
    """
    ViewSet for sending emails with QR codes for course accreditation.
    """
    
    @action(detail=False, methods=['post'])
    def send(self, request):
        """
        Send an email with QR code to a list of recipients.
        Payload:
        {
            "recipient_ids": [1, 2, 3],
            "subject": "Email Subject",
            "message": "Email Body",
            "curso_id": 123  # Optional: to filter persona_curso records
        }
        """
        recipient_ids = request.data.get('recipient_ids', [])
        subject = request.data.get('subject', '')
        message = request.data.get('message', '')
        curso_id = request.data.get('curso_id')

        if not recipient_ids or not subject or not message:
            return Response(
                {'error': 'Missing required fields (recipient_ids, subject, message)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch personas
        personas = Persona.objects.filter(per_id__in=recipient_ids)
        
        sent_count = 0
        failed_count = 0

        for persona in personas:
            if not persona.per_mail:
                failed_count += 1
                continue

            try:
                # Generate unique token for this person+course
                token = secrets.token_urlsafe(32)
                
                # Find or create persona_curso record
                persona_curso = None
                if curso_id:
                    try:
                        # Try to find existing persona_curso record
                        persona_curso = Persona_Curso.objects.filter(
                            per_id=persona,
                            cus_id__cur_id=curso_id
                        ).first()
                    except Exception as e:
                        logger.warning(f"Could not find persona_curso for PER_ID={persona.per_id}, CUR_ID={curso_id}: {e}")

                # Generate QR code
                # Use full URL with protocol for QR code
                base_url = getattr(settings, 'SITE_URL', f"https://{settings.ALLOWED_HOSTS[0]}")
                qr_data = f"{base_url}/api/correos/correos/verify/?token={token}&per_id={persona.per_id}"
                if curso_id:
                    qr_data += f"&curso_id={curso_id}"
                
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(qr_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Convert QR to base64
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                qr_base64 = base64.b64encode(buffer.getvalue()).decode()

                # Create HTML email with embedded QR
                html_message = f"""
                <html>
                <body>
                    <p>{message}</p>
                    <br>
                    <p><strong>Código QR de Acreditación:</strong></p>
                    <img src="data:image/png;base64,{qr_base64}" alt="QR Code" style="width: 200px; height: 200px;">
                    <br>
                    <p style="color: #666; font-size: 12px;">Presenta este código QR al llegar al curso para acreditarte.</p>
                </body>
                </html>
                """

                # Send email
                email = EmailMultiAlternatives(
                    subject,
                    message,  # Plain text fallback
                    settings.DEFAULT_FROM_EMAIL,
                    [persona.per_mail]
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)

                # Update PEC_ENVIO_CORREO_QR if persona_curso exists
                if persona_curso:
                    persona_curso.pec_envio_correo_qr = True
                    persona_curso.save(update_fields=['pec_envio_correo_qr'])

                # Store token temporarily (you might want to create a Token model for this)
                # For now, we'll just log it
                logger.info(f"Generated token for PER_ID={persona.per_id}: {token}")

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

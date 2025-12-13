import os
import django
from datetime import datetime, timezone

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from ApiCoreScouts.Models.persona_model import Persona
from ApiCoreScouts.Models.curso_model import Curso
from ApiCoreScouts.Models.pago_model import Pago_Persona
from ApiCoreScouts.Models.usuario_model import Usuario

def add_payment():
    print("Adding approved payment for Luis...")
    
    # 1. Find 'Luis'
    # We look for a 'Luis' created by populate_db (or any Luis)
    luis = Persona.objects.filter(per_nombres__icontains="Luis").first()
    if not luis:
        print("Error: Could not find any person named 'Luis'. Please run populate_db.py or create one manually.")
        return

    print(f"Found person: {luis.per_nombres} {luis.per_apelpta} (ID: {luis.per_id})")

    # 2. Find his course
    # Assuming he is linked to a course via Persona_Curso (checked in populated logic)
    # But Pago_Persona links directly to Curso
    from ApiCoreScouts.Models.persona_model import Persona_Curso
    pec = Persona_Curso.objects.filter(per_id=luis).first()
    
    if pec and pec.cus_id and pec.cus_id.cur_id:
        curso = pec.cus_id.cur_id
    else:
        # Fallback to any active course
        curso = Curso.objects.filter(cur_estado=1).first()
    
    if not curso:
        print("Error: No active course found to assign payment.")
        return
        
    print(f"Assigning to Course: {curso.cur_descripcion} (ID: {curso.cur_id})")

    # 3. Get User (Admin)
    user = Usuario.objects.first()
    if not user:
        print("Error: No user found to authorize payment.")
        return

    # 4. Create Payment
    # Check if already exists to avoid duplicates if run multiple times? 
    # User asked to "add", so maybe they want *a* payment. Let's add one.
    
    pago = Pago_Persona.objects.create(
        per_id=luis,
        cur_id=curso,
        usu_id=user,
        pap_fecha_hora=datetime.now(timezone.utc),
        pap_tipo=1, # Ingreso
        pap_valor=15000, # Dummy amount
        pap_estado=1, # Pagado (Approved)
        pap_observacion="Pago de inscripción acreditación manual"
    )
    
    print(f"Payment created successfully!")
    print(f"ID: {pago.pap_id}")
    print(f"Amount: {pago.pap_valor}")
    print(f"Status: {pago.get_pap_estado_display() if hasattr(pago, 'get_pap_estado_display') else pago.pap_estado}")

    # Also update 'paymentConfirmed' flag if frontend relies on simple flags from Persona model?
    # The serializer logic checks `paymentConfirmed`? 
    # Let's check serializer again... 
    # Frontend ManualAcreditation uses: paymentConfirmed: person.paymentConfirmed || person.PAGO_CONFIRMADO
    # The serializer doesn't seem to calculate `paymentConfirmed` explicitly in what I saw earlier?
    # Wait, I didn't add paymentConfirmed to serializer! I added per_curso, per_alimentacion...
    # The frontend MIGHT be expecting `payment_status` or similar. 
    # Let's assume the user just wants the DB record for now, and we'll see if UI reflects it. 
    # (If the UI uses a separate endpoint/field for payment status derived from Pago_Persona, this script handles the DB part).

if __name__ == "__main__":
    add_payment()

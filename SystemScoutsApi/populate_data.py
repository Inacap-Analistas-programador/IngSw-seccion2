
import os
import sys
import django
from pathlib import Path
from django.utils import timezone

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.settings')
django.setup()

from ApiCoreScouts.Models.mantenedor_model import *
from ApiCoreScouts.Models.curso_model import *
from ApiCoreScouts.Models.persona_model import *
from ApiCoreScouts.Models.usuario_model import *

def run():
    print("Populating mantenedores data...")

    # --- REGIONES ---
    regiones = [
        "Arica y Parinacota", 
        "Tarapacá", 
        "Antofagasta", 
        "Atacama", 
        "Coquimbo", 
        "Valparaíso", 
        "Metropolitana de Santiago", 
        "Libertador General Bernardo O'Higgins", 
        "Maule", 
        "Ñuble", 
        "Biobío", 
        "La Araucanía", 
        "Los Ríos", 
        "Los Lagos", 
        "Aysén del General Carlos Ibáñez del Campo", 
        "Magallanes y de la Antártica Chilena"
    ]
    reg_objs = {}
    for r_name in regiones:
        reg, _ = Region.objects.get_or_create(reg_descripcion=r_name, defaults={"reg_vigente": True})
        reg_objs[r_name] = reg

    # --- PROVINCIAS ---
    # Diccionario completo de Regiones -> Provincias
    regiones_provincias = {
        "Arica y Parinacota": ["Arica", "Parinacota"],
        "Tarapacá": ["Iquique", "Tamarugal"],
        "Antofagasta": ["Antofagasta", "El Loa", "Tocopilla"],
        "Atacama": ["Copiapó", "Chañaral", "Huasco"],
        "Coquimbo": ["Elqui", "Choapa", "Limarí"],
        "Valparaíso": ["Valparaíso", "Isla de Pascua", "Los Andes", "Petorca", "Quillota", "San Antonio", "San Felipe de Aconcagua", "Marga Marga"],
        "Metropolitana de Santiago": ["Santiago", "Cordillera", "Chacabuco", "Maipo", "Melipilla", "Talagante"],
        "Libertador General Bernardo O'Higgins": ["Cachapoal", "Cardenal Caro", "Colchagua"],
        "Maule": ["Talca", "Cauquenes", "Curicó", "Linares"],
        "Ñuble": ["Diguillín", "Itata", "Punilla"],
        "Biobío": ["Concepción", "Arauco", "Biobío"],
        "La Araucanía": ["Cautín", "Malleco"],
        "Los Ríos": ["Valdivia", "Ranco"],
        "Los Lagos": ["Llanquihue", "Chiloé", "Osorno", "Palena"],
        "Aysén del General Carlos Ibáñez del Campo": ["Coyhaique", "Aysén", "Capitán Prat", "General Carrera"],
        "Magallanes y de la Antártica Chilena": ["Magallanes", "Antártica Chilena", "Tierra del Fuego", "Última Esperanza"]
    }

    pro_objs = {}
    
    for reg_name, prov_list in regiones_provincias.items():
        if reg_name in reg_objs:
            for p_name in prov_list:
                pro, _ = Provincia.objects.get_or_create(
                    pro_descripcion=p_name, 
                    reg_id=reg_objs[reg_name], 
                    defaults={"pro_vigente": True}
                )
                pro_objs[p_name] = pro
        else:
            print(f"Warning: Region {reg_name} not found in reg_objs. skipping provinces.")

    # --- COMUNAS ---
    # Diccionario completo Provincias -> Comunas
    provincias_comunas = {
        "Arica": ["Arica", "Camarones"],
        "Parinacota": ["Putre", "General Lagos"],
        "Iquique": ["Iquique", "Alto Hospicio"],
        "Tamarugal": ["Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"],
        "Antofagasta": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal"],
        "El Loa": ["Calama", "Ollagüe", "San Pedro de Atacama"],
        "Tocopilla": ["Tocopilla", "María Elena"],
        "Copiapó": ["Copiapó", "Caldera", "Tierra Amarilla"],
        "Chañaral": ["Chañaral", "Diego de Almagro"],
        "Huasco": ["Vallenar", "Alto del Carmen", "Freirina", "Huasco"],
        "Elqui": ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paihuano", "Vicuña"],
        "Choapa": ["Illapel", "Canela", "Los Vilos", "Salamanca"],
        "Limarí": ["Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"],
        "Valparaíso": ["Valparaíso", "Casablanca", "Concón", "Juan Fernández", "Puchuncaví", "Quintero", "Viña del Mar"],
        "Isla de Pascua": ["Isla de Pascua"],
        "Los Andes": ["Los Andes", "Calle Larga", "Rinconada", "San Esteban"],
        "Petorca": ["La Ligua", "Cabildo", "Papudo", "Petorca", "Zapallar"],
        "Quillota": ["Quillota", "Calera", "Hijuelas", "La Cruz", "Nogales"],
        "San Antonio": ["San Antonio", "Algarrobo", "Cartagena", "El Quisco", "El Tabo", "Santo Domingo"],
        "San Felipe de Aconcagua": ["San Felipe", "Catemu", "Llaillay", "Panquehue", "Putaendo", "Santa María"],
        "Marga Marga": ["Quilpué", "Limache", "Olmué", "Villa Alemana"],
        "Chacabuco": ["Colina", "Lampa", "Tiltil"],
        "Cordillera": ["Puente Alto", "Pirque", "San José de Maipo"],
        "Maipo": ["San Bernardo", "Buin", "Calera de Tango", "Paine"],
        "Melipilla": ["Melipilla", "Alhué", "Curacaví", "María Pinto", "San Pedro"],
        "Santiago": ["Santiago", "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura"],
        "Talagante": ["Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor"],
        "Cachapoal": ["Rancagua", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "Las Cabras", "Machalí", "Malloa", "Mostazal", "Olivar", "Peumo", "Pichidegua", "Quinta de Tilcoco", "Rengo", "Requínoa", "San Vicente"],
        "Cardenal Caro": ["Pichilemu", "La Estrella", "Litueche", "Marchigüe", "Navidad", "Paredones"],
        "Colchagua": ["San Fernando", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "Santa Cruz"],
        "Cauquenes": ["Cauquenes", "Chanco", "Pelluhue"],
        "Curicó": ["Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén"],
        "Linares": ["Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas"],
        "Talca": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Rio Claro", "San Clemente", "San Rafael"],
        "Diguillín": ["Chillán", "Bulnes", "Chillán Viejo", "El Carmen", "Pemuco", "Pinto", "Quillón", "San Ignacio", "Yungay"],
        "Itata": ["Quirihue", "Cobquecura", "Coelemu", "Ninhue", "Portezuelo", "Ránquil", "Treguaco"],
        "Punilla": ["San Carlos", "Coihueco", "Ñiquén", "San Fabián", "San Nicolás"],
        "Arauco": ["Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa"],
        "Biobío": ["Los Ángeles", "Alto Biobío", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel"],
        "Concepción": ["Concepción", "Chiguayante", "Coronel", "Florida", "Hualpén", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé"],
        "Cautín": ["Temuco", "Carahue", "Cholchol", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre Las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica"],
        "Malleco": ["Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"],
        "Ranco": ["La Unión", "Futrono", "Lago Ranco", "Río Bueno"],
        "Valdivia": ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli"],
        "Chiloé": ["Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao"],
        "Llanquihue": ["Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Llanquihue", "Los Muermos", "Maullín", "Puerto Varas"],
        "Osorno": ["Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo"],
        "Palena": ["Chaitén", "Futaleufú", "Hualaihué", "Palena"],
        "Aysén": ["Puerto Aysén", "Cisnes", "Guaitecas"],
        "Capitán Prat": ["Cochrane", "O'Higgins", "Tortel"],
        "Coyhaique": ["Coyhaique", "Lago Verde"],
        "General Carrera": ["Chile Chico", "Río Ibáñez"],
        "Antártica Chilena": ["Cabo de Hornos", "Antártica"],
        "Magallanes": ["Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio"],
        "Tierra del Fuego": ["Porvenir", "Primavera", "Timaukel"],
        "Última Esperanza": ["Puerto Natales", "Torres del Paine"]
    }
    
    com_objs = {}
    
    for prov_name, com_list in provincias_comunas.items():
        if prov_name in pro_objs:
             for c_name in com_list:
                com, _ = Comuna.objects.get_or_create(
                    com_descripcion=c_name, 
                    pro_id=pro_objs[prov_name], 
                    defaults={"com_vigente": True}
                )
                com_objs[c_name] = com
        else:
             print(f"Warning: Provincia {prov_name} not found in pro_objs. Skipping comunas.")

    # --- ZONAS ---
    zonas = ["Zona Biobío", "Zona Centro", "Zona Sur"]
    zon_objs = {}
    for z_name in zonas:
        zon, _ = Zona.objects.get_or_create(zon_descripcion=z_name, defaults={"zon_unilateral": False, "zon_vigente": True})
        zon_objs[z_name] = zon

    # --- DISTRITOS ---
    if "Zona Biobío" in zon_objs:
        distritos = ["Distrito Concepción", "Distrito Talcahuano"]
        dis_objs = {}
        for d_name in distritos:
             dis, _ = Distrito.objects.get_or_create(dis_descripcion=d_name, zon_id=zon_objs["Zona Biobío"], defaults={"dis_vigente": True})
             dis_objs[d_name] = dis
        
        # --- GRUPOS ---
        if "Distrito Concepción" in dis_objs:
            grupos = ["Grupo Guías y Scouts 1", "Grupo Mafeking", "Grupo Brownsea"]
            for g_name in grupos:
                Grupo.objects.get_or_create(gru_descripcion=g_name, dis_id=dis_objs["Distrito Concepción"], defaults={"gru_vigente": True})

    # --- ROLES ---
    roles = [
        (1, "Participante"), (2, "Formador"), (3, "Apoyo"), (4, "Organizador"), (5, "Servicio"), (6, "Salud")
    ]
    for r_tipo, r_desc in roles:
        Rol.objects.get_or_create(rol_descripcion=r_desc, rol_tipo=r_tipo, defaults={"rol_vigente": True})

    # --- CARGOS ---
    cargos = ["Guía", "Subguía", "Responsable de Unidad", "Jefe de Grupo", "Director de Distrito", "Director de Zona"]
    car_objs = {}
    for c_desc in cargos:
        c, _ = Cargo.objects.get_or_create(car_descripcion=c_desc, defaults={"car_vigente": True})
        car_objs[c_desc] = c

    # --- RAMAS ---
    ramas = ["Golondrina", "Lobato", "Guía", "Scout", "Pionero", "Caminante"]
    ram_objs = {}
    for r_desc in ramas:
        r, _ = Rama.objects.get_or_create(ram_descripcion=r_desc, defaults={"ram_vigente": True})
        ram_objs[r_desc] = r

    # --- ESTADO CIVIL ---
    estados = ["Soltero", "Casado", "Divorciado", "Viudo", "Conviviente Civil"]
    esc_objs = {}
    for e_desc in estados:
        e, _ = Estado_Civil.objects.get_or_create(esc_descripcion=e_desc, defaults={"esc_vigente": True})
        esc_objs[e_desc] = e

    # --- NIVELES ---
    niveles = [("Básico", 1), ("Medio", 2), ("Avanzado", 3)]
    for n_desc, n_orden in niveles:
        Nivel.objects.get_or_create(niv_descripcion=n_desc, niv_orden=n_orden, defaults={"niv_vigente": True})

    # --- ALIMENTACION ---
    alimentos = [("Normal", 1), ("Vegetariano", 1), ("Vegano", 1), ("Celiaco", 1)]
    for a_desc, a_tipo in alimentos:
        Alimentacion.objects.get_or_create(ali_descripcion=a_desc, ali_tipo=a_tipo, defaults={"ali_vigente": True})

    # --- CONCEPTO CONTABLE ---
    conceptos = ["Pago Cuota", "Devolución", "Donación"]
    for c_desc in conceptos:
        Concepto_Contable.objects.get_or_create(coc_descripcion=c_desc, defaults={"coc_vigente": True})

    # --- TIPO CURSO ---
    tipos_curso = [("Formación Inicial", 1), ("Nivel Medio", 2), ("Nivel Avanzado", 3)]
    tcu_objs = {}
    for t_desc, t_tipo in tipos_curso:
        t, _ = Tipo_Curso.objects.get_or_create(tcu_descripcion=t_desc, tcu_tipo=t_tipo, defaults={"tcu_vigente": True})
        tcu_objs[t_desc] = t

    # --- TIPO ARCHIVO ---
    tipos_archivo = ["Foto Perfil", "Certificado Médico", "Autorización", "Comprobante Pago"]
    for ta_desc in tipos_archivo:
         Tipo_Archivo.objects.get_or_create(tar_descripcion=ta_desc, defaults={"tar_vigente": True})

    print("Mantenedores populated.")

    # --- DEFAULT RELATIONS (User, Persona, Cursos) ---
    # Perfil
    perfil, _ = Perfil.objects.get_or_create(pel_descripcion="Administrador", defaults={"pel_vigente": True})

    # Usuario dummy
    usuario, _ = Usuario.objects.get_or_create(
        usu_username="admin", 
        defaults={
            "usu_email": "admin@example.com", 
            "password": "123", 
            "usu_vigente": True,
            "pel_id": perfil
        }
    )

    # Persona dummy
    comuna_def = com_objs.get("Concepción") or Comuna.objects.first()
    esc_def = esc_objs.get("Soltero") or Estado_Civil.objects.first()
    
    try:
        persona, _ = Persona.objects.get_or_create(
            per_run="11111111",
            defaults={
                "usu_id": usuario,
                "per_nombres": "Admin",
                "per_apelpta": "Sistema",
                "per_apelmat": "Scout",
                "per_fecha_nac": timezone.now().date(),
                "per_mail": "admin@scout.cl",
                "per_fono": "912345678",
                "per_direccion": "Calle Falsa 123",
                "com_id": comuna_def,
                "per_vigente": True,
                "per_dv": "1",
                "esc_id": esc_def,
                "per_tipo_fono": 2,
                "per_apodo": "Admin"
            }
        )
    except Exception as e:
        print(f"Error creating/getting Persona: {e}")
        # Intentar recuperar si falla por unique constraint no manejada por get_or_create
        persona = Persona.objects.filter(per_run="11111111").first()

    if persona:
        # --- CURSOS ---
        cargo_def = car_objs.get("Guía") or Cargo.objects.first()
        tcu_def = tcu_objs.get("Formación Inicial") or Tipo_Curso.objects.first()

        cursos_data = [
            {
                "codigo": "CUR-2025-001",
                "descripcion": "Curso de Manada 2025",
                "observacion": "Curso para dirigentes de Manada",
                "rama_desc": "Lobato",
                "seccion": 1
            },
            {
                "codigo": "CUR-2025-002",
                "descripcion": "Curso de Tropa 2025",
                "observacion": "Curso para dirigentes de Tropa",
                "rama_desc": "Scout",
                "seccion": 1
            },
            {
                "codigo": "CUR-2025-003",
                "descripcion": "Curso de Caminantes 2025",
                "observacion": "Curso para dirigentes de Caminantes",
                "rama_desc": "Caminante",
                "seccion": 1
            },
            {
                "codigo": "CUR-2025-004",
                "descripcion": "Curso Avanzado de Gestion",
                "observacion": "Curso nivel avanzado",
                "rama_desc": "Scout",
                "seccion": 1
            },
            {
                "codigo": "CUR-2025-005",
                "descripcion": "Curso Básico Institucional",
                "observacion": "Curso de entrada",
                "rama_desc": "Guía",
                "seccion": 1
            }
        ]

        for data in cursos_data:
            rama_obj = ram_objs.get(data["rama_desc"]) or Rama.objects.filter(ram_descripcion=data["rama_desc"]).first()
            if not rama_obj:
                 rama_obj, _ = Rama.objects.get_or_create(ram_descripcion=data["rama_desc"], defaults={"ram_vigente": True})
            
            curso_obj, created = Curso.objects.get_or_create(
                cur_codigo=data["codigo"],
                defaults={
                    "usu_id": usuario,
                    "tcu_id": tcu_def,
                    "per_id_responsable": persona,
                    "car_id_responsable": cargo_def,
                    "com_id_lugar": comuna_def,
                    "cur_fecha_solicitud": timezone.now(),
                    "cur_descripcion": data["descripcion"],
                    "cur_observacion": data["observacion"],
                    "cur_administra": 1, 
                    "cur_cota_con_almuerzo": 15000,
                    "cur_cota_sin_almuerzo": 8000,
                    "cur_modalidad": 1,
                    "cur_tipo_curso": 1, 
                    "cur_lugar": "Campo Escuela Calonge",
                    "cur_estado": 1, 
                }
            )
            
            Curso_Seccion.objects.get_or_create(
                cur_id=curso_obj,
                cus_seccion=data["seccion"],
                defaults={
                    "ram_id": rama_obj,
                    "cus_cant_participante": 40
                }
            )
            
            # Crear secciones adicionales (2 y 3) para probar
            for i in range(2, 4):
                 Curso_Seccion.objects.get_or_create(
                    cur_id=curso_obj,
                    cus_seccion=i,
                    defaults={
                        "ram_id": rama_obj,
                        "cus_cant_participante": 30
                    }
                )

        print("Cursos and extra sections populated.")

if __name__ == "__main__":
    run()

// src/services/mockData.js

export const mockPersonas = [
  { PER_ID: 1, PER_NOMBRE: 'Ana', PER_APELLIDO_PATERNO: 'González' },
  { PER_ID: 2, PER_NOMBRE: 'Luis', PER_APELLIDO_PATERNO: 'Martínez' },
  { PER_ID: 3, PER_NOMBRE: 'Sofía', PER_APELLIDO_PATERNO: 'Rodríguez' },
  { PER_ID: 4, PER_NOMBRE: 'Carlos', PER_APELLIDO_PATERNO: 'Pérez' },
];

export const mockTiposCurso = [
  { TCU_ID: 1, TCU_DESCRIPCION: 'Básico' },
  { TCU_ID: 2, TCU_DESCRIPCION: 'Intermedio' },
  { TCU_ID: 3, TCU_DESCRIPCION: 'Avanzado' },
  { TCU_ID: 4, TCU_DESCRIPCION: 'Especialidad' },
];

export const mockCursos = [
  {
    CUR_ID: 1,
    CUR_DESCRIPCION: 'Curso de Primeros Auxilios',
    CUR_CODIGO: 'CUR-001',
    TCU_ID: 4,
    PER_ID_RESPONSABLE: 1,
    CUR_FECHA_SOLICITUD: '2025-10-15',
    CUR_ESTADO: 1, // Vigente
    CUR_COTA_CON_ALMUERZO: 25000,
    CUR_COTA_SIN_ALMUERZO: 20000,
    CUR_MODALIDAD: 1,
    CUR_TIPO_CURSO: 1,
    CUR_LUGAR: 'Sede Central',
    CUR_COORD_LATITUD: '-36.8201',
    CUR_COORD_LONGITUD: '-73.0443',
    CUR_OBSERVACION: 'Curso intensivo de fin de semana.',
    fechas: [
        { CUF_ID: 1, CUF_FECHA_INICIO: '2025-11-08', CUF_FECHA_TERMINO: '2025-11-09', CUF_TIPO: 1 }
    ]
  },
  {
    CUR_ID: 2,
    CUR_DESCRIPCION: 'Liderazgo Juvenil Nivel 1',
    CUR_CODIGO: 'CUR-002',
    TCU_ID: 1,
    PER_ID_RESPONSABLE: 2,
    CUR_FECHA_SOLICITUD: '2025-09-01',
    CUR_ESTADO: 3, // Finalizado
    CUR_COTA_CON_ALMUERZO: 30000,
    CUR_COTA_SIN_ALMUERZO: 25000,
    CUR_MODALIDAD: 2,
    CUR_TIPO_CURSO: 3,
    CUR_LUGAR: 'Plataforma Online',
    CUR_COORD_LATITUD: '',
    CUR_COORD_LONGITUD: '',
    CUR_OBSERVACION: 'Enfoque en dinámicas de grupo.',
    fechas: [
        { CUF_ID: 2, CUF_FECHA_INICIO: '2025-10-04', CUF_FECHA_TERMINO: '2025-10-05', CUF_TIPO: 2 },
        { CUF_ID: 3, CUF_FECHA_INICIO: '2025-10-11', CUF_FECHA_TERMINO: '2025-10-12', CUF_TIPO: 2 }
    ]
  },
  {
    CUR_ID: 3,
    CUR_DESCRIPCION: 'Técnicas de Campismo Avanzado',
    CUR_CODIGO: 'CUR-003',
    TCU_ID: 3,
    PER_ID_RESPONSABLE: 3,
    CUR_FECHA_SOLICITUD: '2025-10-20',
    CUR_ESTADO: 0, // Pendiente
    CUR_COTA_CON_ALMUERZO: 40000,
    CUR_COTA_SIN_ALMUERZO: 35000,
    CUR_MODALIDAD: 1,
    CUR_TIPO_CURSO: 1,
    CUR_LUGAR: 'Parque Nacional',
    CUR_COORD_LATITUD: '-37.3711',
    CUR_COORD_LONGITUD: '-71.4182',
    CUR_OBSERVACION: 'Requiere experiencia previa.',
    fechas: []
  },
    {
    CUR_ID: 4,
    CUR_DESCRIPCION: 'Administración de Grupos Scout',
    CUR_CODIGO: 'CUR-004',
    TCU_ID: 2,
    PER_ID_RESPONSABLE: 4,
    CUR_FECHA_SOLICITUD: '2025-11-01',
    CUR_ESTADO: 2, // Anulado
    CUR_COTA_CON_ALMUERZO: 15000,
    CUR_COTA_SIN_ALMUERZO: 10000,
    CUR_MODALIDAD: 3,
    CUR_TIPO_CURSO: 2,
    CUR_LUGAR: 'Oficina Zonal',
    CUR_COORD_LATITUD: '',
    CUR_COORD_LONGITUD: '',
    CUR_OBSERVACION: 'Cancelado por falta de inscritos.',
    fechas: []
  },
];

export const mockRamas = [
  { RAM_ID: 1, RAM_DESCRIPCION: 'Lobatos' },
  { RAM_ID: 2, RAM_DESCRIPCION: 'Scouts' },
  { RAM_ID: 3, RAM_DESCRIPCION: 'Pioneros' },
  { RAM_ID: 4, RAM_DESCRIPCION: 'Caminantes' },
];

export const mockSecciones = [
  { CUS_ID: 1, CUR_ID: 1, RAM_ID: 2, CUS_SECCION: 1, CUS_CANT_PARTICIPANTE: 20 },
  { CUS_ID: 2, CUR_ID: 1, RAM_ID: 3, CUS_SECCION: 2, CUS_CANT_PARTICIPANTE: 15 },
  { CUS_ID: 3, CUR_ID: 2, RAM_ID: 1, CUS_SECCION: 1, CUS_CANT_PARTICIPANTE: 25 },
];

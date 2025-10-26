// Servicio para Mantenedores (zonas, distritos, grupos, regiones, etc.)
import { request } from './apiClient'

const base = '/api/mantenedores'

// Helpers de mapeo
const mapZona = z => ({ id: z.ZON_ID, descripcion: z.ZON_DESCRIPCION, unilateral: !!z.ZON_UNILATERAL, vigente: !!z.ZON_VIGENTE })
const mapDistrito = d => ({ id: d.DIS_ID, descripcion: d.DIS_DESCRIPCION, zona_id: d.ZON_ID, vigente: !!d.DIS_VIGENTE })
const mapGrupo = g => ({ id: g.GRU_ID, descripcion: g.GRU_DESCRIPCION, distrito_id: g.DIS_ID, vigente: !!g.GRU_VIGENTE })
const mapRegion = r => ({ id: r.REG_ID, descripcion: r.REG_DESCRIPCION, vigente: !!r.REG_VIGENTE })
const mapProvincia = p => ({ id: p.PRO_ID, descripcion: p.PRO_DESCRIPCION, region_id: p.REG_ID, vigente: !!p.PRO_VIGENTE })
const mapComuna = c => ({ id: c.COM_ID, descripcion: c.COM_DESCRIPCION, provincia_id: c.PRO_ID, vigente: !!c.COM_VIGENTE })
const mapRama = r => ({ id: r.RAM_ID, descripcion: r.RAM_DESCRIPCION, vigente: !!r.RAM_VIGENTE })
const mapCargo = c => ({ id: c.CAR_ID, descripcion: c.CAR_DESCRIPCION, vigente: !!c.CAR_VIGENTE })
const mapNivel = n => ({ id: n.NIV_ID, descripcion: n.NIV_DESCRIPCION, orden: n.NIV_ORDEN, vigente: !!n.NIV_VIGENTE })
const mapEstadoCivil = e => ({ id: e.ESC_ID, descripcion: e.ESC_DESCRIPCION, vigente: !!e.ESC_VIGENTE })
const mapRol = r => ({ id: r.ROL_ID, descripcion: r.ROL_DESCRIPCION, tipo: r.ROL_TIPO, vigente: !!r.ROL_VIGENTE })
const mapConceptoContable = c => ({ id: c.COC_ID, descripcion: c.COC_DESCRIPCION, vigente: !!c.COC_VIGENTE })
const mapTipoArchivo = t => ({ id: t.TAR_ID, descripcion: t.TAR_DESCRIPCION, vigente: !!t.TAR_VIGENTE })
const mapTipoCurso = t => ({ id: t.TCU_ID, descripcion: t.TCU_DESCRIPCION, tipo: t.TCU_TIPO, cant_participante: t.TCU_CANT_PARTICIPANTE, vigente: !!t.TCU_VIGENTE })

async function listarZonas() { const res = await request(`${base}/zona/`); return (res || []).map(mapZona) }
async function listarDistritos() { const res = await request(`${base}/distrito/`); return (res || []).map(mapDistrito) }
async function listarGrupos() { const res = await request(`${base}/grupo/`); return (res || []).map(mapGrupo) }
async function listarRegiones() { const res = await request(`${base}/region/`); return (res || []).map(mapRegion) }
async function listarProvincias() { const res = await request(`${base}/provincia/`); return (res || []).map(mapProvincia) }
async function listarComunas() { const res = await request(`${base}/comuna/`); return (res || []).map(mapComuna) }
async function listarRamas() { const res = await request(`${base}/rama/`); return (res || []).map(mapRama) }
async function listarCargos() { const res = await request(`${base}/cargo/`); return (res || []).map(mapCargo) }
async function listarNiveles() { const res = await request(`${base}/nivel/`); return (res || []).map(mapNivel) }
async function listarEstadosCiviles() { const res = await request(`${base}/estado-civil/`); return (res || []).map(mapEstadoCivil) }
async function listarRoles() { const res = await request(`${base}/rol/`); return (res || []).map(mapRol) }
async function listarConceptosContables() { const res = await request(`${base}/concepto-contable/`); return (res || []).map(mapConceptoContable) }
async function listarTiposArchivo() { const res = await request(`${base}/tipo-archivos/`); return (res || []).map(mapTipoArchivo) }
async function listarTiposCurso() { const res = await request(`${base}/tipo-cursos/`); return (res || []).map(mapTipoCurso) }

export default {
  listarZonas,
  listarDistritos,
  listarGrupos,
  listarRegiones,
  listarProvincias,
  listarComunas,
  listarRamas,
  listarCargos,
  listarNiveles,
  listarEstadosCiviles,
  listarRoles,
  listarConceptosContables,
  listarTiposArchivo,
  listarTiposCurso,
}

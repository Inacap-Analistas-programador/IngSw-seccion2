import { describe, it, expect, vi, onMounted } from 'vitest'
import { mount } from '@vue/test-utils'
import FormularioDatosCurso from '../formulario/FormularioDatosCurso.vue'
import { cursos as cursosService } from '@/services/cursosService'

// Mock the service
vi.mock('@/services/cursosService', () => ({
    cursos: {
        list: vi.fn(() => Promise.resolve({
            results: [{ cus_id: 1, cus_descripcion: 'Curso Test' }]
        })),
        getSecciones: vi.fn(() => Promise.resolve([
            { cus_id: 101, cus_descripcion: 'Seccion 1' }
        ]))
    }
}))

describe('FormularioDatosCurso', () => {
    it('renders and loads courses on mount', async () => {
        const wrapper = mount(FormularioDatosCurso, {
            props: {
                cursoSeleccionado: '',
                'onUpdate:cursoSeleccionado': (e) => wrapper.setProps({ cursoSeleccionado: e }),
                seccionCurso: '',
                'onUpdate:seccionCurso': (e) => wrapper.setProps({ seccionCurso: e })
            },
            global: {
                stubs: {
                    AppIcons: true,
                    BaseButton: true
                }
            }
        })

        // Wait for internal promises
        await new Promise(resolve => setTimeout(resolve, 0))

        expect(cursosService.list).toHaveBeenCalled()
        // Verify one of the options exist (need to check template structure)
    })

    it('updates seccionCurso and emits event when changed', async () => {
        const wrapper = mount(FormularioDatosCurso, {
            props: {
                cursoSeleccionado: '1',
                seccionCurso: ''
            }
        })

        // Simulate selecting a section
        const select = wrapper.find('#seccion')
        await select.setValue('101')

        expect(wrapper.emitted()).toHaveProperty('update:seccionCurso')
        expect(wrapper.emitted()).toHaveProperty('seccion-change')
    })
})

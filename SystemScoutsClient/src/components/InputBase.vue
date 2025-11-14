<script setup>
import { ref, computed, useSlots } from 'vue'

const props = defineProps({
    modelValue: [String, Number],
    label: { type: String, default: "" },
    placeholder: { type: String, default: "" },
    type: { type: String, default: "text" },
    rules: { type: String, default: "" }, // 'text'|'number'|'email'|'rut'
    required: { type: Boolean, default: false },
    id: { type: String, default: "" },
    // Permite inyectar un error externo (ej: desde el formulario)
    externalError: { type: String, default: "" }
})

const emit = defineEmits(["update:modelValue"])
const error = ref("")
const inputId = computed(() => props.id || `base-input-${Math.random().toString(36).slice(2,9)}`)
const slots = useSlots()
const hasAppend = computed(() => !!slots.append)

function validarRut(rut) {
    if (!rut || !/^[0-9]+-[0-9kK]{1}$/.test(rut)) return false
    // num will be mutated in the algorithm so use let and convert to Number
    let [num, dv] = rut.split("-")
    num = Number(num) || 0
    let M = 0, S = 1
    for (; num; num = Math.floor(num / 10)) S = (S + num % 10 * (9 - M++ % 6)) % 11
    return String(S ? S - 1 : "k") === dv.toLowerCase()
}

function validar(value) {
    if (props.required && !value) return "Campo requerido"
    if (props.rules === "number" && value && !/^[0-9]+$/.test(value)) return "Solo números"
    if (props.rules === "email" && value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(value)) return "Email inválido"
    if (props.rules === "rut" && value && !validarRut(value)) return "RUT inválido"
    return ""
}

function onInput(e) {
    const val = e.target.value
    emit("update:modelValue", val)
    error.value = validar(val)
}
</script>

<template>
    <div class="base-input">
        <label v-if="label" :for="inputId" class="base-label">{{ label }}</label>

        <div class="input-wrapper" :class="{ 'has-append': hasAppend }">
            <input
                :id="inputId"
                :type="type"
                :value="modelValue"
                :placeholder="placeholder"
                @input="onInput"
                class="base-field"
                :aria-invalid="(externalError || error) ? 'true' : 'false'"
            />

            <div v-if="hasAppend" class="input-append">
                <slot name="append" />
            </div>
        </div>

        <span v-if="externalError || error" class="base-error">{{ externalError || error }}</span>    
    </div>
</template>

<style scoped>
.base-input { display: block; width: 100%; margin-bottom: 0; }

/* etiqueta obligatoriamente en bloque -> garantiza que quede arriba */
.base-label { display: block; font-weight: 700; margin-bottom: 6px; color: var(--color-text); font-size: 14px; }

/* input ocupa 100% del ancho y caja con borde gris similar a la imagen */
.base-field {
    display: block;
    width: 100%;
    box-sizing: border-box;
    border: 1px solid var(--color-border);
    background: var(--color-surface);
    padding: 7px 9px; /* Ajustar altura para alineación con selects */
    font-size: 13px;
    color: var(--color-text);
    border-radius: 4px;
}

.input-wrapper { position: relative; }
.input-wrapper.has-append .base-field { padding-right: 40px; }
.input-append { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); display: flex; align-items: center; }

/* placeholder en mayúsculas y gris */
.base-field::placeholder { text-transform: uppercase; color: #9b9b9b; }

/* foco sutil que no desplace la etiqueta */
.base-field:focus { outline: none; border-color: var(--color-primary); }

/* mensaje de error bajo el input */
.base-error { color: #c0392b; font-size: 12px; margin-top: 4px; display: block; }

/* estado de error: borde rojo y halo sutil */
.base-field[aria-invalid="true"] {
    border-color: #dc2626;
}
.base-field[aria-invalid="true"]:focus {
    border-color: #dc2626;
    box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.1) inset;
}
</style>

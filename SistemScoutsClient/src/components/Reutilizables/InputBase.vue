<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
    modelValue: [String, Number],
    label: { type: String, default: "" },
    placeholder: { type: String, default: "" },
    type: { type: String, default: "text" },
    rules: { type: String, default: "" }, // 'text'|'number'|'email'|'rut'
    required: { type: Boolean, default: false },
    id: { type: String, default: "" }
})

const emit = defineEmits(["update:modelValue"])
const error = ref("")
const inputId = computed(() => props.id || `base-input-${Math.random().toString(36).slice(2,9)}`)

function validarRut(rut) {
    if (!rut || !/^[0-9]+-[0-9kK]{1}$/.test(rut)) return false
    const [num, dv] = rut.split("-")
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

        <input
            :id="inputId"
            :type="type"
            :value="modelValue"
            :placeholder="placeholder"
            @input="onInput"
            class="base-field"
        />

        <span v-if="error" class="base-error">{{ error }}</span>    
    </div>
</template>

<style scoped>
.base-input { display: block; width: 100%; margin-bottom: 12px; }

/* etiqueta obligatoriamente en bloque -> garantiza que quede arriba */
.base-label { display: block; font-weight: 700; margin-bottom: 6px; color: #111; font-size: 14px; }

/* input ocupa 100% del ancho y caja con borde gris similar a la imagen */
.base-field {
    display: block;
    width: 100%;
    box-sizing: border-box;
    border: 1px solid #d0d0d0;
    background: #fff;
    padding: 8px 10px;
    font-size: 13px;
    color: #222;
    border-radius: 2px;
}

/* placeholder en mayúsculas y gris */
.base-field::placeholder { text-transform: uppercase; color: #9b9b9b; }

/* foco sutil que no desplace la etiqueta */
.base-field:focus { outline: none; border-color: #9aa8b2; }

/* mensaje de error bajo el input */
.base-error { color: #c0392b; font-size: 12px; margin-top: 6px; display: block; }
</style>

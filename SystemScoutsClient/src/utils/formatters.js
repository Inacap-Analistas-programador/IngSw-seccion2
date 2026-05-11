/**
 * Convierte todas las claves de un objeto a mayúsculas.
 * Útil para compatibilidad con templates legacy que esperan UPPER_CASE.
 */
export const toUpperKeys = (obj) => {
    if (!obj || typeof obj !== 'object') return obj;
    const newObj = Array.isArray(obj) ? [] : {};
    for (const key in obj) {
        const upperKey = key.toUpperCase();
        newObj[upperKey] = obj[key];
        // Mantener la clave original si es diferente (para evitar romper lógica que use snake_case)
        if (upperKey !== key) newObj[key] = obj[key];

        // Si es un objeto anidado, procesarlo recursivamente (opcional, dependiendo de la profundidad necesaria)
        if (obj[key] && typeof obj[key] === 'object' && !Array.isArray(obj[key]) && key !== 'estado_aprobacion') {
            // newObj[upperKey] = toUpperKeys(obj[key]);
        }
    }
    return newObj;
};

/**
 * Valida un RUT chileno (con o sin puntos/guión)
 */
export const validarRutChileno = (rut, dv) => {
    if (!rut || !dv) return false;

    const rutString = String(rut).replace(/\./g, '').replace(/[^0-9]/g, '');
    const rutNumerico = parseInt(rutString);
    if (isNaN(rutNumerico) || rutString === '') return false;

    let suma = 0;
    let multiplicador = 2;

    for (let i = rutString.length - 1; i >= 0; i--) {
        suma += parseInt(rutString[i]) * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
    }

    const resto = suma % 11;
    let dvCalculado = 11 - resto;

    if (dvCalculado === 11) dvCalculado = '0';
    else if (dvCalculado === 10) dvCalculado = 'K';
    else dvCalculado = dvCalculado.toString();

    return String(dv).toUpperCase() === dvCalculado;
};

/**
 * Calcula el DV de un RUT chileno
 */
export const calcularDv = (rut) => {
    if (!rut) return '';

    const rutLimpio = rut.toString().replace(/\./g, '').replace(/-/g, '').replace(/[^0-9]/g, '');
    const rutNumerico = parseInt(rutLimpio);

    if (isNaN(rutNumerico)) return '';

    let suma = 0;
    let multiplicador = 2;

    const rutString = rutNumerico.toString();
    for (let i = rutString.length - 1; i >= 0; i--) {
        suma += parseInt(rutString[i]) * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
    }

    const resto = suma % 11;
    let dvCalculado = 11 - resto;

    if (dvCalculado === 11) return '0';
    else if (dvCalculado === 10) return 'K';
    else return dvCalculado.toString();
};

/**
 * Valida formato de email básico
 */
export const validarEmail = (email) => {
    if (!email) return true;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

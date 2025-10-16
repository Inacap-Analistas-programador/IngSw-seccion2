<!-- 
=========================================
 VISTA PRINCIPAL: Gestión de Pagos
 Sistema Scouts Región del Biobío
 Desarrollado con Vue 3 + Vite
-----------------------------------------
 Descripción:
 Pantalla que permite la carga individual y grupal 
 de comprobantes de pago, así como la validación 
 de estados por parte de los administradores.

 Autor: [Tu Nombre o Equipo]
 Fecha: [Actualizar según entrega]
=========================================
-->

<template>
  <div class="pagos-container">
    <!-- ENCABEZADO PRINCIPAL -->
    <div class="pagos-header">
      <h2>7. Gestión de Pagos</h2>
      <p>Gestión de Comprobantes de Pago</p>
    </div>

    <!-- SECCIÓN 1: CARGA INDIVIDUAL -->
    <section class="pagos-individual">
      <h3>Carga Individual</h3>

      <!-- Buscador por RUT -->
      <div class="pagos-individual-row">
        <input 
          type="text" 
          placeholder="Buscar por RUT (ej: 12.345.678-9)" 
          class="pagos-input" 
        />
        <button class="btn-buscar">Buscar</button>
      </div>

      <!-- Resultado y carga de comprobante -->
      <div class="pagos-individual-content">
        <div class="pagos-datos-personales">
          <strong>Datos del Participante</strong><br>
          <span>Nombre:</span> JUAN PÉREZ GONZÁLEZ<br>
          <span>RUT:</span> 12.345.678-9<br>
          <span>Curso:</span> Formación de Dirigentes<br>
          <span>Estado Pago:</span>
          <span class="badge-pendiente">Pendiente</span>
        </div>

        <!-- Subida de comprobante -->
        <div class="pagos-comprobante">
          <strong>Cargar Comprobante</strong>
          <div class="upload-box">
            <span>📎 Arrastra el archivo aquí o haz clic para seleccionar</span><br>
            <input type="file" id="fileIndividual" style="margin:10px 0;" />
            <button class="btn-file">Subir Comprobante</button>
          </div>
        </div>
      </div>
    </section>

    <!-- SECCIÓN 2: CARGA GRUPAL -->
    <section class="pagos-grupal">
      <h3>Carga Grupal</h3>

      <!-- Tabla de participantes -->
      <table>
        <thead>
          <tr>
            <th></th>
            <th>Nombre</th>
            <th>RUT</th>
            <th>Curso</th>
            <th>Estado Pago</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><input type="checkbox" /></td>
            <td>MARÍA GONZÁLEZ LÓPEZ</td>
            <td>98.765.432-1</td>
            <td>Formación de Dirigentes</td>
            <td><span class="badge-pendiente">Pendiente</span></td>
          </tr>
          <tr>
            <td><input type="checkbox" /></td>
            <td>CARLOS RAMÍREZ SOTO</td>
            <td>11.222.333-4</td>
            <td>Formación de Dirigentes</td>
            <td><span class="badge-pendiente">Pendiente</span></td>
          </tr>
          <tr>
            <td><input type="checkbox" /></td>
            <td>ANA TORRES MUÑOZ</td>
            <td>22.333.444-5</td>
            <td>Formación de Dirigentes</td>
            <td><span class="badge-confirmado">Confirmado</span></td>
          </tr>
        </tbody>
      </table>

      <!-- Subida de comprobante grupal -->
      <div class="upload-box-grupal">
        <span>📎 Comprobante grupal - Arrastra el archivo aquí</span><br />
        <input type="file" id="fileGrupal" style="margin:10px 0;" />
        <button class="btn-file">Asociar Comprobante a Seleccionados</button>
      </div>
    </section>

    <!-- SECCIÓN 3: ACCIONES DE ADMINISTRADOR -->
    <section class="pagos-acciones">
      <h3>Acciones de Pago</h3>
      <button class="btn-confirmar">Confirmar Pagos</button>
      <button class="btn-rechazar">Rechazar Pagos</button>
      <button class="btn-pendiente">Marcar como Pendiente</button>
      <button class="btn-exportar">Exportar Lista de Pagos</button>
    </section>
  </div>
</template>

<!-- ============================================================= -->
<!-- ======================= ESTILOS CSS ========================== -->
<!-- ============================================================= -->
<style scoped>
/* ======== Contenedor general ======== */
.pagos-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 9px rgba(44, 90, 160, 0.12);
  font-family: 'Segoe UI', Arial, sans-serif;
  margin: 20px auto;
  padding: 20px 18px 32px 18px;
  max-width: 900px;
}

/* ======== Encabezado ======== */
.pagos-header h2 {
  background: #2c5aa0;
  color: white;
  padding: 7px 16px;
  border-radius: 9px;
  font-size: 1.16rem;
}
.pagos-header p {
  margin: 8px 0 12px;
  font-size: 1.1em;
  font-weight: 600;
}

/* ======== Secciones ======== */
section {
  margin-bottom: 20px;
}
h3 {
  font-size: 1.07em;
  color: #2c5aa0;
  border-bottom: 2px solid #bddafc;
  margin-bottom: 12px;
  padding-bottom: 4px;
  font-weight: 700;
}

/* ======== Carga individual ======== */
.pagos-individual-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}
.pagos-input {
  flex: 1;
  padding: 7px 10px;
  border: 1px solid #bbcde7;
  border-radius: 6px;
}
.btn-buscar,
.btn-file {
  background: #2c5aa0;
  color: white;
  padding: 7px 18px;
  border: none;
  border-radius: 6px;
  margin-left: 8px;
  font-size: 1em;
}

/* ======== Bloques internos ======== */
.pagos-individual-content {
  display: flex;
  gap: 24px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}
.pagos-datos-personales,
.pagos-comprobante {
  background: #f7faff;
  border-radius: 8px;
  padding: 15px 12px;
  min-width: 260px;
  font-size: 1em;
  border: 1px solid #bddafc;
}

/* ======== Badges de estado ======== */
.badge-pendiente {
  background: #fff4d9;
  color: #d3a001;
  padding: 2px 12px;
  border-radius: 14px;
  font-weight: bold;
  font-size: 0.95em;
}
.badge-confirmado {
  background: #d7ffe0;
  color: #209c40;
  padding: 2px 12px;
  border-radius: 14px;
  font-weight: bold;
  font-size: 0.95em;
}

/* ======== Cuadro de carga ======== */
.upload-box {
  background: #e5edf7;
  border: 1.5px dashed #bac7dc;
  border-radius: 9px;
  text-align: center;
  padding: 18px 10px;
  margin-top: 7px;
}

/* ======== Tabla grupal ======== */
.pagos-grupal table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 10px;
}
.pagos-grupal th,
.pagos-grupal td {
  padding: 7px 2px;
  text-align: left;
  background: #fff;
  font-size: 15px;
}
.pagos-grupal th {
  background: #e8eefa;
  font-weight: bold;
}
.pagos-grupal td {
  border-bottom: 1px solid #e3e3e3;
}
.upload-box-grupal {
  background: #e5edf7;
  border: 1.5px dashed #bac7dc;
  border-radius: 9px;
  text-align: center;
  padding: 14px 10px 18px 10px;
}

/* ======== Acciones ======== */
.pagos-acciones {
  display: flex;
  gap: 16px;
  margin-top: 12px;
  flex-wrap: wrap;
}
.btn-confirmar {
  background: #2cab53;
  color: white;
}
.btn-rechazar {
  background: #c12020;
  color: white;
}
.btn-pendiente {
  background: #e7b325;
  color: white;
}
.btn-exportar {
  background: #2c5aa0;
  color: white;
}
.pagos-acciones button {
  padding: 11px 26px;
  border: none;
  border-radius: 7px;
  font-weight: bold;
  font-size: 1em;
  margin-bottom: 6px;
  cursor: pointer;
  transition: filter 0.15s;
}
.pagos-acciones button:hover {
  filter: brightness(0.93);
}
</style>

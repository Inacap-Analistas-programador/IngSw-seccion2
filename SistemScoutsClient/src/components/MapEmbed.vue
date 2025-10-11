// Componente en Vue para incrustar un mapa interactivo interactivo usando Leaflet y OpenStreetMap...


<template>
  <div ref="mapContainer" style="height: 400px; width: 100%;"></div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  name: 'MapEmbed',
  props: {
    lat: {
      type: Number,
      required: true
    },
    lng: {
      type: Number,
      required: true
    },
    zoom: {
      type: Number,
      default: 13
    }
  },
  mounted() {
    // Inicializa el mapa centrado en las coordenadas dadas y con el nivel de zoom especificado
    this.map = L.map(this.$refs.mapContainer).setView([this.lat, this.lng], this.zoom)

    // Capa base OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map)

    // Marcador en la ubicación específica. Creo que deberia poder conectar aqui para otorgar una posicion manual.
    L.marker([this.lat, this.lng]).addTo(this.map)
      .bindPopup('Ubicación del curso/evento')
      .openPopup()
  }
}
</script>



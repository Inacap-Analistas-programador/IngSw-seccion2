<template>
  <div ref="mapContainer" style="height: 300px; width: 100%; border-radius: 8px;"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Solución para el icono por defecto de Leaflet
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: iconUrl,
  iconRetinaUrl: iconRetinaUrl,
  shadowUrl: shadowUrl,
});


const props = defineProps({
  lat: { type: [Number, String], default: -33.45694 }, // Coordenadas de Santiago por defecto
  lng: { type: [Number, String], default: -70.64827 },
  zoom: { type: Number, default: 13 }
});

const emit = defineEmits(['update:lat', 'update:lng']);

const mapContainer = ref(null);
let map = null;
let marker = null;

// Función para convertir a número de manera segura
const toNumber = (val) => {
  if (val === null || val === undefined || val === '') return null;
  const num = Number(val);
  return isNaN(num) ? null : num;
};

onMounted(() => {
  if (!mapContainer.value) return;

  const lat = toNumber(props.lat) || -33.45694;
  const lng = toNumber(props.lng) || -70.64827;

  map = L.map(mapContainer.value).setView([lat, lng], props.zoom);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  marker = L.marker([lat, lng], {
    draggable: true // Hacer el marcador arrastrable
  }).addTo(map);

  // Escuchar evento de arrastre del marcador
  marker.on('dragend', (event) => {
    const position = event.target.getLatLng();
    emit('update:lat', position.lat);
    emit('update:lng', position.lng);
  });

  // Escuchar clics en el mapa para mover el marcador
  map.on('click', (event) => {
    const position = event.latlng;
    marker.setLatLng(position);
    emit('update:lat', position.lat);
    emit('update:lng', position.lng);
  });
});

// Actualizar el mapa si las props cambian desde fuera
watch(() => [props.lat, props.lng], ([newLat, newLng], [oldLat, oldLng]) => {
  if (!map || !marker) return;
  
  const lat = toNumber(newLat);
  const lng = toNumber(newLng);
  const prevLat = toNumber(oldLat);
  const prevLng = toNumber(oldLng);
  
  // Solo actualizar si ambas coordenadas son válidas y han cambiado realmente
  if (lat !== null && lng !== null && (lat !== prevLat || lng !== prevLng)) {
    console.log('[MapEmbed] Actualizando mapa:', { lat, lng, prevLat, prevLng });
    const newLatLng = L.latLng(lat, lng);
    map.setView(newLatLng, props.zoom);
    marker.setLatLng(newLatLng);
  }
});

onUnmounted(() => {
  if (map) {
    map.remove();
  }
});
</script>


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
  marker.on('dragend', async (event) => {
    const position = event.target.getLatLng();
    emit('update:lat', position.lat);
    emit('update:lng', position.lng);
    await reverseGeocode(position.lat, position.lng);
  });

  // Escuchar clics en el mapa para mover el marcador
  map.on('click', async (event) => {
    const position = event.latlng;
    marker.setLatLng(position);
    emit('update:lat', position.lat);
    emit('update:lng', position.lng);
    await reverseGeocode(position.lat, position.lng);
  });
});

// Función de Geocodificación Inversa (Coordenadas -> Dirección)
async function reverseGeocode(lat, lng) {
  try {
    const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`;
    const response = await fetch(url, {
      headers: { 'Accept-Language': 'es' }
    });
    const data = await response.json();
    if (data && data.display_name) {
      emit('update:address', data.display_name);
    }
  } catch (error) {
    console.error('[MapEmbed] Error en reverse geocoding:', error);
  }
}

// Función de Geocodificación Directa (Dirección -> Coordenadas) - Expuesta al padre
async function buscarDireccion(query) {
  if (!query || query.length < 3) return null;
  
  try {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`;
    const response = await fetch(url, {
      headers: { 'Accept-Language': 'es' }
    });
    const data = await response.json();
    
    if (data && data.length > 0) {
      const result = data[0];
      const lat = parseFloat(result.lat);
      const lng = parseFloat(result.lon);
      
      const newLatLng = L.latLng(lat, lng);
      map.setView(newLatLng, 16); // Zoom más cercano al buscar una dirección específica
      marker.setLatLng(newLatLng);
      
      emit('update:lat', lat);
      emit('update:lng', lng);
      emit('update:address', result.display_name);
      
      return { lat, lng, address: result.display_name };
    }
  } catch (error) {
    console.error('[MapEmbed] Error en forward geocoding:', error);
  }
  return null;
}

// Exponer métodos para que el padre pueda usarlos (ej: buscar desde el input "Lugar")
defineExpose({
  buscarDireccion
});

// Actualizar el mapa si las props cambian desde fuera
watch(() => [props.lat, props.lng], ([newLat, newLng], [oldLat, oldLng]) => {
  if (!map || !marker) return;
  
  const lat = toNumber(newLat);
  const lng = toNumber(newLng);
  // ... resto del watcher igual ...
  // Solo actualizar si ambas coordenadas son válidas y han cambiado realmente
  if (lat !== null && lng !== null && (lat !== Number(oldLat) || lng !== Number(oldLng))) {
    const newLatLng = L.latLng(lat, lng);
    map.setView(newLatLng, map.getZoom()); // Mantener el zoom actual si es actualización externa
    marker.setLatLng(newLatLng);
  }
});

onUnmounted(() => {
  if (map) {
    map.remove();
  }
});
</script>


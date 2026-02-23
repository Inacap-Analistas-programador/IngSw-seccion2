<template>
  <div class="icon-explorer-bg">
    <div class="explorer-container">
      <header class="explorer-header">
        <div class="header-main">
          <AppIcons name="image" :size="32" class="title-icon" />
          <div>
            <h1>Explorador de Iconos</h1>
            <p>Visualiza y copia los nombres de los iconos disponibles en AppIcons.vue</p>
          </div>
        </div>
        
        <div class="search-wrapper">
          <AppIcons name="search" :size="20" class="search-icon" />
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar icono por nombre..." 
            class="search-input"
          />
          <span class="count-badge">{{ filteredIcons.length }} / {{ iconNames.length }}</span>
        </div>
      </header>

      <main class="icon-grid-scroll">
        <div class="icon-grid">
          <div 
            v-for="icon in filteredIcons" 
            :key="icon" 
            class="icon-card"
            @click="copyToClipboard(icon)"
            :title="'Click para copiar: ' + icon"
          >
            <div class="icon-preview">
              <AppIcons :name="icon" :size="32" />
            </div>
            <span class="icon-name">{{ icon }}</span>
          </div>
        </div>
      </main>

      <footer v-if="copiedIcon" class="toast-feedback">
        <AppIcons name="check-circle" :size="18" />
        <span>Copiado: <strong>{{ copiedIcon }}</strong></span>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import AppIcons from '@/components/icons/AppIcons.vue';

const searchQuery = ref('');
const copiedIcon = ref('');

const iconNames = [
  'search', 'plus', 'edit', 'trash', 'check', 'x', 'users', 'book', 'mail', 
  'alert-circle', 'download', 'send', 'credit-card', 'eye', 'eye-off', 
  'filter', 'ban', 'qrcode', 'calendar', 'chart-bar', 'settings', 
  'file-text', 'dollar-sign', 'clipboard', 'user', 'user-check', 'refresh', 
  'file', 'paperclip', 'check-circle', 'x-circle', 'chevron-up', 
  'chevron-left', 'chevron-right', 'chevron-down', 'arrow-up-down', 
  'view', 'add', 'modify', 'delete', 'lock', 'unlock', 'arrow-left', 
  'arrow-right', 'arrow-up', 'arrow-down', 'menu', 'home', 'image', 
  'camera', 'video', 'music', 'phone', 'message-circle', 'message-square', 
  'bell', 'bell-off', 'clock', 'sun', 'moon', 'cloud', 'heart', 'star', 
  'flag', 'bookmark', 'share', 'link', 'external-link', 'info', 
  'help-circle', 'check-square', 'square', 'radio', 'map-pin', 'map', 
  'compass', 'trending-up', 'trending-down', 'pie-chart', 'bar-chart', 
  'package', 'smartphone', 'tablet', 'laptop', 'watch', 'copy', 
  'scissors', 'printer', 'slash'
];

const filteredIcons = computed(() => {
  if (!searchQuery.value) return iconNames;
  const q = searchQuery.value.toLowerCase();
  return iconNames.filter(name => name.toLowerCase().includes(q));
});

const copyToClipboard = (name) => {
  navigator.clipboard.writeText(name).then(() => {
    copiedIcon.value = name;
    setTimeout(() => {
      if (copiedIcon.value === name) copiedIcon.value = '';
    }, 2000);
  });
};
</script>

<style scoped>
.icon-explorer-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 40px 20px;
  display: flex;
  justify-content: center;
}

.explorer-container {
  width: 100%;
  max-width: 1200px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  max-height: 90vh;
}

.explorer-header {
  padding: 30px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.header-main {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 25px;
}

.title-icon {
  color: #1a237e;
  background: #e8eaf6;
  padding: 12px;
  border-radius: 16px;
}

h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #1e293b;
  font-weight: 800;
}

p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 0.95rem;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 15px;
  color: #94a3b8;
}

.search-input {
  width: 100%;
  padding: 14px 15px 14px 45px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background: white;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
}

.search-input:focus {
  border-color: #1a237e;
  box-shadow: 0 0 0 4px rgba(26, 35, 126, 0.1);
}

.count-badge {
  position: absolute;
  right: 15px;
  font-size: 0.85rem;
  color: #94a3b8;
  font-weight: 500;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 20px;
}

.icon-grid-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
}

.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 20px;
}

.icon-card {
  background: white;
  border: 1px solid #f1f5f9;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  user-select: none;
}

.icon-card:hover {
  transform: translateY(-5px);
  border-color: #1a237e;
  box-shadow: 0 10px 25px rgba(26, 35, 126, 0.08);
}

.icon-card:active {
  transform: translateY(0);
}

.icon-preview {
  color: #475569;
  transition: color 0.3s ease;
}

.icon-card:hover .icon-preview {
  color: #1a237e;
}

.icon-name {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
  text-align: center;
  word-break: break-all;
}

.toast-feedback {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: #1e293b;
  color: white;
  padding: 12px 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from { transform: translate(-50%, 20px); opacity: 0; }
  to { transform: translate(-50%, 0); opacity: 1; }
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>

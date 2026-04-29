<template>
  <div v-if="visible" class="modal-overlay" @click.self="$emit('cancel')">
    <div class="modal-content glass-panel" style="max-width: 450px; text-align: center;">
      <h2>{{ title }}</h2>
      <p style="margin: 15px 0; color: #cbd5e1;">
        <slot>{{ message }}</slot>
      </p>
      <p v-if="subtitle" :style="{ marginBottom: '25px', color: subtitleColor, fontSize: '14px' }">
        {{ subtitle }}
      </p>
      <div class="modal-actions" style="justify-content: center;">
        <button type="button" class="btn-secondary" @click="$emit('cancel')">
          {{ cancelText }}
        </button>
        <button
          type="button"
          class="btn-primary confirm-dialog-action"
          :style="actionStyle"
          @click="$emit('confirm')"
        >
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  title: { type: String, default: 'Confirm Action' },
  message: { type: String, default: 'Are you sure?' },
  subtitle: { type: String, default: '' },
  confirmText: { type: String, default: 'Confirm' },
  cancelText: { type: String, default: 'Cancel' },
  variant: { type: String, default: 'danger' } // 'danger' | 'warning' | 'success'
})

defineEmits(['confirm', 'cancel'])

const variantColors = {
  danger: { bg: 'rgba(239, 68, 68, 0.2)', border: '#ef4444', text: '#ef4444' },
  warning: { bg: 'rgba(245, 158, 11, 0.2)', border: '#f59e0b', text: '#f59e0b' },
  success: { bg: 'rgba(16, 185, 129, 0.2)', border: 'var(--success-color)', text: 'var(--success-color)' }
}

const actionStyle = computed(() => {
  const v = variantColors[props.variant] || variantColors.danger
  return {
    background: v.bg,
    borderColor: v.border,
    color: v.text,
    border: `1px solid ${v.border}`
  }
})

const subtitleColor = computed(() => {
  if (props.variant === 'danger') return '#ef4444'
  if (props.variant === 'warning') return '#f59e0b'
  return '#94a3b8'
})
</script>

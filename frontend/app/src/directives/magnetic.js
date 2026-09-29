// v-magnetic - элемент слегка «притягивается» к курсору.
const finePointer = () => window.matchMedia('(hover: hover) and (pointer: fine)').matches
const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches

export const magnetic = {
  mounted(el, { value }) {
    if (!finePointer() || reducedMotion()) return
    const strength = typeof value === 'number' ? value : 0.35

    el._magMove = (e) => {
      const rect = el.getBoundingClientRect()
      const x = e.clientX - (rect.left + rect.width / 2)
      const y = e.clientY - (rect.top + rect.height / 2)
      el.style.transform = `translate3d(${x * strength}px, ${y * strength}px, 0)`
    }
    el._magLeave = () => {
      el.style.transform = ''
    }
    el.addEventListener('pointermove', el._magMove)
    el.addEventListener('pointerleave', el._magLeave)
  },
  unmounted(el) {
    el.removeEventListener('pointermove', el._magMove)
    el.removeEventListener('pointerleave', el._magLeave)
  },
}

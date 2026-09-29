// v-tilt - 3D-наклон карточки за курсором + координаты подсветки (--mx, --my).
const finePointer = () => window.matchMedia('(hover: hover) and (pointer: fine)').matches
const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches

export const tilt = {
  mounted(el, { value }) {
    const max = typeof value === 'number' ? value : 8

    el._tiltMove = (e) => {
      const rect = el.getBoundingClientRect()
      const px = (e.clientX - rect.left) / rect.width
      const py = (e.clientY - rect.top) / rect.height
      el.style.setProperty('--mx', `${px * 100}%`)
      el.style.setProperty('--my', `${py * 100}%`)
      if (!finePointer() || reducedMotion()) return
      el.style.transform = `perspective(900px) rotateX(${(0.5 - py) * max}deg) rotateY(${(px - 0.5) * max}deg) translateZ(0)`
    }
    el._tiltLeave = () => {
      el.style.transform = ''
    }
    el.addEventListener('pointermove', el._tiltMove)
    el.addEventListener('pointerleave', el._tiltLeave)
  },
  unmounted(el) {
    el.removeEventListener('pointermove', el._tiltMove)
    el.removeEventListener('pointerleave', el._tiltLeave)
  },
}

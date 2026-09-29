// v-reveal - появление элемента при прокрутке: v-reveal, v-reveal="'left'", v-reveal="{ variant, delay }"
let observer = null

function getObserver() {
  if (observer) return observer
  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue
        entry.target.classList.add('is-revealed')
        observer.unobserve(entry.target)
      }
    },
    { threshold: 0.12, rootMargin: '0px 0px -8% 0px' }
  )
  return observer
}

function apply(el, value) {
  const options = typeof value === 'string' ? { variant: value } : value || {}
  el.dataset.reveal = options.variant || 'up'
  if (options.delay) el.style.setProperty('--reveal-delay', `${options.delay}ms`)
}

export const reveal = {
  mounted(el, { value }) {
    apply(el, value)
    if (!('IntersectionObserver' in window)) {
      el.classList.add('is-revealed')
      return
    }
    getObserver().observe(el)
  },
  unmounted(el) {
    observer?.unobserve(el)
  },
}

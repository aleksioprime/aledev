<template>
  <canvas ref="canvasRef" class="signal-network" aria-hidden="true"></canvas>
</template>

<script setup>
// «Сигнальная сеть» — узлы-устройства дрейфуют, соединяются линиями,
// а по рёбрам бегут пакеты данных. Курсор — ещё один узел сети,
// клик по фону запускает волну пакетов от курсора.
import { onBeforeUnmount, onMounted, ref } from 'vue'

const canvasRef = ref(null)

const COLORS = ['34, 211, 238', '167, 139, 250', '190, 242, 100']
const LINK_DIST = 150
const MOUSE_DIST = 210

let ctx = null
let width = 0
let height = 0
let dpr = 1
let nodes = []
let packets = []
let rafId = 0
let visible = true
let lastSpawn = 0
const mouse = { x: -9999, y: -9999, active: false }
let io = null
let reducedMotion = false

function rand(min, max) {
  return Math.random() * (max - min) + min
}

function createNodes() {
  const count = Math.round(Math.min(90, Math.max(28, (width * height) / 16000)))
  nodes = Array.from({ length: count }, () => ({
    x: rand(0, width),
    y: rand(0, height),
    vx: rand(-0.18, 0.18),
    vy: rand(-0.18, 0.18),
    r: rand(1, 2.4),
    color: COLORS[Math.random() < 0.7 ? 0 : Math.random() < 0.7 ? 1 : 2],
    pulse: rand(0, Math.PI * 2),
  }))
}

function resize() {
  const canvas = canvasRef.value
  if (!canvas) return
  const rect = canvas.getBoundingClientRect()
  dpr = Math.min(window.devicePixelRatio || 1, 2)
  width = rect.width
  height = rect.height
  canvas.width = Math.round(width * dpr)
  canvas.height = Math.round(height * dpr)
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  createNodes()
  if (reducedMotion) draw(0)
}

function spawnPacket(from, to, color) {
  packets.push({ from, to, t: 0, speed: rand(0.008, 0.02), color: color || from.color })
}

function nearest(point, limit) {
  const result = []
  for (const n of nodes) {
    const d = Math.hypot(n.x - point.x, n.y - point.y)
    if (d < limit && n !== point) result.push({ n, d })
  }
  return result.sort((a, b) => a.d - b.d)
}

function step(time) {
  // движение узлов
  for (const n of nodes) {
    n.x += n.vx
    n.y += n.vy
    if (n.x < -20) n.x = width + 20
    if (n.x > width + 20) n.x = -20
    if (n.y < -20) n.y = height + 20
    if (n.y > height + 20) n.y = -20

    // лёгкое притяжение к курсору
    if (mouse.active) {
      const dx = mouse.x - n.x
      const dy = mouse.y - n.y
      const d = Math.hypot(dx, dy)
      if (d < MOUSE_DIST && d > 1) {
        n.x += (dx / d) * 0.25
        n.y += (dy / d) * 0.25
      }
    }
  }

  // периодически отправляем пакеты по случайным рёбрам
  if (time - lastSpawn > 220 && packets.length < 40) {
    lastSpawn = time
    const from = nodes[(Math.random() * nodes.length) | 0]
    const near = nearest(from, LINK_DIST)
    if (near.length) spawnPacket(from, near[(Math.random() * Math.min(3, near.length)) | 0].n)
  }

  packets = packets.filter((p) => {
    p.t += p.speed
    if (p.t >= 1) {
      // пакет «ретранслируется» дальше с некоторой вероятностью
      if (Math.random() < 0.55) {
        const next = nearest(p.to, LINK_DIST).filter(({ n }) => n !== p.from)
        if (next.length) spawnPacket(p.to, next[0].n, p.color)
      }
      p.to.pulse = 0
      return false
    }
    return true
  })
}

function draw(time) {
  ctx.clearRect(0, 0, width, height)

  // рёбра
  for (let i = 0; i < nodes.length; i++) {
    const a = nodes[i]
    for (let j = i + 1; j < nodes.length; j++) {
      const b = nodes[j]
      const d = Math.hypot(a.x - b.x, a.y - b.y)
      if (d > LINK_DIST) continue
      ctx.strokeStyle = `rgba(${a.color}, ${(1 - d / LINK_DIST) * 0.22})`
      ctx.lineWidth = 1
      ctx.beginPath()
      ctx.moveTo(a.x, a.y)
      ctx.lineTo(b.x, b.y)
      ctx.stroke()
    }
    if (mouse.active) {
      const d = Math.hypot(a.x - mouse.x, a.y - mouse.y)
      if (d < MOUSE_DIST) {
        ctx.strokeStyle = `rgba(34, 211, 238, ${(1 - d / MOUSE_DIST) * 0.5})`
        ctx.beginPath()
        ctx.moveTo(a.x, a.y)
        ctx.lineTo(mouse.x, mouse.y)
        ctx.stroke()
      }
    }
  }

  // узлы
  for (const n of nodes) {
    n.pulse += 0.04
    const glow = Math.max(0, 1 - n.pulse / 2)
    ctx.fillStyle = `rgba(${n.color}, ${0.55 + glow * 0.45})`
    ctx.beginPath()
    ctx.arc(n.x, n.y, n.r + glow * 2.5, 0, Math.PI * 2)
    ctx.fill()
    if (glow > 0) {
      ctx.strokeStyle = `rgba(${n.color}, ${glow * 0.6})`
      ctx.beginPath()
      ctx.arc(n.x, n.y, n.r + (1 - glow) * 14, 0, Math.PI * 2)
      ctx.stroke()
    }
  }

  // пакеты данных
  for (const p of packets) {
    const x = p.from.x + (p.to.x - p.from.x) * p.t
    const y = p.from.y + (p.to.y - p.from.y) * p.t
    const tx = p.from.x + (p.to.x - p.from.x) * Math.max(0, p.t - 0.12)
    const ty = p.from.y + (p.to.y - p.from.y) * Math.max(0, p.t - 0.12)
    const grad = ctx.createLinearGradient(tx, ty, x, y)
    grad.addColorStop(0, `rgba(${p.color}, 0)`)
    grad.addColorStop(1, `rgba(${p.color}, 0.95)`)
    ctx.strokeStyle = grad
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(tx, ty)
    ctx.lineTo(x, y)
    ctx.stroke()
    ctx.fillStyle = `rgba(${p.color}, 1)`
    ctx.beginPath()
    ctx.arc(x, y, 1.8, 0, Math.PI * 2)
    ctx.fill()
  }
}

function loop(time) {
  if (visible && !document.hidden) {
    step(time)
    draw(time)
  }
  rafId = requestAnimationFrame(loop)
}

function onPointerMove(e) {
  const rect = canvasRef.value.getBoundingClientRect()
  mouse.x = e.clientX - rect.left
  mouse.y = e.clientY - rect.top
  mouse.active = mouse.y >= 0 && mouse.y <= rect.height && mouse.x >= 0 && mouse.x <= rect.width
}

function onPointerLeave() {
  mouse.active = false
}

function onClick(e) {
  if (!mouse.active || e.target.closest('a, button, input, textarea')) return
  const origin = { x: mouse.x, y: mouse.y, color: COLORS[1], pulse: 0 }
  for (const { n } of nearest(origin, MOUSE_DIST * 1.3).slice(0, 8)) {
    spawnPacket(origin, n, COLORS[(Math.random() * 3) | 0])
  }
}

onMounted(() => {
  const canvas = canvasRef.value
  ctx = canvas.getContext('2d')
  reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  resize()
  window.addEventListener('resize', resize)

  if (reducedMotion) return

  io = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting
  })
  io.observe(canvas)
  window.addEventListener('pointermove', onPointerMove, { passive: true })
  window.addEventListener('pointerdown', onClick)
  document.addEventListener('pointerleave', onPointerLeave)
  rafId = requestAnimationFrame(loop)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId)
  io?.disconnect()
  window.removeEventListener('resize', resize)
  window.removeEventListener('pointermove', onPointerMove)
  window.removeEventListener('pointerdown', onClick)
  document.removeEventListener('pointerleave', onPointerLeave)
})
</script>

<style scoped>
.signal-network {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  -webkit-mask-image: radial-gradient(ellipse 80% 75% at 50% 45%, #000 40%, transparent 100%);
  mask-image: radial-gradient(ellipse 80% 75% at 50% 45%, #000 40%, transparent 100%);
}
</style>

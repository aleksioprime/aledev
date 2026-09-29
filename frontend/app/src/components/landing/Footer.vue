<template>
  <footer class="footer">
    <div class="shell">
      <div class="footer__top">
        <p class="footer__cta font-display">
          {{ t('footer.cta') }}
        </p>
        <a v-magnetic href="#contacts" class="footer__action" @click.prevent="scrollTo('contacts')">
          <Icon :path="mdiArrowTopRight" />
          <span class="footer__action-text">{{ t('footer.write') }}</span>
        </a>
      </div>

      <div class="footer__bottom">
        <span>© {{ year }} {{ t('footer.copyright') }}</span>
        <ul class="footer__socials">
          <li v-for="link in socials" :key="link.label">
            <a :href="link.href" target="_blank" rel="noopener noreferrer">{{ link.label }}</a>
          </li>
        </ul>
        <button type="button" class="footer__top-btn" @click="scrollTo('hero')">
          {{ t('footer.backToTop') }}
          <Icon :path="mdiArrowUp" />
        </button>
      </div>
    </div>

    <div class="wordmark font-display" aria-hidden="true">aledev</div>
  </footer>
</template>

<script setup>
import Icon from '@/components/ui/Icon.vue'
import { mdiArrowTopRight, mdiArrowUp } from '@mdi/js'
import { useI18n } from 'vue-i18n'
import { socials } from '@/common/constants/socials'

const { t } = useI18n()
const year = new Date().getFullYear()

function scrollTo(anchor) {
  const el = document.getElementById(anchor)
  if (!el) return
  const header = document.querySelector('.site-header')
  const offset = anchor === 'hero' ? 0 : header ? header.offsetHeight : 0
  const sectionPadding = el.classList.contains('section')
    ? Number.parseFloat(getComputedStyle(el).paddingTop) || 0
    : 0
  const gap = el.classList.contains('section') ? 24 : 0
  window.scrollTo({
    top: el.getBoundingClientRect().top + window.scrollY + sectionPadding - offset - gap + 1,
    behavior: 'smooth',
  })
}
</script>

<style scoped>
.footer {
  position: relative;
  overflow: hidden;
  padding-top: clamp(4rem, 8vw, 6rem);
  border-top: 1px solid var(--line);
}

.footer__top {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  padding-bottom: 3rem;
}

.footer__cta {
  max-width: 44rem;
  font-size: clamp(1.8rem, 4.5vw, 3.2rem);
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.footer__action {
  position: relative;
  display: grid;
  place-items: center;
  width: 9rem;
  height: 9rem;
  border-radius: 50%;
  background: var(--grad);
  background-size: 200% 100%;
  color: #05060a !important;
  font-weight: 800;
  text-align: center;
  transition: transform 0.5s var(--ease-out), background-position 0.6s ease;
}

.footer__action .icon {
  position: absolute;
  top: 1.6rem;
  font-size: 1.6rem;
  transition: transform 0.5s var(--ease-out);
}

.footer__action:hover {
  background-position: 100% 0;
}

.footer__action:hover .icon {
  transform: rotate(45deg);
}

.footer__action-text {
  margin-top: 1.2rem;
  font-size: 0.95rem;
}

.footer__bottom {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem 2rem;
  padding-block: 1.5rem;
  border-top: 1px solid var(--line);
  font-size: 0.88rem;
  color: var(--muted);
}

.footer__socials {
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.footer__socials a,
.footer__top-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  min-height: 2.5rem;
  transition: color 0.3s ease;
}

.footer__socials a::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0.45rem;
  height: 1px;
  background: var(--accent);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.5s var(--ease-out);
}

.footer__socials a:hover {
  color: var(--text);
}

.footer__socials a:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}

.footer__top-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  color: var(--muted);
}

.footer__top-btn:hover {
  color: var(--accent);
}

.wordmark {
  margin-bottom: -0.22em;
  font-size: clamp(5rem, 24vw, 22rem);
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.06em;
  text-align: center;
  color: transparent;
  -webkit-text-stroke: 1px rgb(255 255 255 / 0.08);
  background: linear-gradient(180deg, rgb(255 255 255 / 0.06), transparent 80%);
  -webkit-background-clip: text;
  background-clip: text;
  user-select: none;
}
</style>

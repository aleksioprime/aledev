<template>
  <section :id="sectionId" class="section">
    <div class="shell contact">
      <div class="contact__intro">
        <header class="section-head">
          <span v-reveal class="section-kicker">04 — {{ $t('contacts.kicker') }}</span>
          <h2 v-reveal="{ delay: 80 }" class="section-title">
            {{ $t('contacts.titleStart') }} <span class="text-gradient">{{ $t('contacts.titleAccent') }}</span>
          </h2>
          <p v-reveal="{ delay: 160 }" class="section-lead">{{ $t('contacts.lead') }}</p>
        </header>

        <ul class="channels">
          <li v-for="(ch, i) in channels" :key="ch.key" v-reveal="{ variant: 'left', delay: 200 + i * 90 }">
            <a :href="ch.href" :target="ch.key === 'email' ? undefined : '_blank'" rel="noopener noreferrer"
              class="channel">
              <span class="channel__icon">
                <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path :d="ch.icon" /></svg>
              </span>
              <span class="channel__text">
                <span class="channel__label font-mono">{{ $t(`contacts.${ch.key}`) }}</span>
                <span class="channel__value">{{ ch.label }}</span>
              </span>
              <Icon :path="mdiArrowTopRight" class="channel__arrow" />
            </a>
          </li>
        </ul>
      </div>

      <div v-reveal="{ variant: 'scale', delay: 120 }" class="form-card glass">
        <Transition name="swap" mode="out-in" @after-enter="handleTransitionAfterEnter">
          <form v-if="!success" key="form" class="form" novalidate @submit.prevent="submitForm">
            <input v-model="form.website" type="text" name="website" tabindex="-1" autocomplete="off" class="hp"
              aria-hidden="true" />

            <div class="kind" role="radiogroup" :aria-label="$t('contacts.kindLabel')">
              <button v-for="k in kinds" :key="k.value" type="button" role="radio" class="kind__btn"
                :class="{ 'is-active': form.kind === k.value }" :aria-checked="form.kind === k.value"
                @click="form.kind = k.value">
                <Icon :path="k.icon" />
                {{ $t(`contacts.kinds.${k.value}`) }}
              </button>
              <span class="kind__thumb" :class="{ 'is-right': form.kind === 'question' }"></span>
            </div>
            <p class="kind__hint">{{ $t(`contacts.kindHints.${form.kind}`) }}</p>

            <div class="row-2">
              <label class="field" :class="{ 'has-error': showErrors && errors.name }">
                <input v-model="form.name" type="text" autocomplete="name" placeholder=" " maxlength="100" />
                <span class="field__label">{{ $t('contacts.name') }}</span>
                <span v-if="showErrors && errors.name" class="field__error">{{ errors.name }}</span>
              </label>

              <label class="field" :class="{ 'has-error': showErrors && errors.email }">
                <input v-model="form.email" type="email" autocomplete="email" inputmode="email" placeholder=" "
                  maxlength="255" />
                <span class="field__label">{{ $t('contacts.email') }}</span>
                <span v-if="showErrors && errors.email" class="field__error">{{ errors.email }}</span>
              </label>
            </div>

            <label class="field">
              <input v-model="form.contact" type="text" autocomplete="tel" placeholder=" " maxlength="255" />
              <span class="field__label">{{ $t('contacts.contactField') }}</span>
            </label>

            <Transition name="expand">
              <div v-if="form.kind === 'order'" class="order">
                <div class="order__inner">
                <fieldset class="options">
                  <legend class="options__legend">{{ $t('contacts.serviceLabel') }}</legend>
                  <button v-for="key in FEEDBACK_SERVICES" :key="key" type="button" class="option"
                    :class="{ 'is-active': form.service === key }" :aria-pressed="form.service === key"
                    @click="form.service = form.service === key ? null : key">
                    {{ $t(`contacts.services.${key}`) }}
                  </button>
                </fieldset>

                <fieldset class="options">
                  <legend class="options__legend">{{ $t('contacts.budgetLabel') }}</legend>
                  <button v-for="key in FEEDBACK_BUDGETS" :key="key" type="button" class="option"
                    :class="{ 'is-active': form.budget === key }" :aria-pressed="form.budget === key"
                    @click="form.budget = form.budget === key ? null : key">
                    {{ $t(`contacts.budgets.${key}`) }}
                  </button>
                </fieldset>

                <label class="field">
                  <input v-model="form.deadline" type="text" placeholder=" " maxlength="100" />
                  <span class="field__label">{{ $t('contacts.deadline') }}</span>
                </label>
                </div>
              </div>
            </Transition>

            <label class="field field--area" :class="{ 'has-error': showErrors && errors.message }">
              <span class="field__box">
                <textarea v-model="form.message" rows="5" placeholder=" " :maxlength="MESSAGE_MAX"></textarea>
                <span class="field__label">{{ $t(`contacts.messageLabels.${form.kind}`) }}</span>
                <span class="field__counter font-mono">{{ form.message.length }}/{{ MESSAGE_MAX }}</span>
              </span>
              <span v-if="showErrors && errors.message" class="field__error">{{ errors.message }}</span>
            </label>

            <div class="captcha">
              <div ref="turnstileContainer" class="turnstile-widget"></div>
              <div v-if="captchaError" class="captcha__error">
                <span>{{ captchaError }}</span>
                <button type="button" class="captcha__refresh" @click="refreshTurnstile">
                  <Icon :path="mdiRefresh" />
                  {{ $t('contacts.refreshCaptcha') }}
                </button>
              </div>
            </div>

            <button v-magnetic="0.15" type="submit" class="btn btn-primary submit" :disabled="sending">
              <span v-if="sending" class="submit__spinner"></span>
              <template v-else>
                {{ $t('contacts.send') }}
                <Icon :path="mdiSend" />
              </template>
            </button>

            <p v-if="error" class="form__error">{{ error }}</p>
            <p class="form__note">{{ $t('contacts.note') }}</p>
          </form>

          <div v-else key="thanks" class="thanks">
            <svg class="thanks__check" viewBox="0 0 52 52" aria-hidden="true">
              <circle cx="26" cy="26" r="24" fill="none" />
              <path fill="none" d="M15 27l7 7 15-15" />
            </svg>
            <p class="thanks__text">{{ $t(`contacts.successByKind.${sentKind}`) }}</p>
            <button type="button" class="btn btn-ghost" @click="resetForm">{{ $t('contacts.sendAnother') }}</button>
          </div>
        </Transition>
      </div>
    </div>
  </section>
</template>

<script setup>
import Icon from '@/components/ui/Icon.vue'
import { mdiArrowTopRight, mdiBriefcaseOutline, mdiChatQuestionOutline, mdiRefresh, mdiSend } from '@mdi/js'
import { nextTick, onMounted, onUnmounted, ref, watch } from "vue"
import { useI18n } from "vue-i18n"
import { FEEDBACK_SERVICES, FEEDBACK_BUDGETS } from "@/common/constants/feedback"
import { contacts as contactInfo, socialIcons } from "@/common/constants/socials"

import { useFeedbackStore } from "@/stores/feedback";
const feedbackStore = useFeedbackStore();
const { t, locale } = useI18n();

const sectionId = "contacts"
const turnstileSiteKey = import.meta.env.VITE_TURNSTILE_SITE_KEY;

const channels = [
  { key: "email", label: contactInfo.email, href: `mailto:${contactInfo.email}`, icon: socialIcons.email },
  { key: "telegram", label: `@${contactInfo.telegram}`, href: `https://t.me/${contactInfo.telegram}`, icon: socialIcons.telegram },
  { key: "github", label: contactInfo.github, href: `https://github.com/${contactInfo.github}`, icon: socialIcons.github },
]
const sending = ref(false)

const MESSAGE_MAX = 4000
const kinds = [
  { value: "order", icon: mdiBriefcaseOutline },
  { value: "question", icon: mdiChatQuestionOutline },
]
const emptyForm = (kind = "order") => ({
  kind, name: "", email: "", contact: "", service: null, budget: null, deadline: "", message: "", website: "",
})
const form = ref(emptyForm());
const sentKind = ref("order")
const errors = ref({ name: null, email: null, message: null });

const success = ref(false)
const error = ref("")
const captchaError = ref("")
const showErrors = ref(false)
const turnstileToken = ref("")
const turnstileWidgetId = ref(null)
const turnstileContainer = ref(null)
const formStartedAt = ref(Date.now())

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/
const required = (v) => !!(v && v.trim()) || t("contacts.errors.required")
const minLength = (n) => (v) => (v || "").trim().length >= n || t("contacts.errors.minLength", { n })
const validators = {
  name: [required, minLength(2)],
  email: [required, (v) => EMAIL_RE.test((v || "").trim()) || t("contacts.errors.email")],
  message: [required, minLength(10)],
};

for (const field in validators) {
  watch(
    () => form.value[field],
    () => {
      if (showErrors.value) validateField(field)
    }
  );
}

function validateField(field) {
  errors.value[field] = null;
  for (const validate of validators[field]) {
    const result = validate(form.value[field]);
    if (result !== true) {
      errors.value[field] = result;
      break;
    }
  }
}

function validateForm() {
  let isValid = true;
  for (const field in errors.value) errors.value[field] = null;
  for (const field in validators) {
    for (const validate of validators[field]) {
      const result = validate(form.value[field]);
      if (result !== true) {
        errors.value[field] = result;
        isValid = false;
        break;
      }
    }
  }
  return isValid;
}

function waitForTurnstile(triesLeft = 50) {
  return new Promise((resolve, reject) => {
    const check = () => {
      if (window.turnstile) {
        resolve();
        return;
      }
      if (triesLeft <= 0) {
        reject(new Error("Turnstile load timeout"));
        return;
      }
      triesLeft -= 1;
      setTimeout(check, 100);
    };
    check();
  });
}

async function initTurnstile() {
  if (!turnstileSiteKey) {
    captchaError.value = t("contacts.captchaMisconfigured");
    return;
  }

  if (!document.querySelector('script[src*="challenges.cloudflare.com/turnstile"]')) {
    const script = document.createElement("script");
    script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
  }

  try {
    await waitForTurnstile();
    await nextTick();
    if (!turnstileContainer.value || !window.turnstile) return;

    if (turnstileWidgetId.value !== null) {
      window.turnstile.remove(turnstileWidgetId.value);
      turnstileWidgetId.value = null;
    }

    turnstileWidgetId.value = window.turnstile.render(turnstileContainer.value, {
      sitekey: turnstileSiteKey,
      callback: (token) => {
        turnstileToken.value = token;
        captchaError.value = "";
      },
      "expired-callback": () => {
        turnstileToken.value = "";
      },
      "error-callback": () => {
        turnstileToken.value = "";
        captchaError.value = t("contacts.captchaLoadFailed");
      },
    });
  } catch {
    captchaError.value = t("contacts.captchaLoadFailed");
  }
}

function resetTurnstile() {
  turnstileToken.value = "";
  if (turnstileWidgetId.value !== null && window.turnstile) {
    window.turnstile.reset(turnstileWidgetId.value);
  }
}

async function refreshTurnstile() {
  captchaError.value = "";
  destroyTurnstile();
  await initTurnstile();
}

function destroyTurnstile() {
  if (turnstileWidgetId.value !== null && window.turnstile) {
    window.turnstile.remove(turnstileWidgetId.value);
    turnstileWidgetId.value = null;
  }
  turnstileToken.value = "";
}

async function submitForm() {
  error.value = ""
  captchaError.value = ""
  showErrors.value = true

  if (!validateForm()) return;
  if (!turnstileToken.value) {
    captchaError.value = t("contacts.captchaRequired");
    return;
  }

  sending.value = true
  const f = form.value
  const isOrder = f.kind === "order"
  const result = await feedbackStore.sendFeedback({
    kind: f.kind,
    name: f.name.trim(),
    email: f.email.trim(),
    contact: f.contact.trim() || null,
    service: isOrder ? f.service : null,
    budget: isOrder ? f.budget : null,
    deadline: isOrder ? f.deadline.trim() || null : null,
    message: f.message.trim(),
    lang: locale.value,
    website: f.website,
    form_started_at: formStartedAt.value,
    captcha_token: turnstileToken.value,
  })
  sending.value = false

  if (!result) {
    error.value = t("contacts.error")
    resetTurnstile()
    return
  }

  sentKind.value = form.value.kind
  success.value = true
  destroyTurnstile()
}

function resetForm() {
  form.value = emptyForm(sentKind.value)
  formStartedAt.value = Date.now()
  captchaError.value = ""
  error.value = ""
  showErrors.value = false
  for (const field in errors.value) errors.value[field] = null
  success.value = false
}

async function handleTransitionAfterEnter() {
  if (success.value) return;
  await initTurnstile();
}

onMounted(async () => {
  await initTurnstile();
});

onUnmounted(() => {
  destroyTurnstile();
});

</script>

<style scoped>
.contact {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: clamp(2.5rem, 6vw, 5rem);
  align-items: start;
}

.channels {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
  border-top: 1px solid var(--line);
}

.channel {
  display: flex;
  align-items: center;
  gap: 1.1rem;
  padding: 1.15rem 0.25rem;
  border-bottom: 1px solid var(--line);
  transition: padding 0.5s var(--ease-out), background-color 0.3s ease;
}

.channel:hover {
  padding-left: 1rem;
  background: linear-gradient(90deg, rgb(34 211 238 / 0.06), transparent);
}

.channel__icon {
  display: grid;
  place-items: center;
  width: 2.8rem;
  height: 2.8rem;
  flex-shrink: 0;
  border: 1px solid var(--line-strong);
  border-radius: 50%;
  color: var(--accent);
}

.channel__icon svg {
  width: 1.15rem;
  height: 1.15rem;
}

.channel__text {
  display: flex;
  flex: 1;
  min-width: 0;
  flex-direction: column;
}

.channel__label {
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}

.channel__value {
  overflow: hidden;
  font-size: clamp(1rem, 2vw, 1.2rem);
  font-weight: 600;
  text-overflow: ellipsis;
}

.channel__arrow {
  font-size: 1.3rem;
  color: var(--muted);
  transition: transform 0.5s var(--ease-out), color 0.3s ease;
}

.channel:hover .channel__arrow {
  color: var(--accent);
  transform: rotate(45deg);
}

/* --- Форма --- */
.form-card {
  position: relative;
  padding: clamp(1.5rem, 4vw, 2.25rem);
  overflow: hidden;
}

.form-card::before {
  content: "";
  position: absolute;
  top: -40%;
  right: -30%;
  width: 70%;
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(circle, rgb(167 139 250 / 0.18), transparent 65%);
  pointer-events: none;
}

.form {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* --- Переключатель «Заказ / Вопрос» --- */
.kind {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 4px;
  border: 1px solid var(--line-strong);
  border-radius: 999px;
  background: rgb(6 7 11 / 0.6);
}

.kind__btn {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  min-height: 2.75rem;
  padding: 0.5rem 0.75rem;
  border-radius: 999px;
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--muted);
  transition: color 0.3s ease;
}

.kind__btn.is-active {
  color: #05060a;
}

.kind__thumb {
  position: absolute;
  top: 4px;
  bottom: 4px;
  left: 4px;
  width: calc(50% - 4px);
  border-radius: 999px;
  background: var(--grad);
  box-shadow: 0 8px 30px -8px rgb(34 211 238 / 0.6);
  transition: transform 0.5s var(--ease-out);
}

.kind__thumb.is-right {
  transform: translateX(100%);
}

.kind__hint {
  margin-top: -0.35rem;
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--muted);
  text-align: center;
}

.row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.order {
  display: grid;
  grid-template-rows: 1fr;
}

.order__inner {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-height: 0;
}

.options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin: 0;
  padding: 0;
  border: 0;
}

.options__legend {
  width: 100%;
  margin-bottom: 0.55rem;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}

.option {
  min-height: 2.25rem;
  padding: 0.4rem 0.85rem;
  border: 1px solid var(--line-strong);
  border-radius: 999px;
  font-size: 0.85rem;
  color: var(--text);
  transition: border-color 0.25s ease, background-color 0.25s ease, color 0.25s ease, transform 0.3s var(--ease-out);
}

.option:hover {
  border-color: rgb(34 211 238 / 0.6);
}

.option.is-active {
  border-color: var(--accent);
  background: rgb(34 211 238 / 0.14);
  color: #a5f3fc;
  transform: translateY(-1px);
}

.expand-enter-active,
.expand-leave-active {
  transition: opacity 0.35s ease, grid-template-rows 0.45s var(--ease-out), margin 0.45s var(--ease-out);
}

.expand-enter-active .order__inner,
.expand-leave-active .order__inner {
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  grid-template-rows: 0fr;
  margin-block: -0.5rem;
}

.form__note {
  font-size: 0.78rem;
  line-height: 1.5;
  color: rgb(255 255 255 / 0.4);
  text-align: center;
}

.hp {
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  opacity: 0;
}

.field {
  position: relative;
  display: block;
}

.field input,
.field textarea {
  display: block;
  width: 100%;
  padding: 1.45rem 1rem 0.6rem;
  border: 1px solid var(--line-strong);
  border-radius: 0.9rem;
  background: rgb(6 7 11 / 0.6);
  color: var(--text);
  font-size: 1rem;
  outline: none;
  resize: none;
  transition: border-color 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
}

.field input:focus,
.field textarea:focus {
  border-color: var(--accent);
  background: rgb(6 7 11 / 0.85);
  box-shadow: 0 0 0 4px rgb(34 211 238 / 0.12);
}

.field__box {
  position: relative;
  display: block;
}

.field__label {
  position: absolute;
  top: 1.05rem;
  left: 1rem;
  max-width: calc(100% - 2rem);
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  color: var(--muted);
  pointer-events: none;
  transform-origin: 0 0;
  transition: transform 0.35s var(--ease-out), color 0.3s ease;
}

.field input:focus + .field__label,
.field textarea:focus + .field__label,
.field input:not(:placeholder-shown) + .field__label,
.field textarea:not(:placeholder-shown) + .field__label {
  color: var(--accent);
  transform: translateY(-0.6rem) scale(0.75);
}

.field__counter {
  position: absolute;
  right: 0.9rem;
  bottom: 0.7rem;
  font-size: 0.7rem;
  color: rgb(255 255 255 / 0.3);
}

.field.has-error input,
.field.has-error textarea {
  border-color: #f87171;
  animation: shake 0.4s ease;
}

.field__error {
  display: block;
  margin-top: 0.35rem;
  padding-left: 0.25rem;
  font-size: 0.8rem;
  color: #f87171;
}

@keyframes shake {
  25% { transform: translateX(-5px); }
  50% { transform: translateX(5px); }
  75% { transform: translateX(-3px); }
}

.captcha {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
}

.turnstile-widget {
  display: flex;
  justify-content: center;
  min-height: 66px;
}

.captcha__error {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  font-size: 0.82rem;
  color: #f87171;
}

.captcha__refresh {
  display: inline-flex;
  min-height: 2.25rem;
  align-items: center;
  gap: 0.3rem;
  padding: 0.3rem 0.8rem;
  border: 1px solid rgb(34 211 238 / 0.4);
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--accent);
}

.submit {
  width: 100%;
  min-height: 3.2rem;
}

.submit:disabled {
  cursor: progress;
  opacity: 0.8;
}

.submit__spinner {
  width: 1.2rem;
  height: 1.2rem;
  border: 2px solid #05060a;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.form__error {
  text-align: center;
  font-size: 0.88rem;
  color: #f87171;
}

/* --- Успешная отправка --- */
.thanks {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.25rem;
  min-height: 22rem;
  text-align: center;
}

.thanks__check {
  width: 5rem;
  height: 5rem;
  stroke: var(--accent);
  stroke-width: 2.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.thanks__check circle {
  stroke-dasharray: 151;
  stroke-dashoffset: 151;
  animation: draw 0.8s var(--ease-out) forwards;
}

.thanks__check path {
  stroke-dasharray: 36;
  stroke-dashoffset: 36;
  animation: draw 0.5s var(--ease-out) 0.6s forwards;
}

@keyframes draw {
  to { stroke-dashoffset: 0; }
}

.thanks__text {
  font-size: 1.2rem;
  font-weight: 600;
}

.swap-enter-active,
.swap-leave-active {
  transition: opacity 0.4s ease, transform 0.5s var(--ease-out);
}

.swap-enter-from,
.swap-leave-to {
  opacity: 0;
  transform: translateY(12px);
}

@media (max-width: 900px) {
  .contact {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 520px) {
  .row-2 {
    grid-template-columns: 1fr;
  }

  .kind__btn {
    gap: 0.3rem;
    padding-inline: 0.4rem;
    font-size: 0.82rem;
  }

  .kind__btn .icon {
    display: none;
  }

  /* 16px+ в полях — iOS не будет зумить страницу при фокусе */
  .field input,
  .field textarea {
    font-size: 16px;
  }
}
</style>

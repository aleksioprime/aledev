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
              <span class="channel__arrow mdi mdi-arrow-top-right"></span>
            </a>
          </li>
        </ul>
      </div>

      <div v-reveal="{ variant: 'scale', delay: 120 }" class="form-card glass">
        <Transition name="swap" mode="out-in" @after-enter="handleTransitionAfterEnter">
          <form v-if="!success" key="form" class="form" novalidate @submit.prevent="submitForm">
            <input v-model="form.website" type="text" name="website" tabindex="-1" autocomplete="off" class="hp"
              aria-hidden="true" />

            <label class="field" :class="{ 'has-error': showErrors && errors.name, 'is-filled': form.name }">
              <input v-model="form.name" type="text" autocomplete="name" placeholder=" " />
              <span class="field__label">{{ $t('contacts.name') }}</span>
              <span v-if="showErrors && errors.name" class="field__error">{{ errors.name }}</span>
            </label>

            <label class="field" :class="{ 'has-error': showErrors && errors.email, 'is-filled': form.email }">
              <input v-model="form.email" type="email" autocomplete="email" placeholder=" " />
              <span class="field__label">{{ $t('contacts.email') }}</span>
              <span v-if="showErrors && errors.email" class="field__error">{{ errors.email }}</span>
            </label>

            <label class="field field--area" :class="{ 'has-error': showErrors && errors.message, 'is-filled': form.message }">
              <textarea v-model="form.message" rows="5" placeholder=" " maxlength="2000"></textarea>
              <span class="field__label">{{ $t('contacts.message') }}</span>
              <span class="field__counter font-mono">{{ form.message.length }}/2000</span>
              <span v-if="showErrors && errors.message" class="field__error">{{ errors.message }}</span>
            </label>

            <div class="captcha">
              <div ref="turnstileContainer" class="turnstile-widget"></div>
              <div v-if="captchaError" class="captcha__error">
                <span>{{ captchaError }}</span>
                <button type="button" class="captcha__refresh" @click="refreshTurnstile">
                  <span class="mdi mdi-refresh"></span>
                  {{ $t('contacts.refreshCaptcha') }}
                </button>
              </div>
            </div>

            <button v-magnetic="0.15" type="submit" class="btn btn-primary submit" :disabled="sending">
              <span v-if="sending" class="submit__spinner"></span>
              <template v-else>
                {{ $t('contacts.send') }}
                <span class="mdi mdi-send"></span>
              </template>
            </button>

            <p v-if="error" class="form__error">{{ error }}</p>
          </form>

          <div v-else key="thanks" class="thanks">
            <svg class="thanks__check" viewBox="0 0 52 52" aria-hidden="true">
              <circle cx="26" cy="26" r="24" fill="none" />
              <path fill="none" d="M15 27l7 7 15-15" />
            </svg>
            <p class="thanks__text">{{ $t('contacts.success') }}</p>
          </div>
        </Transition>
      </div>
    </div>
  </section>
</template>

<script setup>
import { nextTick, onMounted, onUnmounted, ref, watch } from "vue"
import { useI18n } from "vue-i18n"
import rules from "@/common/helpers/rules"
import { contacts as contactInfo, socialIcons } from "@/common/constants/socials"

import { useFeedbackStore } from "@/stores/feedback";
const feedbackStore = useFeedbackStore();
const { t } = useI18n();

const sectionId = "contacts"
const turnstileSiteKey = import.meta.env.VITE_TURNSTILE_SITE_KEY;

const channels = [
  { key: "email", label: contactInfo.email, href: `mailto:${contactInfo.email}`, icon: socialIcons.email },
  { key: "telegram", label: `@${contactInfo.telegram}`, href: `https://t.me/${contactInfo.telegram}`, icon: socialIcons.telegram },
  { key: "github", label: contactInfo.github, href: `https://github.com/${contactInfo.github}`, icon: socialIcons.github },
]
const sending = ref(false)

const form = ref({ name: "", email: "", message: "", website: "" });
const errors = ref({ name: null, email: null, message: null });

const success = ref(false)
const error = ref("")
const captchaError = ref("")
const showErrors = ref(false)
const turnstileToken = ref("")
const turnstileWidgetId = ref(null)
const turnstileContainer = ref(null)
const formStartedAt = ref(Date.now())

const validators = {
  name: [rules.required, rules.minLength(2)],
  email: [rules.required, rules.email],
  message: [rules.required, rules.minLength(10)],
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
  const result = await feedbackStore.sendFeedback({
    name: form.value.name,
    email: form.value.email,
    message: form.value.message,
    website: form.value.website,
    form_started_at: formStartedAt.value,
    captcha_token: turnstileToken.value,
  })
  sending.value = false

  if (!result) {
    error.value = t("contacts.error")
    resetTurnstile()
    return
  }

  success.value = true
  destroyTurnstile()

  setTimeout(() => {
    success.value = false
    form.value = { name: "", email: "", message: "", website: "" }
    formStartedAt.value = Date.now()
    captchaError.value = ""
    showErrors.value = false
    for (const field in errors.value) errors.value[field] = null
  }, 4000)
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

.field__label {
  position: absolute;
  top: 1.05rem;
  left: 1rem;
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
</style>

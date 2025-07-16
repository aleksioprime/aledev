<template>
  <section :id="sectionId" class="container mx-auto py-12 px-4 max-w-lg">
    <h2 class="text-2xl md:text-3xl font-bold mb-10 text-center tracking-tight">
      {{ $t('contacts.sectionTitle') }}
    </h2>

    <!-- Контакты отдельным блоком -->
    <div class="flex justify-center gap-8 mb-10">
      <a :href="`mailto:${contacts.email}`"
        class="group flex flex-col items-center text-neutral-300 hover:text-cyan-400 transition">
        <svg class="w-7 h-7 mb-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <rect x="3" y="5" width="18" height="14" rx="3" />
          <path d="M3 7l9 6 9-6" />
        </svg>
        <span class="text-xs font-medium">{{ contacts.email }}</span>
      </a>
      <a :href="`https://t.me/${contacts.telegram.replace('@', '')}`" target="_blank"
        class="group flex flex-col items-center text-neutral-300 hover:text-cyan-400 transition">
        <svg class="w-7 h-7 mb-1" fill="currentColor" viewBox="0 0 24 36" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M29.919 6.163l-4.225 19.925c-0.319 1.406-1.15 1.756-2.331 1.094l-6.438-4.744-3.106 2.988c-0.344 0.344-0.631 0.631-1.294 0.631l0.463-6.556 11.931-10.781c0.519-0.462-0.113-0.719-0.806-0.256l-14.75 9.288-6.35-1.988c-1.381-0.431-1.406-1.381 0.288-2.044l24.837-9.569c1.15-0.431 2.156 0.256 1.781 2.013z">
          </path>
        </svg>
        <span class="text-xs font-medium">{{ contacts.telegram }}</span>
      </a>
    </div>

    <!-- Только форма, с отдельным более светлым div -->
    <div class="bg-neutral-100/10 border !border-neutral-700 rounded-2xl shadow pa-6">
      <Transition name="fade" mode="out-in">
        <form v-if="!success" @submit.prevent="submitForm" class="flex flex-col" key="form">

          <input v-model="form.name" type="text" autocomplete="name" placeholder="Ваше имя"
            class="rounded-lg bg-neutral-900/70 border !border-neutral-700 px-4 py-2 focus:outline-none focus:!border-cyan-400 transition placeholder-neutral-400 text-neutral-100" />
          <div v-if="showErrors && errors.name" class="text-xs text-red-500 pt-2">{{ errors.name }}</div>

          <input v-model="form.email" type="email" autocomplete="email" placeholder="Email"
            class="rounded-lg bg-neutral-800 border !border-neutral-700 px-4 py-2 mt-3 focus:outline-none focus:!border-cyan-400 transition placeholder-neutral-400 text-neutral-100" />
          <div v-if="showErrors && errors.email" class="text-xs text-red-500 pt-2">{{ errors.email }}</div>

          <textarea v-model="form.message" rows="4" placeholder="Сообщение"
            class="rounded-lg bg-neutral-900 border !border-neutral-700 px-4 py-2 mt-3 focus:outline-none focus:!border-cyan-400 transition placeholder-neutral-400 text-neutral-100 resize-none" />
          <div v-if="showErrors && errors.message" class="text-xs text-red-500 pt-2">{{ errors.message }}</div>

          <button type="submit"
            class="mt-5 w-full rounded-lg !bg-cyan-400 hover:!bg-cyan-500 text-neutral-950 font-semibold py-2 transition">
            Отправить
          </button>

        </form>

        <div v-else class="mt-3 text-center !text-cyan-400 text-lg min-h-[120px] flex items-center justify-center" key="thanks">
          Спасибо! Ваше сообщение отправлено.
        </div>
      </Transition>

      <div v-if="error" class="mt-3 text-center text-red-500 text-sm">
        {{ error }}
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, watch } from "vue"
import rules from "@/common/helpers/rules"

import { useFeedbackStore } from "@/stores/feedback";
const feedbackStore = useFeedbackStore();

const sectionId = "contacts"

const contacts = ref({
  email: "alesemochkin@gmail.com",
  telegram: "@aleksioprime"
})

const form = ref({ name: "", email: "", message: "" });
const errors = ref({ name: null, email: null, message: null });

const success = ref(false)
const error = ref("")
const showErrors = ref(false)

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

async function submitForm() {
  error.value = ""
  showErrors.value = true

  if (!validateForm()) return;

  const result = await feedbackStore.sendFeedback({
    name: form.value.name,
    email: form.value.email,
    message: form.value.message,
  })

  if (!result) {
    error.value = "Ошибка отправки. Попробуйте ещё раз."
    return
  }

  success.value = true

  setTimeout(() => {
    success.value = false
    form.value = { name: "", email: "", message: "" }
    showErrors.value = false
    for (const field in errors.value) errors.value[field] = null
  }, 4000)
}

</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}
</style>
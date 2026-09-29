import { createI18n } from 'vue-i18n'

import headerRu from '@/common/locales/header/ru.json'
import heroRu from '@/common/locales/hero/ru.json'
import aboutRu from '@/common/locales/about/ru.json'
import mentoringRu from '@/common/locales/mentoring/ru.json'
import projectsRu from '@/common/locales/projects/ru.json'
import experienceRu from '@/common/locales/experience/ru.json'
import contactsRu from '@/common/locales/contacts/ru.json'
import footerRu from '@/common/locales/footer/ru.json'


import headerEn from '@/common/locales/header/en.json'
import heroEn from '@/common/locales/hero/en.json'
import aboutEn from '@/common/locales/about/en.json'
import mentoringEn from '@/common/locales/mentoring/en.json'
import projectsEn from '@/common/locales/projects/en.json'
import experienceEn from '@/common/locales/experience/en.json'
import contactsEn from '@/common/locales/contacts/en.json'
import footerEn from '@/common/locales/footer/en.json'



const messages = {
  ru: {
    header: headerRu,
    hero: heroRu,
    about: aboutRu,
    mentoring: mentoringRu,
    projects: projectsRu,
    experience: experienceRu,
    contacts: contactsRu,
    footer: footerRu,
  },
  en: {
    header: headerEn,
    hero: heroEn,
    about: aboutEn,
    mentoring: mentoringEn,
    projects: projectsEn,
    experience: experienceEn,
    contacts: contactsEn,
    footer: footerEn,
  }
}

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: 'ru',
  fallbackLocale: 'en',
  messages,
})

export default i18n
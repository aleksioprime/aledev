// Контакты для Hero, Contacts и Footer; иконки - path для viewBox 0 0 24 24
export const contacts = {
  email: 'alesemochkin@yandex.ru',
  telegram: 'aleksioprime',
  github: 'aleksioprime',
}

const icons = {
  github: 'M12 .5C5.73.5.5 5.74.5 12.02c0 5.08 3.29 9.39 7.86 10.91.58.1.79-.25.79-.56v-2c-3.2.7-3.87-1.37-3.87-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.19 1.76 1.19 1.03 1.76 2.69 1.25 3.35.96.1-.75.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.84 1.19 3.1 0 4.42-2.69 5.39-5.26 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.53 11.53 0 0 0 23.5 12.02C23.5 5.74 18.27.5 12 .5Z',
  telegram: 'M21.94 4.3 18.7 19.6c-.24 1.06-.87 1.32-1.76.82l-4.86-3.58-2.35 2.26c-.26.26-.48.48-.98.48l.35-4.95 9.01-8.14c.39-.35-.09-.54-.61-.19L6.37 13.3l-4.8-1.5c-1.04-.33-1.06-1.04.22-1.54L20.54 3.04c.87-.32 1.63.2 1.4 1.26Z',
  email: 'M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm1 2.3V17h16V7.3l-7.4 5.2a1 1 0 0 1-1.2 0L4 7.3ZM5.8 7l6.2 4.35L18.2 7H5.8Z',
}

export const socials = [
  { label: 'GitHub', href: `https://github.com/${contacts.github}`, icon: icons.github },
  { label: 'Telegram', href: `https://t.me/${contacts.telegram}`, icon: icons.telegram },
  { label: 'Email', href: `mailto:${contacts.email}`, icon: icons.email },
]

export { icons as socialIcons }

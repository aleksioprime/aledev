// Vuetify нужен только админ-панели. Загружаем его (JS, стили и шрифт иконок)
// лениво — при первом переходе на админский маршрут, чтобы не утяжелять лендинг.
let installing = null

export function installVuetify(app) {
  if (!installing) {
    installing = (async () => {
      const [{ createVuetify }, { aliases, mdi }] = await Promise.all([
        import('vuetify'),
        import('vuetify/iconsets/mdi'),
        import('vuetify/styles'),
        import('@mdi/font/css/materialdesignicons.css'),
      ])
      app.use(createVuetify({
        icons: {
          defaultSet: 'mdi',
          aliases,
          sets: { mdi },
        },
      }))
    })()
  }
  return installing
}

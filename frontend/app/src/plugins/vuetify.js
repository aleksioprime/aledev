// Vuetify только для админки: подключается при первом переходе на её маршрут
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

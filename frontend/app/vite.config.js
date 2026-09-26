import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'url'
import vuetify from 'vite-plugin-vuetify'
import tailwindcss from '@tailwindcss/vite'
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite'
import { dirname, resolve } from 'path'


// https://vite.dev/config/
const config = defineConfig({
	plugins: [
		vue(),
		vuetify({ autoImport: true }),
		tailwindcss(),
		VueI18nPlugin({
			include: resolve(
				dirname(fileURLToPath(import.meta.url)),
				'./src/common/locales/**'
			),
			// сообщения компилируются при сборке — компилятор vue-i18n в бандл не попадает
			runtimeOnly: true,
			compositionOnly: true,
			fullInstall: false,
		}),
	],
	server: {
		host: "0.0.0.0",
		port: 5173,
		proxy: {
			"^/(media)": {
				target: 'http://host.docker.internal:8501',
			}
		},
	},
	resolve: {
		alias: {
			'@': fileURLToPath(new URL('./src', import.meta.url)),
		},
	},
})

export default config

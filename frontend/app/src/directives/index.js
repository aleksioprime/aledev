import { reveal } from './reveal'
import { magnetic } from './magnetic'
import { tilt } from './tilt'

export default {
  install(app) {
    app.directive('reveal', reveal)
    app.directive('magnetic', magnetic)
    app.directive('tilt', tilt)
  },
}

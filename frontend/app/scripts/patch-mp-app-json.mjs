import { readFileSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

const appJsonPath = fileURLToPath(new URL('../dist/build/mp-weixin/app.json', import.meta.url))
const appJson = JSON.parse(readFileSync(appJsonPath, 'utf8'))

appJson.lazyCodeLoading = 'requiredComponents'
writeFileSync(appJsonPath, `${JSON.stringify(appJson, null, 2)}\n`)
console.log('[mp-weixin] injected lazyCodeLoading: requiredComponents')

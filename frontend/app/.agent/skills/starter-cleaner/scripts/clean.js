import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

/**
 * Recursively find the project root by looking for package.json
 * @param {string} dir - Current directory to check
 * @returns {string} - Path to the project root
 */
function findProjectRoot(dir) {
  if (fs.existsSync(path.join(dir, 'package.json'))) {
    return dir
  }
  const parentDir = path.dirname(dir)
  if (parentDir === dir) {
    throw new Error('Could not find project root (package.json not found)')
  }
  return findProjectRoot(parentDir)
}

const projectRoot = findProjectRoot(__dirname)

console.log(`Cleaning project at: ${projectRoot}`)

// 1. Remove Directories and Files
const pathsToRemove = [
  'src/subPages',
  'src/pages.json',
  'pnpm-workspace.yaml',
]

pathsToRemove.forEach((p) => {
  const fullPath = path.join(projectRoot, p)
  if (fs.existsSync(fullPath)) {
    console.log(`Removing: ${p}`)
    fs.rmSync(fullPath, { recursive: true, force: true })
  }
  else {
    console.log(`Skipping (not found): ${p}`)
  }
})

// 2. Modify vite.config.ts
const viteConfigPath = path.join(projectRoot, 'vite.config.ts')
if (fs.existsSync(viteConfigPath)) {
  console.log('Modifying vite.config.ts...')
  let content = fs.readFileSync(viteConfigPath, 'utf-8')

  // Remove from UniHelperPages configuration
  // Matches subPackages: [ ... ] structure
  const subPackagesRegex = /(subPackages:\s*\[)([\s\S]*?)(\])/
  const match = content.match(subPackagesRegex)

  if (match) {
    const subPackagesContent = match[2]
    // Remove lines containing subEcharts or subAsyncEcharts
    content = content.replace(subPackagesRegex, `$1${subPackagesContent}$3`)
    fs.writeFileSync(viteConfigPath, content, 'utf-8')
  }
}

// 3. Modify package.json
const packageJsonPath = path.join(projectRoot, 'package.json')
if (fs.existsSync(packageJsonPath)) {
  console.log('Modifying package.json...')
  const pkg = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'))

  // Remove docs scripts
  let scriptsChanged = false
  if (pkg.scripts) {
    Object.keys(pkg.scripts).forEach((key) => {
      if (key.startsWith('docs:')) {
        delete pkg.scripts[key]
        scriptsChanged = true
      }
    })
  }

  if (scriptsChanged) {
    fs.writeFileSync(packageJsonPath, `${JSON.stringify(pkg, null, 2)}\n`, 'utf-8')
  }
}

console.log('Cleanup complete!')

declare module 'virtual:uni-pages' {
  interface Page {
    path: string
    style?: Record<string, any>
    [key: string]: any
  }

  interface SubPackage {
    root: string
    pages: Page[]
    [key: string]: any
  }

  export const pages: Page[]
  export const subPackages: SubPackage[]
}

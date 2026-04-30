import process from 'node:process'
import Uni from '@uni-helper/plugin-uni'
import { isMpWeixin } from '@uni-helper/uni-env'
import UniHelperComponents from '@uni-helper/vite-plugin-uni-components'
import { WotResolver } from '@uni-helper/vite-plugin-uni-components/resolvers'
import UniHelperLayouts from '@uni-helper/vite-plugin-uni-layouts'
import UniHelperManifest from '@uni-helper/vite-plugin-uni-manifest'
import UniHelperPages from '@uni-helper/vite-plugin-uni-pages'
import Optimization from '@uni-ku/bundle-optimizer'
import UniKuRoot from '@uni-ku/root'
import { UniEchartsResolver } from 'uni-echarts/resolver'
import { UniEcharts } from 'uni-echarts/vite'
import UnoCSS from 'unocss/vite'
import AutoImport from 'unplugin-auto-import/vite'
import { defineConfig } from 'vite'
// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  // base: "/app",
  optimizeDeps: {
    exclude: process.env.NODE_ENV === 'development' ? ['wot-design-uni', 'uni-echarts'] : [],
  },
  plugins: [
    // https://github.com/uni-helper/vite-plugin-uni-manifest
    UniHelperManifest(),
    // https://github.com/uni-helper/vite-plugin-uni-pages
    UniHelperPages({
      dts: 'src/uni-pages.d.ts',
      subPackages: [
        'src/subPages',
      ],
      /**
       * 排除的页面，相对于 dir 和 subPackages
       * @default []
       */
      exclude: ['**/components/**/*.*'],
    }),
    // https://github.com/uni-helper/vite-plugin-uni-layouts
    UniHelperLayouts(),
    // https://github.com/uni-helper/vite-plugin-uni-components
    UniHelperComponents({
      resolvers: [WotResolver(), UniEchartsResolver()],
      dts: 'src/components.d.ts',
      dirs: ['src/components', 'src/business'],
      directoryAsNamespace: true,
    }),
    // https://github.com/uni-ku/root
    UniKuRoot(),
    // https://uni-echarts.xiaohe.ink
    UniEcharts(),
    // https://uni-helper.cn/plugin-uni
    Uni(),
    // https://github.com/uni-ku/bundle-optimizer
    Optimization({
      enable: isMpWeixin,
      logger: false,
    }),
    // https://github.com/antfu/unplugin-auto-import
    AutoImport({
      imports: ['vue', '@vueuse/core', 'pinia', 'uni-app', {
        from: '@wot-ui/router',
        imports: ['createRouter', 'useRouter', 'useRoute'],
      }, {
        from: 'wot-design-uni',
        imports: ['useToast', 'useMessage', 'useNotify', 'CommonUtil'],
      }, {
        from: 'alova/client',
        imports: ['usePagination', 'useRequest'],
      }],
      dts: 'src/auto-imports.d.ts',
      dirs: ['src/composables', 'src/store', 'src/utils', 'src/api'],
      vueTemplate: true,
    }),
    // https://github.com/antfu/unocss
    // see unocss.config.ts for config
    UnoCSS(),
  ],
})

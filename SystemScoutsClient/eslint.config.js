import { defineConfig, globalIgnores } from 'eslint/config'
import globals from 'globals'
import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'

export default defineConfig([
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,jsx,vue}'],
  },

  globalIgnores(['**/dist/**', '**/dist-ssr/**', '**/coverage/**']),

  {
    languageOptions: {
      globals: {
        ...globals.browser,
      },
    },
  },

  // Test files configuration
  {
    files: ['**/__tests__/**/*.{js,mjs,jsx}', '**/*.spec.{js,mjs,jsx}', '**/*.test.{js,mjs,jsx}'],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        describe: 'readonly',
        it: 'readonly',
        expect: 'readonly',
        beforeEach: 'readonly',
        afterEach: 'readonly',
        vi: 'readonly',
      },
    },
  },

  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  skipFormatting,
  
  // Custom rules
  {
    rules: {
      // Allow single-word component names for established components
      'vue/multi-word-component-names': 'off',
      // Allow empty catch blocks when they are intentionally empty (for error suppression)
      'no-empty': ['error', { allowEmptyCatch: true }],
    },
  },
])

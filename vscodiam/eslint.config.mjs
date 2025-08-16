import js from '@eslint/js';
import tseslint from '@typescript-eslint/eslint-plugin';
import globals from 'globals';

export default [
  js.configs.recommended,
  ...tseslint.configs['flat/recommended'],
  {
    languageOptions: {
      globals: {
        ...globals.node,
      },
    },
  },
];

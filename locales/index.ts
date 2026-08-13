import viCatalog from './translations/vi.json';
import enCatalog from './translations/en.json';
import jaCatalog from './translations/ja.json';

export type SupportedLocale = 'vi' | 'en' | 'ja';
export type TranslationCatalog = typeof viCatalog;

const catalogs: Record<SupportedLocale, TranslationCatalog> = {
  vi: viCatalog as TranslationCatalog,
  en: enCatalog as TranslationCatalog,
  ja: jaCatalog as TranslationCatalog,
};

export function getSupportedLocales(): SupportedLocale[] {
  return ['vi', 'en', 'ja'];
}

export function getCatalog(locale: SupportedLocale = 'vi'): TranslationCatalog {
  return catalogs[locale] || catalogs.en;
}

export function t(
  keyPath: string,
  locale: SupportedLocale = 'vi',
  params?: Record<string, string | number>
): string {
  const catalog = catalogs[locale] || catalogs.en;
  const keys = keyPath.split('.');
  let current: any = catalog;

  for (const k of keys) {
    if (current && typeof current === 'object' && k in current) {
      current = current[k];
    } else {
      return keyPath;
    }
  }

  if (typeof current === 'string' && params) {
    let result = current;
    for (const [pKey, pVal] of Object.entries(params)) {
      result = result.replace(new RegExp(`\\{${pKey}\\}`, 'g'), String(pVal));
    }
    return result;
  }

  return typeof current === 'string' ? current : keyPath;
}

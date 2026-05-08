import i18n from "@/locales";

export function translateRouteTitle(title: unknown): string {
  if (typeof title !== "string") return String(title);

  const key = `route.${title}`;
  if (i18n.global.te(key)) {
    const t = i18n.global.t as (key: string) => string;
    return t(key);
  }
  return title;
}

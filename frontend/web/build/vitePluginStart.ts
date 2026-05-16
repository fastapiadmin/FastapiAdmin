import type { PluginOption, ResolvedConfig } from "vite";
import pc from "picocolors";
import { BANNER } from "./banner";

const { green, blue, bold, dim, cyan, yellow, magenta } = pc;

const W = 96;
const ANSI_RE = new RegExp(String.fromCharCode(27) + "\\[\\d+(;\\d+)*m", "g");
const strip = (s: string) => s.replace(ANSI_RE, "");
const BANNER_LINES = BANNER.split("\n");
const row = (content: string) => {
  const pad = Math.max(0, W - strip(content).length - 1);
  return `  ${dim("│")} ${content}${" ".repeat(pad)}${dim("│")}`;
};

function printBanner(env: Record<string, string>, mode: string) {
  const line = dim("─".repeat(W));
  console.log(
    [
      "",
      `  ${dim("┌")}${line}${dim("┐")}`,
      row(""),
      row(`${bold(cyan("fastapiadmin"))}  ${bold(magenta(`v${env.VITE_VERSION || "3.0.0"}`))}`),
      row(""),
      ...BANNER_LINES.map((l) => row(green(l))),
      row(""),
      row(`${dim("mode")}     ${yellow(env.VITE_APP_ENV || mode)}`),
      row(`${dim("api")}      ${blue(env.VITE_API_BASE_URL || "")}`),
      row(`${dim("port")}     ${cyan(env.VITE_PORT || "")}`),
      row(""),
      `  ${dim("└")}${line}${dim("┘")}`,
      "",
    ].join("\n")
  );
}

export default function vitePluginStart(): PluginOption {
  return {
    name: "vite:start-banner",
    enforce: "pre",

    configResolved(resolvedConfig: ResolvedConfig) {
      const env = resolvedConfig.env as Record<string, string>;
      printBanner(env, resolvedConfig.mode);
    },
  };
}

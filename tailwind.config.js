/** @type {import("tailwindcss").Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        workspace: {
          bg: "rgb(var(--wx-workspace-bg) / <alpha-value>)",
          surface: "rgb(var(--wx-workspace-surface) / <alpha-value>)",
          shell: "rgb(var(--wx-workspace-shell) / <alpha-value>)",
          paper: "rgb(var(--wx-workspace-paper) / <alpha-value>)",
          border: "rgb(var(--wx-workspace-border) / <alpha-value>)",
          grid: "rgb(var(--wx-workspace-grid) / <alpha-value>)"
        },
        brand: {
          indigo: "rgb(var(--wx-brand-indigo) / <alpha-value>)",
          "indigo-soft": "rgb(var(--wx-brand-indigo-soft) / <alpha-value>)",
          emerald: "rgb(var(--wx-brand-emerald) / <alpha-value>)",
          "emerald-soft": "rgb(var(--wx-brand-emerald-soft) / <alpha-value>)",
          accent: "rgb(var(--wx-brand-accent) / <alpha-value>)"
        },
        ink: {
          DEFAULT: "rgb(var(--wx-ink) / <alpha-value>)",
          muted: "rgb(var(--wx-ink-muted) / <alpha-value>)",
          subtle: "rgb(var(--wx-ink-subtle) / <alpha-value>)",
          faint: "rgb(var(--wx-ink-faint) / <alpha-value>)"
        },
        neutral: {
          850: "#1f2937",
          925: "#0b1220",
          975: "#050812"
        }
      },
      fontFamily: {
        sans: [
          "Geist",
          "HarmonyOS Sans SC",
          "Microsoft YaHei",
          "PingFang SC",
          "ui-sans-serif",
          "system-ui",
          "sans-serif"
        ],
        editor: [
          "Geist",
          "HarmonyOS Sans SC",
          "Microsoft YaHei",
          "PingFang SC",
          "ui-sans-serif",
          "system-ui",
          "sans-serif"
        ],
        mono: [
          "Geist Mono",
          "JetBrains Mono",
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
          "monospace"
        ]
      },
      fontSize: {
        "ui-xs": ["0.75rem", { lineHeight: "1rem" }],
        "ui-sm": ["0.8125rem", { lineHeight: "1.25rem" }],
        "ui-base": ["0.9375rem", { lineHeight: "1.5rem" }],
        "editor-body": ["1rem", { lineHeight: "1.78" }],
        "editor-title": ["1.875rem", { lineHeight: "2.35rem", fontWeight: "700" }]
      },
      boxShadow: {
        paper: "0 28px 70px -46px rgba(15, 23, 42, 0.55), 0 0 0 1px rgba(15, 23, 42, 0.06)",
        shell: "0 18px 44px -32px rgba(15, 23, 42, 0.45), 0 1px 0 rgba(255, 255, 255, 0.85) inset",
        glass: "0 20px 54px -34px rgba(15, 23, 42, 0.42), 0 0 0 1px rgba(255, 255, 255, 0.62)",
        dropdown: "0 18px 42px -30px rgba(15, 23, 42, 0.48), 0 0 0 1px rgba(15, 23, 42, 0.08)",
        toolbar: "0 12px 32px -24px rgba(15, 23, 42, 0.5), 0 0 0 1px rgba(15, 23, 42, 0.08)",
        focus: "0 0 0 3px rgba(43, 55, 117, 0.14)"
      },
      borderRadius: {
        paper: "2px",
        menu: "10px",
        shell: "14px"
      }
    }
  },
  plugins: [
    require("daisyui"),
    require("@tailwindcss/typography"),
    require("tailwind-scrollbar-hide"),
    require("tailwind-scrollbar")
  ],
  daisyui: {
    themes: ["light"],
    base: false
  }
};

export interface RuntimeConfig {
  python?: string;
  nodejs?: string;
  ruby?: string;
  rust?: string;
  go?: string;
  bun?: string;
  java?: string;
  swift?: string;
}

export const runtimeDefaults: RuntimeConfig = {
  python: "3.12",
  nodejs: "20",
  ruby: "3.4.4",
  rust: "1.87.0",
  go: "1.23.8",
  bun: "1.2.14",
  java: "21",
  swift: "6.1",
};

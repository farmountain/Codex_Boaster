import { execSync } from 'child_process';
import { RuntimeConfig } from '../shared/runtime.config.schema';

function run(cmd: string): string {
  return execSync(cmd, { encoding: 'utf-8' });
}

export function validateRuntime(name: string, version: string): boolean {
  try {
    let command = '';
    switch (name) {
      case 'python':
        command = 'python3 --version';
        break;
      case 'nodejs':
        command = 'node --version';
        break;
      case 'ruby':
        command = 'ruby --version';
        break;
      case 'rust':
        command = 'rustc --version';
        break;
      case 'go':
        command = 'go version';
        break;
      case 'bun':
        command = 'bun --version';
        break;
      case 'java':
        command = 'java -version';
        break;
      case 'swift':
        command = 'swift --version';
        break;
      default:
        return false;
    }
    const output = run(command);
    return output.includes(version);
  } catch {
    return false;
  }
}

export function validateAll(cfg: RuntimeConfig): Record<string, boolean> {
  const result: Record<string, boolean> = {};
  for (const [lang, version] of Object.entries(cfg)) {
    if (!version) continue;
    result[lang] = validateRuntime(lang, version);
  }
  return result;
}

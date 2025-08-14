import * as vscode from 'vscode';
import { readFileSync } from 'fs';
import { join } from 'path';

export function getWebviewContent(webview: vscode.Webview, extensionUri: vscode.Uri): string {
  const outPath = vscode.Uri.joinPath(extensionUri, 'webview', 'out');
  const indexPath = join(outPath.fsPath, 'index.html');
  let html = readFileSync(indexPath, 'utf8');

  // Rewrite local asset URLs so VS Code can load them
  html = html.replace(/"\/_next\//g, `"${webview.asWebviewUri(vscode.Uri.joinPath(outPath, '_next'))}/`);
  return html;
}

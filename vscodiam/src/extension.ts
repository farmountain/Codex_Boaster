import * as vscode from 'vscode';
import { getWebviewContent } from './getWebviewContent';

export function activate(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand('boaster.open', () => {
    const panel = vscode.window.createWebviewPanel(
      'boaster',
      'Boaster',
      vscode.ViewColumn.One,
      {
        enableScripts: true,
        localResourceRoots: [vscode.Uri.joinPath(context.extensionUri, 'webview', 'out')]
      }
    );

    panel.webview.html = getWebviewContent(panel.webview, context.extensionUri);

    panel.webview.onDidReceiveMessage(async (message) => {
      switch (message.type) {
        case 'login':
          await context.globalState.update('token', message.token);
          return;
        case 'mcp-request':
          // TODO: wire to local MCP client
          return;
      }
    });
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}

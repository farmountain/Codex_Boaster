import * as vscode from 'vscode';

const isWeb = typeof navigator !== 'undefined';

export function activate(ctx: vscode.ExtensionContext) {
  const cmd = vscode.commands.registerCommand('boaster.prepareRelease', async () => {
    await vscode.window.showInformationMessage('Preparing release...');
    if (isWeb) {
      // Call backend via HTTP/MCP when running in web.
      return;
    }
    const ws = vscode.workspace.workspaceFolders?.[0]?.uri;
    if (!ws) {
      vscode.window.showErrorMessage('No workspace open');
      return;
    }
    const { signWorkspace } = await import('./slsa');
    await signWorkspace(ws);
    const choice = await vscode.window.showInformationMessage(
      'Artifact signed. Approve release?',
      'Approve',
      'Reject'
    );
    if (choice !== 'Approve') {
      vscode.window.showWarningMessage('Release aborted');
    }
  });
  ctx.subscriptions.push(cmd);
}

export function deactivate() {}

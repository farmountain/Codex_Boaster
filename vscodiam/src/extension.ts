import * as vscode from 'vscode';

const isWeb = typeof navigator !== 'undefined';

export function activate(ctx: vscode.ExtensionContext) {
  // Existing release signing flow
  const releaseCmd = vscode.commands.registerCommand('boaster.prepareRelease', async () => {
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
  ctx.subscriptions.push(releaseCmd);

  // Ticket-to-plan demonstration flow
  const ticketCmd = vscode.commands.registerCommand('boaster.ticketToPlan', async () => {
    const issue = await vscode.window.showQuickPick(
      ['Sample issue: Improve docs', 'Sample issue: Fix bug'],
      { placeHolder: 'Select an issue to plan' }
    );
    if (!issue) {
      return;
    }

    const approval = await vscode.window.showQuickPick(
      ['Approve task graph', 'Reject'],
      { placeHolder: `Approve generated plan for "${issue}"?` }
    );
    if (approval !== 'Approve task graph') {
      vscode.window.showInformationMessage('Plan rejected');
      return;
    }

    const ws = vscode.workspace.workspaceFolders?.[0];
    if (!ws) {
      vscode.window.showWarningMessage('No workspace open to apply diff');
      return;
    }

    const patchUri = vscode.Uri.joinPath(ws.uri, 'TICKET_PATCH.txt');
    const encoder = new TextEncoder();
    await vscode.workspace.fs.writeFile(
      patchUri,
      encoder.encode('Placeholder diff applied\n')
    );
    vscode.window.showInformationMessage(`Diff applied to ${patchUri.fsPath}`);
  });
  ctx.subscriptions.push(ticketCmd);
}

export function deactivate() {}

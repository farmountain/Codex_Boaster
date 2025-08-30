import * as vscode from 'vscode';

/** Generate a simple signed artifact for the workspace. */
export async function signWorkspace(uri: vscode.Uri): Promise<vscode.Uri> {
  const crypto = await import('crypto');
  const fs = await import('fs');
  const path = await import('path');
  const pkgPath = path.join(uri.fsPath, 'package.json');
  const data = fs.readFileSync(pkgPath);
  const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
  const sign = crypto.createSign('sha256');
  sign.update(data);
  sign.end();
  const signature = sign.sign(privateKey, 'base64');
  const sigUri = vscode.Uri.joinPath(uri, 'artifact.sig');
  fs.writeFileSync(sigUri.fsPath, signature);
  const pubUri = vscode.Uri.joinPath(uri, 'artifact.pub');
  fs.writeFileSync(pubUri.fsPath, publicKey.export({ type: 'spki', format: 'pem' }));
  return sigUri;
}

import { copyFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = join(__dirname, '..');
const personalSitePublic = join(rootDir, '..', 'personal-site', 'public');

function syncPdf() {
  const pdfName = 'Germán Küber.pdf';
  const sourcePath = join(rootDir, pdfName);
  const destPath = join(personalSitePublic, pdfName);

  console.log('Syncing PDF to personal-site...');

  if (!existsSync(sourcePath)) {
    console.error(`Source PDF not found: ${sourcePath}`);
    console.log('Run "npm run pdf" first to generate the PDF.');
    process.exit(1);
  }

  if (!existsSync(personalSitePublic)) {
    console.error(`Destination folder not found: ${personalSitePublic}`);
    process.exit(1);
  }

  copyFileSync(sourcePath, destPath);
  console.log(`PDF synced to: ${destPath}`);
}

syncPdf();

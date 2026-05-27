import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import puppeteer from 'puppeteer';

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = join(__dirname, '..');

async function generatePdf() {
  const htmlPath = join(rootDir, 'resume.html');
  const pdfPath = join(rootDir, 'Germán Küber.pdf');

  console.log('Generating PDF...');

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Set viewport to ensure desktop styles
  await page.setViewport({ width: 1200, height: 800 });

  // Load the HTML file using file:// protocol to support relative image paths
  await page.goto(`file://${htmlPath}`, {
    waitUntil: 'networkidle0'
  });

  // Generate PDF
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: {
      top: '8mm',
      right: '8mm',
      bottom: '8mm',
      left: '8mm'
    }
  });

  await browser.close();

  console.log(`PDF generated: ${pdfPath}`);
}

generatePdf().catch(console.error);

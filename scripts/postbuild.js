import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import fse from 'fs-extra';

// Get __dirname in ES6
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define source and destination paths relative to the root directory
const rootDir = path.join(__dirname, '..');
const distDir = path.join(rootDir, 'dist');
const templateDir = path.join(rootDir, 'taskite', 'templates');
const staticDir = path.join(rootDir, 'taskite', 'static');

// Ensure that the destination directories exist
fse.ensureDirSync(templateDir);
fse.ensureDirSync(staticDir);

// Move index.html to taskite/templates
const indexHtmlPath = path.join(distDir, 'index.html');
const destIndexHtmlPath = path.join(templateDir, 'index.html');
fse.moveSync(indexHtmlPath, destIndexHtmlPath, { overwrite: true });
console.log('Moved index.html to taskite/templates/');

// Move static files to taskite/static
const staticSrcDir = path.join(distDir, 'static');
fse.copySync(staticSrcDir, staticDir, { overwrite: true });
console.log('Copied static files to taskite/static/');

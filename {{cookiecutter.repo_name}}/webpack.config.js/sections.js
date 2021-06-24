const path = require('path');
const fs = require('fs');

function getSectionsJS () {
  const sectionsTemplates = path.resolve(__dirname, '../{{cookiecutter.package_name}}/apps/sections/templates/sections/types/')
  const sections = fs.readdirSync(sectionsTemplates);
  const sectionsJS = {}

  for (const section of sections) {
    const sectionDir = path.resolve(sectionsTemplates, section)
    if (!fs.lstatSync(sectionDir).isDirectory()) continue

    const indexFile = path.resolve(sectionDir, 'index.js')
    if (!(fs.existsSync(indexFile) && fs.lstatSync(indexFile).isFile())) continue

    sectionsJS[`section-${section}`] = indexFile
  }

  return sectionsJS
}

module.exports = {
  entries: getSectionsJS()
}

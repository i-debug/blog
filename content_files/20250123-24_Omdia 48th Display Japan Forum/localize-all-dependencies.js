#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🚀 开始本地化所有外部依赖...\n');

// 获取当前目录下所有HTML文件
const htmlFiles = fs.readdirSync('.').filter(file => file.endsWith('.html'));

console.log(`📁 找到 ${htmlFiles.length} 个HTML文件`);

let totalUpdated = 0;

htmlFiles.forEach(file => {
    console.log(`\n处理文件: ${file}`);
    
    // 读取文件内容
    let content = fs.readFileSync(file, 'utf8');
    const originalContent = content;
    let fileUpdated = false;
    
    // 1. 替换Tailwind CSS CDN链接
    const tailwindBefore = content;
    content = content.replace(
        /<script src="https:\/\/cdn\.tailwindcss\.com[^"]*"><\/script>/g,
        '<link rel="stylesheet" href="./output.css">'
    );
    if (content !== tailwindBefore) {
        console.log('  ✅ 更新了 Tailwind CSS');
        fileUpdated = true;
    }
    
    // 2. 替换Font Awesome CDN链接
    const fontAwesomeBefore = content;
    content = content.replace(
        /<link[^>]*href="https:\/\/cdnjs\.cloudflare\.com\/ajax\/libs\/font-awesome\/[^"]*\/css\/all\.min\.css"[^>]*>/g,
        '<link rel="stylesheet" href="./fontawesome/all.min.css">'
    );
    content = content.replace(
        /<link[^>]*href="https:\/\/[^"]*font-awesome[^"]*\.css"[^>]*>/g,
        '<link rel="stylesheet" href="./fontawesome/all.min.css">'
    );
    if (content !== fontAwesomeBefore) {
        console.log('  ✅ 更新了 Font Awesome');
        fileUpdated = true;
    }
    
    // 3. 替换Chart.js CDN链接
    const chartjsBefore = content;
    content = content.replace(
        /<script[^>]*src="https:\/\/cdn\.jsdelivr\.net\/npm\/chart\.js[^"]*"[^>]*><\/script>/g,
        '<script src="./chartjs/chart.umd.min.js"></script>'
    );
    content = content.replace(
        /<script[^>]*src="https:\/\/[^"]*chart[^"]*\.js"[^>]*><\/script>/g,
        '<script src="./chartjs/chart.umd.min.js"></script>'
    );
    content = content.replace(
        /<script[^>]*src="https:\/\/unpkg\.com\/chart\.js[^"]*"[^>]*><\/script>/g,
        '<script src="./chartjs/chart.umd.min.js"></script>'
    );
    if (content !== chartjsBefore) {
        console.log('  ✅ 更新了 Chart.js');
        fileUpdated = true;
    }
    
    // 如果内容有变化，写回文件
    if (content !== originalContent) {
        fs.writeFileSync(file, content, 'utf8');
        totalUpdated++;
        if (!fileUpdated) {
            console.log('  ✅ 文件已更新');
        }
    } else {
        console.log('  ⏭️  无需更新');
    }
});

console.log('\n' + '='.repeat(50));
console.log('✨ 本地化完成！');
console.log(`📊 总计更新了 ${totalUpdated} 个文件`);
console.log('\n📁 本地文件结构:');
console.log('├── output.css              (Tailwind CSS)');
console.log('├── fontawesome/            (Font Awesome)');
console.log('│   ├── all.min.css');
console.log('│   └── webfonts/');
console.log('└── chartjs/                (Chart.js)');
console.log('    └── chart.umd.min.js');
console.log('\n🚀 现在您的网站完全不依赖外部CDN了！');

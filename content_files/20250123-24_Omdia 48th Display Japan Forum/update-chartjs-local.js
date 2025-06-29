#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 获取当前目录下所有HTML文件
const htmlFiles = fs.readdirSync('.').filter(file => file.endsWith('.html'));

console.log(`找到 ${htmlFiles.length} 个HTML文件`);

htmlFiles.forEach(file => {
    console.log(`处理文件: ${file}`);
    
    // 读取文件内容
    let content = fs.readFileSync(file, 'utf8');
    
    // 替换Chart.js CDN链接为本地文件
    const originalContent = content;
    
    // 匹配各种版本的Chart.js CDN链接
    content = content.replace(
        /<script[^>]*src="https:\/\/cdn\.jsdelivr\.net\/npm\/chart\.js[^"]*"[^>]*><\/script>/g,
        '<script src="./chartjs/chart.umd.min.js"></script>'
    );
    
    // 也匹配其他可能的CDN链接格式
    content = content.replace(
        /<script[^>]*src="https:\/\/[^"]*chart[^"]*\.js"[^>]*><\/script>/g,
        '<script src="./chartjs/chart.umd.min.js"></script>'
    );
    
    // 匹配unpkg CDN
    content = content.replace(
        /<script[^>]*src="https:\/\/unpkg\.com\/chart\.js[^"]*"[^>]*><\/script>/g,
        '<script src="./chartjs/chart.umd.min.js"></script>'
    );
    
    // 如果内容有变化，写回文件
    if (content !== originalContent) {
        fs.writeFileSync(file, content, 'utf8');
        console.log(`✅ 已更新: ${file}`);
    } else {
        console.log(`⏭️  跳过: ${file} (未找到Chart.js CDN链接)`);
    }
});

console.log('\n✨ Chart.js本地化完成！');
console.log('📁 Chart.js文件位置: ./chartjs/');
console.log('📝 请确保部署时包含chartjs文件夹');

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
    
    // 替换Font Awesome CDN链接为本地文件
    const originalContent = content;
    
    // 匹配各种版本的Font Awesome CDN链接
    content = content.replace(
        /<link[^>]*href="https:\/\/cdnjs\.cloudflare\.com\/ajax\/libs\/font-awesome\/[^"]*\/css\/all\.min\.css"[^>]*>/g,
        '<link rel="stylesheet" href="./fontawesome/all.min.css">'
    );
    
    // 也匹配其他可能的CDN链接格式
    content = content.replace(
        /<link[^>]*href="https:\/\/[^"]*font-awesome[^"]*\.css"[^>]*>/g,
        '<link rel="stylesheet" href="./fontawesome/all.min.css">'
    );
    
    // 如果内容有变化，写回文件
    if (content !== originalContent) {
        fs.writeFileSync(file, content, 'utf8');
        console.log(`✅ 已更新: ${file}`);
    } else {
        console.log(`⏭️  跳过: ${file} (未找到Font Awesome CDN链接)`);
    }
});

console.log('\n✨ Font Awesome本地化完成！');
console.log('📁 Font Awesome文件位置: ./fontawesome/');
console.log('📝 请确保部署时包含fontawesome文件夹');

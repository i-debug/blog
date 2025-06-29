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
    
    // 替换Tailwind CSS CDN链接为本地文件
    const originalContent = content;
    content = content.replace(
        /<script src="https:\/\/cdn\.tailwindcss\.com[^"]*"><\/script>/g,
        '<link rel="stylesheet" href="./output.css">'
    );
    
    // 如果内容有变化，写回文件
    if (content !== originalContent) {
        fs.writeFileSync(file, content, 'utf8');
        console.log(`✅ 已更新: ${file}`);
    } else {
        console.log(`⏭️  跳过: ${file} (未找到CDN链接)`);
    }
});

console.log('\n✨ 批量更新完成！');
console.log('📝 请确保运行 npm run build-prod 来生成最新的CSS文件');

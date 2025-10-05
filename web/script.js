// StealthNovel 网站脚本

document.addEventListener('DOMContentLoaded', function() {
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // 下载按钮点击统计（可以连接到 Google Analytics）
    const downloadButtons = document.querySelectorAll('.download-btn');
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const type = this.getAttribute('data-type');
            console.log(`Download clicked: ${type}`);
            
            // 这里可以添加 Google Analytics 事件跟踪
            if (typeof gtag !== 'undefined') {
                gtag('event', 'download', {
                    'event_category': 'engagement',
                    'event_label': type
                });
            }
            
            // 显示提示
            alert('下载功能即将上线！\n\n请访问 GitHub 仓库下载源码，或自行编译。');
            e.preventDefault();
        });
    });

    // 响应式导航（移动端）
    const nav = document.querySelector('.nav');
    if (window.innerWidth <= 768) {
        nav.style.display = 'none';
        
        const menuButton = document.createElement('button');
        menuButton.textContent = '☰ 菜单';
        menuButton.style.cssText = `
            background: white;
            color: black;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        `;
        
        menuButton.addEventListener('click', function() {
            nav.style.display = nav.style.display === 'none' ? 'flex' : 'none';
        });
        
        document.querySelector('.header .container').appendChild(menuButton);
    }

    // 添加滚动动画效果
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // 观察所有需要动画的元素
    const animatedElements = document.querySelectorAll('.feature-card, .faq-item, .usage-step');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // 动态更新版本号（可以从 API 获取）
    const version = 'v1.0.0';
    document.querySelectorAll('.version').forEach(el => {
        el.textContent = `版本 ${version}`;
    });

    // 添加平台检测
    const platform = navigator.platform;
    if (!platform.includes('Win')) {
        const downloadSection = document.querySelector('.download');
        const warning = document.createElement('div');
        warning.style.cssText = `
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
            border: 1px solid #ffeaa7;
        `;
        warning.innerHTML = '<strong>⚠️ 注意：</strong> 检测到您的系统不是 Windows，本程序仅支持 Windows 10/11。';
        downloadSection.querySelector('.container').insertBefore(warning, downloadSection.querySelector('.download-cards'));
    }
});

// 添加返回顶部按钮
window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // 创建返回顶部按钮（如果不存在）
    let backToTop = document.getElementById('back-to-top');
    if (!backToTop) {
        backToTop = document.createElement('button');
        backToTop.id = 'back-to-top';
        backToTop.innerHTML = '↑';
        backToTop.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 24px;
            cursor: pointer;
            display: none;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: all 0.3s;
        `;
        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        document.body.appendChild(backToTop);
    }
    
    // 显示/隐藏按钮
    if (scrollTop > 300) {
        backToTop.style.display = 'block';
    } else {
        backToTop.style.display = 'none';
    }
});


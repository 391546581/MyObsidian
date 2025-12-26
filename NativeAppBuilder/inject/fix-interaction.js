/* 针对小红书移动 Web 版在 PC 上的特殊限制进行“物理消灭” */

(function () {
    const DEBUG = true;
    const log = (msg) => { if (DEBUG) console.log('[XHS-Fix] ' + msg); };

    const blastSelectors = [
        '.reds-modal', '.reds-mask', '.reds-alert-mask',
        '.login-modal', '.login-container',
        '.cover.mask', '.mask-paper',
        '[class*="Mask"]', '[class*="Modal"]', '[class*="login"]'
    ];

    const fix = () => {
        // 1. 强制解除滚动锁定类
        document.documentElement.classList.remove('reds-lock-scroll');
        document.body.classList.remove('reds-lock-scroll', 'no-scroll', 'fixed');

        // 2. 强制 Body、HTML 和关键容器溢出可见
        const forceScrollElements = [
            document.documentElement,
            document.body,
            document.getElementById('app'),
            document.getElementById('global'),
            document.querySelector('.layout.limit'),
            document.querySelector('.note-container')
        ];

        forceScrollElements.forEach(el => {
            if (el) {
                el.style.setProperty('overflow', 'auto', 'important');
                el.style.setProperty('overflow-y', 'auto', 'important');
                el.style.setProperty('height', 'auto', 'important');
                el.style.setProperty('position', 'static', 'important');
                el.style.setProperty('touch-action', 'auto', 'important');
                el.style.setProperty('pointer-events', 'auto', 'important');
            }
        });

        // 3. 彻底删除遮罩和模态框
        blastSelectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                // 只有当它是浮层时才删除
                const style = window.getComputedStyle(el);
                if (style.position === 'fixed' || style.position === 'absolute' || parseInt(style.zIndex) > 100) {
                    el.remove();
                    log('Removed blocker: ' + selector);
                }
            });
        });

        // 4. 特殊处理：移除导致无法滚动的 layout 限制
        const globalLayout = document.getElementById('global');
        if (globalLayout) {
            globalLayout.style.maxHeight = 'none';
        }
    };

    // 执行修复
    fix();

    // 监控动态变化
    const observer = new MutationObserver((mutations) => {
        fix();
    });
    observer.observe(document.documentElement, {
        attributes: true,
        childList: true,
        subtree: true,
        attributeFilter: ['class', 'style']
    });

    // 每一秒进行一次硬核复查
    setInterval(fix, 1000);

    log('Advanced Interaction Fix Injected.');
})();

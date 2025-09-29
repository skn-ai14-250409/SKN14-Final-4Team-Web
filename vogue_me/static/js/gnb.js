// GNB 탭 전환 기능
document.addEventListener('DOMContentLoaded', function() {
    const gnbTabs = document.querySelectorAll('.gnb-tab');
    const tabContents = document.querySelectorAll('.main-content > .tab-content-area');

    gnbTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();

            const targetTab = this.getAttribute('data-tab');

            // 모든 탭 비활성화
            gnbTabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => {
                content.classList.remove('active');
                setTimeout(() => {
                    content.style.display = 'none';
                }, 300);
            });

            // 선택된 탭 활성화
            this.classList.add('active');

            setTimeout(() => {
                const targetContent = document.getElementById(`${targetTab}-content`);
                if (targetContent) {
                    targetContent.style.display = 'block';
                    setTimeout(() => {
                        targetContent.classList.add('active');
                    }, 50);
                }
            }, 300);
        });
    });
});
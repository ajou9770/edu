function showTab(tabId) {
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => {
        content.style.display = 'none';
    });

    document.getElementById(tabId).style.display = 'block';
}

// 기본적으로 첫 번째 탭을 보여줍니다.
showTab('info1');

console.log("hello from history.js");

function initializeHistoryTabs() {
    const historyTab = document.querySelector('.history-tab');
    const statsTab = document.querySelector('.stats-tab');
    const historyContent = document.querySelector('.history-content');
    const statsContent = document.querySelector('.stats-content');

    function showHistory() {
        historyContent.style.display = 'block';
        statsContent.style.display = 'none';
        historyTab.style.backgroundColor = '#232b3f';
        statsTab.style.backgroundColor = '#131722';
    }

    function showStats() {
        historyContent.style.display = 'none';
        statsContent.style.display = 'block';
        historyTab.style.backgroundColor = '#131722';
        statsTab.style.backgroundColor = '#232b3f';
    }

    historyTab.addEventListener('click', showHistory);
    statsTab.addEventListener('click', showStats);

    showHistory();
}

export { initializeHistoryTabs };
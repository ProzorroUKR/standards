const CONSTANTS = {
    "RELEASE_ECRITERIA_ARTICLE_17": "2020-12-04T00:00:00+02:00",
    "CRITERIA_ARTICLE_16_REQUIRED": "2024-12-03T00:00:00+02:00"
};

async function loadJSON(url) {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (error) {
        console.error(`Error loading ${url}:`, error);
        return [];
    }
}

function createTable(criteria) {
    const table = document.createElement('div');
    table.className = 'table';
    
    const thead = document.createElement('div');
    thead.className = 'thead';
    
    const tbody = document.createElement('div');
    tbody.className = 'tbody';

    const headerRow = document.createElement('div');
    headerRow.className = 'tr';
    headerRow.innerHTML = `
        <div class="th">#</div>
        <div class="th">Criterion</div>
        <div class="th">Rules</div>
    `;
    thead.appendChild(headerRow);

    let rowNumber = 1;
    for (const [criterion, data] of Object.entries(criteria)) {
        const row = document.createElement('div');
        row.className = 'tr';
        row.innerHTML = `
            <div class="td">${rowNumber}</div>
            <div class="td th-criterion">${criterion}</div>
            <div class="td">${data.rules.join(', ')}</div>
        `;
        tbody.appendChild(row);
        rowNumber++;
    }

    table.appendChild(thead);
    table.appendChild(tbody);
    return table;
}

function createCriterionTable(fileData) {
    const table = document.createElement('div');
    table.className = 'table';
    
    const thead = document.createElement('div');
    thead.className = 'thead';
    
    const tbody = document.createElement('div');
    tbody.className = 'tbody';

    const headerRow = document.createElement('div');
    headerRow.className = 'tr';
    headerRow.innerHTML = `
        <div class="th">#</div>
        <div class="th">File</div>
        <div class="th">Rules</div>
    `;
    thead.appendChild(headerRow);

    let rowNumber = 1;
    for (const [file, periods] of Object.entries(fileData)) {
        const latestPeriod = periods[periods.length - 1];
        const row = document.createElement('div');
        row.className = 'tr';
        row.innerHTML = `
            <div class="td">${rowNumber}</div>
            <div class="td">${file}</div>
            <div class="td">${latestPeriod.rules.join(', ')}</div>
        `;
        tbody.appendChild(row);
        rowNumber++;
    }

    table.appendChild(thead);
    table.appendChild(tbody);
    return table;
}

async function displayRules() {
    const fileContent = document.getElementById('fileContent');
    const criterionContent = document.getElementById('criterionContent');
    document.querySelector('.loading').style.display = 'none';

    const files = {
        'aboveThreshold': await loadJSON('../criteria/rules/aboveThreshold.json'),
        'aboveThresholdEU': await loadJSON('../criteria/rules/aboveThresholdEU.json'),
        'aboveThresholdUA': await loadJSON('../criteria/rules/aboveThresholdUA.json'),
        'aboveThresholdUA.defense': await loadJSON('../criteria/rules/aboveThresholdUA.defense.json'),
        'belowThreshold': await loadJSON('../criteria/rules/belowThreshold.json'),
        'closeFrameworkAgreementUA': await loadJSON('../criteria/rules/closeFrameworkAgreementUA.json'),
        'closeFrameworkAgreementSelectionUA': await loadJSON('../criteria/rules/closeFrameworkAgreementSelectionUA.json'),
        'competitiveDialogueEU': await loadJSON('../criteria/rules/competitiveDialogueEU.json'),
        'competitiveDialogueEU.stage2': await loadJSON('../criteria/rules/competitiveDialogueEU.stage2.json'),
        'competitiveDialogueUA': await loadJSON('../criteria/rules/competitiveDialogueUA.json'),
        'competitiveDialogueUA.stage2': await loadJSON('../criteria/rules/competitiveDialogueUA.stage2.json'),
        'competitiveOrdering': await loadJSON('../criteria/rules/competitiveOrdering.json'),
        'esco': await loadJSON('../criteria/rules/esco.json'),
        'negotiation': await loadJSON('../criteria/rules/negotiation.json'),
        'negotiation.quick': await loadJSON('../criteria/rules/negotiation.quick.json'),
        'priceQuotation': await loadJSON('../criteria/rules/priceQuotation.json'),
        'reporting': await loadJSON('../criteria/rules/reporting.json'),
        'simple.defense': await loadJSON('../criteria/rules/simple.defense.json')
    };

    // Display file view
    fileContent.innerHTML = '';
    for (const [fileName, rules] of Object.entries(files)) {
        const section = document.createElement('div');
        section.className = 'file-section';
        
        const heading = document.createElement('h2');
        const currentPeriod = rules.find(period => !period.period.end_date) || rules[rules.length - 1];
        const rulesCount = currentPeriod ? Object.keys(currentPeriod.criteria).length : 0;
        heading.innerHTML = `${fileName} <small>(${rules.length} periods, ${rulesCount} current rules)</small>`;
        section.appendChild(heading);

        const sectionContent = document.createElement('div');
        sectionContent.className = 'content';

        if (!rules.length) {
            sectionContent.innerHTML = '<div class="no-rules-message">No rules defined</div>';
        } else {
            rules.forEach((period, index) => {
                const periodHeader = document.createElement('div');
                periodHeader.className = 'period-header';
                const startConstant = period.period.start_date || 'Start';
                const endConstant = period.period.end_date || 'Ongoing';
                const startDate = period.period.start_date ? (CONSTANTS[period.period.start_date] || '?') : 'Start';
                const endDate = period.period.end_date ? (CONSTANTS[period.period.end_date] || '?') : 'Ongoing';
                const rulesCount = Object.keys(period.criteria).length;
                
                periodHeader.innerHTML = `
                    <div class="period-number">Period ${index + 1} <small>(${rulesCount} rules)</small></div>
                    <div class="period-dates">
                        <div>
                            <div class="period-constant">${startConstant}</div>
                            <div class="period-value">${startDate}</div>
                        </div>
                        <div class="arrow">→</div>
                        <div>
                            <div class="period-constant">${endConstant}</div>
                            <div class="period-value">${endDate}</div>
                        </div>
                    </div>
                `;
                
                const periodContent = document.createElement('div');
                periodContent.className = 'period-content';
                periodContent.appendChild(createTable(period.criteria));
                
                sectionContent.appendChild(periodHeader);
                sectionContent.appendChild(periodContent);

                // Add click handler for period accordion
                periodHeader.addEventListener('click', (e) => {
                    e.stopPropagation(); // Prevent triggering parent accordion
                    periodHeader.classList.toggle('collapsed');
                });
            });
        }

        section.appendChild(sectionContent);
        fileContent.appendChild(section);

        // Add click handler for accordion
        heading.addEventListener('click', () => {
            section.classList.toggle('collapsed');
        });
    }

    // Display criterion view
    criterionContent.innerHTML = '';
    const criteriaMap = new Map();

    // Process all files and periods for criterion view
    for (const [fileName, periods] of Object.entries(files)) {
        periods.forEach((period, periodIndex) => {
            for (const [criterion, data] of Object.entries(period.criteria)) {
                if (!criteriaMap.has(criterion)) {
                    criteriaMap.set(criterion, new Map());
                }
                if (!criteriaMap.get(criterion).has(fileName)) {
                    criteriaMap.get(criterion).set(fileName, []);
                }
                criteriaMap.get(criterion).get(fileName).push({
                    period: period.period,
                    rules: data.rules,
                    periodIndex
                });
            }
        });
    }

    // Create sections for each criterion
    for (const [criterion, fileData] of criteriaMap) {
        const section = document.createElement('div');
        section.className = 'file-section';
        
        const heading = document.createElement('h2');
        const filesCount = fileData.size;
        const rulesCount = Array.from(fileData.values())
            .reduce((sum, periods) => sum + periods[periods.length - 1].rules.length, 0);
        heading.innerHTML = `${criterion} <small>(${filesCount} files, ${rulesCount} current rules)</small>`;
        section.appendChild(heading);

        const sectionContent = document.createElement('div');
        sectionContent.className = 'content';

        if (fileData.size === 0) {
            sectionContent.innerHTML = '<div class="no-rules-message">No rules defined</div>';
        } else {
            sectionContent.appendChild(createCriterionTable(Object.fromEntries(fileData)));
        }

        section.appendChild(sectionContent);
        criterionContent.appendChild(section);

        // Add click handler for accordion
        heading.addEventListener('click', () => {
            section.classList.toggle('collapsed');
        });
    }
}

// Initialize the display when the page loads
document.addEventListener('DOMContentLoaded', () => {
    displayRules();
    
    // Add view toggle handlers
    const fileView = document.getElementById('fileView');
    const criterionView = document.getElementById('criterionView');
    const fileContent = document.getElementById('fileContent');
    const criterionContent = document.getElementById('criterionContent');

    fileView.addEventListener('click', () => {
        fileView.classList.add('active');
        criterionView.classList.remove('active');
        fileContent.style.display = 'block';
        criterionContent.style.display = 'none';
    });

    criterionView.addEventListener('click', () => {
        criterionView.classList.add('active');
        fileView.classList.remove('active');
        criterionContent.style.display = 'block';
        fileContent.style.display = 'none';
    });

    // Collapse all sections initially
    setTimeout(() => {
        document.querySelectorAll('.file-section').forEach(section => {
            section.classList.add('collapsed');
        });
        document.querySelectorAll('.period-header').forEach(header => {
            header.classList.add('collapsed');
        });
    }, 100);
});

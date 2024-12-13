document.addEventListener('DOMContentLoaded', () => {
    // Add expand/collapse button to navbar
    const navbarLinks = document.querySelector('.navbar-links');
    const button = document.createElement('button');
    button.className = 'btn expand-collapse-btn';
    button.textContent = 'Collapse All';
    navbarLinks.appendChild(button);

    let isExpanded = true;
    button.addEventListener('click', () => {
        const items = document.querySelectorAll('li:has(> ul)');
        const collapsedItems = document.querySelectorAll('li.collapsed');
        
        // If any items are collapsed, expand all. Otherwise, collapse all
        if (collapsedItems.length > 0) {
            items.forEach(item => item.classList.remove('collapsed'));
            button.textContent = 'Collapse All';
            isExpanded = true;
        } else {
            items.forEach(item => item.classList.add('collapsed'));
            button.textContent = 'Expand All';
            isExpanded = false;
        }
        saveCollapsedState();
    });

    // Add collapse functionality
    const parentItems = document.querySelectorAll('li:has(> ul)');
    parentItems.forEach(item => {
        item.addEventListener('click', (e) => {
            if (e.target.tagName === 'A') return;
            e.stopPropagation();
            item.classList.toggle('collapsed');
            saveCollapsedState();
        });
    });

    // Restore collapsed state
    restoreCollapsedState();
});

function saveCollapsedState() {
    const collapsed = Array.from(document.querySelectorAll('li.collapsed')).map(item => {
        // Create a path to this item for unique identification
        let path = [];
        let current = item;
        while (current && current.tagName === 'LI') {
            let index = Array.from(current.parentElement.children).indexOf(current);
            path.unshift(index);
            current = current.parentElement.closest('li');
        }
        return path.join('-');
    });
    localStorage.setItem('collapsedItems', JSON.stringify(collapsed));
}

function restoreCollapsedState() {
    try {
        const collapsed = JSON.parse(localStorage.getItem('collapsedItems') || '[]');
        collapsed.forEach(path => {
            const indices = path.split('-').map(Number);
            let current = document.querySelector('ul');
            indices.forEach(index => {
                if (current) {
                    current = current.children[index];
                    if (current) {
                        current = current.querySelector('ul');
                    }
                }
            });
            if (current && current.parentElement) {
                current.parentElement.classList.add('collapsed');
            }
        });

        // Update button state and isExpanded flag correctly
        const items = document.querySelectorAll('li:has(> ul)');
        const collapsedItems = document.querySelectorAll('li.collapsed');
        const button = document.querySelector('.expand-collapse-btn');
        
        // If all items are collapsed, we want isExpanded to be false
        const allCollapsed = collapsedItems.length === items.length;
        isExpanded = !allCollapsed;  // Important: this is the opposite of allCollapsed
        
        // Set button text based on current state
        if (allCollapsed) {
            button.textContent = 'Expand All';
        } else {
            button.textContent = 'Collapse All';
        }
    } catch (e) {
        console.error('Error restoring collapsed state:', e);
        // Set default state if there's an error
        isExpanded = true;
        const button = document.querySelector('.expand-collapse-btn');
        if (button) button.textContent = 'Collapse All';
    }
}
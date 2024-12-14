document.addEventListener('DOMContentLoaded', () => {
    // Add file counts to folders
    addFileCounts();
    
    // Initialize folder tags
    initializeFolderTags();
});

function addFileCounts() {
    const folders = document.querySelectorAll('li:has(> ul)');
    folders.forEach(folder => {
        const fileCount = folder.querySelectorAll('a').length;
        folder.setAttribute('data-count', fileCount);
        
        // Add count display next to folder name
        const folderText = folder.childNodes[0];
        const countSpan = document.createElement('span');
        countSpan.className = 'file-count';
        countSpan.textContent = ` (${fileCount})`;
        folderText.after(countSpan);
    });
}

function initializeFolderTags() {
    // Create search container
    const searchContainer = document.createElement('div');
    searchContainer.className = 'search-container';
    
    // Create search input
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.id = 'search';
    searchInput.className = 'search-input';
    searchInput.placeholder = 'Search standards...';
    
    // Create tags container
    const tagsContainer = document.createElement('div');
    tagsContainer.className = 'filter-tags';
    
    // Add "All" tag
    const allTag = document.createElement('button');
    allTag.className = 'tag active';
    allTag.textContent = 'All';
    allTag.dataset.folder = 'all';
    tagsContainer.appendChild(allTag);
    
    // Get all top-level folders
    const topLevelFolders = Array.from(document.querySelectorAll('#content > ul > li:has(> ul)'));
    
    // Create tags for each top-level folder
    topLevelFolders.forEach(folder => {
        const folderName = folder.childNodes[0].textContent.trim();
        const tag = document.createElement('button');
        tag.className = 'tag';
        tag.textContent = folderName;
        tag.dataset.folder = folderName;
        tagsContainer.appendChild(tag);
    });
    
    // Append elements to search container
    searchContainer.appendChild(searchInput);
    searchContainer.appendChild(tagsContainer);
    
    // Insert search container after the h1
    const header = document.querySelector('#content h1');
    header.after(searchContainer);
    
    // Search functionality
    searchInput.addEventListener('input', debounce((e) => {
        const searchTerm = e.target.value.toLowerCase();
        filterContent(searchTerm, document.querySelector('.tag.active').dataset.folder);
    }, 300));
    
    // Tag filtering functionality
    const tags = document.querySelectorAll('.tag');
    tags.forEach(tag => {
        tag.addEventListener('click', () => {
            tags.forEach(t => t.classList.remove('active'));
            tag.classList.add('active');
            
            const searchTerm = document.getElementById('search').value.toLowerCase();
            filterContent(searchTerm, tag.dataset.folder);
        });
    });
}

function filterContent(searchTerm, selectedFolder) {
    const items = document.querySelectorAll('#content li');
    const isAllFolder = selectedFolder === 'all';
    
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        const isMatch = text.includes(searchTerm);
        const inSelectedFolder = isAllFolder || isItemInFolder(item, selectedFolder);
        
        if (isAllFolder) {
            // Show everything if "All" is selected and matches search
            item.style.display = isMatch ? '' : 'none';
        } else if (inSelectedFolder) {
            // If item is in selected folder, show it and all its children
            item.style.display = isMatch ? '' : 'none';
            const childItems = item.querySelectorAll('li');
            childItems.forEach(child => {
                child.style.display = child.textContent.toLowerCase().includes(searchTerm) ? '' : 'none';
            });
        } else {
            // Hide items not in selected folder
            item.style.display = 'none';
        }
        
        // If item is visible and has parents, make sure they're visible too
        if ((isMatch && isAllFolder) || (isMatch && inSelectedFolder)) {
            showParents(item);
        }
    });
    
    // Expand all folders when filtering
    if (searchTerm || !isAllFolder) {
        document.querySelectorAll('li:has(> ul)').forEach(folder => {
            folder.classList.remove('collapsed');
        });
    }
    
    // Make sure the selected folder and its contents are visible
    if (!isAllFolder) {
        const selectedFolderElement = Array.from(document.querySelectorAll('#content > ul > li')).find(
            el => el.childNodes[0].textContent.trim() === selectedFolder
        );
        if (selectedFolderElement) {
            selectedFolderElement.style.display = '';
            const children = selectedFolderElement.querySelectorAll('li');
            children.forEach(child => {
                if (child.textContent.toLowerCase().includes(searchTerm)) {
                    child.style.display = '';
                    showParents(child);
                }
            });
        }
    }
}

function isItemInFolder(item, folderName) {
    let current = item;
    while (current && current.parentElement) {
        if (current.parentElement.id === 'content') {
            // We've reached the top level
            const folderText = current.childNodes[0].textContent.trim();
            return folderText === folderName;
        }
        current = current.parentElement.closest('li');
    }
    return false;
}

function showParents(item) {
    let parent = item.parentElement;
    while (parent) {
        if (parent.tagName === 'UL') {
            parent.style.display = '';
            if (parent.parentElement) {
                parent.parentElement.style.display = '';
            }
        }
        parent = parent.parentElement;
    }
}

// Utility function for debouncing search input
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

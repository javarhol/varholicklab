document.addEventListener('DOMContentLoaded', async () => {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results-container');
    const statusArea = document.getElementById('status-area');
    const noResults = document.getElementById('no-results');
    
    let index;
    let chunksData = [];

    // Initialize FlexSearch Document Index
    // We use a simple configuration optimized for fast partial matching
    index = new FlexSearch.Document({
        document: {
            id: "uid",
            index: ["text"],
            store: true // Store the whole object so we can retrieve metadata
        },
        tokenize: "forward"
    });

    try {
        const response = await fetch('search_index.json');
        if (!response.ok) throw new Error("Failed to load search_index.json");
        chunksData = await response.json();
        
        // Feed data into FlexSearch
        let uidCounter = 0;
        chunksData.forEach(chunk => {
            chunk.uid = uidCounter++;
            index.add(chunk);
        });
        
        // Hide loader, enable input
        statusArea.classList.add('hidden');
        searchInput.disabled = false;
        searchInput.placeholder = `Search across ${chunksData.length.toLocaleString()} paragraphs...`;
        searchInput.focus();
        
    } catch (error) {
        console.error("Initialization error:", error);
        statusArea.innerHTML = `<p class="text-red-500 font-medium">Failed to load library database. Ensure search_index.json exists.</p>`;
    }

    // Handle search input with debouncing
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            performSearch(query);
        }, 300); // 300ms debounce
    });

    function performSearch(query) {
        resultsContainer.innerHTML = '';
        noResults.classList.add('hidden');
        
        if (!query) {
            return;
        }

        // FlexSearch returns an array of matching document IDs per indexed field
        const searchResults = index.search(query, {
            enrich: true,
            limit: 50 // Show top 50 paragraphs
        });

        if (searchResults.length === 0 || searchResults[0].result.length === 0) {
            noResults.classList.remove('hidden');
            return;
        }

        // searchResults format for document index:
        // [{ field: "text", result: [ {id: 1, doc: {...}}, {id: 2, doc: {...}} ] }]
        const hits = searchResults[0].result;

        // Group hits by paper ID to organize the results beautifully
        const groupedByPaper = {};
        hits.forEach(hit => {
            const doc = hit.doc;
            if (!groupedByPaper[doc.id]) {
                groupedByPaper[doc.id] = {
                    title: doc.title,
                    authors: doc.authors,
                    year: doc.year,
                    journal: doc.journal,
                    chunks: []
                };
            }
            groupedByPaper[doc.id].chunks.push(doc.text);
        });

        // Render HTML
        for (const paperId in groupedByPaper) {
            const paper = groupedByPaper[paperId];
            
            const paperCard = document.createElement('div');
            paperCard.className = 'bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden';
            
            const header = document.createElement('div');
            header.className = 'bg-gray-50 px-6 py-4 border-b border-gray-200';
            
            const titleLink = document.createElement('a');
            titleLink.href = `https://openalex.org/${paperId.replace('OA_', 'W')}`;
            titleLink.target = '_blank';
            titleLink.className = 'text-lg font-bold text-blue-700 hover:text-blue-900 transition-colors leading-snug block';
            titleLink.textContent = paper.title;
            
            const meta = document.createElement('p');
            meta.className = 'text-sm text-gray-600 mt-2';
            meta.innerHTML = `<span class="font-medium">${paper.authors || "Unknown Authors"}</span> &bull; ${paper.year || "N/A"} &bull; <span class="italic">${paper.journal || "Unknown Journal"}</span>`;
            
            header.appendChild(titleLink);
            header.appendChild(meta);
            paperCard.appendChild(header);
            
            const chunksContainer = document.createElement('div');
            chunksContainer.className = 'px-6 py-4 space-y-4';
            
            paper.chunks.forEach(text => {
                const p = document.createElement('p');
                p.className = 'text-gray-800 text-base leading-relaxed pl-4 border-l-4 border-blue-200 bg-gray-50/50 py-2 pr-2 rounded-r-md';
                // Highlight query terms (case insensitive)
                p.innerHTML = highlightTerms(text, query);
                chunksContainer.appendChild(p);
            });
            
            paperCard.appendChild(chunksContainer);
            resultsContainer.appendChild(paperCard);
        }
    }

    function highlightTerms(text, query) {
        if (!query) return text;
        const terms = query.split(/\s+/).filter(t => t.length > 2);
        if (terms.length === 0) return text;
        
        let highlighted = text;
        terms.forEach(term => {
            const regex = new RegExp(`(${escapeRegExp(term)})`, 'gi');
            highlighted = highlighted.replace(regex, '<mark>$1</mark>');
        });
        return highlighted;
    }

    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
});

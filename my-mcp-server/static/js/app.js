const socket = io();

socket.on('connect', function() {
    document.getElementById('connection-status').textContent = 'Connected';
    document.getElementById('connection-status').classList.add('connected');
    console.log('Connected to server');
});

socket.on('disconnect', function() {
    document.getElementById('connection-status').textContent = 'Disconnected';
    document.getElementById('connection-status').classList.remove('connected');
    console.log('Disconnected from server');
});

socket.on('connected', function(data) {
    console.log('Initial data received:', data);
    if (data.data) {
        updateDashboard(data.data);
    }
});

socket.on('update', function(data) {
    console.log('Update received:', data);
    updateLastUpdateTime();
    if (data.data) {
        updateDashboard(data.data);
    }
    if (data.results) {
        updateAgentStatus(data.results);
    }
});

function updateDashboard(data) {
    if (data.CryptoNewsAgent) {
        updateNewsSection(data.CryptoNewsAgent);
    }
    if (data.CryptoMarketAgent) {
        updateWeatherSection(data.CryptoMarketAgent);
    }
    if (data.CrunchbaseCryptoAgent) {
        updateTrendsSection(data.CrunchbaseCryptoAgent);
    }
}

function updateNewsSection(newsData) {
    const newsGrid = document.getElementById('news-grid');
    newsGrid.innerHTML = '';
    
    if (!newsData || newsData.length === 0) {
        newsGrid.innerHTML = '<div class="loading">No crypto news available</div>';
        return;
    }
    
    newsData.forEach(item => {
        const newsItem = document.createElement('div');
        newsItem.className = 'news-item';
        const sentimentClass = item.sentiment ? item.sentiment.label : 'neutral';
        newsItem.innerHTML = `
            <h3><a href="${item.url}" target="_blank" style="color: inherit; text-decoration: none;">${item.title}</a></h3>
            <div class="description">${item.description || ''}</div>
            <div class="meta">
                <span class="sentiment ${sentimentClass}">Sentiment: ${item.sentiment ? item.sentiment.label : 'neutral'}</span>
                <span>Source: ${item.source || 'Unknown'}</span>
                <span>Category: ${item.category || 'Crypto News'}</span>
                <span>Read time: ${item.read_time_minutes || 1}min</span>
            </div>
            ${item.crypto_mentions && item.crypto_mentions.length > 0 ? 
                `<div class="crypto-mentions">Mentions: ${item.crypto_mentions.join(', ')}</div>` : ''}
        `;
        newsGrid.appendChild(newsItem);
    });
}

function updateWeatherSection(cryptoData) {
    const cryptoGrid = document.getElementById('weather-grid');
    cryptoGrid.innerHTML = '';
    
    if (!cryptoData || cryptoData.length === 0) {
        cryptoGrid.innerHTML = '<div class="loading">No crypto market data available</div>';
        return;
    }
    
    cryptoData.forEach(item => {
        const cryptoCard = document.createElement('div');
        cryptoCard.className = 'crypto-card';
        
        const changeColor = item.change_24h >= 0 ? 'positive' : 'negative';
        const changeSymbol = item.change_24h >= 0 ? '+' : '';
        
        cryptoCard.innerHTML = `
            <div class="crypto-header">
                <div class="crypto-name">${item.name}</div>
                <div class="crypto-symbol">${item.symbol}</div>
            </div>
            <div class="crypto-price">$${formatPrice(item.price_usd)}</div>
            <div class="crypto-change ${changeColor}">${changeSymbol}${item.change_24h.toFixed(2)}%</div>
            <div class="crypto-details">
                <div class="detail-row">
                    <span>Market Cap:</span>
                    <span>$${formatLargeNumber(item.market_cap)}</span>
                </div>
                <div class="detail-row">
                    <span>Volume 24h:</span>
                    <span>$${formatLargeNumber(item.volume_24h)}</span>
                </div>
                ${item.technical_analysis ? `
                <div class="detail-row">
                    <span>Momentum:</span>
                    <span class="momentum-${item.technical_analysis.momentum}">${item.technical_analysis.momentum}</span>
                </div>
                ` : ''}
                ${item.market_strength ? `
                <div class="detail-row">
                    <span>Strength:</span>
                    <span class="strength-${item.market_strength.label}">${item.market_strength.label}</span>
                </div>
                ` : ''}
                ${item.recommendation ? `
                <div class="recommendation">
                    <strong>${item.recommendation.action.replace('_', ' ').toUpperCase()}:</strong>
                    <span>${item.recommendation.reason}</span>
                </div>
                ` : ''}
            </div>
            ${item.price_alerts && item.price_alerts.length > 0 ? `
            <div class="alerts">
                ${item.price_alerts.map(alert => `
                    <div class="alert alert-${alert.level}">
                        <span class="alert-type">${alert.type.replace('_', ' ').toUpperCase()}:</span>
                        ${alert.message}
                    </div>
                `).join('')}
            </div>
            ` : ''}
        `;
        cryptoGrid.appendChild(cryptoCard);
    });
}

function updateTrendsSection(companyData) {
    const companiesGrid = document.getElementById('trends-grid');
    companiesGrid.innerHTML = '';
    
    if (!companyData || companyData.length === 0) {
        companiesGrid.innerHTML = '<div class="loading">No Crunchbase crypto companies available</div>';
        return;
    }
    
    companyData.forEach(item => {
        const companyItem = document.createElement('div');
        companyItem.className = 'company-item';
        
        companyItem.innerHTML = `
            <h3><a href="${item.url}" target="_blank" style="color: inherit; text-decoration: none;">${item.company_name}</a></h3>
            <div class="description">${item.description}</div>
            <div class="company-meta">
                <span class="category">${item.category}</span>
                <span class="funding">${item.funding_info}</span>
                ${item.investment_metrics && item.investment_metrics.total_funding_usd ? `
                <span class="funding-amount">$${formatLargeNumber(item.investment_metrics.total_funding_usd)}</span>
                ` : ''}
            </div>
            ${item.company_analysis ? `
            <div class="company-analysis">
                <div class="analysis-row">
                    <span>Sector:</span>
                    <span class="sector-${item.company_analysis.sector}">${item.company_analysis.sector}</span>
                </div>
                <div class="analysis-row">
                    <span>Stage:</span>
                    <span class="stage-${item.company_analysis.maturity_stage}">${item.company_analysis.maturity_stage}</span>
                </div>
                <div class="analysis-row">
                    <span>Business Model:</span>
                    <span>${item.company_analysis.business_model}</span>
                </div>
                ${item.company_analysis.key_technologies && item.company_analysis.key_technologies.length > 0 ? `
                <div class="technologies">
                    <span>Technologies:</span>
                    <div class="tech-tags">
                        ${item.company_analysis.key_technologies.map(tech => 
                            `<span class="tech-tag">${tech}</span>`
                        ).join('')}
                    </div>
                </div>
                ` : ''}
            </div>
            ` : ''}
            ${item.investment_metrics ? `
            <div class="investment-metrics">
                <div class="metric">
                    <span>Investor Confidence:</span>
                    <span class="confidence-${item.investment_metrics.investor_confidence}">
                        ${item.investment_metrics.investor_confidence}
                    </span>
                </div>
                ${item.investment_metrics.valuation_estimate ? `
                <div class="metric">
                    <span>Est. Valuation:</span>
                    <span>$${formatLargeNumber(item.investment_metrics.valuation_estimate)}</span>
                </div>
                ` : ''}
            </div>
            ` : ''}
            ${item.growth_indicators ? `
            <div class="growth-indicators">
                <div class="growth-potential growth-${item.growth_indicators.growth_potential}">
                    Growth Potential: ${item.growth_indicators.growth_potential}
                </div>
                <div class="growth-score">Score: ${item.growth_indicators.growth_score}/7</div>
            </div>
            ` : ''}
            ${item.risk_assessment ? `
            <div class="risk-assessment">
                <span class="risk-level risk-${item.risk_assessment.risk_level}">
                    Risk: ${item.risk_assessment.risk_level}
                </span>
            </div>
            ` : ''}
        `;
        companiesGrid.appendChild(companyItem);
    });
}

function updateAgentStatus(results) {
    fetch('/api/agents')
        .then(response => response.json())
        .then(data => {
            const agentsGrid = document.getElementById('agents-grid');
            agentsGrid.innerHTML = '';
            
            if (data.agents && data.agents.length > 0) {
                data.agents.forEach(agent => {
                    const agentCard = document.createElement('div');
                    agentCard.className = 'agent-card';
                    
                    const statusClass = agent.status === 'success' ? 'success' : 
                                       agent.status === 'idle' ? 'idle' : 'error';
                    
                    agentCard.innerHTML = `
                        <h3>${agent.name}</h3>
                        <div class="status ${statusClass}">${agent.status}</div>
                        <div class="details">
                            <div>Items: ${agent.items || 0}</div>
                            <div>Last run: ${agent.last_collection ? new Date(agent.last_collection).toLocaleTimeString() : 'Never'}</div>
                        </div>
                    `;
                    agentsGrid.appendChild(agentCard);
                });
            }
        })
        .catch(error => console.error('Error fetching agent status:', error));
}

function formatPrice(price) {
    if (price >= 1000) {
        return price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    } else if (price >= 1) {
        return price.toFixed(4);
    } else {
        return price.toFixed(6);
    }
}

function formatLargeNumber(num) {
    if (num >= 1e12) {
        return (num / 1e12).toFixed(2) + 'T';
    } else if (num >= 1e9) {
        return (num / 1e9).toFixed(2) + 'B';
    } else if (num >= 1e6) {
        return (num / 1e6).toFixed(2) + 'M';
    } else if (num >= 1e3) {
        return (num / 1e3).toFixed(2) + 'K';
    } else {
        return num.toLocaleString();
    }
}

function updateLastUpdateTime() {
    const now = new Date();
    document.getElementById('last-update').textContent = `Last update: ${now.toLocaleTimeString()}`;
}

function requestUpdate() {
    fetch('/api/collect', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log('Manual update triggered:', data);
            if (data.data) {
                updateDashboard(data.data);
            }
            updateLastUpdateTime();
        })
        .catch(error => console.error('Error triggering update:', error));
}

fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        if (data.data) {
            updateDashboard(data.data);
        }
        updateLastUpdateTime();
    })
    .catch(error => console.error('Error fetching initial data:', error));

fetch('/api/agents')
    .then(response => response.json())
    .then(data => {
        if (data.agents) {
            updateAgentStatus(data.agents);
        }
    })
    .catch(error => console.error('Error fetching agent status:', error));

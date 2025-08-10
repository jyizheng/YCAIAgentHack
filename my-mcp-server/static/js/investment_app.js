let currentAnalysis = null;
let socket = null;

// Initialize Socket.IO connection
function initSocket() {
    socket = io();
    
    socket.on('connect', () => {
        console.log('Connected to server');
    });
    
    socket.on('analysis_update', (data) => {
        console.log('Received analysis update:', data);
        updateAnalysisResults(data);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initSocket();
    
    // Add enter key support for input
    document.getElementById('companyInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeCompany();
        }
    });
});

async function analyzeCompany() {
    const companyName = document.getElementById('companyInput').value.trim();
    const errorMsg = document.getElementById('errorMessage');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    // Clear previous error
    errorMsg.textContent = '';
    
    // Validate input
    if (!companyName) {
        errorMsg.textContent = 'Please enter a company name';
        return;
    }
    
    // Show loading state
    showLoading(true);
    analyzeBtn.disabled = true;
    analyzeBtn.querySelector('.btn-text').style.display = 'none';
    analyzeBtn.querySelector('.spinner').style.display = 'inline-block';
    
    try {
        // Make API call to analyze company
        const response = await fetch('/api/investment-analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ company_name: companyName })
        });
        
        if (!response.ok) {
            throw new Error(`Analysis failed: ${response.statusText}`);
        }
        
        const data = await response.json();
        currentAnalysis = data;
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Analysis error:', error);
        errorMsg.textContent = `Error: ${error.message}`;
        hideResults();
    } finally {
        // Reset button state
        showLoading(false);
        analyzeBtn.disabled = false;
        analyzeBtn.querySelector('.btn-text').style.display = 'inline';
        analyzeBtn.querySelector('.spinner').style.display = 'none';
    }
}

function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = show ? 'flex' : 'none';
    
    if (show) {
        // Update loading status messages
        const statusMessages = [
            'Collecting market data...',
            'Analyzing news sentiment...',
            'Evaluating company profile...',
            'Calculating investment metrics...',
            'Generating recommendation...'
        ];
        
        let messageIndex = 0;
        const statusElement = overlay.querySelector('.loading-status');
        
        const interval = setInterval(() => {
            if (!overlay.style.display || overlay.style.display === 'none') {
                clearInterval(interval);
                return;
            }
            
            statusElement.textContent = statusMessages[messageIndex % statusMessages.length];
            messageIndex++;
        }, 2000);
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    
    // Display YC Investment Recommendation
    displayInvestmentRecommendation(data.yc_analysis);
    
    // Display raw agent data
    displayAgentData('newsData', data.news_data);
    displayAgentData('marketData', data.market_data);
    displayAgentData('companyData', data.company_data);
    
    // Display investment timeline
    displayTimeline(data.yc_analysis.investment_timeline);
    
    // Display risk-return chart
    displayRiskReturnChart(data.yc_analysis);
    
    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function displayInvestmentRecommendation(analysis) {
    // Investment Decision with dynamic styling
    const decisionElement = document.getElementById('investmentDecision');
    decisionElement.textContent = analysis.investment_decision;
    decisionElement.className = 'decision-value';
    
    // Add confidence indicator
    const confidenceText = document.createElement('div');
    confidenceText.className = 'confidence-indicator';
    confidenceText.textContent = `Confidence Score: ${(analysis.overall_score * 10).toFixed(0)}%`;
    
    if (analysis.investment_decision === 'INVEST') {
        decisionElement.classList.add('invest');
        decisionElement.innerHTML = `
            <div class="decision-main">✅ ${analysis.investment_decision}</div>
            <div class="decision-sub">Strong Buy - Score: ${analysis.overall_score.toFixed(1)}/10</div>
        `;
    } else if (analysis.investment_decision === 'PASS') {
        decisionElement.classList.add('pass');
        decisionElement.innerHTML = `
            <div class="decision-main">❌ ${analysis.investment_decision}</div>
            <div class="decision-sub">Not Recommended - Score: ${analysis.overall_score.toFixed(1)}/10</div>
        `;
    } else {
        decisionElement.classList.add('conditional');
        decisionElement.innerHTML = `
            <div class="decision-main">⚠️ ${analysis.investment_decision}</div>
            <div class="decision-sub">Proceed with Conditions - Score: ${analysis.overall_score.toFixed(1)}/10</div>
        `;
    }
    
    // Investment Metrics with enhanced display
    document.getElementById('recommendedAmount').innerHTML = `
        <span class="amount-value">${formatCurrency(analysis.recommended_investment)}</span>
        <span class="amount-label">${analysis.recommended_investment > 0 ? 'USD' : 'N/A'}</span>
    `;
    
    document.getElementById('equityStake').innerHTML = `
        <span class="stake-value">${analysis.equity_stake}%</span>
        <span class="stake-label">${analysis.investment_structure.type}</span>
    `;
    
    document.getElementById('companyValuation').innerHTML = `
        <span class="valuation-value">${formatCurrency(analysis.post_money_valuation)}</span>
        <span class="valuation-label">Post-Money</span>
    `;
    
    // Enhanced risk score with color coding
    const riskScoreElement = document.getElementById('riskScore');
    const riskLevel = analysis.risk_score <= 3 ? 'low' : analysis.risk_score <= 6 ? 'medium' : 'high';
    riskScoreElement.innerHTML = `
        <span class="risk-value ${riskLevel}-risk">${analysis.risk_score.toFixed(1)}/10</span>
        <span class="risk-label">${riskLevel.toUpperCase()} RISK</span>
    `;
    
    // Investment Structure
    const structureHtml = `
        <ul>
            <li><strong>Investment Type:</strong> ${analysis.investment_structure.type}</li>
            <li><strong>Investment Amount:</strong> ${formatCurrency(analysis.investment_structure.amount)}</li>
            <li><strong>Pre-Money Valuation:</strong> ${formatCurrency(analysis.investment_structure.pre_money_valuation)}</li>
            <li><strong>Post-Money Valuation:</strong> ${formatCurrency(analysis.investment_structure.post_money_valuation)}</li>
            <li><strong>YC Ownership:</strong> ${analysis.investment_structure.yc_ownership}%</li>
            <li><strong>Board Seats:</strong> ${analysis.investment_structure.board_seats}</li>
            <li><strong>Pro-Rata Rights:</strong> ${analysis.investment_structure.pro_rata_rights ? 'Yes' : 'No'}</li>
            <li><strong>Liquidation Preference:</strong> ${analysis.investment_structure.liquidation_preference}</li>
        </ul>
    `;
    document.getElementById('investmentStructure').innerHTML = structureHtml;
    
    // Detailed Report with enhanced variables and metrics
    const scores = analysis.detailed_report.scores_breakdown || {};
    const reportHtml = `
        <div class="report-section">
            <h4>📊 Score Breakdown</h4>
            <div class="scores-grid">
                <div class="score-item">
                    <span class="score-label">Market Conditions</span>
                    <span class="score-bar">
                        <span class="score-fill" style="width: ${(scores.market_score || 0) * 10}%"></span>
                    </span>
                    <span class="score-value">${(scores.market_score || 0).toFixed(1)}/10</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Company Profile</span>
                    <span class="score-bar">
                        <span class="score-fill" style="width: ${(scores.company_score || 0) * 10}%"></span>
                    </span>
                    <span class="score-value">${(scores.company_score || 0).toFixed(1)}/10</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Market Sentiment</span>
                    <span class="score-bar">
                        <span class="score-fill" style="width: ${(scores.sentiment_score || 0) * 10}%"></span>
                    </span>
                    <span class="score-value">${(scores.sentiment_score || 0).toFixed(1)}/10</span>
                </div>
                <div class="score-item">
                    <span class="score-label">Financial Metrics</span>
                    <span class="score-bar">
                        <span class="score-fill" style="width: ${(scores.financial_score || 0) * 10}%"></span>
                    </span>
                    <span class="score-value">${(scores.financial_score || 0).toFixed(1)}/10</span>
                </div>
            </div>
        </div>
        
        <div class="report-section">
            <h4>Executive Summary</h4>
            <p>${analysis.detailed_report.executive_summary}</p>
        </div>
        
        <div class="report-section">
            <h4>Market Analysis</h4>
            <p>${analysis.detailed_report.market_analysis}</p>
        </div>
        
        <div class="report-section">
            <h4>Investment Rationale</h4>
            <p>${analysis.detailed_report.investment_rationale}</p>
        </div>
        
        <div class="report-section">
            <h4>⚠️ Key Risks (${analysis.detailed_report.key_risks.length} identified)</h4>
            <ul class="risk-list">
                ${analysis.detailed_report.key_risks.map((risk, index) => `
                    <li class="risk-item">
                        <span class="risk-number">${index + 1}</span>
                        <span class="risk-text">${risk}</span>
                    </li>
                `).join('')}
            </ul>
        </div>
        
        <div class="report-section">
            <h4>🚀 Growth Opportunities (${analysis.detailed_report.growth_opportunities.length} identified)</h4>
            <ul class="opportunity-list">
                ${analysis.detailed_report.growth_opportunities.map((opp, index) => `
                    <li class="opportunity-item">
                        <span class="opportunity-icon">💎</span>
                        <span class="opportunity-text">${opp}</span>
                    </li>
                `).join('')}
            </ul>
        </div>
        
        <div class="report-section">
            <h4>Exit Strategy</h4>
            <p>${analysis.detailed_report.exit_strategy}</p>
        </div>
        
        <div class="report-section">
            <h4>📈 Expected Returns</h4>
            <div class="returns-grid">
                <div class="return-item">
                    <div class="return-period">3 Years</div>
                    <div class="return-multiple">${analysis.detailed_report.expected_returns['3_year']}x</div>
                    <div class="return-roi">${((analysis.detailed_report.expected_returns['3_year'] - 1) * 100).toFixed(0)}% ROI</div>
                </div>
                <div class="return-item">
                    <div class="return-period">5 Years</div>
                    <div class="return-multiple">${analysis.detailed_report.expected_returns['5_year']}x</div>
                    <div class="return-roi">${((analysis.detailed_report.expected_returns['5_year'] - 1) * 100).toFixed(0)}% ROI</div>
                </div>
                <div class="return-item">
                    <div class="return-period">7 Years</div>
                    <div class="return-multiple">${analysis.detailed_report.expected_returns['7_year']}x</div>
                    <div class="return-roi">${((analysis.detailed_report.expected_returns['7_year'] - 1) * 100).toFixed(0)}% ROI</div>
                </div>
            </div>
        </div>
        
        <div class="report-section">
            <h4>💰 Investment Summary</h4>
            <div class="summary-box">
                <p><strong>Company:</strong> ${analysis.company_name}</p>
                <p><strong>YC Investment:</strong> ${formatCurrency(analysis.recommended_investment)}</p>
                <p><strong>Ownership:</strong> ${analysis.equity_stake}%</p>
                <p><strong>Expected Exit Value:</strong> ${formatCurrency(analysis.post_money_valuation * analysis.expected_return_multiple)}</p>
                <p><strong>Expected YC Return:</strong> ${formatCurrency(analysis.recommended_investment * analysis.expected_return_multiple)}</p>
                <p><strong>Decision Date:</strong> ${new Date(analysis.analysis_timestamp).toLocaleDateString()}</p>
            </div>
        </div>
    `;
    document.getElementById('detailedReport').innerHTML = reportHtml;
}

function displayAgentData(elementId, data) {
    const element = document.getElementById(elementId);
    
    if (!data || data.length === 0) {
        element.innerHTML = '<div class="no-data">No data available</div>';
        return;
    }
    
    // Format and display raw JSON data
    element.textContent = JSON.stringify(data, null, 2);
}

function displayTimeline(timeline) {
    const timelineContainer = document.getElementById('investmentTimeline');
    
    if (!timeline || timeline.length === 0) {
        timelineContainer.innerHTML = '<p>No timeline data available</p>';
        return;
    }
    
    const timelineHtml = timeline.map(item => `
        <div class="timeline-item">
            <div class="timeline-date">${item.timeframe}</div>
            <div class="timeline-title">${item.milestone}</div>
            <div class="timeline-description">${item.description}</div>
        </div>
    `).join('');
    
    timelineContainer.innerHTML = timelineHtml;
}

function displayRiskReturnChart(analysis) {
    const canvas = document.getElementById('riskReturnChart');
    if (!canvas) {
        console.error('Chart canvas element not found');
        return;
    }
    
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js library not loaded');
        return;
    }
    
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.riskReturnChart && typeof window.riskReturnChart.destroy === 'function') {
        window.riskReturnChart.destroy();
        window.riskReturnChart = null;
    }
    
    // Create new chart
    try {
        window.riskReturnChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Current Investment',
                data: [{
                    x: analysis.risk_score,
                    y: analysis.expected_return_multiple
                }],
                backgroundColor: 'rgba(255, 102, 0, 0.6)',
                borderColor: 'rgba(255, 102, 0, 1)',
                borderWidth: 2,
                pointRadius: 10,
                pointHoverRadius: 12
            }, {
                label: 'YC Portfolio Average',
                data: [{
                    x: 5,
                    y: 10
                }],
                backgroundColor: 'rgba(100, 126, 234, 0.6)',
                borderColor: 'rgba(100, 126, 234, 1)',
                borderWidth: 2,
                pointRadius: 8,
                pointHoverRadius: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Risk vs Expected Return Analysis',
                    color: '#ffffff',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    labels: {
                        color: '#ffffff'
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Risk Score (1-10)',
                        color: '#ffffff'
                    },
                    min: 0,
                    max: 10,
                    ticks: {
                        color: '#b0b0b0'
                    },
                    grid: {
                        color: '#333333'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Expected Return Multiple',
                        color: '#ffffff'
                    },
                    min: 0,
                    max: 20,
                    ticks: {
                        color: '#b0b0b0',
                        callback: function(value) {
                            return value + 'x';
                        }
                    },
                    grid: {
                        color: '#333333'
                    }
                }
            }
        }
    });
    } catch (error) {
        console.error('Error creating chart:', error);
    }
}

function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
}

function formatCurrency(amount) {
    if (amount >= 1000000000) {
        return `$${(amount / 1000000000).toFixed(1)}B`;
    } else if (amount >= 1000000) {
        return `$${(amount / 1000000).toFixed(1)}M`;
    } else if (amount >= 1000) {
        return `$${(amount / 1000).toFixed(0)}K`;
    } else {
        return `$${amount.toFixed(0)}`;
    }
}

// Style additions for report sections
const style = document.createElement('style');
style.textContent = `
    .report-section {
        margin-bottom: 25px;
        padding-bottom: 20px;
        border-bottom: 1px solid var(--border-color);
    }
    
    .report-section:last-child {
        border-bottom: none;
    }
    
    .report-section h4 {
        color: var(--primary-color);
        margin-bottom: 12px;
        font-size: 1.1rem;
    }
    
    .report-section p {
        line-height: 1.8;
        color: var(--text-secondary);
    }
    
    .report-section ul {
        list-style: none;
        padding-left: 0;
    }
    
    .report-section li {
        padding: 8px 0;
        color: var(--text-secondary);
        position: relative;
        padding-left: 20px;
    }
    
    .report-section li::before {
        content: '▸';
        position: absolute;
        left: 0;
        color: var(--primary-color);
    }
    
    .no-data {
        text-align: center;
        color: var(--text-secondary);
        padding: 30px;
        font-style: italic;
    }
`;
document.head.appendChild(style);
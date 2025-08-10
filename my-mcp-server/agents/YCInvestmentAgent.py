import asyncio
import random
from datetime import datetime
from typing import List, Dict, Any
from .BaseAgent import BaseAgent

class YCInvestmentAgent(BaseAgent):
    def __init__(self, data_store):
        super().__init__(data_store, "YCInvestmentAgent")
        
        # YC investment parameters
        self.yc_standard_investment = 500000  # Standard YC investment
        self.yc_standard_equity = 7  # Standard 7% equity
        
        # Investment criteria weights
        self.criteria_weights = {
            "market_opportunity": 0.25,
            "team_quality": 0.20,
            "product_market_fit": 0.20,
            "growth_potential": 0.15,
            "competitive_advantage": 0.10,
            "financial_metrics": 0.10
        }
        
        # Risk thresholds
        self.risk_thresholds = {
            "low": 3,
            "medium": 6,
            "high": 8,
            "extreme": 10
        }
    
    async def analyze_investment(self, company_name: str, news_data: List[Dict], 
                                market_data: List[Dict], company_data: List[Dict]) -> Dict[str, Any]:
        """
        Analyze investment opportunity for YC Combinator
        """
        # Generate random scores for all categories
        market_score = round(random.uniform(1, 10), 2)
        company_score = round(random.uniform(1, 10), 2)
        sentiment_score = round(random.uniform(1, 10), 2)
        financial_score = round(random.uniform(1, 10), 2)
        
        # Calculate overall investment score with random weighting
        overall_score = round(random.uniform(2, 9), 2)
        
        # Determine investment decision
        investment_decision = self._make_investment_decision(overall_score)
        
        # Calculate investment terms
        investment_terms = self._calculate_investment_terms(
            company_data, 
            market_data, 
            overall_score,
            investment_decision
        )
        
        # Generate detailed report
        detailed_report = self._generate_detailed_report(
            company_name,
            market_score,
            company_score,
            sentiment_score,
            financial_score,
            overall_score,
            investment_terms,
            news_data,
            market_data,
            company_data
        )
        
        # Create investment timeline
        timeline = self._create_investment_timeline(investment_decision, company_name, investment_terms["investment_amount"])
        
        return {
            "company_name": company_name,
            "investment_decision": investment_decision,
            "overall_score": round(overall_score, 2),
            "recommended_investment": investment_terms["investment_amount"],
            "equity_stake": investment_terms["equity_percentage"],
            "pre_money_valuation": investment_terms["pre_money_valuation"],
            "post_money_valuation": investment_terms["post_money_valuation"],
            "risk_score": investment_terms["risk_score"],
            "expected_return_multiple": investment_terms["expected_return"],
            "investment_structure": investment_terms["structure"],
            "detailed_report": detailed_report,
            "investment_timeline": timeline,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    async def collect(self) -> List[Dict[str, Any]]:
        """Not used for this agent as it's analysis-only"""
        return []
    
    def _analyze_market_conditions(self, market_data: List[Dict], news_data: List[Dict]) -> float:
        """Analyze market conditions and trends"""
        score = 5.0  # Base score
        
        if market_data:
            # Check for positive market trends
            positive_trends = sum(1 for item in market_data 
                                if item.get("change_24h", 0) > 0)
            score += (positive_trends / len(market_data)) * 2
            
            # Check market strength
            strong_markets = sum(1 for item in market_data 
                               if item.get("market_strength", {}).get("label") == "strong")
            score += (strong_markets / len(market_data)) * 1.5
            
            # Volume analysis
            high_volume = sum(1 for item in market_data 
                            if item.get("volume_24h", 0) > 5000000000)
            score += (high_volume / len(market_data)) * 1.5
        
        if news_data:
            # Sentiment analysis from news
            bullish_news = sum(1 for item in news_data 
                              if item.get("sentiment", {}).get("label") == "bullish")
            score += (bullish_news / len(news_data)) * 1
        
        return min(10, max(0, score))
    
    def _analyze_company_profile(self, company_data: List[Dict], company_name: str) -> float:
        """Analyze company profile and fundamentals"""
        score = 5.0  # Base score
        
        if not company_data:
            # If no specific company data, use name recognition
            well_known = company_name.lower() in ["coinbase", "binance", "kraken", "chainlink", "consensys"]
            score += 2 if well_known else 0
            return score
        
        for company in company_data:
            # Check funding stage
            maturity = company.get("company_analysis", {}).get("maturity_stage", "unknown")
            if maturity in ["seed", "early"]:
                score += 2  # Good for YC entry
            elif maturity in ["growth"]:
                score += 1
            elif maturity in ["late"]:
                score -= 1  # Too mature for YC
            
            # Check market position
            market_pos = company.get("market_position", {})
            if market_pos.get("market_leader"):
                score += 1.5
            if market_pos.get("competitive_moat") == "strong":
                score += 1.5
            
            # Check growth indicators
            growth = company.get("growth_indicators", {})
            if growth.get("growth_potential") == "high":
                score += 2
            elif growth.get("growth_potential") == "medium":
                score += 1
            
            # Technology assessment
            tech = company.get("company_analysis", {}).get("key_technologies", [])
            score += min(2, len(tech) * 0.3)
        
        return min(10, max(0, score))
    
    def _analyze_sentiment(self, news_data: List[Dict]) -> float:
        """Analyze overall sentiment from news"""
        if not news_data:
            return 5.0
        
        sentiment_scores = []
        for item in news_data:
            sentiment = item.get("sentiment", {})
            if sentiment.get("label") == "bullish":
                sentiment_scores.append(7 + sentiment.get("confidence", 0.5) * 3)
            elif sentiment.get("label") == "bearish":
                sentiment_scores.append(3 - sentiment.get("confidence", 0.5) * 2)
            else:
                sentiment_scores.append(5)
        
        return min(10, max(0, sum(sentiment_scores) / len(sentiment_scores)))
    
    def _analyze_financials(self, company_data: List[Dict], market_data: List[Dict]) -> float:
        """Analyze financial metrics and investment potential"""
        score = 5.0
        
        if company_data:
            for company in company_data:
                # Investment metrics
                metrics = company.get("investment_metrics", {})
                funding = metrics.get("total_funding_usd", 0)
                
                if funding > 0:
                    if funding < 10000000:  # Less than $10M raised
                        score += 2  # Good for YC
                    elif funding < 50000000:  # $10-50M
                        score += 1
                    else:  # Over $50M
                        score -= 1  # May be too late stage
                
                # Valuation estimate
                valuation = metrics.get("valuation_estimate", 0)
                if 0 < valuation < 100000000:  # Under $100M valuation
                    score += 1.5
                elif valuation > 1000000000:  # Over $1B (unicorn)
                    score -= 2  # Too expensive for YC
        
        if market_data:
            # Market cap analysis
            relevant_market = [item for item in market_data 
                             if company_data and any(comp.get("company_name", "").lower() 
                                                    in item.get("name", "").lower() 
                                                    for comp in company_data)]
            if relevant_market:
                avg_market_cap = sum(item.get("market_cap", 0) for item in relevant_market) / len(relevant_market)
                if avg_market_cap > 1000000000:
                    score += 1  # Large market opportunity
        
        return min(10, max(0, score))
    
    def _make_investment_decision(self, overall_score: float) -> str:
        """Make investment decision based on score"""
        if overall_score >= 7.5:
            return "INVEST"
        elif overall_score >= 5.5:
            return "CONDITIONAL INVEST"
        else:
            return "PASS"
    
    def _calculate_investment_terms(self, company_data: List[Dict], market_data: List[Dict], 
                                   overall_score: float, decision: str) -> Dict[str, Any]:
        """Calculate investment terms and structure with random values"""
        
        # Generate random investment amounts and equity
        investment_amounts = [125000, 250000, 500000, 750000, 1000000, 1500000, 2000000]
        equity_percentages = [3.0, 5.0, 7.0, 10.0, 12.0, 15.0, 20.0]
        
        if decision == "INVEST":
            base_investment = random.choice([500000, 750000, 1000000, 1500000])
            equity_percentage = random.choice([7.0, 8.0, 10.0, 12.0])
        elif decision == "CONDITIONAL INVEST":
            base_investment = random.choice([125000, 250000, 375000])
            equity_percentage = random.choice([3.0, 5.0, 6.0])
        else:
            base_investment = 0
            equity_percentage = 0
        
        # Generate random valuations
        if equity_percentage > 0:
            post_money_valuation = random.randint(5000000, 100000000)
            pre_money_valuation = post_money_valuation - base_investment
        else:
            pre_money_valuation = 0
            post_money_valuation = 0
        
        # Random risk and return expectations
        risk_score = round(random.uniform(1, 10), 1)
        expected_return = random.choice([2, 3, 5, 8, 10, 15, 20, 25])
        
        # Investment structure
        structure = {
            "type": "SAFE" if decision == "INVEST" else "Convertible Note",
            "amount": base_investment,
            "pre_money_valuation": pre_money_valuation,
            "post_money_valuation": post_money_valuation,
            "yc_ownership": equity_percentage,
            "board_seats": 1 if base_investment >= 500000 else 0,
            "pro_rata_rights": base_investment >= 125000,
            "liquidation_preference": "1x non-participating" if base_investment > 0 else "N/A",
            "conversion_discount": 20 if decision == "CONDITIONAL INVEST" else 0,
            "valuation_cap": post_money_valuation * 1.5 if decision == "CONDITIONAL INVEST" else 0
        }
        
        return {
            "investment_amount": base_investment,
            "equity_percentage": equity_percentage,
            "pre_money_valuation": pre_money_valuation,
            "post_money_valuation": post_money_valuation,
            "risk_score": risk_score,
            "expected_return": expected_return,
            "structure": structure
        }
    
    def _generate_detailed_report(self, company_name: str, market_score: float, 
                                 company_score: float, sentiment_score: float,
                                 financial_score: float, overall_score: float,
                                 investment_terms: Dict, news_data: List[Dict],
                                 market_data: List[Dict], company_data: List[Dict]) -> Dict[str, Any]:
        """Generate comprehensive investment report"""
        
        # Executive Summary
        if overall_score >= 7.5:
            exec_summary = f"{company_name} presents an exceptional investment opportunity with strong market positioning, positive sentiment, and significant growth potential. The company scores {overall_score:.1f}/10 across our evaluation criteria, warranting immediate investment consideration."
        elif overall_score >= 5.5:
            exec_summary = f"{company_name} shows promise with moderate scores across key metrics ({overall_score:.1f}/10). While there are some concerns, the opportunity merits conditional investment with appropriate risk mitigation measures."
        else:
            exec_summary = f"{company_name} currently does not meet YC's investment criteria with a score of {overall_score:.1f}/10. Significant challenges in market positioning, sentiment, or financial metrics suggest this is not an optimal investment at this time."
        
        # Market Analysis
        market_analysis = f"Market conditions score: {market_score:.1f}/10. "
        if market_score >= 7:
            market_analysis += "The crypto market shows strong positive momentum with high trading volumes and bullish sentiment. This creates a favorable environment for growth and adoption."
        elif market_score >= 5:
            market_analysis += "Market conditions are neutral to moderately positive. While not exceptional, there are sufficient opportunities for well-positioned companies to succeed."
        else:
            market_analysis += "Current market conditions are challenging with bearish sentiment and low volumes. This increases execution risk and may limit near-term growth potential."
        
        # Investment Rationale
        rationale = self._generate_investment_rationale(overall_score, company_score, market_score, sentiment_score)
        
        # Key Risks
        risks = self._identify_key_risks(market_score, company_score, sentiment_score, financial_score, company_data)
        
        # Growth Opportunities
        opportunities = self._identify_growth_opportunities(company_data, market_data, news_data)
        
        # Exit Strategy
        exit_strategy = self._develop_exit_strategy(overall_score, investment_terms)
        
        # Expected Returns
        returns = {
            "3_year": round(investment_terms["expected_return"] * 0.4, 1),
            "5_year": round(investment_terms["expected_return"] * 0.7, 1),
            "7_year": round(investment_terms["expected_return"], 1)
        }
        
        return {
            "executive_summary": exec_summary,
            "market_analysis": market_analysis,
            "investment_rationale": rationale,
            "key_risks": risks,
            "growth_opportunities": opportunities,
            "exit_strategy": exit_strategy,
            "expected_returns": returns,
            "scores_breakdown": {
                "market_score": round(market_score, 2),
                "company_score": round(company_score, 2),
                "sentiment_score": round(sentiment_score, 2),
                "financial_score": round(financial_score, 2),
                "overall_score": round(overall_score, 2)
            }
        }
    
    def _generate_investment_rationale(self, overall_score: float, company_score: float, 
                                      market_score: float, sentiment_score: float) -> str:
        """Generate investment rationale"""
        rationale = "Investment rationale: "
        
        strengths = []
        if company_score >= 7:
            strengths.append("strong company fundamentals and team")
        if market_score >= 7:
            strengths.append("favorable market conditions")
        if sentiment_score >= 7:
            strengths.append("positive market sentiment and momentum")
        
        if strengths:
            rationale += f"The investment is supported by {', '.join(strengths)}. "
        
        if overall_score >= 7.5:
            rationale += "This represents a high-conviction opportunity with potential for exceptional returns. The combination of market timing, company quality, and growth potential creates an asymmetric risk-reward profile favorable to YC."
        elif overall_score >= 5.5:
            rationale += "While not without risks, the opportunity offers sufficient upside potential to warrant investment with appropriate structuring and monitoring."
        else:
            rationale += "The risk-reward profile does not currently favor investment. Key concerns include market headwinds, execution risks, or valuation considerations."
        
        return rationale
    
    def _identify_key_risks(self, market_score: float, company_score: float, 
                           sentiment_score: float, financial_score: float,
                           company_data: List[Dict]) -> List[str]:
        """Identify key investment risks"""
        risks = []
        
        if market_score < 5:
            risks.append("Adverse market conditions may limit growth and exit opportunities")
        
        if company_score < 5:
            risks.append("Company fundamentals or team capabilities require improvement")
        
        if sentiment_score < 5:
            risks.append("Negative market sentiment could impact adoption and fundraising")
        
        if financial_score < 5:
            risks.append("Financial metrics or valuation concerns present investment risk")
        
        # Add specific risks from company data
        if company_data:
            for company in company_data:
                risk_assessment = company.get("risk_assessment", {})
                if risk_assessment.get("regulatory_risk") == "high":
                    risks.append("High regulatory risk in current jurisdiction")
                if risk_assessment.get("technology_risk") == "high":
                    risks.append("Technology implementation or scalability risks")
        
        if not risks:
            risks.append("Standard execution and market risks apply")
            risks.append("Cryptocurrency market volatility")
            risks.append("Competitive pressure from established players")
        
        return risks[:5]  # Return top 5 risks
    
    def _identify_growth_opportunities(self, company_data: List[Dict], 
                                      market_data: List[Dict], 
                                      news_data: List[Dict]) -> List[str]:
        """Identify growth opportunities"""
        opportunities = []
        
        # Market-based opportunities
        if market_data:
            high_growth_markets = [item for item in market_data 
                                  if item.get("change_24h", 0) > 10]
            if high_growth_markets:
                opportunities.append("Rapid market expansion in core cryptocurrency segments")
        
        # Company-based opportunities
        if company_data:
            for company in company_data:
                tech = company.get("company_analysis", {}).get("key_technologies", [])
                if "defi" in tech:
                    opportunities.append("DeFi integration and yield generation opportunities")
                if "nft" in tech:
                    opportunities.append("NFT marketplace and digital asset monetization")
                if "web3" in tech:
                    opportunities.append("Web3 infrastructure and decentralized application development")
                
                if company.get("growth_indicators", {}).get("growth_potential") == "high":
                    opportunities.append("Strong organic growth trajectory based on current metrics")
        
        # News-based opportunities
        if news_data:
            bullish_news = [item for item in news_data 
                           if item.get("sentiment", {}).get("label") == "bullish"]
            if len(bullish_news) > len(news_data) / 2:
                opportunities.append("Positive market sentiment driving increased adoption")
        
        # Default opportunities
        if not opportunities:
            opportunities = [
                "Expansion into emerging markets",
                "Product diversification and new revenue streams",
                "Strategic partnerships with established players",
                "International market expansion",
                "Technology licensing and B2B opportunities"
            ]
        
        return opportunities[:5]  # Return top 5 opportunities
    
    def _develop_exit_strategy(self, overall_score: float, investment_terms: Dict) -> str:
        """Develop exit strategy"""
        if overall_score >= 7.5:
            return "Primary exit via IPO within 5-7 years given strong fundamentals and market position. Secondary options include strategic acquisition by major tech/finance companies. Expected valuation of $5-10B at exit based on current trajectory."
        elif overall_score >= 5.5:
            return "Likely exit via strategic acquisition within 4-6 years by larger crypto/fintech players. Alternative paths include merger with complementary businesses or secondary sale. Target exit valuation of $500M-2B."
        else:
            return "Limited exit visibility in current state. Focus on achieving product-market fit and sustainable growth before considering exit options. Potential acqui-hire or asset sale if growth targets not met."
    
    def _create_investment_timeline(self, decision: str, company_name: str, investment_amount: float = 500000) -> List[Dict[str, str]]:
        """Create investment timeline"""
        if decision == "PASS":
            return [{
                "timeframe": "Immediate",
                "milestone": "Investment Declined",
                "description": "Based on current analysis, YC will not proceed with investment"
            }]
        
        timeline = [
            {
                "timeframe": "Week 1",
                "milestone": "Initial Due Diligence",
                "description": f"Complete technical, legal, and financial due diligence on {company_name}"
            },
            {
                "timeframe": "Week 2",
                "milestone": "Term Sheet Negotiation",
                "description": "Present and negotiate investment terms with founding team"
            },
            {
                "timeframe": "Week 3-4",
                "milestone": "Legal Documentation",
                "description": "Finalize SAFE agreement and complete legal requirements"
            },
            {
                "timeframe": "Month 2",
                "milestone": "Capital Deployment",
                "description": f"Transfer ${investment_amount:,} investment to company"
            },
            {
                "timeframe": "Month 3-6",
                "milestone": "YC Program Participation",
                "description": "3-month accelerator program with mentorship and resources"
            },
            {
                "timeframe": "Month 6",
                "milestone": "Demo Day",
                "description": "Present to investor network for Series A fundraising"
            },
            {
                "timeframe": "Year 1",
                "milestone": "Series A Support",
                "description": "Assist with Series A fundraising and strategic introductions"
            },
            {
                "timeframe": "Year 2-3",
                "milestone": "Growth Monitoring",
                "description": "Board participation and strategic guidance for scaling"
            },
            {
                "timeframe": "Year 3-5",
                "milestone": "Exit Preparation",
                "description": "Position company for strategic exit or IPO"
            }
        ]
        
        if decision == "CONDITIONAL INVEST":
            timeline.insert(1, {
                "timeframe": "Week 1-2",
                "milestone": "Condition Resolution",
                "description": "Address specific concerns and meet investment conditions"
            })
        
        return timeline
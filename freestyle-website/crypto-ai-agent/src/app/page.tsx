"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export default function Home() {
  const [chatMessages, setChatMessages] = useState([
    { role: "assistant", content: "Hello! I'm your crypto VC investment assistant. I can help you analyze projects, evaluate investment opportunities, conduct due diligence, and assess market trends for venture capital decisions. What would you like to explore?" }
  ]);
  const [chatInput, setChatInput] = useState("");

  const handleSendMessage = () => {
    if (!chatInput.trim()) return;

    const newMessage = { role: "user", content: chatInput };
    setChatMessages(prev => [...prev, newMessage]);

    // Simulate AI response
    setTimeout(() => {
      const responses = [
        "Based on current market trends, I see strong institutional adoption in the crypto space. Several promising Layer 2 projects are gaining significant traction for potential investment.",
        "The VC landscape is showing increased interest in DeFi infrastructure and cross-chain protocols. These sectors present compelling investment opportunities.",
        "Recent funding rounds indicate strong investor confidence in AI-crypto convergence projects. The intersection of these technologies shows high growth potential.",
        "I'm analyzing several early-stage projects in the RWA (Real World Assets) tokenization space. This sector is attracting significant institutional capital.",
        "Current market conditions favor investments in utility tokens with strong fundamentals and clear revenue models. Focus on projects with proven product-market fit.",
        "The regulatory environment is becoming clearer, which should unlock more institutional capital. Consider positioning in compliant, well-structured projects.",
      ];
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      setChatMessages(prev => [...prev, { role: "assistant", content: randomResponse }]);
    }, 1000);

    setChatInput("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-orange-400 to-orange-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">CA</span>
              </div>
              <h1 className="text-2xl font-bold text-white">Crypto Investment</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-green-400 border-green-400">
                Investment Research
              </Badge>
              <Avatar>
                <AvatarFallback>AI</AvatarFallback>
              </Avatar>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6 h-[calc(100vh-88px)]">
        {/* Split Screen Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">

          {/* AI Chat Section - Left Side */}
          <Card className="bg-slate-800 border-slate-700 flex flex-col h-full">
            <CardHeader className="pb-4">
              <CardTitle className="text-white text-xl">Crypto VC Investment Assistant</CardTitle>
              <CardDescription className="text-slate-300">
                Get investment analysis, due diligence insights, and market research
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col min-h-0">
              <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
                {chatMessages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[85%] p-4 rounded-xl ${
                        message.role === 'user'
                          ? 'bg-orange-600 text-white rounded-br-sm'
                          : 'bg-slate-700 text-slate-100 rounded-bl-sm'
                      }`}
                    >
                      <div className="text-sm leading-relaxed">{message.content}</div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex space-x-3 pt-2 border-t border-slate-700">
                <Input
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="Ask about investment opportunities, due diligence, market analysis, or project evaluation..."
                  className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500"
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                />
                <Button
                  onClick={handleSendMessage}
                  className="bg-orange-600 hover:bg-orange-700 px-6"
                  disabled={!chatInput.trim()}
                >
                  Send
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Company Information Section - Right Side */}
          <div className="space-y-6 h-full overflow-y-auto">
            {/* Company Overview */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white text-xl">Company Information</CardTitle>
                <CardDescription className="text-slate-300">A16Z-style investment analysis framework</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">

                  {/* Thesis Fit */}
                  <div className="space-y-3">
                    <h3 className="text-orange-400 font-semibold text-lg flex items-center">
                      <div className="w-2 h-2 bg-orange-400 rounded-full mr-3"></div>
                      Thesis Fit & Narrative
                    </h3>
                    <p className="text-slate-300 text-sm leading-relaxed pl-5">
                      Evaluate how the startup aligns with a current A16Z crypto investment thesis, and whether it fits with macro trends.
                    </p>
                  </div>

                  {/* Market Analysis */}
                  <div className="space-y-3">
                    <h3 className="text-blue-400 font-semibold text-lg flex items-center">
                      <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
                      Market & Trend Analysis
                    </h3>
                    <p className="text-slate-300 text-sm leading-relaxed pl-5">
                      Assess market size, timing, competitive landscape, and adoption drivers. Use relevant historical funding patterns in blockchain and AI.
                    </p>
                  </div>

                  {/* Team Assessment */}
                  <div className="space-y-3">
                    <h3 className="text-green-400 font-semibold text-lg flex items-center">
                      <div className="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
                      Team Assessment
                    </h3>
                    <p className="text-slate-300 text-sm leading-relaxed pl-5">
                      Judge founder-market fit, technical strength, execution capability, and uniqueness.
                    </p>
                  </div>

                  {/* Traction & Metrics */}
                  <div className="space-y-3">
                    <h3 className="text-purple-400 font-semibold text-lg flex items-center">
                      <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                      Traction & Metrics
                    </h3>
                    <p className="text-slate-300 text-sm leading-relaxed pl-5">
                      Analyze product stage, key KPIs, and growth trajectory.
                    </p>
                  </div>

                  {/* Risk Profile */}
                  <div className="space-y-3">
                    <h3 className="text-red-400 font-semibold text-lg flex items-center">
                      <div className="w-2 h-2 bg-red-400 rounded-full mr-3"></div>
                      Risk Profile
                    </h3>
                    <p className="text-slate-300 text-sm leading-relaxed pl-5">
                      Identify main risks (technical, regulatory, market, adoption).
                    </p>
                  </div>

                  {/* Valuation & Funding */}
                  <div className="space-y-3">
                    <h3 className="text-yellow-400 font-semibold text-lg flex items-center">
                      <div className="w-2 h-2 bg-yellow-400 rounded-full mr-3"></div>
                      Valuation & Funding
                    </h3>
                    <p className="text-slate-300 text-sm leading-relaxed pl-5">
                      Recommend valuation and round size based on comparable deals and market heat.
                    </p>
                  </div>

                  {/* Investment Decision */}
                  <div className="space-y-3">
                    <h3 className="text-cyan-400 font-semibold text-lg flex items-center">
                      <div className="w-2 h-2 bg-cyan-400 rounded-full mr-3"></div>
                      Investment Decision
                    </h3>
                    <p className="text-slate-300 text-sm leading-relaxed pl-5">
                      State whether to invest, why, and what check size to write.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Output Format */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white text-xl">Analysis Output Format</CardTitle>
                <CardDescription className="text-slate-300">Structured investment memo template</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-1 gap-3">
                    <div className="p-3 rounded-lg bg-slate-700/30 border border-slate-600">
                      <div className="text-orange-400 font-medium text-sm">Thesis Fit:</div>
                      <div className="text-slate-400 text-xs mt-1">Alignment with investment thesis</div>
                    </div>

                    <div className="p-3 rounded-lg bg-slate-700/30 border border-slate-600">
                      <div className="text-blue-400 font-medium text-sm">Market Analysis:</div>
                      <div className="text-slate-400 text-xs mt-1">Market size and competitive landscape</div>
                    </div>

                    <div className="p-3 rounded-lg bg-slate-700/30 border border-slate-600">
                      <div className="text-green-400 font-medium text-sm">Team Analysis:</div>
                      <div className="text-slate-400 text-xs mt-1">Founder-market fit assessment</div>
                    </div>

                    <div className="p-3 rounded-lg bg-slate-700/30 border border-slate-600">
                      <div className="text-purple-400 font-medium text-sm">Traction:</div>
                      <div className="text-slate-400 text-xs mt-1">KPIs and growth metrics</div>
                    </div>

                    <div className="p-3 rounded-lg bg-slate-700/30 border border-slate-600">
                      <div className="text-red-400 font-medium text-sm">Risks:</div>
                      <div className="text-slate-400 text-xs mt-1">Key risk factors</div>
                    </div>

                    <div className="p-3 rounded-lg bg-slate-700/30 border border-slate-600">
                      <div className="text-yellow-400 font-medium text-sm">Valuation Recommendation:</div>
                      <div className="text-slate-400 text-xs mt-1">Suggested valuation range</div>
                    </div>

                    <div className="p-3 rounded-lg bg-slate-700/30 border border-slate-600">
                      <div className="text-cyan-400 font-medium text-sm">Decision:</div>
                      <div className="text-slate-400 text-xs mt-1">Invest/Pass with rationale</div>
                    </div>
                  </div>

                  <div className="mt-4 p-4 rounded-lg bg-gradient-to-r from-orange-900/20 to-orange-800/20 border border-orange-700/50">
                    <h4 className="text-orange-400 font-semibold mb-2">One-Sentence Memo Headline:</h4>
                    <p className="text-slate-300 text-sm italic">
                      Short A16Z-style investment summary
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

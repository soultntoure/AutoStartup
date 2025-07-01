import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Lightbulb, Zap, Github, TrendingUp, Search, Clock, CheckCircle, AlertCircle, ChevronDown, ChevronRight } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Job {
  job_id: string;
  status: string;
  started_at: string;
  progress: number;
  current_task?: string;
  progress_percentage?: number;
}

interface JobResults {
  competitor_analysis?: { result: string };
  gap_finding?: { result: string };
  github_scaffolding?: { result: string };
}

const API_BASE = "http://127.0.0.1:8000";
const API_KEY = "92013b1783117dce8440736634d9953ad09887b6";

const Index = () => {
  const [idea, setIdea] = useState("");
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<Job | null>(null);
  const [jobResults, setJobResults] = useState<JobResults | null>(null);
  const [jobHistory, setJobHistory] = useState<Record<string, Job>>({});
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null);
  const [expandedJobs, setExpandedJobs] = useState<Record<string, boolean>>({});
  const [jobResultsCache, setJobResultsCache] = useState<Record<string, JobResults>>({});
  const [selectedResult, setSelectedResult] = useState<{
    jobId: string;
    type: 'competitor_analysis' | 'gap_finding' | 'github_scaffolding';
  } | null>(null);
  const { toast } = useToast();

  const headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY,
  };

  const fetchJobHistory = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/startup/jobs`, { headers });
      const data = await response.json();
      setJobHistory(data.jobs || {});
    } catch (error) {
      console.error("Failed to fetch job history:", error);
    }
  };

  useEffect(() => {
    fetchJobHistory();
  }, []);

  const analyzeIdea = async () => {
    if (!idea.trim()) {
      toast({ title: "Please enter your startup idea", variant: "destructive" });
      return;
    }

    setIsAnalyzing(true);
    setJobResults(null);
    setSelectedJobId(null);
    setSelectedResult(null);

    try {
      const response = await fetch(`${API_BASE}/api/startup/analyze`, {
        method: "POST",
        headers,
        body: JSON.stringify({ idea }),
      });

      const data = await response.json();
      setCurrentJobId(data.job_id);
      setJobStatus(data);
      
      toast({ 
        title: "Analysis Started!", 
        description: `Job ${data.job_id.slice(0, 8)}... is now running` 
      });
    } catch (error) {
      console.error("Failed to start analysis:", error);
      toast({ title: "Failed to start analysis", variant: "destructive" });
      setIsAnalyzing(false);
    }
  };

  const pollJobStatus = async (jobId: string) => {
    try {
      const response = await fetch(`${API_BASE}/api/startup/status/${jobId}`, { headers });
      const data = await response.json();
      setJobStatus(data);

      if (data.status === "completed") {
        const resultsResponse = await fetch(`${API_BASE}/api/startup/results/${jobId}`, { headers });
        const resultsData = await resultsResponse.json();
        setJobResults(resultsData.results);
        setJobResultsCache(prev => ({ ...prev, [jobId]: resultsData.results }));
        setIsAnalyzing(false);
        fetchJobHistory();
        toast({ 
          title: "Analysis Complete!", 
          description: "Your startup analysis is ready to view" 
        });
      } else if (data.status === "failed") {
        setIsAnalyzing(false);
        toast({ title: "Analysis failed", variant: "destructive" });
      }
    } catch (error) {
      console.error("Failed to poll job status:", error);
    }
  };

  useEffect(() => {
    if (currentJobId && isAnalyzing) {
      const interval = setInterval(() => {
        pollJobStatus(currentJobId);
      }, 10000);

      return () => clearInterval(interval);
    }
  }, [currentJobId, isAnalyzing]);

  const loadJobResults = async (jobId: string) => {
    // Check cache first
    if (jobResultsCache[jobId]) {
      setJobResults(jobResultsCache[jobId]);
      setSelectedJobId(jobId);
      setSelectedResult(null);
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/startup/results/${jobId}`, { headers });
      const data = await response.json();
      setJobResults(data.results);
      setJobResultsCache(prev => ({ ...prev, [jobId]: data.results }));
      setSelectedJobId(jobId);
      setSelectedResult(null);
    } catch (error) {
      console.error("Failed to load job results:", error);
      toast({ title: "Failed to load results", variant: "destructive" });
    }
  };

  const toggleJobExpansion = (jobId: string) => {
    setExpandedJobs(prev => ({
      ...prev,
      [jobId]: !prev[jobId]
    }));
  };

  const selectSpecificResult = (jobId: string, type: 'competitor_analysis' | 'gap_finding' | 'github_scaffolding') => {
    setSelectedResult({ jobId, type });
    setSelectedJobId(jobId);
    
    // Load results if not cached
    if (!jobResultsCache[jobId]) {
      loadJobResults(jobId);
    } else {
      setJobResults(jobResultsCache[jobId]);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed": return "bg-green-500";
      case "failed": return "bg-red-500";
      case "running": return "bg-blue-500";
      default: return "bg-gray-500";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed": return <CheckCircle className="h-4 w-4" />;
      case "failed": return <AlertCircle className="h-4 w-4" />;
      case "running": return <Clock className="h-4 w-4" />;
      default: return <Clock className="h-4 w-4" />;
    }
  };

  const getResultTitle = (type: string) => {
    switch (type) {
      case 'competitor_analysis': return 'Competitor Analysis';
      case 'gap_finding': return 'Gap Analysis';
      case 'github_scaffolding': return 'GitHub Repository';
      default: return type;
    }
  };

  const getResultIcon = (type: string) => {
    switch (type) {
      case 'competitor_analysis': return <TrendingUp className="h-4 w-4" />;
      case 'gap_finding': return <Search className="h-4 w-4" />;
      case 'github_scaffolding': return <Github className="h-4 w-4" />;
      default: return <Search className="h-4 w-4" />;
    }
  };

  const renderSelectedResult = () => {
    if (!selectedResult || !jobResults) return null;

    const result = jobResults[selectedResult.type];
    if (!result) return null;

    const title = getResultTitle(selectedResult.type);
    const icon = getResultIcon(selectedResult.type);

    return (
      <div className="space-y-6">
        <div className="text-center">
          <h2 className="text-2xl font-bold">{title}</h2>
          <p className="text-sm text-gray-500">Job ID: {selectedResult.jobId.slice(0, 8)}...</p>
        </div>
        
        <Card className="shadow-lg border-0 bg-white/80 backdrop-blur animate-fade-in">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {icon}
              {title}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {selectedResult.type === 'github_scaffolding' ? (
              <div className="flex items-center justify-between">
                <p className="text-gray-700">Your project scaffolding is ready!</p>
                <Button 
                  asChild
                  className="bg-gray-900 hover:bg-gray-800"
                >
                  <a 
                    href={result.result} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center gap-2"
                  >
                    <Github className="h-4 w-4" />
                    Open Repository
                  </a>
                </Button>
              </div>
            ) : (
              <div className="prose max-w-none">
                <p className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                  {result.result}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="flex">
        {/* Sidebar */}
        <div className="w-80 bg-white border-r shadow-sm min-h-screen">
          <div className="p-6">
            <div className="flex items-center gap-2 mb-6">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
                <Lightbulb className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AutoStartup
                </h1>
                <p className="text-sm text-gray-500">AI-Powered Analysis</p>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                <Clock className="h-4 w-4" />
                Job History
              </h3>
              
              {Object.entries(jobHistory).length === 0 ? (
                <p className="text-sm text-gray-500 italic">No jobs yet</p>
              ) : (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {Object.entries(jobHistory).map(([jobId, job]) => (
                    <div key={jobId} className="space-y-1">
                      <Card 
                        className={`cursor-pointer transition-all hover:shadow-md ${
                          selectedJobId === jobId && !selectedResult ? 'ring-2 ring-blue-500' : ''
                        }`}
                        onClick={() => loadJobResults(jobId)}
                      >
                        <CardContent className="p-3">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              {getStatusIcon(job.status)}
                              <span className="text-sm font-mono">
                                {jobId.slice(0, 8)}...
                              </span>
                              {job.status === "completed" && (
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  className="h-6 w-6 p-0"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    toggleJobExpansion(jobId);
                                  }}
                                >
                                  {expandedJobs[jobId] ? 
                                    <ChevronDown className="h-3 w-3" /> : 
                                    <ChevronRight className="h-3 w-3" />
                                  }
                                </Button>
                              )}
                            </div>
                            <Badge className={`${getStatusColor(job.status)} text-white`}>
                              {job.status}
                            </Badge>
                          </div>
                          <div className="mt-2">
                            <Progress value={job.progress} className="h-1" />
                            <p className="text-xs text-gray-500 mt-1">
                              {new Date(job.started_at).toLocaleString()}
                            </p>
                          </div>
                        </CardContent>
                      </Card>
                      
                      {/* Expandable Results */}
                      {expandedJobs[jobId] && job.status === "completed" && (
                        <div className="ml-4 space-y-1">
                          <div 
                            className={`flex items-center gap-2 p-2 rounded-md cursor-pointer hover:bg-gray-100 transition-colors ${
                              selectedResult?.jobId === jobId && selectedResult?.type === 'competitor_analysis' ? 'bg-blue-50 text-blue-700' : ''
                            }`}
                            onClick={() => selectSpecificResult(jobId, 'competitor_analysis')}
                          >
                            <TrendingUp className="h-4 w-4" />
                            <span className="text-sm">Competitor Analysis</span>
                          </div>
                          <div 
                            className={`flex items-center gap-2 p-2 rounded-md cursor-pointer hover:bg-gray-100 transition-colors ${
                              selectedResult?.jobId === jobId && selectedResult?.type === 'gap_finding' ? 'bg-blue-50 text-blue-700' : ''
                            }`}
                            onClick={() => selectSpecificResult(jobId, 'gap_finding')}
                          >
                            <Search className="h-4 w-4" />
                            <span className="text-sm">Gap Analysis</span>
                          </div>
                          <div 
                            className={`flex items-center gap-2 p-2 rounded-md cursor-pointer hover:bg-gray-100 transition-colors ${
                              selectedResult?.jobId === jobId && selectedResult?.type === 'github_scaffolding' ? 'bg-blue-50 text-blue-700' : ''
                            }`}
                            onClick={() => selectSpecificResult(jobId, 'github_scaffolding')}
                          >
                            <Github className="h-4 w-4" />
                            <span className="text-sm">GitHub Repository</span>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-8">
          <div className="max-w-4xl mx-auto space-y-8">
            {/* Header */}
            <div className="text-center space-y-4">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Transform Your Startup Ideas
              </h1>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Get AI-powered competitor analysis, market gap insights, and a ready-to-code GitHub repository
              </p>
            </div>

            {/* Input Form */}
            <Card className="shadow-lg border-0 bg-white/80 backdrop-blur">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5 text-blue-500" />
                  Describe Your Startup Idea
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder="e.g., An app that helps people find and book local fitness classes easily..."
                  value={idea}
                  onChange={(e) => setIdea(e.target.value)}
                  className="min-h-32 text-lg border-2 focus:border-blue-500 transition-colors"
                  disabled={isAnalyzing}
                />
                <Button
                  onClick={analyzeIdea}
                  disabled={isAnalyzing}
                  className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-lg py-6 transition-all transform hover:scale-105"
                >
                  {isAnalyzing ? (
                    <div className="flex items-center gap-2">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      Analyzing...
                    </div>
                  ) : (
                    <div className="flex items-center gap-2">
                      <Search className="h-5 w-5" />
                      Analyze Idea
                    </div>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Progress Tracker */}
            {isAnalyzing && jobStatus && (
              <Card className="shadow-lg border-0 bg-gradient-to-r from-blue-50 to-purple-50">
                <CardContent className="p-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold">Analysis in Progress</h3>
                      <Badge className="bg-blue-500 text-white">
                        {jobStatus.progress_percentage || 0}% Complete
                      </Badge>
                    </div>
                    
                    <Progress 
                      value={jobStatus.progress_percentage || 0} 
                      className="h-3 bg-white/50"
                    />
                    
                    {jobStatus.current_task && (
                      <div className="mt-2 text-sm text-gray-700 space-y-1">
                        <div className="flex items-center gap-2">
                          <div className="animate-pulse h-2 w-2 bg-blue-500 rounded-full"></div>
                          <span>Task: {jobStatus.current_task.replace('_', ' ').toUpperCase()}</span>
                        </div>
                        {jobStatus.current_agent && (
                          <div className="flex items-center gap-2 pl-4">
                            <span className="font-semibold">Agent:</span>
                            <span>{jobStatus.current_agent}</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Results Display */}
            {selectedResult ? (
              renderSelectedResult()
            ) : jobResults && !selectedResult && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-center">Analysis Results</h2>
                
                {jobResults.competitor_analysis && (
                  <Card className="shadow-lg border-0 bg-white/80 backdrop-blur animate-fade-in">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <TrendingUp className="h-5 w-5 text-green-500" />
                        Competitor Analysis
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="prose max-w-none">
                        <p className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                          {jobResults.competitor_analysis.result}
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {jobResults.gap_finding && (
                  <Card className="shadow-lg border-0 bg-white/80 backdrop-blur animate-fade-in">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Search className="h-5 w-5 text-blue-500" />
                        Gap Analysis
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="prose max-w-none">
                        <p className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                          {jobResults.gap_finding.result}
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {jobResults.github_scaffolding && (
                  <Card className="shadow-lg border-0 bg-gradient-to-r from-green-50 to-blue-50 animate-fade-in">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Github className="h-5 w-5 text-gray-800" />
                        GitHub Repository
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between">
                        <p className="text-gray-700">Your project scaffolding is ready!</p>
                        <Button 
                          asChild
                          className="bg-gray-900 hover:bg-gray-800"
                        >
                          <a 
                            href={jobResults.github_scaffolding.result} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="flex items-center gap-2"
                          >
                            <Github className="h-4 w-4" />
                            Open Repository
                          </a>
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;

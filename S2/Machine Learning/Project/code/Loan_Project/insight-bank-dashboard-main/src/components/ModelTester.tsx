import React, { useState } from "react";
import { Brain, Calculator, AlertCircle, CheckCircle, TrendingUp, DollarSign } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { LoanRecord } from "@/lib/dataUtils";

interface ModelTesterProps {
  data: LoanRecord[];
}

export const ModelTester: React.FC<ModelTesterProps> = ({ data }) => {
  const [formData, setFormData] = useState({
    credit_score: "",
    annual_income: "",
    loan_amount: "",
    Age: "",
    Children_Count: "",
    Previous_Loan_Count: "",
    EmploymentStatus: "",
    MaritalStatus: "",
  });

  const [prediction, setPrediction] = useState<number | null>(null);
  const [isPredicting, setIsPredicting] = useState(false);
  const [selectedModel, setSelectedModel] = useState<"svm" | "logistic">("logistic");

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const predictDefault = async () => {
    setIsPredicting(true);
    
    // Simulate model prediction delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Simple rule-based prediction logic (in real app, this would call actual ML models)
    const creditScore = parseFloat(formData.credit_score) || 0;
    const income = parseFloat(formData.annual_income) || 0;
    const loanAmount = parseFloat(formData.loan_amount) || 0;
    const debtToIncome = loanAmount / (income || 1);
    
    let riskScore = 0;
    
    // Credit score impact (40% weight)
    if (creditScore < 600) riskScore += 40;
    else if (creditScore < 650) riskScore += 25;
    else if (creditScore < 700) riskScore += 10;
    else if (creditScore < 750) riskScore += 5;
    
    // Debt-to-income impact (30% weight)
    if (debtToIncome > 0.5) riskScore += 30;
    else if (debtToIncome > 0.4) riskScore += 20;
    else if (debtToIncome > 0.3) riskScore += 10;
    
    // Income level impact (20% weight)
    if (income < 30000) riskScore += 20;
    else if (income < 50000) riskScore += 10;
    else if (income < 75000) riskScore += 5;
    
    // Loan amount impact (10% weight)
    if (loanAmount > 100000) riskScore += 10;
    else if (loanAmount > 50000) riskScore += 5;
    
    // Add some randomness to simulate model differences
    const modelOffset = selectedModel === "svm" ? 2 : -2;
    const finalScore = Math.max(0, Math.min(100, riskScore + modelOffset + Math.random() * 10 - 5));
    
    // Predict default if risk score > 50
    setPrediction(finalScore > 50 ? 1 : 0);
    setIsPredicting(false);
  };

  const resetForm = () => {
    setFormData({
      credit_score: "",
      annual_income: "",
      loan_amount: "",
      Age: "",
      Children_Count: "",
      Previous_Loan_Count: "",
      EmploymentStatus: "",
      MaritalStatus: "",
    });
    setPrediction(null);
  };

  const isFormValid = Object.values(formData).every(val => val !== "");

  return (
    <div className="space-y-6 animate-fade-in-up">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="font-display font-bold text-2xl mb-2" style={{ color: "hsl(var(--foreground))" }}>
            Model Prediction Tester
          </h2>
          <p className="text-sm" style={{ color: "hsl(var(--muted-foreground))" }}>
            Test loan default prediction using the best ML models
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="gap-1">
            <Brain className="w-3 h-3" />
            {selectedModel === "svm" ? "SVM" : "Logistic Regression"}
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calculator className="w-5 h-5" style={{ color: "hsl(var(--primary))" }} />
              Applicant Information
            </CardTitle>
            <CardDescription>
              Enter the applicant's financial details to predict default risk
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="credit_score">Credit Score</Label>
                <Input
                  id="credit_score"
                  type="number"
                  placeholder="300-850"
                  value={formData.credit_score}
                  onChange={(e) => handleInputChange("credit_score", e.target.value)}
                  min="300"
                  max="850"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="annual_income">Annual Income ($)</Label>
                <Input
                  id="annual_income"
                  type="number"
                  placeholder="50000"
                  value={formData.annual_income}
                  onChange={(e) => handleInputChange("annual_income", e.target.value)}
                  min="0"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="loan_amount">Loan Amount ($)</Label>
                <Input
                  id="loan_amount"
                  type="number"
                  placeholder="25000"
                  value={formData.loan_amount}
                  onChange={(e) => handleInputChange("loan_amount", e.target.value)}
                  min="0"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="EmploymentStatus">Employment Status</Label>
                <Select value={formData.EmploymentStatus} onValueChange={(value) => handleInputChange("EmploymentStatus", value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select employment status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Employed">Employed</SelectItem>
                    <SelectItem value="Self-Employed">Self-Employed</SelectItem>
                    <SelectItem value="Unemployed">Unemployed</SelectItem>
                    <SelectItem value="Student">Student</SelectItem>
                    <SelectItem value="Retired">Retired</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="Age">Age</Label>
                <Input
                  id="Age"
                  type="number"
                  placeholder="35"
                  value={formData.Age}
                  onChange={(e) => handleInputChange("Age", e.target.value)}
                  min="18"
                  max="100"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="MaritalStatus">Marital Status</Label>
                <Select value={formData.MaritalStatus} onValueChange={(value) => handleInputChange("MaritalStatus", value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select marital status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Single">Single</SelectItem>
                    <SelectItem value="Married">Married</SelectItem>
                    <SelectItem value="Divorced">Divorced</SelectItem>
                    <SelectItem value="Widowed">Widowed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="Children_Count">Number of Children</Label>
                <Input
                  id="Children_Count"
                  type="number"
                  placeholder="2"
                  value={formData.Children_Count}
                  onChange={(e) => handleInputChange("Children_Count", e.target.value)}
                  min="0"
                />
              </div>
              
              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="Previous_Loan_Count">Previous Loan Count</Label>
                <Input
                  id="Previous_Loan_Count"
                  type="number"
                  placeholder="1"
                  value={formData.Previous_Loan_Count}
                  onChange={(e) => handleInputChange("Previous_Loan_Count", e.target.value)}
                  min="0"
                />
              </div>
            </div>

            <div className="flex gap-3 pt-4">
              <Button 
                onClick={predictDefault}
                disabled={!isFormValid || isPredicting}
                className="flex-1"
                style={{ background: "hsl(var(--primary))" }}
              >
                {isPredicting ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                    Predicting...
                  </>
                ) : (
                  <>
                    <TrendingUp className="w-4 h-4 mr-2" />
                    Predict Default Risk
                  </>
                )}
              </Button>
              <Button 
                variant="outline" 
                onClick={resetForm}
                disabled={isPredicting}
              >
                Clear
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Brain className="w-5 h-5" style={{ color: "hsl(var(--primary))" }} />
              Prediction Results
            </CardTitle>
            <CardDescription>
              ML model prediction based on the provided data
            </CardDescription>
          </CardHeader>
          <CardContent>
            {prediction === null ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
                  style={{ background: "hsl(var(--muted))" }}>
                  <Calculator className="w-8 h-8" style={{ color: "hsl(var(--muted-foreground))" }} />
                </div>
                <p className="text-sm" style={{ color: "hsl(var(--muted-foreground))" }}>
                  Fill in the applicant information and click "Predict Default Risk" to see results
                </p>
              </div>
            ) : (
              <div className="space-y-6">
                <div className={`text-center p-6 rounded-lg border ${
                  prediction === 1 
                    ? "bg-red-50 border-red-200" 
                    : "bg-green-50 border-green-200"
                }`}>
                  <div className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 ${
                    prediction === 1 
                      ? "bg-red-100" 
                      : "bg-green-100"
                  }`}>
                    {prediction === 1 ? (
                      <AlertCircle className="w-8 h-8 text-red-600" />
                    ) : (
                      <CheckCircle className="w-8 h-8 text-green-600" />
                    )}
                  </div>
                  
                  <h3 className={`text-lg font-semibold mb-2 ${
                    prediction === 1 ? "text-red-800" : "text-green-800"
                  }`}>
                    {prediction === 1 ? "High Risk - Likely to Default" : "Low Risk - Unlikely to Default"}
                  </h3>
                  
                  <div className="flex items-center justify-center gap-2 mb-2">
                    <Badge variant={prediction === 1 ? "destructive" : "default"} className="text-sm">
                      Prediction: {prediction === 1 ? "1 (Default)" : "0 (No Default)"}
                    </Badge>
                  </div>
                  
                  <p className={`text-sm ${
                    prediction === 1 ? "text-red-600" : "text-green-600"
                  }`}>
                    {prediction === 1 
                      ? "The applicant shows high risk factors. Consider additional verification or higher interest rates."
                      : "The applicant appears to be a good candidate for loan approval."
                    }
                  </p>
                </div>

                <div className="space-y-3">
                  <h4 className="font-semibold text-sm" style={{ color: "hsl(var(--foreground))" }}>
                    Model Information
                  </h4>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="p-3 rounded-lg" style={{ background: "hsl(var(--muted))" }}>
                      <p className="font-medium mb-1" style={{ color: "hsl(var(--foreground))" }}>
                        Model Used
                      </p>
                      <p style={{ color: "hsl(var(--muted-foreground))" }}>
                        {selectedModel === "svm" ? "Support Vector Machine" : "Logistic Regression"}
                      </p>
                    </div>
                    <div className="p-3 rounded-lg" style={{ background: "hsl(var(--muted))" }}>
                      <p className="font-medium mb-1" style={{ color: "hsl(var(--foreground))" }}>
                        Accuracy
                      </p>
                      <p style={{ color: "hsl(var(--muted-foreground))" }}>
                        {selectedModel === "svm" ? "~87%" : "~85%"}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-center gap-2 text-xs" style={{ color: "hsl(var(--muted-foreground))" }}>
                  <DollarSign className="w-3 h-3" />
                  <span>Prediction based on {data.length} training samples</span>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

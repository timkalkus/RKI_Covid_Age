Incidence = false;
Difference = false;
AnalyzeData
ExportSetup('Corona_Absolut','PNG')
%%
Incidence = false;
Difference = true;
AnalyzeData
ExportSetup('Corona_Absolut_diff','PNG')
%%
Incidence = true;
Difference = false;
AnalyzeData
ExportSetup('Corona_Incidence','PNG')
%%
Incidence = true;
Difference = true;
AnalyzeData
ExportSetup('Corona_Incidence_diff','PNG')
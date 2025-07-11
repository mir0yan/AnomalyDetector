%% This is an -*- erlang -*- file.
%%
%% %CopyrightBegin%
%%
%% Copyright Ericsson AB 2006-2016. All Rights Reserved.
%%
%% Licensed under the Apache License, Version 2.0 (the "License");
%% you may not use this file except in compliance with the License.
%% You may obtain a copy of the License at
%%
%%     http://www.apache.org/licenses/LICENSE-2.0
%%
%% Unless required by applicable law or agreed to in writing, software
%% distributed under the License is distributed on an "AS IS" BASIS,
%% WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
%% See the License for the specific language governing permissions and
%% limitations under the License.
%%
%% %CopyrightEnd%
%%

{application, dialyzer,
 [{description, "DIscrepancy AnaLYZer of ERlang programs, version 3.0.2"},
  {vsn, "3.0.2"},
  {modules, [dialyzer,
	     dialyzer_analysis_callgraph,
	     dialyzer_behaviours,
	     dialyzer_callgraph,
	     dialyzer_cl,
	     dialyzer_cl_parse,
	     dialyzer_codeserver,
	     dialyzer_contracts,
	     dialyzer_coordinator,
	     dialyzer_dataflow,
	     dialyzer_dep,
	     dialyzer_explanation,
	     dialyzer_gui_wx,
	     dialyzer_options,
	     dialyzer_plt,
	     dialyzer_race_data_server,
	     dialyzer_races,
	     dialyzer_succ_typings,
	     dialyzer_typesig,
	     dialyzer_utils,
             dialyzer_timing,
             dialyzer_worker]},
  {registered, []},
  {applications, [compiler, hipe, kernel, stdlib, wx]},
  {env, []},
  {runtime_dependencies, ["wx-1.2","syntax_tools-2.0","stdlib-3.0",
			  "kernel-5.0","hipe-3.15.1","erts-8.0",
			  "compiler-7.0"]}]}.

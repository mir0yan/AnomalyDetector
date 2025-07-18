%%
%% %CopyrightBegin%
%% 
%% Copyright Ericsson AB 1997-2015. All Rights Reserved.
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
{application, debugger,
 [{description, "Debugger"},
  {vsn, "4.2.1"},
  {modules, [
	     dbg_debugged,
	     dbg_icmd,
	     dbg_idb,
	     dbg_ieval,
	     dbg_iload,
	     dbg_iserver,
	     dbg_istk,
	     dbg_wx_break,
	     dbg_wx_break_win,
	     dbg_wx_code,
	     dbg_wx_filedialog_win,
	     dbg_wx_interpret,
	     dbg_wx_mon,
	     dbg_wx_mon_win,
	     dbg_wx_settings,
	     dbg_wx_src_view,
	     dbg_wx_trace,
	     dbg_wx_trace_win,
	     dbg_wx_view,
	     dbg_wx_win,
	     dbg_wx_winman,
	     debugger,
	     i,
	     int
	    ]},
  {registered, [dbg_iserver, dbg_wx_mon, dbg_wx_winman]},
  {applications, [kernel, stdlib]},
  {runtime_dependencies, ["wx-1.2","stdlib-2.5","kernel-3.0","erts-6.0",
			  "compiler-5.0"]}]}.

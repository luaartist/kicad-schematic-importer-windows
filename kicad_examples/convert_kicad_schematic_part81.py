# Warning: Large block split
<div id="LC19" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-s1>script_dir</span> <span class=pl-c1>=</span> <span class=pl-s1>os</span>.<span class=pl-c1>path</span>.<span class=pl-c1>dirname</span>(<span class=pl-s1>os</span>.<span class=pl-c1>path</span>.<span class=pl-c1>abspath</span>(<span class=pl-s1>__file__</span>))</div>
<div id="LC20" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-s1>exports_dir</span> <span class=pl-c1>=</span> <span class=pl-s1>os</span>.<span class=pl-c1>path</span>.<span class=pl-c1>join</span>(<span class=pl-s1>script_dir</span>, <span class=pl-s>&#39;output&#39;</span>)</div>
<div id="LC21" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">
</div>
<div id="LC22" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-c># Make sure that modules can be imported</span></div>
<div id="LC23" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-s1>sys</span>.<span class=pl-c1>path</span>.<span class=pl-c1>append</span>(<span class=pl-s1>script_dir</span>)</div>
<div id="LC24" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">
</div>
<div id="LC25" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-k>from</span> <span class=pl-s1>libs</span>.<span class=pl-s1>export_util</span> <span class=pl-k>import</span> (</div>
<div id="LC26" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">    <span class=pl-v>PopenContext</span>,</div>
<div id="LC27" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">    <span class=pl-s1>xdotool</span>,</div>
<div id="LC28" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">    <span class=pl-s1>wait_for_window</span>,</div>
<div id="LC29" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">)</div>
<div id="LC30" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">
</div>
<div id="LC31" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">
</div>
<div id="LC32" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-k>def</span> <span class=pl-en>usage</span>():</div>
<div id="LC33" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">    <span class=pl-en>print</span>(<span class=pl-s>&quot;Pass the name of the file to be converted to this script as an argument.&quot;</span>)</div>
<div id="LC34" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">    <span class=pl-en>print</span>(<span class=pl-s>&quot;./convert_kicad_schematic.py input/FILE_TO_EXPORT.sch&quot;</span>)</div>
# Warning: Large block split
<div id="LC35" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">
</div>
<div id="LC36" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div ">
</div>
<div id="LC37" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div "><span class=pl-k>def</span> <span class=pl-en>convertFile</span>(<span class=pl-s1>args</span>):</div>
<div id="LC38" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">    <span class=pl-s1>input_file</span> <span class=pl-c1>=</span> <span class=pl-s1>args</span>.<span class=pl-c1>in_spec</span></div>
<div id="LC39" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">
</div>
<div id="LC40" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">    <span class=pl-k>with</span> <span class=pl-en>PopenContext</span>([<span class=pl-s>&#39;eeschema&#39;</span>, <span class=pl-s1>input_file</span>], <span class=pl-s1>close_fds</span><span class=pl-c1>=</span><span class=pl-c1>True</span>) <span class=pl-k>as</span> <span class=pl-s1>eeschema_proc</span>:</div>
<div id="LC41" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">        <span class=pl-en>wait_for_window</span>(<span class=pl-s>&#39;eeschema&#39;</span>, <span class=pl-s>&#39;kicad_to_svg_converter&#39;</span>)</div>
<div id="LC42" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">
</div>
<div id="LC43" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">        <span class=pl-s1>time</span>.<span class=pl-c1>sleep</span>(<span class=pl-c1>5</span>)</div>
<div id="LC44" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">
</div>
<div id="LC45" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">        <span class=pl-en>xdotool</span>([<span class=pl-s>&#39;search&#39;</span>, <span class=pl-s>&#39;--name&#39;</span>, <span class=pl-s>&#39;kicad_to_svg_converter&#39;</span>, <span class=pl-s>&#39;windowfocus&#39;</span>])</div>
<div id="LC46" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">
</div>
<div id="LC47" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">        <span class=pl-en>xdotool</span>([<span class=pl-s>&#39;key&#39;</span>, <span class=pl-s>&#39;alt+f&#39;</span>])</div>
<div id="LC48" class="react-code-text react-code-line-contents-no-virtualization react-file-line html-div child-of-line-36 ">        <span class=pl-en>xdotool</span>([<span class=pl-s>&#39;key&#39;</span>, <span class=pl-s>&#39;p&#39;</span>])</div>